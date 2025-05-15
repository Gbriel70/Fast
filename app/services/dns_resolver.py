from dns.exception import DNSException
from dns.resolver import Resolver, NoAnswer, NXDOMAIN
import subprocess
import socket
import time
from typing import Dict, Any, List
import urllib.parse

async def resolve_dns(url: str) -> Dict[str, Any]:
    """Resolve DNS para obter endereços IP e registros CNAME de um domínio."""
    start_time = time.time()
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc or parsed_url.path
        
        if ':' in domain:
            domain = domain.split(':')[0]
            
        print(f"Resolving domain: {domain}")
        
        ip_addresses = []
        cname_records = []
        
        try:
            result = subprocess.check_output(['nslookup', '-type=CNAME', domain], universal_newlines=True, stderr=subprocess.STDOUT, timeout=5)
            print(f"nslookup CNAME result: {result}")
            
            for line in result.split('\n'):
                if 'canonical name' in line.lower():
                    cname = line.split('=', 1)[1].strip()
                    # Remover o ponto final se existir
                    if cname.endswith('.'):
                        cname = cname[:-1]
                    cname_records.append(cname)
            
            ip_result = subprocess.check_output(['nslookup', domain], universal_newlines=True, stderr=subprocess.STDOUT, timeout=5)
            for line in ip_result.split('\n'):
                if 'Address:' in line and not 'server' in line.lower():
                    ip = line.split(':', 1)[1].strip()
                    if ip and all(c.isdigit() or c == '.' for c in ip):  # Verificar se é formato IPv4
                        ip_addresses.append(ip)
        except Exception as e:
            print(f"nslookup error: {str(e)}")
            
        if not ip_addresses or not cname_records:
            resolver = Resolver()
            resolver.timeout = 3.0
            resolver.nameservers = ['8.8.8.8', '8.8.4.4']
            
            try:
                if not ip_addresses:
                    a_answers = resolver.resolve(domain, 'A')
                    ip_addresses = [answer.address for answer in a_answers]
            except Exception as e:
                print(f"DNS resolver A record error: {str(e)}")
                
            try:
                if not cname_records:
                    cname_answers = resolver.resolve(domain, 'CNAME')
                    cname_records = [str(answer.target).rstrip('.') for answer in cname_answers]
            except Exception as e:
                print(f"DNS resolver CNAME record error: {str(e)}")
                
        if not ip_addresses:
            try:
                socket_result = socket.gethostbyname(domain)
                ip_addresses = [socket_result]
            except Exception as e:
                print(f"Socket error: {str(e)}")
        
        end_time = time.time()
        
        return {
            "domain": domain,
            "ip_addresses": ip_addresses,
            "cname_records": cname_records,
            "record_types": ['A', 'CNAME'] if cname_records else ['A'],
            "success": True,
            "resolution_time": round(end_time - start_time, 3)
        }

    except Exception as e:
        end_time = time.time()
        print(f"DNS resolution error: {str(e)}")
        
        return {
            "domain": domain if 'domain' in locals() else url,
            "ip_addresses": [],
            "cname_records": [],
            "record_types": [],
            "success": False,
            "error": str(e),
            "resolution_time": round(end_time - start_time, 3)
        }