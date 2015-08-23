#!/usr/bin/env python3

from stream_to_dropbox import StreamToDropbox
import picamera
from time import sleep
from datetime import datetime
import io
import RPi.GPIO as GPIO

import logging
import logging.handlers
import argparse
import sys
import time  # this is only being used as part of the example

# Deafults
LOG_FILENAME = "/tmp/kamera_streamer.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="My simple Python service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
        LOG_FILENAME = args.log

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

# Init camera:
camera = picamera.PiCamera()
camera.exposure_mode = 'sports'
camera.resolution = (1280, 720)

# Init streamer:
streamer = StreamToDropbox()
streamer.init_client()

# Init GPIO:
pin = 8
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)

try:
	while True:
		if not GPIO.input(pin):
			sleep(0.5)
			continue

		# Create an in-memory stream
		my_stream = io.BytesIO()
	
		current_time = datetime.now()
		camera.annotate_text = current_time.isoformat()
		camera.capture(my_stream, 'jpeg')
		
		streamer.put_new_image(my_stream.getvalue())
		my_stream.close()
		sleep(1)

except KeyboardInterrupt:
	print("Exit program")
	exit()
		
