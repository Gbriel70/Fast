from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services.ping import ping_site
from services.nmap import port_scan
from schemas.site_schemas import SiteRequest, SiteResponse, NmapResponse, DNSResponse
import os

router = APIRouter()

templates_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
templates = Jinja2Templates(directory=templates_path)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.post("/ping", response_model=SiteResponse)
async def check_site(request: SiteRequest):
    result = await ping_site(request.url)
    return result

@router.post("/nmap", response_model=NmapResponse)
async def scan_ports(request: SiteRequest):
    result = await port_scan(request.url)
    return result

@router.post("/dns", response_model=DNSResponse)
async def resolve_dns(request: SiteRequest):
	result = await resolve_dns(request.url)
	return result