from ipaddress import ip_address
import logging

from anyio import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
import geoip2.database

from main import ProductionMode, mode, ACCESS_KEYS

app = FastAPI(title="geoip")
logger = logging.getLogger("uvicorn.default")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

DB_PATH = Path(".") / "db" / "GeoLite2-City.mmdb"


@app.middleware("auth")
async def auth_middleware(request: Request, call_next):
    if request.headers.get("X-API-KEY") not in ACCESS_KEYS:
        return JSONResponse({"detail": "Not authorized"}, status_code=403)

    response = await call_next(request)
    return response


def get_ip_header(request: Request) -> str:
    ip = request.client.host if request.client else ""
    if mode != ProductionMode.PROD:
        ip = request.headers.get("Host") or ip

    return ip


def validate_ip(IP: str) -> str:
    def validIPAddress(IP: str) -> bool:
        try:
            type(ip_address(IP))
            return True
        except ValueError:
            return False

    if not validIPAddress(IP):
        return (
            "IPv4 or IPv6 address is in an incorrect format."
            + " You sent: " + IP
        )
    ip_addr = ip_address(IP)
    if ip_addr.is_link_local or ip_addr.is_loopback:
        return "You are on localhost"
    if ip_addr.is_private:
        return "You are on a private network"

    return ""


def lookup_ip_address(IP: str):
    reader = geoip2.database.Reader(DB_PATH)
    response = reader.city(IP)
    result = {
        "country_code": response.country.iso_code,
        "country_name": response.country.name,
        "region_name": response.subdivisions.most_specific.name or "",
        "city": response.city.name or "",
        "ip": IP,
    }
    return result


@app.get("/")
@limiter.limit("5/minute")
def get_myip(request: Request):
    ip = get_ip_header(request).strip()

    error = validate_ip(ip)
    if error != "":
        return JSONResponse({"detail": error})

    result = lookup_ip_address(ip)
    return JSONResponse(result)


@app.get("/geolookup")
@limiter.limit("60/minute")
def get_geolookup(request: Request, ip: str):
    ip = ip.strip()
    error = validate_ip(ip)
    if error != "":
        return JSONResponse({"detail": error})

    result = lookup_ip_address(ip)
    return JSONResponse(result)
