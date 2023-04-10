FROM python:buster
WORKDIR /ChatApp
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src src
EXPOSE 5001
ENTRYPOINT ["python", "./src/chat.py"]