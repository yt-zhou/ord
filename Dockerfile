# Use the official Python image.
FROM python:3.9-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements file and install dependencies.
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask and Streamlit apps into the container.
COPY flask_app /app/flask_app
COPY streamlit_app /app/streamlit_app

# Expose the ports for Flask (5000) and Streamlit (8501).
EXPOSE 5000 8501

# Set environment variables for Flask.
ENV FLASK_APP=/app/flask_app

# Start both Flask and Streamlit when the container launches.
CMD ["sh", "-c", "flask run --host=0.0.0.0 & streamlit run /app/streamlit_app/main.py --server.port 8501 --server.address 0.0.0.0"]
