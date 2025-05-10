"""
cpu_check.py – Monitors CPU core count, utilization, and frequency.
"""
import logging
import psutil

from .base import Check
from .os_detector import detect_operating_system

from tools.write_to_json_file import write_to_check_results

from ..logging_setup import configure_daily_logging
configure_daily_logging()

import logging
logger = logging.getLogger(__name__)

os_info = detect_operating_system()

def get_cpu_information_linux():
    """ Retrieves CPU information on Linux systems using the 'lscpu' command."""
    try:
        cpu_lscpu_linux = subprocess.check_output('lscpu', shell=True).decode('utf-8')
        logger.info("Successfully retrieved CPU information on Linux")

        for line in cpu_lscpu_linux.splitlines():
            if line.startswith("Model name:"):
                cpu_model_name = line.split(":")[1].strip()
                logger.info(f"CPU Model Name: {cpu_model_name}")
            elif line.startswith("Architecture:"):
                architecture = line.split(":")[1].strip()
                logger.info(f"CPU Architecture: {architecture}")
            elif line.startswith("CPU(s):"):
                cpu_count = line.split(":")[1].strip()
                logger.info(f"CPU Count: {cpu_count}")
            elif line.startswith("Thread(s) per core:"):
                cpu_threads_per_core = line.split(":")[1].strip()
                logger.info(f"Threads per Core: {cpu_threads_per_core}")

            json_title = "CPU Information"
            cpu_information = {
                "model_name": cpu_model_name,
                "architecture": architecture,
                "cpu_count": cpu_count,
                "threads_per_core": cpu_threads_per_core
            }

            try:
                data_to_write = {json_title: cpu_information}
                write_to_check_results(data_to_write, "check_results.json")
            
            except Exception as e:
                logging.error(f"Error writing to check_results.json: {e}")


    except subprocess.CalledProcessError as e:
        logger.error(f"Error retrieving CPU information on Linux: {e}")
        return None

def get_cpu_information_windows():
    """ Retrieves CPU information on Windows systems using psutil."""
    
    try:
        cpu_physical_cores = psutil.cpu_count(logical=False)
        cpu_logical_cores = psutil.cpu_count(logical=True)
        cpu_utilization = psutil.cpu_percent(interval=1)
        cpu_frequency = psutil.cpu_freq()
        logger.info("Successfully retrieved CPU information on Windows")

        json_title = "CPU Information"
        cpu_information = {
            "physical_cores": cpu_physical_cores,
            "logical_cores": cpu_logical_cores,
            "utilization": cpu_utilization,
            "frequency": cpu_frequency
        }

        try: 
            data_to_write = {json_title: cpu_information}
            write_to_check_results(data_to_write, "check_results.json")
        
        except:
            logging.error(f"Error writing to check_results.json: {e}")

    except Exception as e:
        logger.error(f"Error retrieving CPU information on Windows: {e}")
        return None


def CheckCPU(Check):
    """ Runs the CPU check and returns the status and details"""

    if os_info[0] == "Linux":
        cpu_information = get_cpu_information_linux()
    elif os_info[0] == "Windows":
        cpu_information = get_cpu_information_windows()
    else:
        logger.error("Attempted to run CPU check on unsupported OS")
        return None

def main():
    CheckCPU(Check)
    logger.info("CPU check completed successfully")
    
if __name__ == "__main__":
    main()