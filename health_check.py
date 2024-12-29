import os
import socket

LOG_FILE_PATH = "/marzneshiniplimitcode/app.log"
CONFIG_FILE_PATH = "/marzneshiniplimitcode/config.json"

def check_logs_for_errors():
    """بررسی لاگ برای متن 'Unexpected error'"""
    try:
        if os.path.exists(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, 'r') as log_file:
                logs = log_file.read()
                if "Unexpected error" in logs:
                    return False, "Unexpected error found in logs"
        else:
            return False, f"Log file not found: {LOG_FILE_PATH}"
    except Exception as e:
        return False, f"Error reading log file: {str(e)}"
    return True, "Logs are clean"

def check_config_file():
    """بررسی وجود فایل config.json"""
    if os.path.exists(CONFIG_FILE_PATH):
        return True, f"Config file exists: {CONFIG_FILE_PATH}"
    return False, f"Config file not found: {CONFIG_FILE_PATH}"

def run_health_checks():
    checks = [
        check_logs_for_errors,
        check_config_file
    ]
    for check in checks:
        result, message = check()
        if not result:
            return False, message
    return True, "All health checks passed"

if __name__ == "__main__":
    health_status, message = run_health_checks()
    if health_status:
        print("HEALTHY: ", message)
        exit(0)
    else:
        print("UNHEALTHY: ", message)
        exit(1)
