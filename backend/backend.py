"""Simple Flask service that proxies job information via SSH."""

import logging
import os
import threading
import time
from typing import List

import paramiko
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

SSH_HOST = os.getenv("SSH_HOST", "cardinal.osc.edu")
SSH_USER = os.getenv("SSH_USER")
SSH_PASS = os.getenv("SSH_PASS")
SQUEUE_COMMAND = os.getenv("SQUEUE_COMMAND", "squeue -A pys0302")
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", "10"))

if not SSH_USER or not SSH_PASS:
    logging.warning("SSH credentials are not set. Job data fetching will fail.")

job_data: List[dict] = []
job_lock = threading.Lock()


def fetch_job_data() -> None:
    """Continuously retrieve job data via SSH and cache the result."""

    global job_data
    while True:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASS)
            stdin, stdout, _ = ssh.exec_command(SQUEUE_COMMAND)
            output = stdout.read().decode()
            ssh.close()

            lines = output.strip().split("\n")
            headers = lines[0].split()
            jobs = [dict(zip(headers, line.split(None, len(headers) - 1))) for line in lines[1:]]

            with job_lock:
                job_data = jobs
            logging.info("Fetched %d jobs", len(jobs))
        except Exception as exc:  # pylint: disable=broad-except
            logging.exception("Failed to fetch jobs: %s", exc)
            with job_lock:
                job_data = [{"error": str(exc)}]
        time.sleep(FETCH_INTERVAL)


@app.route("/")
def hello():
    return "Hello from Python Flask Microservice!"


@app.route("/jobs")
def get_jobs():
    with job_lock:
        return jsonify(job_data)


if __name__ == "__main__":
    threading.Thread(target=fetch_job_data, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
