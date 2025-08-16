import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

blocked_ips_db = {}  # Simulate a database for blocked IPs (using a dictionary)
good_ips_db = set()  # Simulate a set for known good IPs

def block_ip(ip_address, reason="Suspicious Activity"):
    """
    Simulates blocking an IP address and logs it to the blocked IPs database.

    Args:
        ip_address (str): The IP address to block.
        reason (str): The reason for blocking the IP.
    """
    try:
        if ip_address not in blocked_ips_db:
            blocked_ips_db[ip_address] = reason
            logging.info(f"[RESPONSE] Blocking IP address: {ip_address} due to {reason}")
        else:
            logging.info(f"[RESPONSE] IP address {ip_address} is already blocked.")
    except Exception as e:
        logging.error(f"Error in block_ip: {e}")

def log_good_ip(ip_address):
    """
    Simulates logging a "good" IP address.  Uses a set to avoid duplicates.

    Args:
        ip_address (str): The IP address to log as good.
    """
    try:
        good_ips_db.add(ip_address)
        # logging.info(f"[LOG - Good IP] Noted good IP address: {ip_address}") # Noisy.  Only log if you want
    except Exception as e:
        logging.error(f"Error in log_good_ip: {e}")

def display_blocked_ips():
    """Displays the blocked IP addresses and their reasons."""
    logging.info("\n--- Blocked IP Addresses ---")
    if blocked_ips_db:
        for ip, reason in blocked_ips_db.items():
            logging.info(f"IP: {ip}, Reason: {reason}")
    else:
        logging.info("No IPs currently blocked.")


def display_good_ips():
    """Displays the known good IP addresses."""
    logging.info("\n--- Known Good IP Addresses ---")
    if good_ips_db:
        for ip in sorted(list(good_ips_db)):
            logging.info(f"IP: {ip}")
    else:
        logging.info("No good IPs currently logged.")


if __name__ == "__main__":
    logging.info("Response System Initialized")
    try:
        # Simulate getting detected malicious IPs (from other modules)
        malicious_ip1 = "203.0.113.50"
        malicious_ip2 = "192.168.1.200"
        malicious_ip3 = "203.0.113.50"  # Duplicate to test the "already blocked" logic
        block_ip(malicious_ip1, "Blacklisted")
        block_ip(malicious_ip2, "High Request Rate")
        block_ip(malicious_ip3, "Repeated Attacks")  # Try to block again

        # Simulate logging good IPs
        good_ip1 = "192.168.1.100"
        good_ip2 = "10.0.0.25"
        log_good_ip(good_ip1)
        log_good_ip(good_ip2)
        log_good_ip(good_ip1)  # duplicate

        display_blocked_ips()
        display_good_ips()
    except Exception as e:
        logging.error(f"Error in main: {e}")