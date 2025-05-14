from pydantic import BaseModel, HttpUrl

class SiteRequest(BaseModel):
    url: str

class SiteResponse(BaseModel):
    url: str
    status: str
    response_time: float

class PortInfo(BaseModel):
    port: int
    service: str

class NmapResponse(BaseModel):
    host: str
    open_ports: list[PortInfo]
    scan_time: float
    ports_scanned: int

class DNSResponse(BaseModel):
	domain: str
	ip_addresses: list[str]
	record_type: str
	success: bool