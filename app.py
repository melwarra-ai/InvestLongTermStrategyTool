import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import json
import os
import hashlib
import secrets
import re
import smtplib
import time
import copy
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor


# ===== VERSION INFORMATION =====
VERSION = "9.0.1"
VERSION_DATE = "2026-02-08"
VERSION_TIME = "03:30:00"  # EST  
VERSION_NAME = "PostgreSQL Migration - Bugfix"
CHANGELOG = """
v9.0.1 (2026-02-08 03:30 EST) - 🐛 CRITICAL BUGFIX
- FIXED: Renamed remaining save_to_sqlite() calls to save_to_postgres()
- FIXED: JSON migration now works correctly with PostgreSQL
- FIXED: Base schema initialization uses PostgreSQL function
- BUG: v9.0.0 crashed on first load with NameError: 'save_to_sqlite' is not defined
- STATUS: Production-ready for Streamlit Cloud deployment

**Changes:**
Line 1986: save_to_sqlite() → save_to_postgres() (JSON migration)
Line 2015: save_to_sqlite() → save_to_postgres() (base schema)

v9.0.0 (2026-02-08 03:00 EST) - 🚀 POSTGRESQL MIGRATION (CLOUD OPTIMIZED)
- MIGRATED: Complete database backend from SQLite to PostgreSQL
- ADDED: Streamlit Cloud-optimized connection using st.secrets
- ADDED: Connection pooling for better performance and reliability
- IMPROVED: Cloud-native deployment with persistent database storage
- REMOVED: All SQLite dependencies and local file storage
- BENEFIT: Production-ready for Streamlit Cloud with zero data loss on redeploy

**Migration Details:**
- Database: PostgreSQL (replaces SQLite)
- Connection: psycopg2 with connection pooling
- Secrets: Uses st.secrets["postgres"] for credentials
- Schema: Updated to PostgreSQL syntax (SERIAL, VARCHAR, TIMESTAMP)
- Placeholders: Changed from ? to %s for SQL queries
- Tables: database_store (id SERIAL PRIMARY KEY, data_json TEXT, version INT, last_updated TIMESTAMP)

**Required secrets.toml:**
```toml
[postgres]
host = "your-host.postgres.database.azure.com"
dbname = "your-database-name"
user = "your-username"
password = "your-password"
port = "5432"
```

**100% Feature Parity:**
All features, UI, UX, and logic remain identical to v8.1.0.
Only the database backend has changed.

v8.1.0 (2026-02-08 02:00 EST) - 🎯 FORCE 100% DEFAULT ALWAYS
- REMOVED: Session state memory for last deployed percentage
- FIXED: Deploy % now ALWAYS defaults to 100% (no memory of previous values)
- IMPROVED: Clean, predictable default every time you deploy
- BENEFIT: No more confusion from remembered old values like 1.10%

**The Problem:**
v8.0.9 defaulted to 100%, BUT if you previously deployed 1.10%, 
the app "remembered" that value in session state and kept using it!

**The Solution:**
Completely removed session state memory. Deploy % ALWAYS starts at:
- 100.0% if you haven't deployed any of this asset yet
- Remaining % if you've partially deployed (e.g., 40% if 60% done)

**No more surprises!** Every deployment starts fresh at 100%.

v8.0.9 (2026-02-08 01:30 EST) - 📊 DEFAULT DEPLOY 100%
- CHANGED: Deploy % (of asset's target) now defaults to 100%
- IMPROVED: Simple, predictable default instead of complex calculation
- REMOVED: "Smart" default logic that could result in low values like 1.10%
- BENEFIT: Users can now deploy full allocation with one click

**Before:**
Deploy % default: 1.10% (complex calculation based on affordable units)

**After:**
Deploy % default: 100.0% (or remaining %, whichever is smaller)

**How It Works:**
- First deployment of an asset → Defaults to 100%
- Subsequent deployments → Uses last deployed % OR 100%, whichever applies
- If only 30% remaining → Defaults to 30% (respects available amount)

v8.0.8 (2026-02-08 01:00 EST) - ✅ WORKING CLEAR/TODAY BUTTONS
- FIXED: enhanced_date_input() function completely rewritten to work without errors
- FIXED: Clear and Today buttons now appear BELOW the date picker
- FIXED: Deployment date picker now uses enhanced version with working buttons
- IMPROVED: Buttons use emojis (🗑️ Clear | 📅 Today) for better UX
- IMPROVED: Session state properly managed to avoid conflicts
- BENEFIT: Clear/Today buttons finally work as requested!

**How It Works Now:**
Deployment Date Picker shows:
┌────────────────────────────┐
│ Deployment Date            │
│ [Calendar: 2026/02/08]     │
└────────────────────────────┘
┌─────────────┬──────────────┐
│ 🗑️ Clear    │  📅 Today    │
└─────────────┴──────────────┘

- Click "Today" → Sets to current date
- Click "Clear" → Clears selection (defaults to today for deployment)
- No session state errors!

**Note:** Profile creation date (Inception Date) uses standard picker 
because it's inside a form (forms can't have buttons). Enhanced picker 
is used in deployment section which is NOT in a form.

v8.0.7 (2026-02-08 00:00 EST) - 🔧 COMPLETE UI HIDING FIX
- FIXED: ALL asset management UI now properly hidden when mix is locked
- FIXED: Removed duplicate info messages (was showing 2-3 messages)
- FIXED: Ticker Symbol input HIDDEN when locked
- FIXED: Target Allocation field HIDDEN when locked  
- FIXED: Save Asset and Remove buttons HIDDEN when locked
- IMPROVED: Single clear message when locked
- BENEFIT: Clean, minimal UI when assets are locked

**Complete Fix for Asset Allocation Section:**
When locked, EVERYTHING is hidden:
- ❌ Quick Add buttons (SPXL, GLD, DBMF, BIL)
- ❌ Ticker Symbol input
- ❌ Target Allocation % field
- ❌ Save Asset button
- ❌ Remove button

Only shows:
- ✅ Current assets list (SPXL, GLD, etc.)
- ✅ One clear message: "Asset mix is locked"

v8.0.6 (2026-02-07 23:00 EST) - 🔧 CRITICAL UX FIXES
- FIXED: Cannot use st.button() inside st.form() error
- ISSUE: enhanced_date_input() contains buttons, incompatible with forms
- CHANGED: Replaced enhanced_date_input() with regular st.date_input() in profile creation form
- RESULT: Profile creation form now works correctly
- NOTE: Enhanced date pickers can only be used OUTSIDE of forms
- STATUS: Stable release ready for deployment

v8.0.3 (2026-02-07 18:30 EST) - 🔧 BUG FIX
- FIXED: NameError - removed duplicate user_profiles definition
- ISSUE: Line 4757 was redefining user_profiles (already defined at 4659)
- RESULT: Application now loads correctly without NameError
- STATUS: Stable release ready for deployment

v8.0.2 (2026-02-07 18:15 EST) - ✨ UX ENHANCEMENTS
- ENH 1: Enhanced date picker with Today/Clear buttons
- ENH 2: Collapsible sidebar sections (auto-collapse after completion)
- ENH 3: Cleaner sidebar organization with expanders
- ENH 4: Better visual hierarchy in sidebar
- IMPROVED: Date selection for Inception Date and Deployment Date
- IMPROVED: Sidebar sections collapse when not in use
- BENEFIT: Less scrolling, cleaner interface
- BENEFIT: Faster navigation to active tasks

**Enhancement 1: Better Date Pickers**
Before: Basic date input
After: Date input with "Today" and "Clear" buttons ✅
- Quick access to today's date
- Easy way to clear selection
- Consistent across all date fields

**Enhancement 2: Collapsible Sidebar Sections**
Before: All sections always visible (lots of scrolling)
After: Sections collapse after completion ✅
- Profile Creation: Collapses after profile created
- Portfolio Configuration: Collapses when complete
- Asset Deployment: Collapses when fully deployed
- Focus on current active task

v8.0.1 (2026-02-07 17:45 EST) - 🔧 CRITICAL AUTH FIX
- FIXED: Restored missing hash_password() function
- FIXED: Restored missing verify_password() function
- FIXED: Restored missing validate_password_strength() function
- FIXED: Restored missing validate_email() function
- FIXED: Restored missing generate_session_token() function
- FIXED: Added password security configuration constants
- ISSUE: These functions were accidentally removed during SQLite migration
- RESULT: Login and registration now work correctly
- STATUS: All authentication functionality restored

v8.0.0 (2026-02-07 17:30 EST) - 🗄️ SQLITE MIGRATION
- MAJOR: Replaced Google Sheets backend with SQLite database
- REMOVED: All Google Sheets dependencies (gspread, google-auth)
- ADDED: Local SQLite database (alphastream.db)
- ADDED: init_db() function for automatic schema creation
- IMPROVED: Faster data access with local database
- IMPROVED: No external API dependencies
- IMPROVED: Eliminates UTF-8 encoding issues from Google Sheets
- MAINTAINED: 100% feature parity with v7.7.3
- MAINTAINED: All UI/UX elements unchanged
- MAINTAINED: All emojis and special characters preserved

**Tables Created:**
- database_store: Main table storing complete database as JSON

**Benefits:**
- ✅ No Google Sheets API quota limits
- ✅ Faster read/write operations
- ✅ No network dependency for data access
- ✅ Eliminates encoding corruption issues
- ✅ Simpler deployment (no service account needed)
- ✅ Built-in ACID transactions
- ✅ Works offline

**Migration Notes:**
- This is a fresh install - no data migration needed
- All existing functionality preserved
- Database file: alphastream.db (auto-created on first run)
- Backup recommended: export data regularly via Admin Dashboard

v7.7.3 (2026-02-02 22:30 EST) - ✨ 4 UX REFINEMENTS
- ENH 1: Deployment status shows "In Progress - 50% complete" (clearer)
- ENH 2: Deploy % defaults to max whole units % (no fractional)
- ENH 3: Rebalance table shows precise deployed % (e.g., 99.95%)
- ENH 4: Ticker input disabled when asset mix locked

**Enhancement 1: Better Deployment Status**
Before: Deployment: 0/4 - In Progress (confusing!)
After: Deployment: In Progress - 50% complete ✅

**Enhancement 2: Smart Deploy % Default**
Calculates max whole units you can afford and defaults to that %.

Example:
  Available: $12,045
  Price: $120.45
  Max units: 100
  Max amount: $12,045 (100 × $120.45)
  Target budget: $20,000
  Smart default: 60.2% (no fractional shares!)

Before: Always defaulted to 25%
After: Defaults to max whole units % ✅

**Enhancement 3: Precise Deployed %**
Before: Deployed: 99% or 100%
After: Deployed: 99.95% (2 decimal precision)

Shows exact deployment progress, not rounded.

**Enhancement 4: Lock UI When Locked**
Before: Ticker input active, buttons clickable when locked
After: Ticker input disabled + info message shown ✅

Clearer indication that mix is locked.

v7.7.2 (2026-02-02 22:00 EST) - ✨ 7 UX ENHANCEMENTS
- ENH 1: Asset allocation shows "target allocated" instead of price
- ENH 2: "Today" button properly updates Deployment Date field
- ENH 3: "Deploy All" only shows when all assets are 100% deployed
- ENH 4: Deploy All text size matches sidebar (smaller, consistent)
- ENH 5: Target % disabled when asset mix locked (prevents changes)
- ENH 6: Deploy % defaults to previously used value per asset
- ENH 7: Number of Units defaults to max available (v7.7.1 feature)

**Enhancement 1: Better Asset Messages**
Before: ✅ State Street SPDR Bloomberg 1-3 Month T-Bill ETF - $91.41
After: ✅ State Street SPDR Bloomberg 1-3 Month T-Bill ETF - Asset target allocated

**Enhancement 2: Today Button Fixed**
Before: Click "Today" → Nothing happens
After: Click "Today" → Date field updates to today ✅

**Enhancement 3: Deploy All Context**
Before: Shows anytime there's remaining cash
After: Only shows after ALL assets reach 100% deployment
Logic: Makes sense to "Deploy All Remaining" only after main deployment done

**Enhancement 4: Consistent Text Size**
Before: ### headings (very large) in Deploy All section
After: #### and ** headings (normal sidebar size)
Result: Visually consistent with rest of sidebar

**Enhancement 5: Protect Locked Allocations**
Before: Can change target % even when locked
After: Target % field disabled when asset mix locked
Unlock required to change allocations

**Enhancement 6: Remember Deploy %**
Before: Always defaults to 25%
After: Defaults to last used % for each asset
Example:
  - First time SPXL: 25%
  - Deploy 30%
  - Next time SPXL: 30% (remembers!)

**Enhancement 7: Max Units Default**
Status: Already implemented in v7.7.1 ✅
Number of Units defaults to max whole units available

v7.7.1 (2026-02-02 21:30 EST) - 🔢 DEFAULT UNITS TO MAX
- IMPROVED: "Number of Units" now defaults to maximum available
- CHANGED: Default changed from 1 unit to max whole units
- ADDED: Help text explains default behavior
- BENEFIT: Users can deploy full budget with one click
- BENEFIT: Still can manually reduce if needed

**What Changed:**

Before (v7.7.0):
```
💡 Max whole units for available budget: 100
Number of Units: [1] ← Default to 1, user must type 100
```

After (v7.7.1):
```
💡 Max whole units for available budget: 100
Number of Units: [100] ← Defaults to max! User can reduce if needed
```

**Example Scenario:**

Available Budget: $12,045
Asset Price: $120.45
Max Units: 100

Before: User sees [1], must manually type 100
After: User sees [100], can click Deploy or reduce to 50

**Benefits:**
- ✅ One-click full deployment (most common use case)
- ✅ Maximizes capital deployment by default
- ✅ Still allows partial deployment (user can change)
- ✅ Faster workflow for users
- ✅ Better UX - defaults to what most users want

**Use Cases:**

Full Deployment (90% of users):
  1. Select asset
  2. See: "Number of Units: [100]" ✅ Already set!
  3. Click Deploy
  
Partial Deployment (10% of users):
  1. Select asset
  2. See: "Number of Units: [100]"
  3. Change to: [50] (deploy half)
  4. Click Deploy

v7.7.0 (2026-02-02 21:00 EST) - 💰 DEPLOY ALL WITH ACTUAL PRICES
- MAJOR: Deploy All Remaining Cash now allows actual price input
- ADDED: Expandable sections for each asset in deployment plan
- ADDED: Side-by-side comparison: Estimated vs Actual
- ADDED: Real-time cost calculation with actual prices
- ADDED: Price difference indicators (up/down vs estimate)
- ADDED: Summary showing total estimated vs actual costs
- ADDED: Validation prevents over-spending
- IMPROVED: Actual prices used for average cost calculation
- IMPROVED: Clear visual feedback throughout process

**How It Works:**

1. **Show Deployment Plan:**
   - App calculates units based on available cash
   - Shows estimated price from yfinance
   - Displays total estimated cost

2. **User Inputs Actual Prices:**
   - Each asset has editable "Price Paid per Unit" field
   - Defaults to estimated price (can override)
   - Shows price difference vs estimate
   - Calculates actual total in real-time

3. **Summary Section:**
   - Estimated total cost
   - Actual total cost
   - Difference highlighted
   - Remaining cash after deployment

4. **Deploy with Actual Prices:**
   - Uses actual prices for purchase records
   - Correctly calculates average cost per asset
   - Updates allocated % based on actual spend
   - Logs actual prices paid

**Example:**

Available Cash: $10,000

SPXL:
  Estimated: 40 shares × $120.45 = $4,818.00
  Actual: 40 shares × $121.00 = $4,840.00 📈 +$0.55
  
BIL:
  Estimated: 48 shares × $105.30 = $5,054.40
  Actual: 48 shares × $104.95 = $5,037.60 📉 -$0.35

Summary:
  Estimated Total: $9,872.40
  Actual Total: $9,877.60 (+$5.20)
  Remaining: $122.40

✅ Confirm & Deploy All → Records actual prices!

**Benefits:**
- ✅ Accurate average cost tracking
- ✅ No manual price entry errors
- ✅ Real-time validation
- ✅ Clear before/after comparison
- ✅ Prevents over-spending

v7.6.5 (2026-02-02 20:30 EST) - 🇨🇦 CANADIAN BENCHMARK FIX
- FIXED: Canadian benchmarks now display correctly on performance chart
- ADDED: .TO suffix for Toronto Stock Exchange tickers
- IMPROVED: Error messages show if benchmark fails to load
- FIXED: XIU, XIC, ZCN, VCN now work properly

**What Was Wrong (v7.6.4):**
- Canadian tickers (XIU, XIC, ZCN, VCN) weren't showing on chart
- yfinance needs ".TO" suffix for Toronto Stock Exchange
- Silent error handling hid the problem
- Users saw empty chart with no explanation

**What's Fixed (v7.6.5):**
```python
# Before
yf.download("XIU", ...)  # ❌ Fails silently

# After  
yf.download("XIU.TO", ...)  # ✅ Works!
```

**Automatic Suffix Mapping:**
- XIU → XIU.TO (iShares S&P/TSX 60)
- XIC → XIC.TO (iShares Core TSX Composite)
- ZCN → ZCN.TO (BMO TSX Capped Composite)
- VCN → VCN.TO (Vanguard FTSE Canada)

**Error Handling:**
- Shows warning if benchmark fails to load
- Displays specific error message
- Doesn't crash the entire chart
- Other benchmarks still display

**Test It:**
1. Go to Benchmark Comparison
2. Select: 🇨🇦 TSX 60 (XIU)
3. Save benchmarks
4. Check Performance vs Goal Path chart
5. Should see XIU dotted line! ✅
6. Hover shows: "XIU (+X.X%)"

v7.6.4 (2026-02-02 20:00 EST) - 📝 LARGER TEXT IMPROVEMENTS
- IMPROVED: Asset target line now uses ### heading (larger)
- IMPROVED: Deployed/Budget info now 1.1rem font size (larger)
- IMPROVED: Price display now 1.2rem with custom styling (prominent)
- IMPROVED: Budget allocation header now ### (larger)
- IMPROVED: Deployment Preview header now 1.2rem (larger)
- IMPROVED: All preview items now 1.05rem (easier to read)
- IMPROVED: Units highlighted at 1.15rem (most important)
- IMPROVED: "Enter Actual Purchase Details" now ### (larger)

**Before (v7.6.3):**
```
#### SPXL: Target $100,000 (100.0% of portfolio)
**Deployed:** $0 (0%) • **Budget Remaining:** $100,000
```

**After (v7.6.4):**
```
### SPXL: Target $100,000 (100.0% of portfolio)
[1.1rem font] Deployed: $0 (0%) • Budget Remaining: $100,000
```

**Text Size Hierarchy:**
- Asset name: ### (h3 heading - largest)
- Deployed info: 1.1rem (11% larger than normal)
- Price display: 1.2rem in blue box (20% larger, prominent)
- Preview header: 1.2rem (20% larger)
- Preview items: 1.05rem (5% larger)
- Units value: 1.15rem (15% larger, highlighted)

**All text more visible and easier to read!** ✅

v7.6.3 (2026-02-02 19:30 EST) - 🔧 PRICE PRE-FILL FIX
- FIXED: Actual Price Paid now properly pre-fills with estimated price
- FIXED: Widget key now includes date and units to force refresh
- IMPROVED: Price field updates immediately when date or units change

**What Was Wrong (v7.6.2):**
- Streamlit was caching the widget state with static key
- Price field wouldn't update when changing date/units
- Users saw blank or old value instead of preview price

**What's Fixed (v7.6.3):**
- Dynamic key: "actual_deploy_price_{ticker}_{date}_{units}"
- Widget refreshes when any input changes
- Always shows current preview price
- User can still override with actual broker price

**Test It:**
1. Select asset and date
2. Choose units (e.g., 10 units)
3. See preview: "10 units @ $120.45"
4. Scroll down to "Actual Price Paid"
5. Should show: $120.45 (pre-filled!) ✅
6. Change units to 20
7. Price updates to new preview price ✅

v7.6.2 (2026-02-02 19:00 EST) - ✨ UX ENHANCEMENTS
- IMPROVED: Actual Price Paid now defaults to estimated price during deployment
- IMPROVED: Larger, more visible text in Record Asset Deployment section
- ADDED: Canadian benchmark options (XIU, XIC, ZCN, VCN)
- ENHANCED: Deployment section headers now use larger fonts (#### markdown)
- ENHANCED: Better visibility for deployment method selection
- ENHANCED: Clearer labels throughout asset deployment workflow

**Enhancement 1: Price Pre-fill**
- "Actual Price Paid" now defaults to preview price
- Aligns with value shown in "Deployment Preview"
- Users can still override with actual broker price
- Reduces data entry errors

**Enhancement 2: Bigger Text**
- Section title: "Deploy Capital Into Assets" (larger)
- Asset info: Uses #### heading (larger)
- Method selection: "Choose Deployment Method" (larger)
- Date selection: "Select Purchase Date" (larger)
- Better readability for all users

**Enhancement 3: Canadian Benchmarks**
- 🇨🇦 TSX 60 (XIU) - Top 60 large cap
- 🇨🇦 TSX Composite (XIC) - Broad market
- 🇨🇦 TSX Capped Comp (ZCN) - Capped weights
- 🇨🇦 FTSE Canada (VCN) - All cap
- US benchmarks still available (SPY, QQQ, etc.)
- Flag emojis for easy identification

v7.6.1 (2026-02-02 17:30 EST) - 📊 GOAL TRACKER - YEAR START VALUE ADDED
- ADDED: Year Start Value now displayed alongside Current and Year-End Target
- IMPROVED: Three-column layout for clear progression view
- ENHANCED: Shows complete journey: Start → Current → Target
- VISUAL: Grid layout with labels for each metric

**New Display (3 Columns):**
┌─────────────────────────────────────────────────────────────┐
│ Year Start        Current           Year-End Target         │
│ $71,699          $73,252            $85,394                 │
│                                     (19.1% goal)            │
└─────────────────────────────────────────────────────────────┘

**Why This Helps:**
- See starting point (Year Start: $71,699)
- See where you are now (Current: $73,252)  
- See where you're going (Year-End Target: $85,394)
- Understand complete annual journey at a glance

**For Multi-Year Portfolios:**
Year Start Value = Compounded value at start of current year
Example: Started 2024 with $50k, grew to $65k by Jan 1 2026
- Year Start (2026): $65,000
- Not the original $50,000 principal

v7.6.0 (2026-02-02 17:00 EST) - 🎯 GOAL PROGRESS TRACKER FIXED!
- FIXED: Year-End Target now shows correct value (principal × 1.191)
- FIXED: Progress bar shows % of annual goal achieved (not confusing 128%)
- FIXED: Delta shows how far ahead/behind pro-rated target
- IMPROVED: Clear display: Current vs Year-End Target
- ADDED: Annualized projection at current pace
- ENHANCED: Better status badges (Exceeding, On Track, Behind)
- ENHANCED: Color-coded delta (green ahead, red behind)

**What Changed (Your Example):**
OLD (v7.5.1):
- Current: $73,252
- Target: $72,910 (19.1%/yr)  ← Wrong! Lower than current
- Progress: 128% of goal path  ← Confusing!

NEW (v7.6.0):
- Current: $73,252
- Year-End Target: $85,394 (19.1%)  ← Correct! Shows year-end goal
- Progress: 11% done (visual bar)      ← Clear!
- Status: Ahead by $428                ← Precise delta
- Projection: On pace for 26.4% annual ← Future outlook

**The Math:**
Principal: $71,699
Goal: 19.1% = $13,695 growth
Year-End Target: $71,699 + $13,695 = $85,394
Current: $73,252
Progress: ($73,252 - $71,699) / $13,695 = 11.3%
Pro-rated (1 month): Should be at $72,824
Delta: $73,252 - $72,824 = +$428 ahead! 🎯

v7.5.1 (2026-02-02 16:30 EST) - 🎯 ADMIN DASHBOARD STATUS ALIGNMENT
- FIXED: Admin Dashboard Portfolio Comparison Table now uses centralized status check
- FIXED: Status in table matches Global Dashboard and Portfolio Manager
- REMOVED: Duplicate/outdated status calculation logic
- ALIGNED: All three views (Global, Admin, Portfolio) show identical status
- ADDED: "⚙️ Setup" status for portfolios with 0 assets in Admin table

**What This Fixes:**
Your Issue:
- Global Dashboard: "✅ Deployed"
- Admin Table: "📥 Deploying (3/4)" ← WRONG!
- Result: Confusing inconsistency

After v7.5.1:
- Global Dashboard: "✅ Deployed"
- Admin Table: "✅ Deployed" ← CORRECT!
- Portfolio Manager: "✅ Deployed"
- Result: Perfect alignment! ✅

**Now Using ONE Function Everywhere:**
- Portfolio Manager → check_deployment_status()
- Global Dashboard → check_deployment_status()
- Admin Dashboard → check_deployment_status()
- Action Items → check_deployment_status()

v7.5.0 (2026-02-02 16:00 EST) - 🔄 REFRESH BUTTON IMPLEMENTATION
- ADDED: Refresh button at Portfolio Manager header (top right)
- ADDED: Refresh button at Global Dashboard header
- ADDED: Refresh button at Rebalance Analysis section
- FEATURE: 5-second cooldown to prevent spam
- FEATURE: Loading spinner during refresh
- FEATURE: Success message after completion
- FEATURE: Shows "X seconds ago" during cooldown
- UX: Disabled state with helpful tooltips
- UX: Clears cached data for fresh price fetch

**Where Refresh Buttons Are:**
1. Portfolio Manager (top right) - Main refresh for portfolio view
2. Global Dashboard (top right) - Refreshes all portfolios
3. Rebalance Analysis (section header) - Quick update before rebalancing

**How It Works:**
- Click 🔄 Refresh
- Fetches latest market prices
- Updates all calculations
- Shows success message
- 5s cooldown before next refresh

**User Control:**
- Manual refresh when needed
- No constant auto-refresh (saves API calls)
- Perfect for checking prices before decisions

v7.4.3 (2026-02-02 15:30 EST) - 🎯 STATUS BADGE ALIGNMENT
- FIXED: Global Dashboard now shows "⚙️ Setup" for portfolios with 0 assets
- FIXED: Empty portfolios return is_fully_deployed = False (not True)
- ADDED: Setup status badge in Global Dashboard (gray badge)
- ALIGNED: Portfolio Manager and Global Dashboard now show same status
- NOTE: "Test2" with 0 assets now shows "⚙️ Setup" on both views!

**Status Badge Hierarchy:**
1. 🚨 REBALANCE - Drift exceeds tolerance (priority 1)
2. ✅ Balanced - Recently rebalanced and no drift (priority 2)
3. ⚙️ Setup - No assets defined yet (NEW!)
4. 📥 Deploying (X/Y) - Has assets, partial deployment
5. ✅ Deployed - All assets fully deployed
6. ⚪ New - Fallback status

**Your "Test2" Profile:**
- Assets: 0
- Old status: "✅ Deployed" ❌
- New status: "⚙️ Setup" ✅

v7.4.2 (2026-02-02 15:00 EST) - 👁️ SHOW ALL PROFILES
- FIXED: Global Dashboard now shows ALL profiles, regardless of deployment status
- FIXED: Profiles in "Setup" status (no deployments yet) now visible on dashboard
- CHANGED: Welcome page only shown for brand new users with ZERO profiles
- IMPROVED: You can now see your "Test" profile even before deploying assets
- NOTE: Dashboard shows profiles in any state: Setup, Deploying, or Deployed!

**What Changed:**
- Old: Dashboard hidden until at least 1 asset has units deployed
- New: Dashboard shown as soon as ANY profile is created
- Result: "Test" profile with 1 asset but 0 units now shows on dashboard! ✅

v7.4.1 (2026-02-02 04:30 EST) - 🔧 SELF-CONTAINED STATUS CHECK
- FIXED: check_deployment_status() now fetches its own prices
- FIXED: No longer requires prices parameter (self-contained)
- FIXED: Works in Portfolio Manager context (was getting NameError)
- IMPROVED: Function is truly independent and can be called from anywhere
- NOTE: Each view no longer needs to fetch prices before calling the function

**What Changed:**
- Before: check_deployment_status(profile, prices) ← needed prices from caller
- After: check_deployment_status(profile) ← fetches prices itself
- Result: Function works everywhere without dependencies! ✅

v7.4.0 (2026-02-02 04:00 EST) - 🎯 SINGLE SOURCE OF TRUTH (Major Architecture Fix!)
- FIXED: Created centralized check_deployment_status() function
- FIXED: Portfolio Manager, Global Dashboard, and Action Items now use SAME logic
- REMOVED: Duplicate deployment detection code in 3 different places
- IMPROVED: Status is calculated once and used everywhere consistently
- ARCHITECTURE: No more conflicting status between views - ONE source of truth!

**What This Means:**
- Portfolio Manager status: Uses check_deployment_status()
- Global Dashboard cards: Uses check_deployment_status()
- Action Items Dashboard: Uses check_deployment_status()
- Result: ALL THREE always show the SAME status! ✅

**The Fix You Requested:**
"The status at the global dashboard should just reflect what the status at 
the profile level is. There shouldn't be different logic for that."
→ DONE! Now there's only ONE logic, used by all three views.

v7.3.6 (2026-02-02 03:00 EST) - ✅ PER-ASSET BUDGET CHECK (FINAL FIX!)
- FIXED: Now checks remaining budget PER ASSET, not total cash
- FIXED: Treats assets as 100% deployed when remaining budget < share price
- IMPROVED: Exactly implements the logic: "if can't buy 1 share, it's fractional"
- ENHANCED: GLD at 99% with $215 remaining vs $445/share = Fully Deployed ✅
- NOTE: This is the correct implementation of your described logic!

**The Right Logic:**
For GLD specifically:
- Target: 30% = $21,510
- Deployed: 99% = $21,295
- Remaining budget: $215
- GLD price: $445/share
- Can buy 1 share? $215 < $445 = NO
- Status: Fully Deployed ✅ (fractional remainder)

**Result:**
- Action Items: "✅ ALL CLEAR"
- Portfolio Card: "✅ Deployed"
- No more false "GLD needs 1% more" alerts!

v7.3.5 (2026-02-02 02:30 EST) - 🔧 DEPLOYMENT LOGIC SIMPLIFIED
- FIXED: Simplified deployment check to use total undeployed cash
- IMPROVED: Now checks if cash can buy shares in ANY under-allocated asset
- FIXED: Handles edge case where GLD is 99% deployed with $215 remaining
- ENHANCED: More robust logic that actually works in production
- NOTE: If allocated_pct < 100% AND undeployed_cash >= price → Not deployed

**What This Really Fixes:**
Your case:
- GLD: 99% deployed (not 100%!)
- GLD remaining: ~$215
- GLD price: $445/share
- $215 < $445 → Can't buy
- All other assets: 100% deployed
- Result: all_deployed = True ✅
- Status: "✅ Deployed" (finally!)

v7.3.4 (2026-02-02 02:00 EST) - 🎯 SMART DEPLOYMENT DETECTION
- FIXED: Now checks if assets have ROOM in target allocation, not just if cash exists
- IMPROVED: Properly detects when portfolio is fully deployed despite having cash
- ENHANCED: Handles edge case where all assets are at/over target
- FIXED: Portfolio with $285 but all assets over-allocated now shows "✅ Deployed"
- NOTE: Checks both "can afford shares" AND "has allocation budget" per asset!

**What This Fixes:**
Your TFSA case:
- Has: $285 undeployed cash
- DBRM: $28.76/share (affordable!)
- BUT: DBRM already at 14.89% vs 15% target (over-allocated!)
- GLD: Already at 30.70% vs 30% target (over-allocated!)
- Result: No room to deploy without breaking allocation
- Status: ✅ Deployed (correctly!)

v7.3.3 (2026-02-02 01:30 EST) - ✅ ACTION ITEMS FIXED
- FIXED: Action Items Dashboard now uses smart fractional detection
- FIXED: No more false "GLD needs 1% more" alerts
- FIXED: Portfolios with only fractional remainders show "ALL CLEAR"
- ENHANCED: Consistent status logic across entire application
- NOTE: Action Items, Global Dashboard, and Portfolio Manager all synchronized!

**What This Fixes:**
- Action Items Dashboard was using old simple 99.5% check
- Now uses same smart fractional logic as everywhere else
- Your TFSA with $285 fractional will show "✅ ALL CLEAR" not "📥 IN PROGRESS"

v7.3.2 (2026-02-02 01:00 EST) - ✅ DASHBOARD STATUS FIXED
- FIXED: Global Dashboard now correctly shows "✅ Deployed" status
- FIXED: Status uses smart fractional detection like Portfolio Manager
- IMPROVED: Accurate deployed count (X/Y assets) accounting for fractional remainders
- ENHANCED: Portfolio with $285 fractional remainder now shows "Deployed" not "Deploying"
- NOTE: Global Dashboard and Portfolio Manager status now perfectly synchronized!

**What Changed:**
- Old logic: Simple check if allocated_pct >= 99.5%
- New logic: Smart check if undeployed cash < cheapest asset price (fractional)
- Result: Portfolios with only fractional remainders show "✅ Deployed" ✨

v7.3.1 (2026-02-02 00:30 EST) - 📦 AI PACKAGE FIXED
- FIXED: Added anthropic package to requirements.txt
- FIXED: AI Assistant will now work on Streamlit Cloud
- UPDATED: requirements.txt now includes anthropic>=0.18.0
- NOTE: Redeploy app for AI Assistant to work properly!

**After deploying this version:**
1. Streamlit Cloud will automatically install anthropic package
2. AI Assistant feature will work without errors
3. No manual pip install needed!

v7.3.0 (2026-02-02 00:00 EST) - ⚙️ FEATURE VISIBILITY RESTORED
- ADDED: AI Assistant configuration in Admin Dashboard → Settings
- IMPROVED: Clear UI for enabling/disabling AI Assistant
- IMPROVED: Email notifications easier to find and configure
- ENHANCED: Both features now have admin controls in Settings tab
- FIXED: Made feature availability more transparent
- NOTE: Admins can now easily enable AI Assistant and Email Notifications!

**How to Enable Features:**
1. Go to Admin Dashboard → System Management → Global Settings
2. Enable "Email Notifications" and/or "AI Assistant"
3. Configure SMTP settings (for email) or API key (for AI)
4. Save settings
5. Features will appear in user sidebars!

v7.2.9 (2026-02-01 23:00 EST) - 🔧 WELCOME BUTTON FIXED
- FIXED: "Create My First Portfolio" button now works!
- IMPROVED: Button navigates to Portfolio Manager page
- IMPROVED: Auto-expands "Create New Profile" section
- ENHANCED: Seamless flow from welcome page to profile creation
- NOTE: Click the button and you'll be taken right to the form!

v7.2.8 (2026-02-01 22:00 EST) - 🎯 WELCOME PAGE LOGIC FIX
- FIXED: Welcome page now displays FIRST, before dashboard title
- IMPROVED: Logic prioritizes showing welcome page for new users
- IMPROVED: Dashboard title only shows when user has configured portfolios
- ENHANCED: Cleaner flow between welcome and dashboard states
- NOTE: Welcome page now truly shows for users with no portfolios

v7.2.7 (2026-02-01 21:00 EST) - 🎉 WELCOME EXPERIENCE ENHANCED
- IMPROVED: Welcome page now shows for users with empty portfolios
- IMPROVED: Welcome page displays even if profile exists but has no assets
- FIXED: New users now see onboarding guide instead of blank page
- ENHANCED: Better first-time user experience
- NOTE: Makes the app more user-friendly for new accounts

v7.2.6 (2026-02-01 19:30 EST) - 🔧 NATIVE COMPONENTS FIX
- FIXED: HTML rendering issue by using Streamlit native components
- CHANGED: Activity logs now use st.container() and st.columns()
- REMOVED: Raw HTML that was being escaped by Streamlit
- IMPROVED: Cleaner, more reliable rendering
- IMPROVED: Added color emojis for better visual distinction
- NOTE: No more raw HTML tags showing!

v7.2.5 (2026-01-31 07:00 EST) - 🐛 HTML RENDERING FIX (FAILED)
- FIXED: HTML escaping issue in activity logs
- FIXED: Added "user_login" action type mapping
- IMPROVED: More robust HTML generation
- IMPROVED: Better handling of special characters in details
- Note: If you see raw HTML tags, this version fixes it

v7.2.4 (2026-01-31 00:30 EST) - 📊 ENHANCED ANALYTICS
- NEW: Enhanced Recent Activity with detailed view
- NEW: Activity log filtering (by user, action type)
- NEW: Search functionality in activity details
- NEW: Show 5-100 entries (adjustable)
- NEW: CSV export for all activity logs
- NEW: Color-coded action types with icons
- NEW: Time ago display (e.g., "2h ago")
- NEW: Activity statistics (unique users, action types)
- IMPROVED: Better visual design with cards
- IMPROVED: Shows IP address when available
- IMPROVED: Numbered entries for reference

v7.2.3 (2026-01-31 00:15 EST) - 🐛 RESET VERSION FIX
- FIXED: Database reset now properly resets version to 1 (was 84)
- FIXED: Reset now also resets save_count to 1
- IMPROVED: Reset success message shows version number
- Note: After reset, DB version will be 1 as expected

v7.2.2 (2026-01-30 23:50 EST) - 🎨 UI IMPROVEMENTS & BACKUP FIX
- FIXED: Backup download now works (immediate browser download)
- NEW: Restore from backup functionality (upload & restore)
- IMPROVED: Compact button sizes (Download, Restore, Reset)
- IMPROVED: Better visual layout and spacing
- CONFIRMED: Reset Database visible in Danger Zone
- CONFIRMED: All v7.2.1 critical fixes intact
- Note: Incremental version update as requested

v7.2.1 (2026-01-30 04:25 EST) - 🚨 CRITICAL BUG FIXES
- CRITICAL: Fixed Google Sheets 50,000 character limit exceeded error
- CRITICAL: Fixed merge logic to preserve ALL existing users
- FIXED: Data loss bug where users were being overwritten
- FIXED: Username attribution (was showing "unknown")
- NEW: Automatic log trimming (activity: 100, system: 50)
- NEW: Rebalance log trimming (20 per profile)
- NEW: Empty profile cleanup to reduce database size
- NEW: Database size optimization (~60K → ~40K characters)
- Impact: Saves now succeed (below 50K limit) ✅
- Impact: All users preserved during merge ✅
- Impact: Proper save attribution ✅
- Impact: Sustainable database growth ✅
- Note: Existing data automatically cleaned on first save

v7.2.0 (2026-01-30 02:45 EST) - 🔒 MULTI-USER SAFE (CRITICAL UPDATE)
- CRITICAL: Implemented optimistic locking with version tracking
- FIXED: Multiple sessions overwriting each other's data (DATA LOSS BUG)
- NEW: Version-based conflict detection prevents data overwrites
- NEW: Smart merge logic automatically resolves conflicts
- NEW: Audit trail tracks all database changes
- NEW: Session staleness detection (auto-reload after 5 minutes)
- NEW: Detailed conflict warnings with retry logic
- Impact: 100% multi-user safe - no more data loss! ✅
- Impact: Multiple admins can work simultaneously safely ✅
- Impact: All changes tracked with timestamps and user attribution ✅
- Note: Automatic migration adds version metadata to existing data

v7.1.0 (2026-01-27 11:08 EST) - 🎉 PRODUCTION RELEASE
- RELEASE: Production-ready Google Sheets persistent storage
- REMOVED: All debug logging messages for clean UI
- KEPT: All functionality from v7.0.4 (working Google Sheets save)
- KEPT: Critical fix using update_acell() for proper API calls
- Impact: Professional, clean interface with persistent storage ✅
- Status: Fully tested and confirmed working in production
- Note: Data persistence verified and working perfectly

v7.0.4 (2026-01-27 10:51 EST) - 🔧 CRITICAL FIX: Google Sheets Save Error
- FIXED: Error 400 (Bad Request) when saving to Google Sheets
- FIXED: Changed worksheet.update() to worksheet.update_acell()
- Impact: Data now saves correctly to Google Sheets ✅

v7.0.3-debug (2026-01-27 09:54 EST) - 🔍 DIAGNOSTIC BUILD
- ADDED: Comprehensive debug logging to save_db() function
- ADDED: Detailed step-by-step logging in save_to_google_sheets()
- ADDED: Visibility into STORAGE_TYPE and GOOGLE_SHEETS_URL values
- Purpose: Diagnose why data is not being saved to Google Sheets
- Note: This is a temporary diagnostic version with verbose logging

v7.0.2 (2026-01-26 22:31 EST) - 🔧 CRITICAL FIX: Shared Sheet Support
- FIXED: Service account can now access shared sheets via URL
- NEW: Added GOOGLE_SHEETS_URL configuration option
- NEW: Better error messages for storage quota issues
- Changed: Now tries to open by URL first, then by name
- Impact: Works with sheets in user's Drive (no service account storage needed)
- Note: Add GOOGLE_SHEETS_URL to Streamlit Secrets to use existing shared sheet

v7.0.1 (2026-01-26 22:06 EST) - 🔧 CRITICAL HOTFIX
- FIXED: UnboundLocalError in load_db() function
- FIXED: Added global STORAGE_TYPE declaration in load_db()
- FIXED: Added global STORAGE_TYPE declaration in save_db()
- Impact: App now loads correctly with Google Sheets storage
- Note: Critical bug fix for v7.0.0 deployment issues

v7.0.0 (2026-01-26 20:52 EST) - 🚀 GOOGLE SHEETS STORAGE (MAJOR RELEASE)
- MAJOR: Added Google Sheets as persistent storage option
- MAJOR: Data now survives app redeployments when using Google Sheets
- NEW: Configurable storage backend (JSON or Google Sheets)
- NEW: Automatic migration from JSON to Google Sheets on first run
- NEW: Row-based storage structure for efficient querying
- NEW: Automatic retry logic with exponential backoff
- NEW: Comprehensive error handling for API failures
- Changed: STORAGE_TYPE environment variable controls storage backend
- Changed: Backward compatible - defaults to JSON if not configured
- Impact: Zero data loss on Streamlit Cloud redeployments! ✅
- Impact: Automatic backups via Google's infrastructure ✅
- Impact: Version history and point-in-time recovery ✅
- Note: Core app logic unchanged - only storage layer modified
- Note: Setup guide included in documentation

v6.7.33 (2026-01-26 09:13 EST) - COLOR-CODED TABLES
- NEW: Color-coded "Risk Metrics by Account" table
  - Volatility: Green (low) → Yellow → Red (high)
  - Max Drawdown: Green (small) → Yellow → Red (large)
  - Sharpe Ratio: Green (high) → Yellow → Red (low)
- NEW: Color-coded "Portfolio Comparison Table"
  - CAGR/ROI: Green (high) → Yellow → Red (low/negative)
  - Deployed %: Green (100%) → Yellow (75%+) → Orange (partial)
  - Status: Green (Balanced) → Red (Rebalance) → Blue (Deploying) → Gray (New)
- Impact: Much easier to spot good/bad performers at a glance
- Impact: Visual hierarchy helps identify portfolios needing attention

v6.7.32 (2026-01-25 20:19 EST) - QUICK ADD SAVE BUTTON FIX (v3)
- CRITICAL: Removed disabled logic entirely from Save Asset button
- Changed: Button now always enabled after ticker validation
- Changed: Validation done on button click, not before
- Impact: Quick Add works immediately - no widget state sync issues
- Note: v6.7.28 and v6.7.30 approaches didn't work due to widget state

v6.7.31 (2026-01-25 10:58 EST) - GLOBAL SETTINGS FIX + NEW FEATURE
- CRITICAL: Fixed default drift tolerance not being applied to new profiles
- NEW: Added "Default Annual Growth Goal (%)" to global settings
- Changed: Profile creation now uses global defaults for drift tolerance and growth goal
- Changed: Global settings UI improved with two-column layout and help text
- Impact: Admin can now set defaults that actually apply to new profiles
- Impact: All new profiles will use admin-configured defaults instead of hardcoded values

v6.7.30 (2026-01-25 10:44 EST) - QUICK ADD SAVE BUTTON FIX (v2)
- CRITICAL: Fixed Save Asset button staying disabled after Quick Add
- Changed: Removed complex flag logic (v6.7.28 didn't work)
- Changed: Button always enabled when ticker valid, validation done on click
- Impact: Quick Add now works reliably - click button, validation passes, save enabled
- Note: v6.7.28 fix was too complex and didn't work due to widget state issues

v6.7.29 (2026-01-25 10:37 EST) - REBALANCE STATUS FIX
- CRITICAL: Fixed false "Rebalance Needed" status in rebalance table
- Fixed: max_drift now uses current portfolio value (not principal)
- Changed: TOTAL row status now consistent with individual asset drifts
- Impact: ±0.05% drift with 5.0% tolerance now shows "✅ Balanced" not "⚠️ Rebalance Needed"
- Impact: Status accurately reflects actual drift vs tolerance

v6.7.28 (2026-01-25 10:30 EST) - QUICK ADD SAVE BUTTON FIX
- CRITICAL: Fixed Save Asset button not activating after Quick Add
- Changed: Quick Add now clears all widget states for clean slate
- Changed: Save button explicitly enabled after successful Quick Add validation
- Impact: Users no longer need to re-type ticker after Quick Add
- Impact: One-click workflow now works as intended (click → validate → save)

v6.7.27 (2026-01-25 10:16 EST) - TWO CRITICAL FIXES
- CRITICAL: Fixed dashboard message showing "deployment in progress" after rebalancing
- Fixed: -100% ROI bug for profiles with no deployments/current value
- Changed: Dashboard uses smart detection for deployment status
- Changed: Profiles with curr_val = 0 show as 0% not -100%
- Impact: "Balanced" profiles no longer show confusing deployment message
- Impact: SAT PROFILE and similar won't show -100% if not deployed

v6.7.26 (2026-01-24 23:39 EST) - FOUR CRITICAL FIXES
- CRITICAL: Fixed deployable assets filter (removed buggy fallback)
- Fixed: Dashboard counter now uses smart detection (shows 4/4 not 3/4)
- Fixed: Drift alert only shows AFTER deployment complete (not during)
- Fixed: Rebalance table shows "100%" when fractional remainder only
- Impact: GLD ($232 < $458) now properly excluded from dropdown
- Impact: All five status locations now 100% consistent
- Bug in v6.7.25: Fallback logic incorrectly included 99% assets in dropdown

v6.7.25 (2026-01-24 23:22 EST) - CRITICAL DEPLOYMENT FILTER FIX
- CRITICAL: Fixed deployable assets filter to use smart detection
- Fixed: Assets with fractional remainder excluded from "Select Asset" dropdown
- Fixed: Quick Add now properly populates ticker field (improved approach)
- Changed: Dropdown only shows assets that can still receive capital
- Impact: 100% deployed assets (SPXL, GLD) no longer appear in dropdown
- Impact: Deployment status correctly shows 4/4 when all fractional remainder
- Status: SPXL ($165 < $225.60) + GLD ($250 < $458) = both excluded ✅

v6.7.24 (2026-01-24 22:49 EST) - CRITICAL CONSISTENCY FIX
- CRITICAL: Fixed contradictory budget display when asset 100% deployed
- Fixed: Rebalance table now uses smart detection (remaining < price = 100%)
- Fixed: Progress counter uses smart detection for accurate count
- Changed: Hide "Can Deploy Now" message when asset fully deployed (fractional only)
- Impact: All three displays now consistent (Deployment, Table, Progress)
- Example: SPXL with $176 remaining @ $225/unit shows "100% Deployed" everywhere
- Status: 4/4 assets deployed (not 3/4) when all have fractional remainder

v6.7.23 (2026-01-24 22:35 EST)
- Fixed: Quick Add buttons now properly populate ticker field
- Changed: Quick Add buttons to user's assets (SPXL, GLD, DBMF, BIL)
- Added: Visual step-by-step progress tracker in sidebar
- Enhanced: Shows checkmarks for completed steps and hints for next action
- Fixed: Deploy All Remaining Cash shows ALL assets (not just 3)
- Impact: Clearer guidance through setup process, Quick Add now works
- UX: Progress bar shows 0-6 steps complete with color coding

v6.7.22 (2026-01-24 22:21 EST)
- CRITICAL: Fixed progress bar to show continuous deployment (not just fully deployed count)
- Fixed: Today button now properly updates date field by clearing widget cache
- Enhanced: Progress bar now shows "X/Y assets deployed • Z% capital deployed"
- Changed: Progress bar color based on capital deployed percentage
- Impact: Progress updates immediately after each deployment (was stuck at 0/2)
- Impact: Today button now reliably resets date to current date
- Note: Profile dropdown already worked correctly (auto-selects new profiles)

v6.7.21 (2026-01-24 22:05 EST)
- MAJOR: Implemented strict per-asset budget deployment (user's smart logic)
- Changed: Reverted from flexible to per-asset budget constraints
- Logic: Each asset has dedicated budget envelope (can't borrow from other assets)
- Enhanced: Smart "100% deployed" detection when remaining < asset price
- Fixed: Active profile defaults to newly created profile
- Philosophy: Maintain target allocations during deployment, not after
- Impact: More intuitive, matches real-world investment approach
- Example: SPXL budget $50k, remaining $63, price $212 → can't buy 1 → 100% deployed

v6.7.20 (2026-01-24 17:35 EST) - CRITICAL HOTFIX
- CRITICAL: Fixed Portfolio % in rebalance table showing 144.78% total (impossible!)
- CRITICAL: Fixed Portfolio % calculation to use CURRENT portfolio value, not principal
- Fixed: Rebalance table now correctly shows Portfolio % summing to 100%
- Fixed: Drift calculations now accurate for portfolios with gains/losses
- Logic: During deployment uses principal, after deployment uses market value
- Impact: Rebalance table now works correctly for portfolios with market gains
- Example: Portfolio with 44.78% gain now shows correct 50/50 split, not 72/72

v6.7.19 (2026-01-24 17:22 EST)
- MAJOR: Implemented flexible deployment - use ALL undeployed cash for any asset
- Changed: Removed per-asset budget constraint that limited deployment
- Enhanced: Can now exceed target allocation to maximize deployment
- Enhanced: 100% deployment = when remaining cash is fractional only (can't buy any asset)
- Added: Over-target warnings but allows deployment anyway
- Added: Clear messaging about flexible deployment philosophy
- Logic: Prioritizes getting money invested over strict target adherence
- Impact: No more stuck with undeployed cash due to artificial constraints
- Example: $438 undeployed can now buy $414.47 GLD share even if over target

v6.7.18 (2026-01-24 17:11 EST)
- CRITICAL: Fixed "Today" button not updating deployment date field
- Enhanced: Added clear budget breakdown showing target vs total portfolio cash
- Enhanced: Visual metrics for budget allocation (per-asset vs portfolio)
- Enhanced: Better warning when budget insufficient for 1 unit (with actionable steps)
- Added: Explanation of why available budget differs from total portfolio cash
- Added: Guidance on what to do with fractional budget remainder
- UX: Two-column budget display shows allocation constraints clearly
- Impact: No more confusion about budget allocation logic

v6.7.17 (2026-01-24 16:55 EST) - HOTFIX
- CRITICAL: Fixed NameError in debug section - total_allocation not defined
- Fixed: Moved variable calculation before use in troubleshooting panel
- Impact: Debug section now works correctly without crashes

v6.7.16 (2026-01-24 16:48 EST)
- CRITICAL: Fixed asset allocation workflow after deployment
- Enhanced: Ticker validation now shows loading state and timeout handling
- Enhanced: Existing assets prominently displayed with edit capability
- Added: Timeout handling for Yahoo Finance API (10 second limit)
- Added: Quick-add buttons for common tickers (SPY, QQQ, GLD, TLT)
- Fixed: Can now edit target % for existing assets even with deployments
- Fixed: Better error messages when ticker validation fails
- Added: "Show current state" debug info to help troubleshooting
- UX: Asset list shows deployment status more clearly
- Impact: No more getting stuck in asset allocation after deployment

v6.7.15 (2026-01-24 16:38 EST)
- CRITICAL: Fixed max units calculation using per-asset budget instead of total undeployed cash
- CRITICAL: Fixed "exceeds budget" validation showing backwards warning (negative = under budget)
- CRITICAL: Fixed deployed % calculation to always use actual spent vs current target
- Enhanced: Recalculate allocated_pct from purchases on every view (no stale data)
- Enhanced: Max units now respects BOTH per-asset target AND total undeployed cash
- Added: Deployment history events in Capital Overview sidebar
- Added: Clear indication of remaining budget per asset vs total portfolio
- Fixed: Validation now checks total portfolio cash before allowing deployment
- Impact: Accurate deployment tracking, no more confusing warnings

v6.7.14 (2026-01-24 16:23 EST)
- CRITICAL: Fixed "Actual %" column showing confusing 100% when portfolio partially deployed
- Changed: "Actual %" now calculates as % of PRINCIPAL instead of % of deployed capital
- Renamed: "Actual %" → "Portfolio %" for clarity
- Enhanced: Drift shows "⚠️ Deploying" status during deployment phase instead of misleading drift %
- Fixed: "Today" button in deployment date picker now correctly sets today's date
- UX: TOTAL row "Portfolio %" now matches deployment percentage (not always 100%)
- Impact: Much clearer understanding of true portfolio allocation

v6.7.13 (2026-01-23 16:48 EST)
- CRITICAL: Fixed 'actual_undeployed_cash' not defined error in Rebalance Analysis table
- Fixed: Calculate actual_undeployed_cash before using it in smart fractional detection
- Fixed: Error occurred when viewing Portfolio Manager with deployed assets
- Technical: Moved capital calculation to proper location in code flow
- Impact: Rebalance table now displays correctly for all users

v6.7.12 (2026-01-23 16:37 EST)
- CRITICAL: Fixed progress bar showing "1/2 deployed" when portfolio truly 100% deployed
- CRITICAL: Fixed table status showing "Deploying" when fractional remainder only
- Enhanced: Progress bar uses smart fractional detection (checks cheapest asset price)
- Enhanced: All assets show "✅ Deployed" when portfolio has only fractional remainder
- Fixed: Consistency between progress bar, table status, and info box messages
- Fixed: User case where SPXL at 99% showed "Deploying" despite no shares affordable
- UX: Progress shows "2/2 assets fully deployed" when truly complete
- UX: Success message includes fractional amount in progress section

v6.7.11 (2026-01-23 16:19 EST)
- CRITICAL: Smart fractional detection - checks if undeployed cash can buy cheapest asset
- CRITICAL: Fixed false "deployable" warnings when cash < cheapest share price
- Added: "Add More Capital" feature to inject additional funds into portfolio
- Enhanced: Shows green success when truly 100% deployed (fractional remainder only)
- Enhanced: Capital Overview shows "100% deployed" when can't afford any shares
- Enhanced: Info box now uses smart detection for accurate messages
- Fixed: User case where $216 undeployed but can't buy SPXL ($225) or GLD ($467)
- UX: Suggested capital amount to buy 1 more share of cheapest asset
- Feature: Track capital injections in activity log

v6.7.10 (2026-01-23 13:21 EST)
- Added: "Today" quick select button next to deployment calendar
- Enhanced: Two-column layout for date picker (calendar + Today button)
- UX: Click "Today" to instantly select current date without calendar navigation
- Improved: Faster deployment date selection for same-day purchases

v6.7.9 (2026-01-23 13:06 EST)
- CRITICAL: Added over-deployment prevention (can't deploy more than principal)
- CRITICAL: Fixed NaN error in rebalance table with comprehensive error handling
- Added: Pre-deployment validation checks total capital before allowing deployment
- Added: Over-deployment warning in Capital Overview (shows red alert)
- Added: Validation prevents exceeding asset target budgets
- Fixed: All table calculations now protected against NaN/infinite values
- Fixed: Deploy All Remaining respects principal limit
- Enhanced: Clear error messages explain what went wrong and how to fix
- Protection: Multiple validation layers prevent invalid portfolio states

v6.7.8 (2026-01-23 12:52 EST)
- Added: "Deploy All Remaining Cash" auto-deployment button
- Added: Smart analysis distinguishing deployable cash vs fractional remainder
- Added: Deployment opportunities showing exactly what you can buy
- Enhanced: Capital Overview shows which assets can still be deployed to
- Enhanced: Info box warns if you have deployable cash (not just fractional)
- Removed: Confusing per-asset "Undeployed $" column from table
- Fixed: Now correctly identifies when portfolio is truly fully deployed vs partially deployed
- User Experience: Clear guidance on deploying remaining capital with one click

v6.7.7 (2026-01-23 12:31 EST)
- Fixed: Undeployed cash now consistent across sidebar, table, and info box
- Fixed: Info box example now uses actual portfolio data (not hardcoded $5,000)
- Fixed: Example shows real asset prices and target amounts
- Enhanced: Dynamic calculation shows why YOUR specific portfolio has undeployed cash
- Technical: Uses actual deployed capital (sum of purchases) for all calculations

v6.7.6 (2026-01-23 18:00)
- Added: "Capital Overview" section in sidebar showing Principal, Deployed, and Undeployed cash
- Added: "Undeployed $" column in Rebalance Analysis table
- Added: Info box explaining why 100% deployment is impossible (can't buy fractional shares)
- Enhanced: Clear visibility of cash drag and deployment efficiency
- Insight: Shows exact $ amount that couldn't be deployed per asset

v6.7.5 (2026-01-23 07:00)
- Fixed: User registration now visible in Admin Dashboard → Activity & Logs
- Fixed: User login now visible in Admin Dashboard → Activity Timeline
- Added: Failed login attempts logged to activity feed
- Added: Account lockouts visible to admin
- Enhanced: Admin can now see all user activity (registrations, logins, failures)

v6.7.4 (2026-01-23 06:00)
- Fixed: AUM calculation now uses current market prices (not purchase prices)
- Fixed: Avg Portfolio Value calculation corrected
- Added: Activity Timeline chart showing activities by date (last 14 days)
- Added: Activity Types breakdown with top 5 types
- Added: Recent Activity feed with last 10 activities
- Enhanced: System Analytics now shows real-time accurate values

v6.7.3 (2026-01-23 05:00)
- Fixed: Renamed "Phase A/C" to "Step 1/2" for two-step workflow clarity
- Fixed: TOTAL row Status now shows drift status instead of confusing deployment %
- Enhanced: Status shows "⚠️ Rebalance Needed", "🟡 Monitor", or "✅ Balanced"
- Fixed: Eliminated conflicting deployment information (94% vs 100%)

v6.7.2 (2026-01-23 04:15)
- Enhanced: Profile creation now guides users to next step
- Added: Auto-select newly created profile
- Added: Clear instructions after profile creation
- Added: Visual navigation hint with styled box
- Added: Activity logging for profile creation

v6.7.1 (2026-01-22 22:30)
- Added: First-time user welcome experience with beautiful onboarding
- Restored: Full user management controls (Reset Password, Activate/Deactivate, Delete)
- Added: Status badges for active/inactive users
- Added: Delete confirmation for safety
- Enhanced: Activity logging for all admin actions

v6.7.0 (2026-01-22 19:15)
- Added: 5-tab admin dashboard (Overview, Activity & Logs, Analytics, System, Security)
- Added: Activity logging system
- Added: Security monitoring and failed login tracking
- Added: System analytics and health dashboard
- Added: Backup/restore functionality
- Added: Notification tracking
"""

# ===== CONFIGURATION =====
st.set_page_config(
    page_title="Long Term Strategy Optimizer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== PREMIUM STYLING =====
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
    }
    
    .premium-card {
        background: white;
        padding: 28px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 24px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .desc-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 10px 15px -3px rgba(102, 126, 234, 0.4);
    }
    
    .desc-box h4 {
        margin-top: 0;
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    .profile-tile {
        background: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
    }
    
    .profile-tile:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
        border-color: #3b82f6;
    }
    
    .profile-tile-optimized {
        border-left: 4px solid #10b981;
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .profile-tile-optimized:hover {
        box-shadow: 0 8px 16px rgba(16, 185, 129, 0.2);
        transform: translateY(-2px);
    }
    
    .profile-tile-warning {
        border-left: 4px solid #ef4444;
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        animation: pulse-border 2s infinite;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .profile-tile-warning:hover {
        box-shadow: 0 8px 16px rgba(239, 68, 68, 0.2);
        transform: translateY(-2px);
    }
    
    @keyframes pulse-border {
        0%, 100% { 
            border-left-color: #f97316;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }
        50% { 
            border-left-color: #ef4444;
            box-shadow: 0 4px 8px rgba(239, 68, 68, 0.3);
        }
    }
    
    .drift-badge {
        display: inline-block;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        animation: pulse-badge 1.5s infinite;
        box-shadow: 0 4px 6px rgba(239, 68, 68, 0.4);
    }
    
    @keyframes pulse-badge {
        0%, 100% { 
            opacity: 1; 
            transform: scale(1);
            box-shadow: 0 4px 6px rgba(239, 68, 68, 0.4);
        }
        50% { 
            opacity: 0.7; 
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(239, 68, 68, 0.6);
        }
    }
    
    .success-badge {
        display: inline-block;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
    }
    
    .metric-showcase {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.4);
    }
    
    .metric-showcase h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .metric-showcase p {
        margin: 8px 0 0 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .stat-item {
        background: white;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 8px;
        word-wrap: break-word;
    }
    
    .allocation-blocked {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 3px solid #ef4444;
        padding: 20px;
        border-radius: 12px;
        margin: 16px 0;
        text-align: center;
        font-weight: 700;
        color: #991b1b;
        font-size: 1.1rem;
        animation: shake 0.5s;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .buying-guide {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 12px 0;
        font-weight: 600;
        color: #1e40af;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    .buying-guide-highlight {
        background: #1e40af;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 1rem;
        display: inline-block;
        margin: 0 2px;
    }
    
    .neutral-state {
        text-align: center;
        padding: 60px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        color: white;
    }
    
    .neutral-state h2 {
        color: white;
        margin-bottom: 20px;
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 3px solid #f59e0b;
        padding: 20px;
        border-radius: 12px;
        margin: 16px 0;
    }
    
    .recommendation-box h3 {
        color: #92400e;
        margin-top: 0;
    }
    
    h1, h2, h3 {
        font-weight: 600;
        color: #1e293b;
    }
    
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-bottom: 8px;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .profile-tile-header {
        background: linear-gradient(135deg, #475569 0%, #334155 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        margin: -24px -24px 16px -24px;
        font-weight: 600;
        font-size: 1.1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Authentication Styling */
    .auth-container {
        max-width: 450px;
        margin: 40px auto;
        padding: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .user-badge {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .admin-badge {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .user-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }
    
    .user-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    
    /* New Admin Dashboard Styles */
    .impersonate-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        animation: pulse-impersonate 2s infinite;
        box-shadow: 0 4px 6px rgba(245, 158, 11, 0.4);
    }
    
    @keyframes pulse-impersonate {
        0%, 100% { 
            opacity: 1; 
            transform: scale(1);
        }
        50% { 
            opacity: 0.8; 
            transform: scale(1.02);
        }
    }
    
    .warning-banner {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 16px 20px;
        border-radius: 8px;
        margin: 16px 0;
    }
    
    .warning-banner h4 {
        color: #92400e;
        margin: 0 0 8px 0;
        font-size: 1rem;
    }
    
    .status-needs-action {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-balanced {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-empty {
        background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
        color: #374151;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .user-info-card {
        background: white;
        border-radius: 10px;
        padding: 16px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
    }
    
        </style>
""", unsafe_allow_html=True)

# ===== AUTHENTICATION SYSTEM =====
# ===== AUTHENTICATION SYSTEM =====

# Password Security Configuration
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGIT = True
PASSWORD_REQUIRE_SPECIAL = False
SESSION_TIMEOUT_HOURS = 24
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15

def hash_password(password: str, salt: str = None) -> tuple:
    """Hash password using SHA-256 with salt."""
    if salt is None:
        salt = secrets.token_hex(32)
    salted_password = f"{password}{salt}"
    hashed = hashlib.sha256(salted_password.encode()).hexdigest()
    return hashed, salt

def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verify password against stored hash"""
    computed_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(computed_hash, stored_hash)

def validate_password_strength(password: str) -> tuple:
    """Validate password meets security requirements."""
    errors = []
    if len(password) < PASSWORD_MIN_LENGTH:
        errors.append(f"Password must be at least {PASSWORD_MIN_LENGTH} characters")
    if PASSWORD_REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    if PASSWORD_REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    if PASSWORD_REQUIRE_DIGIT and not re.search(r'\d', password):
        errors.append("Password must contain at least one digit")
    if errors:
        return False, errors
    return True, []

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_session_token() -> str:
    """Generate a secure session token"""
    return secrets.token_urlsafe(32)

def enhanced_date_input(label: str, value=None, min_value=None, max_value=None, key=None, help=None):
    """
    Enhanced date input with Today and Clear buttons displayed below the date picker.
    
    This creates a layout with:
    - Date picker field (full width)
    - Clear button (left) | Today button (right) below it
    
    Returns: selected date or None (if cleared)
    """
    # Use a state variable to track the current value
    state_key = f"{key}_value" if key else "date_value_temp"
    
    # Initialize state if needed
    if state_key not in st.session_state:
        st.session_state[state_key] = value if value is not None else date.today()
    
    # Main date input field
    selected_date = st.date_input(
        label,
        value=st.session_state[state_key],
        min_value=min_value,
        max_value=max_value,
        key=f"{key}_input" if key else None,
        help=help
    )
    
    # Update state when date changes
    if selected_date != st.session_state[state_key]:
        st.session_state[state_key] = selected_date
    
    # Buttons row: Clear (left) and Today (right)
    col_clear, col_today = st.columns(2)
    
    with col_clear:
        if st.button("🗑️ Clear", key=f"{key}_clear" if key else None, use_container_width=True):
            # Set to None - caller should handle this
            st.session_state[state_key] = None
            st.rerun()
    
    with col_today:
        if st.button("📅 Today", key=f"{key}_today" if key else None, use_container_width=True):
            st.session_state[state_key] = date.today()
            st.rerun()
    
    return st.session_state[state_key]

# ===== POSTGRESQL DATABASE CONFIGURATION =====

# Connection pool for PostgreSQL (reuses connections for better performance)
connection_pool = None

def get_db_connection():
    """Get PostgreSQL connection from pool using st.secrets"""
    global connection_pool
    
    try:
        # Initialize connection pool if not exists
        if connection_pool is None:
            connection_pool = psycopg2.pool.SimpleConnectionPool(
                1,  # Minimum connections
                10,  # Maximum connections
                host=st.secrets["postgres"]["host"],
                database=st.secrets["postgres"]["dbname"],
                user=st.secrets["postgres"]["user"],
                password=st.secrets["postgres"]["password"],
                port=st.secrets["postgres"]["port"]
            )
        
        # Get connection from pool
        conn = connection_pool.getconn()
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

def release_db_connection(conn):
    """Return connection to pool"""
    global connection_pool
    if connection_pool and conn:
        connection_pool.putconn(conn)

def init_db():
    """Initialize PostgreSQL database with required schema"""
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Create main database table with PostgreSQL syntax
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS database_store (
                id SERIAL PRIMARY KEY,
                data_json TEXT NOT NULL,
                version INTEGER NOT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cursor.close()
    except Exception as e:
        st.error(f"Error initializing database: {e}")
        conn.rollback()
    finally:
        release_db_connection(conn)

def load_from_postgres():
    """Load database from PostgreSQL"""
    try:
        conn = get_db_connection()
        if not conn:
            return None, 0
        
        cursor = conn.cursor()
        
        # Use %s placeholder instead of ? for PostgreSQL
        cursor.execute("SELECT data_json, version FROM database_store WHERE id = 1")
        row = cursor.fetchone()
        
        cursor.close()
        release_db_connection(conn)
        
        if row:
            data = json.loads(row[0])
            version = row[1]
            return data, version
        return None, 0
    except Exception as e:
        st.error(f"Error loading from PostgreSQL: {e}")
        return None, 0

def save_to_postgres(data, version):
    """Save database to PostgreSQL"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        data_json = json.dumps(data, indent=2)
        
        # Use INSERT ... ON CONFLICT for PostgreSQL (equivalent to INSERT OR REPLACE)
        cursor.execute("""
            INSERT INTO database_store (id, data_json, version, last_updated)
            VALUES (1, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (id) DO UPDATE SET
                data_json = EXCLUDED.data_json,
                version = EXCLUDED.version,
                last_updated = CURRENT_TIMESTAMP
        """, (data_json, version))
        
        conn.commit()
        cursor.close()
        release_db_connection(conn)
        return True
    except Exception as e:
        st.error(f"Error saving to PostgreSQL: {e}")
        if conn:
            conn.rollback()
            release_db_connection(conn)
        return False


def load_db():
    """Load multi-user database from PostgreSQL"""
    # Initialize database if needed
    init_db()
    
    base_schema = {
        "metadata": {
            "version": 0,
            "last_save_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_save_by": "system",
            "save_count": 0
        },
        "users": {},
        "global_settings": {
            "allow_registration": True,
            "require_email_verification": False,
            "default_drift_tolerance": 5.0,
            "default_growth_goal": 10.0,
            "ai_assistant_enabled": True,
            "ai_assistant_api_key": "",
            "email_notifications_enabled": False,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "smtp_username": "",
            "smtp_password": "",
            "smtp_from_name": "AlphaStream Portfolio"
        },
        "system_logs": []
    }
    
    # Try to load from PostgreSQL
    data, version = load_from_postgres()
    
    if data:
        # Store version in session for conflict detection
        st.session_state["data_version"] = version
        st.session_state["data_loaded_at"] = datetime.now()
        
        # Ensure schema integrity
        data.setdefault("users", {})
        data.setdefault("global_settings", base_schema["global_settings"])
        data.setdefault("system_logs", [])
        data.setdefault("metadata", base_schema["metadata"])
        
        # Update global settings with any new fields
        for key, value in base_schema["global_settings"].items():
            data["global_settings"].setdefault(key, value)
        
        # Ensure user data integrity
        for user_id, user_data in data["users"].items():
            user_data.setdefault("profiles", {})
            user_data.setdefault("settings", {})
            user_data.setdefault("created_at", "")
            user_data.setdefault("last_login", "")
            user_data.setdefault("role", "user")
            user_data.setdefault("is_active", True)
            user_data.setdefault("login_attempts", 0)
            user_data.setdefault("lockout_until", None)
            
            for p_name, p_data in user_data["profiles"].items():
                p_data.setdefault("drift_tolerance", 5.0)
                p_data.setdefault("rebalance_stats", [])
                p_data.setdefault("last_rebalanced", None)
                p_data.setdefault("benchmark", None)
                p_data.setdefault("benchmarks", [])
                p_data.setdefault("bank_name", "")
                p_data.setdefault("account_type", "")
                p_data.setdefault("account_name", "")
                p_data.setdefault("initialization_date", p_data.get("start_date", ""))
                p_data.setdefault("asset_mix_locked", False)
                
                for asset_key, asset_data in p_data.get("assets", {}).items():
                    asset_data.setdefault("fund_name", asset_key)
                    asset_data.setdefault("allocated_pct", 0.0)
                    asset_data.setdefault("purchases", [])
        
        return data
    
    # No existing database - check for old JSON files to migrate
    OLD_DB_FILE = "alphastream_wealth.json"
    NEW_JSON_DB = "alphastream_multiuser.json"
    
    # Try to migrate from old JSON files
    for json_file in [NEW_JSON_DB, OLD_DB_FILE]:
        if os.path.exists(json_file):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    migrated_data = json.load(f)
                
                # Migrate old single-user format if needed
                if "profiles" in migrated_data and "users" not in migrated_data:
                    old_profiles = migrated_data.get("profiles", {})
                    admin_hash, admin_salt = hash_password("admin123")
                    migrated_data = {
                        "users": {
                            "admin": {
                                "email": "admin@localhost",
                                "password_hash": admin_hash,
                                "password_salt": admin_salt,
                                "display_name": "Administrator",
                                "role": "admin",
                                "is_active": True,
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "last_login": "",
                                "login_attempts": 0,
                                "lockout_until": None,
                                "profiles": old_profiles,
                                "settings": {}
                            }
                        },
                        "global_settings": base_schema["global_settings"],
                        "system_logs": [],
                        "metadata": base_schema["metadata"]
                    }
                
                # Save to PostgreSQL
                migrated_data.setdefault("metadata", base_schema["metadata"])
                migrated_data["metadata"]["version"] = 1
                save_to_postgres(migrated_data, 1)
                st.success(f"✅ Migrated data from {json_file} to PostgreSQL")
                
                # Backup old file
                import shutil
                shutil.copy(json_file, f"{json_file}.backup")
                
                return migrated_data
            except Exception as e:
                st.warning(f"Could not migrate {json_file}: {e}")
    
    # No existing data - create new database with admin user
    admin_hash, admin_salt = hash_password("admin123")
    base_schema["users"]["admin"] = {
        "email": "admin@localhost",
        "password_hash": admin_hash,
        "password_salt": admin_salt,
        "display_name": "Administrator",
        "role": "admin",
        "is_active": True,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_login": "",
        "login_attempts": 0,
        "lockout_until": None,
        "profiles": {},
        "settings": {}
    }
    
    base_schema["metadata"]["version"] = 1
    save_to_postgres(base_schema, 1)
    return base_schema

def save_db(data, bypass_version_increment=False):
    """
    Save database to PostgreSQL with optimistic locking
    
    Args:
        data: Database dictionary to save
        bypass_version_increment: If True, uses data's existing version
    """
    try:
        # Get current version
        expected_version = st.session_state.get("data_version", 0)
        
        # Get current user
        current_user = (
            st.session_state.get("username") or 
            st.session_state.get("current_user") or 
            st.session_state.get("user") or 
            "system"
        )
        
        # Load current data from database
        current_data, current_version = load_from_postgres()
        
        # Determine new version
        if bypass_version_increment:
            new_version = data.get("metadata", {}).get("version", 1)
        else:
            new_version = current_version + 1
        
        # Update metadata
        data["metadata"]["version"] = new_version
        data["metadata"]["last_save_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["metadata"]["last_save_by"] = current_user
        data["metadata"]["save_count"] = data["metadata"].get("save_count", 0) + 1
        
        # Save to PostgreSQL
        if save_to_postgres(data, new_version):
            st.session_state["data_version"] = new_version
            st.session_state["data_loaded_at"] = datetime.now()
            return True
        return False
    except Exception as e:
        st.error(f"Error saving database: {e}")
        return False


def merge_data_changes(base_data, user_changes, current_user):
    """
    Intelligently merge user changes with current database state
    v7.2.1: CRITICAL FIX - Now preserves ALL users from both sources
    """
    import copy
    merged = copy.deepcopy(base_data)
    
    # CRITICAL FIX (v7.2.1): Start with ALL users from base_data
    merged['users'] = copy.deepcopy(base_data.get('users', {}))
    
    # Then add/merge users from user_changes
    for username, user_data in user_changes.get('users', {}).items():
        if username not in merged['users']:
            # New user - add completely
            merged['users'][username] = copy.deepcopy(user_data)
        else:
            # Existing user - merge profiles and update metadata
            existing_user = merged['users'][username]
            
            # Merge profiles (add new ones, preserve existing)
            for profile_name, profile_data in user_data.get('profiles', {}).items():
                if profile_name not in existing_user.get('profiles', {}):
                    # New profile - safe to add
                    existing_user.setdefault('profiles', {})[profile_name] = copy.deepcopy(profile_data)
                else:
                    # Existing profile - prefer newer data or merge
                    # For now, keep base version to avoid conflicts
                    pass
            
            # Update last_login if newer
            if user_data.get('last_login', '') > existing_user.get('last_login', ''):
                existing_user['last_login'] = user_data['last_login']
    
    # Merge global settings - prefer user changes
    if 'global_settings' in user_changes:
        merged['global_settings'].update(user_changes['global_settings'])
    
    # Merge activity logs - combine both, then trim
    if 'activity_logs' in user_changes:
        merged_activity = list(merged.get('activity_logs', []))
        # Add new logs from user_changes
        for log in user_changes.get('activity_logs', []):
            if log not in merged_activity:
                merged_activity.insert(0, log)
        merged['activity_logs'] = merged_activity[:100]  # Keep only 100 most recent
    
    # Merge system logs - combine both, then trim
    if 'system_logs' in user_changes:
        merged_system = list(merged.get('system_logs', []))
        # Add new logs from user_changes
        for log in user_changes.get('system_logs', []):
            if log not in merged_system:
                merged_system.insert(0, log)
        merged['system_logs'] = merged_system[:50]  # Keep only 50 most recent
    
    # Add merge notification to logs
    merged.setdefault('system_logs', []).insert(0, {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'type': 'conflict_resolution',
        'message': f'Data merged automatically due to concurrent changes by {current_user}',
        'user_id': current_user
    })
    
    return merged


def log_system_event(db, event_type: str, message: str, user_id: str = None):
    """Log system-wide events"""
    db.setdefault("system_logs", [])
    db["system_logs"].insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": event_type,
        "message": message,
        "user_id": user_id
    })
    db["system_logs"] = db["system_logs"][:500]

def log_profile(prof, message):
    """Log profile-specific events"""
    prof.setdefault("rebalance_logs", [])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    prof["rebalance_logs"].insert(0, {"date": timestamp, "event": str(message)})
    prof["rebalance_logs"] = prof["rebalance_logs"][:50]

# ===== ADMIN SUITE HELPER FUNCTIONS =====

def log_activity(db, username: str, action: str, details: str = "", ip_address: str = ""):
    """Log user activity for audit trail"""
    db.setdefault("activity_logs", [])
    db["activity_logs"].insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "action": action,
        "details": details,
        "ip_address": ip_address
    })
    db["activity_logs"] = db["activity_logs"][:1000]

def log_notification(db, username: str, notification_type: str, subject: str, status: str, details: str = ""):
    """Log email notifications sent"""
    db.setdefault("notification_history", [])
    db["notification_history"].insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "type": notification_type,
        "subject": subject,
        "status": status,
        "details": details
    })
    db["notification_history"] = db["notification_history"][:500]

def log_failed_login(db, username: str, ip_address: str = ""):
    """Log failed login attempts"""
    db.setdefault("security_logs", [])
    db["security_logs"].insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": "failed_login",
        "username": username,
        "ip_address": ip_address,
        "severity": "warning"
    })
    db["security_logs"] = db["security_logs"][:500]

def log_security_event(db, event_type: str, username: str, details: str, severity: str = "info"):
    """Log security events"""
    db.setdefault("security_logs", [])
    db["security_logs"].insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "username": username,
        "details": details,
        "severity": severity
    })
    db["security_logs"] = db["security_logs"][:500]

def get_analytics_data(db):
    """Calculate system-wide analytics"""
    users = db.get("users", {})
    
    total_users = len([u for u in users.values() if u.get("role") != "admin"])
    total_portfolios = sum(len(u.get("profiles", {})) for u in users.values() if u.get("role") != "admin")
    
    # Calculate total AUM using current market prices
    total_aum = 0
    all_tickers = set()
    portfolio_values = []
    
    # Collect all tickers first
    for user_data in users.values():
        if user_data.get("role") == "admin":
            continue
        profiles = user_data.get("profiles", {})
        for profile_data in profiles.values():
            assets = profile_data.get("assets", {})
            all_tickers.update(assets.keys())
    
    # Fetch current prices for all tickers
    current_prices = {}
    if all_tickers:
        try:
            import yfinance as yf
            data = yf.download(list(all_tickers), period="1d", progress=False)['Close']
            if len(all_tickers) == 1:
                ticker = list(all_tickers)[0]
                if not data.empty:
                    current_prices[ticker] = float(data.iloc[-1])
            else:
                for ticker in all_tickers:
                    try:
                        if ticker in data.columns and not data[ticker].empty:
                            current_prices[ticker] = float(data[ticker].iloc[-1])
                    except:
                        pass
        except:
            pass
    
    # Calculate AUM and portfolio values
    for user_data in users.values():
        if user_data.get("role") == "admin":
            continue
        profiles = user_data.get("profiles", {})
        for profile_data in profiles.values():
            assets = profile_data.get("assets", {})
            portfolio_value = 0
            for ticker, asset_data in assets.items():
                units = float(asset_data.get("units", 0))
                price = current_prices.get(ticker, 0)
                portfolio_value += units * price
            
            if portfolio_value > 0:
                portfolio_values.append(portfolio_value)
                total_aum += portfolio_value
    
    # Count asset popularity
    asset_counts = {}
    for user_data in users.values():
        if user_data.get("role") == "admin":
            continue
        profiles = user_data.get("profiles", {})
        for profile_data in profiles.values():
            assets = profile_data.get("assets", {})
            for ticker in assets.keys():
                asset_counts[ticker] = asset_counts.get(ticker, 0) + 1
    
    top_assets = sorted(asset_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Activity metrics
    activity_logs = db.get("activity_logs", [])
    today = datetime.now().strftime("%Y-%m-%d")
    recent_activities = len([log for log in activity_logs if log.get("timestamp", "")[:10] == today])
    
    # Calculate average portfolio value
    avg_portfolio_value = total_aum / len(portfolio_values) if portfolio_values else 0
    
    return {
        "total_users": total_users,
        "total_portfolios": total_portfolios,
        "total_aum": total_aum,
        "avg_portfolio_value": avg_portfolio_value,
        "top_assets": top_assets,
        "recent_activities": recent_activities,
        "total_activities": len(activity_logs),
        "activity_logs": activity_logs
    }

def get_system_health(db):
    """Check system health metrics"""
    health = {"status": "healthy", "checks": []}
    
    # Database connection check
    try:
        # Check PostgreSQL connection
        conn = get_db_connection()
        if conn:
            # Get database size from PostgreSQL
            cursor = conn.cursor()
            cursor.execute("SELECT pg_database_size(current_database())")
            db_size_bytes = cursor.fetchone()[0]
            db_size_mb = db_size_bytes / (1024 * 1024)
            cursor.close()
            release_db_connection(conn)
            
            health["checks"].append({
                "name": "Database Size",
                "value": f"{db_size_mb:.2f} MB",
                "status": "warning" if db_size_mb > 50 else "healthy",
                "icon": "🟡" if db_size_mb > 50 else "🟢"
            })
        else:
            health["checks"].append({
                "name": "Database Connection",
                "value": "Unable to connect to PostgreSQL",
                "status": "critical",
                "icon": "🔴"
            })
    except Exception as e:
        health["checks"].append({
            "name": "Database Size",
            "value": f"Error: {str(e)[:50]}",
            "status": "warning",
            "icon": "🟡"
        })
    
    users = db.get("users", {})
    health["checks"].append({
        "name": "Total Users",
        "value": str(len(users)),
        "status": "healthy",
        "icon": "🟢"
    })
    
    system_logs = db.get("system_logs", [])
    recent_errors = len([log for log in system_logs[:100] if log.get("type") == "error"])
    health["checks"].append({
        "name": "Recent Errors",
        "value": f"{recent_errors}/100 logs",
        "status": "warning" if recent_errors > 10 else "healthy",
        "icon": "🟡" if recent_errors > 10 else "🟢"
    })
    
    settings = db.get("global_settings", {})
    email_configured = settings.get("email_notifications_enabled") and settings.get("smtp_username")
    health["checks"].append({
        "name": "Email Notifications",
        "value": "Configured" if email_configured else "Not Configured",
        "status": "healthy" if email_configured else "info",
        "icon": "🟢" if email_configured else "ℹ️"
    })
    
    if any(c["status"] == "error" for c in health["checks"]):
        health["status"] = "error"
    elif any(c["status"] == "warning" for c in health["checks"]):
        health["status"] = "warning"
    
    return health

def create_backup(db):
    """Create a backup of the database"""
    try:
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"backup_{timestamp}.json")
        
        with open(backup_file, "w") as f:
            json.dump(db, f, indent=2)
        
        log_system_event(db, "backup_created", f"Database backup created: {backup_file}", "admin")
        return True, f"Backup created: {backup_file}"
    except Exception as e:
        return False, f"Backup failed: {str(e)}"


def reset_database_to_fresh(admin_password: str, keep_admin: bool = True) -> tuple:
    """
    Reset database to fresh state (DANGEROUS!)
    v7.2.1: Added admin dashboard feature
    
    Args:
        admin_password: Admin password for confirmation
        keep_admin: If True, keeps admin account (recommended)
    
    Returns:
        (success: bool, message: str, new_db: dict or None)
    """
    try:
        # Load current database
        current_db = load_db()
        
        # Verify admin password
        admin_user = current_db.get('users', {}).get('admin')
        if not admin_user:
            return False, "Admin account not found", None
        
        if not verify_password(admin_password, admin_user['password_hash'], admin_user['password_salt']):
            return False, "Invalid admin password", None
        
        # Create fresh database structure
        fresh_db = {
            "metadata": {
                "version": 1,
                "last_save_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_save_by": "admin",
                "save_count": 1
            },
            "users": {},
            "global_settings": {
                "allow_registration": True,
                "require_email_verification": False,
                "default_drift_tolerance": 5.0,
                "default_growth_goal": 10.0,
                "ai_assistant_enabled": True,
                "ai_assistant_api_key": "",
                "email_notifications_enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "smtp_username": "",
                "smtp_password": "",
                "smtp_from_name": "AlphaStream Portfolio"
            },
            "system_logs": [],
            "activity_logs": [],
            "security_logs": []
        }
        
        # Keep admin account if requested
        if keep_admin and admin_user:
            # Reset admin account but keep credentials
            fresh_db['users']['admin'] = {
                'email': admin_user['email'],
                'password_hash': admin_user['password_hash'],
                'password_salt': admin_user['password_salt'],
                'display_name': admin_user.get('display_name', 'Administrator'),
                'role': 'admin',
                'is_active': True,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'last_login': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'login_attempts': 0,
                'lockout_until': None,
                'profiles': {},
                'settings': {}
            }
            
            # Log the reset
            fresh_db['system_logs'].append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'type': 'database_reset',
                'message': 'Database reset to fresh state (admin account preserved)',
                'user_id': 'admin'
            })
            
            fresh_db['activity_logs'].append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'username': 'admin',
                'action': 'database_reset',
                'details': 'Database reset to fresh state',
                'ip_address': ''
            })
        
        return True, "Database reset successful", fresh_db
        
    except Exception as e:
        return False, f"Reset failed: {str(e)}", None


def create_backup(db):
    """Create a backup of the database"""
    try:
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"backup_{timestamp}.json")
        
        with open(backup_file, "w") as f:
            json.dump(db, f, indent=2)
        
        log_system_event(db, "backup_created", f"Database backup created: {backup_file}", "admin")
        return True, f"Backup created: {backup_file}"
    except Exception as e:
        return False, f"Backup failed: {str(e)}"

def get_backup_list():
    """Get list of available backups"""
    try:
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            return []
        
        backups = []
        for filename in os.listdir(backup_dir):
            if filename.startswith("backup_") and filename.endswith(".json"):
                filepath = os.path.join(backup_dir, filename)
                size = os.path.getsize(filepath) / (1024 * 1024)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                backups.append({
                    "filename": filename,
                    "size": f"{size:.2f} MB",
                    "created": mtime.strftime("%Y-%m-%d %H:%M:%S"),
                    "path": filepath
                })
        
        return sorted(backups, key=lambda x: x["created"], reverse=True)
    except:
        return []

def check_account_lockout(user_data: dict) -> tuple:
    """Check if account is locked out."""
    lockout_until = user_data.get("lockout_until")
    if not lockout_until:
        return False, 0
    try:
        lockout_time = datetime.strptime(lockout_until, "%Y-%m-%d %H:%M:%S")
        if datetime.now() < lockout_time:
            remaining = (lockout_time - datetime.now()).total_seconds() / 60
            return True, int(remaining) + 1
        else:
            user_data["lockout_until"] = None
            user_data["login_attempts"] = 0
            return False, 0
    except:
        return False, 0

def register_user(db, username: str, email: str, password: str, display_name: str = None) -> tuple:
    """Register a new user."""
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters"
    if not username.isalnum():
        return False, "Username can only contain letters and numbers"
    username = username.lower()
    if username in db["users"]:
        return False, "Username already exists"
    if not validate_email(email):
        return False, "Invalid email format"
    for user in db["users"].values():
        if user.get("email", "").lower() == email.lower():
            return False, "Email already registered"
    is_valid, errors = validate_password_strength(password)
    if not is_valid:
        return False, "; ".join(errors)
    
    password_hash, password_salt = hash_password(password)
    db["users"][username] = {
        "email": email.lower(),
        "password_hash": password_hash,
        "password_salt": password_salt,
        "display_name": display_name or username.capitalize(),
        "role": "user",
        "is_active": True,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_login": "",
        "login_attempts": 0,
        "lockout_until": None,
        "profiles": {},
        "settings": {"default_currency": "USD", "default_drift_tolerance": 5.0}
    }
    
    # Log to both system_logs (security) and activity_logs (admin dashboard)
    log_system_event(db, "registration", f"New user registered: {username}", username)
    log_activity(db, username, "user_registered", f"New user account created: {email}")
    
    save_db(db)
    return True, "Registration successful! You can now log in."

def authenticate_user(db, username: str, password: str) -> tuple:
    """Authenticate user login."""
    username = username.lower()
    if username not in db["users"]:
        return False, "Invalid username or password", None
    user_data = db["users"][username]
    if not user_data.get("is_active", True):
        return False, "Account is deactivated. Contact administrator.", None
    is_locked, minutes = check_account_lockout(user_data)
    if is_locked:
        return False, f"Account locked. Try again in {minutes} minutes.", None
    
    if verify_password(password, user_data["password_hash"], user_data["password_salt"]):
        user_data["login_attempts"] = 0
        user_data["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log to both system_logs (security) and activity_logs (admin dashboard)
        log_system_event(db, "login", f"User logged in: {username}", username)
        log_activity(db, username, "user_login", f"User logged in successfully")
        
        save_db(db)
        return True, "Login successful", user_data
    else:
        user_data["login_attempts"] = user_data.get("login_attempts", 0) + 1
        
        # Log failed login attempt
        log_activity(db, username, "login_failed", f"Failed login attempt #{user_data['login_attempts']}")
        
        if user_data["login_attempts"] >= MAX_LOGIN_ATTEMPTS:
            lockout_time = datetime.now() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            user_data["lockout_until"] = lockout_time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Log to both system (security) and activity (admin dashboard)
            log_system_event(db, "lockout", f"Account locked: {username}", username)
            log_activity(db, username, "account_locked", f"Account locked after {MAX_LOGIN_ATTEMPTS} failed attempts")
        
        save_db(db)
        remaining = MAX_LOGIN_ATTEMPTS - user_data["login_attempts"]
        if remaining > 0:
            return False, f"Invalid password. {remaining} attempts remaining.", None
        else:
            return False, f"Account locked for {LOCKOUT_DURATION_MINUTES} minutes.", None

def change_password(db, username: str, old_password: str, new_password: str) -> tuple:
    """Change user password."""
    username = username.lower()
    if username not in db["users"]:
        return False, "User not found"
    user_data = db["users"][username]
    if not verify_password(old_password, user_data["password_hash"], user_data["password_salt"]):
        return False, "Current password is incorrect"
    is_valid, errors = validate_password_strength(new_password)
    if not is_valid:
        return False, "; ".join(errors)
    new_hash, new_salt = hash_password(new_password)
    user_data["password_hash"] = new_hash
    user_data["password_salt"] = new_salt
    log_system_event(db, "password_change", f"Password changed for: {username}", username)
    save_db(db)
    return True, "Password changed successfully"

def admin_reset_password(db, admin_username: str, target_username: str, new_password: str) -> tuple:
    """Admin function to reset user password."""
    target_username = target_username.lower()
    if db["users"].get(admin_username, {}).get("role") != "admin":
        return False, "Unauthorized: Admin privileges required"
    if target_username not in db["users"]:
        return False, "User not found"
    is_valid, errors = validate_password_strength(new_password)
    if not is_valid:
        return False, "; ".join(errors)
    new_hash, new_salt = hash_password(new_password)
    db["users"][target_username]["password_hash"] = new_hash
    db["users"][target_username]["password_salt"] = new_salt
    db["users"][target_username]["login_attempts"] = 0
    db["users"][target_username]["lockout_until"] = None
    log_system_event(db, "admin_password_reset", f"Admin reset password for: {target_username}", admin_username)
    save_db(db)
    return True, f"Password reset for {target_username}"

# ===== HELPER FUNCTIONS =====
def description_box(title, content):
    st.markdown(f'''
        <div class="desc-box">
            <h4>{title}</h4>
            <div style="line-height:1.7; font-weight: 300;">{content}</div>
        </div>
    ''', unsafe_allow_html=True)

def check_recently_rebalanced(last_rebalanced_str):
    """Check if portfolio was rebalanced in last 24 hours"""
    if not last_rebalanced_str:
        return False
    try:
        last_rebal_time = datetime.strptime(last_rebalanced_str, "%Y-%m-%d %H:%M:%S")
        hours_since = (datetime.now() - last_rebal_time).total_seconds() / 3600
        return hours_since < 24
    except:
        return False

def check_deployment_status(profile_data):
    """
    SINGLE SOURCE OF TRUTH for deployment status.
    
    Returns: (is_fully_deployed: bool, deployed_count: int, total_assets: int)
    
    Logic: An asset is considered deployed if:
    1. It's at 100% of its target allocation, OR
    2. Its remaining budget cannot buy 1 share (fractional remainder)
    """
    assets = profile_data.get("assets", {})
    if not assets:
        # No assets = Setup status, not deployed
        return False, 0, 0
    
    principal_amt = profile_data.get('principal', 0)
    total_assets = len(assets)
    deployed_count = 0
    
    # Fetch current prices for assets in this portfolio
    import yfinance as yf
    import pandas as pd
    
    prices = {}
    try:
        tickers = list(assets.keys())
        raw_px = yf.download(tickers, period="1d", progress=False)['Close']
        if len(tickers) == 1:
            if not raw_px.empty:
                prices = {tickers[0]: float(raw_px.iloc[-1])}
        else:
            for k, v in raw_px.iloc[-1].to_dict().items():
                try:
                    if pd.notna(v):
                        prices[k] = float(v)
                except:
                    pass
    except:
        pass
    
    for ticker, asset_data in assets.items():
        allocated_pct = asset_data.get("allocated_pct", 0)
        
        # Already at 100% of target
        if allocated_pct >= 100:
            deployed_count += 1
            continue
        
        # Check if remaining budget can buy at least 1 share
        target_pct = asset_data.get("target", 0)
        target_amount = (target_pct / 100) * principal_amt
        
        purchases = asset_data.get("purchases", [])
        deployed_amount = sum(p.get("amount", 0) for p in purchases)
        remaining_budget = target_amount - deployed_amount
        
        if remaining_budget > 0:
            # Get current price
            current_price = prices.get(ticker)
            if current_price is None:
                # If we can't get price, be conservative - assume not deployed
                continue
            
            # Can the remaining budget buy at least 1 share?
            if remaining_budget >= current_price:
                # Yes - this asset can still be deployed
                continue
            else:
                # No - fractional remainder, treat as deployed
                deployed_count += 1
        else:
            # No remaining budget (might be over-allocated)
            deployed_count += 1
    
    is_fully_deployed = (deployed_count == total_assets)
    return is_fully_deployed, deployed_count, total_assets

def calculate_average_cost(asset_data):
    """Calculate weighted average cost for an asset."""
    purchases = asset_data.get("purchases", [])
    if not purchases:
        return None
    total_invested = sum(p.get("amount", 0) for p in purchases)
    total_quantity = sum(p.get("quantity", 0) for p in purchases)
    if total_quantity == 0:
        return None
    return total_invested / total_quantity

def calculate_drift_status(p_data, prices):
    """Per-asset drift detection"""
    p_assets = p_data.get("assets", {})
    if not p_assets:
        return False, []
    curr_v = float(sum(p_assets[t]["units"] * prices.get(t, 0) for t in p_assets))
    if curr_v == 0:
        return False, []
    recently_rebalanced = check_recently_rebalanced(p_data.get("last_rebalanced"))
    if recently_rebalanced:
        return False, []
    drift_details = []
    for t in p_assets:
        allocated_pct = p_assets[t].get("allocated_pct", 0)
        cur_units = float(p_assets[t].get("units", 0))
        if allocated_pct == 0 and cur_units > 0:
            allocated_pct = 100.0
        if cur_units == 0:
            continue
        actual_pct = float((p_assets[t]["units"] * prices.get(t, 0) / curr_v * 100))
        target_pct = float(p_assets[t]["target"])
        drift = abs(actual_pct - target_pct)
        if drift >= p_data.get("drift_tolerance", 5.0):
            drift_details.append((t, drift, actual_pct, target_pct))
    return len(drift_details) > 0, drift_details

def validate_deployment_date(deploy_date, inception_date_str):
    """Validate deployment date constraints"""
    try:
        inception_date = datetime.strptime(inception_date_str, '%Y-%m-%d').date()
        if deploy_date < inception_date:
            return False, f"Deployment date cannot be before inception date ({inception_date})"
        if deploy_date > date.today():
            return False, "Deployment date cannot be in the future"
        return True, ""
    except:
        return False, "Invalid date format"

def store_rebalance_recommendation(prof, recommendations):
    """Store recommended rebalance trades for later execution"""
    prof["pending_rebalance"] = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "recommendations": recommendations
    }

def clear_rebalance_recommendation(prof):
    """Clear stored rebalance recommendation"""
    if "pending_rebalance" in prof:
        del prof["pending_rebalance"]

def get_time_ago(dt):
    """
    Calculate human-readable time ago from datetime
    v7.2.4: Added for enhanced activity logs
    """
    now = datetime.now()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes}m ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours}h ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days}d ago"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks}w ago"
    else:
        months = int(seconds / 2592000)
        return f"{months}mo ago"


def get_user_profiles(db, username):
    """Get profiles for a specific user"""
    if username not in db["users"]:
        return {}
    return db["users"][username].get("profiles", {})

def is_admin(db, username):
    """Check if user is admin"""
    if username not in db["users"]:
        return False
    return db["users"][username].get("role") == "admin"



# ===== ADMIN DASHBOARD FUNCTIONS =====
def get_all_profiles_overview(db):
    """Get overview of all profiles across all users for admin dashboard"""
    overview = []
    
    for username, user_data in db["users"].items():
        # Skip admin users in the overview
        if user_data.get("role") == "admin":
            continue
        
        profiles = user_data.get("profiles", {})
        user_email = user_data.get("email", "N/A")
        
        for profile_name, profile_data in profiles.items():
            assets = profile_data.get("assets", {})
            
            # Calculate status
            status = "empty"
            drift_status = "N/A"
            total_value = 0
            needs_action = False
            
            # Check if profile has any assets with targets
            has_targets = any(a.get("target", 0) > 0 for a in assets.values()) if assets else False
            
            if assets and has_targets:
                try:
                    tickers = list(assets.keys())
                    prices = {}
                    for ticker in tickers:
                        try:
                            stock = yf.Ticker(ticker)
                            hist = stock.history(period="1d")
                            if not hist.empty:
                                prices[ticker] = hist['Close'].iloc[-1]
                        except:
                            prices[ticker] = None
                    
                    # Calculate total value
                    for ticker, asset_data in assets.items():
                        if ticker in prices and prices[ticker]:
                            units = asset_data.get("units", 0)
                            total_value += units * prices[ticker]
                    
                    # Calculate current allocation
                    current_allocation = {}
                    if total_value > 0:
                        for ticker, asset_data in assets.items():
                            if ticker in prices and prices[ticker]:
                                units = asset_data.get("units", 0)
                                value = units * prices[ticker]
                                current_allocation[ticker] = (value / total_value) * 100
                    
                    # Calculate drift
                    max_drift = 0
                    drift_tolerance = profile_data.get("drift_tolerance", 5.0)
                    for ticker, asset_data in assets.items():
                        target_pct = asset_data.get("target", 0)
                        current_pct = current_allocation.get(ticker, 0)
                        drift = abs(current_pct - target_pct)
                        max_drift = max(max_drift, drift)
                        
                        if drift > drift_tolerance:
                            needs_action = True
                    
                    if needs_action:
                        status = "needs_action"
                        drift_status = f"{max_drift:.1f}%"
                    else:
                        status = "balanced"
                        drift_status = "Balanced"
                except Exception as e:
                    # Log the error for debugging
                    import traceback
                    print(f"Error calculating portfolio {profile_name} for {username}: {str(e)}")
                    traceback.print_exc()
                    status = "error"
                    drift_status = "Error"
            
            overview.append({
                "username": username,
                "user_email": user_email,
                "profile_name": profile_name,
                "status": status,
                "drift_status": drift_status,
                "total_value": total_value,
                "asset_count": len(assets),
                "needs_action": needs_action,
                "last_rebalanced": profile_data.get("last_rebalanced", "Never"),
                "created_at": profile_data.get("created_at", "Unknown")
            })
    
    return overview

def login_as_user(username):
    """Admin function to login as another user (impersonation)"""
    st.session_state.impersonating_user = username
    st.session_state.active_profile = None

def stop_impersonation():
    """Stop impersonating user and return to admin"""
    if "impersonating_user" in st.session_state:
        del st.session_state.impersonating_user
    st.session_state.active_profile = None

# ===== AI ASSISTANT =====
AI_SYSTEM_PROMPT = """You are a helpful AI assistant for the AlphaStream Portfolio Optimizer application. Your role is to help users understand and use the application effectively.

## About the Application
AlphaStream is a long-term investment portfolio management tool that helps users:
- Create and manage multiple investment portfolios/strategies
- Track asset allocation and monitor drift from targets
- Rebalance portfolios when allocations drift beyond tolerance
- Compare performance against benchmarks and goals

## Key Features to Explain

### 1. Portfolio Setup (Sidebar Steps)
- **Strategy Setup (①)**: Create a profile with name, principal amount, goal %, currency, bank/account info
- **Drift Strategy (②)**: Set tolerance % (how much drift is acceptable before rebalancing)
- **Benchmark (③)**: Select benchmarks to compare against (SPY, QQQ, VTI, etc.)
- **Asset Allocation (④)**: Add tickers and set target percentages (must total 100%)
- **Lock Asset Mix (⑤)**: Lock allocation when ready to deploy capital
- **Asset Deployment (⑥)**: Record actual purchases at real broker prices

### 2. Key Metrics Explained
- **CAGR**: Compound Annual Growth Rate - annualized return
- **ROI**: Total Return on Investment since inception
- **Drift**: Difference between actual % and target % allocation
- **Deployed %**: How much of planned capital has been invested

### 3. Rebalancing
- When an asset drifts beyond tolerance, rebalancing is needed
- The app shows exactly how many shares to buy/sell
- Use Two-Step Workflow: get recommendations, execute at broker, record actual prices

### 4. Global Dashboard
- Overview of all portfolios
- Risk metrics (volatility, Sharpe ratio, max drawdown)
- Combined wealth timeline
- Attribution analysis (top contributors/detractors)

## Guidelines
- Be concise and helpful
- Use bullet points for lists
- Reference specific features by name
- If unsure about a feature, say so
- Suggest using the ℹ️ help expanders throughout the app for detailed explanations
- Keep responses focused on the app's functionality"""

def get_ai_response(user_message, chat_history, api_key):
    """Get response from Anthropic API"""
    try:
        import anthropic
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Build messages from chat history
        messages = []
        for msg in chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=AI_SYSTEM_PROMPT,
            messages=messages
        )
        
        return response.content[0].text
    except ImportError:
        return "❌ The `anthropic` package is not installed. Please run: `pip install anthropic`"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ===== EMAIL NOTIFICATIONS =====
def send_email(to_email, subject, html_body, settings):
    """Send email using SMTP settings"""
    try:
        smtp_server = settings.get("smtp_server", "smtp.gmail.com")
        smtp_port = int(settings.get("smtp_port", 587))
        smtp_username = settings.get("smtp_username", "")
        smtp_password = settings.get("smtp_password", "")
        from_name = settings.get("smtp_from_name", "AlphaStream Portfolio")
        
        if not smtp_username or not smtp_password:
            return False, "SMTP credentials not configured"
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{from_name} <{smtp_username}>"
        msg["To"] = to_email
        
        # Plain text fallback
        plain_text = html_body.replace("<br>", "\n").replace("</p>", "\n")
        plain_text = re.sub('<[^<]+?>', '', plain_text)
        
        msg.attach(MIMEText(plain_text, "plain"))
        msg.attach(MIMEText(html_body, "html"))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, to_email, msg.as_string())
        
        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)

def send_rebalance_notification(user_email, user_name, portfolios_needing_rebalance, settings):
    """Send rebalance alert email"""
    subject = f"🚨 AlphaStream Alert: {len(portfolios_needing_rebalance)} Portfolio(s) Need Rebalancing"
    
    portfolio_list = ""
    for p in portfolios_needing_rebalance:
        portfolio_list += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;"><strong>{p['name']}</strong></td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">${p['value']:,.0f}</td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; color: #ef4444;">{p['max_drift']:.1f}%</td>
        </tr>
        """
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #1e293b; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); padding: 20px; text-align: center;">
            <h1 style="color: white; margin: 0;">🛡️ AlphaStream Portfolio</h1>
        </div>
        
        <div style="padding: 20px;">
            <p>Hi <strong>{user_name}</strong>,</p>
            
            <p>One or more of your portfolios have drifted beyond your tolerance threshold and require rebalancing:</p>
            
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <thead>
                    <tr style="background: #f1f5f9;">
                        <th style="padding: 10px; text-align: left;">Portfolio</th>
                        <th style="padding: 10px; text-align: left;">Value</th>
                        <th style="padding: 10px; text-align: left;">Max Drift</th>
                    </tr>
                </thead>
                <tbody>
                    {portfolio_list}
                </tbody>
            </table>
            
            <div style="background: #fef2f2; border-left: 4px solid #ef4444; padding: 15px; margin: 20px 0;">
                <strong>⚠️ Action Required:</strong> Log in to AlphaStream to review and execute rebalancing trades.
            </div>
            
            <p style="color: #64748b; font-size: 12px; margin-top: 30px;">
                You received this email because you enabled rebalance notifications in AlphaStream.<br>
                To unsubscribe, disable notifications in your account settings.
            </p>
        </div>
    </body>
    </html>
    """
    
    return send_email(user_email, subject, html_body, settings)

def check_and_send_rebalance_notifications(db, username, portfolios_needing_rebalance):
    """Check if notification should be sent and send it"""
    settings = db.get("global_settings", {})
    
    # Check if email notifications are enabled globally
    if not settings.get("email_notifications_enabled", False):
        return False, "Email notifications disabled"
    
    # Check user preferences
    user_data = db.get("users", {}).get(username, {})
    user_settings = user_data.get("settings", {})
    
    if not user_settings.get("email_rebalance_alerts", False):
        return False, "User has disabled rebalance alerts"
    
    user_email = user_data.get("email", "")
    if not user_email or "@" not in user_email:
        return False, "No valid email address"
    
    # Check last notification time (avoid spam - once per 24h per portfolio)
    last_notified = user_settings.get("last_rebalance_notification", "")
    if last_notified:
        try:
            last_time = datetime.strptime(last_notified, "%Y-%m-%d %H:%M:%S")
            if (datetime.now() - last_time).total_seconds() < 86400:  # 24 hours
                return False, "Already notified within 24 hours"
        except:
            pass
    
    # Send notification
    user_name = user_data.get("display_name", username)
    success, msg = send_rebalance_notification(user_email, user_name, portfolios_needing_rebalance, settings)
    
    if success:
        # Update last notification time
        if "settings" not in db["users"][username]:
            db["users"][username]["settings"] = {}
        db["users"][username]["settings"]["last_rebalance_notification"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return success, msg

def send_rebalance_confirmation_email(db, username, profile_name, recommendations, actual_prices):
    """Send email confirmation after rebalance is executed"""
    settings = db.get("global_settings", {})
    
    # Check if email notifications are enabled globally
    if not settings.get("email_notifications_enabled", False):
        return False, "Email notifications disabled"
    
    # Check user preferences
    user_data = db.get("users", {}).get(username, {})
    user_settings = user_data.get("settings", {})
    
    if not user_settings.get("email_rebalance_confirmation", False):
        return False, "User has disabled rebalance confirmation emails"
    
    user_email = user_data.get("email", "")
    if not user_email or "@" not in user_email:
        return False, "No valid email address"
    
    user_name = user_data.get("display_name", username)
    
    # Build trades table
    trades_html = ""
    total_recommended_value = 0
    total_actual_value = 0
    
    for rec in recommendations:
        ticker = rec['ticker']
        action = rec['action']
        shares = int(rec['shares'])
        est_price = rec['estimated_price']
        actual_price = actual_prices.get(ticker, est_price)
        
        est_value = shares * est_price
        actual_value = shares * actual_price
        slippage = ((actual_price / est_price) - 1) * 100 if est_price > 0 else 0
        
        total_recommended_value += est_value
        total_actual_value += actual_value
        
        # Color coding
        action_color = "#10b981" if action == "BUY" else "#ef4444"
        slippage_color = "#10b981" if abs(slippage) < 0.5 else "#f59e0b" if abs(slippage) < 2 else "#ef4444"
        
        trades_html += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">
                <span style="color: {action_color}; font-weight: 600;">{action}</span>
            </td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: 600;">{ticker}</td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: right;">{shares:,}</td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: right;">${est_price:.2f}</td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: right;">${actual_price:.2f}</td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: right;">
                <span style="color: {slippage_color};">{slippage:+.2f}%</span>
            </td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: right;">${actual_value:,.2f}</td>
        </tr>
        """
    
    # Calculate total slippage
    total_slippage = ((total_actual_value / total_recommended_value) - 1) * 100 if total_recommended_value > 0 else 0
    total_slippage_color = "#10b981" if abs(total_slippage) < 0.5 else "#f59e0b" if abs(total_slippage) < 2 else "#ef4444"
    
    subject = f"✅ AlphaStream: Rebalance Complete - {profile_name}"
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #1e293b; max-width: 700px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; text-align: center;">
            <h1 style="color: white; margin: 0;">✅ Rebalance Complete</h1>
        </div>
        
        <div style="padding: 20px;">
            <p>Hi <strong>{user_name}</strong>,</p>
            
            <p>Your portfolio <strong>"{profile_name}"</strong> has been successfully rebalanced.</p>
            
            <div style="background: #f0fdf4; border-left: 4px solid #10b981; padding: 15px; margin: 20px 0;">
                <strong>📅 Executed:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </div>
            
            <h3 style="color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">📊 Trade Summary</h3>
            
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;">
                <thead>
                    <tr style="background: #f1f5f9;">
                        <th style="padding: 10px; text-align: left;">Action</th>
                        <th style="padding: 10px; text-align: left;">Ticker</th>
                        <th style="padding: 10px; text-align: right;">Shares</th>
                        <th style="padding: 10px; text-align: right;">Est. Price</th>
                        <th style="padding: 10px; text-align: right;">Actual Price</th>
                        <th style="padding: 10px; text-align: right;">Slippage</th>
                        <th style="padding: 10px; text-align: right;">Total</th>
                    </tr>
                </thead>
                <tbody>
                    {trades_html}
                </tbody>
                <tfoot>
                    <tr style="background: #f8fafc; font-weight: 600;">
                        <td colspan="5" style="padding: 10px; text-align: right;">TOTAL:</td>
                        <td style="padding: 10px; text-align: right; color: {total_slippage_color};">{total_slippage:+.2f}%</td>
                        <td style="padding: 10px; text-align: right;">${total_actual_value:,.2f}</td>
                    </tr>
                </tfoot>
            </table>
            
            <h3 style="color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">📈 Comparison</h3>
            
            <table style="width: 100%; margin: 20px 0;">
                <tr>
                    <td style="padding: 10px; background: #f1f5f9; border-radius: 8px; text-align: center; width: 50%;">
                        <div style="font-size: 12px; color: #64748b;">Recommended Value</div>
                        <div style="font-size: 24px; font-weight: 700; color: #1e293b;">${total_recommended_value:,.2f}</div>
                    </td>
                    <td style="padding: 10px; background: #f0fdf4; border-radius: 8px; text-align: center; width: 50%;">
                        <div style="font-size: 12px; color: #64748b;">Actual Value</div>
                        <div style="font-size: 24px; font-weight: 700; color: #10b981;">${total_actual_value:,.2f}</div>
                    </td>
                </tr>
            </table>
            
            <p style="color: #64748b; font-size: 12px; margin-top: 30px;">
                This is an automated confirmation from AlphaStream Portfolio Optimizer.<br>
                Log in to view your updated portfolio allocation.
            </p>
        </div>
    </body>
    </html>
    """
    
    return send_email(user_email, subject, html_body, settings)

# ===== SESSION STATE INITIALIZATION =====
if "db" not in st.session_state:
    st.session_state.db = load_db()

# Ensure db has required structure (safety check)
if "users" not in st.session_state.db:
    st.session_state.db["users"] = {}
if "global_settings" not in st.session_state.db:
    st.session_state.db["global_settings"] = {
        "allow_registration": True, 
        "default_drift_tolerance": 5.0,
        "ai_assistant_enabled": True,
        "ai_assistant_api_key": ""
    }
# Ensure AI settings exist in existing databases
if "ai_assistant_enabled" not in st.session_state.db.get("global_settings", {}):
    st.session_state.db["global_settings"]["ai_assistant_enabled"] = True
    st.session_state.db["global_settings"]["ai_assistant_api_key"] = ""
# Ensure email settings exist in existing databases
if "email_notifications_enabled" not in st.session_state.db.get("global_settings", {}):
    st.session_state.db["global_settings"]["email_notifications_enabled"] = False
    st.session_state.db["global_settings"]["smtp_server"] = "smtp.gmail.com"
    st.session_state.db["global_settings"]["smtp_port"] = 587
    st.session_state.db["global_settings"]["smtp_username"] = ""
    st.session_state.db["global_settings"]["smtp_password"] = ""
    st.session_state.db["global_settings"]["smtp_from_name"] = "AlphaStream Portfolio"
if "system_logs" not in st.session_state.db:
    st.session_state.db["system_logs"] = []

# Create default admin if no users exist
if not st.session_state.db["users"]:
    admin_hash, admin_salt = hash_password("admin123")
    st.session_state.db["users"]["admin"] = {
        "email": "admin@localhost",
        "password_hash": admin_hash,
        "password_salt": admin_salt,
        "display_name": "Administrator",
        "role": "admin",
        "is_active": True,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_login": "",
        "login_attempts": 0,
        "lockout_until": None,
        "profiles": {},
        "settings": {}
    }
    save_db(st.session_state.db)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "session_token" not in st.session_state:
    st.session_state.session_token = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "Global Dashboard"
if "active_profile" not in st.session_state:
    st.session_state.active_profile = None
if "show_rebalance_recommendation" not in st.session_state:
    st.session_state.show_rebalance_recommendation = False
if "show_execute_form" not in st.session_state:
    st.session_state.show_execute_form = False
if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"
if "current_page" not in st.session_state:
    st.session_state.current_page = "Global Dashboard"


# ===== ADMIN DASHBOARD UI =====
# ADMIN TAB IMPLEMENTATIONS
# These functions will be inserted before the show_admin_dashboard function

def show_admin_overview_tab(db, all_profiles):
    """Tab 1: Overview - Profiles, Users, Needs Action"""
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "📊 All Profiles Overview",
        "👥 User Management",
        "⚠️ Profiles Needing Action"
    ])
    
    # SUB-TAB 1: All Profiles Overview
    with sub_tab1:
        st.markdown("### 📊 All Profiles Overview")
        st.caption("Complete view of all user portfolios across the system")
        
        # Filters
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            users_list = ["All"] + sorted(list(set([p["username"] for p in all_profiles])))
            filter_user = st.selectbox("Filter by User", users_list, key="filter_user_overview")
        
        with col_f2:
            filter_status = st.selectbox("Filter by Status", 
                                        ["All", "balanced", "needs_action", "empty"],
                                        key="filter_status_overview")
        
        with col_f3:
            sort_by = st.selectbox("Sort by",
                                  ["User", "Portfolio Value", "Action Required", "Last Rebalanced"],
                                  key="sort_by_overview")
        
        # Apply filters
        filtered_profiles = all_profiles
        if filter_user != "All":
            filtered_profiles = [p for p in filtered_profiles if p["username"] == filter_user]
        if filter_status != "All":
            filtered_profiles = [p for p in filtered_profiles if p["status"] == filter_status]
        
        # Apply sorting
        if sort_by == "User":
            filtered_profiles.sort(key=lambda x: x["username"])
        elif sort_by == "Portfolio Value":
            filtered_profiles.sort(key=lambda x: x["total_value"], reverse=True)
        elif sort_by == "Action Required":
            filtered_profiles.sort(key=lambda x: x["needs_action"], reverse=True)
        elif sort_by == "Last Rebalanced":
            filtered_profiles.sort(key=lambda x: x["last_rebalanced"] or "Never", reverse=True)
        
        st.divider()
        st.caption(f"Showing {len(filtered_profiles)} of {len(all_profiles)} profiles")
        
        # Display profiles
        for profile in filtered_profiles:
            col_card, col_action = st.columns([5, 1])
            
            with col_card:
                status_color = {
                    "balanced": "#10b981",
                    "needs_action": "#ef4444",
                    "empty": "#6b7280"
                }.get(profile["status"], "#6b7280")
                
                status_label = {
                    "balanced": "✅ Balanced",
                    "needs_action": "⚠️ Action Required",
                    "empty": "📭 Empty"
                }.get(profile["status"], "Unknown")
                
                st.markdown(f"""
                    <div style="background: white; border-left: 4px solid {status_color}; 
                                padding: 16px; border-radius: 8px; margin-bottom: 12px;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                            <div>
                                <h4 style="margin: 0; color: #1e293b;">📊 {profile['profile_name']}</h4>
                                <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.85rem;">
                                    👤 {profile['username']} ({profile['user_email']})
                                </p>
                            </div>
                            <span style="background: {status_color}; color: white; 
                                         padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">
                                {status_label}
                            </span>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">
                            <div>
                                <p style="margin: 0; color: #64748b; font-size: 0.75rem;">Portfolio Value</p>
                                <p style="margin: 4px 0 0 0; color: #1e293b; font-weight: 600; font-size: 1.1rem;">
                                    ${profile['total_value']:,.2f}
                                </p>
                            </div>
                            <div>
                                <p style="margin: 0; color: #64748b; font-size: 0.75rem;">Assets</p>
                                <p style="margin: 4px 0 0 0; color: #1e293b; font-weight: 600; font-size: 1.1rem;">
                                    {profile['asset_count']}
                                </p>
                            </div>
                            <div>
                                <p style="margin: 0; color: #64748b; font-size: 0.75rem;">Drift Status</p>
                                <p style="margin: 4px 0 0 0; color: #1e293b; font-weight: 600; font-size: 1.1rem;">
                                    {profile['drift_status']}
                                </p>
                            </div>
                            <div>
                                <p style="margin: 0; color: #64748b; font-size: 0.75rem;">Last Rebalanced</p>
                                <p style="margin: 4px 0 0 0; color: #1e293b; font-weight: 600; font-size: 0.85rem;">
                                    {profile['last_rebalanced'][:10] if profile['last_rebalanced'] and profile['last_rebalanced'] != 'Never' else 'Never'}
                                </p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_action:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"👁️ View", key=f"view_{profile['username']}_{profile['profile_name']}", use_container_width=True):
                    login_as_user(profile['username'])
                    st.session_state.active_profile = profile['profile_name']
                    st.session_state.current_page = "Portfolio Manager"
                    st.rerun()
    
    # SUB-TAB 2: User Management
    with sub_tab2:
        st.markdown("### 👥 User Management")
        st.caption("View and manage all registered users")
        
        # Add refresh button to reload fresh data
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔄 Refresh Users", key="refresh_users_list"):
                # Clear cache flags to force fresh load
                if 'admin_dashboard_loaded' in st.session_state:
                    del st.session_state['admin_dashboard_loaded']
                # Force reload from Google Sheets
                st.session_state.db = load_db()
                st.success("✅ User list refreshed!")
                st.rerun()
        
        # IMPORTANT: Get users from session state (freshest data)
        users = st.session_state.db.get("users", {})
        non_admin_users = {k: v for k, v in users.items() if v.get("role") != "admin"}
        
        if not non_admin_users:
            st.info("No users registered yet.")
        else:
            for username, user_data in non_admin_users.items():
                is_active = user_data.get("is_active", True)
                status_color = "#10b981" if is_active else "#ef4444"
                status_text = "Active" if is_active else "Inactive"
                status_icon = "✅" if is_active else "🔴"
                
                st.markdown(f"""
                    <div style="background: white; padding: 20px; border-radius: 10px; 
                                margin-bottom: 16px; border: 1px solid #e2e8f0;">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h4 style="margin: 0; color: #1e293b;">👤 {user_data.get('display_name', username)}</h4>
                                <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.9rem;">
                                    @{username} • {user_data.get('email', 'N/A')}
                                </p>
                                <p style="margin: 8px 0 0 0; color: #64748b; font-size: 0.85rem;">
                                    📁 {len(user_data.get('profiles', {}))} portfolios • 
                                    Joined: {user_data.get('created_at', 'Unknown')[:10]}
                                </p>
                            </div>
                            <span style="background: {status_color}; color: white; padding: 4px 12px; 
                                         border-radius: 12px; font-size: 0.75rem; font-weight: 600;">
                                {status_icon} {status_text}
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button(f"🔐 Login as User", key=f"login_{username}", use_container_width=True):
                        login_as_user(username)
                        st.session_state.current_page = "Global Dashboard"
                        log_security_event(db, "admin_impersonation", "admin", f"Logged in as {username}", "info")
                        save_db(db)
                        st.rerun()
                
                with col2:
                    if st.button(f"🔑 Reset Password", key=f"reset_{username}", use_container_width=True):
                        # Generate a temporary password
                        import secrets
                        import string
                        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                        
                        # Hash the new password
                        pw_hash, pw_salt = hash_password(temp_password)
                        user_data["password_hash"] = pw_hash
                        user_data["password_salt"] = pw_salt
                        
                        # Log the action
                        log_activity(db, username, "password_reset_admin", "Admin reset user password", "")
                        log_security_event(db, "password_reset", username, "Admin reset password", "info")
                        save_db(db)
                        
                        st.success(f"✅ Password reset! New password: `{temp_password}`")
                        st.info("⚠️ User should change this password immediately after login.")
                
                with col3:
                    if is_active:
                        if st.button(f"🚫 Deactivate", key=f"deactivate_{username}", use_container_width=True):
                            user_data["is_active"] = False
                            log_activity(db, username, "user_deactivated", "Admin deactivated user account", "")
                            log_security_event(db, "user_deactivated", username, "Admin deactivated account", "warning")
                            save_db(db)
                            st.warning(f"User {username} has been deactivated")
                            st.rerun()
                    else:
                        if st.button(f"✅ Activate", key=f"activate_{username}", use_container_width=True, type="primary"):
                            user_data["is_active"] = True
                            user_data["login_attempts"] = 0
                            user_data["lockout_until"] = None
                            log_activity(db, username, "user_activated", "Admin activated user account", "")
                            log_security_event(db, "user_activated", username, "Admin activated account", "info")
                            save_db(db)
                            st.success(f"User {username} has been activated")
                            st.rerun()
                
                with col4:
                    if st.button(f"🗑️ Delete User", key=f"delete_{username}", use_container_width=True):
                        # Show confirmation
                        if f"confirm_delete_{username}" not in st.session_state:
                            st.session_state[f"confirm_delete_{username}"] = True
                            st.error(f"⚠️ Click again to confirm deletion of {username}")
                        else:
                            # Actually delete
                            portfolio_count = len(user_data.get('profiles', {}))
                            del db["users"][username]
                            log_activity(db, username, "user_deleted", f"Admin deleted user account ({portfolio_count} portfolios removed)", "")
                            log_security_event(db, "user_deleted", username, "Admin deleted account", "critical")
                            save_db(db)
                            del st.session_state[f"confirm_delete_{username}"]
                            st.success(f"✅ User {username} has been permanently deleted")
                            st.rerun()
                
                st.divider()
    
    # SUB-TAB 3: Profiles Needing Action
    with sub_tab3:
        st.markdown("### ⚠️ Profiles Needing Action")
        st.caption("Portfolios requiring immediate rebalancing")
        
        needs_action = [p for p in all_profiles if p["needs_action"]]
        
        if not needs_action:
            st.success("🎉 All portfolios are balanced! No action required.")
        else:
            st.warning(f"⚠️ {len(needs_action)} portfolio(s) need rebalancing")
            
            for profile in needs_action:
                col_card, col_action = st.columns([5, 1])
                
                with col_card:
                    st.markdown(f"""
                        <div style="background: #fef2f2; border-left: 4px solid #ef4444; 
                                    padding: 16px; border-radius: 8px; margin-bottom: 12px;">
                            <h4 style="margin: 0; color: #991b1b;">📊 {profile['profile_name']}</h4>
                            <p style="margin: 4px 0 0 0; color: #991b1b; font-size: 0.85rem;">
                                👤 {profile['username']} ({profile['user_email']})
                            </p>
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 12px;">
                                <div>
                                    <p style="margin: 0; color: #64748b; font-size: 0.75rem;">Portfolio Value</p>
                                    <p style="margin: 4px 0 0 0; color: #991b1b; font-weight: 600; font-size: 1.1rem;">
                                        ${profile['total_value']:,.2f}
                                    </p>
                                </div>
                                <div>
                                    <p style="margin: 0; color: #64748b; font-size: 0.75rem;">Assets</p>
                                    <p style="margin: 4px 0 0 0; color: #991b1b; font-weight: 600; font-size: 1.1rem;">
                                        {profile['asset_count']}
                                    </p>
                                </div>
                                <div>
                                    <p style="margin: 0; color: #64748b; font-size: 0.75rem;">Drift</p>
                                    <p style="margin: 4px 0 0 0; color: #991b1b; font-weight: 600; font-size: 1.1rem;">
                                        {profile['drift_status']}
                                    </p>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_action:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button(f"🔧 Fix", key=f"fix_{profile['username']}_{profile['profile_name']}", 
                               use_container_width=True, type="primary"):
                        login_as_user(profile['username'])
                        st.session_state.active_profile = profile['profile_name']
                        st.session_state.current_page = "Portfolio Manager"
                        st.rerun()


def show_activity_logs_tab(db):
    """Tab 2: Activity & Logs"""
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "📝 User Activity",
        "🚨 System Errors",
        "📧 Notifications"
    ])
    
    # SUB-TAB 1: User Activity
    with sub_tab1:
        st.markdown("### 📝 User Activity Log")
        st.caption("Track all user actions for audit trail")
        
        activity_logs = db.get("activity_logs", [])
        
        if not activity_logs:
            st.info("No activity logs yet. Actions will appear here as users interact with the system.")
        else:
            # Filters
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                users_list = ["All"] + sorted(list(set([log.get("username", "") for log in activity_logs])))
                filter_user = st.selectbox("Filter by User", users_list, key="activity_user")
            
            with col_f2:
                actions = ["All"] + sorted(list(set([log.get("action", "") for log in activity_logs])))
                filter_action = st.selectbox("Filter by Action", actions, key="activity_action")
            
            with col_f3:
                limit = st.selectbox("Show", [50, 100, 200, 500], key="activity_limit")
            
            # Apply filters
            filtered = activity_logs
            if filter_user != "All":
                filtered = [log for log in filtered if log.get("username") == filter_user]
            if filter_action != "All":
                filtered = [log for log in filtered if log.get("action") == filter_action]
            
            filtered = filtered[:limit]
            
            st.caption(f"Showing {len(filtered)} of {len(activity_logs)} activities")
            
            # Display as table
            if filtered:
                for log in filtered:
                    col1, col2, col3, col4 = st.columns([2, 1, 2, 3])
                    with col1:
                        st.caption(log.get("timestamp", ""))
                    with col2:
                        st.caption(f"👤 {log.get('username', '')}")
                    with col3:
                        st.caption(f"**{log.get('action', '')}**")
                    with col4:
                        st.caption(log.get("details", ""))
                    st.divider()
    
    # SUB-TAB 2: System Errors
    with sub_tab2:
        st.markdown("### 🚨 System Error Logs")
        st.caption("Monitor application errors and issues")
        
        system_logs = db.get("system_logs", [])
        error_logs = [log for log in system_logs if log.get("type") in ["error", "warning"]]
        
        if not error_logs:
            st.success("✅ No errors! System is running smoothly.")
        else:
            st.warning(f"⚠️ {len(error_logs)} error/warning events in logs")
            
            # Display errors
            for log in error_logs[:50]:
                severity = "🔴" if log.get("type") == "error" else "🟡"
                st.markdown(f"""
                    <div style="background: #fef2f2; padding: 12px; border-radius: 6px; margin-bottom: 8px;">
                        <p style="margin: 0; font-size: 0.85rem; color: #64748b;">
                            {severity} {log.get('timestamp', '')} • {log.get('user_id', 'system')}
                        </p>
                        <p style="margin: 4px 0 0 0; color: #991b1b; font-weight: 500;">
                            {log.get('message', '')}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
    
    # SUB-TAB 3: Notifications
    with sub_tab3:
        st.markdown("### 📧 Notification History")
        st.caption("Track all email notifications sent to users")
        
        notifications = db.get("notification_history", [])
        
        if not notifications:
            st.info("No notifications sent yet. Email alerts will appear here.")
        else:
            st.caption(f"Total notifications: {len(notifications)}")
            
            for notif in notifications[:50]:
                status_icon = "✅" if notif.get("status") == "sent" else "❌"
                status_color = "#10b981" if notif.get("status") == "sent" else "#ef4444"
                
                st.markdown(f"""
                    <div style="background: white; padding: 12px; border-radius: 6px; 
                                margin-bottom: 8px; border-left: 3px solid {status_color};">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <p style="margin: 0; font-weight: 600; color: #1e293b;">
                                    {notif.get('subject', '')}
                                </p>
                                <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b;">
                                    To: {notif.get('username', '')} • Type: {notif.get('type', '')}
                                </p>
                                <p style="margin: 4px 0 0 0; font-size: 0.75rem; color: #64748b;">
                                    {notif.get('timestamp', '')}
                                </p>
                            </div>
                            <span style="font-size: 1.5rem;">{status_icon}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)


def show_analytics_tab(db, analytics):
    """Tab 3: Analytics & Reports"""
    sub_tab1, sub_tab2 = st.tabs([
        "📊 System Analytics",
        "🎯 Top Assets"
    ])
    
    # SUB-TAB 1: System Analytics
    with sub_tab1:
        st.markdown("### 📊 System Analytics")
        st.caption("Platform-wide metrics and trends")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Users", analytics['total_users'])
            st.metric("Total Portfolios", analytics['total_portfolios'])
        
        with col2:
            avg_portfolios = analytics['total_portfolios'] / max(analytics['total_users'], 1)
            st.metric("Avg Portfolios/User", f"{avg_portfolios:.1f}")
            st.metric("Avg Portfolio Value", f"${analytics['avg_portfolio_value']:,.0f}")
        
        with col3:
            st.metric("Total AUM", f"${analytics['total_aum']:,.0f}")
            st.metric("Recent Activities", analytics['recent_activities'])
        
        st.divider()
        
        # Activity Timeline
        st.markdown("### 📈 Activity Timeline")
        activity_logs = analytics.get('activity_logs', [])
        
        if activity_logs:
            st.caption(f"Total activities logged: {len(activity_logs)}")
            
            # Group activities by date
            from collections import defaultdict
            activity_by_date = defaultdict(int)
            activity_by_type = defaultdict(int)
            
            for log in activity_logs:
                timestamp = log.get("timestamp", "")
                action = log.get("action", "unknown")
                
                # Extract date
                date_str = timestamp[:10] if len(timestamp) >= 10 else "Unknown"
                activity_by_date[date_str] += 1
                activity_by_type[action] += 1
            
            # Create timeline chart
            col_chart1, col_chart2 = st.columns([2, 1])
            
            with col_chart1:
                st.markdown("#### 📅 Activity by Date")
                if activity_by_date:
                    # Sort by date
                    sorted_dates = sorted(activity_by_date.items())
                    dates = [d[0] for d in sorted_dates[-14:]]  # Last 14 days
                    counts = [d[1] for d in sorted_dates[-14:]]
                    
                    chart_data = pd.DataFrame({
                        'Date': dates,
                        'Activities': counts
                    })
                    
                    st.bar_chart(chart_data.set_index('Date'))
                else:
                    st.info("No timeline data available")
            
            with col_chart2:
                st.markdown("#### 🎯 Activity Types")
                if activity_by_type:
                    # Show top 5 activity types
                    top_types = sorted(activity_by_type.items(), key=lambda x: x[1], reverse=True)[:5]
                    for action, count in top_types:
                        action_display = action.replace("_", " ").title()
                        percentage = (count / len(activity_logs)) * 100
                        st.markdown(f"""
                            <div style="background: white; padding: 8px; border-radius: 6px; 
                                        margin-bottom: 6px; border-left: 3px solid #3b82f6;">
                                <div style="font-weight: 600; color: #1e293b; margin-bottom: 4px;">
                                    {action_display}
                                </div>
                                <div style="color: #64748b; font-size: 0.85rem;">
                                    {count} activities ({percentage:.1f}%)
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No activity types data")
            
            # Recent activity list - ENHANCED v7.2.4
            st.markdown("#### 🕐 Recent Activity Details")
            
            # Export button
            col_title, col_export = st.columns([3, 1])
            with col_export:
                if activity_logs:
                    # Prepare CSV export
                    import io
                    csv_buffer = io.StringIO()
                    csv_buffer.write("Timestamp,Username,Action,Details,IP Address\n")
                    for log in activity_logs:
                        timestamp = log.get("timestamp", "")
                        username = log.get("username", "")
                        action = log.get("action", "")
                        details = log.get("details", "").replace(",", ";")  # Escape commas
                        ip = log.get("ip_address", "")
                        csv_buffer.write(f'"{timestamp}","{username}","{action}","{details}","{ip}"\n')
                    
                    st.download_button(
                        label="📥 Export CSV",
                        data=csv_buffer.getvalue(),
                        file_name=f"activity_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        help="Download all activity logs as CSV"
                    )
            
            # Add filters
            col_filter1, col_filter2, col_filter3 = st.columns([2, 2, 1])
            with col_filter1:
                # User filter
                all_usernames = sorted(set(log.get("username", "Unknown") for log in activity_logs))
                selected_user = st.selectbox(
                    "Filter by User",
                    ["All Users"] + all_usernames,
                    key="activity_user_filter"
                )
            
            with col_filter2:
                # Action type filter
                all_actions = sorted(set(log.get("action", "unknown") for log in activity_logs))
                selected_action = st.selectbox(
                    "Filter by Action",
                    ["All Actions"] + all_actions,
                    key="activity_action_filter"
                )
            
            with col_filter3:
                # Number of entries
                num_entries = st.number_input(
                    "Show entries",
                    min_value=5,
                    max_value=100,
                    value=20,
                    step=5,
                    key="activity_num_entries"
                )
            
            # Search box
            search_query = st.text_input(
                "🔍 Search in details",
                placeholder="Search for keywords in activity details...",
                key="activity_search"
            )
            
            # Filter logs
            filtered_logs = activity_logs
            if selected_user != "All Users":
                filtered_logs = [log for log in filtered_logs if log.get("username") == selected_user]
            if selected_action != "All Actions":
                filtered_logs = [log for log in filtered_logs if log.get("action") == selected_action]
            if search_query:
                search_lower = search_query.lower()
                filtered_logs = [
                    log for log in filtered_logs 
                    if search_lower in log.get("details", "").lower() or 
                       search_lower in log.get("username", "").lower()
                ]
            
            # Sort by timestamp
            recent_logs = sorted(filtered_logs, key=lambda x: x.get("timestamp", ""), reverse=True)[:num_entries]
            
            # Stats summary
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("Showing", f"{len(recent_logs)} of {len(filtered_logs)}")
            with col_stat2:
                if recent_logs:
                    unique_users = len(set(log.get("username") for log in recent_logs))
                    st.metric("Unique Users", unique_users)
            with col_stat3:
                if recent_logs:
                    unique_actions = len(set(log.get("action") for log in recent_logs))
                    st.metric("Action Types", unique_actions)
            
            st.divider()
            
            # Display enhanced activity logs - USING NATIVE STREAMLIT COMPONENTS
            if recent_logs:
                for idx, log in enumerate(recent_logs, 1):
                    timestamp = log.get("timestamp", "Unknown")
                    username = log.get("username", "Unknown")
                    action = log.get("action", "unknown")
                    details = log.get("details", "")
                    ip_address = log.get("ip_address", "")
                    
                    # Format timestamp
                    try:
                        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                        time_ago = get_time_ago(dt)
                    except:
                        time_str = timestamp
                        time_ago = ""
                    
                    # Action icon and color mapping
                    action_icons = {
                        "login": "🔐", "user_login": "🔐", "user_registered": "📝",
                        "logout": "🚪", "profile_created": "➕", "profile_updated": "✏️",
                        "profile_deleted": "🗑️", "rebalance_executed": "⚖️",
                        "user_created": "👤", "user_deleted": "❌",
                        "settings_changed": "⚙️", "password_changed": "🔑",
                        "database_reset": "🔥", "backup_created": "💾",
                        "asset_added": "📈", "asset_removed": "📉"
                    }
                    
                    action_colors = {
                        "login": "🟢", "user_login": "🟢", "user_registered": "🔵",
                        "logout": "⚪", "profile_created": "🔵", "profile_updated": "🟠",
                        "profile_deleted": "🔴", "rebalance_executed": "🟣",
                        "user_created": "🔵", "user_deleted": "🔴",
                        "settings_changed": "🟠", "password_changed": "🟠",
                        "database_reset": "🔴", "backup_created": "🟢",
                        "asset_added": "🟢", "asset_removed": "🔴"
                    }
                    
                    icon = action_icons.get(action, "📝")
                    color_emoji = action_colors.get(action, "⚪")
                    action_display = action.replace("_", " ").title()
                    
                    # Use Streamlit's native container and columns
                    with st.container():
                        # Header row
                        col_main, col_meta = st.columns([3, 1])
                        
                        with col_main:
                            st.markdown(f"**{icon} {color_emoji} {action_display}** • @{username}")
                            if details:
                                st.caption(f"ℹ️ {details}")
                            if ip_address:
                                st.caption(f"🌐 IP: {ip_address}")
                        
                        with col_meta:
                            st.caption(f"**#{idx}**")
                            st.caption(f"{time_str}")
                            if time_ago:
                                st.caption(f"_{time_ago}_")
                        
                        st.divider()
            else:
                st.info("No activities match the selected filters")
        else:
            st.info("No activity data yet")
    
    # SUB-TAB 2: Top Assets
    with sub_tab2:
        st.markdown("### 🎯 Most Popular Assets")
        st.caption("Assets most frequently held across all portfolios")
        
        if analytics['top_assets']:
            for i, (ticker, count) in enumerate(analytics['top_assets'], 1):
                st.markdown(f"""
                    <div style="background: white; padding: 12px; border-radius: 6px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="color: #64748b; font-weight: 600;">#{i}</span>
                                <span style="margin-left: 12px; font-weight: 600; color: #1e293b;">{ticker}</span>
                            </div>
                            <span style="background: #3b82f6; color: white; padding: 4px 12px; 
                                         border-radius: 12px; font-size: 0.85rem;">
                                {count} portfolios
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No asset data available yet")


def show_system_management_tab(db):
    """Tab 4: System Management"""
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "⚙️ Global Settings",
        "🏥 System Health",
        "💾 Backup & Restore"
    ])
    
    # SUB-TAB 1: Global Settings
    with sub_tab1:
        st.markdown("### ⚙️ Global Settings")
        st.caption("Configure system-wide settings")
        
        settings = db.get("global_settings", {})
        
        st.markdown("#### 📧 Email Configuration")
        email_enabled = st.checkbox("Enable Email Notifications", 
                                    value=settings.get("email_notifications_enabled", False),
                                    key="email_enabled_setting")
        
        if email_enabled:
            smtp_server = st.text_input("SMTP Server", value=settings.get("smtp_server", "smtp.gmail.com"))
            smtp_port = st.number_input("SMTP Port", value=settings.get("smtp_port", 587), step=1)
            smtp_username = st.text_input("SMTP Username", value=settings.get("smtp_username", ""))
            smtp_password = st.text_input("SMTP Password", value=settings.get("smtp_password", ""), type="password")
            
            if st.button("💾 Save Email Settings"):
                settings["email_notifications_enabled"] = email_enabled
                settings["smtp_server"] = smtp_server
                settings["smtp_port"] = smtp_port
                settings["smtp_username"] = smtp_username
                settings["smtp_password"] = smtp_password
                db["global_settings"] = settings
                save_db(db)
                st.success("✅ Email settings saved!")
                log_system_event(db, "settings_changed", "Email settings updated", "admin")
        
        st.divider()
        
        st.markdown("#### 🤖 AI Assistant Configuration")
        ai_enabled = st.checkbox("Enable AI Assistant", 
                                 value=settings.get("ai_assistant_enabled", False),
                                 key="ai_enabled_setting",
                                 help="Enable AI-powered chatbot in sidebar for all users")
        
        if ai_enabled:
            ai_api_key = st.text_input("Anthropic API Key", 
                                       value=settings.get("ai_assistant_api_key", ""),
                                       type="password",
                                       help="Your Anthropic API key for Claude")
            
            st.caption("🔑 Get your API key from: https://console.anthropic.com/")
            
            if st.button("💾 Save AI Settings"):
                settings["ai_assistant_enabled"] = ai_enabled
                settings["ai_assistant_api_key"] = ai_api_key
                db["global_settings"] = settings
                save_db(db)
                st.success("✅ AI Assistant settings saved! Users can now see the AI chatbot in the sidebar.")
                log_system_event(db, "settings_changed", "AI Assistant settings updated", "admin")
                st.rerun()
        else:
            # Clear AI key if disabled
            if st.button("💾 Save AI Settings"):
                settings["ai_assistant_enabled"] = False
                settings["ai_assistant_api_key"] = ""
                db["global_settings"] = settings
                save_db(db)
                st.success("✅ AI Assistant disabled")
                log_system_event(db, "settings_changed", "AI Assistant disabled", "admin")
                st.rerun()
        
        st.divider()
        
        st.markdown("#### 🎯 Default Settings")
        st.caption("These defaults apply to all newly created profiles")
        
        col_def1, col_def2 = st.columns(2)
        with col_def1:
            default_drift = st.number_input("Default Drift Tolerance (%)", 
                                           value=settings.get("default_drift_tolerance", 5.0),
                                           min_value=1.0, max_value=20.0, step=0.5,
                                           help="Default drift tolerance for new profiles")
        with col_def2:
            default_growth = st.number_input("Default Annual Growth Goal (%)", 
                                            value=settings.get("default_growth_goal", 10.0),
                                            min_value=0.0, max_value=50.0, step=0.5,
                                            help="Default yearly growth goal for new profiles")
        
        allow_registration = st.checkbox("Allow New User Registration",
                                        value=settings.get("allow_registration", True))
        
        if st.button("💾 Save Default Settings"):
            settings["default_drift_tolerance"] = default_drift
            settings["default_growth_goal"] = default_growth
            settings["allow_registration"] = allow_registration
            db["global_settings"] = settings
            save_db(db)
            st.success("✅ Default settings saved!")
            st.info(f"New profiles will use: {default_drift}% drift tolerance, {default_growth}% growth goal")
            log_system_event(db, "settings_changed", "Default settings updated", "admin")
    
    # SUB-TAB 2: System Health
    with sub_tab2:
        st.markdown("### 🏥 System Health Dashboard")
        st.caption("Monitor system status and performance")
        
        # Database Version Info (NEW for v7.2.0)
        metadata = db.get('metadata', {})
        if metadata:
            st.markdown("#### 🔒 Database Metadata")
            col_meta1, col_meta2, col_meta3 = st.columns(3)
            with col_meta1:
                st.metric("Database Version", metadata.get('version', 0))
            with col_meta2:
                st.metric("Total Saves", metadata.get('save_count', 0))
            with col_meta3:
                st.caption("**Last Modified:**")
                st.caption(f"👤 {metadata.get('last_save_by', 'unknown')}")
                st.caption(f"🕐 {metadata.get('last_save_timestamp', 'unknown')}")
            
            # Show session info
            if 'data_version' in st.session_state:
                session_version = st.session_state.get('data_version', 0)
                loaded_at = st.session_state.get('data_loaded_at')
                if loaded_at:
                    age_seconds = (datetime.now() - loaded_at).total_seconds()
                    age_minutes = int(age_seconds / 60)
                    
                    version_match = "✅ In Sync" if session_version == metadata.get('version', 0) else "⚠️ Out of Sync"
                    staleness = "🟢 Fresh" if age_seconds < 300 else "🟡 Stale"
                    
                    st.info(f"""
                    **Your Session:** Version {session_version} {version_match}  
                    **Session Age:** {age_minutes} minutes {staleness}  
                    **Loaded At:** {loaded_at.strftime('%Y-%m-%d %H:%M:%S')}
                    """)
                    
                    if session_version != metadata.get('version', 0):
                        st.warning("⚠️ Your session data is outdated. Refresh the page to see latest changes.")
                        if st.button("🔄 Refresh Data Now"):
                            st.rerun()
            
            st.divider()
        
        health = get_system_health(db)
        
        status_color = {
            "healthy": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444"
        }.get(health["status"], "#6b7280")
        
        status_icon = {
            "healthy": "🟢",
            "warning": "🟡",
            "error": "🔴"
        }.get(health["status"], "⚪")
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, {status_color}20, {status_color}10); 
                        padding: 20px; border-radius: 12px; border-left: 4px solid {status_color};">
                <h3 style="margin: 0; color: {status_color};">
                    {status_icon} System Status: {health['status'].title()}
                </h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        for check in health["checks"]:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"**{check['name']}**")
            with col2:
                st.caption(check['value'])
            with col3:
                st.markdown(check['icon'])
    
    # SUB-TAB 3: Backup & Restore
    with sub_tab3:
        st.markdown("### 💾 Backup & Restore")
        st.caption("Protect your data with regular backups")
        
        st.info("💡 **Tip:** Download a backup before making major changes or resetting the database!")
        
        # Immediate download option
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}.json"
        backup_data = json.dumps(db, indent=2)
        
        col_backup1, col_backup2 = st.columns([2, 1])
        with col_backup1:
            st.download_button(
                label="📥 Download Database Backup",
                data=backup_data,
                file_name=backup_filename,
                mime="application/json",
                type="primary",
                use_container_width=True,
                help="Downloads current database as JSON file"
            )
        with col_backup2:
            st.metric("Backup Size", f"{len(backup_data):,} chars")
        
        st.divider()
        
        # Show backup info
        st.markdown("### 📊 Current Database Info")
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric("Total Users", len(db.get('users', {})))
        with col_info2:
            total_profiles = sum(len(user.get('profiles', {})) for user in db.get('users', {}).values())
            st.metric("Total Portfolios", total_profiles)
        with col_info3:
            st.metric("Database Version", db.get('metadata', {}).get('version', 0))
        
        st.divider()
        
        # Restore functionality
        st.markdown("### 📤 Restore from Backup")
        st.caption("Upload a previously downloaded backup to restore")
        
        uploaded_file = st.file_uploader(
            "Choose backup file",
            type=['json'],
            help="Select a backup JSON file to restore",
            key="backup_uploader"
        )
        
        if uploaded_file is not None:
            try:
                # Read uploaded file
                backup_content = uploaded_file.read().decode('utf-8')
                restored_db = json.loads(backup_content)
                
                # Show preview
                st.success(f"✅ Backup file loaded: {uploaded_file.name}")
                
                preview_col1, preview_col2, preview_col3 = st.columns(3)
                with preview_col1:
                    st.metric("Users in Backup", len(restored_db.get('users', {})))
                with preview_col2:
                    backup_profiles = sum(len(u.get('profiles', {})) for u in restored_db.get('users', {}).values())
                    st.metric("Portfolios in Backup", backup_profiles)
                with preview_col3:
                    st.metric("Backup Version", restored_db.get('metadata', {}).get('version', 'Unknown'))
                
                st.divider()
                
                # Restore confirmation
                st.warning("⚠️ **WARNING:** Restoring will REPLACE your current database with the backup!")
                
                restore_confirm = st.checkbox(
                    "✅ I understand this will replace all current data",
                    key="restore_confirm"
                )
                
                if restore_confirm:
                    admin_password_restore = st.text_input(
                        "Enter admin password to confirm restore:",
                        type="password",
                        key="restore_password"
                    )
                    
                    if admin_password_restore:
                        col_restore1, col_restore2 = st.columns([3, 1])
                        with col_restore2:
                            if st.button("🔄 RESTORE", type="primary", use_container_width=True):
                                # Verify admin password
                                admin_user = db.get('users', {}).get('admin')
                                if admin_user and verify_password(admin_password_restore, admin_user['password_hash'], admin_user['password_salt']):
                                    # Restore database
                                    st.session_state.db = restored_db
                                    if save_db(restored_db):
                                        st.success("✅ Database restored successfully!")
                                        st.info("🔄 Reloading application...")
                                        
                                        # Clear cache
                                        if 'admin_dashboard_loaded' in st.session_state:
                                            del st.session_state['admin_dashboard_loaded']
                                        
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to save restored database")
                                else:
                                    st.error("❌ Invalid admin password")
                
            except json.JSONDecodeError:
                st.error("❌ Invalid backup file format")
            except Exception as e:
                st.error(f"❌ Error loading backup: {str(e)}")
        
        st.divider()
        
        # DANGER ZONE: Database Reset
        st.markdown("### ⚠️ Danger Zone")
        st.caption("⚠️ **WARNING:** These actions are irreversible!")
        
        with st.expander("🔥 Reset Database to Fresh State", expanded=False):
            st.error("""
            **⚠️ EXTREME CAUTION REQUIRED**
            
            This will **PERMANENTLY DELETE**:
            - All user accounts (except admin)
            - All portfolios
            - All transactions
            - All activity logs
            - All system logs
            
            **What will be kept:**
            - Admin account credentials
            - Global settings
            
            **This action CANNOT be undone!**
            """)
            
            st.warning("💡 **Recommendation:** Create a backup before resetting!")
            
            # Confirmation checkboxes
            col_check1, col_check2 = st.columns(2)
            with col_check1:
                confirm_backup = st.checkbox("✅ I have created a backup", key="reset_confirm_backup")
            with col_check2:
                confirm_understand = st.checkbox("✅ I understand this is permanent", key="reset_confirm_understand")
            
            # Password confirmation
            admin_password = st.text_input(
                "Enter your admin password to confirm:",
                type="password",
                key="reset_admin_password",
                help="Required for security verification"
            )
            
            # Final confirmation
            if confirm_backup and confirm_understand and admin_password:
                col_reset1, col_reset2 = st.columns([3, 1])
                with col_reset2:
                    if st.button("🔥 RESET DATABASE", type="primary", use_container_width=True, key="execute_reset"):
                        with st.spinner("🔄 Resetting database..."):
                            success, message, fresh_db = reset_database_to_fresh(admin_password, keep_admin=True)
                            
                            if success:
                                # Save the fresh database (bypass version increment to keep version=1)
                                st.session_state.db = fresh_db
                                save_result = save_db(fresh_db, bypass_version_increment=True)
                                
                                if save_result:
                                    st.success("✅ Database reset successfully!")
                                    st.success("✅ Admin account preserved")
                                    st.success("✅ All other data removed")
                                    st.info("🔄 Reloading application...")
                                    
                                    # Clear session state
                                    if 'admin_dashboard_loaded' in st.session_state:
                                        del st.session_state['admin_dashboard_loaded']
                                    
                                    # Force reload
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to save reset database")
                            else:
                                st.error(f"❌ {message}")
            elif not (confirm_backup and confirm_understand):
                st.info("☝️ Please check both confirmations above to proceed")
            elif not admin_password:
                st.info("🔑 Enter your admin password to enable reset")


def show_security_tab(db):
    """Tab 5: Security & Audit"""
    sub_tab1, sub_tab2 = st.tabs([
        "🔐 Security Logs",
        "🚨 Failed Logins"
    ])
    
    # SUB-TAB 1: Security Logs
    with sub_tab1:
        st.markdown("### 🔐 Security Event Log")
        st.caption("Monitor security-related events and activities")
        
        security_logs = db.get("security_logs", [])
        
        if not security_logs:
            st.success("✅ No security events logged")
        else:
            # Filter by severity
            severity_filter = st.selectbox("Filter by Severity", 
                                          ["All", "info", "warning", "critical"],
                                          key="security_severity")
            
            filtered = security_logs
            if severity_filter != "All":
                filtered = [log for log in filtered if log.get("severity") == severity_filter]
            
            st.caption(f"Showing {len(filtered)} of {len(security_logs)} events")
            
            for log in filtered[:100]:
                severity_icon = {
                    "info": "ℹ️",
                    "warning": "⚠️",
                    "critical": "🚨"
                }.get(log.get("severity", "info"), "ℹ️")
                
                severity_color = {
                    "info": "#3b82f6",
                    "warning": "#f59e0b",
                    "critical": "#ef4444"
                }.get(log.get("severity", "info"), "#6b7280")
                
                st.markdown(f"""
                    <div style="background: white; padding: 12px; border-radius: 6px; 
                                margin-bottom: 8px; border-left: 3px solid {severity_color};">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 1;">
                                <p style="margin: 0; font-size: 0.75rem; color: #64748b;">
                                    {log.get('timestamp', '')}
                                </p>
                                <p style="margin: 4px 0; font-weight: 600; color: #1e293b;">
                                    {severity_icon} {log.get('event_type', '')}
                                </p>
                                <p style="margin: 0; font-size: 0.85rem; color: #64748b;">
                                    User: {log.get('username', '')} • {log.get('details', '')}
                                </p>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    # SUB-TAB 2: Failed Logins
    with sub_tab2:
        st.markdown("### 🚨 Failed Login Attempts")
        st.caption("Monitor and prevent unauthorized access")
        
        security_logs = db.get("security_logs", [])
        failed_logins = [log for log in security_logs if log.get("event_type") == "failed_login"]
        
        if not failed_logins:
            st.success("✅ No failed login attempts")
        else:
            st.warning(f"⚠️ {len(failed_logins)} failed login attempts detected")
            
            # Group by username
            from collections import Counter
            username_counts = Counter([log.get("username", "") for log in failed_logins[:100]])
            
            st.markdown("#### Top Failed Login Attempts")
            for username, count in username_counts.most_common(10):
                col1, col2, col3 = st.columns([3, 1, 2])
                with col1:
                    st.caption(f"**{username}**")
                with col2:
                    st.caption(f"🔴 {count} attempts")
                with col3:
                    if count >= 5:
                        st.caption("⚠️ Potential brute force")
            
            st.divider()
            
            st.markdown("#### Recent Failed Logins")
            for log in failed_logins[:20]:
                st.caption(f"🔴 {log.get('timestamp', '')} - {log.get('username', '')} from {log.get('ip_address', 'unknown')}")

def show_admin_dashboard(db, current_user):
    """Enhanced Admin Dashboard with 5 comprehensive tabs"""
    
    st.title("👑 Administrator Dashboard")
    st.markdown("""
        <div style="background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%); 
                    color: white; padding: 20px; border-radius: 12px; margin-bottom: 30px;">
            <h3 style="margin: 0 0 8px 0; color: white;">System Overview & Management</h3>
            <p style="margin: 0; opacity: 0.9;">Complete administrative control and monitoring dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    # System-wide metrics at the top
    analytics = get_analytics_data(db)
    all_profiles = get_all_profiles_overview(db)
    needs_action_count = len([p for p in all_profiles if p["needs_action"]])
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                        color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <h2 style="margin: 0; font-size: 2rem;">{analytics['total_users']}</h2>
                <p style="margin: 8px 0 0 0; font-size: 0.9rem;">Total Users</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_m2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                        color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <h2 style="margin: 0; font-size: 2rem;">{analytics['total_portfolios']}</h2>
                <p style="margin: 8px 0 0 0; font-size: 0.9rem;">Total Portfolios</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_m3:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                        color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <h2 style="margin: 0; font-size: 2rem;">{needs_action_count}</h2>
                <p style="margin: 8px 0 0 0; font-size: 0.9rem;">Need Action</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_m4:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); 
                        color: white; padding: 20px; border-radius: 10px; text-align: center;">
                <h2 style="margin: 0; font-size: 2rem;">${analytics['total_aum']:,.0f}</h2>
                <p style="margin: 8px 0 0 0; font-size: 0.9rem;">Total AUM</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # 5 Main Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "📜 Activity & Logs", 
        "📈 Analytics",
        "⚙️ System",
        "🔐 Security"
    ])
    
    with tab1:
        show_admin_overview_tab(db, all_profiles)
    
    with tab2:
        show_activity_logs_tab(db)
    
    with tab3:
        show_analytics_tab(db, analytics)
    
    with tab4:
        show_system_management_tab(db)
    
    with tab5:
        show_security_tab(db)

def show_login_page():
    """Display login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 40px;">
                <h1 style="font-size: 2.5rem; margin-bottom: 8px;">🛡️ Long Term Strategy</h1>
                <p style="color: #64748b; font-size: 1.1rem;">Institutional-Grade Portfolio Management</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔐 Sign In")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            col_login, col_register = st.columns(2)
            with col_login:
                login_btn = st.form_submit_button("🚀 Sign In", use_container_width=True, type="primary")
            with col_register:
                register_btn = st.form_submit_button("📜 Create Account", use_container_width=True)
            
            if login_btn:
                if not username or not password:
                    st.error("❌ Please enter username and password")
                else:
                    success, message, user_data = authenticate_user(st.session_state.db, username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.current_user = username.lower()
                        st.session_state.username = username.lower()  # v7.2.1: Ensure username is stored
                        st.session_state.session_token = generate_session_token()
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
            if register_btn:
                st.session_state.auth_page = "register"
                st.rerun()
        
        if "admin" in st.session_state.db.get("users", {}):
            with st.expander("ℹ️ First time setup?", expanded=False):
                st.markdown("""
                    **Default Admin Account:**
                    - Username: `admin`
                    - Password: `admin123`
                    
                    ⚠️ **Important:** Change the admin password after first login!
                """)

def show_registration_page():
    """Display registration page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-bottom: 40px;">
                <h1 style="font-size: 2.5rem; margin-bottom: 8px;">🛡️ Long Term Strategy</h1>
                <p style="color: #64748b; font-size: 1.1rem;">Create Your Account</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📜 Register")
        if not st.session_state.db.get("global_settings", {}).get("allow_registration", True):
            st.warning("⚠️ New registrations are currently disabled.")
            if st.button("← Back to Login"):
                st.session_state.auth_page = "login"
                st.rerun()
            return
        
        with st.form("register_form"):
            display_name = st.text_input("Display Name", placeholder="Your full name")
            username = st.text_input("Username*", placeholder="Choose a username")
            email = st.text_input("Email*", placeholder="your@email.com")
            col_pwd1, col_pwd2 = st.columns(2)
            with col_pwd1:
                password = st.text_input("Password*", type="password")
            with col_pwd2:
                password_confirm = st.text_input("Confirm Password*", type="password")
            
            st.caption(f"Password: min {PASSWORD_MIN_LENGTH} chars, uppercase, lowercase, digit")
            
            col_reg, col_back = st.columns(2)
            with col_reg:
                register_btn = st.form_submit_button("✅ Create Account", use_container_width=True, type="primary")
            with col_back:
                back_btn = st.form_submit_button("← Back to Login", use_container_width=True)
            
            if register_btn:
                if password != password_confirm:
                    st.error("❌ Passwords do not match")
                else:
                    success, message = register_user(st.session_state.db, username, email, password, display_name)
                    if success:
                        st.success(f"✅ {message}")
                        st.session_state.auth_page = "login"
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
            if back_btn:
                st.session_state.auth_page = "login"
                st.rerun()

# ===== MAIN APPLICATION FLOW =====
if not st.session_state.authenticated:
    if st.session_state.auth_page == "login":
        show_login_page()
    else:
        show_registration_page()
else:
    # Get actual logged-in user and check for impersonation
    actual_user = st.session_state.current_user
    impersonating_user = st.session_state.get("impersonating_user")
    current_user = impersonating_user if impersonating_user else actual_user
    
    user_data = st.session_state.db.get("users", {}).get(actual_user, {})
    is_admin_user = user_data.get("role") == "admin"
    
    # ===== SIDEBAR =====
    with st.sidebar:
        # Show impersonation status if applicable
        if is_admin_user and impersonating_user:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
                            color: white; padding: 16px; border-radius: 10px; margin-bottom: 20px;
                            animation: pulse-impersonate 2s infinite;">
                    <div>
                        <p style="margin: 0; font-size: 0.75rem; opacity: 0.9;">👑 Admin viewing as</p>
                        <p style="margin: 4px 0 0 0; font-size: 1.1rem; font-weight: 600;">👤 {current_user}</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 6px; margin-top: 12px;">
                        <p style="margin: 0; font-size: 0.75rem; text-align: center;">⚠️ IMPERSONATION MODE</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🔙 Return to Admin Dashboard", use_container_width=True, type="secondary", key="return_admin"):
                stop_impersonation()
                st.session_state.current_page = "Admin Dashboard"
                st.rerun()
        else:
            role_badge = "admin-badge" if is_admin_user else "user-badge"
            role_text = "👑 Admin" if is_admin_user else "👤 User"
            st.markdown(f'<div class="{role_badge}">{role_text}: {user_data.get("display_name", actual_user)}</div>', unsafe_allow_html=True)
            st.caption(f"@{actual_user}")
        
        st.divider()
        st.markdown("### 📊 Portfolio Optimizer")
        st.caption(f"Long Term Strategy Suite v{VERSION}")
        
        # Version info expander
        with st.expander("ℹ️ Version Info"):
            st.markdown(f"""
                **Version:** {VERSION}  
                **Released:** {VERSION_DATE}  
                **Build:** {VERSION_NAME}
            """)
            if st.button("📋 View Changelog", key="view_changelog", use_container_width=True):
                st.info(CHANGELOG)
        
        st.divider()
        
        # Navigation using buttons (no state management issues)
        st.markdown("**Navigation**")
        
        # Get current page
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Global Dashboard"
        
        # Style for selected button
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            dash_type = "primary" if st.session_state.current_page == "Global Dashboard" else "secondary"
            if st.button("🏠 Global Dashboard", use_container_width=True, type=dash_type, key="nav_global"):
                st.session_state.current_page = "Global Dashboard"
                st.rerun()
        with nav_col2:
            port_type = "primary" if st.session_state.current_page == "Portfolio Manager" else "secondary"
            if st.button("📊 Portfolio Manager", use_container_width=True, type=port_type, key="nav_portfolio"):
                st.session_state.current_page = "Portfolio Manager"
                st.rerun()
        
        # Show Admin Dashboard button only when admin and not impersonating
        if is_admin_user and not impersonating_user:
            admin_type = "primary" if st.session_state.current_page == "Admin Dashboard" else "secondary"
            if st.button("👑 Admin Dashboard", use_container_width=True, type=admin_type, key="nav_admin"):
                st.session_state.current_page = "Admin Dashboard"
                st.rerun()
        
        view_mode = st.session_state.current_page
        
        st.divider()
        
        # Portfolio Setup Progress Tracker (only show in Portfolio Manager)
        if view_mode == "Portfolio Manager" and st.session_state.active_profile:
            try:
                prof = st.session_state.db["users"][current_user]["profiles"][st.session_state.active_profile]
                
                # Check completion status for each step
                has_profile = True  # If we're here, profile exists
                has_principal = prof.get('principal', 0) > 0
                has_benchmarks = len(prof.get('benchmarks', [])) > 0 or prof.get('benchmark') is not None
                has_assets = len(prof.get('assets', {})) > 0
                asset_mix_locked = prof.get('asset_mix_locked', False)
                has_deployments = any(len(a.get('purchases', [])) > 0 for a in prof.get('assets', {}).values())
                
                # Calculate total completion
                steps_complete = sum([has_profile, has_principal, has_benchmarks, has_assets, asset_mix_locked, has_deployments])
                total_steps = 6
                
                # Show compact progress tracker
                st.markdown("**📋 Setup Progress:**")
                progress_pct = (steps_complete / total_steps) * 100
                
                # Progress bar
                if progress_pct >= 100:
                    bar_color = "#10b981"  # Green
                elif progress_pct >= 50:
                    bar_color = "#fbbf24"  # Yellow
                else:
                    bar_color = "#ef4444"  # Red
                
                st.markdown(f'''
                    <div style="margin: 10px 0;">
                        <div style="background: #e5e7eb; border-radius: 8px; height: 8px; overflow: hidden;">
                            <div style="background: {bar_color}; height: 100%; width: {progress_pct}%;"></div>
                        </div>
                        <div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;">{steps_complete}/{total_steps} steps complete</div>
                    </div>
                ''', unsafe_allow_html=True)
                
                # Show step checklist
                steps = [
                    ("① Profile Created", has_profile, "Profile exists"),
                    ("② Principal Set", has_principal, "Capital amount defined"),
                    ("③ Benchmarks Added", has_benchmarks, "Performance tracking configured"),
                    ("④ Assets Allocated", has_assets, "Investment mix defined"),
                    ("⑤ Mix Locked", asset_mix_locked, "Ready for deployment"),
                    ("⑥ Deployed", has_deployments, "Capital invested")
                ]
                
                for step_name, is_complete, tooltip in steps:
                    if is_complete:
                        st.markdown(f"✅ {step_name}", help=tooltip)
                    else:
                        st.markdown(f"⏳ {step_name}", help=tooltip)
                        # Show what to do next for first incomplete step
                        if steps_complete == steps.index((step_name, is_complete, tooltip)):
                            if not has_principal:
                                st.caption("👉 Set your principal amount below")
                            elif not has_benchmarks:
                                st.caption("👉 Add benchmarks below (optional)")
                            elif not has_assets:
                                st.caption("👉 Add assets in ④ Asset Allocation")
                            elif not asset_mix_locked:
                                st.caption("👉 Lock mix in ⑤ Lock Asset Mix")
                            elif not has_deployments:
                                st.caption("👉 Deploy capital in ⑥ Asset Deployment")
                        break  # Only show hint for first incomplete
                
                st.divider()
            except:
                pass  # If any error, just skip progress tracker
        
        # Get user profiles early (needed for Profile Creation logic)
        user_profiles = get_user_profiles(st.session_state.db, current_user)
        
        # Profile Creation
        st.markdown("### ① Strategy Setup")
        
        # Check if we should auto-expand (from welcome page button or if no profiles exist)
        should_expand = st.session_state.get("auto_expand_create_profile", False) or len(user_profiles) == 0
        if st.session_state.get("auto_expand_create_profile", False):
            # Clear the flag after using it
            st.session_state.auto_expand_create_profile = False
        
        with st.expander("🆕 Create New Profile", expanded=should_expand):
            with st.form("new_profile_form"):
                # Get global defaults for pre-filling form
                global_settings = st.session_state.db.get("global_settings", {})
                default_growth_goal = global_settings.get("default_growth_goal", 10.0)
                
                n_name = st.text_input("Profile Name*", placeholder="e.g., Retirement USD")
                col1, col2 = st.columns(2)
                with col1:
                    n_bank = st.text_input("Bank/Broker*", placeholder="e.g., Fidelity")
                with col2:
                    n_account_type = st.selectbox("Account Type*", ["", "Taxable", "401k", "IRA", "Roth IRA", "TFSA", "RRSP", "529", "HSA", "Other"])
                n_curr = st.selectbox("Currency*", ["USD", "CAD"])
                n_p = st.number_input("Principal ($)*", value=10000.0, step=1000.0, min_value=0.0)
                n_goal = st.number_input("Annual Growth Goal (%)*", 
                                        value=default_growth_goal,  # Use global default! ✅
                                        step=0.5, min_value=0.0,
                                        help=f"Target annual return (default: {default_growth_goal}%)")
                
                # NOTE: Cannot use enhanced_date_input() inside st.form() due to button restrictions
                # Using regular date_input instead
                n_start = st.date_input(
                    "Inception Date*",
                    value=date.today() - timedelta(days=365),
                    max_value=date.today(),
                    help="When did you start this investment strategy?"
                )
                
                submitted = st.form_submit_button("🚀 Initialize Profile", use_container_width=True)
                if submitted:
                    user_profiles = get_user_profiles(st.session_state.db, current_user)
                    
                    # Get global default settings
                    global_settings = st.session_state.db.get("global_settings", {})
                    default_drift = global_settings.get("default_drift_tolerance", 5.0)
                    
                    if not n_name:
                        st.error("❌ Profile name required")
                    elif not n_bank:
                        st.error("❌ Bank/Broker required")
                    elif not n_account_type:
                        st.error("❌ Account Type required")
                    elif n_name in user_profiles:
                        st.warning(f"⚠️ Profile '{n_name}' exists")
                    else:
                        st.session_state.db["users"][current_user]["profiles"][n_name] = {
                            "currency": n_curr, "principal": n_p, "yearly_goal_pct": n_goal,
                            "start_date": str(n_start), "bank_name": n_bank, "account_type": n_account_type,
                            "account_name": f"{n_bank} {n_account_type}", "initialization_date": str(n_start),
                            "asset_mix_locked": False, "assets": {}, "rebalance_logs": [],
                            "drift_tolerance": default_drift,  # Use global default! ✅
                            "rebalance_stats": [], "last_rebalanced": None, 
                            "benchmark": None, "benchmarks": []
                        }
                        save_db(st.session_state.db)
                        prof = st.session_state.db["users"][current_user]["profiles"][n_name]
                        log_profile(prof, "Profile created")
                        
                        # Auto-select the newly created profile
                        st.session_state.active_profile = n_name
                        
                        # Enhanced success message with guidance
                        st.success(f"✅ Portfolio '{n_name}' created successfully!")
                        st.info(f"""
📊 **Next Step:** Click '**Portfolio Manager**' button in the sidebar to:
- Set target allocation percentages for **{n_name}**
- Deploy your initial capital
- Start tracking performance
""")
                        
                        # Visual navigation hint
                        st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; padding: 15px; border-radius: 10px; text-align: center; margin-top: 15px;">
    <p style="margin: 0; font-size: 1rem; font-weight: 600;">
        👉 Click '<strong>📊 Portfolio Manager</strong>' in the sidebar above to continue →
    </p>
</div>
""", unsafe_allow_html=True)
                        
                        # Log the activity
                        log_activity(st.session_state.db, current_user, "profile_created", 
                                   f"Created portfolio: {n_name}", "")
                        
                        st.rerun()
        
        # Profile-specific sidebar (user_profiles already defined above at line 4659)
        
        if view_mode == "Portfolio Manager" and user_profiles:
            st.divider()
            st.markdown("### 🎯 Active Profile")
            
            profile_names = list(user_profiles.keys())
            if st.session_state.active_profile and st.session_state.active_profile in profile_names:
                default_index = profile_names.index(st.session_state.active_profile)
            else:
                default_index = 0
            
            selected = st.selectbox("Select Profile", profile_names, index=default_index, key="profile_selector")
            if selected != st.session_state.active_profile:
                st.session_state.active_profile = selected
                st.rerun()
            
            prof = user_profiles[st.session_state.active_profile]
            p_flag = "🇺🇸" if prof.get("currency") == "USD" else "🇨🇦"
            st.caption(f"🏦 {prof.get('bank_name', 'N/A')} • {prof.get('account_type', 'N/A')}")
            
            # CRUD Actions
            st.divider()
            st.markdown("### ⚙️ Profile Actions")
            col_crud1, col_crud2, col_crud3 = st.columns(3)
            with col_crud1:
                if st.button("✏️ Edit", use_container_width=True, key="edit_profile"):
                    st.session_state.editing_profile = True
            with col_crud2:
                if st.button("🔞 Reset", use_container_width=True, key="reset_profile"):
                    st.session_state.reset_confirm = True
            with col_crud3:
                if st.button("🗑️ Delete", use_container_width=True, key="delete_profile", type="secondary"):
                    st.session_state.delete_confirm = True
            
            # Edit Dialog
            if st.session_state.get("editing_profile", False):
                st.markdown("#### ✏️ Edit Profile")
                with st.form("edit_profile_form"):
                    edit_principal = st.number_input("Principal ($)", value=prof['principal'], step=1000.0, min_value=0.0)
                    edit_goal = st.number_input("Annual Goal (%)", value=prof['yearly_goal_pct'], step=0.5, min_value=0.0)
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        edit_bank = st.text_input("Bank/Broker", value=prof.get('bank_name', ''))
                    with col_e2:
                        current_acct = prof.get('account_type', '')
                        acct_types = ["Taxable", "401k", "IRA", "Roth IRA", "TFSA", "RRSP", "529", "HSA", "Other"]
                        default_idx = acct_types.index(current_acct) if current_acct in acct_types else 0
                        edit_acct = st.selectbox("Account Type", acct_types, index=default_idx)
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.form_submit_button("💾 Save", use_container_width=True):
                            prof['principal'] = edit_principal
                            prof['yearly_goal_pct'] = edit_goal
                            prof['bank_name'] = edit_bank
                            prof['account_type'] = edit_acct
                            prof['account_name'] = f"{edit_bank} {edit_acct}"
                            save_db(st.session_state.db)
                            log_profile(prof, "Profile edited")
                            st.session_state.editing_profile = False
                            st.success("✅ Updated!")
                            st.rerun()
                    with col_cancel:
                        if st.form_submit_button("❌ Cancel", use_container_width=True):
                            st.session_state.editing_profile = False
                            st.rerun()
            
            # Reset Confirmation
            if st.session_state.get("reset_confirm", False):
                st.warning("⚠️ **Reset Profile?**")
                st.caption("Delete all assets and history.")
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    if st.button("🔞 Yes, Reset", use_container_width=True, type="primary", key="confirm_reset"):
                        prof['assets'] = {}
                        prof['rebalance_logs'] = []
                        prof['rebalance_stats'] = []
                        prof['last_rebalanced'] = None
                        prof['asset_mix_locked'] = False
                        clear_rebalance_recommendation(prof)
                        save_db(st.session_state.db)
                        log_profile(prof, "Profile reset")
                        st.session_state.reset_confirm = False
                        st.success("✅ Reset!")
                        st.rerun()
                with col_r2:
                    if st.button("❌ Cancel", use_container_width=True, key="cancel_reset"):
                        st.session_state.reset_confirm = False
                        st.rerun()
            
            # Delete Confirmation
            if st.session_state.get("delete_confirm", False):
                st.error("🗑️ **Delete Profile?**")
                st.caption(f"Permanently delete '{st.session_state.active_profile}'?")
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    if st.button("🗑️ Yes, Delete", use_container_width=True, type="primary", key="confirm_delete"):
                        profile_to_delete = st.session_state.active_profile
                        del st.session_state.db["users"][current_user]["profiles"][profile_to_delete]
                        save_db(st.session_state.db)
                        st.session_state.active_profile = None
                        st.session_state.delete_confirm = False
                        st.success(f"✅ Deleted!")
                        st.rerun()
                with col_d2:
                    if st.button("❌ Cancel", use_container_width=True, key="cancel_delete"):
                        st.session_state.delete_confirm = False
                        st.rerun()
            
            st.divider()
            
            # Drift Strategy
            st.markdown("### ② Drift Strategy")
            
            # Auto-expand if no drift tolerance set
            drift_expand = prof.get('drift_tolerance', 5.0) == 5.0  # Default value means not customized
            
            with st.expander("⚙️ Configure Drift Tolerance", expanded=drift_expand):
                st.caption("Set tolerance threshold")
                with st.expander("ℹ️ What is drift tolerance?", expanded=False):
                    st.markdown("""
                    **Drift tolerance** controls when you get rebalancing alerts.
                    - If an asset's current % differs from target % by more than this, you'll see an alert
                    - **Example:** 5% tolerance means AAPL at 30% (target 25%) triggers an alert
                    """)
                
                new_tolerance = st.number_input("Drift Tolerance (%)", value=float(prof.get('drift_tolerance', 5.0)),
                                               min_value=0.5, max_value=20.0, step=0.5, key="drift_tolerance_input")
                if st.button("💾 Update Tolerance", use_container_width=True, key="update_tolerance"):
                    prof['drift_tolerance'] = new_tolerance
                    save_db(st.session_state.db)
                    log_profile(prof, f"Updated drift tolerance to {new_tolerance}%")
                    st.success("✅ Updated!")
                    st.rerun()
            
            st.divider()
            
            # Benchmark Selection
            st.markdown("### ③ Benchmark Comparison")
            
            # Auto-expand if no benchmarks set
            benchmark_expand = len(prof.get('benchmarks', [])) == 0 and prof.get('benchmark') is None
            
            with st.expander("📊 Configure Benchmarks", expanded=benchmark_expand):
                st.caption("Compare against market benchmarks (US & Canadian)")
                with st.expander("ℹ️ Why use a benchmark?", expanded=False):
                    st.markdown("""
                    **Benchmarks** help evaluate performance.
                    - Chart shows 100% investment in each benchmark
                    - **Outperforming** = your strategy adds value
                    - Select multiple to compare different indices
                    
                    **🇺🇸 US Markets:** SPY, QQQ, VTI, IWM, DIA, BND  
                    **🇨🇦 Canadian Markets:** XIU, XIC, ZCN, VCN
                    """)
                
                benchmark_options = {
                    # US Benchmarks
                    "🇺🇸 S&P 500 (SPY)": "SPY",
                    "🇺🇸 NASDAQ-100 (QQQ)": "QQQ",
                    "🇺🇸 Total Market (VTI)": "VTI",
                    "🇺🇸 Russell 2000 (IWM)": "IWM",
                    "🇺🇸 Dow Jones (DIA)": "DIA",
                    "🇺🇸 US Bonds (BND)": "BND",
                    # Canadian Benchmarks
                    "🇨🇦 TSX 60 (XIU)": "XIU",
                    "🇨🇦 TSX Composite (XIC)": "XIC",
                    "🇨🇦 TSX Capped Comp (ZCN)": "ZCN",
                    "🇨🇦 FTSE Canada (VCN)": "VCN"
                }
                current_benchmarks = prof.get('benchmarks', [])
                # Migration: convert old single benchmark to list
                if not current_benchmarks and prof.get('benchmark'):
                    current_benchmarks = [prof.get('benchmark')]
                
                # Get display names for current benchmarks
                current_display = [k for k, v in benchmark_options.items() if v in current_benchmarks]
                
                selected_benchmarks = st.multiselect("Select Benchmarks", 
                    options=list(benchmark_options.keys()),
                    default=current_display,
                    key="benchmark_multiselect",
                    help="Select one or more benchmarks to compare"
                )
                
                if st.button("💾 Save Benchmarks", use_container_width=True, key="save_benchmark"):
                    prof['benchmarks'] = [benchmark_options[b] for b in selected_benchmarks]
                    prof['benchmark'] = prof['benchmarks'][0] if prof['benchmarks'] else None  # Keep for backward compat
                    save_db(st.session_state.db)
                    st.success("✅ Saved!")
                    st.rerun()
                
                if prof.get('benchmarks'):
                    st.caption(f"📊 Active: {', '.join(prof['benchmarks'])}")
            
            st.divider()
            
            # Asset Allocation
            st.markdown("### ④ Asset Allocation")
            st.caption("Add assets and set target percentages")
            with st.expander("ℹ️ How asset allocation works", expanded=False):
                st.markdown("""
                **Asset allocation** is your investment blueprint.
                - **Target %**: Your desired allocation
                - **Total must equal 100%** to lock
                - **Rebalancing**: When prices change, your % drifts
                
                💡 **Backtest first!** Use tools like [Testfol.io](https://testfol.io/) or 
                [Portfolio Visualizer](https://www.portfoliovisualizer.com/) to validate your 
                allocation strategy with historical data before committing capital.
                """)
            
            current_alloc = sum(a.get('target', 0) for a in prof.get("assets", {}).values())
            
            if current_alloc >= 100:
                bar_color = "#10b981"
            elif current_alloc >= 50:
                bar_color = "#fbbf24"
            else:
                bar_color = "#ef4444"
            
            st.markdown(f'''
                <div style="margin: 12px 0;">
                    <div style="background: #e5e7eb; border-radius: 8px; height: 8px; overflow: hidden;">
                        <div style="background: {bar_color}; height: 100%; width: {min(current_alloc, 100)}%;"></div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            st.markdown(f"**Allocated: {current_alloc:.1f}% / 100%**")
            
            # Show existing assets FIRST (before input) for better UX
            if prof.get("assets"):
                st.divider()
                st.markdown("### 📋 Current Assets")
                st.caption("Click an asset below to edit its target %")
                
                # Show assets in columns
                num_assets = len(prof["assets"])
                cols = st.columns(min(num_assets, 3))
                
                for idx, (ticker, data) in enumerate(prof["assets"].items()):
                    with cols[idx % 3]:
                        units = data.get('units', 0)
                        allocated_pct = data.get('allocated_pct', 0)
                        target = data.get('target', 0)
                        
                        # Create clickable card
                        if units > 0:
                            status = f"✅ {allocated_pct:.0f}% deployed"
                        else:
                            status = "⏳ Not deployed"
                        
                        st.markdown(f"""
                            <div style="background: #f3f4f6; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #3b82f6;">
                                <div style="font-weight: 600; color: #1f2937; margin-bottom: 4px;">{ticker}</div>
                                <div style="color: #6b7280; font-size: 0.9rem;">Target: {target}%</div>
                                <div style="color: #6b7280; font-size: 0.85rem;">{status}</div>
                            </div>
                        """, unsafe_allow_html=True)
                
                st.caption("💡 Enter ticker below to edit or add new asset")
                st.divider()
            
            # Check if asset mix is locked - hide all UI if locked
            is_mix_locked = prof.get("asset_mix_locked", False)
            
            if not is_mix_locked:
                # Quick-add buttons for common tickers (user's specific assets)
                st.markdown("**🚀 Quick Add:**")
                col_q1, col_q2, col_q3, col_q4 = st.columns(4)
                with col_q1:
                    if st.button("SPXL", key="quick_spxl", help="S&P 500 3X", use_container_width=True):
                        # Clear all related widget states for clean slate
                        for key in ['ticker_input', 'target_weight', 'quick_ticker_clicked']:
                            if key in st.session_state:
                                del st.session_state[key]
                        # Set the ticker value
                        st.session_state['ticker_input'] = "SPXL"
                        st.session_state['_quick_add_used'] = True
                        st.rerun()
                with col_q2:
                    if st.button("GLD", key="quick_gld", help="Gold", use_container_width=True):
                        # Clear all related widget states for clean slate
                        for key in ['ticker_input', 'target_weight', 'quick_ticker_clicked']:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.session_state['ticker_input'] = "GLD"
                        st.session_state['_quick_add_used'] = True
                        st.rerun()
                with col_q3:
                    if st.button("DBMF", key="quick_dbmf", help="Managed Futures", use_container_width=True):
                        # Clear all related widget states for clean slate
                        for key in ['ticker_input', 'target_weight', 'quick_ticker_clicked']:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.session_state['ticker_input'] = "DBMF"
                        st.session_state['_quick_add_used'] = True
                        st.rerun()
                with col_q4:
                    if st.button("BIL", key="quick_bil", help="Short-Term Bonds", use_container_width=True):
                        # Clear all related widget states for clean slate
                        for key in ['ticker_input', 'target_weight', 'quick_ticker_clicked']:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.session_state['ticker_input'] = "BIL"
                        st.session_state['_quick_add_used'] = True
                        st.rerun()
            
                # Determine default value for text input
                default_ticker = st.session_state.get('ticker_input', '')
            
                # Enhancement 4: Show info message when asset mix is locked
                is_mix_locked = prof.get("asset_mix_locked", False)
                if is_mix_locked:
                    st.info("🔒 **Asset mix is locked.** Unlock below if you need to add or modify assets.")
            
                a_sym = st.text_input("Ticker Symbol", placeholder="e.g., AAPL", 
                                     key="ticker_input", value=default_ticker,
                                     disabled=is_mix_locked).upper().strip()
                is_existing = a_sym in prof.get("assets", {})
            
                if is_existing:
                    other_allocs = current_alloc - prof["assets"][a_sym].get("target", 0)
                else:
                    other_allocs = current_alloc
                max_available = 100.0 - other_allocs
                block_new = (not is_existing) and (max_available <= 0) and (a_sym != "")
            
                if block_new:
                    st.markdown('<div class="allocation-blocked">🚫 PORTFOLIO AT 100%<br>Remove assets first!</div>', unsafe_allow_html=True)
            
                valid_ticker = False
                last_price = 1.0
                ticker_name = ""
                validation_error = None
            
                if prof.get("asset_mix_locked", False) and not is_existing and a_sym:
                    validation_error = "🔒 **Asset mix locked** - Cannot add new assets. Unlock first to add more."
                    valid_ticker = False
                elif a_sym and not block_new:
                    # Show loading indicator
                    loading_placeholder = st.empty()
                    loading_placeholder.info(f"🔍 Validating {a_sym}... (checking Yahoo Finance)")
                
                    try:
                        # Add timeout handling
                        import signal
                    
                        def timeout_handler(signum, frame):
                            raise TimeoutError("Ticker validation timed out")
                    
                        # Set 10 second timeout (only on Unix systems)
                        try:
                            signal.signal(signal.SIGALRM, timeout_handler)
                            signal.alarm(10)
                        except:
                            pass  # Windows doesn't support SIGALRM
                    
                        try:
                            t_check = yf.Ticker(a_sym)
                            hist = t_check.history(period="1d")
                        
                            # Cancel timeout
                            try:
                                signal.alarm(0)
                            except:
                                pass
                        
                            if not hist.empty:
                                last_price = float(hist['Close'].iloc[-1])
                                try:
                                    ticker_info = t_check.info
                                    ticker_name = ticker_info.get('longName', a_sym)
                                except:
                                    ticker_name = a_sym
                            
                                # Enhancement 1: Show allocation message instead of price
                                if is_existing:
                                    loading_placeholder.success(f"✅ **{ticker_name}** - Asset target allocated")
                                else:
                                    loading_placeholder.success(f"✅ **{ticker_name}** - Ready to allocate")
                                valid_ticker = True
                            else:
                                loading_placeholder.error(f"❌ No data found for '{a_sym}'")
                                validation_error = f"Ticker '{a_sym}' exists but has no price data. Try another ticker."
                            
                        except TimeoutError:
                            loading_placeholder.error(f"⏱️ Timeout validating '{a_sym}'")
                            validation_error = f"Yahoo Finance took too long to respond for '{a_sym}'. Try again or use Quick Add buttons."
                            try:
                                signal.alarm(0)
                            except:
                                pass
                        
                    except Exception as e:
                        loading_placeholder.error(f"❌ Error validating '{a_sym}'")
                        validation_error = f"Could not validate ticker '{a_sym}'. Check spelling or network connection."
                        try:
                            signal.alarm(0)
                        except:
                            pass
                
                    # Show error details if validation failed
                    if validation_error and not valid_ticker:
                        st.caption(f"💡 {validation_error}")
                        st.caption("**Common tickers:** SPY (S&P 500), QQQ (Nasdaq), GLD (Gold), TLT (Bonds)")

            
                if valid_ticker:
                    st.markdown("---")
                    default_target = prof.get("assets", {}).get(a_sym, {}).get("target", 0.0)
                
                    # Enhancement 5: Disable target editing when asset mix is locked (unless editing existing asset)
                    is_locked = prof.get("asset_mix_locked", False)
                    can_edit_target = not is_locked or is_existing
                
                    if is_locked and not is_existing:
                        st.warning("🔒 Asset mix is locked. Unlock first to add new assets or change allocations.")
                
                    a_w = st.number_input("Target Allocation %", 
                                         min_value=0.0, 
                                         max_value=max_available,
                                         value=min(float(default_target), max_available), 
                                         step=0.5, 
                                         help=f"Set the target % for {a_sym}. Max available: {max_available:.1f}%",
                                         key="target_weight",
                                         disabled=is_locked)
                
                    st.markdown("---")
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        # CRITICAL FIX: Remove disabled logic entirely!
                        # Button is ALWAYS enabled once ticker validates.
                        # We validate allocation when button is clicked.
                        # This fixes Quick Add issues with widget state synchronization.
                    
                        if st.button("💾 Save Asset", use_container_width=True, type="primary", key="save_asset"):
                            # Validate allocation when clicked
                            if a_w <= 0:
                                st.error("❌ Target allocation must be greater than 0%")
                            elif a_w > max_available:
                                st.error(f"❌ Target allocation exceeds available {max_available:.1f}%")
                            else:
                                # Validation passed - save the asset
                                # Preserve existing units and purchases if updating
                                existing_units = prof.get("assets", {}).get(a_sym, {}).get("units", 0.0)
                                existing_allocated = prof.get("assets", {}).get(a_sym, {}).get("allocated_pct", 0.0)
                                existing_purchases = prof.get("assets", {}).get(a_sym, {}).get("purchases", [])
                            
                                prof.setdefault("assets", {})[a_sym] = {
                                    "fund_name": ticker_name, "units": existing_units, "target": a_w,
                                    "allocated_pct": existing_allocated,
                                    "purchases": existing_purchases
                                }
                                action = "Updated" if is_existing else "Added"
                                log_profile(prof, f"{action} {a_sym}: {a_w}% target")
                                save_db(st.session_state.db)
                                st.success(f"✅ {action} {a_sym}!")
                                st.rerun()
                    with col_b2:
                        if is_existing:
                            if st.button("🗑️ Remove", use_container_width=True, key="remove_asset"):
                                del prof["assets"][a_sym]
                                log_profile(prof, f"Removed {a_sym}")
                                save_db(st.session_state.db)
                                st.success(f"✅ Removed {a_sym}!")
                                st.rerun()
            
            else:
                # Asset mix is locked - show message, hide all management UI
                st.info("🔒 **Asset mix is locked.** All asset management controls are hidden. Unlock in section ⑤ below to modify assets.")
            
            # Asset Mix Locking
            st.divider()
            st.markdown("### ⑤ Lock Asset Mix")
            
            # Calculate assets and total_allocation BEFORE using them
            assets = prof.get("assets", {})
            total_allocation = sum(a.get('target', 0) for a in assets.values())
            is_complete = (total_allocation == 100.0 and len(assets) > 0)
            is_locked = prof.get("asset_mix_locked", False)
            
            # Auto-expand if not locked or not complete
            lock_expand = not is_locked or not is_complete
            
            with st.expander("🔒 Manage Asset Mix Lock", expanded=lock_expand):
                # Debug info expander
                with st.expander("🔧 Troubleshooting / Current State", expanded=False):
                    st.caption("**Portfolio Status:**")
                    st.json({
                        "Total Allocation": f"{total_allocation:.1f}%",
                        "Assets Defined": len(assets),
                        "Mix Locked": prof.get("asset_mix_locked", False),
                        "Any Deployments": any(a.get("allocated_pct", 0) > 0 for a in assets.values()),
                        "Can Add Assets": not prof.get("asset_mix_locked", False) or (total_allocation < 100),
                    })
                    st.caption("**Assets:**")
                    for ticker, data in assets.items():
                        st.caption(f"• {ticker}: {data.get('target', 0)}% target, {data.get('allocated_pct', 0):.1f}% deployed, {data.get('units', 0)} units")
                    
                    if st.button("🔄 Reset Portfolio (Emergency)", key="emergency_reset"):
                        if st.button("⚠️ Confirm Reset - This will delete ALL data", key="confirm_reset", type="primary"):
                            prof["assets"] = {}
                            prof["asset_mix_locked"] = False
                            save_db(st.session_state.db)
                            log_profile(prof, "Emergency reset - all assets deleted")
                            st.success("✅ Portfolio reset!")
                            st.rerun()
                
                if prof.get("asset_mix_locked", False):
                    st.success("✅ **Asset Mix Locked**")
                    st.caption(f"{len(assets)} assets defined. Ready for deployment.")
                    any_deployments = any(a.get("allocated_pct", 0) > 0 for a in assets.values())
                    
                    if st.button("🔓 Unlock Asset Mix", use_container_width=True, key="unlock_mix"):
                        if any_deployments:
                            # Show warning but allow
                            st.warning("⚠️ You have deployments recorded. Unlocking will allow you to modify targets, but existing deployments remain unchanged.")
                            if st.button("✅ Yes, Unlock Anyway", key="confirm_unlock", type="primary"):
                                prof["asset_mix_locked"] = False
                                save_db(st.session_state.db)
                                log_profile(prof, "Asset mix unlocked (with deployments)")
                                st.rerun()
                        else:
                            prof["asset_mix_locked"] = False
                            save_db(st.session_state.db)
                            log_profile(prof, "Asset mix unlocked")
                            st.rerun()
                else:
                    if is_complete:
                        st.warning("🔜 **Ready to Lock**")
                        st.caption(f"{len(assets)} assets, {total_allocation:.1f}% allocated")
                        if st.button("🔒 Lock Asset Mix", type="primary", use_container_width=True, key="lock_mix"):
                            prof["asset_mix_locked"] = True
                            save_db(st.session_state.db)
                            log_profile(prof, f"Asset mix locked: {len(assets)} assets")
                            st.success("✅ Asset mix locked!")
                            st.rerun()
                    else:
                        st.info("ℹ️ **Asset Mix Not Complete**")
                        st.caption(f"Current: {total_allocation:.1f}% / 100%")
            
            st.divider()
            
            # Asset Deployment
            st.markdown("### ⑥ Asset Deployment")
            st.caption("Deploy capital into individual assets")
            
            if not prof.get("asset_mix_locked", False):
                st.info("🔙 **Lock your asset mix first**")
            else:
                assets = prof.get("assets", {})
                
                # Calculate total deployed and undeployed
                total_deployed_capital = 0
                for ticker, asset_data in assets.items():
                    purchases = asset_data.get("purchases", [])
                    total_deployed_capital += sum(p.get("amount", 0) for p in purchases)
                
                principal_amt = prof['principal']
                undeployed_cash = principal_amt - total_deployed_capital
                
                # Use centralized deployment status check (SINGLE SOURCE OF TRUTH)
                is_truly_fully_deployed, fully_deployed_count, total_assets = check_deployment_status(prof)
                
                # Calculate deployment progress for progress bar
                deployment_progress = (total_deployed_capital / prof['principal']) if prof['principal'] > 0 else 0
                
                st.markdown(f"**Progress:** {fully_deployed_count}/{total_assets} assets fully deployed • {deployment_progress*100:.1f}% capital deployed")
                
                if total_assets > 0:
                    progress_pct = deployment_progress * 100
                    if deployment_progress >= 0.995:  # 99.5% or more
                        bar_color = "#10b981"  # Green
                    elif deployment_progress >= 0.50:
                        bar_color = "#fbbf24"  # Yellow
                    else:
                        bar_color = "#ef4444"  # Red
                    
                    st.markdown(f'''
                        <div style="margin: 20px 0;">
                            <div style="background: #e5e7eb; border-radius: 12px; height: 12px; overflow: hidden;">
                                <div style="background: {bar_color}; height: 100%; width: {progress_pct}%;"></div>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                
                # Determine deployable assets (not yet fully deployed)
                # Use SMART DETECTION: exclude assets where remaining < price
                if is_truly_fully_deployed:
                    # Portfolio is truly fully deployed - no assets can receive more
                    deployable_assets = {}
                else:
                    # Check each asset individually with smart detection
                    deployable_assets = {}
                    for ticker, asset_data in assets.items():
                        allocated_pct = asset_data.get("allocated_pct", 0)
                        target_pct = asset_data.get("target", 0)
                        
                        # Calculate remaining budget
                        purchases = asset_data.get("purchases", [])
                        total_spent = sum(p.get("amount", 0) for p in purchases)
                        target_amount = (target_pct / 100) * prof['principal']
                        remaining_budget = target_amount - total_spent
                        
                        # Check if can still deploy (remaining >= price)
                        can_still_deploy = False
                        try:
                            t_obj = yf.Ticker(ticker)
                            hist = t_obj.history(period="1d")
                            if not hist.empty:
                                current_price = float(hist['Close'].iloc[-1])
                                # Can deploy ONLY if remaining budget >= 1 unit price
                                if remaining_budget >= current_price:
                                    can_still_deploy = True
                                # NO fallback - if can't afford 1 unit, can't deploy!
                            else:
                                # If can't get price, use threshold fallback
                                if allocated_pct < 99.5:
                                    can_still_deploy = True
                        except:
                            # If any error, use threshold fallback
                            if allocated_pct < 99.5:
                                can_still_deploy = True
                        
                        # Add to deployable if can still deploy
                        if can_still_deploy:
                            deployable_assets[ticker] = asset_data
                
                if not deployable_assets:
                    if is_truly_fully_deployed and undeployed_cash > 0:
                        st.success(f"✅ **All assets 100% deployed!** (${undeployed_cash:,.2f} fractional remainder)")
                    else:
                        st.success("✅ **All assets 100% deployed!**")
                else:
                    with st.expander("➢ Record Asset Deployment", expanded=False):
                        st.markdown("### Deploy Capital Into Assets")
                        st.markdown("**Record your actual purchases from your broker**")
                        
                        selected_ticker = st.selectbox("Select Asset", options=list(deployable_assets.keys()),
                            format_func=lambda t: f"{t} - {deployable_assets[t].get('fund_name', t)}", key="deploy_asset_selector")
                        
                        if selected_ticker:
                            asset_data = deployable_assets[selected_ticker]
                            current_allocated = asset_data.get("allocated_pct", 0)
                            remaining_pct = max(0, 100.0 - current_allocated)
                            target_pct = asset_data.get("target", 0)
                            
                            # Calculate dollar amounts - use ACTUAL spend from purchases
                            target_budget = (target_pct / 100) * prof['principal']
                            purchases = asset_data.get("purchases", [])
                            actual_spent = sum(p.get("amount", 0) for p in purchases)
                            remaining_budget = max(0, target_budget - actual_spent)
                            
                            # Calculate TOTAL undeployed cash across entire portfolio
                            # This is critical - user might have less total cash than per-asset remaining budget
                            total_deployed_all = 0
                            for t_check, a_check in assets.items():
                                purchases_check = a_check.get("purchases", [])
                                total_deployed_all += sum(p.get("amount", 0) for p in purchases_check)
                            
                            total_undeployed_cash = prof['principal'] - total_deployed_all
                            
                            # STRICT PER-ASSET DEPLOYMENT: Each asset has its own budget envelope
                            # Can only deploy up to the asset's target allocation
                            # This maintains target allocations throughout deployment
                            # 100% deployed = when remaining budget can't buy 1 unit of the asset
                            actual_available_budget = min(remaining_budget, total_undeployed_cash)
                            
                            # Display with consistent rounding
                            display_allocated = min(round(current_allocated), 100)
                            display_remaining = max(round(remaining_pct), 0)
                            
                            # Make text bigger and more prominent
                            st.markdown(f"### {selected_ticker}: Target ${target_budget:,.0f} ({target_pct}% of portfolio)")
                            st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 12px;'><strong>Deployed:</strong> ${actual_spent:,.0f} ({display_allocated}%) • <strong>Budget Remaining:</strong> ${remaining_budget:,.0f}</div>", unsafe_allow_html=True)
                            
                            # CRITICAL: Check smart "100% deployed" FIRST (before showing budget display)
                            # Asset is 100% deployed when remaining budget can't buy 1 unit
                            is_asset_fully_deployed = False
                            current_price_for_check = None
                            try:
                                t_obj = yf.Ticker(selected_ticker)
                                hist = t_obj.history(period="1d")
                                if not hist.empty:
                                    current_price_for_check = float(hist['Close'].iloc[-1])
                                    # Check if remaining budget can afford 1 unit
                                    if remaining_budget < current_price_for_check:
                                        is_asset_fully_deployed = True
                            except:
                                # Fallback to old threshold if price fetch fails
                                if current_allocated >= 99.5 or remaining_pct < 0.5:
                                    is_asset_fully_deployed = True
                            
                            if is_asset_fully_deployed:
                                # Asset is 100% deployed - show success message only
                                st.markdown("---")
                                st.success(f"""
                                    ✅ **{selected_ticker} is 100% Deployed!**
                                    
                                    Deployed: ${actual_spent:,.0f} ({display_allocated}% of target)
                                    Remaining budget: ${remaining_budget:,.2f}
                                    {f"Current price: ${current_price_for_check:,.2f}/unit" if current_price_for_check else ""}
                                    
                                    **Remaining budget can't buy 1 unit** (fractional remainder only)
                                    
                                    💡 This is normal! You've maximized deployment for this asset.
                                """)
                                st.info("✅ Select another asset to continue deploying.")
                            else:
                                # Asset still has deployable budget - show budget display
                                st.markdown("---")
                                st.markdown("### 💰 Per-Asset Budget Allocation")
                                
                                col_b1, col_b2 = st.columns(2)
                                with col_b1:
                                    st.metric(
                                        label=f"{selected_ticker}'s Budget",
                                        value=f"${target_budget:,.0f}",
                                        delta=f"${remaining_budget:,.0f} remaining"
                                    )
                                with col_b2:
                                    st.metric(
                                        label="💵 Can Deploy Now",
                                        value=f"${actual_available_budget:,.0f}",
                                        delta=f"Limited by asset budget"
                                    )
                                
                                # Show budget constraint explanation
                                if remaining_budget <= 0:
                                    st.success(f"""
                                        ✅ **{selected_ticker} Target Reached**
                                        
                                        You've deployed ${actual_spent:,.0f} to {selected_ticker}.
                                        This meets or exceeds the {target_pct}% target allocation.
                                    """)
                                elif total_undeployed_cash < remaining_budget:
                                    st.info(f"""
                                        ℹ️ **Portfolio Cash Constraint**
                                        
                                        {selected_ticker}'s budget has ${remaining_budget:,.0f} remaining,
                                        but you only have ${total_undeployed_cash:,.0f} total undeployed cash.
                                        
                                        **Available to deploy:** ${actual_available_budget:,.0f}
                                        
                                        💡 Deploy to all assets to free up more budget.
                                    """)
                                else:
                                    st.success(f"""
                                        ✅ **Ready to Deploy**
                                        
                                        You can deploy up to ${actual_available_budget:,.0f} to {selected_ticker}.
                                        This stays within the {target_pct}% target allocation.
                                    """)
                            
                            if not is_asset_fully_deployed:
                                # Deployment method selection
                                st.markdown("#### Choose Deployment Method")
                                deploy_method = st.radio("", ["By Percentage", "By Units"], 
                                                        horizontal=True, key="deploy_method_radio",
                                                        label_visibility="collapsed")
                                
                                # Enhanced date selection with Clear and Today buttons
                                st.markdown("#### Select Purchase Date")
                                deploy_date = enhanced_date_input(
                                    "Deployment Date",
                                    value=date.today(),
                                    max_value=date.today(),
                                    key="deploy_date",
                                    help="Date you purchased this asset"
                                )
                                
                                # Handle None (from Clear button) - default to today
                                if deploy_date is None:
                                    deploy_date = date.today()
                                
                                # Fetch price for preview
                                preview_price = None
                                preview_price_date = None
                                try:
                                    t_obj = yf.Ticker(selected_ticker)
                                    if deploy_date == date.today():
                                        hist = t_obj.history(period="1d")
                                    else:
                                        start_d = pd.to_datetime(deploy_date) - timedelta(days=7)
                                        end_d = pd.to_datetime(deploy_date) + timedelta(days=1)
                                        hist = t_obj.history(start=start_d, end=end_d)
                                    
                                    if not hist.empty:
                                        hist.index = pd.to_datetime(hist.index).date
                                        if deploy_date in hist.index:
                                            preview_price = float(hist.loc[deploy_date]['Close'])
                                            preview_price_date = deploy_date
                                        else:
                                            available_dates = [d for d in hist.index if d <= deploy_date]
                                            if available_dates:
                                                preview_price_date = max(available_dates)
                                                preview_price = float(hist.loc[preview_price_date]['Close'])
                                except:
                                    pass
                                
                                # Show price info - make it bigger and more visible
                                if preview_price:
                                    p_flag = "🇺🇸" if prof.get("currency") == "USD" else "🇨🇦"
                                    st.markdown(f"""
                                    <div style="background: #e0f2fe; border-left: 4px solid #0284c7; padding: 16px; border-radius: 8px; margin: 12px 0;">
                                        <div style="font-size: 1.2rem; font-weight: 600; color: #0c4a6e;">
                                            📈 Price on {preview_price_date}: {p_flag} ${preview_price:,.2f}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    if preview_price_date != deploy_date:
                                        st.caption(f"ℹ️ Using {preview_price_date} price (closest trading day)")
                                
                                # Initialize variables
                                deploy_pct = 0
                                deploy_amount = 0
                                estimated_units = 0
                                exceeds_limit = False
                                
                                if deploy_method == "By Percentage":
                                    # STRICT PER-ASSET DEPLOYMENT: Cap at remaining % for this asset
                                    # Calculate max % based on remaining asset budget
                                    max_deployable_pct = remaining_pct
                                    
                                    # ALWAYS default to 100% (or remaining % if less than 100%)
                                    # No session state memory - clean default every time
                                    default_pct = min(100.0, remaining_pct) if remaining_pct > 0 else 0.1
                                    
                                    deploy_pct = st.number_input("Deploy % (of asset's target)", 
                                                                min_value=0.1, 
                                                                max_value=max(0.1, max_deployable_pct),
                                                                value=max(0.1, default_pct), 
                                                                step=0.1, 
                                                                key="deploy_pct_input",
                                                                help="Percentage of this asset's target allocation to deploy")
                                    
                                    portfolio_pct = (deploy_pct / 100) * target_pct
                                    deploy_amount = (portfolio_pct / 100) * prof['principal']
                                    
                                    # Validate against actual available budget (per-asset limit)
                                    if deploy_amount > actual_available_budget:
                                        deploy_amount = actual_available_budget
                                        st.caption(f"⚠️ Capped at ${actual_available_budget:,.0f} (asset budget limit)")
                                    
                                    if preview_price:
                                        # Round to whole units (can't buy fractional shares)
                                        estimated_units = round(deploy_amount / preview_price)
                                        if estimated_units < 1:
                                            st.warning(f"⚠️ This percentage results in less than 1 unit. Increase the percentage or use 'By Units' with 1 unit.")
                                            estimated_units = 0
                                            deploy_amount = 0
                                        else:
                                            # Recalculate actual amount based on whole units
                                            deploy_amount = estimated_units * preview_price
                                            # Recalculate actual deploy_pct based on final amount
                                            portfolio_pct = (deploy_amount / prof['principal']) * 100
                                            deploy_pct = (portfolio_pct / target_pct) * 100 if target_pct > 0 else 0
                                else:
                                    # By Units - calculate max units allowed (whole units only)
                                    # Use ACTUAL available budget (min of per-asset and total portfolio cash)
                                    if preview_price:
                                        max_units = int(actual_available_budget / preview_price)
                                        
                                        if max_units < 1:
                                            st.warning(f"""
                                                ⚠️ **Can't Buy Whole Units**
                                                
                                                Available budget: ${actual_available_budget:,.2f}  
                                                Price per unit: ${preview_price:,.2f}  
                                                **Not enough for 1 share!**
                                                
                                                **Your options:**
                                                1. Switch to "By Percentage" method (fractional allocation)
                                                2. Select a different asset (with lower price)
                                                3. Add more capital to reach next share
                                                4. Use "Deploy All Remaining Cash" button in Capital Overview
                                            """)
                                            
                                            # Show what this budget could buy from other assets
                                            other_assets = [t for t in prof.get("assets", {}).keys() if t != selected_ticker]
                                            if other_assets and len(other_assets) > 0:
                                                st.caption(f"💡 **Tip:** This ${actual_available_budget:,.2f} might be enough for other assets in your portfolio")
                                            
                                            estimated_units = 0
                                            deploy_amount = 0
                                            deploy_pct = 0
                                        else:
                                            st.caption(f"💡 Max whole units for available budget: {max_units:,} (${actual_available_budget:,.0f} / ${preview_price:.2f})")
                                            
                                            # Default to max_units (user can override to deploy less)
                                            default_units = max_units
                                            deploy_units = st.number_input("Number of Units", min_value=1, max_value=max_units,
                                                                          value=default_units, step=1, key="deploy_units_input",
                                                                          help=f"Defaults to max ({max_units:,} units). You can deploy fewer if needed.")
                                            
                                            deploy_amount = deploy_units * preview_price
                                            estimated_units = deploy_units
                                            # Calculate equivalent deploy_pct
                                            portfolio_pct = (deploy_amount / prof['principal']) * 100
                                            deploy_pct = (portfolio_pct / target_pct) * 100 if target_pct > 0 else 0
                                            
                                            # FLEXIBLE DEPLOYMENT: Only check if exceeds total portfolio cash
                                            # Allow exceeding per-asset target to maximize deployment
                                            if deploy_amount > actual_available_budget + 0.01:
                                                exceeds_limit = True
                                            # Note: Removed per-asset allocation check - flexible deployment allows over-target
                                    else:
                                        deploy_units = st.number_input("Number of Units", min_value=1, value=1, 
                                                                      step=1, key="deploy_units_input")
                                        deploy_amount = 0
                                        estimated_units = deploy_units
                                        deploy_pct = 0
                                
                                # Display deployment preview
                                if preview_price:
                                    new_total_pct = min(current_allocated + deploy_pct, 100.0)
                                    new_total_spent = actual_spent + deploy_amount
                                    
                                    st.markdown(f'''
                                        <div class="buying-guide" style="font-size: 1.05rem;">
                                            <div style="margin-bottom: 10px; font-size: 1.2rem;"><strong>📊 Deployment Preview:</strong></div>
                                            <div style="margin-bottom: 6px;">• <strong>Units:</strong> <span class="buying-guide-highlight" style="font-size: 1.15rem;">{int(estimated_units):,} units</span></div>
                                            <div style="margin-bottom: 6px;">• <strong>Estimated Cost:</strong> ${deploy_amount:,.2f} (based on ${preview_price:,.2f}/unit)</div>
                                            <div style="margin-bottom: 6px;">• <strong>Asset Target Budget:</strong> ${target_budget:,.2f} ({target_pct}% of ${prof['principal']:,.0f})</div>
                                            <div style="margin-bottom: 6px;">• <strong>Already Spent:</strong> ${actual_spent:,.2f} ({current_allocated:.1f}%)</div>
                                        </div>
                                    ''', unsafe_allow_html=True)
                                    
                                    # Actual price input - user enters what they actually paid
                                    st.markdown("---")
                                    st.markdown("### 💰 Enter Actual Purchase Details")
                                    st.caption("After buying at your broker, enter the actual price you paid (pre-filled with estimated price)")
                                    
                                    # Enhancement 1: Default to preview_price to align with Deployment Preview
                                    # Use dynamic key to ensure widget refreshes when date/units change
                                    price_key = f"actual_deploy_price_{selected_ticker}_{deploy_date}_{int(estimated_units)}"
                                    
                                    actual_price = st.number_input(
                                        f"Actual Price Paid (per unit)",
                                        min_value=0.01,
                                        value=float(preview_price),
                                        step=0.01,
                                        format="%.2f",
                                        key=price_key,
                                        help="Defaults to estimated price. Update with your actual broker price if different."
                                    )
                                    
                                    # Recalculate with actual price
                                    actual_deploy_amount = int(estimated_units) * actual_price
                                    new_total_spent_actual = actual_spent + actual_deploy_amount
                                    
                                    # Show price difference if any
                                    price_diff = actual_price - preview_price
                                    price_diff_pct = (price_diff / preview_price) * 100 if preview_price > 0 else 0
                                    
                                    if abs(price_diff) > 0.01:
                                        diff_color = "#ef4444" if price_diff > 0 else "#10b981"
                                        diff_icon = "📈" if price_diff > 0 else "📉"
                                        st.caption(f"{diff_icon} Price difference: ${price_diff:+.2f} ({price_diff_pct:+.1f}%) vs estimated")
                                    
                                    st.markdown(f'''
                                        <div style="background: #f0fdf4; border: 1px solid #10b981; border-radius: 8px; padding: 12px; margin-top: 8px;">
                                            <div style="font-weight: 600; color: #065f46; margin-bottom: 4px;">✅ Final Deployment:</div>
                                            <div style="color: #047857;">• <strong>{int(estimated_units):,} units</strong> @ <strong>${actual_price:,.2f}</strong> = <strong>${actual_deploy_amount:,.2f}</strong></div>
                                            <div style="color: #047857; font-size: 0.85rem;">• After deploy: ${new_total_spent_actual:,.2f} ({new_total_pct:.1f}% of target)</div>
                                        </div>
                                    ''', unsafe_allow_html=True)
                                    
                                    # Warning if exceeds limit
                                    if exceeds_limit:
                                        over_amount = deploy_amount - actual_available_budget
                                        if over_amount > 0:
                                            # Actually over budget
                                            max_whole_units = int(actual_available_budget / preview_price)
                                            st.error(f"⚠️ This exceeds available budget by ${over_amount:,.2f}. Max units: {max_whole_units:,} (${actual_available_budget:,.0f} available).")
                                        else:
                                            # Exceeds per-asset target allocation (but under total portfolio budget)
                                            st.warning(f"⚠️ This exceeds {selected_ticker}'s target allocation. Consider rebalancing other assets first.")
                                else:
                                    st.warning(f"⚠️ Could not fetch price for {deploy_date}.")
                                    actual_price = None
                                    actual_deploy_amount = 0
                                
                                can_deploy = preview_price is not None and deploy_pct > 0 and not exceeds_limit and estimated_units >= 1
                                
                                # Additional validation: check if this would cause over-deployment
                                validation_error = None
                                if can_deploy and actual_price:
                                    # Calculate total deployed across ALL assets after this deployment
                                    total_deployed_all_assets = 0
                                    for t, a in assets.items():
                                        purchases = a.get("purchases", [])
                                        total_deployed_all_assets += sum(p.get("amount", 0) for p in purchases)
                                    
                                    # Add this new deployment
                                    total_after_deploy = total_deployed_all_assets + actual_deploy_amount
                                    
                                    # Check 1: Would exceed principal?
                                    if total_after_deploy > prof['principal']:
                                        over_amt = total_after_deploy - prof['principal']
                                        validation_error = f"❌ This would over-deploy by ${over_amt:,.2f}! You'd have ${total_after_deploy:,.2f} deployed but only ${prof['principal']:,.2f} principal."
                                        can_deploy = False
                                    
                                    # Check 2: Would exceed asset target by too much?
                                    elif new_total_spent_actual > target_budget * 1.01:  # Allow 1% buffer for rounding
                                        over_amt = new_total_spent_actual - target_budget
                                        validation_error = f"⚠️ This would exceed {selected_ticker}'s target by ${over_amt:,.2f}. Target: ${target_budget:,.2f}"
                                        can_deploy = False
                                
                                if validation_error:
                                    st.error(validation_error)
                                
                                if st.button("📥 Record Deployment", type="primary", use_container_width=True, 
                                            key="record_deploy_btn", disabled=not can_deploy):
                                    try:
                                        price = actual_price  # Use actual price entered by user
                                        quantity = int(estimated_units)
                                        final_amount = actual_deploy_amount  # Use actual amount
                                        
                                        # FINAL validation before saving
                                        total_deployed_check = 0
                                        for t, a in assets.items():
                                            purchases = a.get("purchases", [])
                                            total_deployed_check += sum(p.get("amount", 0) for p in purchases)
                                        
                                        if total_deployed_check + final_amount > prof['principal']:
                                            st.error(f"❌ Cannot deploy: This would exceed your principal of ${prof['principal']:,.2f}")
                                        else:
                                            purchase = {"date": str(deploy_date), "deploy_pct": deploy_pct,
                                                       "amount": final_amount, "price": price, "quantity": quantity}
                                            asset_data.setdefault("purchases", []).append(purchase)
                                            asset_data["units"] = asset_data.get("units", 0) + quantity
                                            
                                            # Recalculate allocated_pct from scratch (not incremental)
                                            # This ensures accuracy if principal or targets changed
                                            all_purchases = asset_data.get("purchases", [])
                                            total_spent_on_asset = sum(p.get("amount", 0) for p in all_purchases)
                                            current_target_amount = (asset_data.get("target", 0) / 100) * prof['principal']
                                            asset_data["allocated_pct"] = min(100.0, (total_spent_on_asset / current_target_amount * 100)) if current_target_amount > 0 else 0
                                            
                                            log_profile(prof, f"Deployed {quantity:,} units of {selected_ticker} (${final_amount:,.2f} @ ${price:.2f})")
                                            save_db(st.session_state.db)
                                            st.success(f"✅ Deployed {quantity:,} units of {selected_ticker} @ ${price:.2f}")
                                            if asset_data['allocated_pct'] >= 100.0:
                                                st.balloons()
                                            st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Error: {str(e)}")
            
            # Capital Overview Section
            st.divider()
            st.markdown("### 💰 Capital Overview")
            
            # Calculate total deployed from purchases
            total_deployed_capital = 0
            for ticker, asset_data in assets.items():
                purchases = asset_data.get("purchases", [])
                total_deployed_capital += sum(p.get("amount", 0) for p in purchases)
            
            principal_amt = prof['principal']
            undeployed_cash = principal_amt - total_deployed_capital
            deployment_rate = (total_deployed_capital / principal_amt * 100) if principal_amt > 0 else 0
            
            # Check for over-deployment
            is_over_deployed = total_deployed_capital > principal_amt
            
            if is_over_deployed:
                over_deployed_amount = total_deployed_capital - principal_amt
                st.error(f"""
🚨 **CRITICAL: Portfolio Over-Deployed!**

You have deployed MORE than your principal!
- Principal: ${principal_amt:,.2f}
- Deployed: ${total_deployed_capital:,.2f}
- **Over-deployed by: ${over_deployed_amount:,.2f}**

**This is impossible - you can't spend money you don't have!**

**How to fix:**
1. Review your asset deployments below
2. Remove excess purchases to get under ${principal_amt:,.2f}
3. Check for duplicate or incorrect deployments
                """)
            
            # Analyze what CAN still be deployed vs fractional remainder
            deployable_cash = 0
            fractional_cash = 0
            deployment_opportunities = []
            
            if undeployed_cash > 0 and not is_over_deployed:
                import yfinance as yf
                for ticker, asset_data in assets.items():
                    target_pct = asset_data.get("target", 0)
                    target_amount = (target_pct / 100) * principal_amt
                    purchases = asset_data.get("purchases", [])
                    deployed_amount = sum(p.get("amount", 0) for p in purchases)
                    remaining_target = target_amount - deployed_amount
                    
                    if remaining_target > 0:
                        # Get current price
                        try:
                            ticker_obj = yf.Ticker(ticker)
                            hist = ticker_obj.history(period="1d")
                            if not hist.empty:
                                current_price = float(hist['Close'].iloc[-1])
                                shares_can_buy = int(remaining_target / current_price)
                                
                                if shares_can_buy >= 1:
                                    # Can buy at least 1 share
                                    deployable_amount = shares_can_buy * current_price
                                    
                                    # But check if this would exceed principal
                                    if total_deployed_capital + deployable_amount <= principal_amt:
                                        fractional_amount = remaining_target - deployable_amount
                                        
                                        deployable_cash += deployable_amount
                                        fractional_cash += fractional_amount
                                        
                                        deployment_opportunities.append({
                                            "ticker": ticker,
                                            "shares": shares_can_buy,
                                            "amount": deployable_amount,
                                            "price": current_price,
                                            "fund_name": asset_data.get("fund_name", ticker)
                                        })
                                    else:
                                        # Would exceed principal
                                        max_deployable = principal_amt - total_deployed_capital
                                        if max_deployable > current_price:
                                            shares_can_afford = int(max_deployable / current_price)
                                            if shares_can_afford >= 1:
                                                deployable_amount = shares_can_afford * current_price
                                                deployable_cash += deployable_amount
                                                deployment_opportunities.append({
                                                    "ticker": ticker,
                                                    "shares": shares_can_afford,
                                                    "amount": deployable_amount,
                                                    "price": current_price,
                                                    "fund_name": asset_data.get("fund_name", ticker)
                                                })
                                else:
                                    # Can't even buy 1 share - it's fractional
                                    fractional_cash += remaining_target
                        except:
                            # If can't get price, assume it's deployable
                            deployable_cash += remaining_target
            
            # Smart Fractional Detection: Check if undeployed cash can buy even 1 share of cheapest asset
            cheapest_asset_price = None
            asset_prices = {}
            
            if undeployed_cash > 0 and not is_over_deployed:
                import yfinance as yf
                for ticker in assets.keys():
                    try:
                        ticker_obj = yf.Ticker(ticker)
                        hist = ticker_obj.history(period="1d")
                        if not hist.empty:
                            price = float(hist['Close'].iloc[-1])
                            asset_prices[ticker] = price
                            if cheapest_asset_price is None or price < cheapest_asset_price:
                                cheapest_asset_price = price
                    except:
                        pass
            
            # Determine if truly fractional (can't afford even 1 share of cheapest asset)
            is_truly_fractional = False
            if undeployed_cash > 0 and cheapest_asset_price is not None:
                is_truly_fractional = undeployed_cash < cheapest_asset_price
            
            col_cap1, col_cap2 = st.columns(2)
            with col_cap1:
                st.metric("Principal Set", f"${principal_amt:,.0f}")
                st.metric("Capital Deployed", f"${total_deployed_capital:,.0f}")
            with col_cap2:
                if is_over_deployed:
                    st.metric("Over-Deployed!", f"${abs(undeployed_cash):,.0f}",
                             delta=f"{deployment_rate:.1f}% over limit", delta_color="inverse")
                elif is_truly_fractional:
                    # Show success - portfolio is fully deployed
                    st.metric("Undeployed Cash", f"${undeployed_cash:,.0f}",
                             delta="100% deployed", delta_color="normal")
                    st.caption(f"✅ Fractional remainder (can't buy partial shares)")
                else:
                    st.metric("Undeployed Cash", f"${undeployed_cash:,.0f}",
                             delta=f"{deployment_rate:.1f}% deployed" if undeployed_cash > 0 else None)
                    if undeployed_cash > 0:
                        if deployable_cash > 0:
                            st.caption(f"⚠️ ${deployable_cash:,.0f} can still be deployed!")
                        if fractional_cash > 0:
                            st.caption(f"💡 ${fractional_cash:,.0f} fractional (can't buy partial shares)")
            
            # Recent Deployment History
            st.markdown("---")
            st.markdown("**📋 Recent Deployments**")
            
            # Collect all purchases with dates
            all_deployments = []
            for ticker, asset_data in assets.items():
                purchases = asset_data.get("purchases", [])
                for purchase in purchases:
                    all_deployments.append({
                        "date": purchase.get("date", "Unknown"),
                        "ticker": ticker,
                        "fund_name": asset_data.get("fund_name", ticker),
                        "quantity": purchase.get("quantity", 0),
                        "price": purchase.get("price", 0),
                        "amount": purchase.get("amount", 0)
                    })
            
            if all_deployments:
                # Sort by date (most recent first)
                all_deployments.sort(key=lambda x: x["date"], reverse=True)
                
                # Show last 5 deployments
                for i, deployment in enumerate(all_deployments[:5]):
                    # Calculate remaining cash at time of this deployment
                    # (Sum all deployments after this one)
                    remaining_after = principal_amt - sum(d["amount"] for d in all_deployments[:i+1])
                    
                    icon = "💰" if i == 0 else "📌"
                    st.caption(f"""{icon} **{deployment['date']}** • {deployment['ticker']}: {deployment['quantity']:.0f} units @ ${deployment['price']:.2f} = ${deployment['amount']:,.2f} • Cash left: ${remaining_after:,.0f}""")
                
                if len(all_deployments) > 5:
                    st.caption(f"_... and {len(all_deployments) - 5} more deployments_")
            else:
                st.caption("_No deployments yet_")
            
            # Show fractional explanation or deployment opportunities
            if is_truly_fractional and undeployed_cash > 0:
                # Show success message with fractional explanation
                st.success(f"""
✅ **Portfolio 100% Deployed!**

You have ${undeployed_cash:,.2f} remaining, which is a **fractional remainder**.

**Why can't this be deployed?**
You can't buy partial shares at brokers. The cheapest asset costs ${cheapest_asset_price:.2f}/share, but you only have ${undeployed_cash:,.2f}.

**This is NORMAL and expected in portfolio management!** Your deployment efficiency of {deployment_rate:.1f}% is excellent.

**Options for ${undeployed_cash:,.2f}:**
- Keep as cash reserve for rebalancing (recommended)
- Add more capital to reach next share (see button below)
- Add to next capital injection
                """)
                
                # Add Capital button
                if st.button("➕ Add More Capital to Portfolio", use_container_width=True, key="add_capital_btn"):
                    st.session_state.show_add_capital_form = True
                    st.rerun()
            
            # Show add capital form if triggered
            if st.session_state.get('show_add_capital_form', False):
                with st.form("add_capital_form"):
                    st.markdown("### ➕ Add Capital to Portfolio")
                    st.caption("Inject additional capital into your portfolio")
                    
                    current_principal = prof['principal']
                    st.info(f"Current Principal: ${current_principal:,.2f}")
                    
                    # Calculate suggested amount to buy 1 more share of cheapest asset
                    if cheapest_asset_price and is_truly_fractional:
                        suggested = cheapest_asset_price - undeployed_cash + 1
                        st.caption(f"💡 Suggested: ${suggested:.2f} (enough to buy 1 share of cheapest asset)")
                    
                    additional_amount = st.number_input(
                        "Additional Capital Amount",
                        min_value=0.01,
                        value=float(cheapest_asset_price) if cheapest_asset_price and is_truly_fractional else 1000.0,
                        step=100.0,
                        format="%.2f",
                        help="Amount to add to your portfolio principal"
                    )
                    
                    new_principal = current_principal + additional_amount
                    st.markdown(f"**New Principal:** ${new_principal:,.2f}")
                    st.caption(f"Increase: +${additional_amount:,.2f} ({(additional_amount/current_principal*100):.2f}%)")
                    
                    col_submit, col_cancel = st.columns(2)
                    with col_submit:
                        submit_add = st.form_submit_button("✅ Add Capital", type="primary", use_container_width=True)
                    with col_cancel:
                        cancel_add = st.form_submit_button("❌ Cancel", use_container_width=True)
                    
                    if submit_add:
                        # Update principal
                        prof['principal'] = new_principal
                        log_profile(prof, f"Added capital: ${additional_amount:,.2f} (Principal: ${current_principal:,.2f} → ${new_principal:,.2f})")
                        save_db(st.session_state.db)
                        st.session_state.show_add_capital_form = False
                        st.success(f"✅ Added ${additional_amount:,.2f} to portfolio! New principal: ${new_principal:,.2f}")
                        st.balloons()
                        st.rerun()
                    
                    if cancel_add:
                        st.session_state.show_add_capital_form = False
                        st.rerun()
            
            # Show deployment opportunities if available (and NOT truly fractional)
            # Enhancement 3: Only show if all assets are fully deployed (100%)
            all_assets_deployed = all(
                asset_data.get("allocated_pct", 0) >= 99.5 
                for asset_data in assets.values()
            ) if assets else False
            
            if deployment_opportunities and not is_truly_fractional and all_assets_deployed:
                # Enhancement 4: Use smaller headings to match sidebar text size
                st.markdown("#### 🚀 Deploy All Remaining Cash")
                st.caption(f"Deploy ${deployable_cash:,.0f} remaining across your portfolio with actual broker prices")
                
                # Initialize session state for actual prices if not exists
                if "deploy_all_actual_prices" not in st.session_state:
                    st.session_state.deploy_all_actual_prices = {}
                
                # Show deployment opportunities with editable prices
                st.markdown("**Estimated Deployment Plan**")
                st.caption("Review estimated units and update with actual broker prices before deploying")
                
                total_estimated_cost = 0
                total_actual_cost = 0
                
                for idx, opp in enumerate(deployment_opportunities):
                    ticker = opp['ticker']
                    estimated_price = opp['price']
                    estimated_shares = opp['shares']
                    estimated_amount = opp['amount']
                    
                    # Initialize actual price to estimated price if not set
                    price_key = f"{ticker}_{date.today()}"
                    if price_key not in st.session_state.deploy_all_actual_prices:
                        st.session_state.deploy_all_actual_prices[price_key] = estimated_price
                    
                    total_estimated_cost += estimated_amount
                    
                    # Create expandable section for each asset
                    with st.expander(f"**{ticker}** - {opp['fund_name']}", expanded=True):
                        col1, col2, col3 = st.columns([2, 2, 2])
                        
                        with col1:
                            st.markdown("**Estimated**")
                            st.metric("Units", f"{estimated_shares:,}", help="Whole shares to buy")
                            st.metric("Price/Unit", f"${estimated_price:.2f}", help="Current market price")
                            st.metric("Total Cost", f"${estimated_amount:,.2f}", help="Estimated total")
                        
                        with col2:
                            st.markdown("**Actual Broker Price**")
                            actual_price = st.number_input(
                                "Price Paid per Unit",
                                min_value=0.01,
                                value=float(st.session_state.deploy_all_actual_prices[price_key]),
                                step=0.01,
                                format="%.2f",
                                key=f"actual_price_deploy_all_{ticker}_{idx}",
                                help="Enter the exact price you paid at your broker"
                            )
                            st.session_state.deploy_all_actual_prices[price_key] = actual_price
                            
                            # Calculate actual cost
                            actual_cost = estimated_shares * actual_price
                            total_actual_cost += actual_cost
                            
                            # Show price difference
                            price_diff = actual_price - estimated_price
                            price_diff_pct = (price_diff / estimated_price) * 100 if estimated_price > 0 else 0
                            
                            if abs(price_diff) > 0.01:
                                diff_color = "#ef4444" if price_diff > 0 else "#10b981"
                                diff_icon = "📈" if price_diff > 0 else "📉"
                                st.caption(f"{diff_icon} {price_diff:+.2f} ({price_diff_pct:+.1f}%) vs estimated")
                            else:
                                st.caption("✅ Matches estimate")
                        
                        with col3:
                            st.markdown("**Final Deployment**")
                            st.metric("Units", f"{estimated_shares:,}", help="Shares to deploy")
                            st.metric("Actual Price", f"${actual_price:.2f}", help="Your broker price")
                            st.metric("Actual Total", f"${actual_cost:,.2f}", 
                                     delta=f"{actual_cost - estimated_amount:+,.2f}" if abs(actual_cost - estimated_amount) > 0.01 else None,
                                     help="Total you'll actually pay")
                
                # Summary section
                st.markdown("---")
                col_summary1, col_summary2, col_summary3 = st.columns(3)
                
                with col_summary1:
                    st.markdown("**📊 Summary**")
                    st.metric("Assets to Deploy", len(deployment_opportunities))
                    st.metric("Available Cash", f"${deployable_cash:,.0f}")
                
                with col_summary2:
                    st.markdown("**💰 Estimated**")
                    st.metric("Total Cost", f"${total_estimated_cost:,.2f}")
                    st.metric("Remaining", f"${deployable_cash - total_estimated_cost:,.2f}")
                
                with col_summary3:
                    st.markdown("**✅ Actual**")
                    st.metric("Total Cost", f"${total_actual_cost:,.2f}",
                             delta=f"{total_actual_cost - total_estimated_cost:+,.2f}" if abs(total_actual_cost - total_estimated_cost) > 0.01 else None)
                    st.metric("Remaining", f"${deployable_cash - total_actual_cost:,.2f}")
                
                # Validation and warnings
                if total_actual_cost > deployable_cash:
                    st.error(f"⚠️ Actual cost (${total_actual_cost:,.2f}) exceeds available cash (${deployable_cash:,.2f}) by ${total_actual_cost - deployable_cash:,.2f}. Reduce units or adjust prices.")
                    can_deploy = False
                elif total_actual_cost < deployable_cash - 100:
                    st.info(f"💡 You'll have ${deployable_cash - total_actual_cost:,.2f} left after deployment. This is normal for fractional remainders.")
                    can_deploy = True
                else:
                    can_deploy = True
                
                # Deploy button with confirmation
                st.markdown("---")
                col_cancel, col_deploy = st.columns([1, 2])
                
                with col_cancel:
                    if st.button("❌ Cancel", use_container_width=True, key="cancel_deploy_all"):
                        st.session_state.deploy_all_actual_prices = {}
                        st.info("Deployment cancelled")
                        st.rerun()
                
                with col_deploy:
                    if st.button("✅ Confirm & Deploy All", 
                                 type="primary", 
                                 use_container_width=True, 
                                 disabled=not can_deploy,
                                 key="deploy_all_remaining"):
                        # Execute all deployments with actual prices
                        deployed_assets = []
                        total_deployed = 0
                        
                        for opp in deployment_opportunities:
                            ticker = opp['ticker']
                            shares = opp['shares']
                            price_key = f"{ticker}_{date.today()}"
                            actual_price = st.session_state.deploy_all_actual_prices.get(price_key, opp['price'])
                            actual_amount = shares * actual_price
                            
                            asset_data = assets[ticker]
                            target_pct = asset_data.get("target", 0)
                            target_amount = (target_pct / 100) * principal_amt
                            
                            # Add purchase with actual price
                            purchase = {
                                "date": str(date.today()),
                                "deploy_pct": (actual_amount / target_amount) * 100,
                                "amount": actual_amount,
                                "price": actual_price,
                                "units": shares  # Use "units" for consistency
                            }
                            asset_data.setdefault("purchases", []).append(purchase)
                            asset_data["units"] = asset_data.get("units", 0) + shares
                            
                            # Update allocated percentage based on actual spend
                            purchases = asset_data.get("purchases", [])
                            total_spent = sum(p.get("amount", 0) for p in purchases)
                            asset_data["allocated_pct"] = min(100.0, (total_spent / target_amount) * 100)
                            
                            deployed_assets.append(ticker)
                            total_deployed += actual_amount
                            
                            log_profile(prof, f"Auto-deployed {shares:,} units of {ticker} @ ${actual_price:.2f} (${actual_amount:,.2f} actual cost)")
                        
                        save_db(st.session_state.db)
                        
                        # Clear actual prices from session state
                        st.session_state.deploy_all_actual_prices = {}
                        
                        st.success(f"✅ Successfully deployed ${total_deployed:,.2f} across {len(deployed_assets)} assets!")
                        st.balloons()
                        st.rerun()
            
            # Activity Log
            st.divider()
            st.markdown("### 📜 Activity Log")
            with st.expander("View Recent Activity", expanded=False):
                all_logs = prof.get("rebalance_logs", [])
                if all_logs:
                    for log_entry in all_logs[:20]:
                        st.caption(f"**{log_entry['date']}**: {log_entry['event']}")
                else:
                    st.caption("No activity yet")
        
        # Account section
        st.divider()
        st.markdown("### 👤 Account")
        
        with st.expander("🔘 Change Password", expanded=False):
            with st.form("change_pwd_form"):
                old_pwd = st.text_input("Current Password", type="password")
                new_pwd = st.text_input("New Password", type="password")
                new_pwd2 = st.text_input("Confirm New Password", type="password")
                if st.form_submit_button("Update Password", use_container_width=True):
                    if new_pwd != new_pwd2:
                        st.error("Passwords don't match")
                    else:
                        success, msg = change_password(st.session_state.db, current_user, old_pwd, new_pwd)
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)
        
        # Notification Preferences (only show if email is enabled globally)
        global_settings = st.session_state.db.get("global_settings", {})
        email_enabled_globally = global_settings.get("email_notifications_enabled", False)
        
        if email_enabled_globally:
            with st.expander("📧 Notification Preferences", expanded=False):
                user_settings = user_data.get("settings", {})
                current_email = user_data.get("email", "")
                
                with st.form("notification_prefs_form"):
                    notif_email = st.text_input("Notification Email", value=current_email,
                                               help="Email address for receiving alerts")
                    
                    st.markdown("**Email Notifications:**")
                    email_rebalance = st.checkbox("🚨 Rebalance Needed Alerts", 
                                                  value=user_settings.get("email_rebalance_alerts", False),
                                                  help="Get notified when portfolios need rebalancing (max once per 24h)")
                    email_confirmation = st.checkbox("✅ Rebalance Confirmation Emails", 
                                                     value=user_settings.get("email_rebalance_confirmation", False),
                                                     help="Receive detailed summary after executing a rebalance")
                    
                    if st.form_submit_button("💾 Save Preferences", use_container_width=True):
                        if "settings" not in st.session_state.db["users"][current_user]:
                            st.session_state.db["users"][current_user]["settings"] = {}
                        st.session_state.db["users"][current_user]["email"] = notif_email
                        st.session_state.db["users"][current_user]["settings"]["email_rebalance_alerts"] = email_rebalance
                        st.session_state.db["users"][current_user]["settings"]["email_rebalance_confirmation"] = email_confirmation
                        save_db(st.session_state.db)
                        st.success("✅ Notification preferences saved!")
                        st.rerun()
        
        # ===== AI ASSISTANT CHAT =====
        ai_settings = st.session_state.db.get("global_settings", {})
        ai_enabled = ai_settings.get("ai_assistant_enabled", False)
        ai_api_key = ai_settings.get("ai_assistant_api_key", "")
        
        if ai_enabled and ai_api_key:
            st.divider()
            st.markdown("### 🤖 AI Assistant")
            
            # Initialize chat history
            if "ai_chat_history" not in st.session_state:
                st.session_state.ai_chat_history = []
            
            with st.expander("💬 Ask me anything about the app", expanded=False):
                # Display chat history
                chat_container = st.container()
                with chat_container:
                    if not st.session_state.ai_chat_history:
                        st.caption("👋 Hi! I can help you understand how to use this portfolio app. Ask me anything!")
                    
                    for msg in st.session_state.ai_chat_history[-6:]:  # Show last 6 messages
                        if msg["role"] == "user":
                            st.markdown(f"**You:** {msg['content']}")
                        else:
                            st.markdown(f"**🤖 Assistant:** {msg['content']}")
                
                # Input for new message
                user_input = st.text_input("Type your question...", key="ai_user_input", 
                                          placeholder="e.g., How do I rebalance?")
                
                col_send, col_clear = st.columns([3, 1])
                with col_send:
                    if st.button("📤 Send", use_container_width=True, key="ai_send_btn"):
                        if user_input.strip():
                            # Add user message to history
                            st.session_state.ai_chat_history.append({
                                "role": "user", 
                                "content": user_input
                            })
                            
                            # Get AI response
                            with st.spinner("Thinking..."):
                                response = get_ai_response(
                                    user_input, 
                                    st.session_state.ai_chat_history[:-1],  # Exclude current message
                                    ai_api_key
                                )
                            
                            # Add assistant response to history
                            st.session_state.ai_chat_history.append({
                                "role": "assistant",
                                "content": response
                            })
                            
                            st.rerun()
                
                with col_clear:
                    if st.button("🗑️", use_container_width=True, key="ai_clear_btn", help="Clear chat"):
                        st.session_state.ai_chat_history = []
                        st.rerun()
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            log_system_event(st.session_state.db, "logout", f"User logged out: {current_user}", current_user)
            save_db(st.session_state.db)
            log_activity(st.session_state.db, current_user, "user_logout", "User logged out", "")
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.session_token = None
            st.session_state.active_profile = None
            st.rerun()

    # ===== MAIN CONTENT AREA =====
    if view_mode == "Admin Dashboard" and is_admin_user and not impersonating_user:
        # Auto-refresh data to show latest users (v7.2.1 fix)
        if 'admin_dashboard_loaded' not in st.session_state:
            st.session_state.db = load_db()
            st.session_state.admin_dashboard_loaded = True
        
        show_admin_dashboard(st.session_state.db, actual_user)
    
    elif view_mode == "Global Dashboard":
        # Show impersonation warning if admin is viewing as another user
        if is_admin_user and impersonating_user:
            st.markdown(f"""
                <div class="warning-banner">
                    <h4>⚠️ Admin Impersonation Mode</h4>
                    <p style="margin: 0;">You are viewing <strong>{current_user}</strong>'s account. All actions will affect this user's data.</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Get user profiles
        profiles = get_user_profiles(st.session_state.db, current_user)
        
        # Check if user has created any profiles (even if not deployed)
        # Show dashboard if ANY profile exists, regardless of deployment status
        has_any_profiles = len(profiles) > 0
        
        # Show welcome page ONLY for brand new users with zero profiles
        if not has_any_profiles:
            # ===== FIRST-TIME USER WELCOME EXPERIENCE =====
            
            # Hero Section
            user_display_name = user_data.get('display_name', current_user)
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; padding: 60px 40px; border-radius: 20px; text-align: center; 
                            margin-bottom: 40px; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);">
                    <h1 style="font-size: 3rem; margin: 0 0 20px 0; font-weight: 700; color: white;">
                        🎉 Welcome, {user_display_name}!
                    </h1>
                    <p style="font-size: 1.4rem; margin: 0 0 15px 0; opacity: 0.95; color: white; font-weight: 500;">
                        Your Portfolio Command Center Awaits
                    </p>
                    <p style="font-size: 1.1rem; margin: 0; opacity: 0.9; color: white;">
                        Institutional-grade portfolio management, simplified for you 📊
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Quick Start Guide
            st.markdown("## 🚀 Quick Start Guide")
            st.caption("Follow these steps to set up your first portfolio")
            
            col_step1, col_step2, col_step3 = st.columns(3)
            
            with col_step1:
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 30px; border-radius: 15px; height: 100%; 
                                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);">
                        <div style="background: white; width: 60px; height: 60px; border-radius: 50%; 
                                    display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
                            <span style="font-size: 2rem;">①</span>
                        </div>
                        <h3 style="color: white; text-align: center; margin: 0 0 15px 0;">Create Profile</h3>
                        <p style="color: rgba(255,255,255,0.9); text-align: center; margin: 0; font-size: 0.95rem;">
                            Click "📁 Create New Profile" in the sidebar to set up your portfolio strategy
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_step2:
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                                padding: 30px; border-radius: 15px; height: 100%;
                                box-shadow: 0 4px 15px rgba(240, 147, 251, 0.2);">
                        <div style="background: white; width: 60px; height: 60px; border-radius: 50%; 
                                    display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
                            <span style="font-size: 2rem;">②</span>
                        </div>
                        <h3 style="color: white; text-align: center; margin: 0 0 15px 0;">Set Targets</h3>
                        <p style="color: rgba(255,255,255,0.9); text-align: center; margin: 0; font-size: 0.95rem;">
                            Define your asset allocation with target percentages for each holding
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_step3:
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                                padding: 30px; border-radius: 15px; height: 100%;
                                box-shadow: 0 4px 15px rgba(79, 172, 254, 0.2);">
                        <div style="background: white; width: 60px; height: 60px; border-radius: 50%; 
                                    display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
                            <span style="font-size: 2rem;">③</span>
                        </div>
                        <h3 style="color: white; text-align: center; margin: 0 0 15px 0;">Deploy Capital</h3>
                        <p style="color: rgba(255,255,255,0.9); text-align: center; margin: 0; font-size: 0.95rem;">
                            Record your purchases and start tracking performance automatically
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # What You Can Do Section
            st.markdown("## 🎯 What You Can Do")
            st.caption("Transform how you manage your investments")
            
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                st.markdown("""
                    <div style="background: white; padding: 30px 20px; border-radius: 12px; text-align: center;
                                border: 2px solid #667eea; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);">
                        <div style="font-size: 3rem; margin-bottom: 10px;">♾️</div>
                        <div style="font-size: 2rem; font-weight: 700; color: #667eea; margin-bottom: 5px;">Unlimited</div>
                        <div style="color: #64748b; font-size: 0.95rem;">Portfolios</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with stat_col2:
                st.markdown("""
                    <div style="background: white; padding: 30px 20px; border-radius: 12px; text-align: center;
                                border: 2px solid #10b981; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);">
                        <div style="font-size: 3rem; margin-bottom: 10px;">⚡</div>
                        <div style="font-size: 2rem; font-weight: 700; color: #10b981; margin-bottom: 5px;">Real-Time</div>
                        <div style="color: #64748b; font-size: 0.95rem;">Market Data</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with stat_col3:
                st.markdown("""
                    <div style="background: white; padding: 30px 20px; border-radius: 12px; text-align: center;
                                border: 2px solid #f59e0b; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.1);">
                        <div style="font-size: 3rem; margin-bottom: 10px;">🎯</div>
                        <div style="font-size: 2rem; font-weight: 700; color: #f59e0b; margin-bottom: 5px;">Auto</div>
                        <div style="color: #64748b; font-size: 0.95rem;">Drift Alerts</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with stat_col4:
                st.markdown("""
                    <div style="background: white; padding: 30px 20px; border-radius: 12px; text-align: center;
                                border: 2px solid #8b5cf6; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.1);">
                        <div style="font-size: 3rem; margin-bottom: 10px;">📊</div>
                        <div style="font-size: 2rem; font-weight: 700; color: #8b5cf6; margin-bottom: 5px;">Deep</div>
                        <div style="color: #64748b; font-size: 0.95rem;">Analytics</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Feature Highlights
            st.markdown("## ✨ Powerful Features at Your Fingertips")
            
            col_feat1, col_feat2 = st.columns(2)
            
            with col_feat1:
                st.markdown("""
                    <div style="background: white; padding: 25px; border-radius: 12px; 
                                border-left: 4px solid #667eea; margin-bottom: 20px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        <h3 style="margin: 0 0 12px 0; color: #1e293b;">🎯 Automated Drift Detection</h3>
                        <p style="margin: 0; color: #64748b; line-height: 1.6;">
                            Set your tolerance levels and get instant alerts when your portfolio drifts 
                            from target allocation. Never miss a rebalancing opportunity.
                        </p>
                    </div>
                    
                    <div style="background: white; padding: 25px; border-radius: 12px; 
                                border-left: 4px solid #f093fb; margin-bottom: 20px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        <h3 style="margin: 0 0 12px 0; color: #1e293b;">📈 Real-Time Performance Tracking</h3>
                        <p style="margin: 0; color: #64748b; line-height: 1.6;">
                            Monitor portfolio value, returns (CAGR & ROI), and compare against 
                            benchmarks like SPY, QQQ, and VTI in real-time.
                        </p>
                    </div>
                    
                    <div style="background: white; padding: 25px; border-radius: 12px; 
                                border-left: 4px solid #4facfe; margin-bottom: 20px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        <h3 style="margin: 0 0 12px 0; color: #1e293b;">⚖️ Smart Rebalancing Engine</h3>
                        <p style="margin: 0; color: #64748b; line-height: 1.6;">
                            Two-step rebalancing workflow shows exactly what to buy/sell, 
                            manages slippage, and tracks execution history.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_feat2:
                st.markdown("""
                    <div style="background: white; padding: 25px; border-radius: 12px; 
                                border-left: 4px solid #fbbf24; margin-bottom: 20px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        <h3 style="margin: 0 0 12px 0; color: #1e293b;">📊 Multiple Portfolio Management</h3>
                        <p style="margin: 0; color: #64748b; line-height: 1.6;">
                            Manage unlimited portfolios across different accounts 
                            (401k, IRA, Roth IRA, TFSA, RRSP, Taxable). All in one place.
                        </p>
                    </div>
                    
                    <div style="background: white; padding: 25px; border-radius: 12px; 
                                border-left: 4px solid #10b981; margin-bottom: 20px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        <h3 style="margin: 0 0 12px 0; color: #1e293b;">🔔 Email Notifications</h3>
                        <p style="margin: 0; color: #64748b; line-height: 1.6;">
                            Get automatic alerts when portfolios drift beyond your tolerance. 
                            Stay informed without constantly checking.
                        </p>
                    </div>
                    
                    <div style="background: white; padding: 25px; border-radius: 12px; 
                                border-left: 4px solid #8b5cf6; margin-bottom: 20px;
                                box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                        <h3 style="margin: 0 0 12px 0; color: #1e293b;">📜 Complete History & Logs</h3>
                        <p style="margin: 0; color: #64748b; line-height: 1.6;">
                            Every rebalancing action, deployment, and adjustment is logged 
                            with timestamps for perfect record-keeping.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Call to Action with Interactive Button
            col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
            with col_cta2:
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                color: white; padding: 40px; border-radius: 15px; text-align: center;
                                margin-top: 20px; margin-bottom: 20px; box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);">
                        <h2 style="margin: 0 0 15px 0; font-size: 2rem; color: white;">Ready to Take Control?</h2>
                        <p style="margin: 0 0 25px 0; font-size: 1.1rem; opacity: 0.95; color: white;">
                            Create your first investment profile and start building your wealth strategy
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Big CTA Button
                if st.button("🚀 Create My First Portfolio", 
                           use_container_width=True, 
                           type="primary",
                           key="welcome_create_profile"):
                    # Navigate to Portfolio Manager and auto-expand create profile section
                    st.session_state.current_page = "Portfolio Manager"
                    st.session_state.auto_expand_create_profile = True
                    st.rerun()
                
                st.caption("👆 Click here to get started in seconds!")
            
            # Tips Section
            st.markdown("")
            st.markdown("## 💡 Pro Tips")
            
            tip_col1, tip_col2, tip_col3 = st.columns(3)
            
            with tip_col1:
                st.info("""
                    **🎯 Start Simple**  
                    Begin with 3-5 core holdings. You can always add more complexity later as you get comfortable with the system.
                """)
            
            with tip_col2:
                st.success("""
                    **⚖️ Set Drift Tolerance**  
                    5% is a good starting point for most investors. Adjust based on your rebalancing preferences.
                """)
            
            with tip_col3:
                st.warning("""
                    **📈 Track Benchmarks**  
                    Compare against SPY (S&P 500) or VTI (Total Market) to measure your strategy's performance.
                """)
        else:
            # ===== DASHBOARD FOR USERS WITH CONFIGURED PORTFOLIOS =====
            
            # Dashboard Header with Refresh Button
            col_title, col_refresh = st.columns([5, 1])
            with col_title:
                st.title("🏠 Global Portfolio Dashboard")
            with col_refresh:
                # Check if recently refreshed
                last_refresh = st.session_state.get("last_refresh_global", None)
                can_refresh = True
                
                if last_refresh:
                    from datetime import datetime
                    seconds_ago = (datetime.now() - last_refresh).total_seconds()
                    if seconds_ago < 5:
                        can_refresh = False
                        st.caption(f"🕐 {int(seconds_ago)}s ago")
                
                if st.button("🔄 Refresh", 
                             key="refresh_global_dashboard",
                             disabled=not can_refresh,
                             help="Update all portfolios with latest prices",
                             use_container_width=True,
                             type="secondary"):
                    with st.spinner("📊 Fetching latest data for all portfolios..."):
                        # Clear cached data
                        if hasattr(st, 'cache_data'):
                            st.cache_data.clear()
                        st.session_state["last_refresh_global"] = datetime.now()
                        import time
                        time.sleep(0.3)
                    st.success("✅ All portfolios updated!")
                    time.sleep(0.5)
                    st.rerun()
            
            description_box(
                "Portfolio Command Center",
                f"Welcome back, {user_data.get('display_name', current_user)}! Monitor all your investment strategies at a glance."
            )
            
            # Fetch all prices
            all_tickers = set()
            for p in profiles.values():
                all_tickers.update(p.get("assets", {}).keys())
            
            prices = {}
            if all_tickers:
                try:
                    with st.spinner("📊 Fetching market data..."):
                        raw_px = yf.download(list(all_tickers), period="1d", progress=False)['Close']
                        if len(all_tickers) == 1:
                            if not raw_px.empty:
                                prices = {list(all_tickers)[0]: float(raw_px.iloc[-1])}
                        else:
                            for k, v in raw_px.iloc[-1].to_dict().items():
                                try:
                                    if pd.notna(v):
                                        prices[k] = float(v)
                                except:
                                    pass
                except:
                    st.warning("⚠️ Could not fetch current prices.")
            
            # Calculate summary metrics
            total_value = 0
            total_drift_count = 0
            
            for p_data in profiles.values():
                p_assets = p_data.get("assets", {})
                curr_v = float(sum(p_assets[t]["units"] * prices.get(t, 0) for t in p_assets))
                total_value += curr_v
                needs_rebal, _ = calculate_drift_status(p_data, prices)
                if needs_rebal:
                    total_drift_count += 1
            
            # Top Metrics
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.markdown(f'<div class="metric-showcase"><h3>${total_value:,.0f}</h3><p>Total Portfolio Value</p></div>', unsafe_allow_html=True)
            with col_m2:
                st.markdown(f'<div class="metric-showcase" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);"><h3>{len(profiles)}</h3><p>Active Strategies</p></div>', unsafe_allow_html=True)
            with col_m3:
                alert_color = "#ef4444" if total_drift_count > 0 else "#10b981"
                st.markdown(f'<div class="metric-showcase" style="background: linear-gradient(135deg, {alert_color} 0%, {alert_color} 100%);"><h3>{total_drift_count}</h3><p>Need Rebalancing</p></div>', unsafe_allow_html=True)
            
            st.divider()
            
            # Action Items Dashboard
            action_items = []
            for p_name, p_data in profiles.items():
                p_assets = p_data.get("assets", {})
                needs_rebal, drift_details = calculate_drift_status(p_data, prices)
                
                # Use centralized deployment status check (SINGLE SOURCE OF TRUTH)
                all_deployed, deployed_count, total_assets = check_deployment_status(p_data)
                
                if needs_rebal:
                    drift_count = len(drift_details)
                    max_drift = max([d[1] for d in drift_details]) if drift_details else 0
                    action_items.append({
                        "priority": 1, "type": "rebalance", "profile": p_name,
                        "message": f"🚨 URGENT - {p_name} needs rebalancing ({drift_count} asset(s) drifted, max: {max_drift:.1f}%)",
                        "detail": f"{drift_count} assets exceed {p_data.get('drift_tolerance', 5.0)}% tolerance",
                        "action": "Click profile to view details and execute rebalance"
                    })
                elif not all_deployed and total_assets > 0:
                    remaining = [(t, a.get("allocated_pct", 0)) for t, a in p_assets.items() if a.get("allocated_pct", 0) < 99.5]
                    action_items.append({
                        "priority": 2, "type": "deployment", "profile": p_name,
                        "message": f"📥 IN PROGRESS - {p_name} deployment ({deployed_count}/{total_assets} assets)",
                        "detail": ", ".join([f"{t} needs {100-pct:.0f}% more" for t, pct in remaining[:3]]),
                        "action": "Complete remaining asset deployments"
                    })
            
            # Check and send email notifications for rebalancing
            rebalance_portfolios = [item for item in action_items if item["type"] == "rebalance"]
            if rebalance_portfolios:
                # Build portfolio data for email
                portfolios_for_email = []
                for item in rebalance_portfolios:
                    p_name = item["profile"]
                    p_data = profiles[p_name]
                    p_assets = p_data.get("assets", {})
                    curr_v = float(sum(p_assets[t]["units"] * prices.get(t, 0) for t in p_assets))
                    _, drift_details = calculate_drift_status(p_data, prices)
                    max_drift = max([d[1] for d in drift_details]) if drift_details else 0
                    portfolios_for_email.append({
                        "name": p_name,
                        "value": curr_v,
                        "max_drift": max_drift
                    })
                
                # Send notification (function handles all checks)
                success, msg = check_and_send_rebalance_notifications(
                    st.session_state.db, current_user, portfolios_for_email
                )
                if success:
                    save_db(st.session_state.db)  # Save updated notification timestamp
            
            st.markdown("### ⚡ Action Items Dashboard")
            action_items.sort(key=lambda x: x["priority"])
            
            if action_items:
                st.caption(f"You have **{len(action_items)} action item(s)** requiring attention")
                for item in action_items:
                    if item["type"] == "rebalance":
                        st.markdown(f'''
                            <div style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); 
                                        border-left: 4px solid #ef4444; padding: 16px; border-radius: 8px; margin: 12px 0;">
                                <div style="font-weight: 700; color: #991b1b; font-size: 1.05rem; margin-bottom: 8px;">{item['message']}</div>
                                <div style="color: #7f1d1d; font-size: 0.9rem; margin-bottom: 8px;">📊 {item['detail']}</div>
                                <div style="color: #7f1d1d; font-size: 0.85rem; font-style: italic;">↙ {item['action']}</div>
                            </div>
                        ''', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''
                            <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                                        border-left: 4px solid #f59e0b; padding: 16px; border-radius: 8px; margin: 12px 0;">
                                <div style="font-weight: 700; color: #92400e; font-size: 1.05rem; margin-bottom: 8px;">{item['message']}</div>
                                <div style="color: #78350f; font-size: 0.9rem; margin-bottom: 8px;">📋 {item['detail']}</div>
                                <div style="color: #78350f; font-size: 0.85rem; font-style: italic;">↙ {item['action']}</div>
                            </div>
                        ''', unsafe_allow_html=True)
            else:
                st.markdown('''
                    <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                                border-left: 4px solid #10b981; padding: 16px; border-radius: 8px; margin: 12px 0;">
                        <div style="font-weight: 700; color: #065f46; font-size: 1.05rem; margin-bottom: 8px;">✅ ALL CLEAR - No actions required</div>
                        <div style="color: #047857; font-size: 0.9rem;">All portfolios are properly balanced and fully deployed. Great job! 🎉</div>
                    </div>
                ''', unsafe_allow_html=True)
            
            st.divider()
            
            # Portfolio Strategies Grid
            st.markdown("### 📁 Portfolio Strategies")
            st.caption("Click any profile to view detailed analytics")
            
            cols = st.columns(2)
            for i, (name, p_data) in enumerate(profiles.items()):
                p_assets = p_data.get("assets", {})
                curr_v = float(sum(p_assets[t]["units"] * prices.get(t, 0) for t in p_assets))
                
                has_rebalanced = p_data.get("last_rebalanced") is not None
                recently_rebalanced = check_recently_rebalanced(p_data.get("last_rebalanced"))
                needs_rebal, drift_details = calculate_drift_status(p_data, prices)
                
                start_val = float(p_data.get('principal', 0))
                
                # Calculate deployed capital
                p_deployed = 0
                for t, asset in p_assets.items():
                    purchases = asset.get("purchases", [])
                    p_deployed += sum(p.get("amount", 0) for p in purchases)
                
                p_deployment_pct = (p_deployed / start_val * 100) if start_val > 0 else 0
                p_is_fully_deployed = p_deployment_pct >= 99.5
                
                # Calculate ROI and CAGR based on deployed capital for partially deployed
                if p_is_fully_deployed:
                    roi_pct = ((curr_v / start_val) - 1) * 100 if start_val > 0 else 0
                else:
                    roi_pct = ((curr_v / p_deployed) - 1) * 100 if p_deployed > 0 else 0
                
                start_date = datetime.strptime(p_data.get('start_date', str(date.today())), '%Y-%m-%d')
                years_elapsed = max((date.today() - start_date.date()).days / 365.25, 0.01)
                
                if p_is_fully_deployed:
                    cagr = ((curr_v / start_val) ** (1 / years_elapsed) - 1) * 100 if start_val > 0 else 0
                else:
                    cagr = ((curr_v / p_deployed) ** (1 / years_elapsed) - 1) * 100 if p_deployed > 0 else 0
                
                p_flag = "🇺🇸" if p_data.get("currency") == "USD" else "🇨🇦"
                
                # Use centralized deployment status check (SINGLE SOURCE OF TRUTH)
                all_deployed, deployed_count, total_assets = check_deployment_status(p_data)
                
                # Status and tile class (with pulse animation for rebalance)
                if recently_rebalanced or (has_rebalanced and not needs_rebal):
                    tile_class = "profile-tile-optimized"
                    status_badge = '<span class="success-badge">✅ Balanced</span>'
                elif needs_rebal:
                    tile_class = "profile-tile-warning"
                    status_badge = '<span class="drift-badge">🚨 REBALANCE</span>'
                elif len(p_assets) == 0:
                    # No assets defined yet - Setup status
                    tile_class = "profile-tile"
                    status_badge = '<span style="background: #64748b; color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">⚙️ Setup</span>'
                elif not all_deployed and len(p_assets) > 0:
                    tile_class = "profile-tile"
                    # deployed_count already comes from centralized function above
                    status_badge = f'<span style="background: #f59e0b; color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">📥 Deploying ({deployed_count}/{total_assets})</span>'
                elif all_deployed:
                    tile_class = "profile-tile-optimized"
                    status_badge = '<span class="success-badge">✅ Deployed</span>'
                else:
                    tile_class = "profile-tile"
                    status_badge = '<span style="background: #94a3b8; color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">⚪ New</span>'
                
                with cols[i % 2]:
                    st.markdown(f'''
                        <div class="{tile_class}" style="padding: 24px; margin-bottom: 8px;">
                            <div class="profile-tile-header">{p_flag} {name}</div>
                            <div style="margin-bottom: 16px; text-align: center;">{status_badge}</div>
                            <div style="margin: 20px 0; text-align: center;">
                                <div class="stat-label">Portfolio Value</div>
                                <div class="stat-value" style="font-size: 2rem;">${curr_v:,.0f}</div>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 0.9rem; color: #64748b;">
                                <div>
                                    <div style="font-size: 0.75rem; opacity: 0.8;">Goal</div>
                                    <div style="font-weight: 600;">{p_data['yearly_goal_pct']}%/yr</div>
                                </div>
                                <div style="text-align: center;">
                                    <div style="font-size: 0.75rem; opacity: 0.8;">CAGR</div>
                                    <div style="font-weight: 600; color: {'#10b981' if cagr >= 0 else '#ef4444'};">{cagr:+.1f}%</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-size: 0.75rem; opacity: 0.8;">ROI</div>
                                    <div style="font-weight: 600; color: {'#10b981' if roi_pct >= 0 else '#ef4444'};">{roi_pct:+.1f}%</div>
                                </div>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    if st.button(f"📊 Open {name}", key=f"open_{name}", use_container_width=True):
                        st.session_state.active_profile = name
                        st.session_state.current_page = "Portfolio Manager"
                        st.rerun()
            
            st.divider()
            
            # Performance Breakdown
            st.markdown("### 📊 Performance Breakdown")
            
            performance_data = []
            for p_name, p_data in profiles.items():
                p_assets = p_data.get("assets", {})
                curr_val = float(sum(p_assets[t]["units"] * prices.get(t, 0) for t in p_assets))
                start_val = float(p_data.get('principal', 0))
                start_date = datetime.strptime(p_data.get('start_date', str(date.today())), '%Y-%m-%d').date()
                
                # CRITICAL: Only include profiles with valid data
                # Skip if no principal OR no current value (prevents -100% error)
                if start_val > 0 and curr_val > 0:
                    days_elapsed = (date.today() - start_date).days
                    total_return_pct = ((curr_val / start_val) - 1) * 100
                    performance_data.append({
                        'name': p_name, 'start_date': start_date, 'days_elapsed': days_elapsed,
                        'start_val': start_val, 'curr_val': curr_val,
                        'total_return': curr_val - start_val, 'total_return_pct': total_return_pct
                    })
                elif start_val > 0 and curr_val == 0:
                    # Profile has principal but no deployments yet
                    # Show as 0% return (not -100%)
                    days_elapsed = (date.today() - start_date).days
                    performance_data.append({
                        'name': f"{p_name} (Not Deployed)", 'start_date': start_date, 'days_elapsed': days_elapsed,
                        'start_val': start_val, 'curr_val': 0,
                        'total_return': 0, 'total_return_pct': 0
                    })
            
            if performance_data:
                total_invested = sum(p['start_val'] for p in performance_data)
                total_current = sum(p['curr_val'] for p in performance_data)
                total_gain = total_current - total_invested
                total_return_pct = ((total_current / total_invested) - 1) * 100 if total_invested > 0 else 0
                avg_days = sum(p['days_elapsed'] * p['start_val'] for p in performance_data) / total_invested if total_invested > 0 else 0
                avg_years = avg_days / 365.25
                cagr = ((total_current / total_invested) ** (1 / avg_years) - 1) * 100 if avg_years > 0 else 0
                
                col_j1, col_j2, col_j3, col_j4 = st.columns(4)
                with col_j1:
                    st.markdown(f'''
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                    padding: 20px; border-radius: 12px; color: white; text-align: center;">
                            <div style="font-size: 14px; opacity: 0.9;">🎯 Starting Value</div>
                            <div style="font-size: 28px; font-weight: 700; margin: 8px 0;">${total_invested:,.0f}</div>
                            <div style="font-size: 12px; opacity: 0.8;">{int(avg_days)} days ago</div>
                        </div>
                    ''', unsafe_allow_html=True)
                with col_j2:
                    arrow_color = "#10b981" if total_gain >= 0 else "#ef4444"
                    arrow_icon = "📈" if total_gain >= 0 else "📉"
                    st.markdown(f'''
                        <div style="background: {arrow_color}; padding: 20px; border-radius: 12px; color: white; text-align: center;">
                            <div style="font-size: 14px; opacity: 0.9;">{arrow_icon} Change</div>
                            <div style="font-size: 28px; font-weight: 700; margin: 8px 0;">${total_gain:,.0f}</div>
                            <div style="font-size: 12px; opacity: 0.8;">{total_return_pct:+.1f}%</div>
                        </div>
                    ''', unsafe_allow_html=True)
                with col_j3:
                    st.markdown(f'''
                        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                                    padding: 20px; border-radius: 12px; color: white; text-align: center;">
                            <div style="font-size: 14px; opacity: 0.9;">📊 Current Value</div>
                            <div style="font-size: 28px; font-weight: 700; margin: 8px 0;">${total_current:,.0f}</div>
                            <div style="font-size: 12px; opacity: 0.8;">Live market value</div>
                        </div>
                    ''', unsafe_allow_html=True)
                with col_j4:
                    cagr_color = "#10b981" if cagr >= 0 else "#ef4444"
                    st.markdown(f'''
                        <div style="background: {cagr_color}; padding: 20px; border-radius: 12px; color: white; text-align: center;">
                            <div style="font-size: 14px; opacity: 0.9;">📈 CAGR</div>
                            <div style="font-size: 28px; font-weight: 700; margin: 8px 0;">{cagr:.1f}%</div>
                            <div style="font-size: 12px; opacity: 0.8;">Annualized return</div>
                        </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown("")
                
                # === NEW FEATURE 1: Risk Metrics ===
                st.markdown("#### 📉 Risk Metrics")
                st.caption("Key risk indicators across all portfolios (based on historical data)")
                
                # Fetch historical data for risk calculations
                try:
                    earliest_date = min(p['start_date'] for p in performance_data)
                    all_portfolio_tickers = set()
                    for p_data in profiles.values():
                        all_portfolio_tickers.update(p_data.get("assets", {}).keys())
                    
                    if all_portfolio_tickers:
                        hist_data = yf.download(list(all_portfolio_tickers), start=str(earliest_date), auto_adjust=True, progress=False)['Close']
                        if isinstance(hist_data, pd.Series):
                            hist_data = hist_data.to_frame(name=list(all_portfolio_tickers)[0])
                        
                        # Calculate combined portfolio daily values
                        combined_daily = pd.Series(0.0, index=hist_data.index)
                        for p_name, p_data in profiles.items():
                            p_assets = p_data.get("assets", {})
                            for ticker, asset in p_assets.items():
                                if ticker in hist_data.columns:
                                    units = float(asset.get("units", 0))
                                    combined_daily += hist_data[ticker].ffill() * units
                        
                        combined_daily = combined_daily[combined_daily > 0]
                        
                        if len(combined_daily) > 20:
                            # Calculate daily returns
                            daily_returns = combined_daily.pct_change().dropna()
                            
                            # Volatility (annualized)
                            volatility = daily_returns.std() * np.sqrt(252) * 100
                            
                            # Max Drawdown
                            cumulative = (1 + daily_returns).cumprod()
                            rolling_max = cumulative.expanding().max()
                            drawdowns = (cumulative - rolling_max) / rolling_max
                            max_drawdown = drawdowns.min() * 100
                            
                            # Sharpe Ratio (assuming 5% risk-free rate)
                            risk_free_rate = 0.05
                            excess_returns = daily_returns.mean() * 252 - risk_free_rate
                            sharpe_ratio = excess_returns / (daily_returns.std() * np.sqrt(252)) if daily_returns.std() > 0 else 0
                            
                            # Best/Worst Day
                            best_day = daily_returns.max() * 100
                            worst_day = daily_returns.min() * 100
                            
                            col_r1, col_r2, col_r3, col_r4, col_r5 = st.columns(5)
                            with col_r1:
                                vol_color = "#10b981" if volatility < 15 else "#f59e0b" if volatility < 25 else "#ef4444"
                                st.markdown(f'''
                                    <div style="background: white; border: 2px solid {vol_color}; padding: 16px; border-radius: 10px; text-align: center;">
                                        <div style="font-size: 12px; color: #64748b;">📊 Volatility</div>
                                        <div style="font-size: 24px; font-weight: 700; color: {vol_color};">{volatility:.1f}%</div>
                                        <div style="font-size: 10px; color: #94a3b8;">Annualized</div>
                                    </div>
                                ''', unsafe_allow_html=True)
                            with col_r2:
                                dd_color = "#10b981" if max_drawdown > -10 else "#f59e0b" if max_drawdown > -20 else "#ef4444"
                                st.markdown(f'''
                                    <div style="background: white; border: 2px solid {dd_color}; padding: 16px; border-radius: 10px; text-align: center;">
                                        <div style="font-size: 12px; color: #64748b;">📉 Max Drawdown</div>
                                        <div style="font-size: 24px; font-weight: 700; color: {dd_color};">{max_drawdown:.1f}%</div>
                                        <div style="font-size: 10px; color: #94a3b8;">Peak to trough</div>
                                    </div>
                                ''', unsafe_allow_html=True)
                            with col_r3:
                                sr_color = "#10b981" if sharpe_ratio > 1 else "#f59e0b" if sharpe_ratio > 0.5 else "#ef4444"
                                st.markdown(f'''
                                    <div style="background: white; border: 2px solid {sr_color}; padding: 16px; border-radius: 10px; text-align: center;">
                                        <div style="font-size: 12px; color: #64748b;">⚖️ Sharpe Ratio</div>
                                        <div style="font-size: 24px; font-weight: 700; color: {sr_color};">{sharpe_ratio:.2f}</div>
                                        <div style="font-size: 10px; color: #94a3b8;">Risk-adjusted</div>
                                    </div>
                                ''', unsafe_allow_html=True)
                            with col_r4:
                                st.markdown(f'''
                                    <div style="background: white; border: 2px solid #10b981; padding: 16px; border-radius: 10px; text-align: center;">
                                        <div style="font-size: 12px; color: #64748b;">🚀 Best Day</div>
                                        <div style="font-size: 24px; font-weight: 700; color: #10b981;">{best_day:+.1f}%</div>
                                        <div style="font-size: 10px; color: #94a3b8;">Single day</div>
                                    </div>
                                ''', unsafe_allow_html=True)
                            with col_r5:
                                st.markdown(f'''
                                    <div style="background: white; border: 2px solid #ef4444; padding: 16px; border-radius: 10px; text-align: center;">
                                        <div style="font-size: 12px; color: #64748b;">💥 Worst Day</div>
                                        <div style="font-size: 24px; font-weight: 700; color: #ef4444;">{worst_day:+.1f}%</div>
                                        <div style="font-size: 10px; color: #94a3b8;">Single day</div>
                                    </div>
                                ''', unsafe_allow_html=True)
                            
                            with st.expander("ℹ️ Understanding Risk Metrics"):
                                st.markdown("""
                                - **Volatility**: How much your portfolio value fluctuates. Lower is more stable. <15% is low, >25% is high.
                                - **Max Drawdown**: Largest peak-to-trough decline. Shows worst-case loss experienced.
                                - **Sharpe Ratio**: Return per unit of risk. >1 is good, >2 is excellent, <0.5 is poor.
                                - **Best/Worst Day**: Single-day extremes show tail risk exposure.
                                """)
                            
                            # Per-Account Risk Metrics
                            st.markdown("")
                            with st.expander("📊 Risk Metrics by Account", expanded=False):
                                account_risk_data = []
                                for p_name, p_data in profiles.items():
                                    p_assets = p_data.get("assets", {})
                                    if not p_assets:
                                        continue
                                    
                                    # Calculate per-account daily values
                                    p_daily = pd.Series(0.0, index=hist_data.index)
                                    for ticker, asset in p_assets.items():
                                        if ticker in hist_data.columns:
                                            units = float(asset.get("units", 0))
                                            p_daily += hist_data[ticker].ffill() * units
                                    
                                    p_daily = p_daily[p_daily > 0]
                                    
                                    if len(p_daily) > 20:
                                        p_returns = p_daily.pct_change().dropna()
                                        p_vol = p_returns.std() * np.sqrt(252) * 100
                                        
                                        p_cum = (1 + p_returns).cumprod()
                                        p_rolling_max = p_cum.expanding().max()
                                        p_drawdowns = (p_cum - p_rolling_max) / p_rolling_max
                                        p_max_dd = p_drawdowns.min() * 100
                                        
                                        p_excess = p_returns.mean() * 252 - 0.05
                                        p_sharpe = p_excess / (p_returns.std() * np.sqrt(252)) if p_returns.std() > 0 else 0
                                        
                                        account_risk_data.append({
                                            "Account": p_name,
                                            "Volatility": f"{p_vol:.1f}%",
                                            "Max Drawdown": f"{p_max_dd:.1f}%",
                                            "Sharpe": f"{p_sharpe:.2f}",
                                            "_vol": p_vol,
                                            "_dd": p_max_dd,
                                            "_sharpe": p_sharpe
                                        })
                                
                                if account_risk_data:
                                    # Helper function for color coding
                                    def get_volatility_color(vol):
                                        if vol < 15: return '#dcfce7'  # Light green
                                        elif vol < 25: return '#fef3c7'  # Light yellow
                                        else: return '#fee2e2'  # Light red
                                    
                                    def get_drawdown_color(dd):
                                        if dd > -15: return '#dcfce7'  # Light green
                                        elif dd > -25: return '#fef3c7'  # Light yellow
                                        else: return '#fee2e2'  # Light red
                                    
                                    def get_sharpe_color(sharpe):
                                        if sharpe > 1.5: return '#dcfce7'  # Light green
                                        elif sharpe > 0.5: return '#fef3c7'  # Light yellow
                                        else: return '#fee2e2'  # Light red
                                    
                                    # Create styled HTML table
                                    html = '<table style="width:100%; border-collapse: collapse; font-size: 14px;">'
                                    html += '<thead><tr style="background: #f3f4f6;">'
                                    html += '<th style="padding: 12px; text-align: left; border-bottom: 2px solid #e5e7eb;">Account</th>'
                                    html += '<th style="padding: 12px; text-align: right; border-bottom: 2px solid #e5e7eb;">Volatility</th>'
                                    html += '<th style="padding: 12px; text-align: right; border-bottom: 2px solid #e5e7eb;">Max Drawdown</th>'
                                    html += '<th style="padding: 12px; text-align: right; border-bottom: 2px solid #e5e7eb;">Sharpe</th>'
                                    html += '</tr></thead><tbody>'
                                    
                                    for row in account_risk_data:
                                        html += '<tr style="border-bottom: 1px solid #f3f4f6;">'
                                        html += f'<td style="padding: 10px;">{row["Account"]}</td>'
                                        html += f'<td style="padding: 10px; text-align: right; background: {get_volatility_color(row["_vol"])}; font-weight: 600;">{row["Volatility"]}</td>'
                                        html += f'<td style="padding: 10px; text-align: right; background: {get_drawdown_color(row["_dd"])}; font-weight: 600;">{row["Max Drawdown"]}</td>'
                                        html += f'<td style="padding: 10px; text-align: right; background: {get_sharpe_color(row["_sharpe"])}; font-weight: 600;">{row["Sharpe"]}</td>'
                                        html += '</tr>'
                                    
                                    html += '</tbody></table>'
                                    st.markdown(html, unsafe_allow_html=True)
                                else:
                                    st.caption("Insufficient data for per-account risk metrics")
                            
                            st.markdown("")
                            
                            # === NEW FEATURE 2: Combined Portfolio Timeline ===
                            st.markdown("#### 📈 Combined Wealth Timeline")
                            st.caption("Total portfolio value over time across all strategies")
                            
                            fig_combined = go.Figure()
                            
                            # Normalize to start at total principal
                            first_val = float(combined_daily.iloc[0])
                            combined_normalized = (combined_daily / first_val) * total_invested
                            combined_return = ((float(combined_normalized.iloc[-1]) / total_invested) - 1) * 100
                            
                            # Combined portfolio line
                            fig_combined.add_trace(go.Scatter(
                                x=combined_daily.index, y=combined_normalized,
                                name=f'Total Portfolio ({combined_return:+.1f}%)',
                                line=dict(color='#3b82f6', width=3),
                                fill='tozeroy',
                                fillcolor='rgba(59, 130, 246, 0.1)',
                                hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Value: $%{y:,.0f}<extra></extra>'
                            ))
                            
                            # Add individual portfolio lines (thinner, for reference)
                            portfolio_colors = ['#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']
                            for idx, (p_name, p_data) in enumerate(profiles.items()):
                                p_assets = p_data.get("assets", {})
                                p_daily = pd.Series(0.0, index=hist_data.index)
                                for ticker, asset in p_assets.items():
                                    if ticker in hist_data.columns:
                                        units = float(asset.get("units", 0))
                                        p_daily += hist_data[ticker].ffill() * units
                                p_daily = p_daily[p_daily > 0]
                                if len(p_daily) > 0:
                                    p_first = float(p_daily.iloc[0])
                                    p_principal = float(p_data.get('principal', p_first))
                                    p_normalized = (p_daily / p_first) * p_principal
                                    p_return = ((float(p_normalized.iloc[-1]) / p_principal) - 1) * 100
                                    color = portfolio_colors[idx % len(portfolio_colors)]
                                    fig_combined.add_trace(go.Scatter(
                                        x=p_daily.index, y=p_normalized,
                                        name=f'{p_name} ({p_return:+.1f}%)',
                                        line=dict(color=color, width=1.5, dash='dot'),
                                        hovertemplate=f'<b>{p_name}</b><br>' + '%{x|%Y-%m-%d}<br>Value: $%{y:,.0f}<extra></extra>'
                                    ))
                            
                            fig_combined.update_layout(
                                height=400, plot_bgcolor='white', hovermode='x unified',
                                xaxis=dict(title='Date', showgrid=True, gridcolor='#f1f5f9'),
                                yaxis=dict(title='Portfolio Value ($)', showgrid=True, gridcolor='#f1f5f9', tickformat='$,.0f'),
                                legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5),
                                margin=dict(l=60, r=40, t=20, b=60)
                            )
                            st.plotly_chart(fig_combined, use_container_width=True)
                except Exception as e:
                    st.caption(f"📊 Risk metrics require more historical data")
                
                st.markdown("")
                
                # === GOAL PROGRESS TRACKER (Option 2: Compact but Correct) ===
                st.markdown("#### 🎯 Goal Progress Tracker")
                st.caption("Track progress toward your investment goals")
                
                for p_name, p_data in profiles.items():
                    p_assets = p_data.get("assets", {})
                    current_value = float(sum(p_assets[t]["units"] * prices.get(t, 0) for t in p_assets))
                    principal = float(p_data.get('principal', 0))
                    goal_pct = float(p_data.get('yearly_goal_pct', 10))
                    
                    start_date = datetime.strptime(p_data.get('start_date', str(date.today())), '%Y-%m-%d').date()
                    days_elapsed = (date.today() - start_date).days
                    
                    # Calculate year-end target (what you want by Dec 31 of current year)
                    # For multi-year portfolios, calculate the current year's target
                    current_year_start = date(date.today().year, 1, 1)
                    if start_date >= current_year_start:
                        # Portfolio started this year - use principal as baseline
                        year_start_value = principal
                    else:
                        # Portfolio started in previous year(s) - compound to year start
                        years_to_year_start = (current_year_start - start_date).days / 365.25
                        year_start_value = principal * ((1 + goal_pct/100) ** years_to_year_start)
                    
                    year_end_target = year_start_value * (1 + goal_pct/100)
                    
                    # Calculate pro-rated target (where you should be TODAY based on time elapsed this year)
                    days_in_year = 366 if date.today().year % 4 == 0 else 365
                    days_this_year = (date.today() - current_year_start).days
                    time_fraction = days_this_year / days_in_year
                    
                    expected_growth = year_start_value * (goal_pct/100) * time_fraction
                    pro_rated_target = year_start_value + expected_growth
                    
                    # Calculate actual performance
                    actual_growth = current_value - principal
                    delta = current_value - pro_rated_target
                    
                    # Calculate progress toward year-end goal (what % of annual goal achieved)
                    total_needed_growth = year_end_target - year_start_value
                    if total_needed_growth > 0:
                        progress_pct = min(((current_value - year_start_value) / total_needed_growth) * 100, 150)
                    else:
                        progress_pct = 100 if current_value >= year_end_target else 0
                    
                    # Calculate annualized projection (if current pace continues)
                    if days_elapsed > 0 and current_value > principal:
                        ytd_return_pct = ((current_value / principal) - 1) * 100
                        annualized_projection = ((1 + ytd_return_pct/100) ** (365.25/days_elapsed) - 1) * 100
                    else:
                        annualized_projection = 0
                    
                    # Determine status and colors
                    if delta >= total_needed_growth * 0.05:  # More than 5% ahead
                        status_color = "#10b981"
                        status_text = "🚀 Exceeding Goal"
                        bar_color = "#10b981"
                    elif delta >= 0:  # On track or slightly ahead
                        status_color = "#10b981"
                        status_text = "🎯 On Track"
                        bar_color = "#10b981"
                    elif delta >= -total_needed_growth * 0.05:  # Within 5% behind
                        status_color = "#f59e0b"
                        status_text = "⚠️ Slightly Behind"
                        bar_color = "#f59e0b"
                    else:  # More than 5% behind
                        status_color = "#ef4444"
                        status_text = "🔴 Below Target"
                        bar_color = "#ef4444"
                    
                    # Format delta display
                    delta_display = f"Ahead by ${abs(delta):,.0f}" if delta >= 0 else f"Behind by ${abs(delta):,.0f}"
                    delta_color = "#10b981" if delta >= 0 else "#ef4444"
                    
                    # Calculate months/days for display
                    if days_elapsed < 30:
                        time_display = f"{days_elapsed} of {days_in_year} days"
                    elif days_elapsed < 365:
                        months_elapsed = days_elapsed // 30
                        time_display = f"{months_elapsed} of 12 months"
                    else:
                        years_elapsed = days_elapsed / 365.25
                        time_display = f"{years_elapsed:.1f} years"
                    
                    st.markdown(f'''
                        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                <span style="font-weight: 600; font-size: 1rem;">{p_name}</span>
                                <span style="background: {status_color}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">{status_text}</span>
                            </div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 12px; font-size: 0.85rem;">
                                <div style="text-align: left;">
                                    <div style="color: #64748b; font-size: 0.75rem; margin-bottom: 4px;">Year Start</div>
                                    <div style="color: #1e293b; font-weight: 600; font-size: 1rem;">${year_start_value:,.0f}</div>
                                </div>
                                <div style="text-align: center;">
                                    <div style="color: #64748b; font-size: 0.75rem; margin-bottom: 4px;">Current</div>
                                    <div style="color: #1e293b; font-weight: 700; font-size: 1.15rem;">${current_value:,.0f}</div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="color: #64748b; font-size: 0.75rem; margin-bottom: 4px;">Year-End Target</div>
                                    <div style="color: #1e293b; font-weight: 600; font-size: 1rem;">${year_end_target:,.0f}</div>
                                    <div style="color: #64748b; font-size: 0.7rem;">({goal_pct}% goal)</div>
                                </div>
                            </div>
                            <div style="background: #e2e8f0; border-radius: 10px; height: 12px; overflow: hidden; margin-bottom: 8px;">
                                <div style="background: {bar_color}; height: 100%; width: {min(progress_pct, 100)}%; border-radius: 10px; transition: width 0.3s;"></div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #64748b;">
                                <span>Started: {start_date.strftime('%b %Y')}</span>
                                <span style="color: {delta_color}; font-weight: 600;">{delta_display}</span>
                                <span>{time_display}</span>
                            </div>
                            <div style="margin-top: 8px; padding: 8px; background: #f8fafc; border-radius: 8px; font-size: 0.8rem; color: #475569; text-align: center;">
                                📊 On pace for <strong style="color: {"#10b981" if annualized_projection >= goal_pct else "#ef4444"};">{annualized_projection:.1f}%</strong> annual return
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown("")
                
                # Performance comparison chart
                if len(performance_data) > 1:
                    st.markdown("#### 📊 Portfolio Performance Comparison")
                    perf_sorted = sorted(performance_data, key=lambda x: x['total_return_pct'], reverse=True)
                    
                    # Enhanced color scheme - gradient based on performance
                    def get_color(val, max_val, min_val):
                        if val >= 0:
                            # Green gradient for positive
                            intensity = min(val / max(max_val, 1) * 0.7 + 0.3, 1.0)
                            return f'rgba(16, 185, 129, {intensity})'
                        else:
                            # Red gradient for negative
                            intensity = min(abs(val) / max(abs(min_val), 1) * 0.7 + 0.3, 1.0)
                            return f'rgba(239, 68, 68, {intensity})'
                    
                    max_ret = max(p['total_return_pct'] for p in perf_sorted)
                    min_ret = min(p['total_return_pct'] for p in perf_sorted)
                    colors = [get_color(p['total_return_pct'], max_ret, min_ret) for p in perf_sorted]
                    
                    fig_perf = go.Figure()
                    fig_perf.add_trace(go.Bar(
                        x=[p['name'] for p in perf_sorted],
                        y=[p['total_return_pct'] for p in perf_sorted],
                        marker=dict(
                            color=colors,
                            line=dict(color='rgba(0,0,0,0.1)', width=1)
                        ),
                        text=[f"<b>{p['total_return_pct']:+.1f}%</b><br>${p['curr_val']:,.0f}" for p in perf_sorted],
                        textposition='outside',
                        textfont=dict(size=12),
                        width=0.5,
                        customdata=[[
                            f"{p['total_return_pct']:+.1f}%",
                            f"${p['start_val']:,.0f}",
                            f"${p['curr_val']:,.0f}",
                            f"${p['total_return']:+,.0f}",
                            f"{p['days_elapsed']:.0f}"
                        ] for p in perf_sorted],
                        hovertemplate='<b>%{x}</b><br>' +
                                     'Return: %{customdata[0]}<br>' +
                                     'Invested: %{customdata[1]}<br>' +
                                     'Current: %{customdata[2]}<br>' +
                                     'Gain/Loss: %{customdata[3]}<br>' +
                                     'Days: %{customdata[4]}<br>' +
                                     '<extra></extra>'
                    ))
                    
                    # Add a zero line for reference
                    fig_perf.add_hline(y=0, line_dash="dash", line_color="#94a3b8", line_width=1)
                    
                    fig_perf.update_layout(
                        height=420,
                        showlegend=False,
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        margin=dict(t=40, b=60, l=60, r=40),
                        xaxis=dict(
                            title="Portfolio",
                            title_font=dict(size=13, color='#64748b'),
                            tickfont=dict(size=11, color='#334155'),
                            showgrid=False
                        ),
                        yaxis=dict(
                            title="Total Return (%)",
                            title_font=dict(size=13, color='#64748b'),
                            tickfont=dict(size=11),
                            gridcolor='#f1f5f9',
                            zerolinecolor='#94a3b8',
                            tickformat='+.0f'
                        ),
                        hoverlabel=dict(bgcolor="white", font_size=13, bordercolor="#e2e8f0")
                    )
                    st.plotly_chart(fig_perf, use_container_width=True)
            
            st.divider()
            
            # Attribution Analysis
            st.markdown("### 🎯 Attribution Analysis")
            st.caption("See which assets are contributing to or detracting from your portfolio performance")
            
            attribution_data = {}
            for p_name, p_data in profiles.items():
                p_assets = p_data.get("assets", {})
                for ticker, asset in p_assets.items():
                    if ticker not in attribution_data:
                        attribution_data[ticker] = {
                            "ticker": ticker, "cost_basis": 0, "current_value": 0, "portfolios": []
                        }
                    
                    units = float(asset.get("units", 0))
                    current_price = prices.get(ticker, 0)
                    current_value = units * current_price
                    
                    purchases = asset.get("purchases", [])
                    cost_basis = sum(p.get("amount", 0) for p in purchases)
                    if cost_basis == 0 and units > 0:
                        cost_basis = current_value * 0.9  # Estimate if no purchase history
                    
                    attribution_data[ticker]["cost_basis"] += cost_basis
                    attribution_data[ticker]["current_value"] += current_value
                    attribution_data[ticker]["portfolios"].append(p_name)
            
            if attribution_data:
                attribution_list = []
                total_portfolio_gain = 0
                
                for ticker, data in attribution_data.items():
                    gain = data["current_value"] - data["cost_basis"]
                    total_portfolio_gain += gain
                    return_pct = ((data["current_value"] / data["cost_basis"]) - 1) * 100 if data["cost_basis"] > 0 else 0
                    
                    attribution_list.append({
                        "Asset": ticker,
                        "Cost Basis": data['cost_basis'],
                        "Current Value": data['current_value'],
                        "Gain/Loss": gain,
                        "Return %": return_pct,
                        "In Portfolios": ", ".join(data["portfolios"])
                    })
                
                # Sort by gain for chart
                attribution_sorted = sorted(attribution_list, key=lambda x: x["Gain/Loss"], reverse=True)
                
                # Create horizontal bar chart for attribution
                fig_attr = go.Figure()
                
                colors = ['#10b981' if x["Gain/Loss"] >= 0 else '#ef4444' for x in attribution_sorted]
                
                fig_attr.add_trace(go.Bar(
                    y=[x["Asset"] for x in attribution_sorted],
                    x=[x["Gain/Loss"] for x in attribution_sorted],
                    orientation='h',
                    marker=dict(color=colors, line=dict(width=0)),
                    text=[f'${x["Gain/Loss"]:+,.0f} ({x["Return %"]:+.1f}%)' for x in attribution_sorted],
                    textposition='outside',
                    textfont=dict(size=11),
                    hovertemplate='<b>%{y}</b><br>' +
                                 'Gain/Loss: $%{x:,.0f}<br>' +
                                 '<extra></extra>'
                ))
                
                fig_attr.add_vline(x=0, line_dash="solid", line_color="#94a3b8", line_width=1)
                
                fig_attr.update_layout(
                    height=max(250, len(attribution_sorted) * 45),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    margin=dict(l=80, r=120, t=20, b=40),
                    xaxis=dict(
                        title="Gain/Loss ($)",
                        showgrid=True,
                        gridcolor='#f1f5f9',
                        zeroline=True,
                        zerolinecolor='#94a3b8'
                    ),
                    yaxis=dict(
                        showgrid=False,
                        categoryorder='total ascending'
                    ),
                    showlegend=False
                )
                
                st.plotly_chart(fig_attr, use_container_width=True)
                
                # Summary metric
                net_color = "normal" if total_portfolio_gain >= 0 else "inverse"
                total_cost = sum(a['Cost Basis'] for a in attribution_list)
                st.metric("📊 Net Portfolio Gain/Loss", f"${total_portfolio_gain:,.0f}", 
                         delta=f"{((total_portfolio_gain / total_cost) * 100):+.1f}%" if total_cost > 0 else "N/A",
                         delta_color=net_color)
            
            st.divider()
            
            # Portfolio Comparison Table
            st.markdown("### 📊 Portfolio Comparison Table")
            with st.expander("ℹ️ Understanding the comparison table", expanded=False):
                st.markdown("""
                **Column explanations:**
                - **Profile**: Your portfolio strategy name
                - **Account**: Bank and account type (TFSA, RRSP, IRA, etc.)
                - **Value**: Current market value of all holdings (— if $0)
                - **Deployed**: Percentage of principal that has been invested
                - **Age**: Time since portfolio inception (d=days, mo=months, yr=years)
                - **CAGR**: Compound Annual Growth Rate (shows "< 90d" if portfolio too young)
                - **ROI**: Total Return on Investment since inception
                - **Goal**: Your target annual return percentage
                - **Assets**: Number of different assets in this portfolio (— if none)
                - **Status**: Current state (Balanced, Needs Rebalancing, Deploying, or New)
                
                **Notes:**
                - *Asterisk (*) = Metrics calculated on deployed capital only
                - "< 90d" = CAGR unreliable for portfolios under 90 days old
                - "—" = Not applicable or no data
                """)
            
            comparison_data = []
            for p_name, p_data in profiles.items():
                p_assets = p_data.get("assets", {})
                curr_val = float(sum(p_assets[t]["units"] * prices.get(t, 0) for t in p_assets))
                start_val = float(p_data.get('principal', 0))
                
                # Calculate deployed capital
                ct_deployed = 0
                for t, asset in p_assets.items():
                    purchases = asset.get("purchases", [])
                    ct_deployed += sum(p.get("amount", 0) for p in purchases)
                
                ct_deployment_pct = (ct_deployed / start_val * 100) if start_val > 0 else 0
                ct_is_fully_deployed = ct_deployment_pct >= 99.5
                
                start_date = datetime.strptime(p_data.get('start_date', str(date.today())), '%Y-%m-%d')
                days_elapsed = (date.today() - start_date.date()).days
                years = max(days_elapsed / 365.25, 0.01)
                
                # Age display
                if days_elapsed < 30:
                    age_display = f"{days_elapsed}d"
                elif days_elapsed < 365:
                    age_display = f"{days_elapsed // 30}mo"
                else:
                    age_display = f"{years:.1f}yr"
                
                # Handle $0 portfolios or 0 assets
                if curr_val <= 0 or ct_deployed <= 0:
                    cagr_display = "—"
                    roi_display = "—"
                    cagr_val = None
                    roi_val = None
                elif days_elapsed < 90:
                    # For portfolios < 90 days, show ROI but indicate CAGR is unreliable
                    roi = ((curr_val / ct_deployed) - 1) * 100 if ct_deployed > 0 else 0
                    roi_display = f"{roi:+.1f}%"
                    cagr_display = f"< 90d"
                    cagr_val = None
                    roi_val = roi
                else:
                    # Calculate ROI and CAGR based on deployed capital
                    if ct_is_fully_deployed:
                        roi = ((curr_val / start_val) - 1) * 100 if start_val > 0 else 0
                        cagr = ((curr_val / start_val) ** (1 / years) - 1) * 100 if start_val > 0 else 0
                    else:
                        roi = ((curr_val / ct_deployed) - 1) * 100 if ct_deployed > 0 else 0
                        cagr = ((curr_val / ct_deployed) ** (1 / years) - 1) * 100 if ct_deployed > 0 else 0
                    
                    cagr_display = f"{cagr:+.1f}%" if ct_is_fully_deployed else f"{cagr:+.1f}%*"
                    roi_display = f"{roi:+.1f}%" if ct_is_fully_deployed else f"{roi:+.1f}%*"
                    cagr_val = cagr
                    roi_val = roi
                
                needs_rebal, _ = calculate_drift_status(p_data, prices)
                
                # Use centralized deployment status check (SINGLE SOURCE OF TRUTH)
                all_deployed, deployed_count, total_assets = check_deployment_status(p_data)
                
                # Status determination (same priority as Global Dashboard)
                if needs_rebal:
                    status = "🚨 Rebalance"
                elif len(p_assets) == 0:
                    status = "⚙️ Setup"
                elif not all_deployed and total_assets > 0:
                    status = f"📥 Deploying ({deployed_count}/{total_assets})"
                elif all_deployed:
                    status = "✅ Deployed"
                else:
                    status = "⚪ New"
                
                # Deployed % display
                deployed_display = f"{ct_deployment_pct:.0f}%" if ct_deployment_pct > 0 else "—"
                
                # Assets display
                assets_display = str(total_assets) if total_assets > 0 else "—"
                
                comparison_data.append({
                    "Profile": p_name,
                    "Account": f"{p_data.get('bank_name', 'N/A')} {p_data.get('account_type', '')}",
                    "Value": f"${curr_val:,.0f}" if curr_val > 0 else "—",
                    "Deployed": deployed_display,
                    "Age": age_display,
                    "CAGR": cagr_display,
                    "ROI": roi_display,
                    "Goal": f"{p_data.get('yearly_goal_pct', 0):.1f}%/yr",
                    "Assets": assets_display,
                    "Status": status,
                    "_cagr_val": cagr_val,
                    "_roi_val": roi_val,
                    "_deployed_pct": ct_deployment_pct
                })
            
            # Helper functions for color coding
            def get_performance_color(val):
                """Color code for CAGR/ROI - green for high, red for low"""
                if val is None: return '#f9fafb'  # Gray for N/A
                if val >= 15: return '#dcfce7'  # Light green
                elif val >= 5: return '#fef3c7'  # Light yellow
                elif val >= 0: return '#fff'  # White
                else: return '#fee2e2'  # Light red
            
            def get_deployed_color(pct):
                """Color code for deployed % - green for 100%, yellow for partial"""
                if pct >= 100: return '#dcfce7'  # Light green
                elif pct >= 75: return '#fef3c7'  # Light yellow
                elif pct > 0: return '#fed7aa'  # Light orange
                else: return '#f9fafb'  # Gray
            
            def get_status_color(status):
                """Color code for status"""
                if '✅ Balanced' in status or 'Balanced' in status: return '#dcfce7'  # Light green
                elif '🚨 Rebalance' in status or 'Rebalance' in status: return '#fee2e2'  # Light red
                elif '📥 Deploying' in status or 'Deploying' in status: return '#dbeafe'  # Light blue
                else: return '#f9fafb'  # Light gray for New
            
            # Create styled HTML table
            html = '<table style="width:100%; border-collapse: collapse; font-size: 14px;">'
            html += '<thead><tr style="background: #f3f4f6;">'
            html += '<th style="padding: 10px; text-align: left; border-bottom: 2px solid #e5e7eb;">Profile</th>'
            html += '<th style="padding: 10px; text-align: left; border-bottom: 2px solid #e5e7eb;">Account</th>'
            html += '<th style="padding: 10px; text-align: right; border-bottom: 2px solid #e5e7eb;">Value</th>'
            html += '<th style="padding: 10px; text-align: right; border-bottom: 2px solid #e5e7eb;">Deployed</th>'
            html += '<th style="padding: 10px; text-align: center; border-bottom: 2px solid #e5e7eb;">Age</th>'
            html += '<th style="padding: 10px; text-align: right; border-bottom: 2px solid #e5e7eb;">CAGR</th>'
            html += '<th style="padding: 10px; text-align: right; border-bottom: 2px solid #e5e7eb;">ROI</th>'
            html += '<th style="padding: 10px; text-align: right; border-bottom: 2px solid #e5e7eb;">Goal</th>'
            html += '<th style="padding: 10px; text-align: center; border-bottom: 2px solid #e5e7eb;">Assets</th>'
            html += '<th style="padding: 10px; text-align: center; border-bottom: 2px solid #e5e7eb;">Status</th>'
            html += '</tr></thead><tbody>'
            
            for row in comparison_data:
                html += '<tr style="border-bottom: 1px solid #f3f4f6;">'
                html += f'<td style="padding: 10px; font-weight: 600;">{row["Profile"]}</td>'
                html += f'<td style="padding: 10px;">{row["Account"]}</td>'
                html += f'<td style="padding: 10px; text-align: right;">{row["Value"]}</td>'
                html += f'<td style="padding: 10px; text-align: right; background: {get_deployed_color(row["_deployed_pct"])}; font-weight: 600;">{row["Deployed"]}</td>'
                html += f'<td style="padding: 10px; text-align: center;">{row["Age"]}</td>'
                html += f'<td style="padding: 10px; text-align: right; background: {get_performance_color(row["_cagr_val"])}; font-weight: 600;">{row["CAGR"]}</td>'
                html += f'<td style="padding: 10px; text-align: right; background: {get_performance_color(row["_roi_val"])}; font-weight: 600;">{row["ROI"]}</td>'
                html += f'<td style="padding: 10px; text-align: right;">{row["Goal"]}</td>'
                html += f'<td style="padding: 10px; text-align: center;">{row["Assets"]}</td>'
                html += f'<td style="padding: 10px; text-align: center; background: {get_status_color(row["Status"])}; font-weight: 600;">{row["Status"]}</td>'
                html += '</tr>'
            
            html += '</tbody></table>'
            st.markdown(html, unsafe_allow_html=True)
            
            # Footnotes
            footnotes = []
            if any('*' in str(row.get('CAGR', '')) or '*' in str(row.get('ROI', '')) for row in comparison_data):
                footnotes.append("*Calculated on deployed capital only")
            if any(row.get('CAGR') == '< 90d' for row in comparison_data):
                footnotes.append("'< 90d' = Portfolio too young for reliable CAGR")
            if footnotes:
                st.caption(" | ".join(footnotes))

    elif view_mode == "Portfolio Manager":
        if not st.session_state.active_profile:
            user_profiles = get_user_profiles(st.session_state.db, current_user)
            if user_profiles:
                st.session_state.active_profile = list(user_profiles.keys())[0]
                st.rerun()
            else:
                st.title("📊 Portfolio Manager")
                st.markdown('<div class="neutral-state"><h2>👋 Welcome to Portfolio Manager</h2><p style="font-size: 1.2rem;">Select a profile from the sidebar to view detailed analytics</p></div>', unsafe_allow_html=True)
                st.stop()
        
        user_profiles = get_user_profiles(st.session_state.db, current_user)
        
        if st.session_state.active_profile not in user_profiles:
            st.error("⚠️ Selected profile no longer exists.")
            st.session_state.active_profile = None
            st.rerun()
        
        prof = user_profiles[st.session_state.active_profile]
        p_flag = "🇺🇸" if prof.get("currency") == "USD" else "🇨🇦"
        
        # Portfolio Header with Refresh Button
        col_title, col_refresh = st.columns([5, 1])
        with col_title:
            st.title(f"{p_flag} {st.session_state.active_profile}")
            st.caption(f"Portfolio Manager • Inception: {prof.get('start_date', 'N/A')} • Drift Tolerance: {prof.get('drift_tolerance', 5.0)}%")
        with col_refresh:
            # Check if recently refreshed (prevent spam)
            last_refresh_key = f"last_refresh_{st.session_state.active_profile}"
            last_refresh = st.session_state.get(last_refresh_key, None)
            can_refresh = True
            
            if last_refresh:
                from datetime import datetime
                seconds_ago = (datetime.now() - last_refresh).total_seconds()
                if seconds_ago < 5:
                    can_refresh = False
                    st.caption(f"🕐 {int(seconds_ago)}s ago")
            
            if st.button("🔄 Refresh", 
                         key=f"refresh_portfolio_{st.session_state.active_profile}",
                         disabled=not can_refresh,
                         help="Update with latest market prices",
                         use_container_width=True,
                         type="secondary"):
                with st.spinner("📊 Fetching latest data..."):
                    # Clear cached data to force fresh fetch
                    if hasattr(st, 'cache_data'):
                        st.cache_data.clear()
                    # Store refresh time
                    st.session_state[last_refresh_key] = datetime.now()
                    import time
                    time.sleep(0.3)  # Brief pause for better UX
                st.success("✅ Updated!")
                time.sleep(0.5)
                st.rerun()
        
        # Deployment status banner
        if not prof.get("asset_mix_locked", False):
            st.warning("⚠️ **Asset mix not locked** - Define and lock assets first")
        else:
            assets = prof.get("assets", {})
            
            # Use SMART DETECTION to check if all deployed
            all_deployed = True
            partial = []
            
            for ticker, asset_data in assets.items():
                allocated_pct = asset_data.get("allocated_pct", 0)
                target_pct = asset_data.get("target", 0)
                
                # Check if truly deployed with smart detection
                is_deployed = False
                
                # Calculate remaining budget
                purchases = asset_data.get("purchases", [])
                total_spent = sum(p.get("amount", 0) for p in purchases)
                target_amount = (target_pct / 100) * prof['principal']
                remaining_budget = target_amount - total_spent
                
                # Check if truly deployed (remaining < price)
                try:
                    t_obj = yf.Ticker(ticker)
                    hist = t_obj.history(period="1d")
                    if not hist.empty:
                        current_price = float(hist['Close'].iloc[-1])
                        if remaining_budget < current_price:
                            is_deployed = True  # Truly deployed (fractional only)
                        elif allocated_pct >= 99.5:
                            is_deployed = True  # Fallback
                    elif allocated_pct >= 99.5:
                        is_deployed = True
                except:
                    # If any error, use threshold fallback
                    if allocated_pct >= 99.5:
                        is_deployed = True
                
                if not is_deployed:
                    all_deployed = False
                    partial.append((ticker, allocated_pct))
            
            # Show deployment status message ONLY if not rebalanced yet
            has_rebalanced = prof.get("last_rebalanced") is not None
            
            if assets and not all_deployed:
                st.info(f"📊 **Deployment in progress** - {len(partial)} asset(s) not fully deployed")
            elif assets and all_deployed and not has_rebalanced:
                # Only show "all deployed" message if haven't rebalanced yet
                st.success("✅ **All assets deployed** - Ready to monitor drift")
            # If rebalanced, don't show any deployment message (status badge shows "Balanced/Active")
        
        # Portfolio Summary
        has_rebalanced = prof.get("last_rebalanced") is not None
        recently_rebalanced = check_recently_rebalanced(prof.get("last_rebalanced"))
        
        col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
        with col_sum1:
            st.metric("Total Assets", len(prof.get("assets", {})))
        with col_sum2:
            prof_start = datetime.strptime(prof.get('start_date', str(date.today())), '%Y-%m-%d')
            age_years = max((date.today() - prof_start.date()).days / 365.25, 0.01)
            st.metric("Portfolio Age", f"{age_years:.1f} years")
        with col_sum3:
            st.metric("Last Rebalanced", prof.get("last_rebalanced", "Never")[:10] if prof.get("last_rebalanced") else "Never")
        with col_sum4:
            if not prof.get("asset_mix_locked", False):
                st.metric("Status", "⚙️ Setup", delta="Lock assets", delta_color="off")
            else:
                assets = prof.get("assets", {})
                if assets:
                    # Use smart detection for deployed count (same as progress counter)
                    deployed_count = 0
                    for ticker, asset_data in assets.items():
                        allocated_pct = asset_data.get("allocated_pct", 0)
                        target_pct = asset_data.get("target", 0)
                        
                        # Calculate remaining budget
                        purchases = asset_data.get("purchases", [])
                        total_spent = sum(p.get("amount", 0) for p in purchases)
                        target_amount = (target_pct / 100) * prof['principal']
                        remaining_budget = target_amount - total_spent
                        
                        # Check if truly deployed (remaining < price)
                        try:
                            t_obj = yf.Ticker(ticker)
                            hist = t_obj.history(period="1d")
                            if not hist.empty:
                                current_price = float(hist['Close'].iloc[-1])
                                if remaining_budget < current_price:
                                    deployed_count += 1  # Truly deployed!
                                elif allocated_pct >= 99.5:
                                    deployed_count += 1  # Fallback
                            elif allocated_pct >= 99.5:
                                deployed_count += 1
                        except:
                            # If any error, use threshold fallback
                            if allocated_pct >= 99.5:
                                deployed_count += 1
                    
                    total_count = len(assets)
                    if deployed_count < total_count:
                        # Enhancement 1: Show clearer deployment message
                        deployment_pct = (deployed_count / total_count * 100) if total_count > 0 else 0
                        st.metric("Deployment", "In Progress", delta=f"{deployment_pct:.0f}% complete", delta_color="off")
                    elif has_rebalanced:
                        st.metric("Status", "✅ Balanced" if recently_rebalanced else "Active", delta="Monitoring", delta_color="off")
                    else:
                        st.metric("Status", "✅ Deployed", delta="Ready", delta_color="normal")
        
        st.divider()
        
        asset_dict = prof.get("assets", {})
        tickers = list(asset_dict.keys())
        
        if not tickers:
            st.info("👈 **Add your first asset using the sidebar**")
            st.markdown("### 📚 Quick Start Guide")
            st.markdown("""
            **Follow the sidebar steps in order:**
            
            1. **① Strategy Setup**: Create your investment profile (✅ Done!)
            2. **② Drift Strategy**: Set your rebalancing tolerance threshold
            3. **③ Benchmark**: Choose a market benchmark for comparison
            4. **④ Asset Allocation**: Add ticker symbols and set target percentages
            5. **⑤ Lock Asset Mix**: Lock your allocation when it totals 100%
            6. **⑥ Asset Deployment**: Record your purchases at actual broker prices
            
            **After deployment:**
            - **Monitor Drift**: System alerts when rebalancing is needed
            - **Rebalance**: Execute trades to restore target allocations
            """)
            
            st.info("""
            💡 **Pro Tip - Backtest First!**  
            Before setting your asset allocation and drift strategy, use a backtesting tool like 
            [Portfolio Visualizer](https://www.portfoliovisualizer.com/) or [Testfol.io](https://testfol.io/) 
            to validate your strategy with historical data. This helps you understand expected returns, 
            volatility, and drawdowns before committing real capital.
            """)
            st.stop()
        
        # Fetch data and analyze
        with st.spinner("📊 Analyzing portfolio..."):
            try:
                raw = yf.download(tickers, start=prof["start_date"], auto_adjust=True, progress=False)
                
                if raw.empty:
                    st.error("❌ Could not fetch historical data.")
                    st.stop()
                
                data = raw['Close']
                if len(tickers) == 1:
                    data = pd.DataFrame(data, columns=tickers)
                
                v_t = [t for t in tickers if t in data.columns]
                
                if not v_t:
                    st.error("❌ No valid ticker data found.")
                    st.stop()
                
                if len(v_t) < len(tickers):
                    missing = set(tickers) - set(v_t)
                    st.warning(f"⚠️ Could not load: {', '.join(missing)}")
                
                # Calculate portfolio metrics
                daily_val = data[v_t].apply(
                    lambda r: sum(r[t] * asset_dict[t]["units"] for t in v_t if t in r.index), axis=1
                )
                
                curr_v = float(daily_val.iloc[-1])
                start_val = float(prof['principal'])
                
                # Calculate total deployed capital (actual money invested)
                total_deployed = 0
                for t in v_t:
                    purchases = asset_dict[t].get("purchases", [])
                    total_deployed += sum(p.get("amount", 0) for p in purchases)
                
                # Deployment percentage
                deployment_pct = (total_deployed / start_val * 100) if start_val > 0 else 0
                is_fully_deployed = deployment_pct >= 99.5
                
                if curr_v <= 0:
                    st.warning("⚠️ **Portfolio value is zero**")
                    st.info("Complete asset deployments to see portfolio metrics.")
                    st.stop()
                
                years = max((data.index[-1] - data.index[0]).days / 365.25, 0.01)
                target_val = start_val * (1 + (float(prof['yearly_goal_pct'])/100))**years
                
                perc_diff = ((curr_v / target_val) - 1) * 100 if target_val > 0 else 0
                
                # Calculate ROI and CAGR based on deployed capital for partially deployed portfolios
                if is_fully_deployed:
                    roi_pct = ((curr_v / start_val) - 1) * 100 if start_val > 0 else 0
                else:
                    roi_pct = ((curr_v / total_deployed) - 1) * 100 if total_deployed > 0 else 0
                
                prof_start_date = datetime.strptime(prof.get('start_date', str(date.today())), '%Y-%m-%d')
                prof_years = max((date.today() - prof_start_date.date()).days / 365.25, 0.01)
                
                if is_fully_deployed:
                    profile_cagr = ((curr_v / start_val) ** (1 / prof_years) - 1) * 100 if start_val > 0 else 0
                else:
                    profile_cagr = ((curr_v / total_deployed) ** (1 / prof_years) - 1) * 100 if total_deployed > 0 else 0
                
                # Drift detection
                recently_rebalanced = check_recently_rebalanced(prof.get("last_rebalanced"))
                needs_rebalance = False
                drift_assets = []
                
                if not recently_rebalanced and curr_v > 0:
                    for t in v_t:
                        allocated_pct = asset_dict[t].get("allocated_pct", 0)
                        cur_units = float(asset_dict[t].get("units", 0))
                        if allocated_pct == 0 and cur_units > 0:
                            allocated_pct = 100.0
                        if cur_units == 0:
                            continue
                        actual_pct = float((asset_dict[t]["units"] * data[t].iloc[-1] / curr_v * 100))
                        target_pct = float(asset_dict[t]["target"])
                        drift = float(abs(actual_pct - target_pct))
                        if drift >= prof.get("drift_tolerance", 5.0):
                            needs_rebalance = True
                            drift_assets.append((t, drift, actual_pct, target_pct))
                
                # Drift alert banner - ONLY show after deployment is complete
                # Check if all assets are deployed first
                all_assets_deployed = all(a.get("allocated_pct", 0) >= 99.5 for a in asset_dict.values()) if asset_dict else False
                
                # Also check with smart detection for truly deployed
                if all_assets_deployed:
                    for ticker, asset_data in asset_dict.items():
                        allocated_pct = asset_data.get("allocated_pct", 0)
                        if allocated_pct < 100:  # Might be fractional
                            target_pct = asset_data.get("target", 0)
                            purchases = asset_data.get("purchases", [])
                            total_spent = sum(p.get("amount", 0) for p in purchases)
                            target_amount = (target_pct / 100) * prof['principal']
                            remaining_budget = target_amount - total_spent
                            # If any asset can still afford 1 unit, not fully deployed
                            try:
                                t_obj = yf.Ticker(ticker)
                                hist = t_obj.history(period="1d")
                                if not hist.empty:
                                    current_price = float(hist['Close'].iloc[-1])
                                    if remaining_budget >= current_price:
                                        all_assets_deployed = False
                                        break
                            except:
                                pass
                
                if needs_rebalance and all_assets_deployed:
                    st.markdown(f'''
                        <div style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); 
                                    border: 4px solid #ef4444; border-radius: 16px; padding: 28px; margin-bottom: 28px;">
                            <h2 style="color: #991b1b; margin: 0 0 16px 0; font-size: 1.8rem;">
                                🚨 DRIFT ALERT: Rebalancing Required
                            </h2>
                            <p style="color: #7f1d1d; font-size: 1.2rem; margin: 0;">
                                <strong>{len(drift_assets)} asset(s)</strong> exceeded your <strong>{prof.get('drift_tolerance', 5.0)}% drift tolerance</strong>.
                            </p>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    st.markdown("#### 📊 Assets Requiring Rebalancing:")
                    for ticker, drift, actual, target in drift_assets:
                        col1, col2, col3 = st.columns([2, 2, 2])
                        with col1:
                            st.markdown(f"**{ticker}**")
                        with col2:
                            st.markdown(f"Drift: **{drift:.2f}%** ⚠️")
                        with col3:
                            st.markdown(f"Current: **{actual:.1f}%** (Target: {target:.1f}%)")
                    st.divider()
                
                # Status badge
                has_rebalanced = prof.get("last_rebalanced") is not None
                if recently_rebalanced:
                    alert_html = '<span class="success-badge">✅ Balanced</span>'
                elif needs_rebalance:
                    alert_html = '<span class="drift-badge">🚨 REBALANCE REQUIRED</span>'
                elif has_rebalanced:
                    alert_html = '<span class="success-badge">✅ Balanced</span>'
                else:
                    alert_html = '<span style="background: #3b82f6; color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.75rem;">📊 Monitoring</span>'
                
                # Header
                st.markdown(f'''
                    <div class="premium-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                            <h2 style="margin:0;">Portfolio Analytics</h2>
                            {alert_html}
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
                
                # Key Metrics
                col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
                with col_s1:
                    st.markdown(f'<div class="stat-item"><div class="stat-label">Current Value</div><div class="stat-value">${curr_v:,.0f}</div></div>', unsafe_allow_html=True)
                with col_s2:
                    roi_label = "Total ROI" if is_fully_deployed else "ROI (Deployed)"
                    st.markdown(f'<div class="stat-item"><div class="stat-label">{roi_label}</div><div class="stat-value" style="color: {"#10b981" if roi_pct >= 0 else "#ef4444"};">{roi_pct:+.2f}%</div></div>', unsafe_allow_html=True)
                with col_s3:
                    cagr_label = "CAGR" if is_fully_deployed else "CAGR (Deployed)"
                    st.markdown(f'<div class="stat-item"><div class="stat-label">{cagr_label}</div><div class="stat-value" style="color: {"#10b981" if profile_cagr >= 0 else "#ef4444"};">{profile_cagr:+.2f}%</div></div>', unsafe_allow_html=True)
                with col_s4:
                    st.markdown(f'<div class="stat-item"><div class="stat-label">vs Target Path</div><div class="stat-value" style="color: {"#10b981" if perc_diff >= 0 else "#ef4444"};">{perc_diff:+.2f}%</div></div>', unsafe_allow_html=True)
                with col_s5:
                    if is_fully_deployed:
                        annualized = ((curr_v / start_val) ** (1/years) - 1) * 100
                    else:
                        annualized = ((curr_v / total_deployed) ** (1/years) - 1) * 100 if total_deployed > 0 else 0
                    ann_label = "Annualized" if is_fully_deployed else "Ann. (Deployed)"
                    st.markdown(f'<div class="stat-item"><div class="stat-label">{ann_label}</div><div class="stat-value" style="color: {"#10b981" if annualized >= 0 else "#ef4444"};">{annualized:.2f}%</div></div>', unsafe_allow_html=True)
                
                # Note for partially deployed portfolios
                if not is_fully_deployed:
                    st.caption(f"ℹ️ *Metrics calculated on deployed capital (${total_deployed:,.0f} of ${start_val:,.0f} = {deployment_pct:.1f}% deployed)*")
                
                st.divider()
                
                # Performance Chart
                st.markdown("### 📈 Performance vs Goal Path")
                benchmarks_list = prof.get('benchmarks', [])
                if not benchmarks_list and prof.get('benchmark'):
                    benchmarks_list = [prof.get('benchmark')]
                benchmark_caption = f" & {', '.join(benchmarks_list)}" if benchmarks_list else ""
                st.caption(f"Track your portfolio's actual performance against your target growth trajectory{benchmark_caption}")
                
                fig = go.Figure()
                benchmark_comparison_msgs = []
                
                # Benchmark colors for multiple benchmarks
                benchmark_colors = ['#ef4444', '#f59e0b', '#8b5cf6', '#ec4899', '#14b8a6', '#6366f1']
                
                # Multiple benchmark comparison
                for idx, benchmark_ticker in enumerate(benchmarks_list):
                    if not benchmark_ticker:
                        continue
                    try:
                        # Canadian tickers need .TO suffix for Toronto Stock Exchange
                        ticker_to_fetch = benchmark_ticker
                        if benchmark_ticker in ['XIU', 'XIC', 'ZCN', 'VCN']:
                            ticker_to_fetch = f"{benchmark_ticker}.TO"
                        
                        benchmark_raw = yf.download(ticker_to_fetch, start=prof["start_date"], auto_adjust=True, progress=False)
                        if not benchmark_raw.empty:
                            benchmark_data = benchmark_raw['Close']
                            if isinstance(benchmark_data, pd.DataFrame):
                                benchmark_data = benchmark_data.squeeze()
                            benchmark_data = benchmark_data.dropna()
                            if len(benchmark_data) > 0:
                                first_price = float(benchmark_data.iloc[0])
                                last_price = float(benchmark_data.iloc[-1])
                                benchmark_normalized = (benchmark_data / first_price) * start_val
                                bench_return = ((last_price / first_price) - 1) * 100
                                bench_final_value = float(benchmark_normalized.iloc[-1])
                                
                                # Calculate daily returns for tooltip
                                bench_daily_returns = ((benchmark_normalized / start_val) - 1) * 100
                                
                                # Create customdata with pre-formatted values
                                customdata = [[
                                    f"${val:,.0f}",
                                    f"{ret:+.1f}%",
                                    benchmark_ticker  # Show original ticker (without .TO)
                                ] for val, ret in zip(benchmark_normalized, bench_daily_returns)]
                                
                                color = benchmark_colors[idx % len(benchmark_colors)]
                                fig.add_trace(go.Scatter(
                                    x=benchmark_data.index, y=benchmark_normalized,
                                    name=f'{benchmark_ticker} ({bench_return:+.1f}%)',
                                    line=dict(color=color, width=2, dash='dot'),
                                    customdata=customdata,
                                    hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                                                 'Value: %{customdata[0]}<br>' +
                                                 'Return: %{customdata[1]}<br>' +
                                                 'Ticker: %{customdata[2]}<br>' +
                                                 '<extra></extra>'
                                ))
                                
                                # Store for comparison after portfolio normalization
                                benchmark_comparison_msgs.append({
                                    "ticker": benchmark_ticker,
                                    "return": bench_return,
                                    "final_value": bench_final_value
                                })
                    except Exception as e:
                        # Log error for debugging but don't crash
                        st.warning(f"⚠️ Could not load benchmark {benchmark_ticker}: {str(e)}")
                        pass
                
                # Actual portfolio - normalize to start at principal for fair comparison
                first_portfolio_val = float(daily_val.iloc[0])
                if first_portfolio_val > 0:
                    portfolio_normalized = (daily_val / first_portfolio_val) * start_val
                else:
                    portfolio_normalized = daily_val
                
                portfolio_normalized_final = float(portfolio_normalized.iloc[-1])
                portfolio_return = ((portfolio_normalized_final / start_val) - 1) * 100
                
                # Now calculate benchmark comparisons using normalized portfolio value
                benchmark_display_msgs = []
                for bench_data in benchmark_comparison_msgs:
                    ticker = bench_data["ticker"]
                    bench_final = bench_data["final_value"]
                    portfolio_vs_bench = portfolio_normalized_final - bench_final
                    
                    if portfolio_vs_bench > 0:
                        pct_diff = ((portfolio_normalized_final / bench_final) - 1) * 100
                        benchmark_display_msgs.append(("success", f"📊 Portfolio beat {ticker} by ${portfolio_vs_bench:,.0f} ({pct_diff:+.1f}%)"))
                    else:
                        pct_diff = ((bench_final / portfolio_normalized_final) - 1) * 100
                        benchmark_display_msgs.append(("info", f"📊 {ticker} beat portfolio by ${abs(portfolio_vs_bench):,.0f} ({pct_diff:+.1f}%)"))
                
                # Calculate daily returns for portfolio tooltip
                portfolio_daily_returns = ((portfolio_normalized / start_val) - 1) * 100
                
                # Create customdata for portfolio with pre-formatted values
                portfolio_customdata = [[
                    f"${val:,.0f}",
                    f"{ret:+.1f}%",
                    f"${val - start_val:+,.0f}"
                ] for val, ret in zip(portfolio_normalized, portfolio_daily_returns)]
                
                fig.add_trace(go.Scatter(x=data.index, y=portfolio_normalized, 
                    name=f'Actual Portfolio ({portfolio_return:+.1f}%)',
                    line=dict(color='#3b82f6', width=3),
                    customdata=portfolio_customdata,
                    hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                                 'Value: %{customdata[0]}<br>' +
                                 'Return: %{customdata[1]}<br>' +
                                 'Gain/Loss: %{customdata[2]}<br>' +
                                 '<extra></extra>'
                ))
                
                # Goal path
                days = np.arange(len(data.index))
                daily_rate = (float(prof['yearly_goal_pct']) / 100) / 365.25
                target_path = start_val * (1 + daily_rate) ** days
                
                # Calculate goal path returns for tooltip
                goal_returns = ((target_path / start_val) - 1) * 100
                goal_customdata = [[
                    f"${val:,.0f}",
                    f"{ret:+.1f}%",
                    f"${val - start_val:+,.0f}"
                ] for val, ret in zip(target_path, goal_returns)]
                
                fig.add_trace(go.Scatter(x=data.index, y=target_path,
                    name=f'Goal Path ({prof["yearly_goal_pct"]}%/yr)',
                    line=dict(color='#10b981', width=2, dash='dash'),
                    customdata=goal_customdata,
                    hovertemplate='<b>%{x|%Y-%m-%d}</b><br>' +
                                 'Target: %{customdata[0]}<br>' +
                                 'Return: %{customdata[1]}<br>' +
                                 'Growth: %{customdata[2]}<br>' +
                                 '<extra></extra>'
                ))
                
                fig.update_layout(
                    hovermode='x unified', plot_bgcolor='white', height=550, showlegend=True,
                    hoverlabel=dict(bgcolor="white", font_size=14, font_family="Inter, sans-serif", bordercolor="#e2e8f0"),
                    xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title='Date', title_font=dict(size=14, color='#64748b'), tickfont=dict(size=11)),
                    yaxis=dict(showgrid=True, gridcolor='#f1f5f9', title='Portfolio Value ($)', title_font=dict(size=14, color='#64748b'), tickfont=dict(size=11), tickformat='$,.0f'),
                    legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5, font=dict(size=12), bgcolor='rgba(255,255,255,0.9)', bordercolor='#e2e8f0', borderwidth=1),
                    margin=dict(l=70, r=40, t=20, b=80)
                )
                st.plotly_chart(fig, use_container_width=True)
                
                with st.expander("📊 Understanding This Chart", expanded=False):
                    st.markdown(f"""
                    **What the lines represent:**
                    
                    All lines start at your principal (${start_val:,.0f}) for a fair "apples-to-apples" comparison.
                    
                    📊 **Benchmarks (Dotted lines)** *(if selected)*  
                    Each shows what $100K invested in that index would be worth today.
                    Colors: 🔴 Red, 🟠 Orange, 🟣 Purple, 💗 Pink, 🩵 Teal, 💙 Indigo
                    
                    🔵 **Actual Portfolio (Blue solid line)**  
                    Your portfolio's relative performance - normalized to show how your asset mix 
                    would have grown from the principal value.
                    
                    🟢 **Goal Path (Green dashed line)**  
                    Your target growth trajectory based on your yearly goal of {prof['yearly_goal_pct']}%.
                    
                    **Tooltip Info:**
                    - **Value**: Current value at that date
                    - **Return**: Percentage change from start
                    - **Gain/Loss**: Dollar change from start
                    
                    **Tips:**
                    - Click any legend item to show/hide that line
                    - Hover over the chart to see exact values at any date
                    - Use the toolbar to zoom, pan, or save the chart
                    """)
                
                if benchmark_display_msgs:
                    for msg_type, msg_text in benchmark_display_msgs:
                        if msg_type == "success":
                            st.success(msg_text)
                        else:
                            st.info(msg_text)
                
                st.divider()
                
                # Rebalance Analysis with Refresh
                col_rebal_title, col_rebal_refresh = st.columns([5, 1])
                with col_rebal_title:
                    st.markdown("### ⚖️ Rebalance Analysis")
                    st.caption("Review asset allocation drift and required trades to restore target percentages")
                with col_rebal_refresh:
                    # Refresh button for rebalance section
                    last_refresh_rebal = st.session_state.get(f"last_refresh_rebal_{st.session_state.active_profile}", None)
                    can_refresh_rebal = True
                    
                    if last_refresh_rebal:
                        from datetime import datetime
                        seconds_ago = (datetime.now() - last_refresh_rebal).total_seconds()
                        if seconds_ago < 5:
                            can_refresh_rebal = False
                    
                    if st.button("🔄 Update", 
                                 key=f"refresh_rebalance_{st.session_state.active_profile}",
                                 disabled=not can_refresh_rebal,
                                 help="Refresh prices before rebalancing",
                                 use_container_width=True,
                                 type="secondary"):
                        with st.spinner("Updating prices..."):
                            if hasattr(st, 'cache_data'):
                                st.cache_data.clear()
                            st.session_state[f"last_refresh_rebal_{st.session_state.active_profile}"] = datetime.now()
                            import time
                            time.sleep(0.3)
                        st.success("✅ Prices updated!")
                        time.sleep(0.5)
                        st.rerun()
                
                with st.expander("ℹ️ Understanding the rebalance table", expanded=False):
                    st.markdown("""
                    **This table shows what trades are needed** to restore your target allocation.
                    
                    **Column Explanations:**
                    - **Target %**: Your desired allocation for this asset (e.g., 25% means you want this asset to be 25% of your total portfolio)
                    - **Deployed**: Deployment progress from 0-100% showing how much of YOUR PLANNED CAPITAL for this specific asset has been invested
                        - 0% = haven't started buying this asset yet
                        - 50% = halfway through planned purchases
                        - 100% = finished all planned purchases for this asset
                        - ⚠️ **NOTE:** This is NOT portfolio allocation percentage!
                    - **Portfolio %**: Current portfolio percentage (% of your TOTAL PRINCIPAL, not just deployed capital)
                        - Shows true portfolio allocation
                        - Increases as you deploy more capital
                        - Will match Target % when fully deployed (assuming no price changes)
                    - **Drift**: Difference between Portfolio % and Target %
                        - ⚠️ Gray "Deploying" = asset still being deployed (drift tracking not meaningful yet)
                        - 🔴 Red = exceeds tolerance (action needed after deployment complete)
                        - 🟡 Yellow = warning (close to tolerance)
                        - 🟢 Green = within tolerance (good)
                    - **Status**: Current state (Deploying = adding capital, Deployed = monitoring drift)
                    
                    **Example to clarify Deployed vs Portfolio %:**
                    - You set Target % = 50% for SPXL (you want it to be 50% of your $100k portfolio = $50k)
                    - You've bought $25k worth so far
                    - Deployed = 50% (because $25k is 50% of your planned $50k target)
                    - Portfolio % = 25.0% (because $25k is 25% of your $100k principal)
                    - As you buy more, both Deployed and Portfolio % increase
                    - When Deployed reaches 100%, you've invested the full $50k
                    - Then Portfolio % will be near 50% (your target)
                    
                    💡 **Key Insight:** "Deployed" tracks YOUR deployment progress (0-100%), while "Portfolio %" shows current portfolio allocation (% of total principal)
                    
                    💡 Use the two-step workflow below to rebalance with real broker prices
                    """)
                
                column_config = {
                    "Fund Name": st.column_config.TextColumn("Fund Name ℹ️", help="Full name of the investment fund or security", width="large"),
                    "Ticker": st.column_config.TextColumn("Ticker ℹ️", help="Stock ticker symbol", width="small"),
                    "Target %": st.column_config.TextColumn("Target % ℹ️", help="Your desired allocation percentage for this asset in the portfolio", width="small"),
                    "Deployed": st.column_config.TextColumn("Deployed ℹ️", help="Deployment progress: 0-100% shows how much of your planned capital for THIS ASSET has been deployed (NOT portfolio allocation). 100% = fully deployed.", width="small"),
                    "Portfolio %": st.column_config.TextColumn("Portfolio % ℹ️", help="Current portfolio percentage based on market values (% of total principal). Shows true portfolio allocation.", width="small"),
                    "Drift": st.column_config.TextColumn("Drift ℹ️", help="Difference between Portfolio % and Target % (🔴 = exceeds tolerance and needs rebalancing, ⚠️ = still deploying)", width="small"),
                    "Status": st.column_config.TextColumn("Status ℹ️", help="Current state: Deploying = still adding capital, Deployed = fully funded and monitoring drift", width="medium"),
                    "Avg Cost": st.column_config.TextColumn("Avg Cost ℹ️", help="Weighted average cost per unit (calculated when 100% deployed)", width="small"),
                    "Units": st.column_config.TextColumn("Units ℹ️", help="Total shares/units owned", width="small"),
                    "Current Price": st.column_config.TextColumn("Price ℹ️", help="Latest market price per unit", width="small"),
                    "%Daily Change": st.column_config.TextColumn("%Change ℹ️", help="Price change from previous trading day", width="small"),
                    "Amount": st.column_config.TextColumn("Value ℹ️", help="Current market value (Units × Current Price)", width="medium"),
                    "Buy/Sell Amt": st.column_config.TextColumn("Trade Amt ℹ️", help="Dollar amount to trade for rebalancing", width="medium"),
                    "Buy/Sell Shares": st.column_config.TextColumn("Trade Shares ℹ️", help="Number of shares to buy (+) or sell (-)", width="small")
                }
                
                rows = []
                total_turnover = 0
                total_current_val = 0
                total_undeployed = 0
                
                # Calculate actual_undeployed_cash for smart fractional detection
                # This must be calculated BEFORE using it in the table logic below
                total_deployed_capital = 0
                for ticker_calc, asset_data_calc in asset_dict.items():
                    purchases_calc = asset_data_calc.get("purchases", [])
                    total_deployed_capital += sum(p.get("amount", 0) for p in purchases_calc)
                
                principal_amt = prof['principal']
                actual_undeployed_cash = principal_amt - total_deployed_capital
                
                # CRITICAL FIX: Pre-calculate total current portfolio value
                # This is needed for accurate Portfolio % calculation in rebalance table
                # (Portfolio % should be based on CURRENT value, not original principal)
                total_portfolio_current_value = 0
                for ticker_val in v_t:
                    try:
                        current_price_val = float(data[ticker_val].iloc[-1])
                        current_units_val = float(asset_dict[ticker_val].get("units", 0))
                        asset_current_value = current_units_val * current_price_val
                        if np.isfinite(asset_current_value) and current_price_val > 0:
                            total_portfolio_current_value += asset_current_value
                    except:
                        pass
                
                # Smart fractional detection for table status
                # Calculate if portfolio is truly fully deployed (fractional only)
                table_is_truly_fully_deployed = False
                if actual_undeployed_cash > 0:
                    # Find cheapest asset price in the table
                    cheapest_price_in_table = None
                    for t in v_t:
                        try:
                            price = float(data[t].iloc[-1])
                            if cheapest_price_in_table is None or price < cheapest_price_in_table:
                                cheapest_price_in_table = price
                        except:
                            pass
                    
                    # Check if undeployed cash can buy cheapest asset
                    if cheapest_price_in_table is not None:
                        table_is_truly_fully_deployed = actual_undeployed_cash < cheapest_price_in_table
                
                try:
                    for t in v_t:
                        try:
                            current_price = float(data[t].iloc[-1])
                            if not np.isfinite(current_price) or current_price <= 0:
                                st.warning(f"⚠️ Invalid price data for {t}, skipping from table")
                                continue
                                
                            try:
                                prev_price = float(data[t].iloc[-2])
                                if np.isfinite(prev_price) and prev_price > 0:
                                    daily_change_pct = ((current_price / prev_price) - 1) * 100
                                else:
                                    daily_change_pct = 0.0
                            except:
                                daily_change_pct = 0.0
                            
                            fund_name = asset_dict[t].get("fund_name", t)
                            cur_u = float(asset_dict[t].get("units", 0))
                            tar_w = float(asset_dict[t].get('target', 0))
                            
                            # CRITICAL: Recalculate allocated_pct from scratch for accuracy
                            # Don't rely on stored value - it may be stale if principal/targets changed
                            purchases_for_calc = asset_dict[t].get("purchases", [])
                            total_spent_calc = sum(p.get("amount", 0) for p in purchases_for_calc)
                            target_amount_calc = (tar_w / 100) * start_val if tar_w > 0 else 1
                            allocated_pct = (total_spent_calc / target_amount_calc * 100) if target_amount_calc > 0 else 0
                            
                            # Validation fixes
                            if not np.isfinite(allocated_pct) or allocated_pct > 100:
                                allocated_pct = 100.0
                            elif cur_u > 0 and allocated_pct == 0:
                                allocated_pct = 100.0
                            
                            avg_cost = calculate_average_cost(asset_dict[t])
                            avg_cost_display = f"${avg_cost:.2f}" if avg_cost and np.isfinite(avg_cost) else "Pending"
                            
                            act_val = cur_u * current_price
                            if not np.isfinite(act_val):
                                act_val = 0
                                
                            # CRITICAL FIX: Calculate Portfolio % as % of CURRENT portfolio value (not principal)
                            # This ensures Portfolio % always sums to 100%, even when portfolio has gains/losses
                            # During deployment: use principal (portfolio value ≈ deployed capital)
                            # After deployment: use current market value (accounts for gains/losses)
                            if total_portfolio_current_value > 0:
                                act_w = (act_val / total_portfolio_current_value * 100)
                            else:
                                # Fallback to principal if no current value (shouldn't happen)
                                act_w = (act_val / start_val * 100) if start_val > 0 else 0
                                
                            if not np.isfinite(act_w):
                                act_w = 0
                                
                            drift = act_w - tar_w
                            if not np.isfinite(drift):
                                drift = 0
                            
                            # Calculate target values based on current portfolio value
                            tar_val = (tar_w / 100) * total_portfolio_current_value
                            tar_u = tar_val / current_price if current_price > 0 else 0
                            val_diff = tar_val - act_val
                            unit_diff = tar_u - cur_u
                            
                            # Ensure all values are finite
                            if not np.isfinite(val_diff):
                                val_diff = 0
                            if not np.isfinite(unit_diff):
                                unit_diff = 0
                            
                            total_turnover += abs(val_diff)
                            total_current_val += act_val
                            
                            # SMART DETECTION: Check if asset is truly 100% deployed
                            # (remaining budget < price = can't buy 1 unit = 100% deployed)
                            remaining_budget_for_asset = target_amount_calc - total_spent_calc
                            is_asset_truly_deployed = (remaining_budget_for_asset < current_price) if current_price > 0 else False
                            
                            # Drift display - show "Deploying" status during deployment
                            drift_tolerance = prof.get("drift_tolerance", 5.0)
                            
                            # During deployment phase, show special status
                            # Use smart detection instead of 99.5% threshold
                            if not is_asset_truly_deployed and allocated_pct < 99.5:  # Still deploying
                                drift_display = "⚠️ Deploying"
                            elif abs(drift) >= drift_tolerance:
                                drift_display = f"🔴 {drift:+.2f}%"
                            elif abs(drift) >= drift_tolerance * 0.6:  # Warning at 60% of tolerance
                                drift_display = f"🟡 {drift:+.2f}%"
                            else:
                                drift_display = f"🟢 {drift:+.2f}%"
                            
                            # Status - use smart fractional detection
                            if table_is_truly_fully_deployed or is_asset_truly_deployed:
                                # Asset is truly fully deployed (fractional only)
                                status_display = "✅ Deployed"
                            elif allocated_pct >= 99.5:
                                status_display = "✅ Deployed"
                            else:
                                status_display = f"⏳ Deploying ({allocated_pct:.0f}%)"
                            
                            # Enhancement 3: Show more accurate deployed % (2 decimal places)
                            if is_asset_truly_deployed or allocated_pct >= 99.95:
                                deployed_display = "100%"
                            else:
                                deployed_display = f"{allocated_pct:.2f}%"
                            
                            rows.append({
                                "Fund Name": fund_name, "Ticker": t, "Target %": f"{tar_w:.2f}%",
                                "Deployed": deployed_display, "Portfolio %": f"{act_w:.2f}%",
                                "Drift": drift_display, "Status": status_display,
                                "Avg Cost": avg_cost_display,
                                "Units": f"{cur_u:.0f}", "Current Price": f"${current_price:.2f}",
                                "%Daily Change": f"{daily_change_pct:+.2f}%", "Amount": f"${act_val:,.0f}",
                                "Buy/Sell Amt": f"${abs(val_diff):,.0f}", "Buy/Sell Shares": f"{int(unit_diff):+.0f}" if np.isfinite(unit_diff) else "—"
                            })
                        except Exception as e:
                            st.warning(f"⚠️ Error processing {t}: {str(e)}")
                            continue
                
                except Exception as e:
                    st.error(f"""
                    ❌ **Error building rebalance table**
                    
                    {str(e)}
                    
                    This may be due to:
                    - Over-deployment (deployed > principal)
                    - Invalid price data
                    - Corrupted purchase records
                    
                    Please check your Capital Overview above for issues.
                    """)
                    st.stop()
                
                # Calculate overall drift status for TOTAL row
                # CRITICAL: Use same drift calculation as individual assets
                # (based on CURRENT portfolio value, not principal)
                max_drift = 0
                if v_t and total_portfolio_current_value > 0:
                    for t in v_t:
                        try:
                            cur_u = float(asset_dict[t].get("units", 0))
                            tar_w = float(asset_dict[t].get('target', 0))
                            current_price = float(data[t].iloc[-1])
                            
                            # Calculate actual portfolio % (same as individual rows)
                            act_val = cur_u * current_price
                            act_w = (act_val / total_portfolio_current_value * 100)
                            
                            # Calculate drift (same as individual rows)
                            drift = abs(act_w - tar_w)
                            
                            # Track maximum drift
                            if np.isfinite(drift) and drift > max_drift:
                                max_drift = drift
                        except:
                            pass
                
                drift_tolerance = prof.get("drift_tolerance", 5.0)
                
                # Calculate ACTUAL undeployed cash (same as sidebar)
                actual_undeployed_cash = start_val - total_deployed
                actual_undeployed_pct = (actual_undeployed_cash / start_val * 100) if start_val > 0 else 0
                
                # Calculate total portfolio percentage (should always be 100% since it's sum of parts)
                # Note: Individual asset Portfolio % are now based on current portfolio value
                # So the sum should always be 100% (or very close due to rounding)
                total_portfolio_pct = 100.0  # Always 100% since Portfolio % = % of current value
                
                # Determine overall status
                if not is_fully_deployed:
                    total_status = "⚠️ Deploying"
                elif max_drift >= drift_tolerance:
                    total_status = "⚠️ Rebalance Needed"
                elif max_drift >= drift_tolerance * 0.6:
                    total_status = "🟡 Monitor"
                else:
                    total_status = "✅ Balanced"
                
                rows.append({
                    "Fund Name": "**TOTAL**", "Ticker": "", "Target %": "**100.00%**",
                    "Deployed": f"**{deployment_pct:.0f}%**" if not is_fully_deployed else "**100%**", 
                    "Portfolio %": f"**{total_portfolio_pct:.2f}%**", "Drift": "—", "Status": total_status,
                    "Avg Cost": "", "Units": "", "Current Price": "", "%Daily Change": "",
                    "Amount": f"**${total_current_val:,.0f}**",
                    "Buy/Sell Amt": f"**${total_turnover:,.0f}**", "Buy/Sell Shares": "—"
                })
                
                df_rebalance = pd.DataFrame(rows)
                st.dataframe(df_rebalance, use_container_width=True, hide_index=True, column_config=column_config)
                
                # Explain undeployed cash if it exists - use smart fractional detection
                if actual_undeployed_cash > 0:
                    # Get cheapest asset price for smart detection
                    cheapest_price_table = None
                    try:
                        for t in v_t:
                            price = float(data[t].iloc[-1])
                            if cheapest_price_table is None or price < cheapest_price_table:
                                cheapest_price_table = price
                    except:
                        pass
                    
                    # Determine if truly fractional
                    is_truly_fractional_table = False
                    if cheapest_price_table is not None:
                        is_truly_fractional_table = actual_undeployed_cash < cheapest_price_table
                    
                    if is_truly_fractional_table:
                        # TRUE FRACTIONAL - show success
                        st.success(f"""
✅ **Portfolio 100% Deployed!**

You have ${actual_undeployed_cash:,.2f} ({actual_undeployed_pct:.1f}%) remaining as **fractional remainder**.

**Why can't this be deployed?**
You can't buy partial shares. The cheapest asset in your portfolio costs ${cheapest_price_table:.2f}/share, but you only have ${actual_undeployed_cash:.2f}.

**This is NORMAL and expected!** Your deployment efficiency of **{deployment_pct:.1f}%** is excellent.

**Options for ${actual_undeployed_cash:,.0f}:**
- Keep as cash reserve for rebalancing (recommended)
- Add more capital via **💰 Capital Overview** section above
- Add to next capital injection
                        """)
                    elif actual_undeployed_cash > 100:  # More than just fractional remainder
                        st.warning(f"""
⚠️ **You have ${actual_undeployed_cash:,.0f} ({actual_undeployed_pct:.1f}%) undeployed**

This is NOT just fractional remainder - you can still deploy more capital!

**Why this matters:**
- You haven't fully deployed your portfolio yet
- Capital is sitting idle instead of working for you
- You're not at your target allocation levels

**What to do:**
1. Go to **💰 Capital Overview** section above
2. Click **"🚀 Deploy All Remaining Cash"** button
3. Or manually deploy more in **Asset Deployment** section

After full deployment, you'll typically have only $100-300 left as true fractional remainder (can't buy partial shares).
                        """)
                    else:
                        # Small amount but might still be deployable
                        st.info(f"""
💡 **${actual_undeployed_cash:,.0f} ({actual_undeployed_pct:.1f}%) undeployed**

This is likely fractional remainder - check if you can still deploy any amount in the **💰 Capital Overview** section above.

Your deployment efficiency of **{deployment_pct:.1f}%** is excellent!
                        """)
                
                col_metric1, col_metric2 = st.columns(2)
                with col_metric1:
                    st.metric("CAGR", f"{profile_cagr:.2f}%")
                with col_metric2:
                    st.metric("Total Trade Volume", f"${total_turnover:,.0f}")
                
                st.divider()
                
                # Two-Step Rebalance Workflow
                st.markdown("### 🚀 Two-Step Rebalance Workflow")
                st.caption("Professional slippage management: Get recommendations, execute at broker, then enter actual prices")
                
                with st.expander("ℹ️ How the two-step workflow works", expanded=False):
                    st.markdown("""
                    **Why two steps?**
                    
                    Market prices change constantly. The prices shown are **estimates**.
                    Your **actual broker fills** may differ due to slippage and spreads.
                    
                    **The Workflow:**
                    1. **📋 Recommend**: View suggested trades at current prices
                    2. **🏦 Execute at Broker**: Go to your broker and execute trades
                    3. **✅ Enter Actual Prices**: Return here with your **exact fill prices**
                    4. **💾 Commit**: App updates with real-world data
                    """)
                
                col_exec1, col_exec2 = st.columns(2)
                
                with col_exec1:
                    st.markdown("#### 📋 Step 1: Get Recommendation")
                    if needs_rebalance:
                        st.warning("⚠️ **Rebalancing recommended**")
                    
                    if st.button("📋 Recommend Rebalance", type="primary" if needs_rebalance else "secondary",
                                use_container_width=True, disabled=not needs_rebalance, key="recommend_rebalance"):
                        recommendations = []
                        for t in v_t:
                            old_units = float(asset_dict[t]["units"])
                            new_units = float((asset_dict[t]["target"] / 100 * curr_v) / data[t].iloc[-1])
                            change_units = new_units - old_units
                            # Store both exact and rounded (can't buy/sell fractional shares at most brokers)
                            change_units_rounded = round(change_units)
                            if abs(change_units_rounded) >= 1:
                                action = "BUY" if change_units > 0 else "SELL"
                                current_price = float(data[t].iloc[-1])
                                recommendations.append({
                                    "ticker": t, "action": action, 
                                    "exact_shares": abs(change_units),  # Precise calculation
                                    "shares": abs(change_units_rounded),  # Rounded for execution
                                    "estimated_price": current_price, 
                                    "estimated_value": abs(change_units_rounded) * current_price
                                })
                        store_rebalance_recommendation(prof, recommendations)
                        save_db(st.session_state.db)
                        st.session_state.show_rebalance_recommendation = True
                        st.rerun()
                    
                    if not needs_rebalance:
                        st.info("✔ Portfolio is optimally balanced")
                
                with col_exec2:
                    st.markdown("#### ✅ Step 2: Execute with Actuals")
                    st.caption("After trading, enter your actual fill prices")
                    has_recommendation = "pending_rebalance" in prof
                    if st.button("✅ Execute Rebalance Now", type="primary", use_container_width=True,
                                disabled=not has_recommendation, key="execute_rebalance"):
                        st.session_state.show_execute_form = True
                        st.rerun()
                    if not has_recommendation:
                        st.info("📋 Get recommendation first")
                    elif st.session_state.get("show_execute_form", False):
                        st.success("👇 **Scroll down** to enter your actual broker prices")
                
                # Show recommendation details
                if st.session_state.get("show_rebalance_recommendation", False) and "pending_rebalance" in prof:
                    st.markdown("---")
                    st.markdown("### 📊 Trade Recommendations - Execute at Your Broker")
                    st.caption(f"Generated: {prof['pending_rebalance']['timestamp']}")
                    
                    recommendations = prof["pending_rebalance"]["recommendations"]
                    if recommendations:
                        st.markdown("**Recommended Trades:**")
                        for rec in recommendations:
                            color = "🟢" if rec['action'] == "BUY" else "🔴"
                            exact_shares = rec.get('exact_shares', rec['shares'])
                            rounded_shares = int(rec['shares'])
                            st.markdown(f"{color} **{rec['action']} {rec['ticker']}**: {exact_shares:.4f} shares ↙ **Execute {rounded_shares:,} shares** @ ~${rec['estimated_price']:.2f} (${rec['estimated_value']:.2f})")
                        
                        st.info("💡 **Note:** Exact calculations shown with recommended whole units to execute at your broker.")
                        
                        st.markdown("""
                        **Next Steps:**
                        1. Go to your broker (Fidelity, IBKR, etc.)
                        2. Execute the **rounded** trades listed above
                        3. Note the **actual prices** you received
                        4. Return here and click **"✅ Execute Rebalance Now"**
                        """)
                    else:
                        st.info("No trades needed - portfolio already balanced")
                        clear_rebalance_recommendation(prof)
                        save_db(st.session_state.db)
                        st.session_state.show_rebalance_recommendation = False
                
                # Actual price entry form
                if st.session_state.get("show_execute_form", False) and "pending_rebalance" in prof:
                    st.markdown("---")
                    st.markdown('''
                        <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                                    border-left: 4px solid #10b981; padding: 16px; border-radius: 8px; margin: 12px 0;">
                            <h3 style="margin: 0 0 8px 0; color: #065f46;">💰 ACTION REQUIRED: Enter Actual Broker Prices</h3>
                            <p style="margin: 0; color: #047857;">Enter the exact prices you received when executing trades at your broker.</p>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    recommendations = prof["pending_rebalance"]["recommendations"]
                    
                    with st.form("actual_prices_form"):
                        st.markdown("**For each trade, enter the actual price:**")
                        actual_prices = {}
                        
                        for rec in recommendations:
                            exact_shares = rec.get('exact_shares', rec['shares'])
                            rounded_shares = int(rec['shares'])
                            st.markdown(f"**{rec['action']} {rec['ticker']}**")
                            st.caption(f"Calculated: {exact_shares:.4f} shares ↙ **Execute: {rounded_shares:,} shares**")
                            st.caption(f"Estimated price: ${rec['estimated_price']:.2f}")
                            actual_price = st.number_input(f"Actual price for {rec['ticker']}",
                                min_value=0.01, value=float(rec['estimated_price']), step=0.01,
                                format="%.2f", key=f"actual_price_{rec['ticker']}")
                            actual_prices[rec['ticker']] = actual_price
                            slippage = ((actual_price / rec['estimated_price']) - 1) * 100
                            slippage_color = "🟢" if abs(slippage) < 0.5 else "🟡" if abs(slippage) < 2 else "🔴"
                            st.caption(f"{slippage_color} Slippage: {slippage:+.2f}%")
                            st.markdown("---")
                        
                        col_submit, col_cancel = st.columns(2)
                        with col_submit:
                            submitted = st.form_submit_button("💾 Commit Rebalance", type="primary", use_container_width=True)
                        with col_cancel:
                            cancelled = st.form_submit_button("❌ Cancel", use_container_width=True)
                        
                        if submitted:
                            detail_log = f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - "
                            changes = []
                            for rec in recommendations:
                                ticker = rec['ticker']
                                actual_price = actual_prices[ticker]
                                shares = int(rec['shares'])  # Ensure whole units
                                if rec['action'] == "BUY":
                                    asset_dict[ticker]["units"] = int(asset_dict[ticker]["units"]) + shares
                                    changes.append(f"🟢 {ticker} BUY {shares:,} @ ${actual_price:.2f}")
                                else:
                                    asset_dict[ticker]["units"] = int(asset_dict[ticker]["units"]) - shares
                                    changes.append(f"🔴 {ticker} SELL {shares:,} @ ${actual_price:.2f}")
                            
                            detail_log += ", ".join(changes) if changes else "No changes"
                            prof.setdefault("rebalance_stats", []).insert(0, detail_log)
                            prof["rebalance_stats"] = prof["rebalance_stats"][:50]
                            prof["last_rebalanced"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            # Store recommendations before clearing for email
                            email_recommendations = recommendations.copy()
                            
                            clear_rebalance_recommendation(prof)
                            log_profile(prof, "Portfolio rebalanced with actual prices - Status: Balanced")
                            save_db(st.session_state.db)
                            
                            # Send confirmation email
                            email_success, email_msg = send_rebalance_confirmation_email(
                                st.session_state.db, 
                                current_user, 
                                st.session_state.active_profile,
                                email_recommendations,
                                actual_prices
                            )
                            
                            st.session_state.show_execute_form = False
                            st.session_state.show_rebalance_recommendation = False
                            st.success("✅ Portfolio rebalanced successfully!")
                            if email_success:
                                st.info("🔧 Confirmation email sent!")
                            st.balloons()
                            st.rerun()
                        
                        if cancelled:
                            st.session_state.show_execute_form = False
                            st.rerun()
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Check your internet connection and verify ticker symbols.")
        
        # Rebalance History
        if tickers and st.session_state.active_profile:
            prof = user_profiles[st.session_state.active_profile]
            rebalance_events = prof.get('rebalance_stats', [])
            
            if rebalance_events:
                st.divider()
                st.markdown("## 📜 Rebalance History")
                st.caption("Complete history of all rebalancing events")
                
                with st.expander("ℹ️ How to read rebalance history", expanded=False):
                    st.markdown("""
                    **Each entry shows trades executed:**
                    - 🟢 **BUY**: Shares purchased with actual broker price
                    - 🔴 **SELL**: Shares sold with actual broker price
                    - **Format**: `Date - 🟢 AAPL BUY 5.2345 @ $150.25`
                    """)
                
                col_filter1, col_filter2 = st.columns([3, 1])
                with col_filter1:
                    time_filter = st.selectbox("Group by", ["All Events", "Last 30 Days", "Last 90 Days", "This Year"], key="history_filter")
                with col_filter2:
                    events_per_page = st.selectbox("Show", [10, 25, 50], index=0, key="events_per_page")
                
                filtered_events = []
                now = datetime.now()
                
                for event in rebalance_events:
                    try:
                        event_date_str = event.split(" - ")[0].split(" ")[0]
                        event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
                        
                        if time_filter == "All Events":
                            filtered_events.append((event_date, event))
                        elif time_filter == "Last 30 Days" and (now - event_date).days <= 30:
                            filtered_events.append((event_date, event))
                        elif time_filter == "Last 90 Days" and (now - event_date).days <= 90:
                            filtered_events.append((event_date, event))
                        elif time_filter == "This Year" and event_date.year == now.year:
                            filtered_events.append((event_date, event))
                    except:
                        if time_filter == "All Events":
                            filtered_events.append((now, event))
                
                filtered_events.sort(key=lambda x: x[0], reverse=True)
                
                st.markdown(f"### 📊 Showing {min(len(filtered_events), events_per_page)} of {len(filtered_events)} events")
                for event_date, event in filtered_events[:events_per_page]:
                    st.caption(event)
                
                if len(filtered_events) > events_per_page:
                    st.info(f"💡 {len(filtered_events) - events_per_page} more events available.")
            else:
                st.divider()
                st.info("📜 No rebalancing history yet.")

# Footer
st.divider()
st.markdown(f"""
    <div style="text-align: center; color: #64748b; padding: 20px;">
        <p><strong>Long Term Strategy Optimizer</strong> • v{VERSION} - {VERSION_NAME}</p>
        <p style="font-size: 0.85rem;">Built: {VERSION_DATE} {VERSION_TIME} • Market data by Yahoo Finance</p>
        <p style="font-size: 0.8rem;">For informational purposes only</p>
    </div>
""", unsafe_allow_html=True)
