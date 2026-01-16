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

# ===== VERSION INFORMATION =====
VERSION = "6.0.1"
VERSION_DATE = "2026-01-16"
VERSION_TIME = "09:15:00"
VERSION_NAME = "Multi-User Auth + UI Improvements"

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
    
    </style>
""", unsafe_allow_html=True)

# ===== AUTHENTICATION SYSTEM =====
DB_FILE = "alphastream_multiuser.json"

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

def load_db():
    """Load multi-user database with migration support"""
    base_schema = {
        "users": {},
        "global_settings": {
            "allow_registration": True,
            "require_email_verification": False,
            "default_drift_tolerance": 5.0
        },
        "system_logs": []
    }
    
    # Check for old single-user database file
    OLD_DB_FILE = "alphastream_wealth.json"
    
    # If new DB doesn't exist but old one does, migrate
    if not os.path.exists(DB_FILE) and os.path.exists(OLD_DB_FILE):
        try:
            with open(OLD_DB_FILE, "r") as f:
                old_data = json.load(f)
                old_profiles = old_data.get("profiles", {})
                
                # Create admin user with migrated profiles
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
                    "system_logs": [{"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "type": "migration", "message": f"Migrated {len(old_profiles)} profiles from single-user database", "user_id": "system"}]
                }
                save_db(migrated_data)
                return migrated_data
        except Exception as e:
            pass  # Fall through to create new database
    
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                data = json.load(f)
                
                # Check if this is old single-user format (has "profiles" at root level)
                if "profiles" in data and "users" not in data:
                    # Migrate old data to new multi-user format
                    old_profiles = data.get("profiles", {})
                    
                    # Create admin user with migrated profiles
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
                        "system_logs": [{"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "type": "migration", "message": "Migrated from single-user to multi-user", "user_id": "system"}]
                    }
                    save_db(migrated_data)
                    return migrated_data
                
                # Normal multi-user format - ensure schema integrity
                data.setdefault("users", {})
                data.setdefault("global_settings", base_schema["global_settings"])
                data.setdefault("system_logs", [])
                
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
        except Exception as e:
            st.error(f"Database load error: {e}")
            return base_schema
    
    # Create default admin user
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
    save_db(base_schema)
    return base_schema

def save_db(data):
    """Save database to file"""
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving database: {e}")

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
    log_system_event(db, "registration", f"New user registered: {username}", username)
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
        log_system_event(db, "login", f"User logged in: {username}", username)
        save_db(db)
        return True, "Login successful", user_data
    else:
        user_data["login_attempts"] = user_data.get("login_attempts", 0) + 1
        if user_data["login_attempts"] >= MAX_LOGIN_ATTEMPTS:
            lockout_time = datetime.now() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            user_data["lockout_until"] = lockout_time.strftime("%Y-%m-%d %H:%M:%S")
            log_system_event(db, "lockout", f"Account locked: {username}", username)
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

def calculate_average_cost(asset_data):
    """Calculate weighted average cost for an asset."""
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

# ===== SESSION STATE INITIALIZATION =====
if "db" not in st.session_state:
    st.session_state.db = load_db()

# Ensure db has required structure (safety check)
if "users" not in st.session_state.db:
    st.session_state.db["users"] = {}
if "global_settings" not in st.session_state.db:
    st.session_state.db["global_settings"] = {"allow_registration": True, "default_drift_tolerance": 5.0}
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
if "trigger_portfolio_view" not in st.session_state:
    st.session_state.trigger_portfolio_view = False
if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

# ===== AUTHENTICATION UI =====
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
                register_btn = st.form_submit_button("📝 Create Account", use_container_width=True)
            
            if login_btn:
                if not username or not password:
                    st.error("❌ Please enter username and password")
                else:
                    success, message, user_data = authenticate_user(st.session_state.db, username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.current_user = username.lower()
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
        
        st.markdown("### 📝 Register")
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

def show_admin_dashboard():
    """Display admin dashboard"""
    st.title("👑 Admin Dashboard")
    description_box("System Administration", "Manage users, view system logs, and configure global settings.")
    
    admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs([
        "👥 User Management", "📊 System Statistics", "📜 System Logs", "⚙️ Global Settings"
    ])
    
    with admin_tab1:
        st.markdown("### 👥 All Users")
        users = st.session_state.db["users"]
        
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            st.metric("Total Users", len(users))
        with col_s2:
            admin_count = sum(1 for u in users.values() if u.get("role") == "admin")
            st.metric("Admins", admin_count)
        with col_s3:
            active_count = sum(1 for u in users.values() if u.get("is_active", True))
            st.metric("Active Users", active_count)
        with col_s4:
            total_profiles = sum(len(u.get("profiles", {})) for u in users.values())
            st.metric("Total Portfolios", total_profiles)
        
        st.divider()
        
        for username, user_data in users.items():
            col_u1, col_u2, col_u3, col_u4 = st.columns([2, 2, 1, 1])
            with col_u1:
                role_badge = "👑" if user_data.get("role") == "admin" else "👤"
                status = "🟢" if user_data.get("is_active", True) else "🔴"
                st.markdown(f"**{role_badge} {user_data.get('display_name', username)}** {status}")
                st.caption(f"@{username} • {user_data.get('email', 'N/A')}")
            with col_u2:
                profiles_count = len(user_data.get("profiles", {}))
                st.caption(f"📁 {profiles_count} portfolios")
                last_login = user_data.get('last_login', 'Never')
                st.caption(f"📅 Last: {last_login[:10] if last_login else 'Never'}")
            with col_u3:
                if username != st.session_state.current_user:
                    if user_data.get("is_active", True):
                        if st.button("🔒 Deactivate", key=f"deact_{username}"):
                            st.session_state.db["users"][username]["is_active"] = False
                            log_system_event(st.session_state.db, "user_deactivated", f"Deactivated: {username}", st.session_state.current_user)
                            save_db(st.session_state.db)
                            st.rerun()
                    else:
                        if st.button("🔓 Activate", key=f"act_{username}"):
                            st.session_state.db["users"][username]["is_active"] = True
                            log_system_event(st.session_state.db, "user_activated", f"Activated: {username}", st.session_state.current_user)
                            save_db(st.session_state.db)
                            st.rerun()
            with col_u4:
                if username != st.session_state.current_user:
                    if st.button("🔑 Reset", key=f"rst_{username}"):
                        st.session_state[f"reset_pwd_user"] = username
            st.divider()
        
        if st.session_state.get("reset_pwd_user"):
            target_user = st.session_state.reset_pwd_user
            st.markdown(f"### 🔑 Reset Password for @{target_user}")
            with st.form(f"reset_pwd_form"):
                new_pwd = st.text_input("New Password", type="password")
                new_pwd_confirm = st.text_input("Confirm", type="password")
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    if st.form_submit_button("✅ Reset", type="primary"):
                        if new_pwd != new_pwd_confirm:
                            st.error("Passwords don't match")
                        else:
                            success, msg = admin_reset_password(st.session_state.db, st.session_state.current_user, target_user, new_pwd)
                            if success:
                                st.success(msg)
                                del st.session_state["reset_pwd_user"]
                                st.rerun()
                            else:
                                st.error(msg)
                with col_r2:
                    if st.form_submit_button("❌ Cancel"):
                        del st.session_state["reset_pwd_user"]
                        st.rerun()
    
    with admin_tab2:
        st.markdown("### 📊 System Statistics")
        users = st.session_state.db["users"]
        total_value = 0
        all_tickers = set()
        
        for user_data in users.values():
            for profile in user_data.get("profiles", {}).values():
                for ticker in profile.get("assets", {}).keys():
                    all_tickers.add(ticker)
        
        if all_tickers:
            try:
                with st.spinner("Fetching market data..."):
                    raw_px = yf.download(list(all_tickers), period="1d", progress=False)['Close']
                    prices = {}
                    if len(all_tickers) == 1:
                        if not raw_px.empty:
                            prices = {list(all_tickers)[0]: float(raw_px.iloc[-1])}
                    else:
                        for k, v in raw_px.iloc[-1].to_dict().items():
                            if pd.notna(v):
                                prices[k] = float(v)
                    
                    for user_data in users.values():
                        for profile in user_data.get("profiles", {}).values():
                            for ticker, asset in profile.get("assets", {}).items():
                                total_value += asset.get("units", 0) * prices.get(ticker, 0)
            except:
                prices = {}
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.markdown(f"""
                <div class="metric-showcase">
                    <h3>${total_value:,.0f}</h3>
                    <p>Total AUM</p>
                </div>
            """, unsafe_allow_html=True)
        with col_stat2:
            st.markdown(f"""
                <div class="metric-showcase" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
                    <h3>{len(all_tickers)}</h3>
                    <p>Unique Tickers</p>
                </div>
            """, unsafe_allow_html=True)
    
    with admin_tab3:
        st.markdown("### 📜 System Logs")
        logs = st.session_state.db.get("system_logs", [])
        if logs:
            log_types = list(set(log.get("type", "unknown") for log in logs))
            selected_type = st.selectbox("Filter by Type", ["All"] + log_types)
            filtered_logs = logs if selected_type == "All" else [l for l in logs if l.get("type") == selected_type]
            st.caption(f"Showing {len(filtered_logs)} of {len(logs)} logs")
            for log in filtered_logs[:100]:
                type_emoji = {"login": "🔑", "registration": "📝", "logout": "🚪", "password_change": "🔒",
                             "admin_password_reset": "👑", "lockout": "⚠️", "user_deactivated": "🔴",
                             "user_activated": "🟢"}.get(log.get("type"), "📋")
                st.caption(f"{type_emoji} **{log.get('timestamp')}** | {log.get('type')} | {log.get('message')}")
        else:
            st.info("No system logs yet")
    
    with admin_tab4:
        st.markdown("### ⚙️ Global Settings")
        settings = st.session_state.db.get("global_settings", {})
        with st.form("global_settings_form"):
            allow_reg = st.checkbox("Allow New Registrations", value=settings.get("allow_registration", True))
            default_tolerance = st.number_input("Default Drift Tolerance (%)", value=float(settings.get("default_drift_tolerance", 5.0)), min_value=0.5, max_value=20.0, step=0.5)
            if st.form_submit_button("💾 Save Settings", type="primary"):
                st.session_state.db["global_settings"]["allow_registration"] = allow_reg
                st.session_state.db["global_settings"]["default_drift_tolerance"] = default_tolerance
                save_db(st.session_state.db)
                st.success("✅ Settings saved!")
                st.rerun()

# ===== MAIN APPLICATION FLOW =====
if not st.session_state.authenticated:
    if st.session_state.auth_page == "login":
        show_login_page()
    else:
        show_registration_page()
else:
    current_user = st.session_state.current_user
    user_data = st.session_state.db.get("users", {}).get(current_user, {})
    is_admin_user = user_data.get("role") == "admin"
    
    # ===== SIDEBAR =====
    with st.sidebar:
        role_badge = "admin-badge" if is_admin_user else "user-badge"
        role_text = "👑 Admin" if is_admin_user else "👤 User"
        st.markdown(f'<div class="{role_badge}">{role_text}: {user_data.get("display_name", current_user)}</div>', unsafe_allow_html=True)
        st.caption(f"@{current_user}")
        
        st.divider()
        st.markdown("### 📊 Portfolio Optimizer")
        st.caption(f"Long Term Strategy Suite v{VERSION}")
        st.divider()
        
        if st.session_state.get("trigger_portfolio_view", False):
            st.session_state.trigger_portfolio_view = False
            if "nav_radio" in st.session_state:
                del st.session_state["nav_radio"]
        
        nav_options = ["🏠 Global Dashboard", "📊 Portfolio Manager"]
        if is_admin_user:
            nav_options.append("👑 Admin Dashboard")
        
        default_nav_index = 1 if st.session_state.get("active_profile") else 0
        view_mode = st.radio("Navigation", nav_options, index=default_nav_index, key="nav_radio")
        
        st.divider()
        
        # Profile Creation
        st.markdown("### ① Strategy Setup")
        with st.expander("🆕 Create New Profile", expanded=False):
            with st.form("new_profile_form"):
                n_name = st.text_input("Profile Name*", placeholder="e.g., Retirement USD")
                col1, col2 = st.columns(2)
                with col1:
                    n_bank = st.text_input("Bank/Broker*", placeholder="e.g., Fidelity")
                with col2:
                    n_account_type = st.selectbox("Account Type*", ["", "Taxable", "401k", "IRA", "Roth IRA", "TFSA", "RRSP", "529", "HSA", "Other"])
                n_curr = st.selectbox("Currency*", ["USD", "CAD"])
                n_p = st.number_input("Principal ($)*", value=10000.0, step=1000.0, min_value=0.0)
                n_goal = st.number_input("Annual Growth Goal (%)*", value=10.0, step=0.5, min_value=0.0)
                n_start = st.date_input("Inception Date*", value=date.today() - timedelta(days=365), max_value=date.today())
                
                submitted = st.form_submit_button("🚀 Initialize Profile", use_container_width=True)
                if submitted:
                    user_profiles = get_user_profiles(st.session_state.db, current_user)
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
                            "drift_tolerance": 5.0, "rebalance_stats": [], "last_rebalanced": None, "benchmark": None
                        }
                        save_db(st.session_state.db)
                        prof = st.session_state.db["users"][current_user]["profiles"][n_name]
                        log_profile(prof, "Profile created")
                        st.success(f"✅ '{n_name}' created!")
                        st.rerun()
        
        # Profile-specific sidebar
        user_profiles = get_user_profiles(st.session_state.db, current_user)
        
        if view_mode == "📊 Portfolio Manager" and user_profiles:
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
                    if st.button("🔄 Yes, Reset", use_container_width=True, type="primary", key="confirm_reset"):
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
            st.caption("Compare against market benchmarks")
            with st.expander("ℹ️ Why use a benchmark?", expanded=False):
                st.markdown("""
                **Benchmarks** help evaluate performance.
                - Chart shows 100% investment in the benchmark
                - **Outperforming** = your strategy adds value
                """)
            
            benchmark_options = {
                "None": None, "S&P 500 (SPY)": "SPY", "NASDAQ-100 (QQQ)": "QQQ",
                "Total Market (VTI)": "VTI", "Russell 2000 (IWM)": "IWM", "Dow Jones (DIA)": "DIA"
            }
            current_benchmark = prof.get('benchmark')
            benchmark_index = 0
            for idx, (key, value) in enumerate(benchmark_options.items()):
                if value == current_benchmark:
                    benchmark_index = idx
                    break
            
            selected_benchmark = st.selectbox("Select Benchmark", options=list(benchmark_options.keys()),
                                             index=benchmark_index, key="benchmark_select")
            if st.button("💾 Save Benchmark", use_container_width=True, key="save_benchmark"):
                prof['benchmark'] = benchmark_options[selected_benchmark]
                save_db(st.session_state.db)
                st.success("✅ Saved!")
                st.rerun()
            
            if prof.get('benchmark'):
                st.caption(f"📊 Active: {prof['benchmark']}")
            
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
            
            a_sym = st.text_input("Ticker Symbol", placeholder="e.g., AAPL", key="ticker_input").upper().strip()
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
            
            if prof.get("asset_mix_locked", False) and not is_existing and a_sym:
                st.error("🔒 **Asset mix locked** - Cannot add new assets")
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
                            st.caption(f"**Price:** {p_flag} ${last_price:,.2f}")
                            valid_ticker = True
                        else:
                            st.error(f"❌ No data for '{a_sym}'")
                except:
                    if a_sym:
                        st.error(f"❌ Invalid '{a_sym}'")
            
            if valid_ticker:
                st.markdown("---")
                default_target = prof.get("assets", {}).get(a_sym, {}).get("target", 0.0)
                
                a_w = st.number_input("Target Allocation %", min_value=0.0, max_value=max_available,
                                     value=min(float(default_target), max_available), step=0.5, 
                                     help=f"Set the target % for {a_sym}. Max available: {max_available:.1f}%",
                                     key="target_weight")
                
                st.markdown("---")
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    save_disabled = (a_w <= 0) or (a_w > max_available)
                    if st.button("💾 Save Asset", use_container_width=True, type="primary", key="save_asset", disabled=save_disabled):
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
            
            # Show existing assets
            if prof.get("assets"):
                st.divider()
                st.markdown("### 📋 Current Assets")
                for ticker, data in prof["assets"].items():
                    units = data.get('units', 0)
                    allocated_pct = data.get('allocated_pct', 0)
                    if units > 0:
                        st.caption(f"**{ticker}**: {data['target']}% target • {allocated_pct:.0f}% deployed ({units:.4f} units)")
                    else:
                        st.caption(f"**{ticker}**: {data['target']}% target • Not deployed")
            
            # Asset Mix Locking
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
            
            # Asset Deployment
            st.markdown("### ⑥ Asset Deployment")
            st.caption("Deploy capital into individual assets")
            
            if not prof.get("asset_mix_locked", False):
                st.info("🔒 **Lock your asset mix first**")
            else:
                assets = prof.get("assets", {})
                deployable_assets = {t: d for t, d in assets.items() if d.get("allocated_pct", 0) < 100.0}
                fully_deployed_count = sum(1 for a in assets.values() if a.get("allocated_pct", 0) >= 100.0)
                total_assets = len(assets)
                
                st.markdown(f"**Progress:** {fully_deployed_count}/{total_assets} assets fully deployed")
                
                if total_assets > 0:
                    deployment_progress = fully_deployed_count / total_assets
                    progress_pct = deployment_progress * 100
                    if deployment_progress >= 1.0:
                        bar_color = "#10b981"
                    elif deployment_progress >= 0.5:
                        bar_color = "#fbbf24"
                    else:
                        bar_color = "#ef4444"
                    
                    st.markdown(f'''
                        <div style="margin: 20px 0;">
                            <div style="background: #e5e7eb; border-radius: 12px; height: 12px; overflow: hidden;">
                                <div style="background: {bar_color}; height: 100%; width: {progress_pct}%;"></div>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                
                if not deployable_assets:
                    st.success("✅ **All assets 100% deployed!**")
                else:
                    with st.expander("➕ Record Asset Deployment", expanded=False):
                        st.markdown("**Deploy capital into a specific asset**")
                        
                        selected_ticker = st.selectbox("Select Asset", options=list(deployable_assets.keys()),
                            format_func=lambda t: f"{t} - {deployable_assets[t].get('fund_name', t)}", key="deploy_asset_selector")
                        
                        if selected_ticker:
                            asset_data = deployable_assets[selected_ticker]
                            current_allocated = asset_data.get("allocated_pct", 0)
                            remaining_pct = 100.0 - current_allocated
                            target_pct = asset_data.get("target", 0)
                            
                            st.markdown(f"**{selected_ticker}:** {target_pct}% target, {current_allocated:.1f}% deployed, {remaining_pct:.1f}% remaining")
                            
                            deploy_pct = st.number_input("Deploy % (of asset's target)", min_value=0.1, max_value=remaining_pct,
                                                        value=min(25.0, remaining_pct), step=0.1, key="deploy_pct_input")
                            
                            inception_date = datetime.strptime(prof.get('start_date'), '%Y-%m-%d').date()
                            deploy_date = st.date_input("Deployment Date", value=date.today(), min_value=inception_date,
                                                       max_value=date.today(), key="deploy_date_input")
                            
                            portfolio_pct = (deploy_pct / 100) * target_pct
                            deploy_amount = (portfolio_pct / 100) * prof['principal']
                            
                            # Fetch and display price preview for the selected date
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
                            
                            # Display deployment preview with price info
                            if preview_price:
                                estimated_units = deploy_amount / preview_price
                                p_flag = "🇺🇸" if prof.get("currency") == "USD" else "🇨🇦"
                                
                                st.markdown(f'''
                                    <div class="buying-guide">
                                        <div style="margin-bottom: 8px;"><strong>📊 Deployment Preview:</strong></div>
                                        <div>• <strong>Price on {preview_price_date}:</strong> {p_flag} ${preview_price:,.2f}</div>
                                        <div>• <strong>Investment Amount:</strong> ${deploy_amount:,.2f} ({deploy_pct:.1f}% of {target_pct}% target)</div>
                                        <div>• <strong>Estimated Units:</strong> <span class="buying-guide-highlight">{estimated_units:.4f} units</span></div>
                                    </div>
                                ''', unsafe_allow_html=True)
                                
                                if preview_price_date != deploy_date:
                                    st.caption(f"ℹ️ Using {preview_price_date} price (closest trading day)")
                            else:
                                st.warning(f"⚠️ Could not fetch price for {deploy_date}. Price will be fetched when recording.")
                                st.info(f"**Deploying:** {deploy_pct:.1f}% of {selected_ticker}'s {target_pct}% = ${deploy_amount:,.2f}")
                            
                            if st.button("📥 Record Deployment", type="primary", use_container_width=True, key="record_deploy_btn"):
                                try:
                                    if preview_price:
                                        # Use the already fetched price
                                        price = preview_price
                                        quantity = deploy_amount / price
                                        purchase = {"date": str(deploy_date), "deploy_pct": deploy_pct,
                                                   "amount": deploy_amount, "price": price, "quantity": quantity}
                                        asset_data.setdefault("purchases", []).append(purchase)
                                        asset_data["units"] = asset_data.get("units", 0) + quantity
                                        asset_data["allocated_pct"] = min(100.0, current_allocated + deploy_pct)
                                        log_profile(prof, f"Deployed {deploy_pct:.1f}% of {selected_ticker} (${deploy_amount:,.2f} @ ${price:.2f} = {quantity:.4f} units)")
                                        save_db(st.session_state.db)
                                        st.success(f"✅ Deployed {deploy_pct:.1f}% of {selected_ticker} - {quantity:.4f} units @ ${price:.2f}")
                                        if asset_data['allocated_pct'] >= 100.0:
                                            st.balloons()
                                        st.rerun()
                                    else:
                                        st.error("❌ Could not fetch price. Please try a different date.")
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
            
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
        
        with st.expander("🔑 Change Password", expanded=False):
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
        
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            log_system_event(st.session_state.db, "logout", f"User logged out: {current_user}", current_user)
            save_db(st.session_state.db)
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.session_token = None
            st.session_state.active_profile = None
            st.rerun()

    # ===== MAIN CONTENT AREA =====
    if view_mode == "👑 Admin Dashboard" and is_admin_user:
        show_admin_dashboard()
    
    elif view_mode == "🏠 Global Dashboard":
        st.title("🏠 Global Portfolio Dashboard")
        
        description_box(
            "Portfolio Command Center",
            f"Welcome back, {user_data.get('display_name', current_user)}! Monitor all your investment strategies at a glance."
        )
        
        profiles = get_user_profiles(st.session_state.db, current_user)
        
        if not profiles:
            st.info("👋 Welcome! Create your first investment profile using the sidebar.")
            st.markdown("### 🎯 Key Features")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="premium-card"><h4>🎯 Drift Detection</h4><p style="color: #64748b;">Automatic alerts when assets deviate from target allocation.</p></div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="premium-card"><h4>📈 Performance Tracking</h4><p style="color: #64748b;">Real-time portfolio valuation vs. your target growth path.</p></div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="premium-card"><h4>⚖️ Smart Rebalancing</h4><p style="color: #64748b;">Two-step workflow with slippage management.</p></div>', unsafe_allow_html=True)
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
                all_deployed = all(a.get("allocated_pct", 0) >= 100.0 for a in p_assets.values()) if p_assets else False
                deployed_count = sum(1 for a in p_assets.values() if a.get("allocated_pct", 0) >= 100.0)
                total_assets = len(p_assets)
                
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
                    remaining = [(t, a.get("allocated_pct", 0)) for t, a in p_assets.items() if a.get("allocated_pct", 0) < 100.0]
                    action_items.append({
                        "priority": 2, "type": "deployment", "profile": p_name,
                        "message": f"📥 IN PROGRESS - {p_name} deployment ({deployed_count}/{total_assets} assets)",
                        "detail": ", ".join([f"{t} needs {100-pct:.0f}% more" for t, pct in remaining[:3]]),
                        "action": "Complete remaining asset deployments"
                    })
            
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
                                <div style="color: #7f1d1d; font-size: 0.85rem; font-style: italic;">→ {item['action']}</div>
                            </div>
                        ''', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''
                            <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                                        border-left: 4px solid #f59e0b; padding: 16px; border-radius: 8px; margin: 12px 0;">
                                <div style="font-weight: 700; color: #92400e; font-size: 1.05rem; margin-bottom: 8px;">{item['message']}</div>
                                <div style="color: #78350f; font-size: 0.9rem; margin-bottom: 8px;">📋 {item['detail']}</div>
                                <div style="color: #78350f; font-size: 0.85rem; font-style: italic;">→ {item['action']}</div>
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
                roi_pct = ((curr_v / start_val) - 1) * 100 if start_val > 0 else 0
                
                start_date = datetime.strptime(p_data.get('start_date', str(date.today())), '%Y-%m-%d')
                years_elapsed = max((date.today() - start_date.date()).days / 365.25, 0.01)
                cagr = ((curr_v / start_val) ** (1 / years_elapsed) - 1) * 100 if start_val > 0 else 0
                
                p_flag = "🇺🇸" if p_data.get("currency") == "USD" else "🇨🇦"
                all_deployed = all(a.get("allocated_pct", 0) >= 100.0 for a in p_assets.values()) if p_assets else False
                
                if recently_rebalanced or (has_rebalanced and not needs_rebal):
                    tile_class = "profile-tile-optimized"
                    status_badge = '<span class="success-badge">✅ Balanced</span>'
                elif needs_rebal:
                    tile_class = "profile-tile-warning"
                    status_badge = '<span class="drift-badge">🚨 REBALANCE</span>'
                elif not all_deployed and len(p_assets) > 0:
                    tile_class = "profile-tile"
                    deployed_count = sum(1 for a in p_assets.values() if a.get("allocated_pct", 0) >= 100.0)
                    status_badge = f'<span style="background: #f59e0b; color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.75rem;">📥 Deploying ({deployed_count}/{len(p_assets)})</span>'
                elif all_deployed:
                    tile_class = "profile-tile-optimized"
                    status_badge = '<span class="success-badge">✅ Deployed</span>'
                else:
                    tile_class = "profile-tile"
                    status_badge = '<span style="background: #94a3b8; color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.75rem;">⚪ New</span>'
                
                with cols[i % 2]:
                    st.markdown(f'''
                        <div class="{tile_class}" style="padding: 24px; margin-top: 0px;">
                            <div class="profile-tile-header">{p_flag} {name}</div>
                            <div style="margin-bottom: 16px; text-align: center;">{status_badge}</div>
                            <div style="margin: 20px 0; text-align: center;">
                                <div class="stat-label">Portfolio Value</div>
                                <div class="stat-value" style="font-size: 2rem;">${curr_v:,.0f}</div>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 0.9rem; color: #64748b;">
                                <div><div style="font-size: 0.75rem; opacity: 0.8;">Goal</div><div style="font-weight: 600;">{p_data['yearly_goal_pct']}%/yr</div></div>
                                <div style="text-align: center;"><div style="font-size: 0.75rem; opacity: 0.8;">CAGR</div><div style="font-weight: 600; color: {'#10b981' if cagr >= 0 else '#ef4444'};">{cagr:+.1f}%</div></div>
                                <div style="text-align: right;"><div style="font-size: 0.75rem; opacity: 0.8;">ROI</div><div style="font-weight: 600; color: {'#10b981' if roi_pct >= 0 else '#ef4444'};">{roi_pct:+.1f}%</div></div>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    if st.button(f"📊 Open {name}", key=f"open_{name}", use_container_width=True):
                        st.session_state.active_profile = name
                        st.session_state.trigger_portfolio_view = True
                        st.rerun()
                    st.markdown("")
            
            st.divider()
            
            # Performance Breakdown
            st.markdown("### 📊 Performance Breakdown")
            
            performance_data = []
            for p_name, p_data in profiles.items():
                p_assets = p_data.get("assets", {})
                curr_val = float(sum(p_assets[t]["units"] * prices.get(t, 0) for t in p_assets))
                start_val = float(p_data.get('principal', 0))
                start_date = datetime.strptime(p_data.get('start_date', str(date.today())), '%Y-%m-%d').date()
                
                if start_val > 0:
                    days_elapsed = (date.today() - start_date).days
                    total_return_pct = ((curr_val / start_val) - 1) * 100
                    performance_data.append({
                        'name': p_name, 'start_date': start_date, 'days_elapsed': days_elapsed,
                        'start_val': start_val, 'curr_val': curr_val,
                        'total_return': curr_val - start_val, 'total_return_pct': total_return_pct
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
                
                # Performance comparison chart
                if len(performance_data) > 1:
                    st.markdown("#### 📈 Portfolio Performance Comparison")
                    perf_sorted = sorted(performance_data, key=lambda x: x['total_return_pct'], reverse=True)
                    colors = ['#10b981' if p['total_return_pct'] >= 0 else '#ef4444' for p in perf_sorted]
                    
                    fig_perf = go.Figure()
                    fig_perf.add_trace(go.Bar(
                        x=[p['name'] for p in perf_sorted],
                        y=[p['total_return_pct'] for p in perf_sorted],
                        marker_color=colors,
                        text=[f"{p['total_return_pct']:+.1f}%" for p in perf_sorted],
                        textposition='outside', width=0.4
                    ))
                    fig_perf.update_layout(height=400, showlegend=False, plot_bgcolor='white',
                        xaxis=dict(title="Portfolio"), yaxis=dict(title="Total Return (%)", gridcolor='#f3f4f6'))
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
                        "Cost Basis": f"${data['cost_basis']:,.0f}",
                        "Current Value": f"${data['current_value']:,.0f}",
                        "Gain/Loss": f"${gain:,.0f}",
                        "Return %": f"{return_pct:+.1f}%",
                        "_gain": gain,
                        "_cost_basis": data["cost_basis"],
                        "In Portfolios": ", ".join(data["portfolios"])
                    })
                
                # Sort by absolute gain
                attribution_list_sorted = sorted(attribution_list, key=lambda x: abs(x["_gain"]), reverse=True)
                
                # Separate into contributors and detractors
                contributors = [a for a in attribution_list_sorted if a["_gain"] > 0]
                detractors = [a for a in attribution_list_sorted if a["_gain"] < 0]
                
                col_attr1, col_attr2 = st.columns(2)
                with col_attr1:
                    st.markdown("#### 💚 Top Contributors")
                    if contributors:
                        for asset in contributors[:5]:
                            contribution = (asset["_gain"] / abs(total_portfolio_gain) * 100) if total_portfolio_gain != 0 else 0
                            st.success(f"**{asset['Asset']}**: {asset['Gain/Loss']} ({asset['Return %']}) - {contribution:.1f}% of gains")
                    else:
                        st.info("No assets with gains currently")
                
                with col_attr2:
                    st.markdown("#### 💔 Top Detractors")
                    if detractors:
                        for asset in sorted(detractors, key=lambda x: x["_gain"])[:5]:
                            contribution = (abs(asset["_gain"]) / abs(total_portfolio_gain) * 100) if total_portfolio_gain != 0 else 0
                            st.error(f"**{asset['Asset']}**: {asset['Gain/Loss']} ({asset['Return %']}) - {contribution:.1f}% of losses")
                    else:
                        st.success("✅ No detractors - all assets profitable!")
                
                # Summary
                net_color = "normal" if total_portfolio_gain >= 0 else "inverse"
                st.metric("📊 Net Portfolio Gain/Loss", f"${total_portfolio_gain:,.0f}", 
                         delta=f"{((total_portfolio_gain / sum(a['_cost_basis'] for a in attribution_list_sorted)) * 100):+.1f}%" if sum(a['_cost_basis'] for a in attribution_list_sorted) > 0 else "N/A",
                         delta_color=net_color)
            
            st.divider()
            
            # Portfolio Comparison Table
            st.markdown("### 📊 Portfolio Comparison Table")
            
            comparison_data = []
            for p_name, p_data in profiles.items():
                p_assets = p_data.get("assets", {})
                curr_val = float(sum(p_assets[t]["units"] * prices.get(t, 0) for t in p_assets))
                start_val = float(p_data.get('principal', 0))
                roi = ((curr_val / start_val) - 1) * 100 if start_val > 0 else 0
                start_date = datetime.strptime(p_data.get('start_date', str(date.today())), '%Y-%m-%d')
                years = max((date.today() - start_date.date()).days / 365.25, 0.01)
                cagr = ((curr_val / start_val) ** (1 / years) - 1) * 100 if start_val > 0 else 0
                
                needs_rebal, _ = calculate_drift_status(p_data, prices)
                all_deployed = all(a.get("allocated_pct", 0) >= 100.0 for a in p_assets.values()) if p_assets else False
                deployed_count = sum(1 for a in p_assets.values() if a.get("allocated_pct", 0) >= 100.0)
                total_assets = len(p_assets)
                
                if needs_rebal:
                    status = "🚨 Rebalance"
                elif not all_deployed and total_assets > 0:
                    status = f"📥 Deploying ({deployed_count}/{total_assets})"
                elif all_deployed:
                    status = "✅ Balanced"
                else:
                    status = "⚪ New"
                
                comparison_data.append({
                    "Profile": p_name,
                    "Account": f"{p_data.get('bank_name', 'N/A')} {p_data.get('account_type', '')}",
                    "Value": f"${curr_val:,.0f}",
                    "CAGR": f"{cagr:+.1f}%",
                    "ROI": f"{roi:+.1f}%",
                    "Goal": f"{p_data.get('yearly_goal_pct', 0):.1f}%/yr",
                    "Assets": total_assets,
                    "Status": status
                })
            
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True, hide_index=True)

    elif view_mode == "📊 Portfolio Manager":
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
        
        st.title(f"{p_flag} {st.session_state.active_profile}")
        st.caption(f"Portfolio Manager • Inception: {prof.get('start_date', 'N/A')} • Drift Tolerance: {prof.get('drift_tolerance', 5.0)}%")
        
        # Deployment status banner
        if not prof.get("asset_mix_locked", False):
            st.warning("⚠️ **Asset mix not locked** - Define and lock assets first")
        else:
            assets = prof.get("assets", {})
            all_deployed = all(a.get("allocated_pct", 0) >= 100.0 for a in assets.values())
            if assets and not all_deployed:
                partial = [(t, a.get("allocated_pct", 0)) for t, a in assets.items() if a.get("allocated_pct", 0) < 100.0]
                st.info(f"📊 **Deployment in progress** - {len(partial)} asset(s) not fully deployed")
            elif assets and all_deployed:
                st.success("✅ **All assets deployed** - Portfolio drift monitoring active")
        
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
                    deployed_count = sum(1 for a in assets.values() if a.get("allocated_pct", 0) >= 100.0)
                    total_count = len(assets)
                    if deployed_count < total_count:
                        st.metric("Deployment", f"{deployed_count}/{total_count}", delta="In Progress", delta_color="off")
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
            6. **⑥ Asset Deployment**: Record your purchases at actual prices
            
            **After deployment:**
            - **Monitor Drift**: System alerts when rebalancing is needed
            - **Rebalance**: Execute trades to restore target allocations
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
                
                if curr_v <= 0:
                    st.warning("⚠️ **Portfolio value is zero**")
                    st.info("Complete asset deployments to see portfolio metrics.")
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
                    st.markdown(f'<div class="stat-item"><div class="stat-label">Total ROI</div><div class="stat-value" style="color: {"#10b981" if roi_pct >= 0 else "#ef4444"};">{roi_pct:+.2f}%</div></div>', unsafe_allow_html=True)
                with col_s3:
                    st.markdown(f'<div class="stat-item"><div class="stat-label">CAGR</div><div class="stat-value" style="color: {"#10b981" if profile_cagr >= 0 else "#ef4444"};">{profile_cagr:+.2f}%</div></div>', unsafe_allow_html=True)
                with col_s4:
                    st.markdown(f'<div class="stat-item"><div class="stat-label">vs Target Path</div><div class="stat-value" style="color: {"#10b981" if perc_diff >= 0 else "#ef4444"};">{perc_diff:+.2f}%</div></div>', unsafe_allow_html=True)
                with col_s5:
                    annualized = ((curr_v / start_val) ** (1/years) - 1) * 100
                    st.markdown(f'<div class="stat-item"><div class="stat-label">Annualized</div><div class="stat-value" style="color: {"#10b981" if annualized >= 0 else "#ef4444"};">{annualized:.2f}%</div></div>', unsafe_allow_html=True)
                
                st.divider()
                
                # Performance Chart
                st.markdown("### 📈 Performance vs Goal Path")
                benchmark_caption = f" & 100% {prof.get('benchmark', '')}" if prof.get('benchmark') else ""
                st.caption(f"Track your portfolio's performance against target growth{benchmark_caption}")
                
                fig = go.Figure()
                
                # Benchmark comparison
                benchmark_ticker = prof.get('benchmark')
                if benchmark_ticker:
                    try:
                        benchmark_raw = yf.download(benchmark_ticker, start=prof["start_date"], auto_adjust=True, progress=False)
                        if not benchmark_raw.empty:
                            benchmark_data = benchmark_raw['Close']
                            if isinstance(benchmark_data, pd.DataFrame):
                                benchmark_data = benchmark_data.squeeze()
                            benchmark_data = benchmark_data.dropna()
                            if len(benchmark_data) > 0:
                                first_price = float(benchmark_data.iloc[0])
                                benchmark_normalized = (benchmark_data / first_price) * start_val
                                bench_return = ((float(benchmark_data.iloc[-1]) / first_price) - 1) * 100
                                fig.add_trace(go.Scatter(
                                    x=benchmark_data.index, y=benchmark_normalized,
                                    name=f'100% {benchmark_ticker} ({bench_return:+.1f}%)',
                                    line=dict(color='#ef4444', width=3, dash='dot')
                                ))
                    except:
                        pass
                
                # Actual portfolio
                fig.add_trace(go.Scatter(x=data.index, y=daily_val, name='Actual Portfolio',
                    line=dict(color='#3b82f6', width=3)))
                
                # Goal path
                days = np.arange(len(data.index))
                daily_rate = (float(prof['yearly_goal_pct']) / 100) / 365.25
                target_path = start_val * (1 + daily_rate) ** days
                fig.add_trace(go.Scatter(x=data.index, y=target_path,
                    name=f'Goal Path ({prof["yearly_goal_pct"]}%/yr)',
                    line=dict(color='#10b981', width=2, dash='dash')))
                
                fig.update_layout(
                    hovermode='x unified', plot_bgcolor='white', height=550, showlegend=True,
                    xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title='Date'),
                    yaxis=dict(showgrid=True, gridcolor='#f1f5f9', title='Portfolio Value ($)', tickformat='$,.0f'),
                    legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.divider()
                
                # Holdings Table
                st.markdown("### 📋 Current Holdings & Rebalancing Analysis")
                
                column_config = {
                    "Fund Name": st.column_config.TextColumn("Fund Name", width="large"),
                    "Ticker": st.column_config.TextColumn("Ticker", width="small"),
                    "Target %": st.column_config.TextColumn("Target %", width="small"),
                    "Deployed": st.column_config.TextColumn("Deployed", width="small"),
                    "Actual %": st.column_config.TextColumn("Actual %", width="small"),
                    "Drift": st.column_config.TextColumn("Drift", width="small"),
                    "Status": st.column_config.TextColumn("Status", width="medium"),
                    "Avg Cost": st.column_config.TextColumn("Avg Cost", width="small"),
                    "Units": st.column_config.TextColumn("Units", width="small"),
                    "Current Price": st.column_config.TextColumn("Price", width="small"),
                    "%Daily Change": st.column_config.TextColumn("%Change", width="small"),
                    "Amount": st.column_config.TextColumn("Value", width="medium"),
                    "Buy/Sell Amt": st.column_config.TextColumn("Trade Amt", width="medium"),
                    "Buy/Sell Shares": st.column_config.TextColumn("Trade Shares", width="small")
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
                    cur_u = float(asset_dict[t]["units"])
                    tar_w = float(asset_dict[t]['target'])
                    allocated_pct = asset_dict[t].get("allocated_pct", 0)
                    
                    # Validation fixes
                    if allocated_pct > 100:
                        allocated_pct = 100.0
                    elif cur_u > 0 and allocated_pct == 0:
                        allocated_pct = 100.0
                    
                    avg_cost = calculate_average_cost(asset_dict[t])
                    avg_cost_display = f"${avg_cost:.2f}" if avg_cost else "Pending"
                    
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
                        drift_display = f"⚠️ {drift:+.2f}%"
                        status_display = f"⏳ Deploying ({allocated_pct:.0f}%)"
                    else:
                        if abs(drift) >= prof.get("drift_tolerance", 5.0):
                            drift_display = f"🔴 {drift:+.2f}%"
                        elif abs(drift) > 0.5:
                            drift_display = f"🟡 {drift:+.2f}%"
                        else:
                            drift_display = f"🟢 {drift:+.2f}%"
                        status_display = "✅ Deployed"
                    
                    rows.append({
                        "Fund Name": fund_name, "Ticker": t, "Target %": f"{tar_w:.2f}%",
                        "Deployed": f"{allocated_pct:.0f}%", "Actual %": f"{act_w:.2f}%",
                        "Drift": drift_display, "Status": status_display, "Avg Cost": avg_cost_display,
                        "Units": f"{cur_u:.0f}", "Current Price": f"${current_price:.2f}",
                        "%Daily Change": f"{daily_change_pct:+.2f}%", "Amount": f"${act_val:,.0f}",
                        "Buy/Sell Amt": f"${abs(val_diff):,.0f}", "Buy/Sell Shares": f"{unit_diff:+.0f}"
                    })
                
                rows.append({
                    "Fund Name": "**TOTAL**", "Ticker": "", "Target %": "**100.00%**",
                    "Deployed": "", "Actual %": "**100.00%**", "Drift": "—", "Status": "",
                    "Avg Cost": "", "Units": "", "Current Price": "", "%Daily Change": "",
                    "Amount": f"**${total_current_val:,.0f}**",
                    "Buy/Sell Amt": f"**${total_turnover:,.0f}**", "Buy/Sell Shares": "—"
                })
                
                df_rebalance = pd.DataFrame(rows)
                st.dataframe(df_rebalance, use_container_width=True, hide_index=True, column_config=column_config)
                
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
                    st.markdown("#### 📋 Phase A: Get Recommendation")
                    if needs_rebalance:
                        st.warning("⚠️ **Rebalancing recommended**")
                    
                    if st.button("📋 Recommend Rebalance", type="primary" if needs_rebalance else "secondary",
                                use_container_width=True, disabled=not needs_rebalance, key="recommend_rebalance"):
                        recommendations = []
                        for t in v_t:
                            old_units = float(asset_dict[t]["units"])
                            new_units = float((asset_dict[t]["target"] / 100 * curr_v) / data[t].iloc[-1])
                            change_units = new_units - old_units
                            if abs(change_units) > 0.0001:
                                action = "BUY" if change_units > 0 else "SELL"
                                current_price = float(data[t].iloc[-1])
                                recommendations.append({
                                    "ticker": t, "action": action, "shares": abs(change_units),
                                    "estimated_price": current_price, "estimated_value": abs(change_units) * current_price
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
                    if st.button("✅ Execute Rebalance Now", type="primary", use_container_width=True,
                                disabled=not has_recommendation, key="execute_rebalance"):
                        st.session_state.show_execute_form = True
                        st.rerun()
                    if not has_recommendation:
                        st.info("📋 Get recommendation first")
                
                # Show recommendation details
                if st.session_state.get("show_rebalance_recommendation", False) and "pending_rebalance" in prof:
                    st.markdown("---")
                    st.markdown("### 📋 Phase B: Review & Execute at Broker")
                    st.caption(f"Generated: {prof['pending_rebalance']['timestamp']}")
                    
                    recommendations = prof["pending_rebalance"]["recommendations"]
                    if recommendations:
                        st.markdown("**Recommended Trades:**")
                        for rec in recommendations:
                            color = "🟢" if rec['action'] == "BUY" else "🔴"
                            st.markdown(f"{color} **{rec['action']} {rec['ticker']}**: {rec['shares']:.4f} shares @ ~${rec['estimated_price']:.2f} (${rec['estimated_value']:.2f})")
                        
                        st.markdown("""
                        **Next Steps:**
                        1. Go to your broker (Fidelity, IBKR, etc.)
                        2. Execute the trades listed above
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
                    st.markdown("### 💰 Enter Actual Broker Prices")
                    st.caption("Enter the exact prices you received")
                    
                    recommendations = prof["pending_rebalance"]["recommendations"]
                    
                    with st.form("actual_prices_form"):
                        st.markdown("**For each trade, enter the actual price:**")
                        actual_prices = {}
                        
                        for rec in recommendations:
                            st.markdown(f"**{rec['action']} {rec['ticker']}** ({rec['shares']:.4f} shares)")
                            st.caption(f"Estimated: ${rec['estimated_price']:.2f}")
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
                                if rec['action'] == "BUY":
                                    asset_dict[ticker]["units"] = float(asset_dict[ticker]["units"]) + rec['shares']
                                    changes.append(f"🟢 {ticker} BUY {rec['shares']:.4f} @ ${actual_price:.2f}")
                                else:
                                    asset_dict[ticker]["units"] = float(asset_dict[ticker]["units"]) - rec['shares']
                                    changes.append(f"🔴 {ticker} SELL {rec['shares']:.4f} @ ${actual_price:.2f}")
                            
                            detail_log += ", ".join(changes) if changes else "No changes"
                            prof.setdefault("rebalance_stats", []).insert(0, detail_log)
                            prof["rebalance_stats"] = prof["rebalance_stats"][:50]
                            prof["last_rebalanced"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            clear_rebalance_recommendation(prof)
                            log_profile(prof, "Portfolio rebalanced with actual prices - Status: Balanced")
                            save_db(st.session_state.db)
                            
                            st.session_state.show_execute_form = False
                            st.session_state.show_rebalance_recommendation = False
                            st.success("✅ Portfolio rebalanced successfully!")
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
