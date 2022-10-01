from flask import Flask, render_template, request
from blockchain import *


app = Flask(__name__)

@app.route('/')
def handle_transaction():
    if request.method == "POST":
        sender = request.form.get('sender', '')
        receiver = request.form.get('receiver', '')
        amount = request.form.get('amount', '')
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)