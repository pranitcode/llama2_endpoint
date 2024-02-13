from flask import Flask, request, jsonify
import replicate
# from flask_cors import CORS
app = Flask(__name__)

# CORS(app, origins=['http://localhost:3000'])
@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    prompt_text = data['text']

    # Call replicate.stream with the provided prompt
    response_text = ""
    for event in replicate.stream(
        "meta/llama-2-7b-chat",
        input={
            "debug": False,
            "top_k": -1,
            "top_p": 1,
            "prompt": prompt_text + "in less words Summarize the provided text in 4 small bullet points Condense text into 4 concise bullet points",
            "temperature": 0.75,
            "system_prompt": "You are a helpful,Summarize the provided text in 4 bullet points",
            "max_new_tokens": 800,
            "min_new_tokens": -1,
            "repetition_penalty": 1
        },
    ):
        response_text += str(event)

    # Return the response text as JSON
    return jsonify({'summary': response_text})

# if __name__ == '__main__':
#     app.run(debug=True)
   