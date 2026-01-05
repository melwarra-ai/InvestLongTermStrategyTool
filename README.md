# 📊 Long Term Strategy Optimizer v5.0

**Professional portfolio management and rebalancing tool for long-term investors**

![Version](https://img.shields.io/badge/version-5.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

---

## 🎯 Overview

Long Term Strategy Optimizer is a comprehensive portfolio management application designed for long-term investors who want to:
- Track multiple investment portfolios across different currencies
- Monitor asset allocation and detect portfolio drift
- Execute strategic rebalancing based on target allocations
- Compare performance against market benchmarks
- Visualize portfolio growth and goal achievement

Built with **Streamlit** and powered by real-time market data from **Yahoo Finance**.

---

## ✨ Key Features

### 📁 **Multi-Portfolio Management**
- Manage unlimited investment profiles
- Support for USD and CAD portfolios
- Track starting capital, investment goals, and time horizons
- Set custom yearly return goals (CAGR targets)

### 📈 **Real-Time Portfolio Tracking**
- Live market data integration via Yahoo Finance
- Daily portfolio valuation updates
- Historical performance tracking
- Current holdings and asset allocation monitoring

### ⚖️ **Intelligent Drift Detection**
- Automatic monitoring of target vs. actual allocations
- Customizable drift tolerance thresholds (default: 5%)
- Visual indicators when rebalancing is needed
- Per-asset drift analysis and alerts

### 🔄 **Strategic Rebalancing**
- One-click portfolio rebalancing to target allocations
- Complete rebalancing history with timestamps
- Detailed transaction logs showing all adjustments
- 24-hour cooldown period to prevent over-trading

### 📊 **Advanced Analytics & Visualization**
- **Performance vs Goal Path Chart**: Compare actual performance against target growth trajectory
- **Benchmark Comparison**: See how your portfolio stacks up against market indices (SPY, QQQ, etc.)
- **Allocation Analysis**: Visual breakdown of current holdings vs. targets
- **Multi-Year Portfolio Growth**: Track portfolio evolution over time

### 🎯 **Asset Deployment Tracking**
- Track deployment progress for each asset (0-100%)
- Monitor which assets are fully deployed vs. in progress
- Clear status indicators for portfolio completion

### 🔔 **Smart Alerts & Status Indicators**
- Drift alert banners when action is needed
- Rebalancing status badges (Balanced, Rebalance Required, Deploying)
- Recently rebalanced indicators
- Color-coded priority system

### 📦 **Data Persistence**
- Automatic saving of all portfolio data
- JSON-based data storage
- No database setup required
- Easy backup and restore

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (for market data)

### Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd long-term-strategy-optimizer
   ```

2. **Install required packages**
   ```bash
   pip install streamlit yfinance pandas numpy plotly
   ```

3. **Run the application**
   ```bash
   streamlit run longterminvestortool_v5_FINAL.py
   ```

4. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in terminal

---

## 📖 User Guide

### Getting Started

#### 1. Create Your First Profile

<details>
<summary>Click to expand</summary>

1. Open the sidebar (left panel)
2. Find the "Create New Profile" section
3. Enter profile details:
   - **Name**: Give your portfolio a name (e.g., "Retirement 2050")
   - **Currency**: Choose USD or CAD
   - **Starting Capital**: Your initial investment amount
   - **Yearly Goal**: Target annual return percentage (e.g., 8%)
   - **Benchmark**: Select market index for comparison (SPY, QQQ, etc.)
4. Click "Create Profile"

Your new profile will appear in the Global Dashboard!

</details>

#### 2. Add Assets to Your Portfolio

<details>
<summary>Click to expand</summary>

1. Select your profile from the sidebar
2. Go to "Portfolio Manager" section
3. In "Add New Asset" form:
   - **Ticker**: Stock/ETF symbol (e.g., AAPL, VTI, VXUS)
   - **Target Allocation**: Desired percentage of portfolio (must total 100%)
4. Click "Add Asset"

**Example Allocation:**
- VTI (US Total Market): 60%
- VXUS (International): 30%
- BND (Bonds): 10%

</details>

#### 3. Deploy Your Capital

<details>
<summary>Click to expand</summary>

1. For each asset, use the "Deployment" sliders:
   - **Allocated %**: How much of this asset's target you've deployed
   - **Units**: Actual shares/units purchased
2. Slide to 100% when fully deployed
3. App automatically calculates current value

**Tip:** You don't have to deploy everything at once! Deploy gradually and the app will track your progress.

</details>

#### 4. Monitor and Rebalance

<details>
<summary>Click to expand</summary>

**Monitoring:**
- Dashboard shows current allocation vs. targets
- Drift percentage displayed for each asset
- Alert banner appears when drift exceeds tolerance

**When to Rebalance:**
- Drift alert shows: "🚨 REBALANCE REQUIRED"
- One or more assets exceed your drift tolerance (default 5%)
- Portfolio status shows "⚠️ Rebalancing needed"

**How to Rebalance:**
1. Review drift details in Portfolio Manager
2. Click "⚡ Execute Rebalancing" button
3. Confirm the proposed changes
4. App calculates exact units needed for each asset
5. History is automatically saved

**Note:** 24-hour cooldown after rebalancing prevents over-trading.

</details>

---

## 🎨 Dashboard Overview

### Global Dashboard (Home)
- **Portfolio Tiles**: Quick view of all your profiles
- **Status Indicators**: At-a-glance rebalancing status
- **Total Portfolio Value**: Combined worth across all portfolios
- **Rebalance Analysis**: Summary of portfolios needing attention

### Portfolio Manager (Per Profile)
- **Current Holdings**: Real-time asset values and allocations
- **Target vs Actual**: Visual comparison of desired vs. current allocation
- **Drift Analysis**: Detailed drift calculations per asset
- **Deployment Tracking**: Progress indicators for each asset
- **Rebalancing Tools**: One-click execution with detailed previews

### Analytics
- **Performance Chart**: Visual comparison of portfolio vs. goal vs. benchmark
- **Portfolio Growth**: Historical value progression
- **Return Metrics**: CAGR, total return, gain/loss calculations
- **Benchmark Comparison**: How you're performing vs. market indices

---

## 📊 Understanding the Performance Chart

The **Performance vs Goal Path** chart shows three key lines:

### 🔵 Blue Solid Line - Your Actual Portfolio
- Real-time portfolio value based on current market prices
- Shows your actual investment performance
- Reflects all your buying/selling decisions

### 🟢 Green Dashed Line - Goal Path
- Your target growth trajectory
- Based on your yearly goal percentage
- Shows where you *want* to be

### 🟠 Orange Dotted Line - Benchmark
- Market index performance (SPY, QQQ, etc.)
- Assumes 100% invested at profile start date
- Provides "buy and hold" comparison

**How to Interpret:**
- **Above goal?** 🎉 You're beating your target!
- **Above benchmark?** ✨ You're outperforming the market!
- **Below benchmark?** 🤔 Consider if active management adds value

**Important Note:** The benchmark assumes perfect timing (100% invested on day 1), which is unrealistic for most investors who deploy capital gradually.

---

## ⚙️ Configuration Options

### Drift Tolerance
**What it is:** Maximum allowed deviation from target allocation before triggering rebalance alert.

**Default:** 5%

**How to adjust:**
1. Go to Portfolio Manager
2. Look for "Drift Tolerance" setting
3. Adjust slider (typically 3-10%)

**Recommendations:**
- **Conservative (3-5%)**: More frequent rebalancing, stays closer to targets
- **Moderate (5-7%)**: Balanced approach (recommended for most investors)
- **Aggressive (7-10%)**: Less frequent rebalancing, allows more drift

### Deployment Tracking
**Enable/Disable:** Track partial deployment of assets

**Use case:** 
- Building position over time (dollar-cost averaging)
- Gradual capital deployment
- Monitoring which assets need more investment

### Benchmark Selection
**Available benchmarks:**
- **SPY**: S&P 500 (Large-cap US stocks)
- **QQQ**: NASDAQ 100 (Tech-heavy US stocks)
- **DIA**: Dow Jones Industrial Average
- **IWM**: Russell 2000 (Small-cap US stocks)
- **VTI**: Total US Stock Market
- **VXUS**: Total International Stock Market
- **AGG**: US Aggregate Bonds
- **GLD**: Gold
- **Custom**: Enter any valid ticker

---

## 💾 Data Storage

### Storage Location
All portfolio data is saved in:
```
portfolio_database.json
```

### Data Structure
```json
{
  "My Retirement": {
    "currency": "USD",
    "starting_capital": 10000,
    "start_date": "2025-01-01",
    "yearly_goal_pct": 8.0,
    "benchmark": "SPY",
    "drift_tolerance": 5.0,
    "last_rebalanced": "2025-01-05T10:30:00",
    "assets": {
      "VTI": {
        "target": 60.0,
        "units": 25.5,
        "allocated_pct": 100.0
      }
    },
    "rebalancing_history": [...]
  }
}
```

### Backup & Restore
**To backup:**
```bash
cp portfolio_database.json portfolio_backup_$(date +%Y%m%d).json
```

**To restore:**
```bash
cp portfolio_backup_20250105.json portfolio_database.json
```

---

## 🔧 Advanced Features

### Rebalancing History
- Access complete rebalancing log
- See exact changes made at each rebalance
- Track when and why rebalances occurred
- Export history for tax purposes

### Multi-Currency Support
- Separate USD and CAD portfolios
- Currency-specific flag indicators (🇺🇸 🇨🇦)
- No automatic conversion (keep portfolios separate)

### Custom Asset Support
- Add any ticker supported by Yahoo Finance
- Stocks, ETFs, mutual funds, cryptocurrencies
- International tickers (add exchange suffix, e.g., AAPL.L for London)

---

## 🐛 Troubleshooting

### Common Issues

<details>
<summary><strong>Issue: "No data found for ticker XXX"</strong></summary>

**Cause:** Invalid ticker symbol or Yahoo Finance can't find the asset.

**Solution:**
1. Verify ticker symbol is correct
2. Check if asset is publicly traded
3. For international stocks, add exchange suffix (e.g., .TO for Toronto, .L for London)
4. Try searching the ticker on finance.yahoo.com first

</details>

<details>
<summary><strong>Issue: Benchmark line not visible on chart</strong></summary>

**Cause:** Old version of the app or browser cache.

**Solution:**
1. Ensure you're running `longterminvestortool_v5_FINAL.py`
2. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
3. Restart Streamlit app
4. Check that a benchmark is selected in profile settings

</details>

<details>
<summary><strong>Issue: Portfolio value shows $0</strong></summary>

**Cause:** No units deployed or market data not loading.

**Solution:**
1. Check you've entered units for your assets
2. Verify tickers are correct
3. Check internet connection (app needs access to Yahoo Finance)
4. Try refreshing the app (F5)

</details>

<details>
<summary><strong>Issue: Rebalance button disabled</strong></summary>

**Cause:** Either no drift detected or recently rebalanced (24h cooldown).

**Solution:**
1. Check if any assets show drift > tolerance
2. If recently rebalanced, wait 24 hours
3. Review "Current Status" section for details
4. Verify assets are fully deployed (100%)

</details>

<details>
<summary><strong>Issue: "Module not found" error</strong></summary>

**Cause:** Required Python packages not installed.

**Solution:**
```bash
pip install streamlit yfinance pandas numpy plotly
```

If issues persist:
```bash
pip install --upgrade streamlit yfinance pandas numpy plotly
```

</details>

---

## 🎯 Best Practices

### Portfolio Management

1. **Set Realistic Goals**
   - Historical S&P 500 returns: ~10% annually
   - Conservative: 6-8%
   - Moderate: 8-10%
   - Aggressive: 10-12%+

2. **Rebalance Wisely**
   - Don't rebalance too frequently (increases transaction costs)
   - Annual or semi-annual rebalancing is typical
   - Let drift tolerance guide you (5-7% is common)

3. **Consider Tax Implications**
   - Rebalancing triggers taxable events
   - Consider using tax-advantaged accounts for frequent rebalancing
   - Track cost basis for tax reporting

4. **Diversification**
   - Don't concentrate too heavily in any single asset
   - Consider different asset classes (stocks, bonds, international)
   - Risk tolerance should guide your allocation

5. **Dollar-Cost Averaging**
   - Use deployment tracking to gradually build positions
   - Reduces timing risk
   - Good for volatile markets

### Using Benchmarks

1. **Choose Relevant Benchmark**
   - Stock-heavy portfolio? Use SPY or VTI
   - Tech-focused? Use QQQ
   - Match your portfolio's strategy

2. **Understand Limitations**
   - Benchmark assumes 100% invested immediately
   - You might deploy gradually (and that's okay!)
   - Short-term underperformance is normal

3. **Long-Term Focus**
   - Don't obsess over daily/weekly comparisons
   - Look at 1-year, 3-year, 5-year trends
   - Market timing is nearly impossible

---

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB
- **Disk Space**: 100MB
- **Internet**: Required for market data

### Recommended
- **Python**: 3.10+
- **RAM**: 8GB
- **Browser**: Chrome, Firefox, or Edge (latest version)
- **Internet**: Stable broadband connection

### Dependencies
```
streamlit>=1.28.0
yfinance>=0.2.28
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
```

---

## 📁 File Structure

```
long-term-strategy-optimizer/
├── longterminvestortool_v5_FINAL.py    # Main application file
├── portfolio_database.json              # Data storage (auto-generated)
├── README.md                            # This file
├── requirements.txt                     # Python dependencies (optional)
├── docs/                                # Documentation (optional)
│   ├── CHART_FIXES_v5.md
│   ├── VERSION_5_RELEASE_NOTES.md
│   └── V5_QUICK_REFERENCE.md
└── backups/                             # Backup location (optional)
    └── portfolio_backup_YYYYMMDD.json
```

---

## 🆚 Version History

### v5.0 (Current - January 2026)
**Major Updates:**
- ✅ Rebranded to "Long Term Strategy Optimizer"
- ✅ Enhanced benchmark visibility (now clearly visible on charts)
- ✅ Improved chart layout (no overlapping elements)
- ✅ Better legend positioning
- ✅ Cleaner, more professional appearance
- ✅ Removed redundant chart title
- ✅ Brighter benchmark line (orange dotted, 4px)

### v4.0 (AlphaStream Wealth Master)
- Multi-portfolio management
- Drift detection and alerts
- Rebalancing execution
- Performance tracking
- Benchmark comparison (with visibility issues - fixed in v5.0)

### Earlier Versions
- v1.0-3.0: Initial development and feature additions

---

## 🤝 Contributing

This is a personal portfolio management tool. If you'd like to suggest improvements:

1. Document the feature request or bug
2. Provide examples or screenshots
3. Explain the use case

---

## ⚠️ Disclaimer

**IMPORTANT: This software is for informational and educational purposes only.**

- **NOT FINANCIAL ADVICE**: This tool does not provide financial, investment, or tax advice.
- **NO WARRANTY**: The software is provided "as is" without warranty of any kind.
- **USER RESPONSIBILITY**: All investment decisions are solely your responsibility.
- **MARKET RISK**: Investments carry risk including possible loss of principal.
- **DATA ACCURACY**: While we use reliable data sources (Yahoo Finance), accuracy is not guaranteed.
- **TAX IMPLICATIONS**: Consult a tax professional regarding tax consequences of rebalancing.

**By using this software, you acknowledge:**
1. You are responsible for your own investment decisions
2. You understand the risks involved in investing
3. You will verify all data and calculations independently
4. You will consult with qualified professionals before making financial decisions

---

## 📞 Support

### Getting Help

**For technical issues:**
1. Check the Troubleshooting section above
2. Verify you're running v5.0 (check footer)
3. Review documentation files in `/docs` folder

**For usage questions:**
1. Review this README thoroughly
2. Check the User Guide section
3. Review Best Practices section

**Data Issues:**
1. Verify internet connection
2. Confirm tickers are valid on finance.yahoo.com
3. Check `portfolio_database.json` for corruption

---

## 📄 License

MIT License - Free to use, modify, and distribute with attribution.

```
Copyright (c) 2026 Long Term Strategy Optimizer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web app framework
- **Yahoo Finance (yfinance)**: For real-time market data
- **Plotly**: For interactive charting capabilities
- **The Python Community**: For excellent libraries and support

---

## 🚀 Quick Links

- **Run Application**: `streamlit run longterminvestortool_v5_FINAL.py`
- **Version**: 5.0
- **Release Date**: January 2026
- **Status**: Production Ready ✅

---

<div align="center">

**📊 Long Term Strategy Optimizer v5.0**

*Professional Portfolio Management for Long-Term Investors*

Made with ❤️ for smart investors

**[⬆ Back to Top](#-long-term-strategy-optimizer-v50)**

</div>
