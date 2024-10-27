import hmac
import hashlib
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SECRET_KEY = '1234567890!@>$%'  

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Yonatan:yonatan123@localhost/payroll_info'
db = SQLAlchemy(app)

# Define the WebhookTransaction model
class WebhookTransaction(db.Model):
    id = db.Column(db.String, primary_key=True)
    amount = db.Column(db.Integer)
    currency = db.Column(db.String)
    created_at_time = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)
    cause = db.Column(db.String)
    full_name = db.Column(db.String)
    account_name = db.Column(db.String)
    invoice_url = db.Column(db.String)

# Function to verify the signature
def verify_signature(payload, received_signature, timestamp):
    tolerance = 300  # in seconds 
    current_time = int(time.time())
    if abs(current_time - timestamp) > tolerance:
        return False

    hmac_obj = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256)
    generated_signature = hmac_obj.hexdigest()
    return hmac.compare_digest(generated_signature, received_signature)

# Helper function to generate a test signature for local testing
def generate_test_signature(payload):
    hmac_obj = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256)
    return hmac_obj.hexdigest()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Prepare payload string by concatenating field values
    payload = ''.join([
        data['id'],
        str(data['amount']),
        data['currency'],
        str(data['created_at_time']),
        str(data['timestamp']),
        data['cause'],
        data['full_name'],
        data['account_name'],
        data['invoice_url']
    ])

    # Retrieve signature from header or generate for testing
    received_signature = request.headers.get('YAYA-SIGNATURE') or generate_test_signature(payload)
    print("Payload for HMAC:", payload)
    print("Received Signature:", received_signature)

    # Verify the signature
    if verify_signature(payload, received_signature, data['timestamp']):
        print("Valid Webhook Received:", data)
        
        transaction = WebhookTransaction(
            id=data['id'],
            amount=data['amount'],
            currency=data['currency'],
            created_at_time=data['created_at_time'],
            timestamp=data['timestamp'],
            cause=data['cause'],
            full_name=data['full_name'],
            account_name=data['account_name'],
            invoice_url=data['invoice_url']
        )
        db.session.add(transaction)
        db.session.commit()

        return jsonify({"status": "success"}), 200
    else:
        print("Invalid Webhook Signature")
        return jsonify({"error": "Invalid signature"}), 403

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(port=5000)
