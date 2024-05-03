from flask import Flask, request, jsonify, render_template
from monero.wallet import Wallet
from monero.daemon import Daemon
from monero.backends.jsonrpc import JSONRPCDaemon
from datetime import datetime
import random
import os

app = Flask(__name__)

daemon = Daemon(JSONRPCDaemon(host="moneronode.org", port=18081))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    daemon_info = daemon.info()
    block_height = daemon_info['height']  # Use key access for 'height'
    last_block_hash = daemon_info['top_block_hash']  # Use key access for 'top_block_hash'

    # Getting numbers from the frontend
    num1 = request.json.get('num1', 1)
    num2 = request.json.get('num2', 100)

    # Ensure num1 is less than num2
    if num1 > num2:
        num1, num2 = num2, num1

    # Seed random number generator with the block hash
    random.seed(last_block_hash)
    random_number = random.randint(num1, num2)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return jsonify({
        'current_time': current_time,
        'block_height': block_height,
        'block_hash': last_block_hash,
        'random_number': random_number,
        'timestamp': current_time
    })

port = int(os.getenv('PORT', 5000))  # Default to 5000 if PORT not set
app.run(host='0.0.0.0', port=port)
