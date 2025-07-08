# Use official Python base image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy your local code to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir flask mysql-connector-python

# Expose the port Flask uses
EXPOSE 5001

# Run the app
CMD ["python", "flask_bank_app_mysql.py"]
