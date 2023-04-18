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
# openai.api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key ="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"

# Initialize Firestore client with explicit project ID
project_id = "apiservices-384019"
db = firestore.Client(project=project_id)


@app.route('/chat')
def chat():
    # Save service name, status, and timestamp to Firestore
    service_ref = db.collection('Services').document('ChatService_Status')
    print("Service Started.....")
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

