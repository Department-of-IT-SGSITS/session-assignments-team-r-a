import boto3
import json
from botocore.exceptions import NoCredentialsError

# Print a message to indicate the start of the function
print('Loading function')


def lambda_handler(event, context):

    # Initialize the Simple Email Service (SES) client in the specified AWS region
    ses = boto3.client('ses', region_name="eu-west-2")

    # Define sender and recipient email addresses
    sender_email = 'abc@gmail.com'
    recipent_email = 'def@gmail.com'

    # Compose email subject and message 
    subject = "Contact Form Submission "
    message = "Name"

    # Send email with SES
    response = ses.send_email(
        Source=sender_email,
        Destination={'ToAddresses': [recipent_email]},
        Message={'Subject': {'Data': subject}, 'Body': {'Text': {'Data': message}}}
    )
    print(response)

    return{
        'statusCode' : 200,
        'body' : json.dumps({ 'message': 'Email sent successfully!' })
    }
