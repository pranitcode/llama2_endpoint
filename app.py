from flask import Flask, request, jsonify
import replicate
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/app/summarize": {"origins": "https://testaii.netlify.app"}})
@app.route('/app/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        if 'text' not in data:
            return jsonify({'error': 'No text provided in request'}), 400

        prompt_text = data['text']

        # Call replicate.stream with the provided prompt
        response_text = ""
        for event in replicate.stream(
            "meta/llama-2-7b-chat",
            input={
                "debug": False,
                "top_k": -1,
                "top_p": 1,
                "prompt": prompt_text,
                "temperature": 0.75,
                "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
                "max_new_tokens": 800,
                "min_new_tokens": -1,
                "repetition_penalty": 1
            },
        ):
            response_text += str(event)

        # Return the response text as JSON
        return jsonify({'summary': response_text}), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred while summarizing text'}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
