# 🚀 AlphaStream Wealth Master

**Professional Portfolio Management & Investment Strategy Tool**

AlphaStream is a comprehensive, multi-user portfolio management application built with Streamlit and PostgreSQL. It enables sophisticated portfolio tracking, asset allocation, deployment monitoring, and performance analytics for individual investors and family offices.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791.svg)](https://www.postgresql.org/)

---

## ✨ Features

### 💼 **Portfolio Management**
- Multi-user support with secure authentication
- Unlimited portfolio/profile creation per user
- Support for multiple account types (TFSA, RRSP, Non-Registered, etc.)
- Bank/broker tracking (TD, RBC, Questrade, etc.)

### 📊 **Asset Allocation**
- Interactive asset allocation with real-time validation
- Drift detection and rebalancing alerts
- Target vs. actual allocation tracking
- Asset mix locking to prevent accidental changes

### 💰 **Deployment Tracking**
- Dollar-cost averaging (DCA) deployment
- Real-time price fetching via Yahoo Finance
- Purchase history with cost basis tracking
- Deployment progress monitoring

### 📈 **Analytics & Reporting**
- Portfolio performance metrics
- Benchmark comparison (SPY, QQQ, XIU, XIC, etc.)
- Interactive charts with Plotly
- Drift analysis and rebalancing recommendations

### 🔒 **Security**
- Password hashing with SHA-256 + salt
- Session-based authentication
- Role-based access control (User/Admin)
- Account lockout after failed login attempts

### 🛠️ **Admin Dashboard**
- System health monitoring
- User management
- Database statistics
- Activity logs

---

## 🚀 Quick Start

### **Prerequisites**

- Python 3.9 or higher
- PostgreSQL database (we recommend [Neon](https://neon.tech) for serverless hosting)
- Git

### **1. Clone Repository**

```bash
git clone https://github.com/yourusername/alphastream-portfolio-manager.git
cd alphastream-portfolio-manager
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Configure Database**

Create `.streamlit/secrets.toml`:

```toml
[postgres]
host = "your-postgres-host.com"
dbname = "your-database-name"
user = "your-username"
password = "your-password"
port = "5432"
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed setup instructions.

### **4. Run Application**

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501`

---

## 📦 Tech Stack

- **Frontend:** Streamlit 1.28+
- **Backend:** Python 3.9+
- **Database:** PostgreSQL 14+
- **Data:** Yahoo Finance (yfinance)
- **Visualization:** Plotly
- **Deployment:** Streamlit Cloud

---

## 🗄️ Database Schema

AlphaStream uses a document-store pattern with PostgreSQL:

```sql
CREATE TABLE database_store (
    id SERIAL PRIMARY KEY,
    data_json TEXT NOT NULL,
    version INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

All application data (users, portfolios, assets) is stored as JSON in a single row, providing flexibility while maintaining ACID compliance.

---

## 📖 Documentation

- **[Deployment Guide](DEPLOYMENT.md)** - Complete deployment instructions
- **[SQL Query Reference](SQL_QUERIES.md)** - Database queries for monitoring
- **[Architecture Overview](ARCHITECTURE.md)** - System design and data flow
- **[User Guide](docs/USER_GUIDE.md)** - How to use the application
- **[Admin Guide](docs/ADMIN_GUIDE.md)** - Administrative functions
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

---

## 🎯 Use Cases

### **Individual Investors**
- Track personal investment portfolios
- Monitor asset allocation drift
- Plan systematic deployments (DCA)
- Compare performance vs. benchmarks

### **Family Offices**
- Manage multiple family member portfolios
- Consolidated reporting across accounts
- Track different account types (TFSA, RRSP, etc.)
- Multi-user access with role controls

### **Financial Advisors**
- Client portfolio management
- Rebalancing recommendations
- Performance reporting
- Asset allocation modeling

---

## 🔐 Security Features

- ✅ Password hashing with SHA-256 + random salt
- ✅ Session-based authentication
- ✅ Brute-force protection (account lockout)
- ✅ Role-based access control
- ✅ Secure credential storage (PostgreSQL)
- ✅ No sensitive data in client-side storage

---

## 🌐 Deployment

### **Streamlit Cloud (Recommended)**

1. Push code to GitHub
2. Connect repository to [Streamlit Cloud](https://share.streamlit.io)
3. Configure secrets in Streamlit Cloud dashboard
4. Deploy!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### **Other Platforms**

AlphaStream can also be deployed on:
- Heroku
- AWS EC2
- Google Cloud Platform
- Azure App Service
- Docker containers

---

## 📊 Version History

**Current Version:** v9.0.1 (PostgreSQL Migration - Stable)

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

### Recent Updates

- **v9.0.1** (2026-02-08) - PostgreSQL migration bugfix
- **v9.0.0** (2026-02-08) - PostgreSQL backend migration
- **v8.1.0** (2026-02-08) - Force 100% default deploy percentage
- **v8.0.7** (2026-02-08) - Complete asset allocation UI hiding
- **v8.0.0** (2026-02-07) - SQLite backend implementation

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Market data from [Yahoo Finance](https://finance.yahoo.com)
- Database hosting on [Neon](https://neon.tech)
- Inspiration from modern portfolio theory

---

## 📧 Support

For questions or issues:
- Open a GitHub Issue
- Email: your-email@example.com
- Documentation: [docs/](docs/)

---

## 🎓 Learn More

- [Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory)
- [Dollar-Cost Averaging](https://www.investopedia.com/terms/d/dollarcostaveraging.asp)
- [Asset Allocation](https://www.investopedia.com/terms/a/assetallocation.asp)
- [Portfolio Rebalancing](https://www.investopedia.com/terms/r/rebalancing.asp)

---

**Built with ❤️ for smarter investing**

[![Star on GitHub](https://img.shields.io/github/stars/yourusername/alphastream-portfolio-manager?style=social)](https://github.com/yourusername/alphastream-portfolio-manager)
