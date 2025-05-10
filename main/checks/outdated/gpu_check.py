"""
gpu_check.py - monitors GPU temperatures, loading, throttling status, and errors

"""

import os
import platform
import subprocess
import logging
import psutil
from .base import Check
from .os_detector import detect_operating_system
import datetime
import time

def get_gpu_temperature_linux():
    pass

def get_gpu_temperature_windows():
    pass

def get_gpu_load_linux():
    pass

def get_gpu_load_windows():
    pass

def GPUCheck(Check):
    pass