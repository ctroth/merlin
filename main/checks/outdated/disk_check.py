"""
disk_check.py - Monitors disk space, usage, I/O, performance, and errors
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

def get_disk_information_linux():
  """ Retrieves disk information on Linux system using the 'df' command and psutil."""

  try:
    disk_df_linux = subprocess.check_output('df -h', shell=True).decode('utf-8')
    logger.info("Successfully retrieved disk information on Linux using df command")

    for line in disk_df_linux.splitlines()[1:]:
      parts = line.split()
      if len(parts) >= 6:
        filesystem = parts[0]
        size = parts[1]
        used = parts[2]
        available = parts[3]
        percent_used = parts[4]

        logger.info(f"Retrieved Disk Information | Filesystem: {filesystem} | Size: {size} | Used: {used} | Available: {available} | Percentage Used: {percent_used}")

      json_title = "Disk Information"
      disk_information = {
        "FileSystem": filesystem,
        "Disk Size": size,
        "Total Used": used,
        "Total Available": available,
        "Percentage Used": percent_used
      }

      try:
        data_to_write = {json_title: disk_information}
        write_to_check_results(data_to_write, "check_results.json")
      
      except Exception as e:
        logger.error(f"Failed to write disk information to check_results.json: {e}")
        return None

  except Exception as e:
    logging.error(f"Error retrieving disk partition information on Linux.: {e}")
        
def get_disk_information_windows():
    """ Retrieves disk information on Windows systems using psutil."""
    try:
        disk_partitions = psutil.disk_partitions()
        
        for partition in disk_partitions:
            partition_name = partition.device
            partition_size = psutil.disk_usage(partition.mountpoint).total
            partition_used = psutil.disk_usage(partition.mountpoint).used
            partition_free = psutil.disk_usage(partition.mountpoint).free
            partition_percent = psutil.disk_usage(partition.mountpoint).percent

            logger.info(f"Retrieved Disk Information | Partition: {partition_name} | Size: {partition_size} Bytes | Used: {partition_used} Bytes | Free: {partition_free} Bytes | Percentage Used: {partition_percent}%")

            json_title = "Disk Information"
            disk_information = {
                "File System": partition_name,
                "Disk Size": partition_size,
                "Total Used": partition_used,
                "Total Available": partition_free,
                "Percentage Used": partition_percent
            }
            
            try:
                data_to_write = {json_title: disk_information}
                write_to_check_results(data_to_write, "check_results.json")
                logger.info(f"Successfully wrote disk information to check_results.json")
                
            except Exception as e:
                logger.error(f"Failed to write disk information to check_results.json : {e}")
                return None
    
    except Exception as e:
        logging.error(f"Error retrieving disk information on Windows for partition {partition.device if 'partition' in locals() else 'unknown'}: {e}")
        return None

def CheckDisk(Check):
    """ Runs the disk check and returns the status and details"""

    if os_info[0] == "Linux":
        disk_information = get_disk_information_linux()
        logger.info("Successfully retrieved disk information on Linux")
    elif os_info[0] == "Windows":
        disk_information = get_disk_information_windows()
        logger.info("Successfully retrieved disk information on Windows")
    else:
        logger.error("Attempted to run Disk check on unsupported OS")
        return None

def main():
    CheckDisk(Check)
    logger.info("Disk check completed successfully")
    
if __name__ == "__main__":
    main()