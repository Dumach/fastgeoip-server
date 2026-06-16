from ipaddress import ip_address

from anyio import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import geoip2.database

from main import DEBUG, ACCESS_KEY

app = FastAPI()
DB_PATH = Path(".") / "db" / "GeoLite2-City.mmdb"


@app.middleware("auth")
async def auth(request: Request, call_next):
    if request.headers.get("X-API-KEY") != ACCESS_KEY:
        return JSONResponse({"detail": "Not found"}, status_code=404)

    response = await call_next(request)
    return response


def get_ip_header(request: Request) -> str:
    ip = request.client.host if request.client else ""
    if DEBUG:
        ip = request.headers.get("Host") or ""

    return ip


def validate_ip(IP: str) -> str:
    def validIPAddress(IP: str) -> bool:
        try:
            type(ip_address(IP))
            return True
        except ValueError:
            return False

    if not validIPAddress(IP):
        return """IPv4 or IPv6 address is in an incorrect format.
            Dotted decimal for IPv4 or textual representation for IPv6 are required."""
    ip_addr = ip_address(IP)
    if ip_addr.is_link_local or ip_addr.is_loopback:
        return "You are on localhost"

    return ""


def lookup_ip_address(IP: str):
    reader = geoip2.database.Reader(DB_PATH)
    response = reader.city(IP)
    result = {
        "geoInfo": {
            "countryCode": response.country.iso_code,
            "country": response.country.name,
            "county": response.subdivisions.most_specific.name or "",
            "city": response.city.name or "",
        },
        "ipAddress": IP,
    }
    return result


@app.get("/")
def get_myip(request: Request):
    ip = get_ip_header(request)

    error = validate_ip(ip)
    if error != "":
        return JSONResponse({"detail": error})

    result = lookup_ip_address(ip)
    return JSONResponse({"detail": "success", "result": result})


@app.get("/geolookup")
def get_geolookup(ip: str):
    error = validate_ip(ip)
    if error != "":
        return JSONResponse({"detail": error})

    result = lookup_ip_address(ip)
    return JSONResponse({"detail": "success", "result": result})
