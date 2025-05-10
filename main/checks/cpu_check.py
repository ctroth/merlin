from .base import Check
from ..logging_setup import configure_daily_logging
from .os_detector import detect_operating_system
from tools.write_to_json_file import write_to_check_results

import psutil
import subprocess
import os

class CPUCheck(Check):

    name = "cpu"

    def run(self):

        os_information = detect_operating_system()
        os_type = os_information[0]
        results = []

        if os_type == "Windows":
            results = self._get_windows_cpu_info()
        elif os_type == "Linux":
            self.install_mpstat()
            results = self._get_linux_cpu_info()
        else:
            logger.error(f"Unsupported OS for CPU check: {os_type}")
            return[{"name": elf.name, "status": "UNKNOWN", "details": f"Unsupported OS: {os_type}"}]
        
        for result in results:
            write_to_check_results({"CPU Information": result})
        
        return result

    def install_mpstat(self):

    try:
        subprocess.run('sudo apt-get install sysstat')
    except Exception as e:
        logger.info(f"Encountered error while attempting to install sysstat on Linux system. Issue may be related to permissions or it is already installed on RHEL based systems.")
        

    def get_cpu_usage_linux(self):
        
        cpu_usage = subprocess.run(['mpstat', 1, 1], capture_output = True, text = True, check = True)

        lines = cpu_usage.stdout.strip().splitlines()

        try:
            for line in lines:
                cols = line.split()
                if len(cols) >= 12 and cols[1] == "all":

                    idle = float(cols[-1])
                    return 100.0 - idle
        
        except Exception as e:
            raise RuntimeError("Error encountered attempting to parse mpstat output.")
            logger.error(f"Error encountered attempting to parse mpstat output: {e}")

    
    def get_cpu_usage_windows():
        try:
            powershell_command = ["powershell", "-NoProfile", "-Command", "Get-Counter '\\Processor(_Total)\\% Processor Time' -SampleInterval 1 -MaxSamples 1 " "| Select -ExpandProperty CounterSamples " "| Select -ExpandProperty CookedValue"]
            cpu_usage = subprocess.run(powershell_command, capture_output = True, text = True)


            if cpu_usage.returncode != 0:
                print("Error running Get-Counter", cpu_usage.stderr.strip())
                return
            
            complete_cpu_usage = cpu_usage.stdout.strip()
            
            try:
                usage = float(complete_cpu_usage)
                return usage
                
            except ValueError:
                print("Unexpected output from Get-Counter", complete_cpu_usage)
        
        except Exception as e:
            print(f"Encountered error: {e}")

    
    def _get_linux_cpu_info(self):

        results = []

        try:
            cpu_lscpu_linux = subprocess.check_output('lscpu', shell=True).decode("utf-8")
            logger.info("Successfully retrieved CPU information on Linux")

            try: 
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
                    
                    cpu_linux_usage = subprocess.check_output('')

                metrics = {
                    "Model Name": cpu_model_name,
                    "Architecture": architecture,
                    "CPU Count": cpu_count,
                    "CPU Threads": cpu_threads_per_core
                }

                logger.info(f"Successfully retrieved all system CPU information.")

