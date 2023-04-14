import os
from datetime import datetime
import mysql.connector
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Load OpenAI API key to API
# secrets = openai_secret_manager.get_secret("openai", path="config/secrets.json") secrets["api_key"]
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Database connection
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="971051213vGOT@",
  database="rapalk"
)
timestamp = datetime.now()
mycursor = mydb.cursor()

@app.route('/chat')
def chat():
    print("Service Started.....")
    prompt = request.args.get('prompt')
    if not prompt:
        sql = "INSERT INTO api_service(service_name, status, executed_time) VALUES (%s, %s,%s)"
        val = ("chatAPI", "Error", timestamp)
        mycursor.execute(sql, val)
        mydb.commit()
        return jsonify(error="Prompt parameter is missing"), 400

    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5
        )
        # Store service status in database
        sql = "INSERT INTO api_service(service_name, status, executed_time) VALUES (%s, %s,%s)"
        val = ("chatAPI", "Success", timestamp)
        mycursor.execute(sql, val)
        mydb.commit()
        return jsonify(response=response.choices[0].text.strip())
    except Exception as e:

        sql = "INSERT INTO api_service(service_name, status, executed_time) VALUES (%s, %s,%s)"
        val = ("chatAPI", "Error", timestamp)
        mycursor.execute(sql, val)
        mydb.commit()
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

