import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import resend
from twilio.rest import Client
from flask_cors import CORS

# --- 1. SETUP ---
load_dotenv()
app = Flask(__name__)
CORS(app)

# --- 2. CONFIGURE APIs ---
resend.api_key = os.getenv("RESEND_API_KEY")
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
twilio_client = Client(twilio_account_sid, twilio_auth_token)


# --- HOMEPAGE ROUTE ---
@app.route('/')
def home():
    """Serves the index.html file as the homepage."""
    return render_template('index.html')


# --- API ENDPOINT ---
@app.route('/notify', methods=['POST'])
def send_notification():
    """Handles the form submission."""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        message = data.get('message')

        if not all([name, email, phone, message]):
            return jsonify({"message": "Missing required fields."}), 400

        # Action 1: Send email
        print(f"Sending email to {email}...")
        # We now send from your own verified domain.
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": email,
            "subject": f"New form submission from {name}",
            "html": (
                f"<h1>New Website Message</h1>"
                f"<p><b>From:</b> {name} ({email})</p>"
                f"<p><b>Message:</b> {message}</p>"
            )
        })
        print("Email sent successfully.")

        # Action 2: Send SMS
        print(f"Sending SMS to {phone}...")
        twilio_client.messages.create(
            body=f'New form submission from {name}: "{message}"',
            from_=twilio_phone_number,
            to=phone
        )
        print("SMS sent successfully.")
        return jsonify({
            "message": "Success! Your notification has been sent."
        }), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"message": "An internal error occurred."}), 500


# --- RUN THE SERVER ---
if __name__ == '__main__':
    app.run(debug=True)
