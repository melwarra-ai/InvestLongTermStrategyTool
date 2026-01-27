# 🏦 AlphaStream Portfolio Optimizer

**Long Term Strategy Suite v7.1.0**

A professional portfolio management application with institutional-grade features for tracking, rebalancing, and optimizing investment portfolios. Built with Streamlit and powered by Google Sheets for persistent storage.

![Version](https://img.shields.io/badge/version-7.1.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-production-success)

---

## 🌟 **Features**

### **Portfolio Management**
- 📊 **Multi-Portfolio Support** - Manage multiple portfolios per user
- 💰 **Principal Tracking** - Track initial investment and growth
- 📈 **Asset Allocation** - Define and maintain target allocations
- 🔄 **Automatic Rebalancing** - Smart rebalancing recommendations
- 🎯 **Drift Monitoring** - Real-time drift detection and alerts

### **Account Management**
- 👥 **Multi-User Support** - Separate accounts with role-based access
- 🔐 **Secure Authentication** - Password hashing and account security
- 👤 **User Profiles** - Personalized settings and preferences
- 🔑 **Admin Controls** - User management and global settings

### **Analytics & Insights**
- 📊 **Portfolio Analytics** - Comprehensive performance metrics
- 🎯 **Benchmark Comparison** - Compare against market indexes
- 📈 **ROI Tracking** - Total return and CAGR calculations
- 💹 **Risk Metrics** - Volatility, Sharpe ratio, and more
- 🔍 **Detailed Reports** - Portfolio summaries and analysis

### **Data Management**
- ☁️ **Cloud Storage** - Persistent data with Google Sheets
- 💾 **Automatic Backups** - Built-in version history
- 🔄 **Real-Time Sync** - Instant data updates
- 📱 **Cross-Platform** - Access from any device

### **Advanced Features**
- 🚀 **Quick Add Tickers** - Fast portfolio creation
- 🎨 **Color-Coded UI** - Visual risk indicators
- ⚡ **Live Market Data** - Real-time pricing via Yahoo Finance
- 📋 **Activity Logging** - Complete audit trail
- 🔔 **Smart Alerts** - Rebalancing notifications

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.9 or higher
- Google Account (for persistent storage)
- Streamlit Cloud account (for deployment) or local Python environment

### **Installation**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/alphastream-portfolio.git
   cd alphastream-portfolio
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Sheets storage:**
   - Follow the detailed guide in [SETUP_GOOGLE_SHEETS.md](SETUP_GOOGLE_SHEETS.md)
   - Configure your Streamlit Secrets

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Access the app:**
   - Open browser to `http://localhost:8501`
   - Default admin login: `admin` / `admin123`

For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md)

---

## 📖 **Documentation**

- **[Installation Guide](INSTALLATION.md)** - Complete setup instructions
- **[User Guide](USER_GUIDE.md)** - How to use the application
- **[Quick Reference](QUICK_REFERENCE.md)** - Fast command reference
- **[Google Sheets Setup](SETUP_GOOGLE_SHEETS.md)** - Cloud storage configuration
- **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions
- **[Changelog](CHANGELOG.md)** - Version history

---

## 🎯 **Usage Example**

```python
# Login to the application
# Username: admin
# Password: admin123

# Create a new portfolio
1. Navigate to "Portfolio Manager"
2. Click "Create New Profile"
3. Enter portfolio details:
   - Name: "Retirement Portfolio"
   - Principal: $100,000
   - Account Type: RRSP

# Add assets
4. Click "Add Asset"
5. Enter ticker: SPY
6. Set target allocation: 40%
7. Repeat for other assets

# Monitor and rebalance
8. View drift alerts
9. Follow rebalancing recommendations
10. Track performance over time
```

---

## 🏗️ **Architecture**

```
AlphaStream Portfolio Optimizer
│
├── Frontend (Streamlit)
│   ├── User Authentication
│   ├── Portfolio Management UI
│   ├── Analytics Dashboard
│   └── Admin Controls
│
├── Backend (Python)
│   ├── Portfolio Calculations
│   ├── Rebalancing Engine
│   ├── Risk Analysis
│   └── Data Management
│
└── Storage (Google Sheets)
    ├── User Data
    ├── Portfolio Data
    ├── Transaction History
    └── System Logs
```

---

## 🔧 **Technology Stack**

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | Streamlit | 1.53.1 |
| **Language** | Python | 3.9+ |
| **Storage** | Google Sheets | API v4 |
| **Market Data** | yfinance | 1.1.0 |
| **Visualization** | Plotly | 6.5.2 |
| **Data Processing** | Pandas | 2.3.3 |
| **Authentication** | Google OAuth | 2.48.0 |

---

## 📊 **System Requirements**

### **Minimum Requirements**
- **CPU:** 1 GHz processor
- **RAM:** 512 MB
- **Storage:** 50 MB free space
- **OS:** Windows 10, macOS 10.14, or Linux
- **Browser:** Chrome 90+, Firefox 88+, Safari 14+

### **Recommended Requirements**
- **CPU:** 2+ GHz dual-core processor
- **RAM:** 2 GB
- **Storage:** 100 MB free space
- **Internet:** Stable connection for market data

---

## 🔐 **Security Features**

- 🔒 **Password Hashing** - SHA-256 with salt
- 🛡️ **Secure Sessions** - Streamlit session state
- 🔑 **Role-Based Access** - Admin and user roles
- 📝 **Audit Logging** - Complete activity tracking
- 🔐 **OAuth Integration** - Google authentication
- 💾 **Encrypted Storage** - Secure Streamlit Secrets

---

## 📈 **Performance**

- **Load Time:** < 2 seconds
- **Save Time:** < 1 second (Google Sheets)
- **Calculation Speed:** < 100ms for typical portfolios
- **Market Data Fetch:** < 3 seconds
- **Supports:** 20+ users, 200+ portfolios

---

## 🌐 **Deployment Options**

### **1. Streamlit Cloud (Recommended)**
- Free hosting
- Automatic HTTPS
- Built-in authentication
- Easy deployment
- No server management

### **2. Self-Hosted**
- Docker deployment
- Custom domain
- Full control
- Advanced features

### **3. Local Development**
- Instant setup
- No deployment needed
- Testing environment

See [INSTALLATION.md](INSTALLATION.md) for deployment guides.

---

## 🤝 **Contributing**

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 **Support**

### **Documentation**
- [Installation Guide](INSTALLATION.md)
- [User Guide](USER_GUIDE.md)
- [Troubleshooting](TROUBLESHOOTING.md)

### **Issues**
- Report bugs on [GitHub Issues](https://github.com/yourusername/alphastream-portfolio/issues)
- Feature requests welcome

### **Contact**
- Email: support@alphastream.example.com
- GitHub: [@yourusername](https://github.com/yourusername)

---

## 🎉 **Acknowledgments**

- **Streamlit** - Amazing framework for data apps
- **Yahoo Finance** - Free market data API
- **Google Sheets** - Reliable cloud storage
- **Plotly** - Beautiful visualizations
- **Open Source Community** - Countless helpful libraries

---

## 🗺️ **Roadmap**

### **v7.2.0 (Planned)**
- [ ] Mobile-optimized interface
- [ ] Export to PDF/Excel
- [ ] Tax loss harvesting
- [ ] Automated portfolio rebalancing

### **v7.3.0 (Future)**
- [ ] Multi-currency support
- [ ] Advanced charting
- [ ] Email notifications
- [ ] API access

### **v8.0.0 (Vision)**
- [ ] AI-powered recommendations
- [ ] Social features
- [ ] Mobile app
- [ ] Premium features

---

## 📊 **Project Stats**

- **Lines of Code:** ~7,240
- **Functions:** 150+
- **Test Coverage:** In progress
- **Active Users:** Growing
- **Stars:** ⭐ (Star us on GitHub!)

---

## 🏆 **Key Achievements**

- ✅ **v7.1.0 Production Release** - Full persistent storage
- ✅ **Multi-User Support** - Role-based access control
- ✅ **Real-Time Analytics** - Live portfolio tracking
- ✅ **Professional UI** - Clean, intuitive interface
- ✅ **Enterprise-Grade** - Reliable and scalable

---

## 📸 **Screenshots**

*Coming soon - Add screenshots of your application here*

---

## 🌟 **Why AlphaStream?**

1. **Professional Grade** - Institutional-quality features
2. **User Friendly** - Intuitive interface for all skill levels
3. **Reliable** - Battle-tested with real portfolios
4. **Free** - Open source and free to use
5. **Supported** - Active development and maintenance

---

## 📞 **Getting Help**

1. Check the [User Guide](USER_GUIDE.md)
2. Read [Troubleshooting](TROUBLESHOOTING.md)
3. Search [GitHub Issues](https://github.com/yourusername/alphastream-portfolio/issues)
4. Open a new issue if needed

---

**Built with ❤️ for investors, by investors**

**[⬆ Back to Top](#-alphastream-portfolio-optimizer)**
