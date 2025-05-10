# thresholds.py

thresholds = {
    "disk": {
        "warn": 75.0,  # % disk used at which to warn
        "crit": 90.0   # % disk used at which to raise a critical alert
    },
    "cpu": {
        "warn": 80.0,  # % CPU usage to warn
        "crit": 95.0   # % CPU usage to alert
    },
    "memory": {
        "warn": 70.0,  # % memory used to warn
        "crit": 90.0   # % memory used to alert
    }
    # Add more component thresholds as needed
}
