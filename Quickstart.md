# ⚡ Quick Start Guide - Long Term Strategy Optimizer v5.0

Get up and running in **5 minutes**!

---

## 📦 Installation (2 minutes)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install streamlit yfinance pandas numpy plotly
```

### Step 2: Run the App
```bash
streamlit run longterminvestortool_v5_FINAL.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 🎯 First-Time Setup (3 minutes)

### 1. Create Your Profile
In the sidebar (left panel):
- Click **"Profile Name"** field
- Enter a name (e.g., "My Retirement")
- Select **Currency** (USD or CAD)
- Enter **Starting Capital** (e.g., 10000)
- Set **Yearly Goal** (e.g., 8%)
- Choose **Benchmark** (e.g., SPY)
- Click **"Create Profile"**

### 2. Add Assets
In the "Add New Asset" section:
- **Ticker**: Enter stock symbol (e.g., VTI)
- **Target %**: Enter allocation (e.g., 60)
- Click **"Add Asset"**

Repeat for all assets (must total 100%).

**Example Portfolio:**
```
VTI  (US Total Market)     60%
VXUS (International)       30%
BND  (Bonds)              10%
                         ----
                         100%
```

### 3. Deploy Capital
For each asset:
- Move **"Allocated %"** slider to 100%
- Enter **"Units"** (shares owned)
- App calculates current value automatically

### 4. Monitor & Rebalance
- Dashboard shows drift automatically
- Click **"Execute Rebalancing"** when needed
- Review history anytime

---

## 🎨 What You'll See

### Home Dashboard
- All your portfolios at a glance
- Status indicators (Green = Balanced, Red = Needs rebalancing)
- Total portfolio values

### Portfolio Manager
- Current asset values and allocations
- Target vs. Actual comparison
- Drift warnings (when > 5%)
- One-click rebalancing

### Performance Chart
- 🔵 Blue line = Your portfolio
- 🟢 Green dashed = Your goal
- 🟠 Orange dotted = Market benchmark

---

## 💡 Pro Tips

1. **Start Simple**: 3-5 assets is plenty
2. **Set Realistic Goals**: 7-10% annual return is reasonable
3. **Don't Over-Rebalance**: 1-2 times per year is typical
4. **Use Benchmarks**: SPY (S&P 500) is most common
5. **Backup Data**: Copy `portfolio_database.json` regularly

---

## ⚠️ Common First-Time Issues

### "No data found for ticker"
→ Verify ticker on finance.yahoo.com first

### Benchmark not visible
→ Make sure you selected a benchmark in profile settings

### Portfolio shows $0
→ Enter units (shares) for your assets

### Can't rebalance
→ Need drift > 5% or wait 24 hours after last rebalance

---

## 📚 Need More Help?

- **Full Guide**: See README.md
- **Troubleshooting**: Check README.md → Troubleshooting section
- **Best Practices**: See README.md → Best Practices section

---

## 🚀 You're Ready!

That's it! You now have a professional portfolio management system running.

**What to do now:**
1. ✅ Create your first profile
2. ✅ Add your assets
3. ✅ Enter your holdings
4. ✅ Monitor and rebalance as needed

**Happy investing!** 📈

---

## 🎯 Example Session

```bash
# 1. Install
pip install streamlit yfinance pandas numpy plotly

# 2. Run
streamlit run longterminvestortool_v5_FINAL.py

# 3. Create profile in browser
Name: Retirement 2050
Capital: $10,000
Goal: 8%
Benchmark: SPY

# 4. Add assets
VTI: 60%
VXUS: 30%
BND: 10%

# 5. Deploy
Enter your actual units/shares

# 6. Monitor
Check dashboard daily
Rebalance when drift > 5%
```

**Time to first rebalance: ~5 minutes!** ⚡
