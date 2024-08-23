from flask import Flask, jsonify, request
from .models import get_mysql_connection, get_local_mongo_connection, get_master_mongo_connection

app = Flask(__name__)

# MySQL: Count of messages sent per campaign (inbound = 0)
@app.route('/smslogs/messages-sent', methods=['GET'])
def get_messages_sent():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT campaignId, COUNT(*) as message_count FROM SmsLog WHERE inbound = 0 GROUP BY campaignId"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# MySQL: Count of responses per campaign (inbound = 1)
@app.route('/smslogs/responses', methods=['GET'])
def get_responses():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT campaignId, COUNT(*) as response_count FROM SmsLog WHERE inbound = 1 GROUP BY campaignId"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# MongoDB Local: Count of members opted in per campaign
@app.route('/members/opted-in', methods=['GET'])
def get_opted_in_members():
    db = get_local_mongo_connection()
    members = db['members']
    pipeline = [
        {"$unwind": "$anchorDates"},
        {"$match": {"anchorDates.OPT_IN": {"$exists": True}}},
        {"$group": {"_id": "$anchorDates.campId", "opted_in_count": {"$sum": 1}}}
    ]
    data = list(members.aggregate(pipeline))
    return jsonify(data)

# MongoDB Master: Active vs suspended campaigns per clientName
@app.route('/campaigns/status', methods=['GET'])
def get_campaign_status():
    db = get_master_mongo_connection()
    campaigns = db['masterCampaignMaps']
    pipeline = [
        {"$group": {"_id": {"clientName": "$clientName", "status": "$suspended"}, "count": {"$sum": 1}}}
    ]
    data = list(campaigns.aggregate(pipeline))
    return jsonify(data)

# MongoDB Master: Campaigns created per year per clientName
@app.route('/campaigns/yearly', methods=['GET'])
def get_campaigns_per_year():
    db = get_master_mongo_connection()
    campaigns = db['masterCampaignMaps']
    pipeline = [
        {"$group": {"_id": {"clientName": "$clientName", "year": {"$year": "$createdAt"}}, "count": {"$sum": 1}}}
    ]
    data = list(campaigns.aggregate(pipeline))
    return jsonify(data)


@app.route('/campaigns/abvh', methods=['GET'])
def get_abvh_campaigns():
    db = get_master_mongo_connection()
    campaigns = db['masterCampaignMaps']
    
    # MongoDB query to filter by clientName and project required fields
    results = campaigns.find(
        {"clientName": "Aetna Better Health of Virginia"},
        {
            "clientName": 1,
            "campaignName": 1,
            "sources.SMS": 1,
            "opClientId": 1,
            "opCampaignId": 1,
            "campaignCates": {"$slice": 1},  # Get the first element of campaignCates array
            "createdAt": 1,
            "active": 1,
            "suspended": 1
        }
    )
    
    # Convert results to a list of dictionaries
    campaign_list = []
    for campaign in results:
        campaign_dict = {
            "clientName": campaign.get("clientName"),
            "campaignName": campaign.get("campaignName"),
            "smsSource": campaign.get("sources", {}).get("SMS"),
            "opClientId": campaign.get("opClientId"),
            "opCampaignId": campaign.get("opCampaignId"),
            "firstCampaignCate": campaign.get("campaignCates", [None])[0],
            "createdAt": campaign.get("createdAt"),
            "active": campaign.get("active"),
            "suspended": campaign.get("suspended"),
        }
        campaign_list.append(campaign_dict)

    return jsonify(campaign_list)


@app.route('/campaigns/aetva', methods=['GET'])
def get_aetva_campaign_ids():
    # Connect to the local MongoDB database
    db = get_local_mongo_connection()
    collection = db['campaigns']  # Assuming the collection name is 'campaigns'

    # Define the query to find campaigns with names starting with "Aetva"
    query = {"name":"Vaya22Q2OptIn"}

    # Define the fields to extract
    projection = {
        "_id": 1,
        "name": 1
    }

    # Query the collection
    campaigns = list(collection.find({"name":{"$regex": "^Vaya"}},{"_id":1,"name":1}).limit(100))

    campaign_list = []
    for campaign in campaigns:
        campaign_dict = {
            "name": campaign.get("name"),
            "_id":str(campaign.get("_id"))
        }
        campaign_list.append(campaign_dict)

    print(campaign_list)
    # Convert ObjectId to string for _id
    # for campaign in campaigns:
    #    campaign["_id"] = str(campaign["_id"])

    # Return the results as JSON
    return jsonify(campaign_list)

@app.route('/members/aetva-campaigns', methods=['GET'])
def get_member_counts_for_aetva_campaigns():
    # Connect to the local MongoDB database
    db = get_local_mongo_connection()
    members_collection = db['members']

    # Get campaign IDs from the first function
    campaign_ids = get_aetva_campaign_ids().get_json()

    # Extract the campaign IDs as a list
    campaign_id_list = [campaign['_id'] for campaign in campaign_ids]

    # Build the query to match members with specific anchorDates
    anchor_date_queries = [{"anchorDates." + campaign_id + ":OPT_IN": {"$exists": True}} for campaign_id in campaign_id_list]

    # If there are no campaign IDs, return an empty result
    if not anchor_date_queries:
        return jsonify([])

    # Combine queries using $or to find any member matching at least one campId:OPT_IN
    query = {"$or": anchor_date_queries}

    # Query the members collection
    members = members_collection.find(query)

    # Initialize a dictionary to store the count of members per campaign
    member_counts = {campaign_id: 0 for campaign_id in campaign_id_list}

    # Count members per campaign
    for member in members:
        for campaign_id in campaign_id_list:
            opt_in_key = f"{campaign_id}:OPT_IN"
            if opt_in_key in member.get("anchorDates", {}):
                member_counts[campaign_id] += 1

    # Convert the dictionary to a list of dictionaries for JSON response
    result = [{"campaignId": campaign_id, "memberCount": count} for campaign_id, count in member_counts.items()]

    # Return the results as JSON
    return jsonify(result)

@app.route('/campaigns/active', methods=['GET'])
def get_active_campaigns_abvh():
    # Connect to the master MongoDB database
    db = get_master_mongo_connection()
    collection = db['masterCampaignMaps']

    # Query to find active campaigns for clientName "ABVH"
    query = {"clientName": "Vaya Health", "active": True}

    # Count the number of active campaigns
    active_campaign_count = collection.count_documents(query)

    # Return the count as JSON
    return jsonify({"active_campaigns": active_campaign_count})

# Fetch total messages sent by campaign
@app.route('/campaigns/total-messages', methods=['GET'])
def get_total_messages():
    campaign_ids = request.args.getlist('campaign_ids[]')
    
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT COUNT(*)
        FROM SmsLog
        WHERE campaignId IN (%s)
        AND inbound != 1
    """ % ','.join(['%s'] * len(campaign_ids))
    
    cursor.execute(query, tuple(campaign_ids))
    total_messages = cursor.fetchone()[0]

    print(total_messages)
    
    cursor.close()
    conn.close()
    
    return jsonify({"total_messages": total_messages})

# Fetch unique targets that replied back
@app.route('/campaigns/reply-rate', methods=['GET'])
def get_reply_rate():
    campaign_ids = request.args.getlist('campaign_ids[]')
    
    conn = get_mysql_connection()
    cursor = conn.cursor()
    
    query_unique_targets = """
        SELECT COUNT(DISTINCT target)
        FROM SmsLog
        WHERE campaignId IN (%s)
        AND inbound != 1
    """ % ','.join(['%s'] * len(campaign_ids))
    
    cursor.execute(query_unique_targets, tuple(campaign_ids))
    total_unique_targets = cursor.fetchone()[0]

    print(total_unique_targets)

    query_replies = """
        SELECT COUNT(DISTINCT source)
        FROM SmsLog
        WHERE campaignId IN (%s)
        AND inbound = 1
    """ % ','.join(['%s'] * len(campaign_ids))
    
    cursor.execute(query_replies, tuple(campaign_ids))
    replied_targets = cursor.fetchone()[0]

    print(replied_targets)
    
    cursor.close()
    conn.close()
    
    return jsonify({
        "total_unique_targets": total_unique_targets,
        "replied_targets": replied_targets
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
