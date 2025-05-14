from dns.exception import DNSException
from dns.resolver import Resolver
from typing import Dict, Any, List

def resolve_dns(url: str) -> Dict[str, Any]:

	if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

	try:
		resolver = Resolver()
		resolver.timeout = timeout

		answers = resolver.resolve(url, 'A')
		ip_addresses = [answer.address for answer in answers]

		return {
			"domain" : url,
			"ip_addresses": ip_addresses,
			"record_type": 'A',
			"success": True
		}

	except DNSException as e:
		return {
			"domain": url,
			"ip_addresses": [],
			"record_type": 'A',
			"success": False
		}