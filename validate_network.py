# --------------------------------------------
# Written by Aabhaas Vijayvergia  
# 14th April 2025  
# Validates reachability of devices in a network topology using ping
# Logs results, counts reachable vs unreachable nodes
# Saves final results to a JSON file (results.json)
# --------------------------------------------

import argparse        # For parsing command-line arguments
import subprocess      # To run shell commands like 'ping'
import logging         # For professional-looking log messages
import json            # To load/save JSON files
import os              # To check file paths

# Set up logging format with timestamps
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

# Function to ping an IP and return True if reachable, else False
def ping_host(host):
    try:
        # Run 'ping' command with 2 packets
        result = subprocess.run(['ping', '-c', '2', host], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"✅ Host {host} is reachable.")
            return True
        else:
            logging.warning(f"❌ Host {host} is NOT reachable.")
            return False
    except Exception as e:
        logging.error(f"⚠️ Error pinging {host}: {e}")
        return False

# Main function — handles reading config, pinging nodes, saving summary
def main():
    # Set up CLI argument parser
    parser = argparse.ArgumentParser(description="Validate reachability of nodes in a network topology.")
    parser.add_argument('--config', required=True, help='Path to topology JSON file')
    args = parser.parse_args()

    # Check if file exists
    if not os.path.exists(args.config):
        logging.error("❌ Config file not found.")
        return

    # Load topology JSON file into Python dict
    with open(args.config, 'r') as f:
        topology = json.load(f)

    # Set up counters and result tracking list
    reachable_count = 0
    unreachable_count = 0
    detailed_results = []

    # Go through each node and ping its IP
    for node in topology.get('nodes', []):
        name = node.get('name', 'Unnamed Node')
        host = node.get('ip')

        if host:
            success = ping_host(host)
            if success:
                reachable_count += 1
                detailed_results.append({"name": name, "ip": host, "status": "reachable"})
            else:
                unreachable_count += 1
                detailed_results.append({"name": name, "ip": host, "status": "unreachable"})
        else:
            logging.warning(f"⚠️ Node '{name}' has no IP.")
            detailed_results.append({"name": name, "ip": None, "status": "missing_ip"})

    # Print validation summary
    logging.info("🔍 Validation Summary:")
    logging.info(f"🟢 Reachable: {reachable_count}")
    logging.info(f"🔴 Unreachable: {unreachable_count}")
    logging.info(f"📊 Total Nodes Checked: {reachable_count + unreachable_count}")

    # Save results to a JSON file for records
    output_data = {
        "reachable": reachable_count,
        "unreachable": unreachable_count,
        "total": reachable_count + unreachable_count,
        "results": detailed_results
    }

    with open("results.json", "w") as out_file:
        json.dump(output_data, out_file, indent=2)

    logging.info("📁 Results saved to results.json")

# Run script only if executed directly
if __name__ == "__main__":
    main()