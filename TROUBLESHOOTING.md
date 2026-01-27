# 🔧 Troubleshooting Guide

Solutions to common issues in AlphaStream Portfolio Optimizer

---

## 📋 **Table of Contents**

- [Installation Issues](#installation-issues)
- [Authentication Problems](#authentication-problems)
- [Google Sheets Issues](#google-sheets-issues)
- [Portfolio & Data Issues](#portfolio--data-issues)
- [Performance Problems](#performance-problems)
- [Market Data Issues](#market-data-issues)
- [UI & Display Issues](#ui--display-issues)
- [Getting Additional Help](#getting-additional-help)

---

## 🚫 **Installation Issues**

### **Problem: `pip install` fails**

**Error:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solutions:**

1. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Check Python version:**
   ```bash
   python --version  # Must be 3.9+
   ```

3. **Install with verbose output:**
   ```bash
   pip install -r requirements.txt --verbose
   ```

### **Problem: `ModuleNotFoundError` when running app**

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solutions:**

1. **Verify virtual environment activated:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Check installation:**
   ```bash
   pip list | grep streamlit
   ```

### **Problem: Port 8501 already in use**

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**

1. **Kill process using port:**
   ```bash
   # Mac/Linux
   lsof -ti:8501 | xargs kill -9
   
   # Windows
   netstat -ano | findstr :8501
   taskkill /PID [PID_NUMBER] /F
   ```

2. **Use different port:**
   ```bash
   streamlit run app.py --server.port 8502
   ```

---

## 🔐 **Authentication Problems**

### **Problem: Can't login with admin credentials**

**Symptoms:**
- "Invalid username or password" error
- Admin account not found

**Solutions:**

1. **Verify credentials:**
   ```
   Default username: admin
   Default password: admin123
   ```

2. **Check if data exists:**
   - If using JSON: Check `alphastream_multiuser.json` exists
   - If using Google Sheets: Check cell A1 in database tab

3. **Reset to defaults:**
   - Delete data file (JSON) or clear Sheet cell A1
   - Restart app
   - Default admin account recreated

### **Problem: "Account locked" message**

**Cause:** Too many failed login attempts

**Solution:**

**If you're admin:**
1. Access data directly
2. JSON: Edit `lockout_until` to null
3. Google Sheets: Edit user data in cell A1

**If you're user:**
1. Wait 15 minutes for automatic unlock
2. Contact administrator
3. Request password reset

### **Problem: Password change doesn't save**

**Symptoms:**
- Old password still works
- New password rejected

**Solutions:**

1. **Check storage:**
   - Verify Google Sheets configured
   - Check data persists after save

2. **Clear browser cache:**
   ```
   Ctrl+Shift+Delete (Windows)
   Cmd+Shift+Delete (Mac)
   ```

3. **Try in incognito/private mode**

---

## ☁️ **Google Sheets Issues**

### **Problem: "Google Sheets storage selected but libraries not installed"**

**Error:**
```
❌ Google Sheets storage selected but libraries not installed!
```

**Solution:**

Add to `requirements.txt`:
```
gspread>=5.12.0
google-auth>=2.23.0
```

Redeploy application.

### **Problem: "Sheet not found at URL"**

**Error:**
```
❌ Sheet not found at URL: https://docs.google.com/...
```

**Solutions:**

1. **Verify URL in secrets:**
   ```toml
   GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
   ```

2. **Check sheet exists:**
   - Open URL in browser
   - Should open Google Sheet

3. **Verify sharing:**
   - Sheet must be shared with service account
   - Permission: Editor (not Viewer)

4. **Check service account email:**
   - From `credentials.json`: `client_email` field
   - Format: `name@project.iam.gserviceaccount.com`

### **Problem: "Permission denied" (403 error)**

**Error:**
```
APIError: [403]: Permission denied
```

**Solutions:**

1. **Share sheet with service account:**
   - Open sheet → Click "Share"
   - Add service account email
   - Set role: Editor
   - Uncheck "Notify people"
   - Click "Share"

2. **Verify APIs enabled:**
   - Google Sheets API ✅
   - Google Drive API ✅ (often forgotten!)

3. **Wait for propagation:**
   - Changes take 2-3 minutes
   - Reboot app after waiting

### **Problem: "Storage quota exceeded"**

**Error:**
```
APIError: [403]: The user's Drive storage quota has been exceeded
```

**Cause:** Service account tried to create sheet in its own storage

**Solution:**

1. Create sheet in YOUR Google Drive
2. Share with service account (Editor permission)
3. Add sheet URL to secrets:
   ```toml
   GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/YOUR_ID/edit"
   ```

### **Problem: Data not appearing in Google Sheet**

**Symptoms:**
- Cell A1 is empty
- No "database" tab
- Changes don't sync

**Solutions:**

1. **Check STORAGE_TYPE:**
   ```toml
   STORAGE_TYPE = "google_sheets"  # NOT "json"
   ```

2. **Verify URL placement:**
   ```toml
   # CORRECT:
   GOOGLE_SHEETS_URL = "..."  # At top level
   
   [google_sheets]
   type = "service_account"
   
   # WRONG:
   [google_sheets]
   GOOGLE_SHEETS_URL = "..."  # Inside section
   ```

3. **Test save manually:**
   - Create portfolio
   - Check for error messages
   - Review Streamlit Cloud logs

### **Problem: "Error 400 (Bad Request)"**

**Symptoms:**
- Data won't save
- "Malformed request" error

**Cause:** Using wrong API method

**Solution:**

Verify app code uses:
```python
worksheet.update_acell('A1', data_json)  # ✅ Correct

# NOT:
worksheet.update('A1', data_json)  # ❌ Wrong
```

**This should already be fixed in v7.0.4+**

---

## 📊 **Portfolio & Data Issues**

### **Problem: Portfolio not saving**

**Symptoms:**
- Data lost after refresh
- Changes don't persist

**Solutions:**

1. **Check storage type:**
   - If using JSON on Streamlit Cloud: Won't persist!
   - Use Google Sheets for persistence

2. **Verify Google Sheets:**
   - Check secrets configured
   - Verify sheet accessible
   - Look for error messages

3. **Check browser console:**
   - Press F12
   - Look for JavaScript errors

### **Problem: "Drift calculation seems wrong"**

**Symptoms:**
- Drift numbers don't match expectations
- Inconsistent drift values

**Solutions:**

1. **Verify target allocations:**
   - Sum must equal 100%
   - Check each asset target

2. **Update market prices:**
   - Refresh page
   - Wait for price update
   - Check internet connection

3. **Check for rounding:**
   - Small differences (<0.1%) are normal
   - Due to share quantity rounding

### **Problem: Can't add asset with ticker**

**Error:**
```
Asset [TICKER] not found
```

**Solutions:**

1. **Verify ticker symbol:**
   - Check on Yahoo Finance
   - Try alternative ticker
   - Example: BRK.B not BRK-B

2. **Check market hours:**
   - Some tickers unavailable after hours
   - Try during market hours (9:30 AM - 4:00 PM ET)

3. **Try common alternatives:**
   ```
   Apple: AAPL
   Microsoft: MSFT
   S&P 500: SPY or ^GSPC
   ```

### **Problem: Portfolio value shows zero**

**Symptoms:**
- Total value = $0
- All assets show $0

**Solutions:**

1. **Deploy capital:**
   - Must record purchases
   - Can't just set allocations

2. **Check purchase records:**
   - Navigate to Asset Mix
   - Verify purchases exist
   - Review quantities and prices

3. **Update prices:**
   - Refresh page
   - Check internet connection

---

## ⚡ **Performance Problems**

### **Problem: App loads slowly**

**Symptoms:**
- Long initial load time
- Spinning/waiting indicators

**Solutions:**

1. **Check internet connection**

2. **Clear browser cache:**
   ```
   Ctrl+Shift+Delete
   ```

3. **Reduce portfolio size:**
   - Fewer assets (< 20)
   - Less transaction history

4. **For Streamlit Cloud:**
   - Free tier has resource limits
   - Consider upgrading

### **Problem: Market data not updating**

**Symptoms:**
- Stale prices
- Last updated time old

**Solutions:**

1. **Refresh page:**
   ```
   Ctrl+F5 (hard refresh)
   ```

2. **Check Yahoo Finance:**
   - Visit finance.yahoo.com
   - Verify symbol exists
   - Check if delayed data

3. **API rate limits:**
   - yfinance has rate limits
   - Wait 1 minute, try again

---

## 📈 **Market Data Issues**

### **Problem: "No data found for ticker"**

**Error:**
```
No data found, symbol may be delisted
```

**Solutions:**

1. **Verify ticker symbol:**
   - Check Yahoo Finance directly
   - Try full exchange suffix
   - Example: GOOGL vs GOOG

2. **Check delisting:**
   - Stock may be delisted
   - Merger or acquisition
   - Update to new ticker

3. **Try alternative data sources:**
   - Use ETF instead of individual stock
   - Check if ticker moved exchanges

### **Problem: Prices seem incorrect**

**Symptoms:**
- Prices don't match broker
- Significantly off-market

**Solutions:**

1. **Check price source:**
   - yfinance uses Yahoo Finance data
   - May have 15-20 minute delay
   - Compare to Yahoo Finance website

2. **Currency mismatch:**
   - Ensure same currency
   - Convert if necessary

3. **After-hours trading:**
   - May show after-hours price
   - Refresh during market hours

---

## 🎨 **UI & Display Issues**

### **Problem: Layout looks broken**

**Symptoms:**
- Elements overlapping
- Text cut off
- Buttons missing

**Solutions:**

1. **Zoom level:**
   - Reset browser zoom to 100%
   - Ctrl+0 (Windows) / Cmd+0 (Mac)

2. **Browser compatibility:**
   - Use latest Chrome/Firefox/Safari
   - Clear cache
   - Try different browser

3. **Screen size:**
   - Minimum width: 1024px recommended
   - Use desktop/laptop, not phone

### **Problem: Colors not showing correctly**

**Symptoms:**
- All items same color
- No green/yellow/red indicators

**Solutions:**

1. **Refresh page:**
   ```
   Ctrl+F5
   ```

2. **Check browser mode:**
   - Disable dark mode extensions
   - Use standard mode

3. **Update browser:**
   - May need latest version
   - Update and restart

---

## 🔍 **Diagnostic Steps**

### **General Troubleshooting Process**

1. **Check error messages:**
   - Read full error
   - Note error code
   - Screenshot if possible

2. **Check logs:**
   - **Local:** Terminal output
   - **Streamlit Cloud:** App → Manage → Logs

3. **Verify configuration:**
   - Review secrets/environment variables
   - Check all values correct
   - Look for typos

4. **Test isolation:**
   - Try in incognito mode
   - Test on different device
   - Check different browser

5. **Search docs:**
   - Check this guide
   - Review [USER_GUIDE.md](USER_GUIDE.md)
   - Search [GitHub Issues](https://github.com/yourusername/alphastream-portfolio/issues)

### **Getting Debug Information**

**For Support Requests, include:**

1. **Version:**
   - Check footer: `v7.1.0`

2. **Environment:**
   - Local or Streamlit Cloud
   - Python version
   - Operating system

3. **Error details:**
   - Full error message
   - Steps to reproduce
   - Expected vs actual behavior

4. **Configuration:**
   - Storage type (JSON or Sheets)
   - Deployment method
   - Browser and version

5. **Logs:**
   - Last 50 lines from logs
   - Timestamp of error
   - Any warnings

---

## 🆘 **Getting Additional Help**

### **Before Opening Issue**

1. ✅ Check this guide
2. ✅ Search [existing issues](https://github.com/yourusername/alphastream-portfolio/issues)
3. ✅ Review [USER_GUIDE.md](USER_GUIDE.md)
4. ✅ Try basic troubleshooting steps

### **Opening GitHub Issue**

**Use this template:**

```
**Version:** v7.1.0
**Environment:** Streamlit Cloud / Local
**Storage:** Google Sheets / JSON

**Description:**
[What happened?]

**Steps to Reproduce:**
1. [First step]
2. [Second step]
3. [Error occurs]

**Expected Behavior:**
[What should happen?]

**Actual Behavior:**
[What actually happened?]

**Error Messages:**
```
[Paste error messages]
```

**Logs:**
```
[Paste relevant logs]
```

**Screenshots:**
[Attach if helpful]
```

### **Contact Support**

- **Email:** support@alphastream.example.com
- **GitHub:** [Open Issue](https://github.com/yourusername/alphastream-portfolio/issues/new)
- **Response Time:** 24-48 hours

---

## ✅ **Common Solutions Checklist**

Quick checklist for most issues:

- [ ] Check internet connection
- [ ] Refresh page (Ctrl+F5)
- [ ] Clear browser cache
- [ ] Try incognito/private mode
- [ ] Check Streamlit Cloud logs
- [ ] Verify secrets configured correctly
- [ ] Check Google Sheets permissions
- [ ] Restart application
- [ ] Update dependencies
- [ ] Check for typos in configuration

---

## 📚 **Additional Resources**

- [User Guide](USER_GUIDE.md) - Complete usage guide
- [Installation Guide](INSTALLATION.md) - Setup instructions
- [Google Sheets Setup](SETUP_GOOGLE_SHEETS.md) - Storage configuration
- [GitHub Issues](https://github.com/yourusername/alphastream-portfolio/issues) - Known issues
- [Streamlit Docs](https://docs.streamlit.io) - Framework documentation

---

**Can't find your issue? [Open a GitHub Issue](https://github.com/yourusername/alphastream-portfolio/issues/new)!** 🆘
