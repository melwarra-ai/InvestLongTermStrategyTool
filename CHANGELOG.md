# 📋 AlphaStream Changelog

All notable changes to AlphaStream Portfolio Manager are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---

## [9.0.1] - 2026-02-08 (CURRENT - STABLE)

### 🐛 Fixed
- **CRITICAL:** Renamed remaining `save_to_sqlite()` calls to `save_to_postgres()`
- Fixed JSON migration code (line 1986)
- Fixed base schema initialization (line 2015)
- Resolved `NameError: 'save_to_sqlite' is not defined` crash on startup

### 📝 Notes
- This is a critical bugfix for v9.0.0
- All users should update from v9.0.0 to v9.0.1
- No new features - stability fix only

---

## [9.0.0] - 2026-02-08

### 🚀 Added
- **PostgreSQL backend** - Complete migration from SQLite
- Connection pooling for better performance and reliability
- Cloud-native deployment ready for Streamlit Cloud
- Support for Neon, AWS RDS, Azure, Supabase PostgreSQL

### 🔧 Changed
- Database: SQLite → PostgreSQL
- Secrets: Uses `st.secrets["postgres"]` for credentials
- Schema: Updated to PostgreSQL syntax (SERIAL, VARCHAR, TIMESTAMP)
- SQL placeholders: `?` → `%s`
- UPSERT: `INSERT OR REPLACE` → `INSERT ... ON CONFLICT ... DO UPDATE`

### ❌ Removed
- All SQLite dependencies (`sqlite3` module)
- Local file-based database storage
- `alphastream.db` file

### 📦 Dependencies
- Added: `psycopg2-binary>=2.9.9`

### ⚠️ Breaking Changes
- Requires PostgreSQL database (no longer works with SQLite)
- Requires `secrets.toml` configuration
- Data migration required from v8.x SQLite versions

---

## [8.1.0] - 2026-02-08

### 🎯 Changed
- Deploy % now ALWAYS defaults to 100% (or remaining %)
- Removed "smart" default calculation based on affordable units
- Simplified deployment UX

### ❌ Removed
- Session state memory for last deployed percentage
- Complex default calculation logic (14 lines → 1 line)

### 💡 Benefits
- Predictable, consistent defaults
- One-click full deployment
- No confusion from remembered values (e.g., 1.10%)

---

## [8.0.8] - 2026-02-08

### ✅ Added
- Enhanced date picker with Clear and Today buttons
- Buttons appear below deployment date field
- Proper session state management

### 🐛 Fixed
- Session state errors in enhanced_date_input()
- Date picker now works without StreamlitAPIException

### 📝 Notes
- Clear/Today buttons work outside of forms only
- Profile creation uses standard date picker (inside form)

---

## [8.0.7] - 2026-02-08

### 🔧 Fixed
- **COMPLETE:** All asset management UI now hidden when mix is locked
- Removed duplicate info messages (was showing 2-3 messages)
- Hidden ticker symbol input when locked
- Hidden target allocation field when locked
- Hidden Save Asset and Remove buttons when locked

### 💡 Benefits
- Clean, minimal UI when assets locked
- No visual clutter
- Clear user experience

---

## [8.0.6] - 2026-02-07

### 🐛 Fixed
- Date picker session state error resolved
- Quick Add buttons properly hidden when asset mix locked

### 🔧 Changed
- Using native `st.date_input()` instead of custom enhanced function
- Improved indentation for conditional asset allocation UI

---

## [8.0.5] - 2026-02-07

### ⚠️ Issues (Fixed in 8.0.6)
- StreamlitAPIException in enhanced_date_input()
- Quick Add buttons still visible when locked (indentation error)

---

## [8.0.4] - 2026-02-07

### 🐛 Fixed
- Form button issue resolved
- Removed enhanced_date_input from forms

---

## [8.0.3] - 2026-02-07

### 🐛 Fixed
- NameError for user_profiles definition

---

## [8.0.2] - 2026-02-07

### ✨ Added (attempted)
- Enhanced date picker with Today/Clear buttons
- Collapsible sidebar sections

### ⚠️ Issues (Fixed in 8.0.3)
- Session state errors

---

## [8.0.1] - 2026-02-07

### 🐛 Fixed
- Authentication bug - restored password hashing functions
- Password verification working correctly

---

## [8.0.0] - 2026-02-07

### 🚀 Added
- **SQLite backend** - Migrated from JSON file storage
- Database schema with versioning
- Optimistic locking for concurrent access
- Session state management

### 🔧 Changed
- Data persistence: JSON files → SQLite database
- Improved multi-user support
- Better data integrity

---

## [7.7.3] - 2026-02-02

### 📝 Baseline
- Last version before database migration
- JSON file-based storage
- All core features functional
- Multi-user support with authentication

---

## Version History Summary

| Version | Date | Type | Status |
|---------|------|------|--------|
| **9.0.1** | 2026-02-08 | Bugfix | ✅ **STABLE - CURRENT** |
| 9.0.0 | 2026-02-08 | Major | ❌ Critical bug |
| 8.1.0 | 2026-02-08 | Minor | ✅ Stable |
| 8.0.8 | 2026-02-08 | Patch | ✅ Stable |
| 8.0.7 | 2026-02-08 | Patch | ✅ Stable |
| 8.0.6 | 2026-02-07 | Patch | ✅ Stable |
| 8.0.0 | 2026-02-07 | Major | ✅ Stable |
| 7.7.3 | 2026-02-02 | Baseline | ⚠️ Legacy |

---

## Migration Guides

### 8.x → 9.0.1 (SQLite → PostgreSQL)

**Required Steps:**

1. **Set up PostgreSQL database** (Neon recommended)
2. **Configure secrets.toml** with database credentials
3. **Update requirements.txt** to include `psycopg2-binary`
4. **Deploy v9.0.1** (skip 9.0.0 - it has bugs)

**Data Migration:**

If you have SQLite data to preserve:

```python
# Migration script (run once)
import sqlite3
import psycopg2
import json

# Load from SQLite
conn_sqlite = sqlite3.connect('alphastream.db')
cursor = conn_sqlite.cursor()
cursor.execute("SELECT data_json, version FROM database_store WHERE id = 1")
row = cursor.fetchone()

if row:
    # Save to PostgreSQL
    conn_pg = psycopg2.connect(
        host="your-host",
        database="your-db",
        user="your-user",
        password="your-pass",
        port="5432"
    )
    cursor_pg = conn_pg.cursor()
    cursor_pg.execute("""
        INSERT INTO database_store (id, data_json, version)
        VALUES (1, %s, %s)
    """, (row[0], row[1]))
    
    conn_pg.commit()
    print("✅ Migration complete!")
```

---

## Deprecation Notices

### v9.0.0+
- ❌ **SQLite support removed** - PostgreSQL required
- ❌ **Local database files deprecated** - Cloud database required
- ❌ **JSON file storage deprecated** - Use PostgreSQL only

---

## Known Issues

### v9.0.1
- None - stable release

### Previous Versions
- v9.0.0: Critical startup crash (use 9.0.1 instead)
- v8.0.5: Session state errors (fixed in 8.0.6)
- v8.0.2: Form compatibility issues (fixed in 8.0.3)

---

## Roadmap

### Planned Features

**v9.1.0** (Next Minor Release)
- [ ] Performance dashboard
- [ ] Advanced charting options
- [ ] Export portfolio reports (PDF)
- [ ] Email notifications for drift alerts

**v9.2.0**
- [ ] Mobile-responsive design improvements
- [ ] Dark mode theme
- [ ] Multi-currency support
- [ ] Tax loss harvesting recommendations

**v10.0.0** (Future Major Release)
- [ ] Real-time portfolio sync
- [ ] Automated rebalancing
- [ ] API integration with brokers
- [ ] Machine learning price predictions

### Under Consideration
- Custom benchmarks
- Goal-based planning
- Monte Carlo simulations
- Social features (share strategies)

---

## Support & Feedback

**Report Bugs:**
- GitHub Issues: [github.com/yourusername/alphastream/issues](https://github.com/yourusername/alphastream/issues)
- Email: your-email@example.com

**Request Features:**
- GitHub Discussions
- Email with subject: "Feature Request: [title]"

**Get Help:**
- Documentation: [docs/](docs/)
- Troubleshooting: [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- SQL Queries: [SQL_QUERIES.md](SQL_QUERIES.md)

---

**Current Stable Version: v9.0.1** ✅
