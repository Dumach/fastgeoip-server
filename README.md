## Create self-signed cert
```bash
openssl req -x509 -newkey rsa:4096 -subj '/CN=aruljohn.com/C=US' -new -sha256 -days 3650 -nodes -keyout key.pem -out cert.pem
```

# Create socket directory
sudo mkdir -p /var/run/uvicorn
sudo chown www-data:www-data /var/run/uvicorn

# Reload systemd configuration
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable fastgeoip-server.socket
sudo systemctl enable fastgeoip-server.service
sudo systemctl start fastgeoip-server.socket
sudo systemctl start fastgeoip-server.service

# Check status
sudo systemctl status fastgeoip-server.service

# View logs
sudo journalctl -u fastgeoip-server.service -f

# Graceful reload (zero downtime)
sudo systemctl reload fastgeoip-server.service

# Restart (brief downtime)
sudo systemctl restart fastgeoip-server.service

# Stop the service
sudo systemctl stop fastgeoip-server.service