import time
import random
import logging
import requests
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_ip_list_from_url(url):
    """
    Fetches a list of IP addresses from a given URL, handling various formats.

    Args:
        url (str): The URL to retrieve the IP address list from.

    Returns:
        list: A list of IP addresses, or an empty list on error.
    """
    try:
        response = requests.get(url, timeout=10)  # Add a timeout
        response.raise_for_status()  # Raise exception for bad status
        text = response.text.strip()

        # Regular expression to find IP addresses (IPv4)
        ip_regex = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        ip_list = re.findall(ip_regex, text)

        if not ip_list:
            logging.warning(f"No IPs found at {url}.  Trying alternative parsing.")
            # Alternative parsing: split by lines, look for IPs
            ip_list = [line.strip() for line in text.splitlines() if re.match(ip_regex, line.strip())]

        if not ip_list:
            logging.warning(f"No IPs found at {url} with alternative parsing. Returning empty list.")
            return []

        logging.info(f"Successfully fetched {len(ip_list)} IPs from {url}")
        return ip_list
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching IP list from {url}: {e}")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return []


def generate_traffic(filename="simulated_traffic.log", duration=20, ip_source_url=None):
    """
    Simulates network traffic and writes it to a log file.

    Args:
        filename (str): The name of the log file to create.
        duration (int): The duration of the simulation in seconds.
        ip_source_url (str, optional): URL to fetch IP addresses.
    """
    ip_source_list = []

    if ip_source_url:
        ip_source_list = get_ip_list_from_url(ip_source_url)
        if not ip_source_list:
            logging.warning("Failed to fetch IPs from URL. Using random IPs.")

    try:
        with open(filename, "w") as f:
            start_time = time.time()
            while time.time() - start_time < duration:
                # Simulate traffic
                if ip_source_list:
                    source_ip = random.choice(ip_source_list)
                else:
                    if random.random() < 0.8:
                        source_ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
                    else:
                        source_ip = f"203.0.113.{random.randint(1, 254)}"

                destination_ip = "your_cloud_server.com"  # Replace with a placeholder.
                request_type = random.choice(["GET", "POST", "PUT", "DELETE"])
                resource = random.choice(
                    ["/", "/index.html", "/api/data", "/product/123", "/login", "/upload", "/download/file.zip"]
                )
                user_agent = random.choice(
                    [
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                        "Chrome/100.0.0.0",
                        "Safari/15.0",
                        "MaliciousBot/1.0",  # Simulate malicious user agent
                        "curl/7.81.0",
                    ]
                )
                f.write(
                    f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Source: {source_ip}, Dest: {destination_ip}, Method: {request_type}, Resource: {resource}, User-Agent: {user_agent}\n"
                )
                time.sleep(random.uniform(0.2, 1.0))
        logging.info(f"Traffic simulation completed. The output is located in {filename}")
    except Exception as e:
        logging.error(f"Error in generate_traffic: {e}")



if __name__ == "__main__":
    logging.info("Initiating network traffic simulation...")
    ip_source_url = "https://www.wiz.io/hubfs/Wiz-Research- злоумышленники-IP-адреса.txt"  #  <--- Replace this
    generate_traffic(ip_source_url=ip_source_url)
    logging.info("Traffic simulation complete.")