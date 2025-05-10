from .base import Check
from ..logging_setup import configure_daily_logging
from .os_detector import detect_operating_system
from tools.write_to_json_file import write_to_check_results

import psutil
import subprocess
import os
import logging

configure_daily_logging()
logger = logging.getLogger(__name__)

class DiskCheck(Check):

    name = "disk"

    def run(self):

        os_information = detect_operating_system()
        os_type = os_information[0]
        results = []

        if os_type == "Windows":
            results = self._get_windows_disk_info()
        elif os_type == "Linux":
            results = self._get_linux_disk_info()
        else: 
            logger.error(f"Unsupported OS for disk check: {os_type}")
            return[{"name": self.name, "status": "UNKNOWN", "details": f"Unsupported OS: {os_type}"}]
        
        for result in results:
            write_to_check_results({"Disk Information": result})
        
        return results

    def _get_windows_disk_info(self):

        results = []

        try:
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    percent_used = usage.percent
                    status = self.evaluate("percent used", percent_used)

                    metrics = {
                        "File System": partition.device,
                        "Disk Size": usage.total,
                        "Total Used": usage.used,
                        "Total Available": usage.free,
                        "Percentage Used": percent_used
                    }

                    logger.info(f"Retrieved Disk Information | Partition: {partition.device} | Size: {usage.total} | Used: {usage.used} | Free: {usage.free} | Percentage Used: {percent_used}%")
                    logger.info("Successfully wrote disk information to check_results.json")

                    results.append({
                        "name": self.name,
                        "status": status,
                        "metrics": metrics,
                        "details": f"Disk {partition.device} is {percent_used}% full."
                    })

                except Exception as e:
                    logger.error(f"Failed to get disk usage for {partition.devicxe}: {e}")
                    results.append({
                        "name": self.name,
                        "status": "UNKNOWN",
                        "metrics": {"partition": partition.device},
                        "details": f"Error: {e}"
                    })

        except Exception as e:
            logger.error(f"Failed to retrieve disk partitions on Windows system: {e}")
        
        return results

    def _get_linux_disk_info(self):  

        results = []

        try:
            disk_df_output = subprocess.check_output('df -h', shell = True).decode('utf-8')
            logger.info("Successfully retrieved disk information on Linux using df command")

            for line in disk_df_output.splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 6:
                    filesystem = parts[0]
                    size = parts[1]
                    used = parts[2]
                    available = parts[3]
                    percent_used_str = parts[4]

                    try:
                        percent_used = float(percent_used_str.strip('%'))
                        status = self.evaluate("percent_used", percent_used)
                    except ValueError:
                        percent_used = 0.0
                        status = "UNKNOWN"

                    metrics = {
                        "File System": filesystem,
                        "Disk Size": size,
                        "Total Used": used, 
                        "Total Available": available,
                        "Percentage Used": percent_used
                    }

                    logger.info(f"Retrieved Disk Information | Filesystem: {filesystem} | Size: {size} | Used: {used} | Available: {available} | Percentage Used: {percent_used_str}")

                    results.append({
                        "name": self.name,
                        "status": status,
                        "metrics": metrics,
                        "details": f"Disk {filesystem} is {percent_used_str} full."
                    })
        
        except Exception as e:
            logger.error(f"Error retrieving disk partition information on Linux: {e}")

        return results

