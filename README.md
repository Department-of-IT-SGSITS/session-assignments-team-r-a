# SERVERLESS CONTACT FORM

## PROMPT
Build a serverless contact form using AWS Lambda, Amazon API Gateway, and Amazon Simple Email Service (SES). When users submit the form, the Lambda function will trigger and send the form data to your email using SES.

## USE CASE FOR EACH SERVICE
- SES: For delivering and receiving emails.
- Lambda: Handle form submissions
- S3: Store HTML form
- API Gateway: ecpose Lambda securely on the internet. 

## ARCHITECTURE DIAGRAM

## STEPS
1. Configure SES to send emails to myself
    - Navigate to SES in the Management Console
    - Create SMTP Credentials
        - Click SMTP Credentials
        - Create User (under smtp)
        - Retrieve SMTP credentials by downloading .csv file or by copying the credentials and storing in a file.
        - Click "Return to SES Console".
    - Click Verified Identities
        - Click Create new identity
        - Set identity type to "email"
        - Enter email address
        - Click "Create Identity"
        - To verify ownership of the identity, check the inbox of the email you entered.
        - Click the link in the email to verify email address.
2. Set up Lambda function to respond to API Gateway triggers
    - Navigate to Lambda in the Management Console
        - Click Create function
        - Select "use a blueprint"
        - Choose "microservices that interacts with with a DDB Table".
        - Enter "ContactFormFunction" as Function Name.
        - For Execution role, select "Create a new role from AWS policy templates".
        - Enter "mySESContactFormRole" as Role name.
        - Select "Simple microservices permissions" as Policy Templates.
        - Scroll down to API Gateway Triggers
            - Choose Create new API
            - Select Open as Security
            - Expand Additional Settings
                - Enter "ContactFormFunction-API" as API Name
                - Enter "default" as Deployment stage
        - Create Function
3. Configure IAM Role to send email via SES
    - Navigate to Lambda in the Management Console
        - Create Policy
            - Click Policies
            - Click Create Policy
            - Search for "SES" under Select a Service
            - Specify Actions Allowed
                - SendEmail
                - SendRawEmail
            - Specify "All" Resources
            - Click Next
            - Review and Create
                - Enter "contact-form-send-email-ses-policy" as policy name
                - Enter "allow_role_sendEmail_and_sendRawEmail_with_SES" in Description (it is optional)
                - Create policy
        - Attach Policy to IAM Role
            - Click Policies
            - Search for "mySESContactFormRole"
            - Click it
            - - Scroll to "Permissions"
            - Click Add permissions
            - Select Attach policies
            - In "Other permission policies", search for "contact-form-send-email-ses-policy"
            - Select it
            - Click Add permissions
4. Send email with SES from Lambda function
    - Navigate to Lambda in the Management Console
    - Click the "myContactFormFunction"
5. Test endpoint on API Gateway
6. Enable CORS and Deploy API
7. Create S3 bucket
8. Test: Send an email


## RESULTS
https://www.youtube.com/watch?v=HKpb3AqL8FU
https://www.youtube.com/watch?v=2K73Rcx7sJ0