# 🔧 Network Reachability Validator

**Built by Aabhaas Vijayvergia**  
*April 14, 2025*

## 📌 About the Project

This is a small Python tool I built to simulate how network engineers validate device connectivity in real-world infrastructures. It reads a JSON config of devices, pings each IP, logs the results, and saves a final summary to `results.json`.

I built this while preparing for my software engineering internship at **Juniper Networks**, to explore concepts like network topology, validation, and infrastructure scripting.

## 🚀 Features

- CLI-based tool using `argparse`
- Reads config from a `topology.json` file
- Uses `subprocess` to ping each IP
- Logs success, failure, and errors with clean formatting
- Counts reachable vs unreachable devices
- Saves output to `results.json`

## 🧪 How to Run

```bash
python validate_network.py --config topology.json
