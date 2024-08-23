# Orchestrated Reporting Dashboard

This project includes two components:
- Flask Application: Backend logic.
- Streamlit Application: Data dashboard.

## Setup

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
   pip install -r flask_app/requirements.txt
   pip install -r streamlit_app/requirements.txt
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

