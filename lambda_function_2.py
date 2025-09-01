import boto3
import json
from botocore.exceptions import NoCredentialsError

# Print a message to indicate the start of the function
print('Loading function')

# Initialize the Simple Email Service (SES) client in the specified AWS region
ses = boto3.client('ses', region_name="eu-west-2")

def lambda_handler(event, context):
    
    try:
        # Parse the incoming JSON data from the 'event' parameter
        body = json.loads(event['body'])

        # Define sender and recipient email addresses
        sender_email = 'abc@gmail.com'
        recipent_email = 'def@gmail.com'

        # Compose email subject and message using data from the contact form
        subject = f"Contact Form Submission - {body['name']}"
        message = f"Name: {body['name']}\nEmail: {body['email']}\nMessage: {body['message']}"

        # Send email with SES, specifying the sender, recipient, subject, and message
        response = ses.send_email(
            Source=sender_email,
            Destination={'ToAddresses': [recipent_email]},
            Message={'Subject': {'Data': subject}, 'Body': {'Text': {'Data': message}}}
        )

        # Return a success response with a status code of 200 and a success message
        return{
            'statusCode' : 200,
            'body' : json.dumps({ 'message': 'Email sent successfully!' })
        }
    except Exception as e:
        # In case of any exceptions or errors, return a failure response with a status code of 500
        # and an error message
        return{
            'statusCode': 500,
            'body': json.dumps({ 'message' : 'Email sending failed!' })
        }
        