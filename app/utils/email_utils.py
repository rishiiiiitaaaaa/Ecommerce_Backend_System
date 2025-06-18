import smtplib #Imports Python's built-in module for sending emails using the SMTP (Simple Mail Transfer Protocol).
from email.mime.text import MIMEText # a class to create plain text email messages
from app.core.logger import logger
def send_reset_email(to_email, token):
    # Specifies Gmail’s SMTP server and port.
    smtp_server = "smtp.gmail.com" 
    smtp_port = 587
    from_email = "ecommercebackenddb@gmail.com"
    from_password = "ijizicedpltgliwk"  
    try:
       # Connect and Authenticate with SMTP Server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()  
        server.starttls()
        server.ehlo()  #identifies the client to the server 
        server.login(from_email, from_password)

        reset_link = f"http://localhost:3000/reset-password?token={token}" # includes the token in the query string.
        subject = "Password Reset"
        body = f"Click the following link to reset your password: {reset_link}"
        message = MIMEText(body, "plain")
        message["Subject"] = subject
        message["From"] = from_email
        message["To"] = to_email

        server.sendmail(from_email, to_email, message.as_string())
        server.quit()
        logger.info("Reset email sent successfully.")
    except Exception as e:
        logger.exception("Failed to send email") 
        raise
