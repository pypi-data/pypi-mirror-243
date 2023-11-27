import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import logging.config

from netapi import *

logging.config.fileConfig('logging.conf')

logging.info("Initialized logging from logging.conf")