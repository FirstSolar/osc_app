import streamlit as st
import os
import requests
from streamlit_autorefresh import st_autorefresh

BACKEND_URL = os.getenv("BACKEND_URL", "http://job-backend:5000")

st.set_page_config(page_title="Job Monitor", layout="wide")
st_autorefresh(interval=10_000, key="refresh")

st.markdown(
    """
    <style>
    body {
        background-color: #f3f3f3;
        font-family: 'Segoe UI', sans-serif;
    }
    .tile {
        background-color: #0078D7;
        color: white;
        padding: 20px;
        margin: 10px;
        border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        width: 300px;
    }
    .tile:hover {
        transform: scale(1.02);
    }
    .tile h3 {
        margin: 0;
        font-size: 1.2rem;
    }
    .tile p {
        margin: 5px 0 0;
        font-size: 0.9rem;
    }
    .grid-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🧩 Windows-Style Job Queue Dashboard")

try:
    response = requests.get(f"{BACKEND_URL}/jobs")
    jobs = response.json() if response.ok else [{"error": "Failed to fetch job data"}]
except Exception as e:
    jobs = [{"error": str(e)}]

if jobs and "error" not in jobs[0]:
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)
    for job in jobs:
        st.markdown(
            f"""
            <div class="tile">
                <h3>Job ID: {job.get('JOBID')}</h3>
                <p><strong>Name:</strong> {job.get('NAME')}</p>
                <p><strong>User:</strong> {job.get('USER')}</p>
                <p><strong>Status:</strong> {job.get('ST')}</p>
                <p><strong>Time:</strong> {job.get('TIME')}</p>
                <p><strong>Nodes:</strong> {job.get('NODES')}</p>
                <p><strong>Node List:</strong> {job.get('NODELIST(REASON)')}</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error(jobs[0].get("error", "Unknown error"))
