# ✅ Pre-Deployment Checklist

## Before You Deploy - Complete All Items

### 🔧 Code & Configuration
- [ ] `server.py` uses `host='0.0.0.0'` (not 'localhost')
- [ ] Port is configurable via environment variables
- [ ] `DEBUG=False` in production
- [ ] All imports work correctly
- [ ] `index.html` is in same directory as `server.py`
- [ ] No hardcoded secrets or API keys
- [ ] All file paths use relative paths (not absolute)
- [ ] Error handling implemented
- [ ] Logging configured

### 📦 Dependencies
- [ ] `requirements.txt` is complete and updated
  ```bash
  pip freeze > requirements.txt
  ```
- [ ] All packages listed with versions
- [ ] No development-only packages included
- [ ] Added `gunicorn` for production
- [ ] Tested: `pip install -r requirements.txt`

### 📁 Files & Structure
- [ ] Project organized properly:
  ```
  medical-diagnosis-kbs/
  ├── server.py
  ├── index.html
  ├── *.py (all source files)
  ├── requirements.txt
  ├── Procfile (for Heroku)
  ├── Dockerfile (for Docker)
  ├── .gitignore
  └── .env.example
  ```
- [ ] No `__pycache__/` directories
- [ ] No `*.pyc` files
- [ ] No `.vscode/` or IDE folders
- [ ] `.gitignore` configured properly

### 🔐 Security
- [ ] No passwords in code
- [ ] No API keys in code
- [ ] Use environment variables for secrets
- [ ] `CORS` properly configured
  ```python
  CORS(app)  # or restrict to your domain
  ```
- [ ] No debug mode in production
- [ ] HTTPS enabled (auto on most platforms)
- [ ] Input validation implemented
- [ ] Error messages don't leak information

### 🌐 Networking
- [ ] Application binds to `0.0.0.0` (not `localhost`)
- [ ] Port is configurable (via `PORT` env var)
- [ ] CORS headers set correctly
- [ ] Static files serve correctly
- [ ] API endpoints respond properly
- [ ] Tested with external network access

### 📝 Documentation
- [ ] `README.md` updated with deployment URL
- [ ] `.env.example` created with required variables
- [ ] Deployment instructions in README
- [ ] API documentation complete
- [ ] Architecture documented
- [ ] Any custom setup noted

### 🧪 Testing
- [ ] App runs locally without errors
  ```bash
  python server.py
  ```
- [ ] All endpoints tested (http://localhost:5000/api/triage)
- [ ] Frontend loads correctly
- [ ] API returns valid JSON
- [ ] Error handling works
- [ ] Static files load (CSS, JS)

### 🚀 Platform-Specific

#### For Heroku:
- [ ] `Procfile` created
- [ ] `runtime.txt` specifies Python version
- [ ] `requirements.txt` includes `gunicorn`
- [ ] Tested locally with gunicorn:
  ```bash
  gunicorn -w 4 -b 0.0.0.0:5000 server:app
  ```
- [ ] Heroku CLI installed
- [ ] Git repository initialized

#### For Docker:
- [ ] `Dockerfile` created
- [ ] `.dockerignore` created
- [ ] Tested locally:
  ```bash
  docker build -t medical-kbs .
  docker run -p 5000:5000 medical-kbs
  ```
- [ ] Docker Desktop installed
- [ ] Image builds without errors

#### For AWS EC2:
- [ ] EC2 instance running (Ubuntu 22.04)
- [ ] Security group allows ports 22, 80, 443
- [ ] SSH key downloaded and secured
- [ ] Can SSH into instance
- [ ] Application can start on port 5000
- [ ] Systemd service file created (if using)

#### For PythonAnywhere:
- [ ] Account created (free tier)
- [ ] Files uploaded
- [ ] Web app configured
- [ ] WSGI file updated
- [ ] Working on pythonanywhere.com domain

#### For DigitalOcean:
- [ ] Account created
- [ ] Droplet deployed (Ubuntu 22.04)
- [ ] Can SSH into droplet
- [ ] Application can start

### 📊 Performance
- [ ] Using `gunicorn` (not Flask dev server)
- [ ] Multiple workers configured (4+)
- [ ] Timeout set appropriately
- [ ] No synchronous heavy operations
- [ ] Logging doesn't slow down app

### 🔍 Monitoring & Logging
- [ ] Logging configured
- [ ] Error logs captured
- [ ] Access logs available
- [ ] Can view platform logs
  ```bash
  # Heroku
  heroku logs --tail
  
  # Others: check platform dashboard
  ```
- [ ] Health endpoint available (`/api/health`)

### 🌍 Domain & HTTPS
- [ ] HTTPS enabled (usually automatic)
- [ ] Custom domain configured (optional)
- [ ] DNS records updated (if custom domain)
- [ ] SSL certificate valid
- [ ] Redirects work (http → https)

### 📱 Frontend
- [ ] `index.html` loads without errors
- [ ] API URLs use relative paths (not hardcoded localhost)
- [ ] CSS loads correctly
- [ ] JavaScript executes
- [ ] Responsive design works
- [ ] No console errors

### 📚 Version Control
- [ ] Code committed to Git
- [ ] `.gitignore` excludes cache files
- [ ] No secrets in commit history
- [ ] Clean commit history
- [ ] README.md in root directory
- [ ] All necessary files in repo

---

## Pre-Deployment Commands

### Test Everything Locally First:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test with Flask dev server
python server.py
# Visit http://localhost:5000

# 3. Test with Gunicorn (production-like)
gunicorn -w 4 -b 0.0.0.0:5000 server:app
# Visit http://localhost:5000

# 4. Test with Docker
docker build -t medical-kbs .
docker run -p 5000:5000 medical-kbs
# Visit http://localhost:5000
```

---

## Deployment Readiness Score

**Grade your readiness:**

- 0-5 items unchecked: ❌ Not ready - Fix issues first
- 6-15 items unchecked: ⚠️  Partially ready - Fix critical items
- 16-30 items unchecked: 🟡 Mostly ready - Final checks
- 30+ items checked: ✅ Ready to deploy!

---

## Final Steps Before Clicking "Deploy"

1. **Take a Screenshot** of your working local app
2. **Save Deployment URL** somewhere safe
3. **Test All Endpoints** one more time
4. **Verify Environment Variables** are set
5. **Check Platform Logs** are accessible
6. **Have a Rollback Plan** (just in case)

---

## Emergency Rollback

If something goes wrong:

### Heroku
```bash
heroku releases
heroku rollback v123  # Replace with version number
```

### Docker
```bash
docker stop container_id
docker run -p 5000:5000 medical-kbs:previous-tag
```

### AWS/DigitalOcean
Stop the application, revert code, restart

---

## Post-Deployment

After successful deployment:

- [ ] Access live URL and test
- [ ] Verify all endpoints work
- [ ] Check API responses
- [ ] Monitor logs for errors
- [ ] Share URL on GitHub profile
- [ ] Update portfolio with live link
- [ ] Test on mobile devices
- [ ] Bookmark application URL
- [ ] Monitor first 24 hours for issues

---

## Common Issues & Quick Fixes

| Issue | Solution |
|-------|----------|
| 404 errors | Check `index.html` location |
| CORS errors | Add `CORS(app)` to server.py |
| Port already in use | Change port or kill process |
| Module not found | Add to `requirements.txt` |
| Timeout errors | Check logs, increase timeout |
| Static files not loading | Verify relative paths |
| API not responding | Check error logs |
| Can't connect | Check firewall/security groups |

---

**Once all items are checked, you're ready to deploy! 🚀**
