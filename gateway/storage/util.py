import pika, json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload(f, fs, channel, access):
  # Parameter validation
  if not (f and fs and channel and access):
    logger.error("Missing required parameters.")
    return "internal server error", 500
  

  try:
    # Attemp to upload the file
    fid = fs.put(f)
    logger.info("File uploaded successfully: %s", fid)
  except Exception as err:
    logger.error("Error in file putting: %s", err)
    return "internal server error", 500
  

  message = {
    "video_fid": str(fid),
    "mp3_fid": None,
    "username": access["username"]
  }

  try:

    logger.info("Preparing to queue message: %s", message)

    channel.basic_publish(
      exchange="",
      routing_key="video",
      body=json.dumps(message),
      properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
      ),
    )
    logger.info("Message queued successfully. ")
  except Exception as err:
    logger.error("Error on queuing file: %s", err)
    # If queuing fails, clean up by deleting the uploaded file
    fs.delete(fid)
    return "internal server error", 500
  