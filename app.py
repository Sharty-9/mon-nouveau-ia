import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Initialisation du client avec votre clé
API_KEY = "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"
client = Groq(api_key=API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"error": "Message vide"}), 400

        # Appel à Groq avec le modèle Llama 3.1
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Tu es un assistant IA intelligent et amical."},
                {"role": "user", "content": user_message}
            ]
        )
        
        reponse = completion.choices[0].message.content
        return jsonify({"response": reponse})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Pour le test local sur Pydroid
    app.run(host='0.0.0.0', port=5000, debug=True)
