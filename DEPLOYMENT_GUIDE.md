# 🚀 Deployment Guide: Medical Diagnosis KBS

Complete guide to deploy your application on various platforms.

---

## 📊 Deployment Options Comparison

| Platform | Cost | Ease | Speed | Best For |
|----------|------|------|-------|----------|
| **Heroku** | Free/Paid | ⭐⭐⭐⭐⭐ | 5 min | Quick demos, prototypes |
| **AWS EC2** | Paid (~$5-15/mo) | ⭐⭐⭐ | 15 min | Production, scalability |
| **PythonAnywhere** | Free/Paid | ⭐⭐⭐⭐ | 10 min | Python-specific, simple |
| **Docker + Any Host** | Variable | ⭐⭐⭐ | 20 min | Flexibility, containers |
| **ngrok (Local)** | Free | ⭐⭐⭐⭐⭐ | 2 min | Testing, sharing links |
| **Google Cloud** | Free tier available | ⭐⭐⭐ | 20 min | Enterprise, scalability |
| **DigitalOcean** | Paid (~$5/mo) | ⭐⭐⭐⭐ | 15 min | VPS, full control |

---

# 🎯 OPTION 1: Heroku (Recommended for Beginners)

## Why Heroku?
✅ Free tier available  
✅ Easiest deployment (5 minutes)  
✅ Perfect for portfolios/demos  
✅ Automatic HTTPS  
✅ Minimal configuration  

## Step 1: Prepare Your Project

### Create `Procfile` (in project root)
```
web: python server.py
```

### Update `server.py` for Production
Replace the last line in `server.py`:

```python
# Change this:
if __name__ == '__main__':
    app.run(debug=True)

# To this:
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### Update `requirements.txt`
```
flask==2.3.2
flask-cors==4.0.0
gunicorn==20.1.0
```

### Create `runtime.txt` (optional but recommended)
```
python-3.11.0
```

## Step 2: Install Heroku CLI

**Windows/Mac/Linux:**
Download from [heroku.com/download](https://www.heroku.com/download)

Verify installation:
```bash
heroku --version
```

## Step 3: Deploy

```bash
# 1. Login to Heroku
heroku login

# 2. Create Heroku app
heroku create your-app-name

# 3. Deploy code
git push heroku main

# 4. View live app
heroku open
```

**Your app is live!** Share the URL: `https://your-app-name.herokuapp.com`

## Step 4: Monitor & Manage

```bash
# View logs
heroku logs --tail

# Restart app
heroku restart

# View environment variables
heroku config

# Scale dynos (if needed)
heroku ps:scale web=1
```

---

# 🐳 OPTION 2: Docker + Any Host (Most Flexible)

## Why Docker?
✅ Works anywhere (Windows, Mac, Linux, Cloud)  
✅ Consistent environment  
✅ Easy to scale  
✅ Deploy to any platform  

## Step 1: Create Dockerfile

Create file named `Dockerfile` (no extension) in project root:

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Update server.py to use host 0.0.0.0
RUN sed -i "s/app.run(debug=True)/app.run(host='0.0.0.0', port=5000, debug=False)/" server.py

# Run app
CMD ["python", "server.py"]
```

## Step 2: Create `.dockerignore`

```
__pycache__/
*.py[cod]
.vscode/
.git/
.gitignore
README.md
*.zip
```

## Step 3: Build & Test Locally

```bash
# Build Docker image
docker build -t medical-kbs .

# Run locally on port 5000
docker run -p 5000:5000 medical-kbs

# Visit: http://localhost:5000
```

## Step 4: Deploy to Cloud

### Option A: Heroku with Docker

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add Heroku registry
heroku container:login

# Push Docker image
heroku container:push web -a your-app-name

# Release
heroku container:release web -a your-app-name

# Open app
heroku open -a your-app-name
```

### Option B: AWS ECR + ECS (More Complex)

```bash
# Create ECR repository
aws ecr create-repository --repository-name medical-kbs

# Build and push
docker build -t medical-kbs .
docker tag medical-kbs:latest YOUR_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/medical-kbs:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/medical-kbs:latest

# Deploy via ECS (use AWS Console or CLI)
```

### Option C: DigitalOcean App Platform

```bash
# Connect GitHub repo
# Navigate to App Platform
# Select Dockerfile deployment
# Auto-deploys on git push
```

---

# ☁️ OPTION 3: AWS EC2 (Full Control)

## Why AWS EC2?
✅ Full control over environment  
✅ Scalable infrastructure  
✅ Good for production  
✅ Free tier available (1 year)  

## Step 1: Launch EC2 Instance

1. Go to [AWS Console](https://console.aws.amazon.com)
2. Navigate to **EC2 → Instances → Launch Instance**
3. Choose:
   - **AMI**: Ubuntu 22.04 LTS
   - **Instance Type**: t2.micro (free tier)
   - **Storage**: 20 GB
4. Configure Security Group:
   - Allow HTTP (port 80)
   - Allow HTTPS (port 443)
   - Allow SSH (port 22)
5. Create and download `.pem` key file

## Step 2: Connect via SSH

```bash
# On your computer
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_INSTANCE_IP
```

## Step 3: Install Dependencies

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip git -y

# Clone your repository
git clone https://github.com/yourusername/medical-diagnosis-kbs.git
cd medical-diagnosis-kbs

# Install Python packages
pip3 install -r requirements.txt
```

## Step 4: Run Application

### Option A: Simple (for testing)
```bash
# Run directly
python3 server.py
```

### Option B: Production with Gunicorn

```bash
# Install gunicorn
pip3 install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:80 server:app
```

### Option C: Systemd Service (Recommended)

Create `/etc/systemd/system/medical-kbs.service`:

```ini
[Unit]
Description=Medical Diagnosis KBS
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/medical-diagnosis-kbs
ExecStart=/usr/bin/python3 /home/ubuntu/medical-diagnosis-kbs/server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable medical-kbs
sudo systemctl start medical-kbs
sudo systemctl status medical-kbs
```

## Step 5: Setup Nginx Reverse Proxy

```bash
# Install Nginx
sudo apt install nginx -y

# Create config
sudo nano /etc/nginx/sites-available/medical-kbs
```

Paste:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/medical-kbs /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

# 🔗 OPTION 4: PythonAnywhere (Easiest for Python)

## Why PythonAnywhere?
✅ Python-specific hosting  
✅ No command line needed  
✅ Free tier available  
✅ Web-based interface  

## Step 1: Create Account

Go to [pythonanywhere.com](https://www.pythonanywhere.com) and sign up (free tier available)

## Step 2: Upload Files

1. Go to **Files** tab
2. Upload your project folder (or clone from GitHub)
3. Upload all `.py` files and `index.html`

## Step 3: Configure Web App

1. Click **Web** tab
2. Click **Add a new web app**
3. Choose **Flask** and **Python 3.10+**
4. Edit WSGI file to point to your app:

```python
import sys
path = '/home/yourusername/medical-diagnosis-kbs'
if path not in sys.path:
    sys.path.append(path)

from server import app as application
```

## Step 4: Launch

Your app is live at: `yourusername.pythonanywhere.com`

---

# 📱 OPTION 5: ngrok (Quick Sharing & Testing)

## Why ngrok?
✅ Instant public URL  
✅ No setup needed  
✅ Perfect for testing  
✅ Great for demos  

## Step 1: Install ngrok

Download from [ngrok.com](https://ngrok.com/download)

```bash
# Extract and add to PATH
# Or use directly
./ngrok http 5000
```

## Step 2: Run Your App

```bash
# Terminal 1: Run your Flask app
python server.py

# Terminal 2: Expose via ngrok
ngrok http 5000
```

## Step 3: Share URL

ngrok gives you a public URL like:
```
https://abc123def456.ngrok.io
```

Share this URL with anyone! ✅

---

# 🎯 OPTION 6: DigitalOcean (Best Value)

## Why DigitalOcean?
✅ Affordable ($5-6/month)  
✅ Simple droplets (VPS)  
✅ Good documentation  
✅ App Platform (easy deployment)  

## Step 1: Using DigitalOcean App Platform

1. Create DigitalOcean account
2. Go to **App Platform → Create App**
3. Connect GitHub repo
4. Configure:
   - **Source**: GitHub repository
   - **Branch**: main
   - **Build command**: (leave empty)
   - **Run command**: `python server.py`
5. Add environment variables if needed
6. Deploy!

Auto-deploys on every git push 🎉

---

# 📋 Deployment Checklist

Before deploying, verify:

- [ ] `server.py` uses `host='0.0.0.0'`
- [ ] Port is configurable or uses 5000
- [ ] `requirements.txt` updated with all dependencies
- [ ] `index.html` is in same directory as `server.py`
- [ ] No hardcoded file paths (use relative paths)
- [ ] No debug mode in production
- [ ] All imports work correctly
- [ ] `.gitignore` excludes cache files

---

# 🔒 Production Security Checklist

- [ ] Set `debug=False` in production
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Set proper CORS headers (limit to your domain)
- [ ] Add rate limiting
- [ ] Use strong secret keys
- [ ] Keep dependencies updated
- [ ] Monitor logs for errors

---

# 🚦 Environment Variables

Create `.env` file (don't commit to GitHub):

```
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your-secret-key-here
```

Load in `server.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()

app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'
app.secret_key = os.getenv('SECRET_KEY', 'dev-key')
```

---

# 🔗 Useful Links by Platform

| Platform | Link | Time to Deploy |
|----------|------|-----------------|
| Heroku | https://www.heroku.com | 5 minutes |
| AWS | https://aws.amazon.com | 20 minutes |
| PythonAnywhere | https://pythonanywhere.com | 10 minutes |
| DigitalOcean | https://digitalocean.com | 10 minutes |
| ngrok | https://ngrok.com | 2 minutes |
| Docker Hub | https://hub.docker.com | 15 minutes |

---

# 📊 Deployment Comparison Matrix

## Free Tier
- ✅ Heroku (limited, 550 hours/month)
- ✅ PythonAnywhere (free tier)
- ✅ ngrok (free tier)
- ✅ AWS (1 year free tier)

## Best for Beginners
1. **ngrok** - Fastest (2 min)
2. **Heroku** - Easiest (5 min)
3. **PythonAnywhere** - Python-native (10 min)

## Best for Production
1. **AWS EC2** - Most control
2. **DigitalOcean** - Best value
3. **Docker + Any Host** - Most flexible

---

# 🆘 Troubleshooting

### Port Already in Use
```python
# In server.py
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Module Not Found
```bash
# Ensure all dependencies in requirements.txt
pip freeze > requirements.txt
```

### CORS Errors
```python
# server.py
from flask_cors import CORS
CORS(app)
```

### Static Files Not Loading
```python
# Ensure index.html in same directory as server.py
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')
```

### 502 Bad Gateway
- Check application logs
- Verify app starts without errors locally
- Check environment variables
- Verify port binding

---

# 📈 Performance Tips

1. **Use Gunicorn** in production (not Flask dev server)
2. **Enable gzip compression** in Nginx
3. **Add caching headers** for static files
4. **Use CDN** for frontend files (optional)
5. **Monitor server resources**

---

# 🎓 Recommended Learning Path

1. **Start**: Deploy with ngrok (2 minutes) - test your app
2. **Next**: Deploy with Heroku (5 minutes) - share with others
3. **Advanced**: Deploy with Docker (20 minutes) - learn containerization
4. **Production**: Deploy with AWS/DO (30 minutes) - scale your app

---

# 📞 Next Steps After Deployment

1. **Share URL** on LinkedIn, portfolio, GitHub
2. **Update README** with deployment URL
3. **Monitor performance** with platform's dashboard
4. **Add custom domain** (most platforms support this)
5. **Enable HTTPS** (automatic on most platforms)
6. **Setup uptime monitoring** (UptimeRobot free tier)

---

## Quick Reference: Fastest Deployments

### 🏃 Fastest (2 minutes)
```bash
# ngrok - share local app instantly
ngrok http 5000
```

### ⚡ Fast (5 minutes)
```bash
# Heroku
heroku create your-app
git push heroku main
```

### 🚀 Medium (10 minutes)
```bash
# PythonAnywhere - GUI setup
# DigitalOcean App Platform - Connect GitHub
```

---

**Choose the deployment option that fits your needs! 🎉**

Need help with a specific platform? See detailed instructions above.
