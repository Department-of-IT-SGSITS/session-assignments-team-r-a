import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import resend
from twilio.rest import Client
from flask_cors import CORS
from datetime import datetime

# MongoDB logging 
try:
    from pymongo import MongoClient
    mongo_enabled = True
except ImportError:
    mongo_enabled = False

# SETUP 
load_dotenv()
app = Flask(__name__)
CORS(app)

# CONFIGURE APIs 
resend.api_key = os.getenv("RESEND_API_KEY")

twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

twilio_client = Client(twilio_account_sid, twilio_auth_token)

# MONGODB CONNECTION 
if mongo_enabled and os.getenv("MONGO_URI"):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["serverless_email_clone"]
    logs_collection = db["notifications"]
else:
    logs_collection = None


# HOMEPAGE ROUTE 
@app.route('/')
def home():
    """Serves the index.html file as the homepage."""
    return render_template('index.html')


# API ENDPOINT 
@app.route('/notify', methods=['POST'])
def send_notification():
    """Handles email + SMS + attachments."""
    try:
        name = request.form.get('name')
        to_field = request.form.get('email')  
        cc_field = request.form.get('cc')
        bcc_field = request.form.get('bcc')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Validation 
        if not all([name, to_field, subject, message]):
            return jsonify({"message": "Missing required fields."}), 400

        # Split comma-separated emails into lists
        to_list = [email.strip() for email in to_field.split(",") if email.strip()]
        cc_list = [email.strip() for email in cc_field.split(",")] if cc_field else []
        bcc_list = [email.strip() for email in bcc_field.split(",")] if bcc_field else []

        # Handle Attachments 
        attachments = []
        uploaded_files = request.files.getlist("attachments")
        for file in uploaded_files:
            attachments.append({
                "filename": file.filename,
                "content": file.read(),
            })

        # Send Email via Resend 
        print(f"Sending email to: {to_list}, cc: {cc_list}, bcc: {bcc_list}")
        resend.Emails.send({
            "from": "onboarding@resend.dev", 
            "to": to_list,
            "cc": cc_list,
            "bcc": bcc_list,
            "subject": subject,
            "html": (
                f"<h2>Message from {name}</h2>"
                f"<p>{message}</p>"
                f"<hr><p><i>Sent via Serverless Email Clone</i></p>"
            ),
            "attachments": attachments if attachments else None
        })
        print("Email sent successfully!")

        
        if phone:
            print(f"Sending SMS to {phone}...")
            twilio_client.messages.create(
                body=f'New message from {name}: "{message}"',
                from_=twilio_phone_number,
                to=phone
            )
            print("SMS sent successfully!")

        # Log to MongoDB 
        if logs_collection:
            logs_collection.insert_one({
                "name": name,
                "to": to_list,
                "cc": cc_list,
                "bcc": bcc_list,
                "subject": subject,
                "message": message,
                "attachments": [f.filename for f in uploaded_files],
                "phone": phone,
                "timestamp": datetime.now().isoformat()
            })

        return jsonify({"message": "Success! Your email and SMS have been sent."}), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"message": f"An internal error occurred: {e}"}), 500


#  RUN SERVER 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
