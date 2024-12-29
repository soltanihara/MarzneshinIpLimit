import os
import socket

LOG_FILE_PATH = "/marzneshiniplimitcode/app.log"

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

def run_health_checks():
    checks = [
        check_logs_for_errors,
    ]
    for check in checks:
        result, message = check()
        if not result:
            return False, message
    return True, "Health check passed"

if __name__ == "__main__":
    health_status, message = run_health_checks()
    if health_status:
        print("HEALTHY: ", message)
        exit(0)
    else:
        print("UNHEALTHY: ", message)
        exit(1)
