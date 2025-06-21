# Network Scanner

A basic network port scanner built with Python for educational purposes.

## Features

- Multi-threaded port scanning
- Banner grabbing for service identification
- Command-line interface with customizable options
- Support for custom port ranges
- Built-in timeout and thread control

## Usage

# Basic scan of common ports
python network_scanner.py scanme.nmap.org

# Scan specific ports
python network_scanner.py google.com -p "80,443,22"

# Adjust timeout and threads
python network_scanner.py 127.0.0.1 -t 2 --threads 50