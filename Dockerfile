FROM python:buster
WORKDIR /ChatApp
COPY requirements.txt .
COPY src/serviceAccountKey.json .
RUN pip install -r requirements.txt

COPY src src
# Set environment variables for Firestore connection
ENV GOOGLE_APPLICATION_CREDENTIALS="./serviceAccountKey.json"
RUN pip install google-cloud-firestore

EXPOSE 5001
ENTRYPOINT ["python", "./src/chat.py"]