from flask import Flask, request, jsonify
import openai_secret_manager
import openai

app = Flask(__name__)

# Load OpenAI API key
# secrets = openai_secret_manager.get_secret("openai", path="config/secrets.json") secrets["api_key"]
openai.api_key = "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"

@app.route('/chat')
def chat():
    print("server starting")
    prompt = request.args.get('prompt')
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )
    return jsonify({'response': response.choices[0].text.strip()})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)