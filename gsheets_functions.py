"""
Google Sheets Database Functions for InvestLongTermStrategyTool
Replaces JSON file storage with persistent Google Sheets backend
Maintains exact same interface as load_db() and save_db()
"""

import streamlit as st
from st_gsheets_connection import GSheetsConnection
import pandas as pd
import json
from datetime import datetime
from typing import Dict, Any

# ===== CONFIGURATION =====
WORKSHEET_PROFILES = "profiles"
WORKSHEET_LOGS = "app_logs"
CACHE_TTL = 300  # 5 minutes

# ===== CONNECTION =====
@st.cache_resource
def get_gsheets_connection():
    """
    Initialize and cache Google Sheets connection
    Shared across all users
    """
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn
    except Exception as e:
        st.error(f"❌ Failed to connect to Google Sheets")
        st.error(f"Error: {e}")
        st.info("💡 Check your .streamlit/secrets.toml configuration")
        st.info("📄 Make sure the sheet is shared with your service account:")
        st.code("investlongtermstrategytool-ser@investlongtermstrategytool.iam.gserviceaccount.com")
        st.stop()

# ===== INITIALIZATION =====
def initialize_sheets():
    """
    Create required worksheets if they don't exist
    Only runs once at startup
    """
    if "sheets_initialized" in st.session_state:
        return
    
    try:
        conn = get_gsheets_connection()
        
        # Try to read profiles sheet
        try:
            df = conn.read(worksheet=WORKSHEET_PROFILES, ttl=0)
            if df is None or df.empty:
                # Create empty profiles sheet
                df = pd.DataFrame(columns=["profile_name", "data_json", "last_modified"])
                conn.update(worksheet=WORKSHEET_PROFILES, data=df)
        except:
            # Sheet doesn't exist, create it
            df = pd.DataFrame(columns=["profile_name", "data_json", "last_modified"])
            conn.update(worksheet=WORKSHEET_PROFILES, data=df)
        
        # Try to read logs sheet
        try:
            df = conn.read(worksheet=WORKSHEET_LOGS, ttl=0)
            if df is None or df.empty:
                # Create empty logs sheet
                df = pd.DataFrame(columns=["timestamp", "event", "details", "session_id"])
                conn.update(worksheet=WORKSHEET_LOGS, data=df)
        except:
            # Sheet doesn't exist, create it
            df = pd.DataFrame(columns=["timestamp", "event", "details", "session_id"])
            conn.update(worksheet=WORKSHEET_LOGS, data=df)
        
        st.session_state.sheets_initialized = True
        
    except Exception as e:
        st.warning(f"⚠️ Could not initialize sheets: {e}")
        st.session_state.sheets_initialized = True  # Don't retry every time

# ===== STARTUP LOGGING =====
def log_app_startup():
    """
    Log app startup to Google Sheet
    Only runs once per session
    """
    if "app_startup_logged" in st.session_state:
        return
    
    try:
        conn = get_gsheets_connection()
        
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event": "App Launch",
            "details": "InvestLongTermStrategyTool v5.11.7",
            "session_id": st.session_state.get("session_id", "unknown")
        }
        
        # Read existing logs
        try:
            logs_df = conn.read(worksheet=WORKSHEET_LOGS, ttl=0)
            if logs_df is None or logs_df.empty:
                logs_df = pd.DataFrame(columns=["timestamp", "event", "details", "session_id"])
        except:
            logs_df = pd.DataFrame(columns=["timestamp", "event", "details", "session_id"])
        
        # Append new log
        new_log = pd.DataFrame([log_entry])
        updated_logs = pd.concat([logs_df, new_log], ignore_index=True)
        
        # Keep only last 1000 logs
        if len(updated_logs) > 1000:
            updated_logs = updated_logs.tail(1000)
        
        conn.update(worksheet=WORKSHEET_LOGS, data=updated_logs)
        st.session_state.app_startup_logged = True
        
    except Exception as e:
        # Don't fail app if logging fails
        st.session_state.app_startup_logged = True

# ===== LOAD FUNCTION (Replaces original load_db) =====
def load_db():
    """
    Load data from Google Sheets
    Maintains exact same return structure as original load_db()
    Returns: {"profiles": {...}, "global_logs": [...]}
    """
    # Initialize sheets on first run
    initialize_sheets()
    
    # Log startup on first run
    log_app_startup()
    
    base_schema = {"profiles": {}, "global_logs": []}
    
    try:
        conn = get_gsheets_connection()
        
        # Read profiles from Google Sheet with caching
        df = conn.read(worksheet=WORKSHEET_PROFILES, ttl=CACHE_TTL)
        
        if df is None or df.empty:
            return base_schema
        
        # Convert DataFrame to profiles dictionary
        profiles = {}
        for _, row in df.iterrows():
            profile_name = row.get("profile_name")
            data_json = row.get("data_json")
            
            if profile_name and data_json and str(data_json).strip():
                try:
                    profile_data = json.loads(data_json)
                    
                    # Apply default values (same as original)
                    profile_data.setdefault("drift_tolerance", 5.0)
                    profile_data.setdefault("rebalance_stats", [])
                    profile_data.setdefault("last_rebalanced", None)
                    profile_data.setdefault("benchmark", None)
                    profile_data.setdefault("bank_name", "")
                    profile_data.setdefault("account_type", "")
                    profile_data.setdefault("account_name", "")
                    profile_data.setdefault("initialization_date", profile_data.get("start_date", ""))
                    profile_data.setdefault("asset_mix_locked", False)
                    
                    # Migrate assets to new schema
                    for asset_key, asset_data in profile_data.get("assets", {}).items():
                        asset_data.setdefault("fund_name", asset_key)
                        asset_data.setdefault("allocated_pct", 0.0)
                        asset_data.setdefault("purchases", [])
                    
                    profiles[profile_name] = profile_data
                    
                except json.JSONDecodeError:
                    continue
        
        return {
            "profiles": profiles,
            "global_logs": []  # Logs stored in separate sheet
        }
        
    except Exception as e:
        st.error(f"❌ Error loading data from Google Sheets: {e}")
        return base_schema

# ===== SAVE FUNCTION (Replaces original save_db) =====
def save_db(data):
    """
    Save data to Google Sheets
    Maintains exact same interface as original save_db()
    Args: data = {"profiles": {...}, "global_logs": [...]}
    """
    try:
        conn = get_gsheets_connection()
        
        # Extract profiles
        profiles = data.get("profiles", {})
        
        # Convert profiles to DataFrame rows
        rows = []
        for profile_name, profile_data in profiles.items():
            rows.append({
                "profile_name": profile_name,
                "data_json": json.dumps(profile_data, default=str),
                "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Create DataFrame
        df = pd.DataFrame(rows)
        
        # Write to Google Sheets
        conn.update(worksheet=WORKSHEET_PROFILES, data=df)
        
        # Clear cache to ensure fresh reads
        # Force reload on next read
        st.cache_data.clear()
        
        return True
        
    except Exception as e:
        st.error(f"❌ Error saving data to Google Sheets: {e}")
        return False

# ===== HELPER FUNCTIONS =====
def get_app_logs(limit=100):
    """
    Get app launch logs from Google Sheet
    """
    try:
        conn = get_gsheets_connection()
        logs_df = conn.read(worksheet=WORKSHEET_LOGS, ttl=60)
        
        if logs_df is None or logs_df.empty:
            return pd.DataFrame(columns=["timestamp", "event", "details", "session_id"])
        
        return logs_df.tail(limit)
        
    except Exception as e:
        st.warning(f"⚠️ Could not load logs: {e}")
        return pd.DataFrame(columns=["timestamp", "event", "details", "session_id"])

def clear_cache():
    """
    Clear Google Sheets cache
    Useful for debugging or forcing fresh data
    """
    st.cache_data.clear()
    st.cache_resource.clear()

# ===== STATUS FUNCTIONS =====
def get_connection_status():
    """
    Check Google Sheets connection status
    Returns: dict with status info
    """
    try:
        conn = get_gsheets_connection()
        # Try a simple read
        df = conn.read(worksheet=WORKSHEET_PROFILES, ttl=0)
        return {
            "connected": True,
            "message": "✅ Connected to Google Sheets",
            "sheet_name": "InvestLongTermStrategyTool Database"
        }
    except Exception as e:
        return {
            "connected": False,
            "message": f"❌ Connection failed: {e}",
            "sheet_name": None
        }
