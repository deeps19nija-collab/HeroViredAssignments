import psutil
import logging
import sys
import time


#--------------Configuration--------------------------------

CPU_USAGE_THRESHOLD = 5 # Threshold for alert in percentage
CHECK_INTERVAL = 1       # Time (in seconds) between each check

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),                  # Output to console
        logging.FileHandler("cpu_monitor.log", mode='a')    # Log alerts to file
    ]
)
#-----------------------Core Function ------------------------

def monitor_cpu(threshold: int, interval: int):

    """
    Continuously monitors the CPU usage and logs an alert
    if it exceeds the given threshold.

    Args:
        threshold (int): CPU usage percentage to trigger alert.
        interval (int): Time interval (in seconds) between checks.

    """
    logging.info("Starting cpu usage monitoring... ")
    try:
        while True:
            # Get current CPU usage over defined interval
            cpu_usage = psutil.cpu_percent(interval=interval)

            # Log an alert if usage exceeds threshold
            if cpu_usage > threshold:
                logging.warning(f"Alert ! CPU usage exceeds threshold: {cpu_usage}%")

                # Short sleep is redundant due to interval in cpu_percent()

    except KeyboardInterrupt:
        logging.info("Monitoring interrupted by user. Exiting gracefully.")
    except Exception as e:
        logging.error(f"Unexpected error occured: {e}", exc_info=True)

# ---------------------- Entry Point ----------------------

if __name__ == "__main__":
    monitor_cpu(CPU_USAGE_THRESHOLD, CHECK_INTERVAL)

