import imapclient
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
load_dotenv()

IMAP_HOST = os.getenv("IMAP_HOST", "imap.gmail.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", 993))
USER = os.getenv("GMAIL_USER")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def _decode_header(h):
    if not h:
        return ""
    parts = decode_header(h)
    out = ""
    for text, enc in parts:
        if isinstance(text, bytes):
            out += text.decode(enc or "utf-8", errors="ignore")
        else:
            out += text
    return out

def fetch_latest_headers(limit=5):
    if not USER or not PASSWORD:
        raise ValueError("Missing GMAIL_USER or GMAIL_APP_PASSWORD in .env")

    server = imapclient.IMAPClient(IMAP_HOST, port=IMAP_PORT, ssl=True, use_uid=True)
    server.login(USER, PASSWORD)
    server.select_folder("INBOX", readonly=True)
    uids = server.search(['ALL'])
    uids = sorted(uids, reverse=True)[:limit]
    headers = []
    for uid in uids:
        raw = server.fetch(uid, ['RFC822'])[uid][b'RFC822']
        msg = email.message_from_bytes(raw)
        hdr = {
            'from': _decode_header(msg.get('From')),
            'subject': _decode_header(msg.get('Subject')),
            'date': _decode_header(msg.get('Date'))
        }
        headers.append(hdr)
    server.logout()
    return headers
