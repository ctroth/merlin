import subprocess

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

def main():
    get_cpu_usage_windows()

if __name__ == "__main__":
    main()