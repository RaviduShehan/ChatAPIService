FROM python:buster
WORKDIR /ChatApp
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src src
# Set environment variables for database connection
ENV DB_HOST="127.0.0.1"
ENV DB_NAME="rapalk"
ENV DB_USER="rapalk"
ENV DB_PASSWORD="971051213vGOT@"
RUN pip install mysql-connector-python

EXPOSE 5001
ENTRYPOINT ["python", "./src/chat.py"]