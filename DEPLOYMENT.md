# 🚀 AlphaStream Deployment Guide

Complete deployment instructions for AlphaStream Portfolio Manager v9.0.1

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Database Setup (Neon)](#database-setup-neon)
3. [Local Development](#local-development)
4. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
5. [Alternative Platforms](#alternative-platforms)
6. [Post-Deployment](#post-deployment)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### **Required**
- GitHub account
- PostgreSQL database (we recommend Neon - free tier available)
- Python 3.9+ (for local development)

### **Recommended**
- Git installed locally
- Basic knowledge of PostgreSQL
- Streamlit Cloud account (free)

---

## 🗄️ Database Setup (Neon)

### **Step 1: Create Neon Account**

1. Visit [https://neon.tech](https://neon.tech)
2. Click **"Sign Up"**
3. Choose sign-up method:
   - GitHub (recommended - fastest)
   - Google
   - Email

### **Step 2: Create Database**

1. Click **"Create a project"**
2. Configure project:
   - **Name:** `alphastream-prod`
   - **Region:** Choose closest to your users
   - **PostgreSQL version:** Latest (default)
3. Click **"Create Project"**
4. Wait 10-30 seconds for provisioning

### **Step 3: Get Connection Details**

1. In project dashboard, find **"Connection Details"**
2. Copy the following:
   - **Host:** `ep-xxxxx.region.aws.neon.tech`
   - **Database:** `neondb`
   - **User:** Your username
   - **Password:** Click "Show password" and copy (save this!)
   - **Port:** `5432`

⚠️ **IMPORTANT:** Save the password now - it's only shown once!

### **Step 4: Verify Connection**

The database table will be created automatically on first app run. If you want to create it manually:

```sql
CREATE TABLE IF NOT EXISTS database_store (
    id SERIAL PRIMARY KEY,
    data_json TEXT NOT NULL,
    version INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 💻 Local Development

### **Step 1: Clone Repository**

```bash
git clone https://github.com/yourusername/alphastream-portfolio-manager.git
cd alphastream-portfolio-manager
```

### **Step 2: Create Virtual Environment**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### **Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 4: Configure Secrets**

```bash
# Create .streamlit directory
mkdir .streamlit

# Copy template
cp secrets.toml.example .streamlit/secrets.toml

# Edit with your database credentials
# On Windows: notepad .streamlit/secrets.toml
# On macOS: open -e .streamlit/secrets.toml
# On Linux: nano .streamlit/secrets.toml
```

Fill in your Neon credentials:

```toml
[postgres]
host = "ep-xxxxx.us-east-2.aws.neon.tech"
dbname = "neondb"
user = "your-username"
password = "your-password"
port = "5432"
```

### **Step 5: Run Application**

```bash
streamlit run app.py
```

Application will open at `http://localhost:8501`

### **Step 6: Create First Admin Account**

1. Click **"Register"**
2. Create account:
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: Strong password
3. First user is automatically assigned admin role

---

## ☁️ Streamlit Cloud Deployment

### **Step 1: Push to GitHub**

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - AlphaStream v9.0.1"

# Create repository on GitHub and push
git remote add origin https://github.com/yourusername/alphastream-portfolio-manager.git
git branch -M main
git push -u origin main
```

⚠️ **Verify .gitignore is working:**
```bash
# This should NOT show secrets.toml
git status
```

### **Step 2: Deploy to Streamlit Cloud**

1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Configure deployment:
   - **Repository:** `yourusername/alphastream-portfolio-manager`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy"**

### **Step 3: Add Secrets**

1. In Streamlit Cloud, click **⚙️ Settings** (three dots menu)
2. Select **"Secrets"**
3. Paste your secrets:

```toml
[postgres]
host = "ep-xxxxx.us-east-2.aws.neon.tech"
dbname = "neondb"
user = "your-username"
password = "your-password"
port = "5432"
```

4. Click **"Save"**

### **Step 4: Wait for Deployment**

- Initial deployment: 2-5 minutes
- App will restart automatically
- You'll see a green "Your app is live!" message

### **Step 5: Access Your App**

Your app URL will be:
```
https://alphastream-portfolio-manager-[random-id].streamlit.app
```

---

## 🔄 Updates & Redeployment

### **Push Updates**

```bash
# Make changes to app.py
git add app.py
git commit -m "Update: description of changes"
git push

# Streamlit Cloud auto-detects and redeploys (30-60 seconds)
```

### **Update Dependencies**

If you add new packages to `requirements.txt`:
```bash
git add requirements.txt
git commit -m "Add new dependency: package-name"
git push

# Streamlit Cloud reinstalls all dependencies
```

### **Update Secrets**

1. Go to Streamlit Cloud app settings
2. Click "Secrets"
3. Update values
4. Click "Save"
5. App restarts automatically

---

## 🌐 Alternative Platforms

### **Heroku**

```bash
# Install Heroku CLI
# Add Procfile:
echo "web: streamlit run app.py --server.port $PORT" > Procfile

# Deploy
heroku create alphastream-app
heroku addons:create heroku-postgresql:mini
heroku config:set STREAMLIT_SERVER_HEADLESS=true
git push heroku main
```

### **AWS EC2**

```bash
# Launch Ubuntu 22.04 instance
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# Run with tmux (persists after logout)
tmux new -s alphastream
streamlit run app.py --server.port 8501
# Detach: Ctrl+B then D
```

### **Docker**

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Build and run:

```bash
docker build -t alphastream .
docker run -p 8501:8501 alphastream
```

---

## ✅ Post-Deployment

### **1. Create Admin Account**

First registered user becomes admin automatically.

### **2. Test Core Features**

- [ ] User registration works
- [ ] Login works
- [ ] Create portfolio
- [ ] Add assets
- [ ] Deploy capital
- [ ] Data persists after refresh

### **3. Configure Neon Backups**

Neon automatically backs up your database:
- Free tier: 7 days of point-in-time recovery
- Pro tier: 30 days of point-in-time recovery

Verify in Neon Console → Backups → "Continuous Backup: Enabled"

### **4. Monitor Database**

Use SQL queries from [SQL_QUERIES.md](SQL_QUERIES.md):

```sql
-- Quick health check
SELECT 
    version,
    last_updated,
    pg_size_pretty(pg_database_size(current_database())) as db_size
FROM database_store;
```

### **5. Set Up Monitoring (Optional)**

- Streamlit Cloud provides basic analytics
- Neon provides database metrics
- Consider UptimeRobot for uptime monitoring

---

## 🐛 Troubleshooting

### **Issue: "No module named 'psycopg2'"**

**Solution:**
```bash
# Ensure requirements.txt has:
echo "psycopg2-binary>=2.9.9" >> requirements.txt
git add requirements.txt
git commit -m "Add psycopg2-binary"
git push
```

---

### **Issue: "could not connect to server"**

**Causes:**
1. Incorrect credentials in secrets
2. Database not running
3. Firewall blocking connection

**Solution:**
1. Verify secrets.toml matches Neon exactly
2. Check Neon Console - project should be "Active"
3. Neon allows all IPs by default - no firewall config needed

---

### **Issue: App crashes on startup**

**Check Streamlit Cloud logs:**
1. Open app on Streamlit Cloud
2. Click "Manage app" (bottom right)
3. View logs for error messages

**Common errors:**
- Missing secrets → Add to Streamlit Cloud secrets
- Syntax error → Check local deployment first
- Import error → Update requirements.txt

---

### **Issue: Data not persisting**

**Verify PostgreSQL connection:**

In Neon SQL Editor:
```sql
SELECT * FROM database_store;
```

Should show data. If empty:
- Check app is actually saving (create test profile)
- Verify secrets are correct
- Check Streamlit Cloud logs for errors

---

### **Issue: Slow performance**

**Optimize:**
1. Neon free tier has limits - upgrade if needed
2. Use connection pooling (already implemented)
3. Check database size isn't excessive:
   ```sql
   SELECT pg_size_pretty(pg_database_size(current_database()));
   ```

---

## 📊 Production Checklist

Before going live with real data:

- [ ] ✅ Neon database created and tested
- [ ] ✅ Secrets configured (never committed to Git)
- [ ] ✅ App deployed to Streamlit Cloud
- [ ] ✅ SSL/HTTPS enabled (automatic on Streamlit Cloud)
- [ ] ✅ Admin account created with strong password
- [ ] ✅ Test registration/login flow
- [ ] ✅ Test portfolio creation and data persistence
- [ ] ✅ Backups enabled in Neon (automatic)
- [ ] ✅ Database health check queries saved
- [ ] ✅ Custom domain configured (optional)

---

## 🔒 Security Best Practices

1. **Never commit secrets to Git**
   - Always use .gitignore
   - Use secrets.toml.example as template

2. **Use strong passwords**
   - Database: 20+ characters, random
   - Admin account: 16+ characters, complex

3. **Enable database SSL**
   - Neon enables by default
   - Verify: `sslmode=require` in connection string

4. **Regular backups**
   - Neon: Automatic (verify in console)
   - Manual: Export data periodically

5. **Monitor access**
   - Review active connections in Neon
   - Check admin logs for suspicious activity

6. **Rotate credentials**
   - Change database password every 90 days
   - Update in both Neon and Streamlit Cloud secrets

---

## 📞 Support

**Issues?**
- Check [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- Review [SQL_QUERIES.md](SQL_QUERIES.md) for database queries
- Open GitHub issue
- Contact: your-email@example.com

**Resources:**
- [Neon Documentation](https://neon.tech/docs)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

**Deployment Status:** ✅ v9.0.1 is production-ready for Streamlit Cloud with PostgreSQL
