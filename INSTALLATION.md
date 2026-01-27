# 📦 Installation Guide

Complete guide to installing and deploying AlphaStream Portfolio Optimizer

---

## 📋 **Table of Contents**

- [Prerequisites](#prerequisites)
- [Local Installation](#local-installation)
- [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
- [Google Sheets Setup](#google-sheets-setup)
- [Configuration](#configuration)
- [First Run](#first-run)
- [Troubleshooting](#troubleshooting)

---

## ✅ **Prerequisites**

### **Required**
- Python 3.9 or higher
- pip (Python package manager)
- Git
- Google Account
- Internet connection

### **Optional**
- Streamlit Cloud account (for deployment)
- GitHub account (for version control)
- Code editor (VS Code recommended)

### **Check Prerequisites**

```bash
# Check Python version
python --version  # Should be 3.9+

# Check pip
pip --version

# Check git
git --version
```

---

## 💻 **Local Installation**

### **Step 1: Clone the Repository**

```bash
# Clone the repository
git clone https://github.com/yourusername/alphastream-portfolio.git

# Navigate to project directory
cd alphastream-portfolio
```

### **Step 2: Create Virtual Environment (Recommended)**

#### **Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

#### **macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### **Step 3: Install Dependencies**

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

### **Step 4: Configure Storage**

**Option A: Use JSON Storage (Simple, No Setup)**
- No configuration needed
- Data stored locally
- ⚠️ **Warning:** Data lost on redeployment

**Option B: Use Google Sheets Storage (Recommended)**
- Persistent data storage
- Automatic backups
- Cross-device access
- **See:** [SETUP_GOOGLE_SHEETS.md](SETUP_GOOGLE_SHEETS.md)

### **Step 5: Run the Application**

```bash
# Start the application
streamlit run app.py
```

### **Step 6: Access the Application**

1. Open browser automatically (or manually go to `http://localhost:8501`)
2. Login with default credentials:
   - **Username:** `admin`
   - **Password:** `admin123`
3. ⚠️ **Change the admin password immediately!**

---

## ☁️ **Streamlit Cloud Deployment**

### **Step 1: Prepare Repository**

1. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/alphastream-portfolio.git
   git push -u origin main
   ```

2. **Verify files:**
   - ✅ `app.py`
   - ✅ `requirements.txt`
   - ✅ `.gitignore`

### **Step 2: Create Streamlit Cloud Account**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Authorize Streamlit

### **Step 3: Deploy Application**

1. **Click "New app"**

2. **Configure deployment:**
   - **Repository:** Select your repo
   - **Branch:** `main`
   - **Main file path:** `app.py`

3. **Click "Deploy"**

4. **Wait 2-3 minutes** for deployment

### **Step 4: Configure Secrets**

1. **Click "Settings" → "Secrets"**

2. **Add configuration:**

#### **For JSON Storage (Simple):**
```toml
# No secrets needed
```

#### **For Google Sheets Storage (Recommended):**
```toml
STORAGE_TYPE = "google_sheets"
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"

[google_sheets]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40project.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

3. **Click "Save"**

4. **Wait for auto-redeploy** (30 seconds)

### **Step 5: Verify Deployment**

1. Access your app URL: `https://yourapp.streamlit.app`
2. Login with admin credentials
3. Create a test portfolio
4. Verify data persists after refresh

---

## 🗄️ **Google Sheets Setup**

**For persistent storage, you MUST configure Google Sheets.**

See detailed guide: [SETUP_GOOGLE_SHEETS.md](SETUP_GOOGLE_SHEETS.md)

### **Quick Setup (30 minutes)**

1. **Create Google Cloud Project**
2. **Enable APIs** (Sheets + Drive)
3. **Create Service Account**
4. **Download credentials JSON**
5. **Create Google Sheet**
6. **Share sheet with service account**
7. **Configure Streamlit Secrets**

---

## ⚙️ **Configuration**

### **Environment Variables**

#### **STORAGE_TYPE**
```toml
STORAGE_TYPE = "json"  # or "google_sheets"
```
- `json` - Local file storage (ephemeral on Streamlit Cloud)
- `google_sheets` - Cloud storage (persistent)

#### **GOOGLE_SHEETS_URL**
```toml
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/SHEET_ID/edit"
```
- Required when `STORAGE_TYPE = "google_sheets"`
- Get from your Google Sheet URL

### **Application Settings**

**Default Admin Account:**
- Username: `admin`
- Password: `admin123`
- ⚠️ Change immediately after first login

**Global Settings (Configurable in app):**
- Default drift tolerance: 5.0%
- Allow user registration: True
- Default currency: USD

---

## 🚀 **First Run**

### **Step 1: Initial Login**

1. Access the application
2. Login as admin:
   - Username: `admin`
   - Password: `admin123`

### **Step 2: Change Admin Password**

1. Click on username → "Account"
2. Click "Change Password"
3. Enter new secure password
4. Save

### **Step 3: Configure Global Settings**

1. Navigate to "Admin Panel"
2. Review global settings:
   - Default drift tolerance
   - Allow registration
   - Other preferences
3. Adjust as needed
4. Save changes

### **Step 4: Create First Portfolio**

1. Go to "Portfolio Manager"
2. Click "Create New Profile"
3. Enter details:
   - Name: "My First Portfolio"
   - Principal: $10,000
   - Account type: Personal
4. Add assets:
   - Click "Add Asset"
   - Enter ticker: SPY
   - Set target: 60%
   - Repeat for other assets
5. Save portfolio

### **Step 5: Verify Data Persistence**

1. Create portfolio (as above)
2. Refresh the page (Ctrl+F5)
3. Login again
4. **Verify portfolio still exists** ✅

**If using Google Sheets:**
- Check Google Sheet (database tab, cell A1)
- Should see JSON data
- Data persists after app restarts

---

## 🐛 **Troubleshooting**

### **Common Installation Issues**

#### **Issue: pip install fails**
```bash
# Solution: Upgrade pip
python -m pip install --upgrade pip

# Then retry
pip install -r requirements.txt
```

#### **Issue: Python version too old**
```bash
# Check version
python --version

# If < 3.9, install Python 3.9+
# Download from: https://www.python.org/downloads/
```

#### **Issue: ModuleNotFoundError**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### **Common Deployment Issues**

#### **Issue: App won't start on Streamlit Cloud**
**Solution:**
1. Check logs in Streamlit Cloud
2. Verify `requirements.txt` is present
3. Check Python version in logs
4. Ensure all dependencies are listed

#### **Issue: "Google Sheets storage selected but libraries not installed"**
**Solution:**
Add to `requirements.txt`:
```
gspread>=5.12.0
google-auth>=2.23.0
```

#### **Issue: "Sheet not found" error**
**Solution:**
1. Verify `GOOGLE_SHEETS_URL` in Secrets
2. Check sheet is shared with service account
3. Verify service account has Editor permission

### **Getting More Help**

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review [GitHub Issues](https://github.com/yourusername/alphastream-portfolio/issues)
3. Open new issue with:
   - Error message
   - Steps to reproduce
   - Environment details

---

## ✅ **Installation Checklist**

Use this checklist to verify complete installation:

### **Local Installation:**
- [ ] Python 3.9+ installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Application runs locally
- [ ] Can login as admin
- [ ] Can create portfolio
- [ ] Data persists (if using Google Sheets)

### **Streamlit Cloud Deployment:**
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] App deployed successfully
- [ ] Secrets configured (if using Google Sheets)
- [ ] App accessible via URL
- [ ] Can login as admin
- [ ] Can create portfolio
- [ ] Data persists after refresh

---

## 🎯 **Next Steps**

After successful installation:

1. **Read User Guide:** [USER_GUIDE.md](USER_GUIDE.md)
2. **Create portfolios:** Start tracking your investments
3. **Invite users:** Add team members (if multi-user)
4. **Customize settings:** Adjust to your preferences
5. **Monitor regularly:** Check portfolio drift and rebalance

---

## 📞 **Support**

Need help with installation?

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Search [GitHub Issues](https://github.com/yourusername/alphastream-portfolio/issues)
3. Open new issue with details
4. Contact support: support@alphastream.example.com

---

**Installation complete? Move on to the [User Guide](USER_GUIDE.md)!** 🎉
