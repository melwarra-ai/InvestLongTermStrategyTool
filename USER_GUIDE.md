# 📖 User Guide

Complete guide to using AlphaStream Portfolio Optimizer

---

## 📋 **Table of Contents**

- [Getting Started](#getting-started)
- [User Authentication](#user-authentication)
- [Portfolio Management](#portfolio-management)
- [Asset Management](#asset-management)
- [Drift Monitoring & Rebalancing](#drift-monitoring--rebalancing)
- [Benchmark Comparison](#benchmark-comparison)
- [Analytics & Reports](#analytics--reports)
- [Admin Features](#admin-features)
- [Best Practices](#best-practices)

---

## 🚀 **Getting Started**

### **First Login**

1. **Access the application**
   - Local: `http://localhost:8501`
   - Cloud: `https://yourapp.streamlit.app`

2. **Login with credentials**
   - **Admin:** `admin` / `admin123`
   - **User:** Your assigned credentials

3. **Change your password**
   - Click username → Account → Change Password

### **Interface Overview**

```
┌─────────────────────────────────────┐
│  [Logo] Portfolio Optimizer         │
│  User: John Doe                     │
├─────────────────────────────────────┤
│                                     │
│  ⚙️ Setup Progress: X/6 steps      │
│                                     │
│  📊 Navigation:                     │
│    - Global Dashboard               │
│    - Portfolio Manager              │
│                                     │
│  📋 Strategy Setup:                 │
│    ① Create New Profile            │
│                                     │
│  🎯 Active Portfolio:               │
│    Select from dropdown             │
│                                     │
│  ② Drift Strategy                  │
│  ③ Benchmark Comparison            │
│  ④ Asset Mix                       │
│  ⑤ Deploy Capital                  │
│  ⑥ Monitor & Rebalance             │
│                                     │
└─────────────────────────────────────┘
```

---

## 🔐 **User Authentication**

### **Logging In**

1. **Enter credentials**
   ```
   Username: [your_username]
   Password: [your_password]
   ```

2. **Click "Sign In"**

3. **Access your dashboard**

### **Changing Password**

1. **Navigate to Account**
   - Click username (top right)
   - Select "Change Password"

2. **Enter passwords**
   ```
   Current Password: [current]
   New Password: [new_secure_password]
   Confirm New Password: [new_secure_password]
   ```

3. **Click "Update Password"**

4. **Success confirmation**

### **Creating New Account (If Enabled)**

1. **Click "Create Account"** (login page)

2. **Fill registration form**
   ```
   Username: [choose_username]
   Email: [your_email]
   Password: [secure_password]
   Confirm Password: [secure_password]
   Display Name: [Your Name]
   ```

3. **Submit registration**

4. **Wait for admin approval** (if required)

5. **Login with new credentials**

---

## 📊 **Portfolio Management**

### **Creating a New Portfolio**

#### **Step 1: Navigate to Portfolio Creation**
```
Portfolio Manager → Create New Profile
```

#### **Step 2: Enter Portfolio Details**

**Required Information:**
```
Profile Name: "Retirement Portfolio"
Principal Amount: $100,000
Currency: USD (default)
```

**Account Information (Optional):**
```
Bank Name: "TD"
Account Type: "RRSP"
Account Name: "TD RRSP"
Initialization Date: 2025-01-27 (auto-filled)
```

**Settings:**
```
Drift Tolerance: 5.0% (default)
Yearly Goal: 10.0% (optional)
```

#### **Step 3: Click "Create Profile"**

#### **Step 4: Verify Creation**
- Profile appears in dropdown
- Setup progress shows "✅ ① Profile Created"

### **Selecting Active Portfolio**

1. **Go to "Active Profile" section**

2. **Click dropdown**
   ```
   Select Profile
   ├── Retirement Portfolio
   ├── Trading Account
   └── College Fund
   ```

3. **Choose portfolio**

4. **View portfolio details**

### **Editing Portfolio Settings**

1. **Select portfolio** (from dropdown)

2. **Click "Profile Actions" → "Edit Settings"**

3. **Modify fields:**
   - Principal amount
   - Drift tolerance
   - Account details
   - Yearly goal

4. **Save changes**

### **Deleting a Portfolio**

⚠️ **Warning: This action cannot be undone!**

1. **Select portfolio**

2. **Admin Panel** → User Management → Manage Profiles

3. **Find portfolio** in list

4. **Click "Delete"**

5. **Confirm deletion**

---

## 💼 **Asset Management**

### **Adding Assets to Portfolio**

#### **Method 1: Manual Entry**

1. **Select portfolio**

2. **Navigate to "Asset Mix"**

3. **Click "Add Asset"**

4. **Enter asset details:**
   ```
   Ticker Symbol: SPY
   Fund Name: S&P 500 ETF (auto-filled)
   Target Allocation: 40.0%
   ```

5. **Click "Save Asset"**

6. **Repeat** for other assets

#### **Method 2: Quick Add (Fast)**

1. **Go to "Asset Mix" section**

2. **Use Quick Add buttons:**
   ```
   [SPY] [QQQ] [VTI] [VXUS] [AGG]
   [GLD] [VNQ] [SCHD] [BND] [TLT]
   ```

3. **Click ticker button**

4. **Asset added with default allocation**

5. **Adjust allocation** as needed

### **Editing Asset Allocation**

1. **Select portfolio**

2. **View asset list:**
   ```
   Asset         Target    Current    Drift
   SPY           40.0%     38.5%      🟡 -1.5%
   QQQ           30.0%     31.2%      🟡 +1.2%
   AGG           30.0%     30.3%      🟢 +0.3%
   ```

3. **Click "Edit" next to asset**

4. **Modify target allocation**

5. **Save changes**

### **Removing Assets**

1. **Select asset** from list

2. **Click "Remove Asset"**

3. **Confirm removal**

4. **Rebalance** remaining allocations

### **Locking Asset Mix**

⚠️ **Lock asset mix before deploying capital**

1. **Review all assets**

2. **Verify total allocation = 100%**

3. **Click "Lock Asset Mix"**

4. **Confirmation:**
   ```
   ✅ Asset mix locked
   ⚠️ Asset mix not locked (if total ≠ 100%)
   ```

---

## 🔄 **Drift Monitoring & Rebalancing**

### **Understanding Drift**

**Drift** = Difference between current and target allocation

**Example:**
```
Asset: SPY
Target: 40.0%
Current: 38.5%
Drift: -1.5% (underweight)
```

**Drift Tolerance:**
- Default: 5.0%
- Customizable per portfolio
- Alert when drift exceeds tolerance

### **Monitoring Drift**

#### **Portfolio Dashboard View**

```
🎯 Drift Status: BALANCED / NEEDS REBALANCING

✅ All assets within tolerance

OR

⚠️ DRIFT ALERT: Rebalancing Required
2 asset(s) exceeded your 5.0% drift tolerance
```

#### **Detailed Drift Table**

```
Assets Requiring Rebalancing:

Asset    Drift      Current    Target    Action
SPY      🔴 -8.2%   31.8%     40.0%     BUY
QQQ      🔴 +7.5%   37.5%     30.0%     SELL
AGG      🟢 +0.7%   30.7%     30.0%     HOLD
```

**Color Codes:**
- 🟢 **Green:** Within tolerance (< 3%)
- 🟡 **Yellow:** Moderate drift (3-5%)
- 🔴 **Red:** Exceeds tolerance (> 5%)

### **Rebalancing Your Portfolio**

#### **Step 1: Review Recommendations**

```
📊 Rebalancing Required

Current Portfolio Value: $105,234

Recommended Actions:
├─ BUY $8,650 of SPY (buy 52 shares)
├─ SELL $7,890 of QQQ (sell 20 shares)
└─ HOLD AGG
```

#### **Step 2: Implement Trades**

**Option A: Manual Trading**
1. Note recommendations
2. Execute trades in your brokerage
3. Record purchases in app

**Option B: Record Purchase**
1. Click "Record Purchase" for asset
2. Enter details:
   ```
   Date: 2025-01-27
   Amount: $8,650
   Price: $167.20
   Quantity: 52
   ```
3. Save transaction

#### **Step 3: Verify Rebalance**

1. **Check drift status:**
   ```
   ✅ All assets balanced
   Last Rebalanced: 2025-01-27
   ```

2. **Review portfolio:**
   - All assets within tolerance ✅
   - Target allocations met ✅

---

## 📈 **Benchmark Comparison**

### **Adding Benchmarks**

1. **Navigate to "Benchmark Comparison"**

2. **Click "Select Benchmarks"**

3. **Choose from available options:**
   ```
   Available Benchmarks:
   ☐ S&P 500 (^GSPC)
   ☐ NASDAQ (^IXIC)
   ☐ Dow Jones (^DJI)
   ☐ Russell 2000 (^RUT)
   ☐ 60/40 Portfolio
   ☐ All Weather Portfolio
   ```

4. **Select benchmarks** (multiple allowed)

5. **Save selection**

### **Viewing Benchmark Comparison**

```
Portfolio vs Benchmarks (1 Year)

Portfolio:          +12.5% 📈
S&P 500:            +10.3% 📈
60/40 Portfolio:     +8.7% 📈
All Weather:         +7.2% 📈

Performance:        OUTPERFORMING ✅
```

### **Analyzing Performance**

**Metrics Compared:**
- Total Return (%)
- Annualized Return (CAGR)
- Volatility (Standard Deviation)
- Sharpe Ratio
- Maximum Drawdown

**Example Analysis:**
```
Your Portfolio Performance:
├─ Return: +12.5% (vs S&P 500: +10.3%)
├─ Volatility: 15.2% (vs S&P 500: 18.5%)
├─ Sharpe Ratio: 0.82 (vs S&P 500: 0.56)
└─ Max Drawdown: -12.3% (vs S&P 500: -15.8%)

Conclusion: ✅ Outperforming with lower risk
```

---

## 📊 **Analytics & Reports**

### **Portfolio Analytics Dashboard**

#### **Current Value Section**
```
Total Portfolio Value: $105,234
Principal Invested: $100,000
Total Gain: $5,234 (+5.23%)
Undeployed Cash: $1,523
```

#### **Performance Metrics**
```
Total ROI: +5.23%
Annualized Return (CAGR): +8.45%
Portfolio Age: 1.3 years
Time-Weighted Return: +5.18%
```

#### **Risk Metrics**
```
Volatility (σ): 15.2%
Sharpe Ratio: 0.82
Beta: 0.95
Max Drawdown: -12.3%
```

#### **Asset Allocation Chart**
```
[Pie Chart showing current allocation]

SPY  40.2%  ████████
QQQ  30.5%  ██████
AGG  29.3%  ██████
```

### **Transaction History**

```
📜 Activity Log

Date         Type        Asset  Amount    Details
2025-01-27  Purchase    SPY    $40,000   Initial
2025-01-27  Purchase    QQQ    $30,000   Initial
2025-01-27  Purchase    AGG    $30,000   Initial
2025-02-15  Rebalance   SPY    +$2,500   Drift correction
2025-02-15  Rebalance   QQQ    -$2,500   Drift correction
```

### **Generating Reports**

1. **Navigate to Portfolio Manager**

2. **Select "View Analytics"**

3. **Choose report type:**
   - Portfolio Summary
   - Performance Report
   - Asset Allocation
   - Transaction History

4. **Export options:**
   - View on screen
   - Download PDF (if enabled)
   - Copy to clipboard

---

## 👑 **Admin Features**

### **User Management**

#### **Viewing All Users**
```
Admin Panel → User Management

Users List:
├─ admin (Administrator) - 3 portfolios
├─ john_doe (User) - 5 portfolios
└─ jane_smith (User) - 2 portfolios
```

#### **Creating New Users**

1. **Admin Panel** → User Management

2. **Click "Create New User"**

3. **Enter user details:**
   ```
   Username: new_user
   Email: newuser@example.com
   Password: [generate secure]
   Display Name: New User
   Role: User / Admin
   ```

4. **Set initial settings**

5. **Create user**

#### **Managing User Portfolios**

1. **Select user** from list

2. **View user's portfolios:**
   ```
   john_doe's Portfolios:
   ├─ Retirement Fund ($500,000)
   ├─ Trading Account ($50,000)
   └─ College Savings ($30,000)
   ```

3. **Available actions:**
   - View portfolio details
   - Edit settings
   - Delete portfolio (⚠️ caution)
   - Impersonate user (admin only)

#### **Impersonation Mode**

**For troubleshooting/support:**

1. **Admin Panel** → User Management

2. **Select user**

3. **Click "View as User"**

4. **Warning displayed:**
   ```
   ⚠️ IMPERSONATION MODE
   👑 Admin viewing as: john_doe
   ```

5. **Experience app as that user**

6. **Exit:** Click username → "Back to Admin"

### **Global Settings**

#### **Configuring Defaults**

1. **Admin Panel** → Global Settings

2. **Available settings:**
   ```
   Default Drift Tolerance: 5.0%
   Allow User Registration: Yes/No
   Default Currency: USD
   Max Portfolios Per User: 10
   Market Data Update Frequency: Real-time
   ```

3. **Modify as needed**

4. **Save changes**

#### **System Configuration**

```
Storage Configuration:
├─ Type: Google Sheets / JSON
├─ Status: Connected ✅
└─ Last Sync: 2025-01-27 10:30:15

Performance:
├─ Active Users: 15
├─ Total Portfolios: 47
└─ Total Assets Tracked: 203
```

### **Activity Logs**

```
System Logs:
Date Time         User      Action
2025-01-27 10:30  john_doe  Created portfolio "Retirement"
2025-01-27 10:35  john_doe  Added asset SPY
2025-01-27 10:40  admin     Changed global setting
2025-01-27 11:00  jane      Rebalanced portfolio
```

---

## 💡 **Best Practices**

### **Portfolio Setup**

1. **Start with clear goals**
   - Define investment objectives
   - Set realistic return targets
   - Determine risk tolerance

2. **Diversify appropriately**
   - Mix of asset classes
   - 60/40 or 80/20 stocks/bonds
   - Consider international exposure

3. **Set reasonable drift tolerance**
   - 5% for typical portfolios
   - 3% for tighter control
   - 10% for lazy rebalancing

### **Asset Management**

1. **Use established ETFs**
   - Lower costs
   - High liquidity
   - Transparent holdings

2. **Keep it simple**
   - 5-10 assets maximum
   - Avoid overlap
   - Clear purpose for each

3. **Lock asset mix before deploying**
   - Prevents accidental changes
   - Ensures allocation accuracy

### **Monitoring & Rebalancing**

1. **Check drift regularly**
   - Monthly for active portfolios
   - Quarterly for long-term

2. **Rebalance when needed**
   - When drift exceeds tolerance
   - During contributions
   - At tax loss harvest opportunities

3. **Consider costs**
   - Trading fees
   - Tax implications
   - Spread costs

### **Security**

1. **Use strong passwords**
   - Minimum 12 characters
   - Mix of letters, numbers, symbols
   - Unique per account

2. **Change passwords regularly**
   - Every 90 days
   - Immediately if compromised

3. **Limit admin access**
   - Only necessary personnel
   - Review permissions regularly

### **Data Management**

1. **Regular backups** (if using JSON)
   - Weekly minimum
   - Store securely
   - Test restoration

2. **Monitor storage** (Google Sheets)
   - Check cell A1 periodically
   - Verify data updates
   - Review version history

3. **Clean up old data**
   - Archive old portfolios
   - Remove inactive users
   - Optimize performance

---

## 🆘 **Getting Help**

### **In-App Help**

- ℹ️ **Info buttons** - Hover for tooltips
- 📖 **Help sections** - Click "?" icons
- 📋 **Setup guide** - Follow step numbers

### **Documentation**

- [Installation Guide](INSTALLATION.md)
- [Quick Reference](QUICK_REFERENCE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Setup Google Sheets](SETUP_GOOGLE_SHEETS.md)

### **Support Channels**

1. **GitHub Issues** - Bug reports and features
2. **Email** - support@alphastream.example.com
3. **Community** - Forums and discussions

---

## 📚 **Additional Resources**

### **Investment Education**
- Modern Portfolio Theory
- Asset Allocation Strategies
- Rebalancing Best Practices
- Risk Management

### **Technical Resources**
- API Documentation
- Developer Guide
- Contributing Guidelines

---

**Ready to start? Create your first portfolio!** 🚀

**Questions? Check the [Quick Reference](QUICK_REFERENCE.md) for fast answers!**
