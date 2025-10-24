import streamlit as st
import random
from datetime import datetime
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

# -----------------------------
# Initialize AI Models
# -----------------------------
st.set_page_config(page_title="AutoMind AI Pro", layout="wide")
st.title("🧠 AutoMind AI Pro — Ultimate Interactive Dashboard")

st.markdown("### ✨ Features: AI Q&A, Plagiarism Checker, Summarizer, Word Extractor, Chatbot, Quotes, Tasks")

# AI Question Answering pipeline (HuggingFace)
@st.cache_resource(show_spinner=False)
def load_qa_model():
    return pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

qa_model = load_qa_model()

# -----------------------------
# Global States
# -----------------------------
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Helper Functions
# -----------------------------

# Task Manager
def add_task(task):
    if task:
        st.session_state.tasks.append({"task": task, "time": datetime.now().strftime("%H:%M:%S")})

def remove_task(index):
    st.session_state.tasks.pop(index)

# Summarizer (first 3 sentences)
def summarize_text(text):
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return " ".join(sentences[:3]) + ("..." if len(sentences) > 3 else "")

# Word Extractor
def extract_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return sorted(set(words))

# Mini Chatbot
def chatbot_reply(user_input):
    user_input = user_input.lower()
    greetings = ["hi", "hello", "hey"]
    if any(g in user_input for g in greetings):
        return random.choice(["Hello! How are you?", "Hey there! 😊", "Hi! Nice to meet you!"])
    elif "your name" in user_input:
        return "I am AutoMind AI Pro 🤖, your interactive assistant!"
    elif "task" in user_input:
        return f"You currently have {len(st.session_state.tasks)} tasks."
    elif "quote" in user_input:
        return random.choice(quotes)
    else:
        return "I am learning every day! 😄"

# Plagiarism Checker (basic cosine similarity)
def check_plagiarism(text, reference):
    vectorizer = TfidfVectorizer().fit_transform([text, reference])
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
    return round(float(similarity[0][0])*100,2)

# -----------------------------
# UI Sections
# -----------------------------
quotes = [
    "Believe in yourself! 💪",
    "Every day is a new opportunity 🌟",
    "Success is the sum of small efforts repeated daily 🚀",
    "Keep pushing forward, no matter what 🌈"
]

# -----------------------------
# Column Layout
# -----------------------------
col1, col2 = st.columns([1,2])

# ----------- Column 1 -----------
with col1:
    st.subheader("💡 Daily Inspiration")
    if st.button("Generate Quote"):
        st.info(random.choice(quotes))

    st.subheader("📝 Task Manager")
    task_input = st.text_input("Enter a new task:")
    if st.button("Add Task"):
        add_task(task_input)
    for idx, t in enumerate(st.session_state.tasks):
        st.write(f"{idx+1}. {t['task']} (added at {t['time']})")
        if st.button(f"Remove {idx+1}", key=f"r{idx}"):
            remove_task(idx)

# ----------- Column 2 -----------
with col2:
    st.subheader("✂️ Text Summarizer")
    text_to_summarize = st.text_area("Paste text here:")
    if st.button("Summarize Text"):
        summary = summarize_text(text_to_summarize)
        st.success(summary)

    st.subheader("📝 Word Extractor")
    text_for_words = st.text_area("Paste text to extract words:")
    if st.button("Extract Words"):
        words = extract_words(text_for_words)
        st.write(f"**Unique Words ({len(words)}):**")
        st.write(words)

    st.subheader("🤖 Mini Chatbot")
    user_msg = st.text_input("Talk to AutoMind AI:")
    if st.button("Send Message"):
        reply = chatbot_reply(user_msg)
        st.session_state.chat_history.append({"user": user_msg, "bot": reply})
        st.info(f"AutoMind AI: {reply}")
    if st.session_state.chat_history:
        st.write("**Chat History:**")
        for chat in st.session_state.chat_history:
            st.write(f"**You:** {chat['user']}")
            st.write(f"**AI:** {chat['bot']}")

    st.subheader("❓ AI Question Answering")
    context_text = st.text_area("Paste context / paragraph here for AI Q&A")
    question = st.text_input("Enter your question:")
    if st.button("Get Answer"):
        if context_text.strip() and question.strip():
            answer = qa_model(question=question, context=context_text)
            st.success(f"Answer: {answer['answer']}")
        else:
            st.warning("Please provide context and a question.")

    st.subheader("📋 Plagiarism Checker")
    original_text = st.text_area("Paste original/reference text")
    check_text = st.text_area("Paste text to check for plagiarism")
    if st.button("Check Plagiarism"):
        if original_text.strip() and check_text.strip():
            score = check_plagiarism(check_text, original_text)
            st.success(f"Similarity: {score}%")
        else:
            st.warning("Please provide both texts for comparison.")

# -----------------------------
# Analytics
# -----------------------------
st.subheader("📊 Task Analytics")
num_tasks = len(st.session_state.tasks)
st.bar_chart({"Number of tasks": [num_tasks]})
