from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load your API key securely from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/answer", methods=["POST"])
def answer():
    data = request.get_json(force=True)
    question = data.get("question", "")

    # Start a fresh conversation history for each request
    conversation_history = [
        {"role": "system", "content": "You are VP StudyBot, a helpful and friendly AI assistant."},
        {"role": "user", "content": question}
    ]

    try:
        # Call OpenAI with the fresh conversation
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            max_tokens=200
        )

        # Extract the assistant's reply
        answer_text = (response.choices[0].message.content or "").strip()

        return jsonify({
            "answer": answer_text,
            "suggestions": ["Ask me another topic", "Try a fun fact", "Need help with studies?"]
        })

    except Exception as e:
        return jsonify({
            "answer": "Oops, something went wrong while fetching the answer.",
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)