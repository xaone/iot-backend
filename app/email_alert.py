import os
from dotenv import load_dotenv
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

def process_base64_image(base64_string, distance):
    try:
        image_data = base64.b64decode(base64_string)

        with open("received_image.png", "wb") as img_file:
            img_file.write(image_data)
        
        print("Image processed successfully")
        send_email_with_attachment("received_image.png", distance)
        return True
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

def send_email_with_attachment(attachment_path, distance):
    try:
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        recipient_email = os.getenv("RECIPIENT_EMAIL")
        subject = "Alert on the IoT device!"
        body = f"Distance seen from the device: {distance}cm"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
            msg.attach(part)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls() 
            server.login(sender_email, sender_password)  
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
        
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")