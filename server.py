from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def webhook():
    return "Solo envie este msg si el bot no responde!\n [MENSAJE DE ACTIVACION]", 200

app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 10000)))