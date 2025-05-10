"""
network_check.py - monitors network connectivity, speed, interfaces, and errors
"""

import logging
import psutil
import subprocess
import os

from .base import Check
from .os_detector import detect_operating_system

from tools.write_to_json_file import write_to_check_results

from ..logging_setup import configure_daily_logging
configure_daily_logging()

import logging
logger = logging.getLogger(__name__)

os_info = detect_operating_system()

def get_network_information_linux():
    pass

def get_network_information_windows():



def NetworkCheck(Check):
    pass