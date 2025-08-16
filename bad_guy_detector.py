import logging
from response_system import block_ip, log_good_ip  # Import the blocking function

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_blacklist(ip_address, blacklist_file="external_blacklist.txt"):
    """
    Checks if an IP address is in the blacklist.

    Args:
        ip_address (str): The IP address to check.
        blacklist_file (str): The path to the blacklist file.

    Returns:
        bool: True if the IP is blacklisted, False otherwise.
    """
    try:
        with open(blacklist_file, 'r') as bl_file:
            blacklist = [line.strip() for line in bl_file]
            return ip_address in blacklist
    except FileNotFoundError:
        logging.warning(f"Blacklist file '{blacklist_file}' not found.  Continuing without blacklist.")
        return False  # Important: handle the case where the file doesn't exist.
    except Exception as e:
        logging.error(f"Error in check_blacklist: {e}")
        return False

def detect_signature(log_file="simulated_traffic.log", signature_file="malware_signatures.txt"):
    """
    Detects malicious signatures in the simulated traffic log and checks IPs against a blacklist.

    Args:
        log_file (str): The path to the simulated traffic log file.
        signature_file (str): The path to the malware signatures file.
    """
    try:
        with open(signature_file, 'r') as s_file, open(log_file, 'r') as t_file:
            signatures = [line.strip() for line in s_file]
            for line in t_file:
                ip = line.split(" - Source: ")[1].split(",")[0].strip() if " - Source: " in line else None
                for signature in signatures:
                    if signature in line:
                        if ip:
                            block_ip(ip, f"Signature match: '{signature}'")
                if ip:
                    if check_blacklist(ip):
                        block_ip(ip, "Blacklisted IP")
                    else:
                        log_good_ip(ip)  # Log as potentially good
    except FileNotFoundError as e:
        logging.error(f"Error: {e}.  Ensure the necessary files exist.")
    except Exception as e:
        logging.error(f"Error in detect_signature: {e}")

if __name__ == "__main__":
    logging.info("Checking simulated traffic for blacklisted IPs and signatures...")
    detect_signature()
    logging.info("Signature and blacklist check complete.")