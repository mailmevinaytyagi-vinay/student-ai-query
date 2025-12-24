import streamlit as st
import matplotlib.pyplot as plt

from auth import authenticate
from llm_sql import english_to_sql
from db import fetch_data
from voice_input import listen_from_mic

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Student Data AI Query",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE INITIALIZATION
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
            st.success(f"Logged in as {role}")
            st.rerun()
        else:
            st.error("Invalid username or password")

# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------
else:
    # Sidebar
    st.sidebar.success(f"Role: {st.session_state.role}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.query = ""
        st.rerun()

    st.title("🎓 Student Data AI Query")
    st.write("Ask questions using **text or voice** (powered by Local LLM)")

    # --------------------------------------------------
    # UNIFIED INPUT (TEXT + VOICE)
    # --------------------------------------------------
    st.subheader("🔎 Ask your question")

    col1, col2 = st.columns([4, 1])

    # Text input
    with col1:
        typed_query = st.text_input(
            "Type your question:",
            value=st.session_state.query
        )

    # Voice input
    with col2:
        if st.button("🎤 Speak"):
            with st.spinner("Listening..."):
                spoken_query = listen_from_mic()
                st.session_state.query = spoken_query
                st.success(f"You said: {spoken_query}")

    # Decide final query (single source of truth)
    if typed_query:
        st.session_state.query = typed_query

    query = st.session_state.query

    # --------------------------------------------------
    # QUERY → SQL → DB
    # --------------------------------------------------
    if query:
        try:
            st.subheader("🧠 Interpreted Query")
            st.write(query)

            sql_query = english_to_sql(query)

            st.subheader("🧾 Generated SQL")
            st.code(sql_query, language="sql")

            df = fetch_data(sql_query)

            if df.empty:
                st.warning("No data found.")
            else:
                st.subheader("📋 Query Result")
                st.dataframe(df)

                # --------------------------------------------------
                # ADMIN-ONLY ANALYTICS
                # --------------------------------------------------
                if st.session_state.role == "admin":
                    st.divider()
                    st.subheader("📊 Admin Analytics")

                    col_a, col_b = st.columns(2)

                    # Marks Distribution
                    with col_a:
                        fig1, ax1 = plt.subplots()
                        ax1.hist(df["marks"], bins=10)
                        ax1.set_title("Marks Distribution")
                        ax1.set_xlabel("Marks")
                        ax1.set_ylabel("Number of Students")
                        st.pyplot(fig1)

                    # Class-wise Average Marks
                    with col_b:
                        avg_marks = df.groupby("class")["marks"].mean()
                        fig2, ax2 = plt.subplots()
                        avg_marks.plot(kind="bar", ax=ax2)
                        ax2.set_title("Class-wise Average Marks")
                        ax2.set_xlabel("Class")
                        ax2.set_ylabel("Average Marks")
                        st.pyplot(fig2)

                    # Top Scorers
                    st.subheader("🏆 Top Scorers")
                    top_students = df.sort_values("marks", ascending=False).head(5)
                    st.table(top_students)

        except Exception as e:
            st.error(str(e))
