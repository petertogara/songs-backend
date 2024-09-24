FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /app

# Copy only the requirements file first for better caching
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app folder into the container
COPY . .

# Copy SSL certificates
COPY cert.pem /etc/nginx/certs/cert.pem
COPY key.pem /etc/nginx/certs/key.pem

# Run the application
CMD ["gunicorn", "--certfile=/etc/nginx/certs/cert.pem", "--keyfile=/etc/nginx/certs/key.pem", "-w", "4", "-b", "0.0.0.0:5001", "manage:app"]



