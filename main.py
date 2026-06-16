import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()


ENVIRONMENT = os.environ.get("ENVIRONMENT", "PROD")
DEBUG = True if ENVIRONMENT == "DEBUG" else False
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 8080))

SSL_CERT = os.environ.get("SSL_CERT")
SSL_KEY = os.environ.get("SSL_KEY")
ACCESS_KEY = os.environ.get("ACCESS_KEY")

if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host=HOST,
        port=PORT,
        log_level="info",
        reload=DEBUG,
        ssl_certfile=SSL_CERT,
        ssl_keyfile=SSL_KEY,
    )
