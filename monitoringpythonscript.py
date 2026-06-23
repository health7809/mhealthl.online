#!/usr/bin/env python3
import ssl, socket, hashlib
from datetime import datetime, timezone
import smtplib
from email.message import EmailMessage

HOST = "example.com"
PORT = 443
ALERT_EMAIL = "you@example.com"
SMTP_HOST = "smtp.example.com"
SMTP_USER = "alert@example.com"
SMTP_PASS = "your-smtp-pass"
FINGERPRINT_FILE = "/var/lib/cert_monitor/example_com_fp.txt"
WARN_DAYS = 30

def get_cert(host, port=443):
    ctx = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=10) as s:
        with ctx.wrap_socket(s, server_hostname=host) as ss:
            der = ss.getpeercert(True)
            cert = ssl.DER_cert_to_PEM_cert(der)
            info = ss.getpeercert()
            return der, cert, info

def sha256_fp(der_bytes):
    return hashlib.sha256(der_bytes).hexdigest()

def send_alert(subject, body):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = ALERT_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(SMTP_HOST, 587) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)

def main():
    der, pem, info = get_cert(HOST, PORT)
    fp = sha256_fp(der)
    notAfter = info.get("notAfter")
    expires = datetime.strptime(notAfter, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
    days_left = (expires - datetime.now(timezone.utc)).days

    try:
        old_fp = open(FINGERPRINT_FILE).read().strip()
    except FileNotFoundError:
        old_fp = None

    if old_fp is None:
        open(FINGERPRINT_FILE, "w").write(fp)
    elif old_fp != fp:
        send_alert(f"Certificate fingerprint changed for {HOST}",
                   f"Old: {old_fp}\nNew: {fp}\nExpires: {expires.isoformat()}")
        open(FINGERPRINT_FILE, "w").write(fp)

    if days_left <= WARN_DAYS:
        send_alert(f"Certificate expiry warning for {HOST}",
                   f"Certificate expires in {days_left} days on {expires.isoformat()}")

if __name__ == "__main__":
    main()
