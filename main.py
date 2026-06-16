import uvicorn
import os
from dotenv import load_dotenv
from config.logging import log_config

load_dotenv()


ENVIRONMENT = os.environ.get("ENVIRONMENT", "PROD")
DEBUG = True if ENVIRONMENT == "DEBUG" else False
DEV = True if ENVIRONMENT == "DEV" else False
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 8080))

SSL_CERT = os.environ.get("SSL_CERT")
SSL_KEY = os.environ.get("SSL_KEY")
ACCESS_KEY = os.environ.get("ACCESS_KEY")

log_level = ""
if DEBUG:
    log_level = "debug"

if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host=HOST,
        port=PORT,
        log_level=log_level,
        log_config=log_config,
        reload=DEV,
        ssl_certfile=SSL_CERT,
        ssl_keyfile=SSL_KEY,
    )
