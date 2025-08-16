import logging
from collections import defaultdict
import time
from response_system import block_ip, log_good_ip  # Import the blocking function

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_traffic_behavior(log_file="simulated_traffic.log", threshold=10, time_window=5):
    """
    Analyzes traffic behavior for anomalies, such as a high number of requests from a single IP
    within a time window.

    Args:
        log_file (str): The path to the simulated traffic log file.
        threshold (int): The maximum number of requests allowed from an IP within the time window.
        time_window (int): The time window in seconds to check for excessive requests.
    """
    request_counts = defaultdict(int)
    timestamps = defaultdict(list)

    try:
        with open(log_file, 'r') as f:
            for line in f:
                parts = line.split(" - Source: ")[1].split(",")[0].strip() if " - Source: " in line else None
                timestamp_str = line.split(" - ")[0]
                try:
                    timestamp = time.mktime(time.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S'))
                    if parts:
                        ip_address = parts
                        timestamps[ip_address].append(timestamp)
                        # Check requests in the current time window
                        recent_requests = [t for t in timestamps[ip_address] if t > timestamp - time_window]
                        if len(recent_requests) > threshold:
                            block_ip(
                                ip_address,
                                f"High request rate: {len(recent_requests)} requests in {time_window} seconds",
                            )
                        else:
                            log_good_ip(ip_address)  # Log as potentially good
                except ValueError:
                    logging.warning(f"Skipping invalid timestamp format in line: {line.strip()}")
                    continue  # Skip lines with invalid timestamps
    except FileNotFoundError:
        logging.error(f"Error: Log file '{log_file}' not found.")
    except Exception as e:
        logging.error(f"Error in analyze_traffic_behavior: {e}")

if __name__ == "__main__":
    logging.info("Analyzing traffic behavior for anomalies...")
    analyze_traffic_behavior()
    logging.info("Behavior analysis complete.")