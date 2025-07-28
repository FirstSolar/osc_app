# OSC Job Monitoring App

This project provides a small containerized setup with a Flask backend and a Streamlit frontend served through NGINX. The backend connects to a remote cluster via SSH to fetch job queue data, while the frontend displays that information in a dashboard.

## Running locally

The easiest way to run the application is using Docker Compose:

```bash
docker-compose up --build
```

The frontend will be available at `https://localhost` (NGINX terminates TLS), and the backend is exposed on port `5000` within the compose network.

### Environment variables

The backend requires SSH credentials to connect to the cluster. These values can be provided using environment variables:

- `SSH_HOST` – remote host name
- `SSH_USER` – SSH user
- `SSH_PASS` – SSH password
- `SQUEUE_COMMAND` – command used to fetch job information (default: `squeue -A pys0302`)

You can set them in a `.env` file or directly in the environment before running Docker Compose. An example configuration is provided in `.env.example`.

## Development

Typical Python build artefacts and virtual environments are ignored through `.gitignore`.

