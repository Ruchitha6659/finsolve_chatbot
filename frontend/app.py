import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="FinSolve Chatbot", page_icon="💬", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def login_page():
    st.title("🔐 FinSolve Chatbot")
    st.subheader("Login to continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if not username or not password:
            st.error("Please enter username and password")
            return
        try:
            response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            if response.status_code == 200:
                data = response.json()
                st.session_state.logged_in = True
                st.session_state.username = data["username"]
                st.session_state.role = data["role"]
                st.session_state.chat_history = []
                st.rerun()
            else:
                st.error("Invalid username or password")
        except Exception as e:
            st.error(f"Cannot connect to server: {e}")
    with st.expander("Available test users"):
        st.markdown("""
        | Username | Password | Role |
        |---|---|---|
        | alice | alice123 | finance |
        | bob | bob123 | hr |
        | charlie | charlie123 | marketing |
        | diana | diana123 | engineering |
        | eve | eve123 | c_level |
        | frank | frank123 | employee |
        """)

def chat_page():
    st.title("💬 FinSolve Chatbot")
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"👤 **{st.session_state.username}**")
    with col2:
        st.markdown(f"🔑 **{st.session_state.role}**")
    with col3:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.session_state.chat_history = []
            st.rerun()
    st.divider()
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["question"])
        with st.chat_message("assistant"):
            st.write(chat["answer"])
            if chat["sources"]:
                st.caption(f"📄 Sources: {', '.join(chat['sources'])}")
    question = st.chat_input("Ask something...")
    if question:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(f"{API_URL}/chat", json={"question": question, "role": st.session_state.role})
                    if response.status_code == 200:
                        data = response.json()
                        st.write(data["answer"])
                        if data["sources"]:
                            st.caption(f"📄 Sources: {', '.join(data['sources'])}")
                        st.session_state.chat_history.append({"question": question, "answer": data["answer"], "sources": data["sources"]})
                    else:
                        st.error("Something went wrong. Try again.")
                except Exception as e:
                    st.error(f"Cannot connect to server: {e}")

def main():
    if st.session_state.logged_in:
        chat_page()
    else:
        login_page()

if __name__ == "__main__":
    main()