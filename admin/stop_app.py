#!/usr/bin/python3
import sys
import os
import signal
import time
import logging 
sys.path.append('/opt/rest')
from modules.setlogs import setlogger
print("whyy")
logger = setlogger("stop_app")
logger.info(f"shutting down app: {sys.argv[1]}")
time.sleep(5)
os.kill(int(sys.argv[1]),signal.SIGTERM)
