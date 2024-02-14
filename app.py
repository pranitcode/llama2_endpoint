from flask import Flask, request, jsonify
import replicate
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/app/summarize": {"origins": "https://testaii.netlify.app"}})

@app.route('/app/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        if data is None or 'text' not in data:
            return jsonify({'error': 'No text provided in request'}), 400
    
        prompt_text = data['text']
        prompt = "Summarize the following points in a point-by-point format: " + prompt_text
        prompt += " Do not use any information not provided for creating summary points."
        
        response_text = ""
        for event in replicate.stream(
            "meta/llama-2-7b-chat",
            input={
                "debug": False,
                "top_k": -1,
                "top_p": 1,
                "prompt": prompt,
                "temperature": 0.75,
                "system_prompt": "You are an incredibly helpful, respectful, and trustworthy assistant. Your expertise lies in your ability to skillfully summarize information with precision and clarity. Your proficiency as a summarizer is unmatched, making you an invaluable resource for anyone seeking concise and insightful summaries.",
                "max_new_tokens": 300,
                "min_new_tokens": -1,
                "repetition_penalty": 1
            },
        ):
            response_text += str(event)

        return jsonify({'summary': response_text}), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred while summarizing text'}), 500

if __name__ == '__main__':
    app.run(debug=True)
