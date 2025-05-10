"""
Detect the operating system and architecture of the current environment
"""

import os
import platform

from ..logging_setup import configure_daily_logging
configure_daily_logging()

import logging
logger = logging.getLogger(__name__)

from tools.write_to_json_file import write_to_check_results

def detect_operating_system():
    """""
    Detects the operating system and architecture
    """
    
    operating_system_name = platform.system()
    operating_system_version = platform.version()
    system_architecture = platform.architecture()

    return operating_system_name, operating_system_version, system_architecture


def main():
    os_info = detect_operating_system()
    logger.info(f"Retrieved OS information: {os_info[0]} {os_info[1]} {os_info[2]}")

    try:
        json_title = "Operating System Information"
        operating_system_information ={
            
            "Operating System": os_info[0],
            "Version": os_info[1],
            "Architecture": os_info[2]
        }

        data_to_write = {json_title: operating_system_information}

        write_to_check_results(data_to_write, "check_results.json")
        logger.info("Successfully wrote OS information to JSON file")

    except Exception as e:
        logger.error(f"Error writing OS information to JSON file: {e}")
        return None

    
if __name__ == "__main__":
    main()