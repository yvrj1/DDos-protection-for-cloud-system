import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_blacklist(blacklist_file="external_blacklist.txt", ip_source_url="https://www.wiz.io/hubfs/Wiz-Research-злоумышленники-IP-адреса.txt"):
    """
    Updates the external blacklist file with IP addresses from a given URL.

    Args:
        blacklist_file (str): The path to the blacklist file.
        ip_source_url (str): The URL to retrieve the IP address list from.
    """
    try:
        response = requests.get(ip_source_url, timeout=10)
        response.raise_for_status()  # Raise exception for bad status
        ips = response.text.strip().splitlines()

        with open(blacklist_file, "w") as f:
            for ip in ips:
                f.write(ip + "\n")
        logging.info(f"Successfully updated blacklist file '{blacklist_file}' with {len(ips)} IPs from {ip_source_url}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error updating blacklist: {e}")
    except Exception as e:
        logging.error(f"Error updating blacklist: {e}")



if __name__ == "__main__":
    logging.info("Updating external blacklist...")
    update_blacklist()
    logging.info("Blacklist update complete.")