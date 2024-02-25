import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start(message, fs_videos, fs_mp3s, channel):
  message = json.loads(message)
  logger.info("converter got message: %s", message)
  # empty temp file
  tf = tempfile.NamedTemporaryFile()
  # video contents
  out = fs_videos.get(ObjectId(message["video_fid"]))
  logger.info("fetched db file: %s", out)
  # add video contents to empty file
  tf.write(out.read())
  # create audio from teemp video file
  audio = moviepy.editor.VideoFileClip(tf.name).audio
  tf.close()
  logger.info("video converted to mp3: %s", message['video_fid'])

  # write audio to the file
  tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
  audio.write_audiofile(tf_path)

  # save the file to mongo
  f = open(tf_path, "rb")
  data = f.read()
  fid = fs_mp3s.put(data)
  f.close()
  os.remove(tf_path)

  message["mp3_fid"] = str(fid)

  try:
    channel.basic_publish(
      exchange="",
      routing_key=os.environ.get("MP3_QUEUE"),
      body=json.dumps(message),
      properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
      ),
    )
  except Exception as err:
    fs_mp3s.delete(fid)
    return "failed to publish message"