from flask import Flask, jsonify, request
import os
import paramiko
import sqlite3
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SSH_HOST = os.getenv("SSH_HOST", "cardinal.osc.edu")
SQUEUE_COMMAND = os.getenv("SQUEUE_COMMAND", "squeue -A PYS0302")
SHOW_JOB_COMMAND = os.getenv("SHOW_JOB_COMMAND", "scontrol show job")
DB_PATH = os.getenv("DB_PATH", "users.db")

sessions = {}


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        ssh_user TEXT NOT NULL,
        ssh_pass TEXT NOT NULL
    )"""
    )
    conn.commit()
    conn.close()


def run_command(user, pwd, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SSH_HOST, username=user, password=pwd)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    ssh.close()
    return output


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")
    ssh_user = data.get("ssh_user")
    ssh_pass = data.get("ssh_pass")
    if not (username and password and ssh_user and ssh_pass):
        return jsonify({"error": "Missing fields"}), 400

    pw_hash = generate_password_hash(password)
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (username, password_hash, ssh_user, ssh_pass) VALUES (?, ?, ?, ?)",
            (username, pw_hash, ssh_user, ssh_pass),
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "registered"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "User exists"}), 400


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT password_hash, ssh_user, ssh_pass FROM users WHERE username=?",
        (username,),
    )
    row = c.fetchone()
    conn.close()
    if not row or not check_password_hash(row[0], password):
        return jsonify({"error": "Invalid credentials"}), 401
    token = str(uuid.uuid4())
    sessions[token] = {"ssh_user": row[1], "ssh_pass": row[2]}
    return jsonify({"token": token})


def get_session(request):
    token = request.headers.get("Authorization")
    if not token:
        return None
    return sessions.get(token)


@app.route("/jobs")
def get_jobs():
    sess = get_session(request)
    if not sess:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        output = run_command(sess["ssh_user"], sess["ssh_pass"], SQUEUE_COMMAND)
        lines = output.strip().split("\n")
        headers = lines[0].split()
        jobs = [dict(zip(headers, line.split(None, len(headers) - 1))) for line in lines[1:]]
        return jsonify(jobs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/job/<jobid>")
def get_job_detail(jobid):
    sess = get_session(request)
    if not sess:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        output = run_command(
            sess["ssh_user"], sess["ssh_pass"], f"{SHOW_JOB_COMMAND} {jobid}"
        )
        detail = {}
        for token_ in output.replace("\n", " ").split():
            if "=" in token_:
                key, value = token_.split("=", 1)
                detail[key] = value
        return jsonify(detail)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def index():
    return "OSC Job Backend"


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
