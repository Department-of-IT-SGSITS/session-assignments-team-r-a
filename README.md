# SERVERLESS CONTACT FORM

## PROMPT
Build a serverless contact form using AWS Lambda, Amazon API Gateway, and Amazon Simple Email Service (SES). When users submit the form, the Lambda function will trigger and send the form data to your email using SES.

## USE CASE FOR EACH SERVICE
- **SES**: For delivering and receiving emails.
- **Lambda**: Handle form submissions.
- **S3**: Store the HTML form.
- **API Gateway**: Expose Lambda securely on the internet.

## Architecture Diagram

![Serverless Contact Form Architecture](images/architecture.png)


## STEPS
1. **Configure SES to send emails to yourself**
    - Navigate to SES in the AWS Management Console.
    - **Create SMTP Credentials**
        - Click **SMTP Credentials**.
        - Create a new user (under SMTP).
        - Retrieve SMTP credentials by downloading the `.csv` file or by copying the credentials and storing them in a file.
        - Click **Return to SES Console**.
    - **Verify Email Identity**
        - Click **Verified Identities**.
        - Click **Create new identity**.
        - Set identity type to **Email**.
        - Enter your email address.
        - Click **Create Identity**.
        - To verify ownership of the identity, check the inbox of the email you entered.
        - Click the link in the email to verify the address.

2. **Set up Lambda function to respond to API Gateway triggers**
    - Navigate to Lambda in the AWS Management Console.
        - Click **Create function**.
        - Select **Use a blueprint**.
        - Choose **Microservices that interact with a DDB Table**.
        - Enter `ContactFormFunction` as the Function Name.
        - For Execution role, select **Create a new role from AWS policy templates**.
        - Enter `mySESContactFormRole` as the Role name.
        - Select **Simple microservices permissions** as Policy Templates.
        - Scroll down to API Gateway Triggers:
            - Choose **Create new API**.
            - Select **Open** as Security.
            - Expand Additional Settings:
                - Enter `ContactFormFunction-API` as API Name.
                - Enter `default` as Deployment stage.
        - Click **Create Function**.

3. **Configure IAM Role to send email via SES**
    - Navigate to IAM in the AWS Management Console.
        - **Create Policy**:
            - Click **Policies** → **Create Policy**.
            - Search for **SES** under *Select a Service*.
            - Specify Actions Allowed:
                - `SendEmail`
                - `SendRawEmail`
            - Specify **All Resources**.
            - Click **Next**.
            - Review and Create:
                - Enter `contact-form-send-email-ses-policy` as the policy name.
                - (Optional) Description: `allow_role_sendEmail_and_sendRawEmail_with_SES`.
                - Click **Create policy**.
        - **Attach Policy to IAM Role**:
            - Navigate to **Roles** and search for `mySESContactFormRole`.
            - Click the role.
            - Scroll to **Permissions**.
            - Click **Add permissions** → **Attach policies**.
            - In *Other permission policies*, search for `contact-form-send-email-ses-policy`.
            - Select it and click **Add permissions**.

4. **Send email with SES from Lambda function**
    - Navigate to **Lambda** in the AWS Management Console.
    - Click the `ContactFormFunction`.
    - Add the code to send email using SES.

5. **Test endpoint on API Gateway**.

6. **Enable CORS and Deploy API**.

7. **Create S3 bucket** and upload the HTML contact form.

8. **Test: Submit the form and verify email delivery**.

---

### CONTRIBUTORS
Rohit  
Adarsh
