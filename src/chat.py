
import datetime
import os

import prometheus_client
from flask import Flask, request, jsonify
import openai
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time

from requests import Response

_INF = float("inf")
graph = {}
graph['c'] = Counter('Python_request_operations_total', 'The total number of processed requests')
graph['h'] = Histogram('Python_request_duration_seconds','Histogram for the duration in seconds.', buckets=(1,2,5,6,10,_INF))


cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
database = 'Services'
app = Flask(__name__)

# Load OpenAI API ke to API
openai.api_key = os.environ.get('OPENAI_API_KEY')


# Initialize Firestore client with explicit project ID
project_id = "apiservices-384019"
db = firestore.Client(project=project_id)


@app.route('/')
def chat():
    start = time.time()
    graph['c'].inc()

    time.sleep(0.600)

    # Save service name, status, and timestamp to Firestore
    service_ref = db.collection(database).document('ChatService_Status')
    print("Service Started.....")
    service_data = {
        'service_name': 'Chat',
        'status': 'Starting',
        'timestamp': datetime.datetime.now()
    }
    service_ref.set(service_data)
    prompt = request.args.get('prompt')
    if not prompt:
        service_ref.update({'status': 'Empty Prompt'})
        return jsonify(error="Prompt parameter is missing"), 400
    end = time.time()
    graph['h'].observe(end - start)
    service_ref.update({'status': 'Running'})
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
        service_ref.update({'status': 'Error'})
        return jsonify(error=str(e)), 500

@app.route('/metrics', methods=['POST'])
def request_count():
    res = []
    for k, v in graph.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

