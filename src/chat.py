# import os
# from datetime import datetime
# import mysql.connector
# from flask import Flask, request, jsonify
# import openai
#
# app = Flask(__name__)
#
# # Load OpenAI API key to API
# # secrets = openai_secret_manager.get_secret("openai", path="config/secrets.json") secrets["api_key"]
# openai.api_key = os.environ.get('OPENAI_API_KEY')
#
# # Database connection
# mydb = mysql.connector.connect(
#   host="127.0.0.1",
#   user="root",
#   password="971051213vGOT@",
#   database="rapalk"
# )
#
# mycursor = mydb.cursor()
#
# @app.route('/chat')
# def chat():
#     print("Service Started.....")
#     prompt = request.args.get('prompt')
#     if not prompt:
#         sql = "INSERT INTO api_service(service_name, status, executed_time) VALUES (%s, %s,%s)"
#         val = ("chatAPI", "Error: Prompt parameter is missing", datetime.now())
#         mycursor.execute(sql, val)
#         mydb.commit()
#         return jsonify(error="Prompt parameter is missing"), 400
#
#     try:
#         response = openai.Completion.create(
#             engine="davinci",
#             prompt=prompt,
#             max_tokens=100,
#             n=1,
#             stop=None,
#             temperature=0.5
#         )
#         # Store service status in database
#         sql = "INSERT INTO api_service(service_name, status, executed_time) VALUES (%s, %s,%s)"
#         val = ("chatAPI", "Success", datetime.now())
#         mycursor.execute(sql, val)
#         mydb.commit()
#         return jsonify(response=response.choices[0].text.strip())
#     except Exception as e:
#
#         sql = "INSERT INTO api_service(service_name, status, executed_time) VALUES (%s, %s,%s)"
#         val = ("chatAPI", "Error: Server error", datetime.now())
#         mycursor.execute(sql, val)
#         mydb.commit()
#         return jsonify(error=str(e)), 500

import os
import datetime

from flask import Flask, request, jsonify
import openai
from google.cloud import firestore



import firebase_admin
from firebase_admin import credentials




cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

# Load OpenAI API key to API
# secrets = openai_secret_manager.get_secret("openai", path="config/secrets.json") secrets["api_key"]
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Initialize Firestore client with explicit project ID
project_id = "apiservices-384019"
db = firestore.Client(project=project_id)


@app.route('/chat')
def chat():
    # Save service name, status, and timestamp to Firestore
    service_ref = db.collection('Services').document('ChatService_Status')
    print("Service Started.....")
    print(service_ref)
    prompt = request.args.get('prompt')
    if not prompt:
        service_ref.update({'status': 'error'})
        return jsonify(error="Prompt parameter is missing"), 400

    service_data = {
        'service_name': 'chat',
        'status': 'running',
        'timestamp': datetime.datetime.now()
    }
    service_ref.set(service_data)

    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5
        )
        return jsonify(response=response.choices[0].text.strip())
    except Exception as e:
        # Update service status to 'error' if an exception occurs
        service_ref.update({'status': 'error'})
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

