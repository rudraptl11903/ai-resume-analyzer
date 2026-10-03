"""
recommendations.py
Smart Career & Resume Recommendations Page.
Provides XYZ-formula bullet rewrites, high-impact project suggestions, and interview prep guidance.
"""

import os
import sys
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

st.set_page_config(page_title="Recommendations | AI Resume Analyzer", page_icon="💡", layout="wide")

st.title("💡 Smart Resume & Placement Recommendations")
st.markdown("Proven engineering strategies to elevate your resume for software engineering internships and placements.")

resume = st.session_state.get("resume_data")

tab1, tab2, tab3 = st.tabs(["✍️ Bullet Point Optimizer (Google XYZ)", "🛠️ High-Impact Project Ideas", "🎯 Interview Preparation"])

with tab1:
    st.subheader("The Google 'XYZ' Formula for Engineering Bullets")
    st.info("Formula: **Accomplished [X] as measured by [Y], by doing [Z]**")

    st.markdown("#### ❌ Common Weak Bullets vs. ✅ High-Impact Rewrites")

    examples = [
        {
            "weak": "Worked on a web application using React and Python.",
            "strong": "Engineered a full-stack job application tracker using React and FastAPI, reducing manual application logging time by 45% for 200+ active student users."
        },
        {
            "weak": "Responsible for writing backend database queries and bug fixes.",
            "strong": "Optimized PostgreSQL relational queries and added Redis caching, decreasing API endpoint response latency from 680ms to 110ms under peak simulated load."
        },
        {
            "weak": "Created a machine learning model to classify images.",
            "strong": "Trained and deployed a PyTorch convolutional neural network (CNN) reaching 94.2% top-1 accuracy on medical imaging, packaged inside a Dockerized microservice."
        }
    ]

    for eg in examples:
        with st.container():
            st.markdown(f"**Weak:** `{eg['weak']}`")
            st.success(f"**Optimized:** {eg['strong']}")
            st.write("")

with tab2:
    st.subheader("Standout Portfolio Projects for Placements")
    st.markdown("Recruiters and hiring managers look for complete, deployed systems with tests and clean README documentation.")

    p1, p2 = st.columns(2)
    with p1:
        with st.expander("⚡ Distributed Task Queue / Rate Limiter", expanded=True):
            st.markdown("""
            - **Tech Stack:** Python, Redis, Docker, FastAPI
            - **Why it stands out:** Demonstrates deep systems thinking, concurrency, asynchronous background jobs, and backend architecture beyond basic CRUD.
            - **Key Metric:** Handles 5,000+ requests/sec with Token Bucket algorithm.
            """)

        with p1:
            with st.expander("📊 Real-Time Financial / Log Streaming Pipeline", expanded=True):
                st.markdown("""
                - **Tech Stack:** Kafka / RabbitMQ, Python, WebSockets, TimescaleDB / SQLite
                - **Why it stands out:** Shows familiarity with message brokers, event-driven pipelines, and distributed data.
                """)

    with p2:
        with st.expander("📄 AI Resume Analyzer & Job Matcher (This Project!)", expanded=True):
            st.markdown("""
            - **Tech Stack:** Streamlit, Scikit-Learn (TF-IDF), spaCy / NLTK, PyMuPDF, SQLite
            - **Why it stands out:** Solves a real problem, zero paid API dependencies, clean modular Python architecture, explainable ML metrics.
            """)

        with p2:
            with st.expander("🔐 Role-Based Access Auth Microservice", expanded=True):
                st.markdown("""
                - **Tech Stack:** Python / Go, JWT, OAuth2, Bcrypt, Unit Testing
                - **Why it stands out:** Demonstrates secure software design, hashing, stateless authentication, and enterprise reliability.
                """)

with tab3:
    st.subheader("Placement Interview Readiness Checklist")
    c_prep1, c_prep2 = st.columns(2)
    with c_prep1:
        st.markdown("##### 💻 Technical & Coding Round")
        st.checkbox("Master Core Data Structures (Arrays, Hash Maps, Trees, Graphs)")
        st.checkbox("Practice 75 Blind / NeetCode LeetCode problems")
        st.checkbox("Explain Big-O Time & Space Complexity fluently")
        st.checkbox("Be ready to write unit tests for edge cases on a whiteboard / shared IDE")

    with c_prep2:
        st.markdown("##### 🗣️ Engineering & Behavioral Round")
        st.checkbox("Prepare 2-minute elevator pitch highlighting this portfolio project")
        st.checkbox("Explain trade-offs: Why TF-IDF vs deep embeddings? Why PyMuPDF over OCR?")
        st.checkbox("Structure answers using STAR (Situation, Task, Action, Result)")
        st.checkbox("Prepare 3 thoughtful questions for the engineering team about their stack")
