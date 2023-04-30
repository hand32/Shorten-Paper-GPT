# Base Image
FROM python:3.11-slim-buster

# Copy requirement file
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Working Directory
WORKDIR /app

# Execute script
ENTRYPOINT ["python", "-m", "shorten_paper"]