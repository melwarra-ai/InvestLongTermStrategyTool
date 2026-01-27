# ☁️ Google Sheets Setup Guide

Complete guide to configuring persistent storage with Google Sheets

---

## 📋 **Overview**

**Time Required:** 30-45 minutes (one-time setup)  
**Difficulty:** ⭐⭐⭐ Moderate  
**Cost:** Free (Google Cloud free tier)  
**Result:** Persistent data storage with automatic backups

---

## ✅ **Prerequisites**

- Google Account
- Admin access to application
- Basic understanding of Google Cloud Console
- Text editor for copying credentials

---

## 🎯 **Setup Steps Overview**

1. Create Google Cloud Project (5 min)
2. Enable Required APIs (3 min)
3. Create Service Account (5 min)
4. Download Credentials (2 min)
5. Create Google Sheet (3 min)
6. Share Sheet with Service Account (2 min)
7. Configure Streamlit Secrets (10 min)
8. Test and Verify (5 min)

---

## 📝 **Step 1: Create Google Cloud Project**

### **1.1 Access Google Cloud Console**

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Sign in with your Google Account
3. Accept Terms of Service (if first time)

### **1.2 Create New Project**

1. Click project dropdown (top left)
2. Click "New Project"
3. Enter project details:
   ```
   Project Name: AlphaStream Portfolio
   Organization: (leave default or select)
   Location: (leave default)
   ```
4. Click "Create"
5. Wait for project creation (10-30 seconds)
6. **Select your new project** from dropdown

---

## 🔧 **Step 2: Enable Required APIs**

### **2.1 Enable Google Sheets API**

1. In Google Cloud Console, go to:
   ```
   APIs & Services → Library
   ```

2. Search for "Google Sheets API"

3. Click on "Google Sheets API"

4. Click "Enable"

5. Wait for activation (30 seconds)

### **2.2 Enable Google Drive API**

1. Go back to API Library

2. Search for "Google Drive API"

3. Click on "Google Drive API"

4. Click "Enable"

5. Wait for activation (30 seconds)

⚠️ **Important:** Both APIs are required!

### **2.3 Verify APIs Enabled**

1. Go to: APIs & Services → Enabled APIs & Services

2. Confirm you see:
   - ✅ Google Sheets API
   - ✅ Google Drive API

---

## 👤 **Step 3: Create Service Account**

### **3.1 Navigate to Service Accounts**

1. In Google Cloud Console:
   ```
   APIs & Services → Credentials
   ```

2. Click "Create Credentials" → "Service Account"

### **3.2 Configure Service Account**

**Step 1: Service Account Details**
```
Service Account Name: alphastream-portfolio-sa
Service Account ID: alphastream-portfolio-sa
Description: Service account for AlphaStream Portfolio data storage
```

Click "Create and Continue"

**Step 2: Grant Access (Optional)**

Select role: **Editor** (for full access)

Or leave empty for manual permission setup

Click "Continue"

**Step 3: Grant Users Access (Optional)**

Leave empty

Click "Done"

### **3.3 Note Service Account Email**

After creation, you'll see:
```
Service Account Email:
alphastream-portfolio-sa@your-project-id.iam.gserviceaccount.com
```

**⚠️ COPY THIS EMAIL** - You'll need it later!

---

## 🔑 **Step 4: Download Credentials**

### **4.1 Create Key**

1. In Credentials page, find your service account

2. Click on service account name

3. Go to "Keys" tab

4. Click "Add Key" → "Create new key"

5. Select key type: **JSON**

6. Click "Create"

7. **JSON file downloads automatically**

8. Save as `credentials.json` in safe location

⚠️ **Security:** Never commit this file to Git!

### **4.2 Verify Credentials File**

Open `credentials.json` - should look like:

```json
{
  "type": "service_account",
  "project_id": "alphastream-portfolio",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "alphastream-portfolio-sa@project.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/...",
  "universe_domain": "googleapis.com"
}
```

---

## 📊 **Step 5: Create Google Sheet**

### **5.1 Create New Sheet**

1. Go to [Google Sheets](https://sheets.google.com)

2. Click "Blank" to create new sheet

3. Rename sheet:
   ```
   File → Rename
   New Name: AlphaStream_Portfolio_Data
   ```

4. Save (auto-saves)

### **5.2 Copy Sheet URL**

1. Look at browser address bar:
   ```
   https://docs.google.com/spreadsheets/d/1kK1npRBFH3GO_JSxJkuw30OM6wdefsRMsdb1Z4Os3Zw/edit#gid=0
                                          ↑ This is your SHEET_ID
   ```

2. **Copy the entire URL** or just the SHEET_ID

3. Save for later use

⚠️ **Note:** Don't create any tabs or add data - app does this automatically

---

## 🔗 **Step 6: Share Sheet with Service Account**

### **6.1 Open Sharing Settings**

1. In your Google Sheet, click "Share" (top right)

2. In "Add people and groups" field:
   ```
   Paste service account email:
   alphastream-portfolio-sa@your-project-id.iam.gserviceaccount.com
   ```

3. Set permission: **Editor** (not Viewer!)

4. **Uncheck "Notify people"** (service accounts don't need emails)

5. Click "Share"

### **6.2 Verify Sharing**

1. Click "Share" again

2. Under "People with access", verify:
   ```
   ✅ your@email.com (Owner)
   ✅ alphastream-portfolio-sa@... (Editor)
   ```

---

## ⚙️ **Step 7: Configure Streamlit Secrets**

### **7.1 Format Credentials for Streamlit**

Convert your `credentials.json` to TOML format:

**From JSON:**
```json
{
  "type": "service_account",
  "project_id": "alphastream-portfolio",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIE...\n-----END PRIVATE KEY-----\n",
  "client_email": "alphastream-portfolio-sa@project.iam.gserviceaccount.com",
  ...
}
```

**To TOML:**
```toml
STORAGE_TYPE = "google_sheets"
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"

[google_sheets]
type = "service_account"
project_id = "alphastream-portfolio"
private_key_id = "abc123..."
private_key = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
-----END PRIVATE KEY-----
"""
client_email = "alphastream-portfolio-sa@project.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/alphastream-portfolio-sa%40project.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

### **7.2 Add to Streamlit Secrets**

#### **For Streamlit Cloud:**

1. Go to [Streamlit Cloud](https://share.streamlit.io)

2. Open your app

3. Click "Settings" (⚙️) → "Secrets"

4. Paste TOML configuration above

5. **Replace placeholders:**
   - `YOUR_SHEET_ID` → Your actual sheet ID
   - All credential values → From your `credentials.json`

6. **Important formatting notes:**
   - Private key uses triple quotes `"""`
   - Keep all `\n` in private key
   - No quotes around STORAGE_TYPE and GOOGLE_SHEETS_URL

7. Click "Save"

8. Wait for auto-redeploy (30 seconds)

#### **For Local Development:**

1. Create `.streamlit/secrets.toml` in project root

2. Add same configuration as above

3. Save file

⚠️ **Security:** Add `.streamlit/` to `.gitignore`!

### **7.3 Complete Secrets Example**

```toml
# ===== STORAGE CONFIGURATION =====
STORAGE_TYPE = "google_sheets"
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1kK1npRBFH3GO_JSxJkuw30OM6wdefsRMsdb1Z4Os3Zw/edit"

# ===== GOOGLE SHEETS CREDENTIALS =====
[google_sheets]
type = "service_account"
project_id = "alphastream-portfolio-123456"
private_key_id = "abc123def456ghi789"
private_key = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC4Z8...
[FULL PRIVATE KEY HERE - DO NOT TRUNCATE]
...7K8M9N0O1P2Q3R4S5T6U7V8W9X0Y1Z2=
-----END PRIVATE KEY-----
"""
client_email = "alphastream-portfolio-sa@alphastream-portfolio-123456.iam.gserviceaccount.com"
client_id = "123456789012345678901"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/alphastream-portfolio-sa%40alphastream-portfolio-123456.iam.gserviceaccount.com"
universe_domain = "googleapis.com"
```

---

## ✅ **Step 8: Test and Verify**

### **8.1 Test Application Startup**

1. Access your application

2. Check for errors in logs

3. **Success indicators:**
   - App loads without errors
   - No "Google Sheets not found" messages
   - Database loads successfully

### **8.2 Test Data Persistence**

1. **Login to application**

2. **Create test portfolio:**
   ```
   Name: "Test Persistence"
   Principal: $1,000
   Asset: SPY 100%
   ```

3. **Save portfolio**

4. **Check Google Sheet immediately:**
   - Open: AlphaStream_Portfolio_Data
   - Look for new tab: "database"
   - Click cell A1
   - **Should see JSON data** ✅

5. **Test persistence:**
   - Refresh browser (Ctrl+F5)
   - Login again
   - **Portfolio should still exist** ✅

### **8.3 Verify Continuous Sync**

1. Make changes in app (add asset, edit allocation)

2. Check Google Sheet

3. Verify changes appear in cell A1

4. **All updates should sync immediately** ✅

---

## 🐛 **Troubleshooting**

### **Error: "Google Sheets storage selected but libraries not installed"**

**Solution:**
```
Add to requirements.txt:
gspread>=5.12.0
google-auth>=2.23.0
```

### **Error: "Sheet not found at URL"**

**Causes & Solutions:**

1. **Wrong URL in secrets**
   - Verify `GOOGLE_SHEETS_URL` matches your sheet URL
   - Include full URL with https://

2. **Sheet not shared**
   - Check sheet is shared with service account
   - Permission must be "Editor" not "Viewer"

3. **Service account email wrong**
   - Copy exact email from Cloud Console
   - Include full domain

### **Error: "Permission denied" or "403 Forbidden"**

**Solutions:**

1. **Check sheet permissions:**
   - Open sheet → Share
   - Verify service account listed as Editor

2. **Verify APIs enabled:**
   - Google Cloud Console → APIs & Services
   - Confirm both Sheets and Drive APIs enabled

3. **Wait for propagation:**
   - API changes take 2-3 minutes to propagate
   - Reboot app after waiting

### **Error: "Storage quota exceeded"**

**This happens when service account tries to create sheet in its own storage.**

**Solution:**
1. Create sheet in YOUR Google Drive (done in Step 5)
2. Share with service account (done in Step 6)
3. Add sheet URL to secrets (done in Step 7)
4. Service account reads/writes to YOUR sheet (uses your 15GB)

### **Error: "Failed to save after 3 attempts"**

**Causes & Solutions:**

1. **Internet connection:**
   - Check connectivity
   - Try again

2. **API rate limit:**
   - Wait 1 minute
   - Retry

3. **Credentials expired:**
   - Regenerate service account key
   - Update secrets
   - Redeploy

### **Data Not Appearing in Sheet**

**Check:**

1. **STORAGE_TYPE set correctly:**
   ```toml
   STORAGE_TYPE = "google_sheets"  # NOT "json"
   ```

2. **URL outside [google_sheets] section:**
   ```toml
   GOOGLE_SHEETS_URL = "..."  # At TOP level
   
   [google_sheets]  # BELOW URL
   type = "service_account"
   ```

3. **Sheet permissions:**
   - Service account has Editor role
   - Not just Viewer

---

## 🔐 **Security Best Practices**

### **DO:**
- ✅ Keep `credentials.json` secure and private
- ✅ Add credentials to `.gitignore`
- ✅ Use Streamlit Secrets for cloud deployment
- ✅ Limit service account permissions
- ✅ Rotate credentials periodically
- ✅ Monitor access logs

### **DON'T:**
- ❌ Commit credentials to Git
- ❌ Share service account keys
- ❌ Use service account for other purposes
- ❌ Give unnecessary permissions
- ❌ Leave credentials in code

---

## 📊 **Understanding the Setup**

### **Data Flow**

```
Application
    ↓ (save)
Service Account
    ↓ (authenticate)
Google Sheets API
    ↓ (write)
Your Google Sheet
    ↓ (store)
Google Drive (Your 15GB)
```

### **Storage Architecture**

```
Your Google Sheet: AlphaStream_Portfolio_Data
├─ Sheet1 (default, unused)
└─ database (created by app)
   └─ Cell A1: JSON data
       ├─ users
       ├─ portfolios
       ├─ settings
       └─ logs
```

### **Why This Works**

1. **Service Account** - Automated access without human login
2. **Shared Sheet** - Your storage, service account access
3. **API Access** - Programmatic read/write
4. **Cell A1** - Single cell contains all data as JSON
5. **Version History** - Google's built-in backups

---

## 📈 **Storage Capacity**

### **Free Tier Limits**

| Resource | Limit | Your Usage | % Used |
|----------|-------|------------|--------|
| **Google Drive** | 15 GB | ~5 MB | < 0.1% |
| **Sheet Cells** | 5M | ~45K | < 1% |
| **API Requests** | 300/min | ~40/min | 13% |

### **Scalability**

**Current capacity supports:**
- 20 users
- 200 portfolios
- 1,000 assets
- Years of transaction history

**Well within free tier limits!** ✅

---

## ✅ **Setup Checklist**

Use this to verify complete setup:

- [ ] Google Cloud Project created
- [ ] Google Sheets API enabled
- [ ] Google Drive API enabled
- [ ] Service Account created
- [ ] Service Account key downloaded
- [ ] Google Sheet created
- [ ] Sheet shared with service account (Editor permission)
- [ ] Sheet URL copied
- [ ] Streamlit Secrets configured
- [ ] STORAGE_TYPE set to "google_sheets"
- [ ] GOOGLE_SHEETS_URL added (at top level)
- [ ] All credentials from JSON added to [google_sheets] section
- [ ] Private key formatted correctly (triple quotes, all \n preserved)
- [ ] App redeployed
- [ ] Test portfolio created
- [ ] Data appears in Google Sheet
- [ ] Data persists after refresh

---

## 🎉 **Success!**

If you've completed all steps:

✅ **Your application now has enterprise-grade persistent storage!**

**Benefits:**
- Data survives app restarts ✅
- Automatic backups ✅
- Version history ✅
- 99.99% uptime ✅
- Free forever (within limits) ✅

---

## 📚 **Additional Resources**

- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [gspread Documentation](https://docs.gspread.org)
- [Streamlit Secrets](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)

---

**Setup complete? Return to [Installation Guide](INSTALLATION.md)!** 🚀

**Having issues? Check [Troubleshooting](TROUBLESHOOTING.md)!** 🔧
