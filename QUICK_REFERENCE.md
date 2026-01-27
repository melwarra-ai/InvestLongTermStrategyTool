# ⚡ Quick Reference Guide

Fast lookup guide for common tasks in AlphaStream Portfolio Optimizer

---

## 🔑 **Default Login**

```
Username: admin
Password: admin123
```
⚠️ Change immediately after first login!

---

## 🚀 **Quick Start (5 Minutes)**

1. **Login** → Use credentials above
2. **Create Portfolio** → Portfolio Manager → Create New Profile
3. **Add Assets** → Quick Add buttons or manual entry
4. **Set Targets** → Define allocation percentages
5. **Lock Mix** → Enable after all assets added
6. **Done!** → Monitor drift and rebalance as needed

---

## 📊 **Common Tasks**

### **Create New Portfolio**
```
Portfolio Manager → Create New Profile
├─ Name: "My Portfolio"
├─ Principal: $100,000
└─ Create
```

### **Add Asset**
```
Asset Mix → Quick Add: [SPY] [QQQ] [AGG]
OR
Add Asset → Enter ticker → Set target → Save
```

### **Check Drift**
```
Portfolio Manager → View active portfolio
└─ Drift Status: BALANCED / NEEDS REBALANCING
```

### **Rebalance**
```
Follow recommendations in drift alert
Record Purchase → Enter details → Save
```

### **Change Password**
```
Username (top right) → Account → Change Password
```

---

## 🎯 **Key Metrics**

| Metric | Description | Ideal Range |
|--------|-------------|-------------|
| **Drift** | % difference from target | < 5% |
| **ROI** | Total return on investment | > Market average |
| **Sharpe Ratio** | Risk-adjusted return | > 1.0 |
| **Volatility** | Standard deviation of returns | < 20% |
| **Max Drawdown** | Largest peak-to-trough decline | < 30% |

---

## 🚦 **Status Indicators**

### **Drift Colors**
- 🟢 **Green** - Within tolerance (< 3%)
- 🟡 **Yellow** - Moderate drift (3-5%)
- 🔴 **Red** - Exceeds tolerance (> 5%)

### **Portfolio Status**
- ✅ **Deployed** - Capital allocated, ready to track
- ⚙️ **Setup** - Configuration in progress
- ⚠️ **Alert** - Rebalancing required

---

## 📋 **Setup Steps**

1. ✅ **Profile Created** - Portfolio exists
2. ✅ **Principal Set** - Initial investment defined
3. ✅ **Benchmarks Added** - Comparison baselines set
4. ✅ **Assets Allocated** - Investments selected
5. ✅ **Mix Locked** - Asset allocation finalized
6. ✅ **Deployed** - Capital invested and tracking

---

## 💼 **Popular Asset Tickers**

### **US Stocks**
- **SPY** - S&P 500
- **QQQ** - NASDAQ 100
- **VTI** - Total US Market
- **SCHD** - Dividend Aristocrats

### **International**
- **VXUS** - Total International
- **EFA** - Developed Markets
- **VWO** - Emerging Markets

### **Bonds**
- **AGG** - Total Bond Market
- **BND** - Bond Index
- **TLT** - Long-term Treasury
- **VCSH** - Short-term Corporate

### **Other**
- **GLD** - Gold
- **VNQ** - Real Estate
- **DBC** - Commodities

---

## 🔧 **Keyboard Shortcuts**

| Action | Shortcut |
|--------|----------|
| **Refresh page** | Ctrl+F5 (Windows) / Cmd+Shift+R (Mac) |
| **Navigate back** | Backspace |
| **Search** | Ctrl+F / Cmd+F |
| **Open settings** | (Click username) |

---

## ⚙️ **Common Settings**

### **Drift Tolerance**
```
Conservative: 3%
Moderate: 5% (default)
Aggressive: 10%
```

### **Rebalancing Frequency**
```
Active: Monthly
Moderate: Quarterly
Passive: Annually
```

### **Asset Mix Strategies**
```
Conservative: 40/60 (stocks/bonds)
Balanced: 60/40
Aggressive: 80/20
Very Aggressive: 100/0
```

---

## 📊 **Sample Portfolios**

### **Conservative (Low Risk)**
```
40% SPY (US Stocks)
30% AGG (Bonds)
20% VXUS (International)
10% GLD (Gold)
```

### **Balanced (Moderate Risk)**
```
50% VTI (US Stocks)
30% VXUS (International)
15% AGG (Bonds)
5% VNQ (Real Estate)
```

### **Aggressive (High Risk)**
```
60% QQQ (Tech-heavy)
20% VWO (Emerging Markets)
10% GLD (Gold)
10% TLT (Bonds)
```

### **All Weather (Ray Dalio)**
```
30% SPY (Stocks)
40% TLT (Long-term Bonds)
15% AGG (Intermediate Bonds)
7.5% GLD (Gold)
7.5% DBC (Commodities)
```

---

## 🐛 **Quick Troubleshooting**

### **Can't login**
- Check username/password
- Try password reset
- Contact admin

### **Portfolio not saving**
- Check Google Sheets connection
- Verify secrets configured
- Review app logs

### **Drift calculation wrong**
- Verify current prices updated
- Check target allocations sum to 100%
- Refresh market data

### **Asset not found**
- Verify ticker symbol correct
- Check market is open
- Try alternative ticker

### **Data not persisting**
- Confirm Google Sheets configured
- Check STORAGE_TYPE setting
- Verify sheet permissions

---

## 📞 **Quick Support**

### **Error Messages**

| Error | Solution |
|-------|----------|
| "Google Sheets not installed" | Add gspread to requirements.txt |
| "Sheet not found" | Check GOOGLE_SHEETS_URL in secrets |
| "Permission denied" | Share sheet with service account |
| "Failed to save" | Check internet connection |

### **Get Help**
1. **Check logs** - Streamlit Cloud → Logs
2. **Review docs** - [USER_GUIDE.md](USER_GUIDE.md)
3. **Search issues** - GitHub Issues
4. **Open ticket** - support@alphastream.example.com

---

## 🔐 **Security Quick Tips**

- ✅ Change default admin password
- ✅ Use unique passwords per user
- ✅ Enable 2FA if available
- ✅ Review user permissions regularly
- ✅ Monitor activity logs
- ❌ Never share credentials
- ❌ Don't use public computers
- ❌ Avoid simple passwords

---

## 📱 **Mobile Usage**

### **Accessing on Mobile**
```
1. Open browser (Chrome/Safari)
2. Go to app URL
3. Login normally
4. Use landscape mode for better experience
```

### **Mobile-Friendly Features**
- ✅ Responsive layout
- ✅ Touch-friendly buttons
- ✅ Scrollable tables
- ⚠️ Some features better on desktop

---

## 💡 **Pro Tips**

### **Portfolio Management**
1. Rebalance during market dips (buy opportunities)
2. Consider tax implications before selling
3. Use limit orders for large rebalances
4. Track cost basis for tax reporting

### **Asset Selection**
1. Prefer low-cost index funds
2. Avoid overlapping holdings
3. Consider expense ratios
4. Review fund holdings periodically

### **Drift Management**
1. Small drifts don't need immediate action
2. Rebalance during contributions
3. Use new money to rebalance
4. Set calendar reminders

### **Performance Tracking**
1. Compare to benchmarks regularly
2. Focus on long-term trends
3. Don't panic on short-term drops
4. Review annually, adjust quarterly

---

## 📊 **Calculation Formulas**

### **Drift Calculation**
```
Drift = Current Allocation - Target Allocation
Example: 38.5% - 40.0% = -1.5% (underweight)
```

### **ROI Calculation**
```
ROI = (Current Value - Principal) / Principal × 100%
Example: ($105,000 - $100,000) / $100,000 = 5%
```

### **CAGR (Annualized Return)**
```
CAGR = (End Value / Start Value)^(1/Years) - 1
Example: ($105,000 / $100,000)^(1/1.3) - 1 = 3.7%
```

### **Sharpe Ratio**
```
Sharpe = (Portfolio Return - Risk-Free Rate) / Volatility
Example: (12% - 2%) / 15% = 0.67
```

---

## 🎯 **Decision Matrix**

### **When to Rebalance?**

| Drift | Action | Priority |
|-------|--------|----------|
| < 3% | Monitor | 🟢 Low |
| 3-5% | Plan rebalance | 🟡 Medium |
| 5-10% | Rebalance soon | 🟠 High |
| > 10% | Rebalance now | 🔴 Critical |

### **Asset Allocation by Age**

| Age | Stocks | Bonds | Rule of Thumb |
|-----|--------|-------|---------------|
| 20-30 | 90% | 10% | Aggressive growth |
| 30-40 | 80% | 20% | Growth focused |
| 40-50 | 70% | 30% | Balanced |
| 50-60 | 60% | 40% | Conservative growth |
| 60+ | 40-50% | 50-60% | Capital preservation |

---

## 📅 **Recommended Schedule**

### **Daily**
- Quick drift check (if desired)
- Monitor major market movements

### **Weekly**
- Review portfolio value
- Check for alerts

### **Monthly**
- Detailed drift analysis
- Review performance metrics
- Consider rebalancing

### **Quarterly**
- Compare to benchmarks
- Adjust allocations if needed
- Review investment thesis

### **Annually**
- Comprehensive portfolio review
- Tax loss harvesting
- Rebalance to targets
- Update goals and risk tolerance

---

## 🔗 **Quick Links**

| Resource | Link |
|----------|------|
| **Full User Guide** | [USER_GUIDE.md](USER_GUIDE.md) |
| **Installation** | [INSTALLATION.md](INSTALLATION.md) |
| **Setup Google Sheets** | [SETUP_GOOGLE_SHEETS.md](SETUP_GOOGLE_SHEETS.md) |
| **Troubleshooting** | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| **Changelog** | [CHANGELOG.md](CHANGELOG.md) |
| **GitHub Issues** | [Open Issue](https://github.com/yourusername/alphastream-portfolio/issues) |

---

## 📌 **Bookmarks**

Save these for quick access:

```
🏠 Home: [App URL]
📊 Portfolio Manager: [App URL]/portfolio
👤 Account Settings: [App URL]/account
👑 Admin Panel: [App URL]/admin (admin only)
📖 Documentation: [Repo URL]/docs
```

---

## ✅ **Quick Checklist**

### **Daily/Weekly**
- [ ] Check drift status
- [ ] Monitor alerts
- [ ] Review market conditions

### **Monthly**
- [ ] Analyze performance
- [ ] Compare to benchmarks
- [ ] Rebalance if needed

### **Quarterly**
- [ ] Review asset allocation
- [ ] Update targets
- [ ] Assess risk tolerance

### **Annually**
- [ ] Comprehensive review
- [ ] Tax optimization
- [ ] Goal assessment
- [ ] Strategy adjustment

---

**Need more detail? Check the [Full User Guide](USER_GUIDE.md)!** 📖

**Having issues? See [Troubleshooting](TROUBLESHOOTING.md)!** 🔧
