import streamlit as st
import matplotlib.pyplot as plt

from auth import authenticate
from llm_sql import english_to_sql
from db import fetch_data

# Optional voice support (local only)
try:
    from voice_input import listen_from_mic
    VOICE_ENABLED = True
except Exception:
    VOICE_ENABLED = False

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Student Data AI Query", layout="wide")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.query = ""

# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------
if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = authenticate(username, password)
        if role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.rerun()
        else:
            st.error("Invalid username or password")

# --------------------------------------------------
# MAIN APP
# --------------------------------------------------
else:
    st.sidebar.success(f"Role: {st.session_state.role}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.query = ""
        st.rerun()

    st.title("🎓 Student Data AI Query")
    st.write("Ask questions using **text** (voice available in local app)")

    st.subheader("🔎 Ask your question")

    col1, col2 = st.columns([4, 1])

    with col1:
        typed_query = st.text_input(
            "Type your question:",
            value=st.session_state.query
        )

    with col2:
        if VOICE_ENABLED:
            if st.button("🎤 Speak"):
                spoken_query = listen_from_mic()
                st.session_state.query = spoken_query
                st.success(f"You said: {spoken_query}")
        else:
            st.caption("🎤 Voice input available only in local app")

    # ✅ SINGLE SOURCE OF TRUTH (NO INDENTATION ERROR)
    if typed_query:
        st.session_state.query = typed_query

    query = st.session_state.query

    # --------------------------------------------------
    # QUERY EXECUTION
    # --------------------------------------------------
    if query:
        try:
            sql_query = english_to_sql(query)
            st.code(sql_query, language="sql")

            df = fetch_data(sql_query)

            if df.empty:
                st.warning("No data found")
            else:
                st.dataframe(df)

                if st.session_state.role == "admin":
                    st.subheader("📊 Analytics")

                    fig, ax = plt.subplots()
                    ax.hist(df["marks"], bins=10)
                    ax.set_xlabel("Marks")
                    ax.set_ylabel("Students")
                    st.pyplot(fig)

        except Exception as e:
            st.error(str(e))
