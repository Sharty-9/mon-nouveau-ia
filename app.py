from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Utilise la variable d'environnement sur Render ou votre clé en local
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "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"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": user_input}]
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
