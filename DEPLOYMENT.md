# OpenClawMD Deployment Guide

Complete guide for deploying OpenClawMD to production.

---

## 🚀 Quick Deploy (Vercel)

### 1. Prepare for Vercel

Create `vercel.json` in root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/openclaw_api_service.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/openclaw_api_service.py"
    },
    {
      "src": "/(.*)",
      "dest": "website/$1"
    }
  ]
}
```

### 2. Deploy

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd /tmp/OC-skills
vercel --prod
```

### 3. Configure Domain

```bash
# In Vercel Dashboard:
# Settings → Domains → Add: openclawmd.com
```

---

## 🐳 Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY api/requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application
COPY api/ ./api/
COPY website/ ./website/

# Expose port
EXPOSE 5000

# Start server
CMD ["python3", "api/openclaw_api_service.py"]
```

### 2. Build & Run

```bash
docker build -t openclawmd .
docker run -p 5000:5000 -d openclawmd
```

### 3. Deploy to Server

```bash
# On your VPS
docker pull openclawmd
docker run -p 80:5000 -d --restart=always openclawmd
```

---

## 🖥️ Manual VPS Deployment

### 1. Setup Server

```bash
# SSH to server
ssh user@your-server.com

# Install Python
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Create app directory
mkdir -p /var/www/openclawmd
cd /var/www/openclawmd
```

### 2. Clone Repository

```bash
git clone https://github.com/DYAI2025/OC-skills.git .
cd api
pip3 install -r requirements.txt
```

### 3. Setup Systemd Service

Create `/etc/systemd/system/openclawmd.service`:

```ini
[Unit]
Description=OpenClawMD Skill Generator
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/openclawmd/api
ExecStart=/usr/bin/python3 openclaw_api_service.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4. Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable openclawmd
sudo systemctl start openclawmd
sudo systemctl status openclawmd
```

### 5. Setup Nginx (Optional)

Create `/etc/nginx/sites-available/openclawmd`:

```nginx
server {
    listen 80;
    server_name openclawmd.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/openclawmd /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 📊 Monitoring

### Health Check

```bash
curl http://localhost:5000/
# Should return: {"status": "healthy", ...}
```

### Logs

```bash
# Systemd service
journalctl -u openclawmd -f

# Docker
docker logs -f openclawmd

# Vercel
vercel logs
```

---

## 💾 Database (Optional)

For production, replace in-memory storage with database:

### SQLite (Simple)

```python
# In openclaw_api_service.py
import sqlite3

conn = sqlite3.connect('skills.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS skills (
        id TEXT PRIMARY KEY,
        data TEXT,
        zip BLOB,
        created_at TEXT
    )
''')
```

### PostgreSQL (Production)

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="openclawmd",
    user="openclaw",
    password="your-password"
)
```

---

## 🔒 Security

### Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(
    app=app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)

@app.route('/api/skills/generate', methods=['POST'])
@limiter.limit("10 per minute")
def generate():
    ...
```

### CORS

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://openclawmd.com"],
        "methods": ["GET", "POST"]
    }
})
```

---

## 📈 Scaling

### Horizontal Scaling

```bash
# Run multiple instances behind load balancer
docker run -p 5001:5000 -d openclawmd
docker run -p 5002:5000 -d openclawmd
docker run -p 5003:5000 -d openclawmd
```

### Redis Cache

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379)

# Cache generated skills
redis_client.setex(f'skill:{skill_id}', 3600, skill_zip)
```

---

## ✅ Production Checklist

- [ ] Domain configured (openclawmd.com)
- [ ] SSL certificate (Let's Encrypt)
- [ ] Rate limiting enabled
- [ ] Database configured (not in-memory)
- [ ] Logging setup
- [ ] Monitoring enabled
- [ ] Backups configured
- [ ] Error tracking (Sentry)
- [ ] Analytics (Google Analytics/Plausible)
- [ ] Payment integration (Stripe)
- [ ] Email service (SendGrid)

---

**Ready for Production! 🚀**
