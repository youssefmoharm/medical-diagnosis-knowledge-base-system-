# 🚀 Deployment Quick Reference

## One-Page Deployment Cheat Sheet

### 🏃 Fastest (2 minutes)
```bash
# ngrok - Instant public URL for testing
ngrok http 5000
# Share the https://xxx.ngrok.io URL
```

---

### ⚡ Fast (5 minutes)

#### Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
# Live at: https://your-app-name.herokuapp.com
```

**Files needed:**
- `Procfile`
- `runtime.txt`
- `requirements.txt` (with gunicorn)

---

### 🚀 Medium (10-15 minutes)

#### Docker
```bash
docker build -t medical-kbs .
docker run -p 5000:5000 medical-kbs
# Test locally first
```

#### PythonAnywhere
1. Sign up at pythonanywhere.com
2. Upload files
3. Add Flask web app
4. Live at: yourusername.pythonanywhere.com

#### DigitalOcean App Platform
1. Connect GitHub repo
2. Select Dockerfile
3. Deploy
4. Auto-deploys on push

---

### 🔧 Full Control (20 minutes)

#### AWS EC2
```bash
# SSH into instance
ssh -i key.pem ubuntu@IP

# Setup
sudo apt update
sudo apt install python3 python3-pip git
git clone your-repo
pip3 install -r requirements.txt

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:80 server:app
```

---

## Platform Comparison Quick Table

| Platform | Time | Cost | Ease | Best For |
|----------|------|------|------|----------|
| ngrok | 2 min | Free | ⭐⭐⭐⭐⭐ | Testing |
| Heroku | 5 min | Free/Paid | ⭐⭐⭐⭐⭐ | Demos |
| Docker | 10 min | Varies | ⭐⭐⭐ | Flexibility |
| PythonAnywhere | 10 min | Free/Paid | ⭐⭐⭐⭐ | Python |
| DigitalOcean | 15 min | $5-6/mo | ⭐⭐⭐⭐ | Production |
| AWS EC2 | 20 min | Free 1yr | ⭐⭐⭐ | Enterprise |

---

## Pre-Deployment Essentials (5-minute check)

```bash
# 1. Test locally
python server.py
# Visit http://localhost:5000 ✓

# 2. Test with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server:app
# Visit http://localhost:5000 ✓

# 3. Check requirements.txt
cat requirements.txt
# Should include: flask, flask-cors, gunicorn ✓

# 4. Verify files
ls -la server.py index.html
# Both should exist ✓

# 5. Check server.py
grep "host=" server.py
# Should have: host='0.0.0.0' ✓
```

---

## Key Files Needed

| Platform | Files |
|----------|-------|
| **Heroku** | Procfile, runtime.txt, requirements.txt |
| **Docker** | Dockerfile, .dockerignore, requirements.txt |
| **All** | requirements.txt, server.py, index.html |

---

## Environment Variables

Create `.env` file (don't commit):
```
FLASK_ENV=production
DEBUG=False
PORT=5000
```

Or set in platform:
```bash
# Heroku
heroku config:set FLASK_ENV=production

# DigitalOcean/Others: Use platform dashboard
```

---

## Troubleshooting Quick Fixes

| Error | Fix |
|-------|-----|
| Port in use | `lsof -i :5000` then `kill -9 PID` |
| Module not found | `pip install -r requirements.txt` |
| index.html not found | Put in same dir as `server.py` |
| localhost not working | Use `0.0.0.0` instead |
| 502 Bad Gateway | Check application logs |
| CORS error | Add `CORS(app)` to server.py |

---

## Checking Deployment Status

```bash
# Heroku
heroku logs --tail
heroku status

# Docker
docker logs container_id

# DigitalOcean
# Check dashboard or SSH in

# AWS
# Check CloudWatch logs
```

---

## Testing Live App

```bash
# Test main page
curl https://your-domain.com

# Test API
curl -X POST https://your-domain.com/api/triage \
  -H "Content-Type: application/json" \
  -d '{"symptoms":{"fever":true},"vitals":{},"history":{}}'

# Health check
curl https://your-domain.com/api/health
```

---

## Performance Tuning

```python
# In Procfile or startup
gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 60 server:app
```

- `-w 4`: 4 worker processes
- `--timeout 60`: 60-second timeout
- Adjust workers based on CPU cores: `workers = (2 × cores) + 1`

---

## Monitoring URLs

| Platform | Monitoring URL |
|----------|-----------------|
| Heroku | `heroku apps` (dashboard) |
| AWS | `aws.amazon.com/console` |
| DigitalOcean | `cloud.digitalocean.com` |
| Docker Hub | `hub.docker.com` |

---

## Rollback Commands

```bash
# Heroku
heroku releases
heroku rollback v10

# Docker
docker pull myimage:previous-tag
docker run previous-tag

# Git
git revert HEAD~1
git push
```

---

## After Deployment Checklist

- [ ] Access live URL
- [ ] Test all endpoints
- [ ] Check logs for errors
- [ ] Monitor performance
- [ ] Share link on GitHub
- [ ] Add to portfolio
- [ ] Update resume
- [ ] Share on LinkedIn

---

## One-Command Deployments

```bash
# ngrok (instant sharing)
ngrok http 5000

# Heroku (full deployment)
heroku login && heroku create && git push heroku main

# Docker (build and run)
docker build -t medical-kbs . && docker run -p 5000:5000 medical-kbs
```

---

## Deployment Decision Tree

```
Do you need production deployment?
├─ No → Use ngrok (2 min)
├─ Yes, need quick demo?
│  └─ Heroku (5 min)
├─ Yes, need flexibility?
│  └─ Docker (10 min)
├─ Yes, need full control?
│  └─ AWS/DigitalOcean (20 min)
└─ Yes, Python-specific?
   └─ PythonAnywhere (10 min)
```

---

## Useful URLs

- Heroku: https://heroku.com
- Docker: https://docker.com
- DigitalOcean: https://digitalocean.com
- AWS: https://aws.amazon.com
- PythonAnywhere: https://pythonanywhere.com
- ngrok: https://ngrok.com

---

## Cost Comparison (Monthly)

- ngrok: Free/Paid ($5)
- Heroku: Free/Paid ($7+)
- Docker: Free (host cost varies)
- PythonAnywhere: Free/Paid ($5+)
- DigitalOcean: $5-6
- AWS: Free 1yr, then $5-15+

---

## Pro Tips

✅ **Always test locally first**
```bash
python server.py
```

✅ **Use production-like setup**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

✅ **Check logs immediately**
```bash
heroku logs --tail  # or platform equivalent
```

✅ **Set up monitoring**
- Heroku Metrics
- CloudWatch (AWS)
- Dashboard monitoring (DigitalOcean)

✅ **Use environment variables**
```python
import os
port = int(os.environ.get('PORT', 5000))
debug = os.environ.get('DEBUG') == 'True'
```

---

## Next Steps

1. **Choose platform** from comparison table
2. **Check pre-deployment checklist** (PRE_DEPLOYMENT_CHECKLIST.md)
3. **Follow detailed guide** (DEPLOYMENT_GUIDE.md)
4. **Test locally first** (always!)
5. **Deploy** (you've got this! 🚀)
6. **Monitor** (check logs)
7. **Share** (LinkedIn, GitHub, portfolio)

---

**Remember: Deploy confidently, monitor actively, iterate quickly! 🎉**

For detailed instructions on any platform, see: `DEPLOYMENT_GUIDE.md`
