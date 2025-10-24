# 🧠 AutoMind AI – Smart Email Automation Dashboard (Single File Version)
# ---------------------------------------------------------
import streamlit as st
import imaplib, email
from email.header import decode_header
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables (.env)
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# -----------------------------
# Helper Functions
# -----------------------------

def decode_header_value(hdr):
    if not hdr:
        return ""
    parts = decode_header(hdr)
    decoded = ""
    for text, enc in parts:
        if isinstance(text, bytes):
            decoded += text.decode(enc or "utf-8", errors="ignore")
        else:
            decoded += text
    return decoded


def fetch_latest_emails(limit=5):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        result, data = mail.search(None, "ALL")
        mail_ids = data[0].split()
        latest_ids = mail_ids[-limit:]

        emails = []
        for i in reversed(latest_ids):
            res, msg_data = mail.fetch(i, "(RFC822)")
            raw_msg = msg_data[0][1]
            msg = email.message_from_bytes(raw_msg)

            subject = decode_header_value(msg["Subject"])
            sender = decode_header_value(msg["From"])
            date = decode_header_value(msg["Date"])

            summary = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        try:
                            summary = part.get_payload(decode=True).decode("utf-8")[:120]
                        except:
                            pass
                        break
            else:
                summary = msg.get_payload(decode=True).decode("utf-8", errors="ignore")[:120]

            emails.append({
                "from": sender,
                "subject": subject,
                "date": date,
                "summary": summary
            })

        mail.logout()
        return emails

    except Exception as e:
        st.error(f"Error fetching emails: {e}")
        return []


# -----------------------------
# Streamlit Dashboard
# -----------------------------
st.set_page_config(page_title="AutoMind AI", layout="wide")
st.title("🧠 AutoMind AI – Smart Email Automation Dashboard")
st.markdown("### Manage your emails smartly with AI 💌")

col1, col2 = st.columns([1, 3])

with col1:
    limit = st.number_input("Number of latest emails to fetch:", 1, 20, 5)
    fetch_btn = st.button("📩 Fetch Emails")

with col2:
    if fetch_btn:
        if not EMAIL_USER or not EMAIL_PASS:
            st.error("⚠️ Please set EMAIL_USER and EMAIL_PASS in your .env file.")
        else:
            emails = fetch_latest_emails(limit)
            if emails:
                st.success(f"Fetched {len(emails)} emails successfully!")
                for em in emails:
                    with st.expander(f"📧 {em['subject']}"):
                        st.write(f"**From:** {em['from']}")
                        st.write(f"**Date:** {em['date']}")
                        st.write(f"**Summary:** {em['summary']}")
            else:
                st.warning("No emails found or failed to fetch.")
