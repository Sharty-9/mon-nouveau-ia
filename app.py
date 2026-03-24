from flask import Flask, request, render_template_string, jsonify, session
from groq import Groq
import base64

app = Flask(__name__)
app.secret_key = "mael_pro_key"
client = Groq(api_key="VOTRE_CLE_GROQ")

# On utilise un modèle Vision pour comprendre les images
MODEL_VISION = "llama-3.2-11b-vision-preview"

@app.route("/")
def home():
    session['chat_history'] = []
    return render_template_string(HTML_PAGE)

@app.route("/get_response", methods=["POST"])
def get_response():
    user_msg = request.form.get("msg")
    image_data = request.form.get("image") # Image en base64
    
    chat_history = session.get('chat_history', [])
    
    # Construction du contenu du message (Texte + Optionnellement Image)
    content = [{"type": "text", "text": user_msg or "Que vois-tu sur cette image ?"}]
    
    if image_data:
        content.append({
            "type": "image_url",
            "image_url": {"url": image_data} # Format: data:image/jpeg;base64,...
        })

    chat_history.append({"role": "user", "content": content})

    try:
        completion = client.chat.completions.create(
            model=MODEL_VISION,
            messages=chat_history
        )
        bot_reply = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": bot_reply})
        session['chat_history'] = chat_history
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Erreur : {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)

