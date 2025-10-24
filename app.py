import streamlit as st
from dotenv import load_dotenv
import os
from imap_client import fetch_latest_headers
from db import init_db

# .env file load karo (gmail credentials)
load_dotenv()

# Streamlit basic setup
st.set_page_config(page_title="AutoMind AI", layout="wide")
st.title("AutoMind AI — Email Automation Dashboard")

# Initialize SQLite database
init_db()

# Button to fetch email headers
if st.button("Fetch latest 5 emails (headers)"):
    try:
        headers = fetch_latest_headers(limit=5)
        st.write("Fetched headers:")
        for h in headers:
            st.markdown(f"**From:** {h.get('from')}  \n**Subject:** {h.get('subject')}  \n**Date:** {h.get('date')}")
    except Exception as e:
        st.error(f"Error: {e}")

st.info("Step 1: Streamlit + IMAP test. When this works, we’ll move to Step 2 (summarization).")
