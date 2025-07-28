from flask import Flask, jsonify
import os
import paramiko
import threading
import time

app = Flask(__name__)

SSH_HOST = os.getenv("SSH_HOST", "cardinal.osc.edu")
SSH_USER = os.getenv("SSH_USER", "")
SSH_PASS = os.getenv("SSH_PASS", "")
SQUEUE_COMMAND = os.getenv("SQUEUE_COMMAND", "squeue -A pys0302")

job_data = []

def fetch_job_data():
    global job_data
    while True:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASS)
            stdin, stdout, stderr = ssh.exec_command(SQUEUE_COMMAND)
            output = stdout.read().decode()
            ssh.close()

            lines = output.strip().split('\n')
            headers = lines[0].split()
            jobs = [dict(zip(headers, line.split(None, len(headers) - 1))) for line in lines[1:]]
            job_data = jobs
        except Exception as e:
            job_data = [{"error": str(e)}]
        time.sleep(10)

threading.Thread(target=fetch_job_data, daemon=True).start()

@app.route("/")
def hello():
    return "Hello from Python Flask Microservice!"

@app.route("/jobs")
def get_jobs():
    return jsonify(job_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
