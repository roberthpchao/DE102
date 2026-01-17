from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import random

app = Flask(__name__)

def generate_data(acc_id):
    data_list = []
    start_date = datetime(2025, 4, 1)
    for i in range(10): # Let's start with just 10 days to keep it simple
        date_str = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        data_list.append({
            "date": date_str,
            "revenue": round(random.uniform(100, 500), 2),
            "subscribers_total": random.randint(1000, 1100)
        })
    return data_list

@app.route('/v1/metrics')
def get_metrics():
    acc_id = request.args.get('account_id', 'Unknown')
    return jsonify({
        "account_info": {"id": acc_id},
        "data": generate_data(acc_id)
    })

if __name__ == '__main__':
    app.run(port=5000)