FROM python:buster
WORKDIR /ChatApp
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY serviceAccountKey.json .
COPY src src
# Set environment variables for Firestore connection
ENV GOOGLE_APPLICATION_CREDENTIALS="/ChatApp/serviceAccountKey.json"
RUN pip install google-cloud-firestore
RUN pip install firebase-admin

EXPOSE 5001
ENTRYPOINT ["python", "./src/chat.py"]