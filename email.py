import smtplib
from email.message import EmailMessage
import traceback

def send_error_email(error_message):
    # --- CONFIGURATION ---
    sender_email = "liambousada@gmail.com"
    receiver_email = "liambousada@gmail.com"
    app_password = "typs hxyt zyfw kpfs"  # Use the 16-char App Password
    
    msg = EmailMessage()
    msg.set_content(f"The scraper has crashed.\n\nERROR DETAILS:\n{error_message}")
    msg['Subject'] = " Heffel 🚨 Scraper Error Notification"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        print("Error email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")