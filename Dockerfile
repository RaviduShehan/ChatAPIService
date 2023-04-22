FROM python:buster
WORKDIR /ChatApp
COPY requirements.txt .
COPY src/serviceAccountKey.json .
RUN pip install -r requirements.txt

COPY src src
# Set environment variables for Firestore connection
RUN pip install google-cloud-firestore
RUN pip install firebase-admin

EXPOSE 5001
ENTRYPOINT ["python", "./src/chat.py"]