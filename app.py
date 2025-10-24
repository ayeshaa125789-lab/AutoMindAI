import streamlit as st
import random
from datetime import datetime

# -----------------------------
# Extra Features (No .env needed)
# -----------------------------

# Inspirational Quotes
quotes = [
    "Believe in yourself! 💪",
    "Every day is a new opportunity 🌟",
    "Success is the sum of small efforts repeated daily 🚀",
    "Keep pushing forward, no matter what 🌈"
]

# Simple To-Do List
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

def add_task(task):
    if task:
        st.session_state.tasks.append({"task": task, "time": datetime.now().strftime("%H:%M:%S")})

def remove_task(index):
    st.session_state.tasks.pop(index)

# Simple Text Summarizer (2-line summary)
def summarize_text(text):
    lines = text.strip().split('\n')
    if len(lines) > 2:
        return "\n".join(lines[:2]) + "..."
    return text

# -----------------------------
# Streamlit Dashboard
# -----------------------------
st.set_page_config(page_title="AutoMind AI + Extras", layout="wide")
st.title("🧠 AutoMind AI Dashboard — Email + Extras")

st.markdown("### ✨ Fun Features (No Email Required)")

# -----------------------------
# Inspirational Quote
# -----------------------------
st.subheader("💡 Daily Inspiration")
if st.button("Generate Quote"):
    st.info(random.choice(quotes))

# -----------------------------
# To-Do List
# -----------------------------
st.subheader("📝 Task Manager")
task_input = st.text_input("Enter a new task:")
if st.button("Add Task"):
    add_task(task_input)

for idx, t in enumerate(st.session_state.tasks):
    st.write(f"{idx+1}. {t['task']} (added at {t['time']})")
    if st.button(f"Remove {idx+1}", key=idx):
        remove_task(idx)

# -----------------------------
# Text Summarizer
# -----------------------------
st.subheader("✂️ Mini Text Summarizer")
text_to_summarize = st.text_area("Paste your text here:")
if st.button("Summarize Text"):
    summary = summarize_text(text_to_summarize)
    st.success(summary)

# -----------------------------
# Simple Analytics
# -----------------------------
st.subheader("📊 Task Analytics")
num_tasks = len(st.session_state.tasks)
st.bar_chart({"Number of tasks": [num_tasks]})
