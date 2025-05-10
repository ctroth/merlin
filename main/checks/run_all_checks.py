from .disk_check import DiskCheck
# from .cpu_check import CPUCheck  # Uncomment when implemented
# from .os_check import OSCheck    # Uncomment when implemented

from .thresholds import thresholds
from .base import Check

# Use imported thresholds from thresholds.py
check_config = {
    "thresholds": thresholds
}

def run_all_checks():
    checks = [
        DiskCheck(check_config),
        # CPUCheck(check_config),
        # OSCheck(check_config),
    ]

    results = []
    for check in checks:
        try:
            check_results = check.run()
            results.extend(check_results if isinstance(check_results, list) else [check_results])
        except Exception as e:
            results.append({
                "name": check.name,
                "status": "UNKNOWN",
                "details": f"Error running check: {e}"
            })

    return results

if __name__ == "__main__":
    all_results = run_all_checks()
    for result in all_results: #this is a debugging tool.  outputs to the CLI
        print(result)
