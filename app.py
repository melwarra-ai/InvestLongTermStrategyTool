import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import json
import os

# ===== VERSION INFORMATION =====
VERSION = "5.10.1"
VERSION_DATE = "2026-01-10"
VERSION_NAME = "Dashboard Reorganization: Optimized Section Order"

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
    
    /* v5.8.2 NEW: Professional fintech profile tile header - Slate/Charcoal */
    /* Green reserved ONLY for status indicators (deployment, rebalance success) */
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
    
    </style>
""", unsafe_allow_html=True)

# ===== PERSISTENCE LAYER =====
DB_FILE = "alphastream_wealth.json"

def load_db():
    base_schema = {"profiles": {}, "global_logs": []}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try: 
                data = json.load(f)
                data.setdefault("profiles", {})
                data.setdefault("global_logs", [])
                for p in data["profiles"].values():
                    p.setdefault("drift_tolerance", 5.0)
                    p.setdefault("rebalance_stats", [])
                    p.setdefault("last_rebalanced", None)
                    p.setdefault("benchmark", None)
                    
                    # v5.6 fields
                    p.setdefault("bank_name", "")
                    p.setdefault("account_type", "")
                    
                    # Workflow field migration
                    p.setdefault("account_name", "")
                    p.setdefault("initialization_date", p.get("start_date", ""))
                    p.setdefault("asset_mix_locked", False)
                    
                    # Migrate assets to new schema
                    for asset_key, asset_data in p.get("assets", {}).items():
                        asset_data.setdefault("fund_name", asset_key)
                        asset_data.setdefault("allocated_pct", 0.0)
                        asset_data.setdefault("purchases", [])
                return data
            except: 
                return base_schema
    return base_schema

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_profile(prof, message):
    prof.setdefault("rebalance_logs", [])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    prof["rebalance_logs"].insert(0, {
        "date": timestamp, 
        "event": str(message)
    })
    prof["rebalance_logs"] = prof["rebalance_logs"][:50]

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

def calculate_average_cost(asset_data):
    """
    Calculate weighted average cost for an asset.
    Only returns value when asset is 100% allocated.
    """
    allocated_pct = asset_data.get("allocated_pct", 0)
    if allocated_pct < 100.0:
        return None
    
    purchases = asset_data.get("purchases", [])
    if not purchases:
        return None
    
    total_invested = sum(p.get("amount", 0) for p in purchases)
    total_quantity = sum(p.get("quantity", 0) for p in purchases)
    
    if total_quantity == 0:
        return None
    
    return total_invested / total_quantity

def calculate_drift_status(p_data, prices):
    """
    Per-asset drift detection:
    Check drift for ANY asset that is 100% deployed
    """
    p_assets = p_data.get("assets", {})
    if not p_assets:
        return False, []
    
    curr_v = float(sum(p_assets[t]["units"] * prices.get(t, 0) for t in p_assets))
    if curr_v == 0:
        return False, []
    
    has_rebalanced = p_data.get("last_rebalanced") is not None
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
    """v5.6: Validate deployment date constraints"""
    try:
        inception_date = datetime.strptime(inception_date_str, '%Y-%m-%d').date()
        
        if deploy_date < inception_date:
            return False, f"Deployment date cannot be before inception date ({inception_date})"
        
        if deploy_date > date.today():
            return False, "Deployment date cannot be in the future"
        
        return True, ""
    except:
        return False, "Invalid date format"

# v5.7 NEW: Rebalance recommendation storage
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

# ===== SESSION STATE =====
if "db" not in st.session_state:
    st.session_state.db = load_db()
if "current_page" not in st.session_state:
    st.session_state.current_page = "Global Dashboard"
if "active_profile" not in st.session_state:
    st.session_state.active_profile = None
# v5.7 NEW: Rebalance workflow state
if "show_rebalance_recommendation" not in st.session_state:
    st.session_state.show_rebalance_recommendation = False
if "show_execute_form" not in st.session_state:
    st.session_state.show_execute_form = False

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### 📊 Portfolio Optimizer")
    st.caption(f"Long Term Strategy Suite v{VERSION}")
    
    st.divider()
    
    # Navigation - v5.8.3 FIX: Auto-switch to Portfolio Manager when profile clicked
    # Determine default index based on whether a profile is selected
    if st.session_state.get("active_profile"):
        default_nav_index = 1  # Portfolio Manager
    else:
        default_nav_index = 0  # Global Dashboard
    
    view_mode = st.radio(
        "Navigation",
        ["🏠 Global Dashboard", "📊 Portfolio Manager"],
        index=default_nav_index,
        key="nav_radio"
    )
    
    st.divider()
    
    # ① Profile Creation
    st.markdown("### ① Strategy Setup")
    with st.expander("🆕 Create New Profile", expanded=False):
        with st.form("new_profile_form"):
            n_name = st.text_input("Profile Name*", placeholder="e.g., Retirement USD")
            
            col1, col2 = st.columns(2)
            with col1:
                n_bank = st.text_input(
                    "Bank/Broker*",
                    placeholder="e.g., Fidelity, IBKR",
                    help="Name of your financial institution"
                )
            with col2:
                n_account_type = st.selectbox(
                    "Account Type*",
                    ["", "Taxable", "401k", "IRA", "Roth IRA", "TFSA", "RRSP", "529", "HSA", "Other"],
                    help="Type of investment account"
                )
            
            n_curr = st.selectbox("Currency*", ["USD", "CAD"])
            n_p = st.number_input("Principal ($)*", value=10000.0, step=1000.0, min_value=0.0)
            n_goal = st.number_input("Annual Growth Goal (%)*", value=10.0, step=0.5, min_value=0.0)
            
            n_start = st.date_input(
                "Inception Date*", 
                value=date.today() - timedelta(days=365),
                max_value=date.today(),
                help="Portfolio start date (cannot be in the future)"
            )
            
            submitted = st.form_submit_button("🚀 Initialize Profile", use_container_width=True)
            
            if submitted:
                if not n_name:
                    st.error("❌ Profile name is required")
                elif not n_bank:
                    st.error("❌ Bank/Broker is required")
                elif not n_account_type:
                    st.error("❌ Account Type is required")
                elif n_name in st.session_state.db["profiles"]:
                    st.warning(f"⚠️ Profile '{n_name}' already exists")
                else:
                    st.session_state.db["profiles"][n_name] = {
                        "currency": n_curr,
                        "principal": n_p,
                        "yearly_goal_pct": n_goal,
                        "start_date": str(n_start),
                        "bank_name": n_bank,
                        "account_type": n_account_type,
                        "account_name": f"{n_bank} {n_account_type}",
                        "initialization_date": str(n_start),
                        "asset_mix_locked": False,
                        "assets": {},
                        "rebalance_logs": [],
                        "drift_tolerance": 5.0,
                        "rebalance_stats": [],
                        "last_rebalanced": None,
                        "benchmark": None
                    }
                    save_db(st.session_state.db)
                    log_profile(st.session_state.db["profiles"][n_name], "Profile created")
                    st.success(f"✅ Profile '{n_name}' created!")
                    st.rerun()
    
    # Profile-specific sidebar content
    if view_mode == "📊 Portfolio Manager" and st.session_state.db["profiles"]:
        st.divider()
        st.markdown("### 🎯 Active Profile")
        
        profile_names = list(st.session_state.db["profiles"].keys())
        
        if st.session_state.active_profile and st.session_state.active_profile in profile_names:
            default_index = profile_names.index(st.session_state.active_profile)
        else:
            default_index = 0
        
        selected = st.selectbox(
            "Select Profile",
            profile_names,
            index=default_index,
            key="profile_selector"
        )
        
        if selected != st.session_state.active_profile:
            st.session_state.active_profile = selected
            st.rerun()
        
        prof = st.session_state.db["profiles"][st.session_state.active_profile]
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
            if st.button("🔄 Reset", use_container_width=True, key="reset_profile"):
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
                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                        prof['principal'] = edit_principal
                        prof['yearly_goal_pct'] = edit_goal
                        prof['bank_name'] = edit_bank
                        prof['account_type'] = edit_acct
                        prof['account_name'] = f"{edit_bank} {edit_acct}"
                        save_db(st.session_state.db)
                        log_profile(prof, "Profile edited")
                        st.session_state.editing_profile = False
                        st.success("✅ Profile updated!")
                        st.rerun()
                
                with col_cancel:
                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                        st.session_state.editing_profile = False
                        st.rerun()
        
        # Reset Confirmation
        if st.session_state.get("reset_confirm", False):
            st.warning("⚠️ **Reset Profile?**")
            st.caption("This will delete all assets, deployments, and rebalance history. Profile metadata will be preserved.")
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                if st.button("🔄 Yes, Reset", use_container_width=True, type="primary", key="confirm_reset"):
                    prof['assets'] = {}
                    prof['rebalance_logs'] = []
                    prof['rebalance_stats'] = []
                    prof['last_rebalanced'] = None
                    prof['asset_mix_locked'] = False
                    clear_rebalance_recommendation(prof)  # v5.7 NEW
                    save_db(st.session_state.db)
                    log_profile(prof, "Profile reset - all asset data cleared")
                    st.session_state.reset_confirm = False
                    st.success("✅ Profile reset successfully!")
                    st.rerun()
            
            with col_r2:
                if st.button("❌ Cancel", use_container_width=True, key="cancel_reset"):
                    st.session_state.reset_confirm = False
                    st.rerun()
        
        # Delete Confirmation
        if st.session_state.get("delete_confirm", False):
            st.error("🗑️ **Delete Profile?**")
            st.caption(f"This will permanently delete '{st.session_state.active_profile}'. This action cannot be undone.")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if st.button("🗑️ Yes, Delete", use_container_width=True, type="primary", key="confirm_delete"):
                    profile_to_delete = st.session_state.active_profile
                    del st.session_state.db["profiles"][profile_to_delete]
                    save_db(st.session_state.db)
                    st.session_state.active_profile = None
                    st.session_state.delete_confirm = False
                    st.success(f"✅ Profile '{profile_to_delete}' deleted!")
                    st.rerun()
            
            with col_d2:
                if st.button("❌ Cancel", use_container_width=True, key="cancel_delete"):
                    st.session_state.delete_confirm = False
                    st.rerun()
        
        st.divider()
        
        # ② Drift Strategy
        st.markdown("### ② Drift Strategy")
        st.caption("Set tolerance threshold for rebalance alerts")
        with st.expander("ℹ️ What is drift tolerance?", expanded=False):
            st.markdown("""
            **Drift tolerance** controls when you get rebalancing alerts.
            
            - If an asset's current % differs from target % by more than this amount, you'll see a 🚨 alert
            - **Example:** 5% tolerance means AAPL at 30% (target 25%) triggers an alert
            - **Lower tolerance** = more frequent rebalancing, tighter control
            - **Higher tolerance** = less frequent rebalancing, more flexibility
            """)
        
        new_tolerance = st.number_input(
            "Drift Tolerance (%)",
            value=float(prof.get('drift_tolerance', 5.0)),
            min_value=0.5,
            max_value=20.0,
            step=0.5,
            help="Alert when any asset drifts this much from target",
            key="drift_tolerance_input"
        )
        if st.button("💾 Update Tolerance", use_container_width=True, key="update_tolerance"):
            prof['drift_tolerance'] = new_tolerance
            save_db(st.session_state.db)
            log_profile(prof, f"Updated drift tolerance to {new_tolerance}%")
            st.success("✅ Updated!")
            st.rerun()
        
        st.divider()
        
        # ③ Benchmark Selection
        st.markdown("### ③ Benchmark Comparison")
        st.caption("Compare your portfolio against market benchmarks")
        with st.expander("ℹ️ Why use a benchmark?", expanded=False):
            st.markdown("""
            **Benchmarks** help you evaluate your portfolio's performance.
            
            - The chart shows what would happen if you invested 100% in the benchmark
            - **Example:** If you choose SPY, you'll see S&P 500 performance vs your allocation
            - **Outperforming** the benchmark means your strategy is adding value
            - **Underperforming** suggests passive investing might be better
            """)
        
        benchmark_options = {
            "None": None,
            "S&P 500 (SPY) - Large Cap US Stocks": "SPY",
            "NASDAQ-100 (QQQ) - Tech-Heavy Large Cap": "QQQ",
            "Total Market (VTI) - All US Stocks": "VTI",
            "Russell 2000 (IWM) - Small Cap US": "IWM",
            "Dow Jones (DIA) - 30 Blue Chip Stocks": "DIA"
        }
        
        current_benchmark = prof.get('benchmark')
        benchmark_index = 0
        for idx, (key, value) in enumerate(benchmark_options.items()):
            if value == current_benchmark:
                benchmark_index = idx
                break
        
        selected_benchmark = st.selectbox(
            "Select Benchmark for Comparison",
            options=list(benchmark_options.keys()),
            index=benchmark_index,
            key="benchmark_select",
            help="Choose a market index to compare your portfolio's performance."
        )
        
        if st.button("💾 Save Benchmark", use_container_width=True, key="save_benchmark"):
            prof['benchmark'] = benchmark_options[selected_benchmark]
            save_db(st.session_state.db)
            st.success("✅ Benchmark saved!")
            st.rerun()
        
        if prof.get('benchmark'):
            st.caption(f"📊 Active: {prof['benchmark']} - Shows 100% investment comparison")
        else:
            st.caption("No benchmark selected")
        
        st.divider()
        
        # ④ Asset Allocation
        st.markdown("### ④ Asset Allocation")
        st.caption("Add assets to your portfolio and set target percentages")
        with st.expander("ℹ️ How asset allocation works", expanded=False):
            st.markdown("""
            **Asset allocation** is your investment strategy blueprint.
            
            - **Target %**: Your desired allocation (e.g., 40% AAPL, 30% GOOGL, 30% MSFT)
            - **Total must equal 100%** to be fully allocated
            - **Buying Guide**: Shows exactly how many shares to buy
            - **Rebalancing**: When prices change, your % drifts—rebalance to restore targets
            
            💡 **Pro tip:** Diversify across sectors to reduce risk
            """)
        
        with st.expander("💡 Need help finding tickers?", expanded=False):
            st.caption("**Popular Examples:**")
            st.caption("• Stocks: AAPL, MSFT, GOOGL, AMZN, TSLA")
            st.caption("• ETFs: SPY, QQQ, VTI, VOO, IWM")
            st.caption("• Bonds: AGG, BND, TLT")
            st.caption("")
            st.caption("Find more at: finance.yahoo.com")
        
        # Calculate current allocation
        current_alloc = sum(a.get('target', 0) for a in prof.get("assets", {}).values())
        
        # Allocation progress bar
        progress_color = "🟢" if current_alloc >= 100 else "🟡"
        bar_color = "#10b981" if current_alloc >= 100 else "#f97316"
        
        st.markdown(f"""
            <div style="margin: 12px 0;">
                <div style="background: #e5e7eb; border-radius: 8px; height: 8px; overflow: hidden;">
                    <div style="background: {bar_color}; height: 100%; width: {min(current_alloc, 100)}%; transition: all 0.3s;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**{progress_color} Allocated: {current_alloc:.1f}% / 100%**")
        
        # Asset ticker input
        a_sym = st.text_input(
            "Ticker Symbol",
            placeholder="e.g., AAPL, MSFT",
            help="Enter stock ticker and press Enter",
            key="ticker_input"
        ).upper().strip()
        
        is_existing = a_sym in prof.get("assets", {})
        
        # Calculate available allocation space
        if is_existing:
            other_allocs = current_alloc - prof["assets"][a_sym].get("target", 0)
        else:
            other_allocs = current_alloc
        
        max_available = 100.0 - other_allocs
        block_new = (not is_existing) and (max_available <= 0) and (a_sym != "")
        
        # Show allocation block warning
        if block_new:
            st.markdown("""
                <div class="allocation-blocked">
                    🚫 PORTFOLIO AT 100%<br>
                    Remove or reduce existing assets first!
                </div>
            """, unsafe_allow_html=True)
        
        valid_ticker = False
        last_price = 1.0
        ticker_name = ""
        
        # Validate ticker
        if prof.get("asset_mix_locked", False) and not is_existing and a_sym:
            st.error("🔒 **Asset mix is locked**")
            st.caption("Cannot add new assets during deployment phase.")
            st.caption("Complete all deployments, then unlock mix to modify assets.")
            valid_ticker = False
        elif a_sym and not block_new:
            try:
                with st.spinner(f"🔍 Validating {a_sym}..."):
                    t_check = yf.Ticker(a_sym)
                    hist = t_check.history(period="1d")
                    if not hist.empty:
                        last_price = float(hist['Close'].iloc[-1])
                        try:
                            ticker_info = t_check.info
                            ticker_name = ticker_info.get('longName', a_sym)
                        except:
                            ticker_name = a_sym
                        st.success(f"✓ {ticker_name}")
                        st.caption(f"**Current Price:** {p_flag} ${last_price:,.2f}")
                        valid_ticker = True
                    else:
                        st.error(f"❌ No price data available for '{a_sym}'")
            except:
                if a_sym:
                    st.error(f"❌ Cannot validate '{a_sym}'. Please verify it's a valid stock symbol.")
                    st.caption("💡 Try: AAPL, MSFT, GOOGL, TSLA, SPY, QQQ")
        
        # Asset form
        if valid_ticker:
            st.markdown("---")
            
            default_target = prof.get("assets", {}).get(a_sym, {}).get("target", 0.0)
            default_units = prof.get("assets", {}).get(a_sym, {}).get("units", 0.0)
            
            a_w = st.number_input(
                f"Target Allocation %",
                min_value=0.0,
                max_value=max_available,
                value=min(float(default_target), max_available),
                step=0.5,
                help=f"Maximum available: {max_available:.1f}%",
                key="target_weight"
            )
            
            # Buying Guide
            if a_w > 0:
                target_value = (a_w / 100) * prof['principal']
                suggested_units = target_value / last_price
                
                st.markdown(f"""
                    <div class="buying-guide">
                        💡 <strong>Buy Guide:</strong> To reach {a_w}% → Buy <span class="buying-guide-highlight">{suggested_units:.4f} units</span> (${target_value:,.0f} @ ${last_price:,.2f}/unit)
                    </div>
                """, unsafe_allow_html=True)
            
            a_u = st.number_input(
                "Units Currently Owned",
                min_value=0.0,
                value=float(default_units),
                step=0.0001,
                format="%.4f",
                help="How many shares do you own?",
                key="units_owned"
            )
            
            st.markdown("---")
            
            col_b1, col_b2 = st.columns(2)
            
            with col_b1:
                save_disabled = (a_w <= 0) or (a_w > max_available)
                if st.button("💾 Save Asset", use_container_width=True, type="primary", key="save_asset", disabled=save_disabled):
                    prof.setdefault("assets", {})[a_sym] = {
                        "fund_name": ticker_name,
                        "units": a_u,
                        "target": a_w,
                        "allocated_pct": prof.get("assets", {}).get(a_sym, {}).get("allocated_pct", 0.0),
                        "purchases": prof.get("assets", {}).get(a_sym, {}).get("purchases", [])
                    }
                    action = "Updated" if is_existing else "Added"
                    log_profile(prof, f"{action} {a_sym}: {a_w}% target, {a_u:.4f} units")
                    save_db(st.session_state.db)
                    st.success(f"✅ {action} {a_sym}!")
                    st.rerun()
            
            with col_b2:
                if is_existing:
                    if st.button("🗑️ Remove", use_container_width=True, key="remove_asset"):
                        del prof["assets"][a_sym]
                        log_profile(prof, f"Removed {a_sym} from portfolio")
                        save_db(st.session_state.db)
                        st.success(f"✅ Removed {a_sym}!")
                        st.rerun()
        
        # Show existing assets
        if prof.get("assets"):
            st.divider()
            st.markdown("### 📋 Current Assets")
            for ticker, data in prof["assets"].items():
                st.caption(f"**{ticker}**: {data['target']}% ({data['units']:.4f} units)")
        
        # ⑤ Asset Mix Locking
        st.divider()
        st.markdown("### ⑤ Lock Asset Mix")
        
        assets = prof.get("assets", {})
        total_allocation = sum(a.get('target', 0) for a in assets.values())
        is_complete = (total_allocation == 100.0 and len(assets) > 0)
        
        if prof.get("asset_mix_locked", False):
            st.success("✅ **Asset Mix Locked**")
            st.caption(f"{len(assets)} assets defined. Ready for deployment.")
            
            any_deployments = any(a.get("allocated_pct", 0) > 0 for a in assets.values())
            
            if not any_deployments:
                if st.button("🔓 Unlock Asset Mix", use_container_width=True, key="unlock_mix"):
                    prof["asset_mix_locked"] = False
                    save_db(st.session_state.db)
                    log_profile(prof, "Asset mix unlocked")
                    st.rerun()
            else:
                st.caption("⚠️ Cannot unlock - deployments recorded")
        else:
            if is_complete:
                st.warning("🔓 **Ready to Lock**")
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
        
        # ⑥ Asset Deployment
        st.markdown("### ⑥ Asset Deployment")
        st.caption("Deploy capital into individual assets over time")
        
        if not prof.get("asset_mix_locked", False):
            st.info("🔒 **Lock your asset mix first** to enable deployment")
            st.caption("Complete asset definitions (totaling 100%) and lock the mix before deploying capital.")
        else:
            assets = prof.get("assets", {})
            deployable_assets = {
                ticker: data 
                for ticker, data in assets.items()
                if data.get("allocated_pct", 0) < 100.0
            }
            
            fully_deployed_count = sum(
                1 for a in assets.values() 
                if a.get("allocated_pct", 0) >= 100.0
            )
            total_assets = len(assets)
            
            st.markdown(f"**Progress:** {fully_deployed_count}/{total_assets} assets fully deployed")
            
            if total_assets > 0:
                deployment_progress = fully_deployed_count / total_assets
                
                if deployment_progress >= 1.0:
                    bar_color = "#10b981"
                    st.markdown("""
                        <style>
                        div[data-testid="stProgress"] > div > div > div {
                            background-color: #10b981 !important;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                else:
                    bar_color = "#f97316"
                    st.markdown("""
                        <style>
                        div[data-testid="stProgress"] > div > div > div {
                            background-color: #f97316 !important;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                
                st.progress(deployment_progress)
                
                status_text = "✅ All Deployed" if deployment_progress >= 1.0 else f"⏳ In Progress ({fully_deployed_count}/{total_assets})"
                st.markdown(f"**{status_text}**")
            
            if not deployable_assets:
                st.success("✅ **All assets 100% deployed!**")
                st.caption("Portfolio-level drift monitoring is now active.")
                
                with st.expander("✏️ View Deployment History", expanded=False):
                    st.markdown("Review your deployment history for each asset. All assets are fully deployed.")
                    
                    for ticker, asset_data in assets.items():
                        fund_name = asset_data.get("fund_name", ticker)
                        purchases = asset_data.get("purchases", [])
                        allocated_pct = asset_data.get("allocated_pct", 0)
                        avg_cost = calculate_average_cost(asset_data)
                        
                        st.markdown(f"### {ticker} - {fund_name}")
                        st.caption(f"✅ {allocated_pct:.1f}% deployed | Avg Cost: ${avg_cost:.2f}" if avg_cost else f"✅ {allocated_pct:.1f}% deployed")
                        
                        if purchases:
                            history_data = []
                            for p in purchases:
                                history_data.append({
                                    "Date": p.get("date", "N/A"),
                                    "Deploy %": f"{p.get('deploy_pct', 0):.1f}%",
                                    "Amount": f"${p.get('amount', 0):,.2f}",
                                    "Price": f"${p.get('price', 0):.2f}",
                                    "Quantity": f"{p.get('quantity', 0):.4f}"
                                })
                            
                            df_history = pd.DataFrame(history_data)
                            st.dataframe(df_history, use_container_width=True, hide_index=True)
                        else:
                            st.caption("No deployment history recorded")
                        
                        st.markdown("---")
                        
            else:
                with st.expander("➕ Record Asset Deployment", expanded=False):
                    st.markdown("""
                    **Deploy capital into a specific asset** at market prices from a selected date.
                    
                    - **Deployment %** is relative to that asset's target allocation
                    - Each asset can be deployed gradually over multiple events
                    - **Average cost** activates when an asset reaches 100% deployment
                    - **Portfolio drift** activates when ALL assets reach 100%
                    """)
                    
                    selected_ticker = st.selectbox(
                        "Select Asset to Deploy",
                        options=list(deployable_assets.keys()),
                        format_func=lambda t: f"{t} - {deployable_assets[t].get('fund_name', t)}",
                        key="deploy_asset_selector",
                        help="Choose which asset to deploy capital into"
                    )
                    
                    if selected_ticker:
                        asset_data = deployable_assets[selected_ticker]
                        current_allocated = asset_data.get("allocated_pct", 0)
                        remaining_pct = 100.0 - current_allocated
                        target_pct = asset_data.get("target", 0)
                        fund_name = asset_data.get("fund_name", selected_ticker)
                        
                        st.markdown(f"""
                            **Asset Information:**  
                            • **Fund:** {fund_name}  
                            • **Ticker:** {selected_ticker}  
                            • **Target Allocation:** {target_pct}% of total portfolio  
                            • **Currently Deployed:** {current_allocated:.1f}% of this asset's target  
                            • **Remaining:** {remaining_pct:.1f}% of this asset's target
                        """)
                        
                        existing_purchases = asset_data.get("purchases", [])
                        if existing_purchases:
                            st.markdown("**Previous Deployments:**")
                            for idx, p in enumerate(existing_purchases, 1):
                                st.caption(f"{idx}. {p.get('date')}: {p.get('deploy_pct', 0):.1f}% (${p.get('amount', 0):,.2f} @ ${p.get('price', 0):.2f})")
                        
                        st.divider()
                        
                        deploy_pct = st.number_input(
                            "Deploy % (of this asset's target allocation)",
                            min_value=0.1,
                            max_value=remaining_pct,
                            value=min(25.0, remaining_pct),
                            step=0.1,
                            help=f"Enter % of {selected_ticker}'s {target_pct}% target to deploy (max: {remaining_pct:.1f}%)",
                            key="deploy_pct_input"
                        )
                        
                        if deploy_pct > remaining_pct:
                            st.error(f"❌ Cannot deploy {deploy_pct:.1f}% - only {remaining_pct:.1f}% remaining for this asset")
                            deploy_pct = remaining_pct
                        
                        inception_date = datetime.strptime(prof.get('start_date'), '%Y-%m-%d').date()
                        
                        deploy_date = st.date_input(
                            "Deployment Date*",
                            value=date.today(),
                            min_value=inception_date,
                            max_value=date.today(),
                            help=f"Deployment date (must be on or after inception: {inception_date})",
                            key="deploy_date_input"
                        )
                        
                        portfolio_pct = (deploy_pct / 100) * target_pct
                        deploy_amount = (portfolio_pct / 100) * prof['principal']
                        
                        st.info(f"""
                            **📊 Deployment Calculation:**  
                            • {deploy_pct:.1f}% of {selected_ticker}'s {target_pct}% target  
                            • = {portfolio_pct:.2f}% of total ${prof['principal']:,.0f} portfolio  
                            • = **${deploy_amount:,.2f}** to be invested
                        """)
                        
                        if deploy_date == date.today():
                            st.caption("💹 Will use today's closing price")
                        else:
                            st.caption(f"📅 Will use {deploy_date} historical closing price")
                        
                        st.divider()
                        
                        if st.button("🔥 Record Deployment", type="primary", use_container_width=True, key="record_deploy_btn"):
                            try:
                                with st.spinner(f"Fetching price for {selected_ticker} on {deploy_date}..."):
                                    t_obj = yf.Ticker(selected_ticker)
                                    deploy_datetime = pd.to_datetime(deploy_date)
                                    today_dt = pd.to_datetime(date.today())
                                    
                                    if deploy_datetime.date() == today_dt.date():
                                        hist = t_obj.history(period="1d")
                                    else:
                                        start_date = deploy_datetime - timedelta(days=7)
                                        end_date = deploy_datetime + timedelta(days=1)
                                        hist = t_obj.history(start=start_date, end=end_date)
                                    
                                    if hist.empty:
                                        st.error(f"❌ Could not fetch price data for {selected_ticker}")
                                    else:
                                        hist.index = pd.to_datetime(hist.index).date
                                        
                                        if deploy_datetime.date() in hist.index:
                                            price = float(hist.loc[deploy_datetime.date()]['Close'])
                                            price_date = deploy_datetime.date()
                                        else:
                                            available_dates = [d for d in hist.index if d <= deploy_datetime.date()]
                                            if available_dates:
                                                price_date = max(available_dates)
                                                price = float(hist.loc[price_date]['Close'])
                                                
                                                if price_date != deploy_datetime.date():
                                                    st.caption(f"ℹ️ Using {price_date} closing price (closest trading day before {deploy_date})")
                                            else:
                                                st.error(f"❌ No price data available on or before {deploy_date}")
                                                price = None
                                                price_date = None
                                        
                                        if price is not None:
                                            quantity = deploy_amount / price
                                            
                                            purchase = {
                                                "date": str(deploy_date),
                                                "deploy_pct": deploy_pct,
                                                "amount": deploy_amount,
                                                "price": price,
                                                "quantity": quantity
                                            }
                                            
                                            asset_data.setdefault("purchases", []).append(purchase)
                                            asset_data["units"] = asset_data.get("units", 0) + quantity
                                            asset_data["allocated_pct"] = min(100.0, current_allocated + deploy_pct)
                                            
                                            log_msg = (
                                                f"Deployed {deploy_pct:.1f}% of {selected_ticker} "
                                                f"(${deploy_amount:,.2f} @ ${price:.2f}/unit = {quantity:.4f} units)"
                                            )
                                            log_profile(prof, log_msg)
                                            
                                            save_db(st.session_state.db)
                                            
                                            st.success(f"✅ Deployed {deploy_pct:.1f}% of {selected_ticker}")
                                            st.info(f"📊 {selected_ticker} is now {asset_data['allocated_pct']:.1f}% deployed")
                                            
                                            if asset_data['allocated_pct'] >= 100.0:
                                                st.balloons()
                                                st.success(f"🎉 {selected_ticker} is now 100% deployed! Average cost will be calculated.")
                                            
                                            st.rerun()
                            
                            except Exception as e:
                                st.error(f"❌ Error recording deployment: {str(e)}")
                                st.caption("Please check your internet connection and ticker symbol.")
        
        # Activity Log
        st.divider()
        st.markdown("### 📜 Activity Log")
        st.caption("Track all portfolio changes and updates")
        with st.expander("View Recent Activity", expanded=False):
            all_logs = prof.get("rebalance_logs", [])
            logs_to_show = all_logs[:20]
            if logs_to_show:
                for log_entry in logs_to_show:
                    st.caption(f"**{log_entry['date']}**: {log_entry['event']}")
                if len(all_logs) > 20:
                    st.caption(f"... and {len(all_logs) - 20} more entries")
            else:
                st.caption("No activity yet")

# ===== MAIN CONTENT =====
if view_mode == "🏠 Global Dashboard":
    st.title("🏠 Global Portfolio Dashboard")
    
    description_box(
        "Portfolio Command Center",
        "Monitor all your investment strategies at a glance. Track performance, detect drift, and manage multiple portfolios with institutional-grade precision."
    )
    
    profiles = st.session_state.db.get("profiles", {})
    
    if not profiles:
        st.info("👋 Welcome to Long Term Strategy Optimizer! Create your first investment profile using the sidebar.")
        
        st.markdown("### 🎯 Key Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="premium-card">
                    <h4>🎯 Drift Detection</h4>
                    <p style="color: #64748b;">
                        Automatic alerts when assets deviate from target allocation. Stay disciplined with your strategy.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="premium-card">
                    <h4>📈 Performance Tracking</h4>
                    <p style="color: #64748b;">
                        Real-time portfolio valuation vs. your target growth path. See if you're on track.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="premium-card">
                    <h4>⚖️ Smart Rebalancing</h4>
                    <p style="color: #64748b;">
                        Two-step workflow with slippage management for real-world trading accuracy.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
    else:
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
                st.warning("⚠️ Could not fetch current prices. Portfolio values may be outdated.")
        
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
            st.markdown(f"""
                <div class="metric-showcase">
                    <h3>${total_value:,.0f}</h3>
                    <p>Total Portfolio Value</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            st.markdown(f"""
                <div class="metric-showcase" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
                    <h3>{len(profiles)}</h3>
                    <p>Active Strategies</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_m3:
            alert_color = "#ef4444" if total_drift_count > 0 else "#10b981"
            alert_text = f"⚠️ {total_drift_count} Need Rebalancing" if total_drift_count > 0 else f"{total_drift_count} Need Rebalancing"
            st.markdown(f"""
                <div class="metric-showcase" style="background: linear-gradient(135deg, {alert_color} 0%, {alert_color} 100%);">
                    <h3>{total_drift_count}</h3>
                    <p>{alert_text}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # ===== DATA AGGREGATION: Calculate shared data used by multiple sections =====
        # This section runs FIRST to prepare data for Health Score, Performance Insights, 
        # Action Items, Comparison Table, and Pie Chart sections below
        
        comparison_data = []
        action_items = []
        global_assets = {}
        
        for p_name, p_data in profiles.items():
            p_assets = p_data.get("assets", {})
            
            # Calculate current value
            curr_val = float(sum(p_assets[t]["units"] * prices.get(t, 0) for t in p_assets))
            
            # Calculate ROI
            start_val = float(p_data.get('principal', 0))
            roi = ((curr_val / start_val) - 1) * 100 if start_val > 0 else 0
            
            # Calculate CAGR
            start_date = datetime.strptime(p_data.get('start_date', str(date.today())), '%Y-%m-%d')
            years = max((date.today() - start_date.date()).days / 365.25, 0.01)
            cagr = ((curr_val / start_val) ** (1 / years) - 1) * 100 if start_val > 0 else 0
            
            # Check drift status
            needs_rebal, drift_details = calculate_drift_status(p_data, prices)
            
            # Check deployment status
            all_deployed = all(a.get("allocated_pct", 0) >= 100.0 for a in p_assets.values()) if p_assets else False
            deployed_count = sum(1 for a in p_assets.values() if a.get("allocated_pct", 0) >= 100.0)
            total_assets = len(p_assets)
            
            # Determine status
            if needs_rebal:
                status = "🚨 Rebalance"
                status_priority = 1
            elif not all_deployed and total_assets > 0:
                status = f"🔥 Deploying ({deployed_count}/{total_assets})"
                status_priority = 2
            elif all_deployed:
                status = "✅ Balanced"
                status_priority = 3
            else:
                status = "⚪ New"
                status_priority = 4
            
            # Build comparison row
            comparison_data.append({
                "Profile": p_name,
                "Account": f"{p_data.get('bank_name', 'N/A')} {p_data.get('account_type', '')}",
                "Value": curr_val,
                "Value_Display": f"${curr_val:,.0f}",
                "CAGR": cagr,
                "CAGR_Display": f"{cagr:+.1f}%",
                "ROI": roi,
                "ROI_Display": f"{roi:+.1f}%",
                "Goal": f"{p_data.get('yearly_goal_pct', 0):.1f}%/yr",
                "Assets": total_assets,
                "Status": status,
                "Status_Priority": status_priority
            })
            
            # Collect action items
            if needs_rebal:
                drift_count = len(drift_details)
                max_drift = max([d[1] for d in drift_details]) if drift_details else 0
                action_items.append({
                    "priority": 1,
                    "type": "rebalance",
                    "profile": p_name,
                    "message": f"🚨 URGENT - {p_name} needs rebalancing ({drift_count} asset{'s' if drift_count > 1 else ''} drifted, max: {max_drift:.1f}%)",
                    "detail": f"{drift_count} assets exceed {p_data.get('drift_tolerance', 5.0)}% tolerance",
                    "action": "Click profile to view details and execute rebalance"
                })
            elif not all_deployed and total_assets > 0:
                remaining_assets = [(t, a.get("allocated_pct", 0)) for t, a in p_assets.items() if a.get("allocated_pct", 0) < 100.0]
                action_items.append({
                    "priority": 2,
                    "type": "deployment",
                    "profile": p_name,
                    "message": f"🔥 IN PROGRESS - {p_name} deployment ({deployed_count}/{total_assets} assets fully deployed)",
                    "detail": ", ".join([f"{t} needs {100-pct:.0f}% more" for t, pct in remaining_assets[:3]]),
                    "action": "Complete remaining asset deployments"
                })
            
            # Aggregate global assets
            for ticker, asset_data in p_assets.items():
                if ticker in prices:
                    asset_value = asset_data["units"] * prices[ticker]
                    
                    if ticker not in global_assets:
                        global_assets[ticker] = {
                            "value": 0,
                            "units": 0,
                            "portfolios": [],
                            "fund_name": asset_data.get("fund_name", ticker)
                        }
                    
                    global_assets[ticker]["value"] += asset_value
                    global_assets[ticker]["units"] += asset_data["units"]
                    global_assets[ticker]["portfolios"].append(p_name)
        
        # ===== NEW v5.10.0: PORTFOLIO HEALTH SCORE =====
        st.markdown("### 💪 Portfolio Health Score")
        st.caption("Comprehensive assessment of your portfolio's overall health")
        
        with st.expander("ℹ️ How the Health Score Works", expanded=False):
            st.markdown("""
            **Your health score (0-100) is based on:**
            
            1. **Diversification (25 points)**
               - Number of different assets
               - Distribution across portfolios
               - No over-concentration
            
            2. **Deployment (25 points)**
               - % of assets fully deployed
               - Capital utilization
            
            3. **Drift Control (25 points)**
               - How many portfolios are balanced
               - Adherence to target allocations
            
            4. **Performance (25 points)**
               - % of portfolios meeting goals
               - Overall returns vs targets
            
            **Score Ranges:**
            - 90-100: Excellent 🟢
            - 75-89: Good 🟡
            - 60-74: Fair 🟠
            - Below 60: Needs Improvement 🔴
            """)
        
        # Calculate health score components
        if len(profiles) > 0:
            # Component 1: Diversification (0-25 points)
            total_assets = len(global_assets) if global_assets else 0
            diversification_score = 0
            
            if total_assets >= 10:
                diversification_score = 25
            elif total_assets >= 7:
                diversification_score = 20
            elif total_assets >= 5:
                diversification_score = 15
            elif total_assets >= 3:
                diversification_score = 10
            else:
                diversification_score = 5
            
            # Check for over-concentration
            if global_assets:
                total_value = sum(a["value"] for a in global_assets.values())
                if total_value > 0:
                    max_concentration = max(a["value"] / total_value * 100 for a in global_assets.values())
                    if max_concentration > 50:
                        diversification_score -= 10  # Penalty for concentration
                    elif max_concentration > 40:
                        diversification_score -= 5
            
            diversification_score = max(0, min(25, diversification_score))
            
            # Component 2: Deployment (0-25 points)
            if total_assets_count > 0:
                deployment_ratio = deployed_assets / total_assets_count
                deployment_score = deployment_ratio * 25
            else:
                deployment_score = 0
            
            # Component 3: Drift Control (0-25 points)
            balanced_count = len(profiles) - total_drift_count
            if len(profiles) > 0:
                drift_control_score = (balanced_count / len(profiles)) * 25
            else:
                drift_control_score = 0
            
            # Component 4: Performance (0-25 points)
            if len(profiles) > 0:
                performance_score = (on_track_count / len(profiles)) * 25
            else:
                performance_score = 0
            
            # Total score
            total_health_score = diversification_score + deployment_score + drift_control_score + performance_score
            
            # Determine grade
            if total_health_score >= 90:
                grade = "Excellent"
                grade_color = "#10b981"
                grade_emoji = "🟢"
            elif total_health_score >= 75:
                grade = "Good"
                grade_color = "#84cc16"
                grade_emoji = "🟡"
            elif total_health_score >= 60:
                grade = "Fair"
                grade_color = "#f59e0b"
                grade_emoji = "🟠"
            else:
                grade = "Needs Improvement"
                grade_color = "#ef4444"
                grade_emoji = "🔴"
            
            # Display health score gauge
            col_gauge, col_breakdown = st.columns([1, 2])
            
            with col_gauge:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {grade_color} 0%, {grade_color} 100%); 
                                color: white; padding: 40px; border-radius: 16px; text-align: center;
                                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);">
                        <div style="font-size: 4rem; font-weight: 700; margin-bottom: 8px;">
                            {int(total_health_score)}
                        </div>
                        <div style="font-size: 1.5rem; font-weight: 600; margin-bottom: 8px;">
                            {grade} {grade_emoji}
                        </div>
                        <div style="font-size: 1rem; opacity: 0.9;">
                            Portfolio Health Score
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_breakdown:
                st.markdown("**Score Breakdown:**")
                
                # Diversification
                div_pct = (diversification_score / 25) * 100
                div_color = "#10b981" if div_pct >= 75 else "#f59e0b" if div_pct >= 50 else "#ef4444"
                st.markdown(f"""
                    <div style="margin: 12px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="font-weight: 600;">📊 Diversification</span>
                            <span style="font-weight: 700;">{diversification_score:.0f}/25</span>
                        </div>
                        <div style="background: #e5e7eb; border-radius: 8px; height: 12px; overflow: hidden;">
                            <div style="background: {div_color}; height: 100%; width: {div_pct}%; transition: all 0.3s;"></div>
                        </div>
                        <div style="font-size: 0.8rem; color: #64748b; margin-top: 4px;">
                            {total_assets} different assets
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Deployment
                dep_pct = (deployment_score / 25) * 100
                dep_color = "#10b981" if dep_pct >= 75 else "#f59e0b" if dep_pct >= 50 else "#ef4444"
                st.markdown(f"""
                    <div style="margin: 12px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="font-weight: 600;">🔥 Deployment</span>
                            <span style="font-weight: 700;">{deployment_score:.0f}/25</span>
                        </div>
                        <div style="background: #e5e7eb; border-radius: 8px; height: 12px; overflow: hidden;">
                            <div style="background: {dep_color}; height: 100%; width: {dep_pct}%; transition: all 0.3s;"></div>
                        </div>
                        <div style="font-size: 0.8rem; color: #64748b; margin-top: 4px;">
                            {deployed_assets}/{total_assets_count} assets fully deployed
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Drift Control
                drift_pct = (drift_control_score / 25) * 100
                drift_color = "#10b981" if drift_pct >= 75 else "#f59e0b" if drift_pct >= 50 else "#ef4444"
                st.markdown(f"""
                    <div style="margin: 12px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="font-weight: 600;">⚖️ Drift Control</span>
                            <span style="font-weight: 700;">{drift_control_score:.0f}/25</span>
                        </div>
                        <div style="background: #e5e7eb; border-radius: 8px; height: 12px; overflow: hidden;">
                            <div style="background: {drift_color}; height: 100%; width: {drift_pct}%; transition: all 0.3s;"></div>
                        </div>
                        <div style="font-size: 0.8rem; color: #64748b; margin-top: 4px;">
                            {balanced_count}/{len(profiles)} portfolios balanced
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Performance
                perf_pct = (performance_score / 25) * 100
                perf_color = "#10b981" if perf_pct >= 75 else "#f59e0b" if perf_pct >= 50 else "#ef4444"
                st.markdown(f"""
                    <div style="margin: 12px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="font-weight: 600;">🎯 Performance</span>
                            <span style="font-weight: 700;">{performance_score:.0f}/25</span>
                        </div>
                        <div style="background: #e5e7eb; border-radius: 8px; height: 12px; overflow: hidden;">
                            <div style="background: {perf_color}; height: 100%; width: {perf_pct}%; transition: all 0.3s;"></div>
                        </div>
                        <div style="font-size: 0.8rem; color: #64748b; margin-top: 4px;">
                            {on_track_count}/{len(profiles)} portfolios meeting goals
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Recommendations
            st.markdown("---")
            st.markdown("**💡 Recommendations:**")
            
            recommendations = []
            
            if diversification_score < 15:
                recommendations.append("📊 **Increase diversification:** Consider adding more assets (target: 5-10 different holdings)")
            
            if deployment_score < 20:
                recommendations.append("🔥 **Complete deployments:** Finish deploying capital to inactive assets")
            
            if drift_control_score < 15:
                recommendations.append("⚖️ **Rebalance portfolios:** Multiple portfolios have drifted beyond tolerance")
            
            if performance_score < 15:
                recommendations.append("🎯 **Review underperformers:** More than half of portfolios are missing their goals")
            
            if total_health_score >= 90:
                recommendations.append("🎉 **Excellent work!** Your portfolio is in great shape. Keep monitoring and stay disciplined.")
            
            if recommendations:
                for rec in recommendations:
                    st.markdown(f"• {rec}")
            else:
                st.success("✅ Your portfolio health is good! Keep up the great work!")
        
        else:
            st.info("ℹ️ Create a portfolio to see your health score")
        
        st.divider()
        
        # ===== NEW v5.9.2: PERFORMANCE SUMMARY CARDS =====
        st.markdown("### 🏆 Performance Insights")
        st.caption("Quick overview of your portfolio performance and status")
        
        # Calculate summary metrics
        if len(comparison_data) > 0:
            # Find best/worst performers
            best_performer = max(comparison_data, key=lambda x: x['CAGR'])
            worst_performer = min(comparison_data, key=lambda x: x['CAGR'])
            
            # Calculate deployment stats
            total_assets_count = sum(p['Assets'] for p in comparison_data)
            deployed_assets = 0
            total_portfolio_value = 0
            total_deployed_value = 0
            
            for p_name, p_data in profiles.items():
                p_assets = p_data.get("assets", {})
                for ticker, asset_data in p_assets.items():
                    if asset_data.get("allocated_pct", 0) >= 100.0:
                        deployed_assets += 1
                        if ticker in prices:
                            total_deployed_value += asset_data["units"] * prices[ticker]
                
                for ticker in p_assets:
                    if ticker in prices:
                        total_portfolio_value += p_assets[ticker]["units"] * prices[ticker]
            
            # Calculate on-track count
            on_track_count = sum(1 for p in comparison_data if p['CAGR'] >= profiles[p['Profile']].get('yearly_goal_pct', 0))
            
            # Display cards
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            
            with col_c1:
                goal_vs = best_performer['CAGR'] - profiles[best_performer['Profile']].get('yearly_goal_pct', 0)
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                                color: white; padding: 20px; border-radius: 12px; text-align: center;
                                box-shadow: 0 4px 6px rgba(16, 185, 129, 0.4);">
                        <div style="font-size: 2rem; margin-bottom: 8px;">🏆</div>
                        <div style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 4px;">Best Performer</div>
                        <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 4px;">{best_performer['Profile']}</div>
                        <div style="font-size: 1.1rem; font-weight: 600;">{best_performer['CAGR_Display']} CAGR</div>
                        <div style="font-size: 0.8rem; opacity: 0.85; margin-top: 4px;">
                            {'+' if goal_vs >= 0 else ''}{goal_vs:.1f}% vs goal
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_c2:
                goal_vs_worst = worst_performer['CAGR'] - profiles[worst_performer['Profile']].get('yearly_goal_pct', 0)
                color = "#ef4444" if goal_vs_worst < 0 else "#f59e0b"
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {color} 0%, {color} 100%); 
                                color: white; padding: 20px; border-radius: 12px; text-align: center;
                                box-shadow: 0 4px 6px rgba(239, 68, 68, 0.4);">
                        <div style="font-size: 2rem; margin-bottom: 8px;">📉</div>
                        <div style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 4px;">Needs Attention</div>
                        <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 4px;">{worst_performer['Profile']}</div>
                        <div style="font-size: 1.1rem; font-weight: 600;">{worst_performer['CAGR_Display']} CAGR</div>
                        <div style="font-size: 0.8rem; opacity: 0.85; margin-top: 4px;">
                            {'+' if goal_vs_worst >= 0 else ''}{goal_vs_worst:.1f}% vs goal
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_c3:
                deployment_pct = (deployed_assets / total_assets_count * 100) if total_assets_count > 0 else 0
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                                color: white; padding: 20px; border-radius: 12px; text-align: center;
                                box-shadow: 0 4px 6px rgba(59, 130, 246, 0.4);">
                        <div style="font-size: 2rem; margin-bottom: 8px;">📊</div>
                        <div style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 4px;">Total Deployed</div>
                        <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 4px;">
                            {deployed_assets}/{total_assets_count} Assets
                        </div>
                        <div style="font-size: 1.1rem; font-weight: 600;">{deployment_pct:.1f}%</div>
                        <div style="font-size: 0.8rem; opacity: 0.85; margin-top: 4px;">
                            ${total_deployed_value:,.0f} deployed
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_c4:
                on_track_pct = (on_track_count / len(profiles) * 100) if len(profiles) > 0 else 0
                track_color = "#10b981" if on_track_pct >= 50 else "#f59e0b"
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {track_color} 0%, {track_color} 100%); 
                                color: white; padding: 20px; border-radius: 12px; text-align: center;
                                box-shadow: 0 4px 6px rgba(16, 185, 129, 0.4);">
                        <div style="font-size: 2rem; margin-bottom: 8px;">🎯</div>
                        <div style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 4px;">On Track</div>
                        <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 4px;">
                            {on_track_count}/{len(profiles)} Portfolios
                        </div>
                        <div style="font-size: 1.1rem; font-weight: 600;">{on_track_pct:.0f}%</div>
                        <div style="font-size: 0.8rem; opacity: 0.85; margin-top: 4px;">
                            meeting goals
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        
        # ===== NEW v5.9.0: ACTION ITEMS DASHBOARD =====
        st.markdown("### ⚡ Action Items Dashboard")
        
        # Sort action items by priority
        action_items.sort(key=lambda x: x["priority"])
        
        if action_items:
            st.caption(f"You have **{len(action_items)} action item(s)** requiring attention")
            
            for item in action_items:
                if item["type"] == "rebalance":
                    # Urgent rebalance needed
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); 
                                    border-left: 4px solid #ef4444; padding: 16px; border-radius: 8px; margin: 12px 0;">
                            <div style="font-weight: 700; color: #991b1b; font-size: 1.05rem; margin-bottom: 8px;">
                                {item['message']}
                            </div>
                            <div style="color: #7f1d1d; font-size: 0.9rem; margin-bottom: 8px;">
                                📊 {item['detail']}
                            </div>
                            <div style="color: #7f1d1d; font-size: 0.85rem; font-style: italic;">
                                → {item['action']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                elif item["type"] == "deployment":
                    # Deployment in progress
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                                    border-left: 4px solid #f59e0b; padding: 16px; border-radius: 8px; margin: 12px 0;">
                            <div style="font-weight: 700; color: #92400e; font-size: 1.05rem; margin-bottom: 8px;">
                                {item['message']}
                            </div>
                            <div style="color: #78350f; font-size: 0.9rem; margin-bottom: 8px;">
                                📋 {item['detail']}
                            </div>
                            <div style="color: #78350f; font-size: 0.85rem; font-style: italic;">
                                → {item['action']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            # All clear
            st.markdown("""
                <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                            border-left: 4px solid #10b981; padding: 16px; border-radius: 8px; margin: 12px 0;">
                    <div style="font-weight: 700; color: #065f46; font-size: 1.05rem; margin-bottom: 8px;">
                        ✅ ALL CLEAR - No actions required
                    </div>
                    <div style="color: #047857; font-size: 0.9rem;">
                        All portfolios are properly balanced and fully deployed. Great job! 🎉
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # ===== NEW v5.10.0: AGGREGATED PERFORMANCE CHART =====
        st.markdown("### 📈 Combined Portfolio Performance")
        st.caption("See all your portfolios' growth over time in one unified view")
        
        with st.expander("ℹ️ Understanding the Aggregated Chart", expanded=False):
            st.markdown("""
            **This chart shows:**
            - Total combined value of all portfolios over time
            - Each portfolio as a colored layer (stacked area chart)
            - Combined goal path overlay
            - Weighted benchmark comparison (if benchmarks set)
            
            **How to read it:**
            - **Y-axis:** Total portfolio value ($)
            - **X-axis:** Time
            - **Colored areas:** Each portfolio's contribution
            - **Dashed line:** Combined goal path
            - **Dotted line:** Weighted benchmark (if available)
            
            **Pro tip:** This shows your total net worth evolution!
            """)
        
        # Fetch historical data for all portfolios
        try:
            all_portfolio_data = {}
            earliest_date = None
            
            for p_name, p_data in profiles.items():
                p_assets = p_data.get("assets", {})
                p_tickers = list(p_assets.keys())
                
                if not p_tickers:
                    continue
                
                # Get start date
                p_start = datetime.strptime(p_data.get('start_date', str(date.today())), '%Y-%m-%d')
                if earliest_date is None or p_start < earliest_date:
                    earliest_date = p_start
                
                # Fetch historical data
                try:
                    p_raw = yf.download(p_tickers, start=p_data["start_date"], auto_adjust=True, progress=False)
                    
                    if p_raw.empty:
                        continue
                    
                    p_close = p_raw['Close']
                    if len(p_tickers) == 1:
                        p_close = pd.DataFrame(p_close, columns=p_tickers)
                    
                    # Calculate daily portfolio value
                    valid_tickers = [t for t in p_tickers if t in p_close.columns]
                    if valid_tickers:
                        daily_val = p_close[valid_tickers].apply(
                            lambda r: sum(r[t] * p_assets[t]["units"] for t in valid_tickers if t in r.index),
                            axis=1
                        )
                        
                        all_portfolio_data[p_name] = {
                            "values": daily_val,
                            "start_date": p_start,
                            "principal": p_data.get("principal", 0),
                            "goal_pct": p_data.get("yearly_goal_pct", 0)
                        }
                except:
                    continue
            
            if len(all_portfolio_data) > 0:
                # Align all portfolios to common date range
                # Use the earliest start date and today as the range
                date_range = pd.date_range(start=earliest_date, end=date.today(), freq='D')
                
                # Create aligned dataframe
                aligned_data = pd.DataFrame(index=date_range)
                
                for p_name, p_info in all_portfolio_data.items():
                    # Reindex to common range, forward fill for dates before portfolio started
                    aligned_series = p_info["values"].reindex(date_range)
                    # For dates before this portfolio started, use 0
                    start_date = p_info["start_date"]
                    aligned_series.loc[aligned_series.index < start_date] = 0
                    # Forward fill for missing data
                    aligned_series = aligned_series.fillna(method='ffill')
                    aligned_data[p_name] = aligned_series
                
                # Calculate total
                aligned_data['Total'] = aligned_data.sum(axis=1)
                
                # Create stacked area chart
                fig_agg = go.Figure()
                
                # Add each portfolio as a stacked area
                portfolio_names = [col for col in aligned_data.columns if col != 'Total']
                
                for p_name in portfolio_names:
                    fig_agg.add_trace(go.Scatter(
                        x=aligned_data.index,
                        y=aligned_data[p_name],
                        name=p_name,
                        mode='lines',
                        stackgroup='one',
                        fillcolor=None,  # Auto color
                        hovertemplate='<b>%{fullData.name}</b><br>' +
                                     'Date: %{x|%Y-%m-%d}<br>' +
                                     'Value: $%{y:,.0f}<br>' +
                                     '<extra></extra>'
                    ))
                
                # Calculate combined goal path
                total_principal = sum(p["principal"] for p in all_portfolio_data.values())
                weighted_goal = sum(
                    p["principal"] * p["goal_pct"] 
                    for p in all_portfolio_data.values()
                ) / total_principal if total_principal > 0 else 0
                
                # Goal path from earliest date
                days_from_start = (aligned_data.index - aligned_data.index[0]).days
                daily_rate = (weighted_goal / 100) / 365.25
                goal_path = total_principal * (1 + daily_rate) ** days_from_start
                
                fig_agg.add_trace(go.Scatter(
                    x=aligned_data.index,
                    y=goal_path,
                    name=f'Combined Goal ({weighted_goal:.1f}%/yr)',
                    mode='lines',
                    line=dict(color='#10b981', width=2, dash='dash'),
                    hovertemplate='<b>Goal Path</b><br>' +
                                 'Date: %{x|%Y-%m-%d}<br>' +
                                 'Target: $%{y:,.0f}<br>' +
                                 '<extra></extra>'
                ))
                
                fig_agg.update_layout(
                    hovermode='x unified',
                    plot_bgcolor='white',
                    height=550,
                    showlegend=True,
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='#f1f5f9',
                        title='Date',
                        title_font=dict(size=14, color='#64748b'),
                        tickfont=dict(size=11)
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='#f1f5f9',
                        title='Total Portfolio Value ($)',
                        title_font=dict(size=14, color='#64748b'),
                        tickfont=dict(size=11),
                        tickformat='$,.0f'
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.15,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=11),
                        bgcolor='rgba(255, 255, 255, 0.9)',
                        bordercolor='#e2e8f0',
                        borderwidth=1
                    ),
                    margin=dict(l=70, r=40, t=20, b=80)
                )
                
                st.plotly_chart(fig_agg, use_container_width=True)
                
                # Show summary stats
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                
                current_total = float(aligned_data['Total'].iloc[-1])
                start_total = total_principal
                total_return = ((current_total / start_total) - 1) * 100 if start_total > 0 else 0
                
                days_elapsed = (aligned_data.index[-1] - aligned_data.index[0]).days
                years_elapsed = max(days_elapsed / 365.25, 0.01)
                total_cagr = ((current_total / start_total) ** (1 / years_elapsed) - 1) * 100 if start_total > 0 else 0
                
                with col_stat1:
                    st.metric("Combined Value", f"${current_total:,.0f}")
                
                with col_stat2:
                    st.metric("Total Return", f"{total_return:+.1f}%")
                
                with col_stat3:
                    st.metric("Combined CAGR", f"{total_cagr:+.1f}%")
                
                with col_stat4:
                    goal_diff = total_cagr - weighted_goal
                    st.metric(
                        "vs Goal", 
                        f"{goal_diff:+.1f}%",
                        delta=f"{'Beating' if goal_diff >= 0 else 'Behind'} target",
                        delta_color="normal" if goal_diff >= 0 else "inverse"
                    )
                
            else:
                st.info("ℹ️ No portfolio data available for aggregated chart. Add assets and deploy capital to see your combined performance.")
        
        except Exception as e:
            st.warning(f"⚠️ Could not generate aggregated chart: {str(e)}")
        
        st.divider()
        
        # ===== NEW v5.9.0: PORTFOLIO COMPARISON TABLE =====
        st.markdown("### 📊 Portfolio Comparison Table")
        st.caption("Compare all portfolios at a glance with sortable metrics")
        
        # Data already calculated in aggregation section above
        # Sort comparison data by Value (descending)
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df = comparison_df.sort_values("Value", ascending=False)
        
        # Calculate totals
        total_row = {
            "Profile": "**TOTAL**",
            "Account": "",
            "Value_Display": f"**${comparison_df['Value'].sum():,.0f}**",
            "CAGR_Display": f"**{comparison_df['CAGR'].mean():+.1f}%**",
            "ROI_Display": f"**{comparison_df['ROI'].mean():+.1f}%**",
            "Goal": "",
            "Assets": f"**{comparison_df['Assets'].sum()}**",
            "Status": ""
        }
        
        # Create display dataframe
        display_data = comparison_df[[
            "Profile", "Account", "Value_Display", "CAGR_Display", 
            "ROI_Display", "Goal", "Assets", "Status"
        ]].copy()
        display_data.columns = ["Profile", "Account", "Value", "CAGR ℹ️", "ROI ℹ️", "Goal ℹ️", "Assets", "Status"]
        
        # Append total row
        display_data = pd.concat([display_data, pd.DataFrame([total_row])], ignore_index=True)
        
        # Display with column config
        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Profile": st.column_config.TextColumn("Profile", help="Portfolio name", width="medium"),
                "Account": st.column_config.TextColumn("Account", help="Bank and account type", width="medium"),
                "Value": st.column_config.TextColumn("Value", help="Current portfolio value", width="small"),
                "CAGR ℹ️": st.column_config.TextColumn("CAGR ℹ️", help="Compound Annual Growth Rate - annualized return", width="small"),
                "ROI ℹ️": st.column_config.TextColumn("ROI ℹ️", help="Total Return on Investment since inception", width="small"),
                "Goal ℹ️": st.column_config.TextColumn("Goal ℹ️", help="Target annual growth rate", width="small"),
                "Assets": st.column_config.TextColumn("Assets", help="Number of assets in portfolio", width="small"),
                "Status": st.column_config.TextColumn("Status", help="Current portfolio status", width="medium")
            }
        )
        
        st.divider()
        
        # ===== NEW v5.9.2: ASSET ALLOCATION PIE CHART =====
        st.markdown("### 🥧 Global Asset Allocation")
        st.caption("Your total exposure across all portfolios")
        
        # Data already calculated in aggregation section above
        if global_assets:
            # Calculate total value for percentages
            total_global_value = sum(a["value"] for a in global_assets.values())
            
            # Sort by value (descending)
            sorted_assets = sorted(global_assets.items(), key=lambda x: x[1]["value"], reverse=True)
            
            # Create pie chart data
            labels = []
            values = []
            hover_text = []
            
            for ticker, data in sorted_assets:
                pct = (data["value"] / total_global_value * 100) if total_global_value > 0 else 0
                labels.append(f"{ticker}")
                values.append(data["value"])
                
                portfolio_list = ", ".join(set(data["portfolios"]))
                hover_text.append(
                    f"<b>{ticker}</b> - {data['fund_name']}<br>" +
                    f"Value: ${data['value']:,.0f}<br>" +
                    f"Percentage: {pct:.1f}%<br>" +
                    f"Units: {data['units']:.2f}<br>" +
                    f"In: {portfolio_list}"
                )
            
            # Create pie chart
            fig_pie = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hovertemplate='%{hovertext}<extra></extra>',
                hovertext=hover_text,
                textposition='auto',
                textinfo='label+percent',
                marker=dict(
                    line=dict(color='white', width=2)
                )
            )])
            
            fig_pie.update_layout(
                showlegend=True,
                height=500,
                margin=dict(l=20, r=20, t=40, b=20),
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    font=dict(size=11)
                )
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Asset breakdown table
            with st.expander("📋 Detailed Asset Breakdown", expanded=False):
                breakdown_rows = []
                for ticker, data in sorted_assets:
                    pct = (data["value"] / total_global_value * 100) if total_global_value > 0 else 0
                    portfolio_count = len(set(data["portfolios"]))
                    
                    breakdown_rows.append({
                        "Asset": ticker,
                        "Fund Name": data["fund_name"],
                        "Value": f"${data['value']:,.0f}",
                        "% of Total": f"{pct:.1f}%",
                        "Units": f"{data['units']:.2f}",
                        "Portfolios": portfolio_count
                    })
                
                df_breakdown = pd.DataFrame(breakdown_rows)
                st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
                
                st.caption(f"💡 **Diversification:** You own {len(global_assets)} different assets across {len(profiles)} portfolios")
        else:
            st.info("ℹ️ No assets deployed yet. Start deploying capital to see your allocation breakdown.")
        
        st.divider()
        
        # ===== NEW v5.9.2: RECENT ACTIVITY FEED =====
        st.markdown("### 📰 Recent Activity")
        st.caption("Latest portfolio updates and events")
        
        # Collect all logs from all profiles
        all_activities = []
        for p_name, p_data in profiles.items():
            logs = p_data.get("rebalance_logs", [])
            for log in logs:
                try:
                    # Parse date from log
                    log_date_str = log.get("date", "")
                    log_event = log.get("event", "")
                    
                    # Parse datetime
                    log_datetime = datetime.strptime(log_date_str, "%Y-%m-%d %H:%M")
                    
                    all_activities.append({
                        "datetime": log_datetime,
                        "date_str": log_date_str,
                        "profile": p_name,
                        "event": log_event
                    })
                except:
                    continue
        
        # Sort by datetime (most recent first)
        all_activities.sort(key=lambda x: x["datetime"], reverse=True)
        
        # Filter to last 7 days
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_activities = [a for a in all_activities if a["datetime"] >= seven_days_ago]
        
        if recent_activities:
            # Show activities
            activity_count = st.selectbox(
                "Show last",
                [5, 10, 15, 20],
                index=1,
                key="activity_count"
            )
            
            for activity in recent_activities[:activity_count]:
                # Format datetime
                dt = activity["datetime"]
                now = datetime.now()
                
                if dt.date() == now.date():
                    time_str = f"Today, {dt.strftime('%I:%M %p')}"
                elif dt.date() == (now - timedelta(days=1)).date():
                    time_str = f"Yesterday, {dt.strftime('%I:%M %p')}"
                else:
                    time_str = dt.strftime("%b %d, %I:%M %p")
                
                # Determine icon based on event content
                event_lower = activity["event"].lower()
                if "rebalance" in event_lower:
                    icon = "⚖️"
                    color = "#3b82f6"
                elif "deploy" in event_lower:
                    icon = "🔥"
                    color = "#f59e0b"
                elif "created" in event_lower or "added" in event_lower:
                    icon = "✨"
                    color = "#10b981"
                elif "removed" in event_lower or "deleted" in event_lower:
                    icon = "🗑️"
                    color = "#ef4444"
                elif "updated" in event_lower or "edited" in event_lower:
                    icon = "✏️"
                    color = "#8b5cf6"
                else:
                    icon = "📝"
                    color = "#64748b"
                
                st.markdown(f"""
                    <div style="border-left: 3px solid {color}; padding: 12px 16px; margin: 8px 0; 
                                background: white; border-radius: 0 8px 8px 0; 
                                box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 1;">
                                <div style="font-size: 0.75rem; color: #64748b; margin-bottom: 4px;">
                                    {time_str}
                                </div>
                                <div style="font-weight: 600; color: #1e293b; margin-bottom: 4px;">
                                    {icon} {activity['profile']}
                                </div>
                                <div style="color: #475569; font-size: 0.9rem;">
                                    {activity['event']}
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            if len(recent_activities) > activity_count:
                st.caption(f"💡 {len(recent_activities) - activity_count} more activities in the last 7 days")
        else:
            st.info("ℹ️ No recent activity in the last 7 days")
        
        st.divider()
        
        # Portfolio Grid
        st.markdown("### 🔍 Portfolio Strategies")
        st.caption("Click any profile tile or 'Open' button to view detailed analytics and manage assets")
        
        cols = st.columns(2)
        for i, (name, p_data) in enumerate(profiles.items()):
            p_assets = p_data.get("assets", {})
            curr_v = float(sum(p_assets[t]["units"] * prices.get(t, 0) for t in p_assets))
            
            has_rebalanced = p_data.get("last_rebalanced") is not None
            recently_rebalanced = check_recently_rebalanced(p_data.get("last_rebalanced"))
            needs_rebal, drift_details = calculate_drift_status(p_data, prices)
            
            start_val = float(p_data.get('principal', 0))
            roi_pct = ((curr_v / start_val) - 1) * 100 if start_val > 0 else 0
            
            start_date = datetime.strptime(p_data.get('start_date', str(date.today())), '%Y-%m-%d')
            years_elapsed = max((date.today() - start_date.date()).days / 365.25, 0.01)
            cagr = ((curr_v / start_val) ** (1 / years_elapsed) - 1) * 100 if start_val > 0 and years_elapsed > 0 else 0
            
            p_flag = "🇺🇸" if p_data.get("currency") == "USD" else "🇨🇦"
            
            all_deployed = all(
                asset.get("allocated_pct", 0) >= 100.0 
                for asset in p_assets.values()
            ) if p_assets else False
            
            if recently_rebalanced:
                tile_class = "profile-tile-optimized"
                status_badge = '<span class="success-badge">✅ Balanced</span>'
            elif needs_rebal:
                tile_class = "profile-tile-warning"
                status_badge = '<span class="drift-badge">🚨 REBALANCE REQUIRED</span>'
            elif has_rebalanced:
                tile_class = "profile-tile-optimized"
                status_badge = '<span class="success-badge">✅ Balanced</span>'
            elif not all_deployed and len(p_assets) > 0:
                tile_class = "profile-tile"
                deployed_count = sum(1 for a in p_assets.values() if a.get("allocated_pct", 0) >= 100.0)
                status_badge = f'<span style="background: #f59e0b; color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">🔥 Deploying ({deployed_count}/{len(p_assets)})</span>'
            elif all_deployed:
                tile_class = "profile-tile-optimized"
                status_badge = '<span class="success-badge">✅ Deployed</span>'
            else:
                tile_class = "profile-tile"
                status_badge = '<span style="background: #94a3b8; color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">⚪ New</span>'
            
            with cols[i % 2]:
                # v5.8.2: Clickable profile tile - entire tile navigates to profile view
                with st.container():
                    # Tile content with integrated navigation
                    st.markdown(f"""
                        <div class="{tile_class}" style="padding: 24px; margin-top: 0px; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;">
                            <div class="profile-tile-header">
                                {p_flag} {name}
                            </div>
                            <div style="margin-bottom: 16px; text-align: center;">
                                {status_badge}
                            </div>
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
                                    <div style="font-weight: 700; color: {'#10b981' if cagr >= 0 else '#ef4444'};">
                                        {cagr:+.1f}%
                                    </div>
                                </div>
                                <div style="text-align: right;">
                                    <div style="font-size: 0.75rem; opacity: 0.8;">ROI</div>
                                    <div style="font-weight: 700; color: {'#10b981' if roi_pct >= 0 else '#ef4444'};">
                                        {roi_pct:+.1f}%
                                    </div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # v5.8.3 FIX: Changed to 'secondary' to avoid red confusion
                    if st.button(
                        "📂 Click to Open →",
                        key=f"open_{name}",
                        use_container_width=True,
                        type="secondary",
                        help=f"Open {name} portfolio manager"
                    ):
                        st.session_state.active_profile = name
                        st.rerun()
                
                
                if needs_rebal and drift_details:
                    with st.expander("⚠️ View Drift Details", expanded=False):
                        for t, drift, actual, target in drift_details:
                            st.caption(f"• {t}: {drift:.1f}% drift")
                
                st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

else:  # Portfolio Manager
    if not st.session_state.active_profile:
        st.title("📊 Portfolio Manager")
        
        st.markdown("""
            <div class="neutral-state">
                <h2>👋 Welcome to Portfolio Manager</h2>
                <p style="font-size: 1.2rem; margin-bottom: 30px;">Select a profile from the sidebar to view detailed analytics</p>
                <p style="opacity: 0.9;">or</p>
                <p style="font-size: 1.1rem; margin-top: 20px;">Create a new profile to get started →</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        profiles = st.session_state.db.get("profiles", {})
        if profiles:
            st.markdown("### 📁 Available Profiles")
            
            for name in profiles.keys():
                if st.button(f"📂 {name}", key=f"select_{name}", use_container_width=True):
                    st.session_state.active_profile = name
                    st.rerun()
        else:
            st.info("ℹ️ No profiles yet. Create your first profile using the sidebar!")
        
        st.stop()
    
    if st.session_state.active_profile not in st.session_state.db["profiles"]:
        st.error("⚠️ Selected profile no longer exists. Please select another.")
        st.session_state.active_profile = None
        st.rerun()
    
    prof = st.session_state.db["profiles"][st.session_state.active_profile]
    p_flag = "🇺🇸" if prof.get("currency") == "USD" else "🇨🇦"
    
    st.title(f"{p_flag} {st.session_state.active_profile}")
    st.caption(f"Portfolio Manager • Inception: {prof.get('start_date', 'N/A')} • Drift Tolerance: {prof.get('drift_tolerance', 5.0)}%")
    
    # Deployment status banner
    if not prof.get("asset_mix_locked", False):
        st.warning("⚠️ **Asset mix not locked** - Define and lock assets first")
    else:
        assets = prof.get("assets", {})
        all_deployed = all(a.get("allocated_pct", 0) >= 100.0 for a in assets.values())
        
        if assets and not all_deployed:
            partial = [(t, a.get("allocated_pct", 0)) for t, a in assets.items() 
                       if a.get("allocated_pct", 0) < 100.0]
            st.info(f"📊 **Deployment in progress** - {len(partial)} asset(s) not fully deployed")
            with st.expander("View deployment status"):
                for ticker, pct in partial:
                    st.caption(f"• {ticker}: {pct:.1f}% deployed")
        elif assets and all_deployed:
            st.success("✅ **All assets deployed** - Portfolio drift monitoring active")
    
    # Portfolio Summary
    has_rebalanced = prof.get("last_rebalanced") is not None
    recently_rebalanced = check_recently_rebalanced(prof.get("last_rebalanced"))
    
    col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
    with col_sum1:
        asset_count = len(prof.get("assets", {}))
        st.metric("Total Assets", asset_count)
    with col_sum2:
        prof_start = datetime.strptime(prof.get('start_date', str(date.today())), '%Y-%m-%d')
        age_years = max((date.today() - prof_start.date()).days / 365.25, 0.01)
        st.metric("Portfolio Age", f"{age_years:.1f} years")
    with col_sum3:
        if prof.get("last_rebalanced"):
            st.metric("Last Rebalanced", prof["last_rebalanced"][:10])
        else:
            st.metric("Last Rebalanced", "Never")
    with col_sum4:
        if not prof.get("asset_mix_locked", False):
            st.metric("Status", "⚙️ Setup", delta="Lock assets", delta_color="off")
        else:
            assets = prof.get("assets", {})
            if assets:
                deployed_count = sum(1 for a in assets.values() if a.get("allocated_pct", 0) >= 100.0)
                total_count = len(assets)
                
                if deployed_count < total_count:
                    st.metric("Deployment", f"{deployed_count}/{total_count}", delta="In Progress", delta_color="off")
                elif has_rebalanced:
                    if recently_rebalanced:
                        st.metric("Status", "✅ Balanced", delta="Optimized", delta_color="normal")
                    else:
                        st.metric("Status", "Active", delta="Monitoring", delta_color="off")
                else:
                    st.metric("Status", "✅ Deployed", delta="Ready to Monitor", delta_color="normal")
            else:
                st.metric("Status", "⚙️ Setup", delta="Add assets", delta_color="off")
    
    st.divider()
    
    asset_dict = prof.get("assets", {})
    tickers = list(asset_dict.keys())
    
    if not tickers:
        st.info("👈 **Add your first asset using the sidebar** to start building your portfolio")
        
        st.markdown("---")
        st.markdown("### 🚀 Quick Start Guide: Building Your Investment Strategy")
        
        st.markdown("""
        Follow these numbered steps matching the sidebar workflow:
        """)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 12px; margin: 15px 0;">
            <h4 style="margin-top: 0; color: white;">① Strategy Setup</h4>
            <p style="margin-bottom: 0;">
                Create your profile with bank/broker, account type, principal, and inception date.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    color: white; padding: 20px; border-radius: 12px; margin: 15px 0;">
            <h4 style="margin-top: 0; color: white;">② Drift Strategy</h4>
            <p style="margin-bottom: 0;">
                Set your drift tolerance % to control when rebalance alerts trigger.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    color: white; padding: 20px; border-radius: 12px; margin: 15px 0;">
            <h4 style="margin-top: 0; color: white;">③ Benchmark Comparison</h4>
            <p style="margin-bottom: 0;">
                Select a market index (SPY, QQQ, etc.) to compare your performance.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                    color: white; padding: 20px; border-radius: 12px; margin: 15px 0;">
            <h4 style="margin-top: 0; color: white;">④ Asset Allocation</h4>
            <p style="margin-bottom: 0;">
                Add tickers and set target allocation % for each asset (total must = 100%).
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); 
                    color: white; padding: 20px; border-radius: 12px; margin: 15px 0;">
            <h4 style="margin-top: 0; color: white;">⑤ Lock Asset Mix</h4>
            <p style="margin-bottom: 0;">
                Once assets total 100%, lock the mix to finalize and enable deployment.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                    color: white; padding: 20px; border-radius: 12px; margin: 15px 0;">
            <h4 style="margin-top: 0; color: white;">⑥ Asset Deployment</h4>
            <p style="margin-bottom: 0;">
                Record your capital deployments for each asset until all reach 100%.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        ### 💡 Pro Tips
        - **Follow the numbers:** Complete steps ①→⑥ in order for smooth workflow
        - **Diversify:** Spread investments across different asset classes
        - **Deploy Gradually:** Use multiple deployment events to dollar-cost average
        - **Track History:** All deployments and rebalances are logged
        - **Stay Disciplined:** Rebalance when drift exceeds tolerance
        """)
        
        st.markdown("---")
        st.success("👈 **Ready to start?** Add your first asset in the sidebar!")
        
        st.stop()
    
    # Fetch data and analyze
    with st.spinner("📊 Analyzing portfolio..."):
        try:
            raw = yf.download(tickers, start=prof["start_date"], auto_adjust=True, progress=False)
            
            if raw.empty:
                st.error("❌ Could not fetch historical data. Please check your tickers and date range.")
                st.stop()
            
            data = raw['Close']
            if len(tickers) == 1:
                data = pd.DataFrame(data, columns=tickers)
            
            v_t = [t for t in tickers if t in data.columns]
            
            if not v_t:
                st.error("❌ No valid ticker data found. Please check your asset symbols.")
                st.stop()
            
            if len(v_t) < len(tickers):
                missing = set(tickers) - set(v_t)
                st.warning(f"⚠️ Could not load data for: {', '.join(missing)}")
            
            # Calculate portfolio metrics
            daily_val = data[v_t].apply(
                lambda r: sum(r[t] * asset_dict[t]["units"] for t in v_t if t in r.index),
                axis=1
            )
            
            curr_v = float(daily_val.iloc[-1])
            start_val = float(prof['principal'])
            
            if curr_v <= 0:
                st.warning("⚠️ **Portfolio value is zero**")
                st.info("""
                    Your portfolio shows zero value. This can happen if:
                    - You haven't entered any units for your assets yet
                    - Asset deployment is not complete
                    
                    **Next steps:**
                    1. Go to **💰 Asset Deployment** section
                    2. Record your capital deployments for each asset
                    3. The system will automatically calculate units based on purchase prices
                """)
                st.stop()
            
            years = max((data.index[-1] - data.index[0]).days / 365.25, 0.01)
            target_val = start_val * (1 + (float(prof['yearly_goal_pct'])/100))**years
            
            perc_diff = ((curr_v / target_val) - 1) * 100 if target_val > 0 else 0
            roi_pct = ((curr_v / start_val) - 1) * 100 if start_val > 0 else 0
            
            prof_start_date = datetime.strptime(prof.get('start_date', str(date.today())), '%Y-%m-%d')
            prof_years = max((date.today() - prof_start_date.date()).days / 365.25, 0.01)
            profile_cagr = ((curr_v / start_val) ** (1 / prof_years) - 1) * 100 if start_val > 0 else 0
            
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
            
            # Drift alert banner
            if needs_rebalance:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); 
                                border: 4px solid #ef4444; border-radius: 16px; padding: 28px; 
                                margin-bottom: 28px;">
                        <h2 style="color: #991b1b; margin: 0 0 16px 0; font-size: 1.8rem;">
                            🚨 DRIFT ALERT: Immediate Rebalancing Required
                        </h2>
                        <p style="color: #7f1d1d; font-size: 1.2rem; margin: 0; line-height: 1.6;">
                            <strong>{len(drift_assets)} asset(s)</strong> have exceeded your <strong>{prof.get('drift_tolerance', 5.0)}% drift tolerance</strong>.<br>
                            Your portfolio allocation has shifted significantly. Review the analysis below and execute rebalancing.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
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
            
            # Determine status badge
            has_rebalanced = prof.get("last_rebalanced") is not None
            has_assets = len(asset_dict) > 0
            
            if recently_rebalanced:
                alert_html = '<span class="success-badge">✅ Balanced</span>'
            elif needs_rebalance:
                alert_html = '<span class="drift-badge">🚨 REBALANCE REQUIRED</span>'
            elif has_rebalanced:
                alert_html = '<span class="success-badge">✅ Balanced</span>'
            elif has_assets:
                alert_html = '<span style="background: #3b82f6; color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">📊 Monitoring</span>'
            else:
                alert_html = '<span style="background: #94a3b8; color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">⚪ New</span>'
            
            # Header
            st.markdown(f"""
                <div class="premium-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                        <h2 style="margin:0;">Portfolio Analytics</h2>
                        {alert_html}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Key Metrics
            col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
            
            with col_s1:
                st.markdown(f"""
                    <div class="stat-item">
                        <div class="stat-label">Current Value</div>
                        <div class="stat-value">${curr_v:,.0f}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_s2:
                st.markdown(f"""
                    <div class="stat-item">
                        <div class="stat-label">Total ROI</div>
                        <div class="stat-value" style="color: {'#10b981' if roi_pct >= 0 else '#ef4444'};">
                            {roi_pct:+.2f}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_s3:
                st.markdown(f"""
                    <div class="stat-item">
                        <div class="stat-label">CAGR</div>
                        <div class="stat-value" style="color: {'#10b981' if profile_cagr >= 0 else '#ef4444'};">
                            {profile_cagr:+.2f}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_s4:
                st.markdown(f"""
                    <div class="stat-item">
                        <div class="stat-label">vs Target Path</div>
                        <div class="stat-value" style="color: {'#10b981' if perc_diff >= 0 else '#ef4444'};">
                            {perc_diff:+.2f}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_s5:
                annualized = ((curr_v / start_val) ** (1/years) - 1) * 100
                st.markdown(f"""
                    <div class="stat-item">
                        <div class="stat-label">Annualized Return</div>
                        <div class="stat-value" style="color: {'#10b981' if annualized >= 0 else '#ef4444'};">
                            {annualized:.2f}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Performance Chart
            st.markdown("### 📈 Performance vs Goal Path")
            benchmark_caption = f" & 100% {prof.get('benchmark', '')}" if prof.get('benchmark') else ""
            st.caption(f"Track your portfolio's actual performance against your target growth trajectory{benchmark_caption}")
            
            fig = go.Figure()
            
            # Benchmark comparison
            benchmark_ticker = prof.get('benchmark')
            benchmark_comparison_msg = None
            
            if benchmark_ticker:
                try:
                    benchmark_raw = yf.download(benchmark_ticker, start=prof["start_date"], auto_adjust=True, progress=False)
                    if not benchmark_raw.empty:
                        benchmark_data = benchmark_raw['Close']
                        
                        if isinstance(benchmark_data, pd.DataFrame):
                            benchmark_data = benchmark_data.squeeze()
                        
                        benchmark_data = benchmark_data.dropna()
                        
                        if len(benchmark_data) == 0:
                            st.warning(f"⚠️ No valid benchmark data for {benchmark_ticker}")
                        else:
                            first_price = float(benchmark_data.iloc[0])
                            last_price = float(benchmark_data.iloc[-1])
                            benchmark_normalized = (benchmark_data / first_price) * start_val
                            bench_return = ((last_price / first_price) - 1) * 100
                            bench_final_value = float(benchmark_normalized.iloc[-1])
                            
                            bench_dates = benchmark_normalized.index.tolist()
                            bench_values = benchmark_normalized.values.tolist()
                            
                            fig.add_trace(go.Scatter(
                                x=bench_dates,
                                y=bench_values,
                                name=f'100% {benchmark_ticker} Benchmark ({bench_return:+.1f}%)',
                                line=dict(
                                    color='#ef4444',
                                    width=3,
                                    dash='dot'
                                ),
                                mode='lines',
                                visible=True,
                                showlegend=True,
                                hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br>' +
                                             '<b>Benchmark Value:</b> $%{y:,.0f}<br>' +
                                             f'<b>Ticker:</b> {benchmark_ticker}<br>' +
                                             f'<b>Return:</b> {bench_return:+.1f}%<br>' +
                                             '<extra></extra>'
                            ))
                            
                            portfolio_vs_bench = curr_v - bench_final_value
                            if portfolio_vs_bench > 0:
                                benchmark_comparison_msg = ("success", f"📊 Your portfolio outperformed {benchmark_ticker} by ${portfolio_vs_bench:,.0f} ({((curr_v/bench_final_value - 1)*100):+.1f}%)" if bench_final_value > 0 else f"📊 Your portfolio: ${curr_v:,.0f}")
                            else:
                                benchmark_comparison_msg = ("info", f"📊 {benchmark_ticker} outperformed your portfolio by ${abs(portfolio_vs_bench):,.0f} ({((bench_final_value/curr_v - 1)*100):+.1f}%)" if curr_v > 0 else f"📊 Benchmark: ${bench_final_value:,.0f}")
                    else:
                        st.warning(f"⚠️ No benchmark data available for {benchmark_ticker}")
                except Exception as e:
                    st.error(f"⚠️ Benchmark error: {str(e)}")
            
            # Actual portfolio
            fig.add_trace(go.Scatter(
                x=data.index,
                y=daily_val,
                name='Actual Portfolio',
                line=dict(color='#3b82f6', width=3),
                hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br>' +
                             '<b>Portfolio Value:</b> $%{y:,.2f}<br>' +
                             '<b>Performance:</b> Actual<br>' +
                             '<extra></extra>'
            ))
            
            # Goal path
            days = np.arange(len(data.index))
            daily_rate = (float(prof['yearly_goal_pct']) / 100) / 365.25
            target_path = start_val * (1 + daily_rate) ** days
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=target_path,
                name=f'Goal Path ({prof["yearly_goal_pct"]}%/yr)',
                line=dict(color='#10b981', width=2, dash='dash'),
                hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br>' +
                             '<b>Target Value:</b> $%{y:,.2f}<br>' +
                             f'<b>Goal Rate:</b> {prof["yearly_goal_pct"]}% annually<br>' +
                             '<extra></extra>'
            ))
            
            fig.update_layout(
                hovermode='x unified',
                plot_bgcolor='white',
                height=550,
                showlegend=True,
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=14,
                    font_family="Inter, sans-serif",
                    bordercolor="#e2e8f0"
                ),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#f1f5f9',
                    title='Date',
                    title_font=dict(size=14, color='#64748b'),
                    tickfont=dict(size=11)
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#f1f5f9',
                    title='Portfolio Value ($)',
                    title_font=dict(size=14, color='#64748b'),
                    tickfont=dict(size=11),
                    tickformat='$,.0f'
                ),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=12),
                    bgcolor='rgba(255, 255, 255, 0.9)',
                    bordercolor='#e2e8f0',
                    borderwidth=1
                ),
                margin=dict(l=70, r=40, t=20, b=80)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("📊 Understanding This Chart", expanded=False):
                st.markdown("""
                **What the lines represent:**
                
                🔴 **Benchmark (Red dotted line)** *(if selected)*  
                Shows what would happen if you invested 100% in the market index at profile start.
                
                🔵 **Actual Portfolio (Blue solid line)**  
                Your portfolio's real performance based on actual asset prices and your holdings.
                
                🟢 **Goal Path (Green dashed line)**  
                Your target growth trajectory based on your yearly goal percentage.
                
                **Tips:**
                - Click any legend item to show/hide that line
                - Hover over the chart to see exact values at any date
                - Use the toolbar to zoom, pan, or save the chart
                """)
            
            if benchmark_comparison_msg:
                msg_type, msg_text = benchmark_comparison_msg
                if msg_type == "success":
                    st.success(msg_text)
                else:
                    st.info(msg_text)
            
            st.divider()
            
            # Rebalance Analysis
            st.markdown("### ⚖️ Rebalance Analysis")
            st.caption("Review asset allocation drift and required trades to restore target percentages")
            with st.expander("ℹ️ Understanding the rebalance table", expanded=False):
                st.markdown("""
                **This table shows what trades are needed** to restore your target allocation.
                
                - **Target %**: Your desired allocation for this asset
                - **Allocated %**: How much of this asset's target has been deployed
                - **Actual %**: Current portfolio percentage based on market values
                - **Drift**: Difference between Actual % and Target %
                    - 🔴 Red = exceeds tolerance (action needed)
                    - 🟡 Yellow = warning (close to tolerance)
                    - 🟢 Green = within tolerance (good)
                - **Status**: Deployment or drift monitoring state
                
                💡 Use the two-step workflow below to rebalance with real broker prices
                """)
            
            # v5.8.1: Column config with ℹ️ info icons
            column_config = {
                "Fund Name": st.column_config.TextColumn(
                    "Fund Name ℹ️",
                    help="Full name of the investment fund or security",
                    width="large"
                ),
                "Ticker": st.column_config.TextColumn(
                    "Ticker ℹ️",
                    help="Stock ticker symbol",
                    width="small"
                ),
                "Target %": st.column_config.TextColumn(
                    "Target % ℹ️",
                    help="Your desired allocation percentage for this asset",
                    width="small"
                ),
                "Allocated %": st.column_config.TextColumn(
                    "Allocated % ℹ️",
                    help="Percentage of target that has been deployed (100% = fully deployed)",
                    width="small"
                ),
                "Actual %": st.column_config.TextColumn(
                    "Actual % ℹ️",
                    help="Current portfolio percentage based on market values",
                    width="small"
                ),
                "Drift": st.column_config.TextColumn(
                    "Drift ℹ️",
                    help="Difference between Actual % and Target % (🔴 = exceeds tolerance)",
                    width="small"
                ),
                "Status": st.column_config.TextColumn(
                    "Status ℹ️",
                    help="Deployment status or drift monitoring state",
                    width="medium"
                ),
                "Avg Cost": st.column_config.TextColumn(
                    "Avg Cost ℹ️",
                    help="Weighted average cost per unit (available when 100% deployed)",
                    width="small"
                ),
                "Units": st.column_config.TextColumn(
                    "Units ℹ️",
                    help="Total shares/units owned",
                    width="small"
                ),
                "Current Price": st.column_config.TextColumn(
                    "Current Price ℹ️",
                    help="Latest market price per unit",
                    width="small"
                ),
                "%Daily Change": st.column_config.TextColumn(
                    "%Daily Change ℹ️",
                    help="Price change from previous trading day",
                    width="small"
                ),
                "Amount": st.column_config.TextColumn(
                    "Amount ℹ️",
                    help="Current market value (Units × Current Price)",
                    width="medium"
                ),
                "Buy/Sell Amt": st.column_config.TextColumn(
                    "Buy/Sell Amt ℹ️",
                    help="Dollar amount to trade for rebalancing",
                    width="medium"
                ),
                "Buy/Sell Shares": st.column_config.TextColumn(
                    "Buy/Sell Shares ℹ️",
                    help="Number of shares to buy (+) or sell (-)",
                    width="small"
                )
            }
            
            rows = []
            total_turnover = 0
            total_current_val = 0
            
            for t in v_t:
                current_price = float(data[t].iloc[-1])
                try:
                    prev_price = float(data[t].iloc[-2])
                    daily_change_pct = ((current_price / prev_price) - 1) * 100
                except:
                    daily_change_pct = 0.0
                
                fund_name = asset_dict[t].get("fund_name", t)
                if fund_name == t:
                    try:
                        ticker_obj = yf.Ticker(t)
                        info = ticker_obj.info
                        if info and 'longName' in info:
                            fund_name = info.get('longName', t)
                    except:
                        pass
                
                cur_u = float(asset_dict[t]["units"])
                tar_w = float(asset_dict[t]['target'])
                allocated_pct = asset_dict[t].get("allocated_pct", 0)
                
                avg_cost = calculate_average_cost(asset_dict[t])
                avg_cost_display = f"${avg_cost:.2f}" if avg_cost is not None else "Pending"
                
                act_val = cur_u * current_price
                act_w = (act_val / curr_v * 100) if curr_v > 0 else 0
                drift = act_w - tar_w
                
                tar_val = (tar_w / 100) * curr_v
                tar_u = tar_val / current_price if current_price > 0 else 0
                
                val_diff = tar_val - act_val
                unit_diff = tar_u - cur_u
                
                total_turnover += abs(val_diff)
                total_current_val += act_val
                
                if allocated_pct < 100.0:
                    drift_display = "—"
                    status_display = f"⏳ Deploying ({allocated_pct:.0f}%)"
                else:
                    drift_display = f"{drift:+.2f}%"
                    if abs(drift) >= prof.get("drift_tolerance", 5.0):
                        drift_display = f"🔴 {drift:+.2f}%"
                    elif abs(drift) > 0.5:
                        drift_display = f"🟡 {drift:+.2f}%"
                    else:
                        drift_display = f"🟢 {drift:+.2f}%"
                    status_display = "✅ Deployed"
                
                daily_change_display = f"{daily_change_pct:+.2f}%"
                
                rows.append({
                    "Fund Name": fund_name,
                    "Ticker": t,
                    "Target %": f"{tar_w:.2f}%",
                    "Allocated %": f"{allocated_pct:.1f}%",
                    "Actual %": f"{act_w:.2f}%",
                    "Drift": drift_display,
                    "Status": status_display,
                    "Avg Cost": avg_cost_display,
                    "Units": f"{cur_u:.0f}",
                    "Current Price": f"${current_price:.2f}",
                    "%Daily Change": daily_change_display,
                    "Amount": f"${act_val:,.0f}",
                    "Buy/Sell Amt": f"${abs(val_diff):,.0f}",
                    "Buy/Sell Shares": f"{unit_diff:+.0f}"
                })
            
            rows.append({
                "Fund Name": "**TOTAL**",
                "Ticker": "",
                "Target %": "**100.00%**",
                "Allocated %": "",
                "Actual %": "**100.00%**",
                "Drift": "—",
                "Status": "",
                "Avg Cost": "",
                "Units": "",
                "Current Price": "",
                "%Daily Change": "",
                "Amount": f"**${total_current_val:,.0f}**",
                "Buy/Sell Amt": f"**${total_turnover:,.0f}**",
                "Buy/Sell Shares": "—"
            })
            
            df_rebalance = pd.DataFrame(rows)
            
            st.dataframe(
                df_rebalance, 
                use_container_width=True, 
                hide_index=True,
                column_config=column_config
            )
            
            all_deployed = all(a.get("allocated_pct", 0) >= 100.0 for a in asset_dict.values())
            if not all_deployed:
                st.info("ℹ️ **Portfolio-level drift monitoring** activates when all assets reach 100% deployment")
            
            col_metric1, col_metric2 = st.columns(2)
            with col_metric1:
                st.metric("CAGR", f"{profile_cagr:.2f}%", help="Compound Annual Growth Rate")
            with col_metric2:
                st.metric("Total Trade Volume", f"${total_turnover:,.0f}", help="Total dollar amount needed to rebalance")
            
            st.divider()
            
            # v5.7 NEW: Two-Step Rebalance Workflow
            st.markdown("### 🚀 Two-Step Rebalance Workflow")
            st.caption("Professional slippage management: Get recommendations, execute at broker, then enter actual prices")
            
            with st.expander("ℹ️ How the two-step workflow works", expanded=False):
                st.markdown("""
                **Why two steps?**
                
                Market prices change constantly. The prices shown above are **estimates** from the app.  
                Your **actual broker fills** may differ due to slippage, spreads, and market movement.
                
                **The Workflow:**
                
                1. **📋 Recommend Rebalance**: View suggested trades at current market prices
                2. **🏦 Execute at Broker**: Go to your broker and execute the trades manually
                3. **✅ Enter Actual Prices**: Return here and enter the **exact prices you received**
                4. **💾 Commit**: App updates your portfolio with real-world data (not estimates)
                
                **Benefits:**
                - Accurate portfolio tracking with actual fill prices
                - No errors from market slippage
                - Professional-grade record keeping
                - Realistic performance metrics
                """)
            
            col_exec1, col_exec2 = st.columns(2)
            
            with col_exec1:
                st.markdown("#### 📋 Phase A: Get Recommendation")
                st.caption("View suggested trades based on current market prices")
                
                if needs_rebalance:
                    st.warning("⚠️ **Rebalancing recommended**")
                
                # v5.7 NEW: Recommend button
                if st.button("📋 Recommend Rebalance", 
                            type="primary" if needs_rebalance else "secondary", 
                            use_container_width=True, 
                            disabled=not needs_rebalance,
                            key="recommend_rebalance"):
                    # Calculate recommendations
                    recommendations = []
                    for t in v_t:
                        old_units = float(asset_dict[t]["units"])
                        new_units = float((asset_dict[t]["target"] / 100 * curr_v) / data[t].iloc[-1])
                        
                        change_units = new_units - old_units
                        if abs(change_units) > 0.0001:
                            action = "BUY" if change_units > 0 else "SELL"
                            current_price = float(data[t].iloc[-1])
                            
                            recommendations.append({
                                "ticker": t,
                                "action": action,
                                "shares": abs(change_units),
                                "estimated_price": current_price,
                                "estimated_value": abs(change_units) * current_price
                            })
                    
                    store_rebalance_recommendation(prof, recommendations)
                    save_db(st.session_state.db)
                    st.session_state.show_rebalance_recommendation = True
                    st.rerun()
                
                if not needs_rebalance:
                    st.info("✓ Portfolio is optimally balanced")
            
            with col_exec2:
                st.markdown("#### ✅ Phase C: Execute with Actuals")
                st.caption("After trading, enter your actual fill prices")
                
                has_recommendation = "pending_rebalance" in prof
                
                # v5.7 NEW: Execute button
                if st.button("✅ Execute Rebalance Now", 
                            type="primary", 
                            use_container_width=True,
                            disabled=not has_recommendation,
                            key="execute_rebalance"):
                    st.session_state.show_execute_form = True
                    st.rerun()
                
                if not has_recommendation:
                    st.info("📋 Generate recommendation first")
                else:
                    rec_time = prof["pending_rebalance"]["timestamp"]
                    st.caption(f"📌 Recommendation from: {rec_time}")
            
            # v5.7 NEW: Show recommendation
            if st.session_state.get("show_rebalance_recommendation", False) and "pending_rebalance" in prof:
                st.markdown("---")
                st.markdown("""
                    <div class="recommendation-box">
                        <h3>📋 Rebalance Recommendation</h3>
                        <p style="color: #78350f; margin-bottom: 16px;">
                            <strong>IMPORTANT:</strong> These are <u>estimated prices</u> from the market.  
                            Your actual broker fills may differ. Execute these trades at your broker, then return here to enter the <strong>actual prices you received</strong>.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                recommendations = prof["pending_rebalance"]["recommendations"]
                
                if recommendations:
                    st.markdown("**Recommended Trades:**")
                    
                    for rec in recommendations:
                        action_color = "🟢" if rec["action"] == "BUY" else "🔴"
                        st.markdown(f"""
                        **{action_color} {rec['action']} {rec['ticker']}**  
                        • Shares: {rec['shares']:.4f}  
                        • Est. Price: ${rec['estimated_price']:.2f}  
                        • Est. Value: ${rec['estimated_value']:,.2f}
                        """)
                    
                    st.markdown("---")
                    st.markdown("""
                    **🏦 Phase B: Next Steps**
                    
                    1. Go to your broker (Fidelity, IBKR, etc.)
                    2. Execute the trades listed above
                    3. Note the **actual prices** you received for each trade
                    4. Return here and click **"✅ Execute Rebalance Now"**
                    5. Enter your actual prices in the form
                    """)
                else:
                    st.info("No trades needed - portfolio already balanced")
                    clear_rebalance_recommendation(prof)
                    save_db(st.session_state.db)
                    st.session_state.show_rebalance_recommendation = False
            
            # v5.7 NEW: Actual price entry form
            if st.session_state.get("show_execute_form", False) and "pending_rebalance" in prof:
                st.markdown("---")
                st.markdown("### 💰 Enter Actual Broker Prices")
                st.caption("Enter the exact prices you received when executing the trades at your broker")
                
                recommendations = prof["pending_rebalance"]["recommendations"]
                
                with st.form("actual_prices_form"):
                    st.markdown("**For each trade, enter the actual price you received:**")
                    
                    actual_prices = {}
                    
                    for rec in recommendations:
                        st.markdown(f"**{rec['action']} {rec['ticker']}** ({rec['shares']:.4f} shares)")
                        st.caption(f"Estimated price was: ${rec['estimated_price']:.2f}")
                        
                        actual_price = st.number_input(
                            f"Actual price received for {rec['ticker']}",
                            min_value=0.01,
                            value=float(rec['estimated_price']),
                            step=0.01,
                            format="%.2f",
                            key=f"actual_price_{rec['ticker']}",
                            help="Enter the exact fill price from your broker confirmation"
                        )
                        
                        actual_prices[rec['ticker']] = actual_price
                        
                        # Show slippage
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
                        # v5.7 NEW: Update portfolio with actual prices
                        detail_log = f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - "
                        changes = []
                        
                        for rec in recommendations:
                            ticker = rec['ticker']
                            actual_price = actual_prices[ticker]
                            
                            if rec['action'] == "BUY":
                                # Add shares
                                asset_dict[ticker]["units"] = float(asset_dict[ticker]["units"]) + rec['shares']
                                changes.append(f"🟢 {ticker} BUY {rec['shares']:.4f} @ ${actual_price:.2f}")
                            else:
                                # Remove shares
                                asset_dict[ticker]["units"] = float(asset_dict[ticker]["units"]) - rec['shares']
                                changes.append(f"🔴 {ticker} SELL {rec['shares']:.4f} @ ${actual_price:.2f}")
                        
                        detail_log += ", ".join(changes) if changes else "No changes needed"
                        
                        prof.setdefault("rebalance_stats", []).insert(0, detail_log)
                        prof["rebalance_stats"] = prof["rebalance_stats"][:50]
                        prof["last_rebalanced"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        clear_rebalance_recommendation(prof)
                        log_profile(prof, "Portfolio rebalanced with actual broker prices - Status: Balanced")
                        save_db(st.session_state.db)
                        
                        st.session_state.show_execute_form = False
                        st.session_state.show_rebalance_recommendation = False
                        
                        st.success("✅ Portfolio rebalanced successfully with actual broker prices! Status: **Balanced** ✅")
                        st.balloons()
                        st.rerun()
                    
                    if cancelled:
                        st.session_state.show_execute_form = False
                        st.rerun()
        
        except Exception as e:
            st.error(f"❌ Error analyzing portfolio: {str(e)}")
            st.info("💡 Please check your internet connection and verify all ticker symbols are valid.")
    
    # Rebalance History
    if tickers and st.session_state.active_profile:
        prof = st.session_state.db["profiles"][st.session_state.active_profile]
        rebalance_events = prof.get('rebalance_stats', [])
        
        if rebalance_events:
            st.divider()
            st.markdown("## 📜 Rebalance History")
            st.caption("Complete history of all rebalancing events with actual broker prices")
            
            with st.expander("ℹ️ How to read rebalance history", expanded=False):
                st.markdown("""
                **Each entry shows the trades executed** during that rebalance.
                
                - 🟢 **BUY**: Shares purchased with actual broker price
                - 🔴 **SELL**: Shares sold with actual broker price
                - **Format**: `Date - 🟢 AAPL BUY 5.2345 @ $150.25, 🔴 MSFT SELL 3.1234 @ $380.50`
                
                All prices shown are the **actual fill prices** received from your broker, not estimates.
                """)
            
            col_filter1, col_filter2 = st.columns([3, 1])
            with col_filter1:
                time_filter = st.selectbox(
                    "Group by",
                    ["All Events", "Last 30 Days", "Last 90 Days", "This Year", "By Quarter", "By Month"],
                    key="history_filter"
                )
            with col_filter2:
                events_per_page = st.selectbox("Show", [10, 25, 50, 100], index=0, key="events_per_page")
            
            filtered_events = []
            now = datetime.now()
            
            for event in rebalance_events:
                try:
                    event_date_str = event.split(" - ")[0].split(" ")[0]
                    event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
                    
                    if time_filter == "All Events":
                        filtered_events.append((event_date, event))
                    elif time_filter == "Last 30 Days":
                        if (now - event_date).days <= 30:
                            filtered_events.append((event_date, event))
                    elif time_filter == "Last 90 Days":
                        if (now - event_date).days <= 90:
                            filtered_events.append((event_date, event))
                    elif time_filter == "This Year":
                        if event_date.year == now.year:
                            filtered_events.append((event_date, event))
                    else:
                        filtered_events.append((event_date, event))
                except:
                    if time_filter == "All Events":
                        filtered_events.append((now, event))
            
            filtered_events.sort(key=lambda x: x[0], reverse=True)
            
            if time_filter == "By Quarter":
                st.markdown("### 📊 Events by Quarter")
                quarters = {}
                for event_date, event in filtered_events:
                    quarter = f"Q{(event_date.month-1)//3 + 1} {event_date.year}"
                    quarters.setdefault(quarter, []).append(event)
                
                for quarter in sorted(quarters.keys(), reverse=True):
                    with st.expander(f"📅 {quarter} ({len(quarters[quarter])} events)", expanded=False):
                        for event in quarters[quarter][:events_per_page]:
                            st.caption(event)
            
            elif time_filter == "By Month":
                st.markdown("### 📊 Events by Month")
                months = {}
                for event_date, event in filtered_events:
                    month = event_date.strftime("%B %Y")
                    months.setdefault(month, []).append(event)
                
                for month in sorted(months.keys(), key=lambda x: datetime.strptime(x, "%B %Y"), reverse=True):
                    with st.expander(f"📅 {month} ({len(months[month])} events)", expanded=False):
                        for event in months[month][:events_per_page]:
                            st.caption(event)
            
            else:
                st.markdown(f"### 📊 Showing {min(len(filtered_events), events_per_page)} of {len(filtered_events)} events")
                for event_date, event in filtered_events[:events_per_page]:
                    st.caption(event)
                
                if len(filtered_events) > events_per_page:
                    st.info(f"💡 {len(filtered_events) - events_per_page} more events available. Increase 'Show' count or use filters.")
        else:
            st.divider()
            st.info("📜 No rebalancing history yet. Execute your first rebalance to see history here.")

# Footer
st.divider()
st.markdown(f"""
    <div style="text-align: center; color: #64748b; padding: 20px;">
        <p><strong>Long Term Strategy Optimizer</strong> • v{VERSION} - {VERSION_NAME}</p>
        <p style="font-size: 0.85rem;">Market data by Yahoo Finance • For informational purposes only</p>
    </div>
""", unsafe_allow_html=True)
