FROM python:3.12.0a7-alpine3.17
WORKDIR /chatapiapp
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY Src Src
EXPOSE 5001
ENTRYPOINT ["python", "./Src/chat.py"]