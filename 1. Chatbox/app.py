from flask import Flask, render_template, request
from Chatbot_camping import chat_bot

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["user_input"]
    response = chat_bot(user_input)
    return render_template("chat.html", user_input=user_input, response=response)

if __name__ == "__main__":
    app.run(debug=True)

