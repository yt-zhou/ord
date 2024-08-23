from flask import Flask, jsonify
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
