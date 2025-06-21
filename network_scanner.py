#!/usr/bin/env python3
"""
Basic Network Scanner
A simple port scanner for educational purposes
"""

import socket
import sys
import threading
from datetime import datetime
import argparse

class NetworkScanner:
    def __init__(self, target, ports=None, timeout=1, threads=100):
        self.target = target
        self.ports = ports or [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5432, 5900]
        self.timeout = timeout
        self.threads = threads
        self.open_ports = []
        self.lock = threading.Lock()
    
    def resolve_target(self):
        """Resolve hostname to IP address"""
        try:
            ip = socket.gethostbyname(self.target)
            print(f"Scanning target: {self.target} ({ip})")
            return ip
        except socket.gaierror:
            print(f"Error: Could not resolve hostname {self.target}")
            return None
    
    def scan_port(self, ip, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            
            if result == 0:
                # Try to grab banner
                banner = self.grab_banner(sock, port)
                with self.lock:
                    self.open_ports.append((port, banner))
                    print(f"[+] Port {port}: Open {banner}")
            
            sock.close()
        except Exception as e:
            pass  # Silently handle exceptions for closed ports
    
    def grab_banner(self, sock, port):
        """Attempt to grab service banner"""
        try:
            if port in [21, 22, 23, 25, 110, 143]:  # Services that send banners
                sock.settimeout(2)
                banner = sock.recv(1024).decode().strip()
                return f"- {banner[:50]}..." if len(banner) > 50 else f"- {banner}"
            elif port == 80:
                sock.send(b"GET / HTTP/1.1\r\nHost: " + self.target.encode() + b"\r\n\r\n")
                response = sock.recv(1024).decode()
                if "Server:" in response:
                    server = response.split("Server:")[1].split("\r\n")[0].strip()
                    return f"- {server}"
        except:
            pass
        return ""
    
    def threaded_scan(self, ip):
        """Multi-threaded port scanning"""
        def worker():
            while True:
                try:
                    port = port_queue.get(timeout=1)
                    self.scan_port(ip, port)
                    port_queue.task_done()
                except:
                    break
        
        # Create thread pool
        import queue
        port_queue = queue.Queue()
        
        # Add ports to queue
        for port in self.ports:
            port_queue.put(port)
        
        # Start threads
        for _ in range(min(self.threads, len(self.ports))):
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()
        
        # Wait for completion
        port_queue.join()
    
    def scan(self):
        """Main scanning function"""
        print("=" * 60)
        print("Network Scanner v1.0")
        print("=" * 60)
        print(f"Starting scan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Resolve target
        ip = self.resolve_target()
        if not ip:
            return
        
        print(f"Scanning {len(self.ports)} ports...")
        print("-" * 40)
        
        # Perform scan
        start_time = datetime.now()
        self.threaded_scan(ip)
        end_time = datetime.now()
        
        # Display results
        print("-" * 40)
        print(f"Scan completed in {end_time - start_time}")
        print(f"Found {len(self.open_ports)} open ports:")
        
        if self.open_ports:
            print("\nOpen Ports Summary:")
            for port, banner in sorted(self.open_ports):
                service = self.get_service_name(port)
                print(f"  {port:>5} | {service:<15} | {banner}")
        else:
            print("No open ports found.")
    
    def get_service_name(self, port):
        """Get common service name for port"""
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS", 143: "IMAP",
            443: "HTTPS", 993: "IMAPS", 995: "POP3S", 1723: "PPTP",
            3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC"
        }
        return services.get(port, "Unknown")

def main():
    parser = argparse.ArgumentParser(description="Basic Network Scanner")
    parser.add_argument("target", help="Target hostname or IP address")
    parser.add_argument("-p", "--ports", help="Comma-separated list of ports (default: common ports)")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Socket timeout (default: 1)")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads (default: 100)")
    
    args = parser.parse_args()
    
    # Parse custom ports if provided
    ports = None
    if args.ports:
        try:
            ports = [int(p.strip()) for p in args.ports.split(",")]
        except ValueError:
            print("Error: Invalid port format. Use comma-separated numbers.")
            sys.exit(1)
    
    # Create and run scanner
    scanner = NetworkScanner(args.target, ports, args.timeout, args.threads)
    
    try:
        scanner.scan()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()