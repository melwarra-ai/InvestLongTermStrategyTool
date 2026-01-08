# 📚 Version 5.5 Quick Reference Guide

**Version:** 5.5  
**Status:** ✅ STABLE  
**Release Date:** January 8, 2026  
**Codename:** Stable Benchmark Release

---

## 🚀 Quick Start

### Installation
```bash
pip install streamlit yfinance pandas numpy plotly --break-system-packages
streamlit run longterminvestor_v5.5_STABLE.py
```

### First Steps
1. **Create Profile** → Sidebar → "🆕 Create New Profile"
2. **Add Assets** → Define tickers and target % (must total 100%)
3. **Lock Mix** → Click "🔒 Lock Asset Mix" when complete
4. **Deploy Capital** → Record purchases for each asset
5. **Monitor** → Track drift and rebalance when needed

---

## 📂 File Structure

### Main Application
- **`longterminvestor_v5.5_STABLE.py`** - Main application file (USE THIS!)

### Documentation
- **`RELEASE_NOTES_v5.5.md`** - Complete release notes
- **`CHANGELOG.md`** - Version history (updated with v5.5)
- **`README.md`** - Complete user manual
- **`QUICKSTART.md`** - 5-minute setup guide

### Data
- **`alphastream_wealth.json`** - Your portfolio data (auto-created)

---

## 🎯 Key Features

### Portfolio Management
✅ Multiple portfolio profiles  
✅ USD & CAD currency support  
✅ Asset allocation with target %  
✅ Drift detection with alerts  
✅ Automated rebalancing  

### Performance Tracking
✅ Real-time portfolio valuation  
✅ CAGR & ROI calculations  
✅ Goal path comparison  
✅ **Benchmark comparison** (SPY, QQQ, VTI, IWM, DIA)  
✅ Interactive charts  

### Deployment Workflow
✅ Asset mix locking  
✅ Gradual capital deployment  
✅ Historical price fetching  
✅ Average cost basis calculation  
✅ Deployment history tracking  

### History & Logging
✅ Rebalance history with filtering  
✅ Activity log  
✅ Event timestamps  
✅ Trade details  

---

## 🔧 Configuration Options

### Drift Tolerance
- **Default:** 5.0%
- **Range:** 0.5% - 20.0%
- **Location:** Sidebar → "⚙️ Drift Strategy"
- **Effect:** Controls when rebalance alerts trigger

### Benchmark Selection
- **Default:** None
- **Options:** SPY, QQQ, VTI, IWM, DIA
- **Location:** Sidebar → "📊 Benchmark Comparison"
- **Effect:** Shows market comparison on chart

### Currency
- **Options:** USD, CAD
- **Set:** During profile creation
- **Effect:** Determines currency symbol (🇺🇸 or 🇨🇦)

---

## 📊 Understanding the Dashboard

### Global Dashboard (🏠)
Shows all profiles at a glance:
- Total portfolio value across all profiles
- Number of active strategies
- Drift alerts count
- Individual profile cards with status

### Portfolio Manager (📊)
Detailed view of selected profile:
- Portfolio analytics and metrics
- Performance vs Goal Path chart
- Benchmark comparison
- Rebalance analysis table
- Execution controls

---

## 🎨 Status Indicators

### Profile Status Badges
- **⚪ New** - Profile created, no assets yet
- **🔥 Deploying (X/Y)** - Assets being deployed
- **✅ Deployed** - All assets 100% deployed
- **✅ Balanced** - Recently rebalanced, within tolerance
- **🚨 REBALANCE REQUIRED** - Drift exceeds tolerance

### Drift Colors
- **🟢 Green** - Within tolerance
- **🟡 Yellow** - Approaching tolerance
- **🔴 Red** - Exceeds tolerance (action needed)

---

## 🔄 Typical Workflow

### 1. Initial Setup (One Time)
```
Create Profile → Add Assets → Lock Mix → Deploy Capital
```

### 2. Ongoing Management (Regular)
```
Check Dashboard → Review Drift → Rebalance if Needed → Log Activity
```

### 3. Performance Review (Periodic)
```
View Charts → Compare to Benchmark → Analyze CAGR → Adjust Strategy
```

---

## ⚡ Keyboard Shortcuts

### Navigation
- **Click profile name** → Switch to that profile
- **Sidebar radio** → Switch between Dashboard and Manager
- **Expander arrows** → Show/hide sections

### Chart Interaction
- **Hover** → See exact values
- **Click legend item** → Hide/show that line
- **Double-click chart** → Reset zoom
- **Toolbar** → Zoom, pan, save image

---

## 🐛 Common Issues & Solutions

### Issue: "Could not fetch price data"
**Solution:** 
- Check internet connection
- Verify ticker exists on Yahoo Finance
- Try again in a few minutes

### Issue: "Portfolio value is zero"
**Solution:**
- Deploy capital first (💰 Asset Deployment)
- Check units are recorded correctly
- Verify prices are loading

### Issue: "Rebalancing disabled"
**Solution:**
- Ensure all assets 100% deployed
- Check drift exceeds tolerance
- Wait 24 hours after last rebalance

### Issue: "Can't add new assets"
**Solution:**
- Unlock asset mix first (🔓 Unlock Asset Mix)
- Note: Can only unlock if no deployments recorded

### Issue: "Benchmark not showing"
**Solution:**
- Select benchmark in sidebar
- Check internet connection
- Verify chart is fully loaded
- Try clicking legend items to show/hide

---

## 💡 Pro Tips

### Allocation Strategy
- **Diversify** across asset classes
- **Target 100%** before locking
- **Plan ahead** - can't add assets after locking

### Deployment Strategy
- **Deploy gradually** to dollar-cost average
- **Record dates** for accurate historical tracking
- **Track avg cost** becomes available at 100%

### Rebalancing Strategy
- **Set tolerance** based on your rebalance frequency
- **Lower tolerance** = more frequent, tighter control
- **Higher tolerance** = less frequent, more flexibility

### Performance Tracking
- **Enable benchmark** to compare vs market
- **Check CAGR** for long-term performance
- **Review drift** regularly to stay disciplined

---

## 📞 Getting Help

### In-App Help
- Look for **ℹ️ icons** throughout the app
- Click to expand detailed explanations
- Most sections have contextual help

### Documentation
- **README.md** - Complete manual
- **RELEASE_NOTES_v5.5.md** - What's new
- **CHANGELOG.md** - Version history

### Activity Log
- Review **📜 Activity Log** in sidebar
- See all changes made to portfolio
- Timestamp and event details

---

## 🔐 Data Security

### Local Storage
- All data stored in `alphastream_wealth.json`
- Located in same directory as app
- **No cloud sync** - your data stays local

### Backup Recommendations
- **Before major changes** - Copy JSON file
- **Regular backups** - Weekly or monthly
- **Version control** - Consider git if familiar

### Privacy
- **No external tracking**
- **No data collection**
- **No account registration**
- **100% local operation**

---

## 📈 Performance Metrics

### CAGR (Compound Annual Growth Rate)
- Annualized return accounting for compounding
- Shows true long-term performance
- More accurate than simple ROI for multi-year periods

### ROI (Return on Investment)
- Total % gain/loss from start
- Simple calculation: (Current - Start) / Start
- Good for quick overview

### vs Target Path
- Shows if you're ahead/behind goal
- Positive = beating your target
- Negative = below target

### Annualized Return
- What your return would be per year
- Useful for comparing different time periods
- Similar to CAGR but different calculation method

---

## 🎯 Best Practices

### 1. Set Realistic Goals
- Research historical market returns
- 10% is common for stock-heavy portfolios
- Adjust based on risk tolerance

### 2. Maintain Discipline
- Don't chase performance
- Stick to your allocation plan
- Rebalance when drift alerts trigger

### 3. Track History
- Review rebalance history monthly
- Check deployment accuracy
- Learn from past decisions

### 4. Use Benchmarks
- Compare to relevant market index
- SPY for broad market
- QQQ for tech-heavy
- Adjust strategy if consistently underperforming

### 5. Regular Reviews
- Weekly: Check drift alerts
- Monthly: Review performance
- Quarterly: Assess strategy
- Yearly: Major review and adjustments

---

## 🔄 Version Information

### Current Version
**v5.5** - Stable Benchmark Release

### Version History
- **v5.5** (2026-01-08) - Stable baseline ← **YOU ARE HERE**
- **v5.0** (2026-01-05) - Rebranding and enhancements
- **v4.x** - Core feature development
- **v3.x** - Initial deployment workflow
- **v2.x** - Drift detection
- **v1.x** - Basic portfolio management

### What's Next?
- **v5.6** - Planned enhancements (CSV export, email alerts)
- **v6.0** - Major release (real-time features, cloud sync)

---

## ✅ Stability Checklist

Before using for real portfolio management:

- [ ] Create test profile with small amounts
- [ ] Add 2-3 test assets
- [ ] Lock asset mix
- [ ] Record test deployment
- [ ] Check drift detection
- [ ] Test rebalancing
- [ ] Review all charts
- [ ] Check history logs
- [ ] Backup JSON file
- [ ] Read full documentation

**Once comfortable, start with your real portfolio!**

---

## 📄 License & Disclaimer

**License:** Personal use

**Disclaimer:** This tool is for informational purposes only. It does not provide investment advice. The calculations and suggestions are based on your inputs and market data, but should not be considered professional financial guidance. Always consult with a qualified financial advisor before making investment decisions.

---

## 🎉 You're All Set!

**Version 5.5 is production-ready and waiting for you!**

**File to run:** `longterminvestor_v5.5_STABLE.py`

**Command:**
```bash
streamlit run longterminvestor_v5.5_STABLE.py
```

**Have questions?** Check the ℹ️ help icons throughout the app!

---

**Last Updated:** January 8, 2026  
**Version:** 5.5 STABLE  
**Status:** ✅ Ready for Production Use
