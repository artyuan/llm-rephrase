FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else into the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8501

# Run streamlit app
CMD ["streamlit", "run", "app.py", "0.0.0.0", "--server.port=8501","--server.address=0.0.0.0"]