# Cloud API Deployment

A minimal REST API built with Python (FastAPI) and deployed on an AWS EC2 instance with Nginx as a reverse proxy and pm2 as the process manager.

## Tech Stack

- **Language/Framework:** Python 3 / FastAPI
- **ASGI Server:** Uvicorn
- **Reverse Proxy:** Nginx
- **Process Manager:** pm2
- **Cloud Provider:** AWS EC2 (Amazon Linux)

---

## Running Locally

### 1. Clone the repo

```bash
git clone https://github.com/DivineObido/cloud-api-deployment.git
cd cloud-api-deployment
```

### 2. Create a virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn[standard]
```

### 4. Start the server

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000`

---

## Endpoints

### `GET /`

Returns a simple status message.

**Response:**
```json
{
  "message": "API is running"
}
```

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "message": "healthy"
}
```

### `GET /me`

Returns personal information.

**Response:**
```json
{
  "name": "Divine Obido",
  "email": "divineobido64@gmail.com",
  "github": "https://github.com/DivineObido"
}
```

---

## Live Deployment

**Base URL:** `http://54.242.186.88`

---

## Deployment Process

### 1. Provision the server

Spun up an AWS EC2 instance (Amazon Linux, t2.micro) with inbound rules open for SSH (port 22) and HTTP (port 80).

### 2. Install dependencies on the server

```bash
sudo yum install python3 python3-pip nginx git nodejs -y
sudo npm install -g pm2
```

### 3. Clone the repo and set up the virtual environment

```bash
git clone https://github.com/DivineObido/cloud-api-deployment.git
cd cloud-api-deployment
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn[standard]
```

### 4. Start the app with pm2

The app runs on port 8000 internally and is never exposed directly to the public.

```bash
pm2 start "uvicorn main:app --host 127.0.0.1 --port 8000" --name personal-api
pm2 startup
pm2 save
```

### 5. Configure Nginx as a reverse proxy

Created `/etc/nginx/conf.d/personal-api.conf`:

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 10s;
    }
}
```

Then tested and restarted Nginx:

```bash
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
```
