# Network Scanner

A basic network port scanner built with Python for educational purposes.

# Features

- Multi-threaded port scanning
- Banner grabbing for service identification
- Command-line interface with customizable options
- Support for custom port ranges
- Built-in timeout and thread control

# Usage

### Basic scan of common ports
`python network_scanner.py scanme.nmap.org`

### Scan specific ports
`python network_scanner.py google.com -p "80,443,22"`

### Adjust timeout and threads
`python network_scanner.py 127.0.0.1 -t 2 --threads 50`

# Installation

### Clone the repository:
`git clone https://github.com/yourusername/network-scanner.git`

`cd network-scanner`

### Create a virtual environment:

`python3 -m venv scanner_env`

`source scanner_env/bin/activate`

On Windows: `scanner_env\Scripts\activate`

### Run the scanner:

`bashpython network_scanner.py --help`

## Legal Notice
This tool is for educational purposes only. Only use on networks you own or have explicit permission to test. Unauthorized network scanning may be illegal in your jurisdiction.

## Built With
Python 3.x
Threading for concurrent scanning
Socket programming for network connections
Argparse for command-line interface

## Author
Built while learning cybersecurity concepts after completing CompTIA Security+.