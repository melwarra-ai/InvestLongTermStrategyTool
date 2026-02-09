# 🏗️ AlphaStream Architecture

System design and technical architecture for AlphaStream Portfolio Manager v9.0.1

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     USER INTERFACE                      │
│                   (Streamlit Frontend)                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🏠 Login/Register     💼 Portfolio Manager            │
│  👤 User Dashboard     📊 Analytics                    │
│  🔧 Admin Panel        ⚙️  Settings                     │
│                                                         │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ HTTP/HTTPS
                 │
┌────────────────▼────────────────────────────────────────┐
│              APPLICATION LAYER                          │
│              (Python + Streamlit)                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  • Authentication (SHA-256 + Salt)                     │
│  • Session Management                                   │
│  • Business Logic                                       │
│  • Data Validation                                      │
│  • Yahoo Finance Integration                            │
│  • Chart Generation (Plotly)                            │
│                                                         │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ psycopg2
                 │ Connection Pool
                 │
┌────────────────▼────────────────────────────────────────┐
│              DATABASE LAYER                             │
│         (PostgreSQL - Neon/AWS/Azure)                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Table: database_store                                  │
│  ├─ id (SERIAL)                                        │
│  ├─ data_json (TEXT) ← All app data                   │
│  ├─ version (INTEGER)                                  │
│  └─ last_updated (TIMESTAMP)                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🗂️ Data Model

### **Document Store Pattern**

AlphaStream uses a **document-store** approach within PostgreSQL:
- Single table (`database_store`)
- All data stored as JSON in `data_json` column
- Optimistic locking via `version` column

### **JSON Structure**

```json
{
  "metadata": {
    "version": 15,
    "save_count": 42,
    "last_save_timestamp": "2026-02-08 15:30:00",
    "last_save_by": "morris"
  },
  "users": {
    "morris": {
      "email": "morris@example.com",
      "password_hash": "sha256_hash_here",
      "salt": "random_salt",
      "role": "admin",
      "is_active": true,
      "created_at": "2026-02-08 10:00:00",
      "last_login": "2026-02-08 15:29:00",
      "profiles": {
        "TFSA Portfolio": {
          "principal": 100000,
          "bank_name": "TD",
          "account_type": "TFSA",
          "initialization_date": "2025-02-08",
          "drift_tolerance": 5.0,
          "asset_mix_locked": true,
          "assets": {
            "SPXL": {
              "fund_name": "Direxion Daily S&P 500 Bull 3X",
              "target": 50.0,
              "allocated_pct": 100.0,
              "units": 442,
              "purchases": [
                {
                  "date": "2025-05-06",
                  "price": 130.15,
                  "units": 442,
                  "total_cost": 57526.30
                }
              ]
            },
            "GLD": {
              "fund_name": "SPDR Gold Trust",
              "target": 50.0,
              "allocated_pct": 0.0,
              "units": 0,
              "purchases": []
            }
          }
        }
      }
    }
  },
  "global_settings": {
    "allow_registration": true,
    "default_drift_tolerance": 5.0
  }
}
```

---

## 🔐 Security Architecture

### **Authentication Flow**

```
User Login Request
    │
    ├─→ Hash password with SHA-256 + user's salt
    │
    ├─→ Compare with stored password_hash
    │
    ├─→ If match:
    │   ├─ Create session token
    │   ├─ Store in st.session_state
    │   ├─ Update last_login timestamp
    │   └─ Grant access
    │
    └─→ If no match:
        ├─ Increment login_attempts
        ├─ If >= 5 attempts:
        │   └─ Lock account for 30 minutes
        └─ Show error message
```

### **Session Management**

```python
st.session_state = {
    "logged_in": True,
    "username": "morris",
    "user_role": "admin",
    "session_token": "random_token_123",
    "data_version": 15,
    "data_loaded_at": datetime.now(),
    "current_profile": "TFSA Portfolio"
}
```

### **Password Security**

- **Algorithm:** SHA-256
- **Salt:** Random 16-byte per user
- **Storage:** Hash + Salt stored separately
- **No plaintext:** Passwords never stored in plain text

---

## 💾 Database Architecture

### **Connection Pooling**

```python
# Global connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,      # Minimum connections
    maxconn=10,     # Maximum connections
    host="...",
    database="...",
    user="...",
    password="...",
    port="5432"
)

# Get connection from pool
conn = connection_pool.getconn()

# Use connection
cursor = conn.cursor()
# ... execute queries ...

# Return to pool (not close!)
connection_pool.putconn(conn)
```

### **Optimistic Locking**

Prevents data loss from concurrent edits:

```python
# Load data
data, version = load_from_postgres()  # version = 15

# User modifies data
data["users"]["morris"]["last_login"] = "..."

# Save with version increment
new_version = version + 1  # version = 16
save_to_postgres(data, new_version)

# If another user saved version 16 first,
# this save would fail (version conflict)
```

### **Schema Evolution**

Database schema is managed programmatically:

```python
def load_db():
    """Load and upgrade schema automatically"""
    data, version = load_from_postgres()
    
    # Add new fields to existing data
    data.setdefault("new_field", default_value)
    
    # Upgrade user structures
    for user in data["users"].values():
        user.setdefault("new_user_field", default)
    
    return data
```

---

## 🔄 Data Flow

### **Portfolio Creation Flow**

```
1. User fills form
   ├─ Profile name: "Retirement"
   ├─ Principal: $100,000
   ├─ Bank: "TD"
   └─ Account type: "RRSP"

2. Validation
   ├─ Check principal > 0
   ├─ Check unique profile name
   └─ Validate date

3. Load database
   └─ data = load_db()

4. Add profile to user
   data["users"]["morris"]["profiles"]["Retirement"] = {
       "principal": 100000,
       "bank_name": "TD",
       "account_type": "RRSP",
       "assets": {},
       "initialization_date": "2026-02-08"
   }

5. Save to PostgreSQL
   └─ save_db(data)

6. Update UI
   └─ st.success("✅ Profile created!")
```

### **Asset Deployment Flow**

```
1. User selects asset (SPXL) and amount (100%)

2. Fetch current price
   └─ yfinance.Ticker("SPXL").history()

3. Calculate units
   ├─ Target allocation: 50% of $100,000 = $50,000
   ├─ Deploy 100% of target = $50,000
   ├─ Current price: $130.15
   └─ Units: $50,000 / $130.15 = 384 units

4. Create purchase record
   purchase = {
       "date": "2026-02-08",
       "price": 130.15,
       "units": 384,
       "total_cost": 49977.60
   }

5. Update asset
   asset["units"] += 384
   asset["allocated_pct"] = 100.0
   asset["purchases"].append(purchase)

6. Save to database
   └─ Atomic update with version increment
```

---

## 📡 External Integrations

### **Yahoo Finance (yfinance)**

```python
import yfinance as yf

# Fetch ticker info
ticker = yf.Ticker("SPXL")

# Get current price
current_price = ticker.info.get("regularMarketPrice")

# Get historical prices
history = ticker.history(period="1mo")

# Get ticker metadata
name = ticker.info.get("longName")
```

**Usage in AlphaStream:**
- Real-time price fetching for deployments
- Historical price data for cost basis
- Ticker validation
- Fund name retrieval

### **Plotly Charts**

```python
import plotly.graph_objects as go

# Create interactive chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates,
    y=values,
    name="Portfolio"
))

# Display in Streamlit
st.plotly_chart(fig)
```

**Usage:**
- Portfolio value over time
- Asset allocation pie charts
- Benchmark comparison line charts
- Drift visualization

---

## 🔀 State Management

### **Session State Structure**

```python
st.session_state = {
    # Authentication
    "logged_in": bool,
    "username": str,
    "user_role": str,
    "session_token": str,
    
    # Data Management
    "db": dict,                    # Cached database
    "data_version": int,           # Version for conflict detection
    "data_loaded_at": datetime,    # Load timestamp
    
    # Navigation
    "page": str,                   # Current page
    "current_profile": str,        # Selected profile
    
    # UI State
    "deploy_date_value": date,     # Date picker values
    "ticker_input": str,           # Form input values
    
    # Flags
    "show_admin_panel": bool,
    "refresh_data": bool
}
```

### **State Persistence**

- **Session State:** Temporary (lost on page refresh)
- **Database:** Permanent (persists forever)

```python
# Temporary (session only)
st.session_state["temp_value"] = 123

# Permanent (database)
data = st.session_state.db
data["users"]["morris"]["setting"] = value
save_db(data)
```

---

## 🚀 Performance Optimization

### **1. Connection Pooling**
- Reuse database connections
- Avoid connection overhead
- Max 10 concurrent connections

### **2. Lazy Loading**
- Database loaded once per session
- Cached in `st.session_state.db`
- Only reload when explicitly needed

### **3. Caching**
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_ticker_price(ticker):
    return yf.Ticker(ticker).info["regularMarketPrice"]
```

### **4. Minimal Reloads**
- Avoid `st.rerun()` when possible
- Use conditional rendering
- Update UI state without full reload

---

## 📦 Deployment Architecture

### **Streamlit Cloud**

```
GitHub Repository
    │
    ├─→ Push code changes
    │
    ├─→ Streamlit Cloud detects changes
    │
    ├─→ Install dependencies (requirements.txt)
    │
    ├─→ Load secrets (st.secrets)
    │
    ├─→ Start app (streamlit run app.py)
    │
    └─→ Serve on HTTPS URL
```

### **Environment Variables**

Streamlit Cloud injects secrets as environment variables:

```python
# Access PostgreSQL credentials
st.secrets["postgres"]["host"]
st.secrets["postgres"]["dbname"]
st.secrets["postgres"]["user"]
st.secrets["postgres"]["password"]
st.secrets["postgres"]["port"]
```

---

## 🔧 Code Structure

### **Main Application (app.py)**

```
app.py (9,134 lines)
├─ Imports (20 lines)
├─ Version Info (50 lines)
├─ Security Functions (150 lines)
│  ├─ hash_password()
│  ├─ verify_password()
│  └─ validate_password_strength()
├─ Database Functions (200 lines)
│  ├─ get_db_connection()
│  ├─ init_db()
│  ├─ load_from_postgres()
│  ├─ save_to_postgres()
│  ├─ load_db()
│  └─ save_db()
├─ Helper Functions (500 lines)
│  ├─ enhanced_date_input()
│  ├─ log_profile()
│  ├─ calculate_drift()
│  └─ fetch_benchmark_data()
├─ Authentication Pages (400 lines)
│  ├─ login_page()
│  ├─ register_page()
│  └─ logout()
├─ Portfolio Manager (3,000 lines)
│  ├─ Strategy Setup (create profiles)
│  ├─ Asset Allocation (manage assets)
│  ├─ Asset Deployment (deploy capital)
│  ├─ Performance Dashboard
│  └─ Settings
├─ Admin Dashboard (1,000 lines)
│  ├─ User Management
│  ├─ System Health
│  └─ Database Stats
└─ Main Navigation (200 lines)
```

---

## 🛡️ Error Handling

### **Database Errors**

```python
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
except psycopg2.Error as e:
    st.error(f"Database error: {e}")
    conn.rollback()
finally:
    release_db_connection(conn)
```

### **Yahoo Finance Errors**

```python
try:
    ticker = yf.Ticker(symbol)
    price = ticker.info["regularMarketPrice"]
except Exception as e:
    st.warning(f"Could not fetch price for {symbol}")
    price = None
```

### **Validation Errors**

```python
if principal <= 0:
    st.error("Principal must be greater than 0")
    return

if total_allocation > 100:
    st.error("Total allocation cannot exceed 100%")
    return
```

---

## 📊 Scalability Considerations

### **Current Limits**

- **Users:** Unlimited (designed for 10-100 active users)
- **Portfolios per user:** Unlimited (typically 2-5)
- **Assets per portfolio:** Unlimited (typically 5-20)
- **Database size:** Limited by PostgreSQL plan
- **Concurrent connections:** 10 (connection pool max)

### **Scaling Options**

**Vertical Scaling:**
- Upgrade PostgreSQL instance
- Increase connection pool size
- Add caching layer (Redis)

**Horizontal Scaling:**
- Load balancer with multiple Streamlit instances
- Read replicas for PostgreSQL
- CDN for static assets

**Performance Improvements:**
- Index frequently queried JSON paths
- Move to relational schema (from document store)
- Implement GraphQL for efficient queries

---

## 🔮 Future Architecture

### **Planned Improvements**

1. **Microservices Architecture**
   - Authentication service
   - Portfolio service
   - Analytics service
   - Notification service

2. **Event-Driven Design**
   - Pub/Sub for real-time updates
   - Webhook integrations
   - Audit logging

3. **Advanced Caching**
   - Redis for session management
   - Memcached for query results
   - Edge caching for static content

4. **API Layer**
   - REST API for mobile apps
   - GraphQL for flexible queries
   - WebSocket for real-time updates

---

## 📚 Technology Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Streamlit 1.28+ | Web UI framework |
| **Backend** | Python 3.9+ | Application logic |
| **Database** | PostgreSQL 14+ | Data persistence |
| **Connection** | psycopg2 | Database adapter |
| **Market Data** | yfinance | Price & ticker info |
| **Charts** | Plotly 5.17+ | Interactive visualizations |
| **Deployment** | Streamlit Cloud | Hosting platform |
| **Database Host** | Neon | Serverless PostgreSQL |

---

**Architecture Version:** 9.0.1  
**Last Updated:** 2026-02-08  
**Status:** Production-Ready ✅
