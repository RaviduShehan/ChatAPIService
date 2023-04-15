FROM python:buster
WORKDIR /ChatApp

# Install mysql-connector-python
RUN pip install mysql-connector-python
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src src
# Set environment variables for database connection
ENV DB_HOST="127.0.0.1"
ENV DB_NAME="rapalk"
ENV DB_USER="rapalk"
ENV DB_PASSWORD="971051213vGOT@"
# Install mysql client
RUN apt-get update && apt-get install -y mysql-client

# Copy init.sql script to initialize the database
COPY init.sql .
# Start the mysql client and execute the init.sql script
RUN /usr/bin/mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p$DB_PASSWORD < init.sql
EXPOSE 5001
ENTRYPOINT ["python", "./src/chat.py"]




