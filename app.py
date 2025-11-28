from flask import Flask, request, jsonify
import openai
import os
from openai.types.chat import ChatCompletionMessageParam  # type-safe import

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Store conversation history in memory (per server run)
conversation_history: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": "You are VP StudyBot, a helpful and friendly AI assistant."}
]

@app.route("/answer", methods=["POST"])
def answer():
    data = request.get_json(force=True)
    question = data.get("question", "")

    # Add user message to history
    conversation_history.append({"role": "user", "content": question})

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            max_tokens=200
        )

        answer_text = (response.choices[0].message.content or "").strip()

        # Add assistant reply to history
        conversation_history.append({"role": "assistant", "content": answer_text})

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