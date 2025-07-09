# Use official Python base image
FROM python:3.9

# Set working directory inside container
WORKDIR /app

# Copy all app files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Streamlit app on container startup
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
