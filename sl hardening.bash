sudo nginx -t && sudo systemctl reload nginx

# Check with OpenSSL
openssl s_client -connect example.com:443 -status </dev/null 2>/dev/null | sed -n '/OCSP response/,$p'

sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow HTTPS / HTTP
sudo ufw allow 443/tcp
sudo ufw allow 80/tcp

# Restrict SSH to your office/home IP (replace x.x.x.x)
sudo ufw allow from x.x.x.x to any port 22 proto tcp

sudo ufw enable
sudo ufw status numbered

sudo systemctl restart fail2ban

sudo apt update
sudo apt install certbot python3-certbot-nginx -y

# Obtain cert
sudo certbot --nginx -d example.com -d www.example.com

# Test renewal
sudo certbot renew --dry-run

