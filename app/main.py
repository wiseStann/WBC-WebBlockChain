import re
from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify

from uuid import uuid4
from random import random

from block import Blockchain


app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()
_WBC = 0.0000000000


@app.route('/', methods=['GET'])
def start_page():
    return render_template('start_page.html', WBC=_WBC)

@app.route('/transactions/list', methods=['GET'])
def transaction_list():
    return render_template('transaction_list.html', list=blockchain.chain)

@app.route('/transactions/new', methods=['GET', 'POST'])
def handle_transaction():
    if request.method == 'GET':
        return redirect(url_for('start_page'))
    else:
        blockchain.trans_number -= 1
        required = ['sender', 'recipient', 'amount']
        if not all(k in request.form.keys() and len(request.form[k]) > 0 for k in required):
            return render_template('new_transaction.html', missing_values=True, transactions_numbers=blockchain.trans_number)
        else:
            blockchain.new_transaction(request.form['sender'], request.form['recipient'], request.form['amount'])

        if blockchain.trans_number > 0:
            print("Transactions left: ", blockchain.trans_number)
            return render_template('new_transaction.html', transactions_numbers=blockchain.trans_number)
        else:
            # We run the proof of work algorithm to get the next proof...
            last_block = blockchain.last_block
            proof = blockchain.proof_of_work(last_block)
            # Forge the new Block by adding it to the chain
            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(f"Block {last_block['index'] + 1}", proof, previous_hash)
            blockchain.trans_number = 0
            return redirect(url_for('start_page'))

@app.route('/WBC/mine', methods=['GET', 'POST'])
def mine_WBC():
    if request.method == 'GET':
        return render_template('mine.html')
    else:
        global _WBC
        _WBC += random() / 10
        blockchain.trans_number = int(request.form['transactions-number'])
        return render_template('new_transaction.html', transactions_number=blockchain.trans_number)

@app.route('/blockchain-clear')
def clear_blockchain():
    blockchain.clear_chain()
    return redirect(url_for('start_page'))


if __name__ == "__main__":
    app.run(debug=True)