from flask import Flask, render_template, request, jsonify
import string
import json

app = Flask(__name__)

# ===============================
# STATE UNTUK KONFIRMASI EXIT
# ===============================
waiting_exit_confirmation = False

# ===============================
# DATASET CHATBOT
# ===============================
with open("dataset.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)


# ===============================
# PREPROCESSING
# ===============================
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

# ===============================
# CHATBOT LOGIC
# ===============================
def get_response(user_input):
    global waiting_exit_confirmation

    user_input = preprocess(user_input)

    # JIKA MENUNGGU KONFIRMASI EXIT
    if waiting_exit_confirmation:
        if user_input in ["ya", "iya", "y", "yes"]:
            waiting_exit_confirmation = False
            return "__EXIT__"
        elif user_input in ["tidak", "ga", "gak", "belum", "no"]:
            waiting_exit_confirmation = False
            return "Baik 😊 Silakan lanjutkan pertanyaan Anda seputar beasiswa UNPAM."
        else:
            return "Silakan jawab dengan 'ya' atau 'tidak'."

    # DETEKSI TERIMA KASIH
    if "terima kasih" in user_input or "makasih" in user_input:
        waiting_exit_confirmation = True
        return "Sama-sama 😊 Apakah Anda ingin mengakhiri percakapan? (ya / tidak)"

    # EXIT LANGSUNG
    if user_input in ["exit", "keluar", "selesai", "quit"]:
        return "__EXIT__"

    # LOGIC NORMAL
    for item in qa_data:
        for pattern in item["patterns"]:
            pattern = preprocess(pattern)
            if pattern in user_input or user_input in pattern:
                return item["response"]

    return "Maaf, saya belum memahami pertanyaan tersebut. Silakan tanyakan seputar beasiswa UNPAM."

# ===============================
# ROUTES
# ===============================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response = get_response(user_input)
    return jsonify({"response": response})

# ===============================
# RUN SERVER
# ===============================
# if __name__ == "__main__":
#     app.run(debug=True)
