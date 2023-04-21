FROM python:buster
WORKDIR /ChatApp
COPY requirements.txt .
COPY src/serviceAccountKey.json .
COPY tests/test_chat.py .
RUN pip install -r requirements.txt

COPY src src
COPY tests tests
# Set environment variables for Firestore connection
ENV GOOGLE_APPLICATION_CREDENTIALS="./serviceAccountKey.json"
RUN pip install google-cloud-firestore
RUN pip install firebase-admin

EXPOSE 5001
ENTRYPOINT ["python", "./src/chat.py"]