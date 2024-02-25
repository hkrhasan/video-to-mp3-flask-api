import smtplib, os, json
from email.message import EmailMessage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def notification(message):
  try:
    message = json.loads(message)
    mp3_fid = message['mp3_fid']
    sender_address = os.environ.get("SENDER_ADDRESS")
    sender_password = os.environ.get("SENDER_PASSWORD")
    receiver_address = message["username"]

    msg = EmailMessage()
    msg.set_content(f"mp3 file_id: {mp3_fid}.mp3 is now ready!")
    msg["Subject"] = "MP3 Download"
    msg["From"] = sender_address
    msg["To"] = receiver_address

    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(sender_address, sender_password)
    session.send_message(msg, sender_address, receiver_address)
    session.quit()
    logger.info("mail sent successfully for file: %s.mp3", mp3_fid)

  except Exception as err:
    logger.error(err)
    return err
    
