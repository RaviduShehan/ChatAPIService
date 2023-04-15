FROM python:3.8-slim-buster

# Install MySQL server
RUN apt-get update && \
    apt-get install -y mysql-server && \
    rm -rf /var/lib/apt/lists/*

# Start MySQL service and create a database and user
RUN service mysql start && \
    mysql -e "CREATE DATABASE mydb;" && \
    mysql -e "CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';" && \
    mysql -e "GRANT ALL PRIVILEGES ON mydb.* TO 'myuser'@'localhost';" && \
    mysql -e "FLUSH PRIVILEGES;"

# Copy and run the SQL script to populate the database
COPY init.sql /docker-entrypoint-initdb.d/init.sql

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app

# Expose the application port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
