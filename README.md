## Create self-signed cert
```bash
openssl req -x509 -newkey rsa:4096 -subj '/CN=aruljohn.com/C=US' -new -sha256 -days 3650 -nodes -keyout key.pem -out cert.pem
```