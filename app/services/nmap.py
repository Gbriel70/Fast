import socket
import asyncio
from typing import Dict, Any, List
from urllib.parse import urlparse
import time

async def scan_port(host: str, port: int, timeout: float = 3.0) -> Dict[str, Any]:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: sock.connect_ex((host, port)) == 0
        )

        sock.close()
        return result
    except socket.error:
        return False
    

async def port_scan(url: str, max_ports = 10000, common_only = True) -> Dict[str, Any]:
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    parsed_url = urlparse(url)
    host = parsed_url.netloc
    
    if not host or host in ['localhost', '127.0.0.1']:
        return {
            "host": url,
            "open_ports": [],
            "scan_time": 0,
            "ports_scanned": 0,
            "error": "Invalid or local host specified"
        }
    
    common_services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        465: "SMTPS",
        587: "SMTP",
        993: "IMAPS",
        995: "POP3S",
        1433: "MSSQL",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        8080: "HTTP-Proxy",
        8443: "HTTPS-Alt"
    }

    start_time = time.time()
    open_ports = []
    ports_to_scan = list(common_services.keys()) if common_only else range(1, max_ports + 1)
    ports_count = len(ports_to_scan)
    
    timeout = 1.0
    batch_size = 20
    port_batches = [ports_to_scan[i:i+batch_size] for i in range(0, len(ports_to_scan), batch_size)]

    for batch in port_batches:
        tasks = []
        for port in batch:
            tasks.append(scan_port(host, port, timeout))

        batch_results = await asyncio.gather(*tasks)

        for i, is_open in enumerate(batch_results):
            port = batch[i]
            if is_open:
                service = common_services.get(port, "Unknown")
                open_ports.append({
                    "port": port, 
                    "service": service
                })
                
    scan_time = time.time() - start_time

    return {
        "host": host,
        "open_ports": open_ports,
        "scan_time": round(scan_time, 2),
        "ports_scanned": ports_count
    }