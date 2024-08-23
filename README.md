# Orchestrated Reporting Dashboard
## Background
This project is created during the 2024 mPulse Innovation Day. It is designed to enhance data-driven decision-making by providing powerful and user-friendly data visualization tools

### For mPulse:
- Reduce turnaround time for basic data pull and analytics requests.
- Provide clear and engaging visuals for client meetings, presentations, and demos.
- Explore new upsell opportunities through advanced data insights.

### For Clients:
- Streamlined processes for quicker access to critical insights.
- Empower clients with intuitive tools to visualize and act on their data effectively.

## Setup
This project includes two components:
- Flask Application: Backend logic.
- Streamlit Application: Data dashboard.

1. **Fork and Clone the Repository**
```bash
    git clone <forked-repository-url>
    cd <repository-directory>
```

2. **Create and Activate Virtual Environment**
```bash
   python -m venv venv
   source venv/bin/activate  # Use `venv\Scripts\activate` on Windows
```

3. **Install Dependencies**
```bash
   pip install -r requirements.txt
```
## Running the Applications

### Flask

1. Navigate to the `flask_app` directory:
```bash
   cd flask_app
```
2. Set the Flask environment variable and run the server:
```bash
   export FLASK_APP=routes.py
   flask run
```
   The Flask app will be accessible at http://localhost:5000.

### Streamlit

1. Open a new terminal and navigate to the `streamlit_app` directory:
```bash
   cd streamlit_app
```
2. Run the Streamlit app:
```bash
   streamlit run main.py --server.port 8501 --server.address 0.0.0.0
```
   The Streamlit app will be accessible at http://localhost:8501.

## Notes

- Ensure the virtual environment is activated when running the applications.
- Adjust configuration as needed based on your environment.

