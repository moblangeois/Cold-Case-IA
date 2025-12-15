# SSL Certificates

This directory should contain your SSL certificates for HTTPS.

## For Production (Let's Encrypt - Recommended)

```bash
# Install certbot
sudo apt install certbot

# Generate certificates
sudo certbot certonly --standalone -d coldcase.citadelle.work

# Copy to this directory
sudo cp /etc/letsencrypt/live/coldcase.citadelle.work/fullchain.pem ./cert.pem
sudo cp /etc/letsencrypt/live/coldcase.citadelle.work/privkey.pem ./key.pem
```

## For Development (Self-Signed)

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout key.pem \
  -out cert.pem \
  -subj "/CN=localhost"
```

## Required Files

- `cert.pem` - SSL certificate
- `key.pem` - Private key

**Note:** These files are gitignored for security. Never commit SSL private keys to version control.
