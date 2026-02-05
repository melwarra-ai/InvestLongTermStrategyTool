-- =====================================================
-- AlphaStream Wealth Master - SQLite Database Schema
-- Version: 8.0.0
-- Date: 2026-02-05
-- =====================================================
-- 
-- This schema provides a normalized relational database structure
-- to replace the nested JSON/Google Sheets storage system.
--
-- Design Principles:
-- 1. Normalized to 3NF to eliminate redundancy
-- 2. Uses INTEGER PRIMARY KEY for auto-increment (SQLite best practice)
-- 3. Comprehensive foreign keys for referential integrity
-- 4. Indexes on frequently queried columns
-- 5. Future-proof for strategy versioning and stock splits
-- =====================================================

-- Enable foreign key constraints (must be set per connection)
PRAGMA foreign_keys = ON;

-- =====================================================
-- METADATA TABLE
-- Tracks database version and save history
-- =====================================================
CREATE TABLE IF NOT EXISTS metadata (
    id INTEGER PRIMARY KEY CHECK (id = 1),  -- Only one row allowed
    version INTEGER NOT NULL DEFAULT 1,
    last_save_timestamp TEXT NOT NULL,
    last_save_by TEXT NOT NULL,
    save_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    schema_version TEXT NOT NULL DEFAULT '8.0.0'
);

-- Insert initial metadata row
INSERT OR IGNORE INTO metadata (id, version, last_save_timestamp, last_save_by, save_count)
VALUES (1, 1, datetime('now'), 'system', 0);

-- =====================================================
-- USERS TABLE
-- Core user authentication and profile information
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL COLLATE NOCASE,
    email TEXT UNIQUE NOT NULL COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    password_salt TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    display_name TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_login TEXT,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    failed_login_attempts INTEGER NOT NULL DEFAULT 0,
    account_locked_until TEXT,
    session_token TEXT,
    session_expires_at TEXT
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_session_token ON users(session_token);

-- =====================================================
-- USER SETTINGS TABLE
-- User-specific preferences and notification settings
-- =====================================================
CREATE TABLE IF NOT EXISTS user_settings (
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    email_rebalance_alerts INTEGER NOT NULL DEFAULT 1 CHECK (email_rebalance_alerts IN (0, 1)),
    email_rebalance_confirmation INTEGER NOT NULL DEFAULT 1 CHECK (email_rebalance_confirmation IN (0, 1)),
    email_deployment_alerts INTEGER NOT NULL DEFAULT 0 CHECK (email_deployment_alerts IN (0, 1)),
    preferred_currency TEXT DEFAULT 'USD' CHECK (preferred_currency IN ('USD', 'CAD')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX idx_user_settings_user ON user_settings(user_id);

-- =====================================================
-- GLOBAL SETTINGS TABLE
-- Application-wide configuration
-- =====================================================
CREATE TABLE IF NOT EXISTS global_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),  -- Only one row allowed
    allow_registration INTEGER NOT NULL DEFAULT 1 CHECK (allow_registration IN (0, 1)),
    require_email_verification INTEGER NOT NULL DEFAULT 0 CHECK (require_email_verification IN (0, 1)),
    default_drift_tolerance REAL NOT NULL DEFAULT 5.0,
    default_growth_goal REAL NOT NULL DEFAULT 10.0,
    
    -- Email Configuration
    email_notifications_enabled INTEGER NOT NULL DEFAULT 0 CHECK (email_notifications_enabled IN (0, 1)),
    smtp_server TEXT DEFAULT 'smtp.gmail.com',
    smtp_port INTEGER DEFAULT 587,
    smtp_username TEXT,
    smtp_password TEXT,  -- Should be encrypted
    smtp_from_name TEXT DEFAULT 'AlphaStream Portfolio',
    
    -- AI Assistant Configuration
    ai_assistant_enabled INTEGER NOT NULL DEFAULT 1 CHECK (ai_assistant_enabled IN (0, 1)),
    ai_assistant_api_key TEXT,  -- Should be encrypted
    
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Insert initial global settings
INSERT OR IGNORE INTO global_settings (id) VALUES (1);

-- =====================================================
-- PORTFOLIOS TABLE
-- User portfolios (formerly "profiles")
-- =====================================================
CREATE TABLE IF NOT EXISTS portfolios (
    portfolio_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    portfolio_name TEXT NOT NULL,
    
    -- Portfolio Configuration
    principal REAL NOT NULL DEFAULT 0.0,
    start_date TEXT NOT NULL,
    inception_date TEXT,
    currency TEXT NOT NULL DEFAULT 'USD' CHECK (currency IN ('USD', 'CAD')),
    
    -- Goals and Thresholds
    yearly_goal_pct REAL NOT NULL DEFAULT 10.0,
    drift_threshold REAL NOT NULL DEFAULT 5.0,
    
    -- Status
    asset_mix_locked INTEGER NOT NULL DEFAULT 0 CHECK (asset_mix_locked IN (0, 1)),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    
    -- Timestamps
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_rebalanced TEXT,
    
    -- Ensure unique portfolio names per user
    UNIQUE(user_id, portfolio_name),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_portfolios_user ON portfolios(user_id);
CREATE INDEX idx_portfolios_active ON portfolios(is_active);
CREATE INDEX idx_portfolios_user_name ON portfolios(user_id, portfolio_name);

-- =====================================================
-- PORTFOLIO BENCHMARKS TABLE
-- Benchmark tickers for portfolio comparison
-- =====================================================
CREATE TABLE IF NOT EXISTS portfolio_benchmarks (
    benchmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    ticker TEXT NOT NULL,
    added_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(portfolio_id, ticker),
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id) ON DELETE CASCADE
);

CREATE INDEX idx_benchmarks_portfolio ON portfolio_benchmarks(portfolio_id);

-- =====================================================
-- ASSETS TABLE
-- Assets held in portfolios with target allocations
-- =====================================================
CREATE TABLE IF NOT EXISTS assets (
    asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    ticker TEXT NOT NULL COLLATE NOCASE,
    fund_name TEXT,
    
    -- Allocation
    target_pct REAL NOT NULL CHECK (target_pct >= 0 AND target_pct <= 100),
    current_units REAL NOT NULL DEFAULT 0.0 CHECK (current_units >= 0),
    allocated_pct REAL NOT NULL DEFAULT 0.0 CHECK (allocated_pct >= 0 AND allocated_pct <= 100),
    
    -- Timestamps
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    -- Ensure unique tickers per portfolio
    UNIQUE(portfolio_id, ticker),
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id) ON DELETE CASCADE
);

CREATE INDEX idx_assets_portfolio ON assets(portfolio_id);
CREATE INDEX idx_assets_ticker ON assets(ticker);
CREATE INDEX idx_assets_portfolio_ticker ON assets(portfolio_id, ticker);

-- =====================================================
-- PURCHASES TABLE
-- Asset purchase history (deployment tracking)
-- =====================================================
CREATE TABLE IF NOT EXISTS purchases (
    purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    
    -- Purchase Details
    purchase_date TEXT NOT NULL,
    units REAL NOT NULL CHECK (units > 0),
    price REAL NOT NULL CHECK (price > 0),
    amount REAL NOT NULL CHECK (amount > 0),
    deploy_pct REAL NOT NULL DEFAULT 0.0 CHECK (deploy_pct >= 0 AND deploy_pct <= 100),
    
    -- Metadata
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    notes TEXT,
    
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id) ON DELETE CASCADE
);

CREATE INDEX idx_purchases_asset ON purchases(asset_id);
CREATE INDEX idx_purchases_date ON purchases(purchase_date);
CREATE INDEX idx_purchases_asset_date ON purchases(asset_id, purchase_date DESC);

-- =====================================================
-- REBALANCE LOGS TABLE
-- Portfolio rebalancing history
-- =====================================================
CREATE TABLE IF NOT EXISTS rebalance_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    
    -- Event Details
    event_timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    event_type TEXT NOT NULL DEFAULT 'rebalance' CHECK (event_type IN ('rebalance', 'deployment', 'adjustment')),
    event_description TEXT NOT NULL,
    
    -- Optional: Store structured trade data as JSON
    trades_json TEXT,  -- JSON array of trade details
    
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id) ON DELETE CASCADE
);

CREATE INDEX idx_rebalance_logs_portfolio ON rebalance_logs(portfolio_id);
CREATE INDEX idx_rebalance_logs_timestamp ON rebalance_logs(event_timestamp DESC);
CREATE INDEX idx_rebalance_logs_portfolio_time ON rebalance_logs(portfolio_id, event_timestamp DESC);

-- =====================================================
-- ACTIVITY LOGS TABLE
-- General user activity tracking
-- =====================================================
CREATE TABLE IF NOT EXISTS activity_logs (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT NOT NULL,
    
    -- Activity Details
    action TEXT NOT NULL,
    details TEXT,
    ip_address TEXT,
    
    -- Timestamp
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE INDEX idx_activity_logs_user ON activity_logs(user_id);
CREATE INDEX idx_activity_logs_timestamp ON activity_logs(created_at DESC);
CREATE INDEX idx_activity_logs_action ON activity_logs(action);

-- =====================================================
-- SYSTEM LOGS TABLE
-- System-level events and notifications
-- =====================================================
CREATE TABLE IF NOT EXISTS system_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    message TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'info' CHECK (severity IN ('debug', 'info', 'warning', 'error', 'critical')),
    user_id INTEGER,
    
    -- Timestamp
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE INDEX idx_system_logs_type ON system_logs(event_type);
CREATE INDEX idx_system_logs_timestamp ON system_logs(created_at DESC);
CREATE INDEX idx_system_logs_severity ON system_logs(severity);

-- =====================================================
-- NOTIFICATION LOGS TABLE
-- Email notification tracking
-- =====================================================
CREATE TABLE IF NOT EXISTS notification_logs (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT NOT NULL,
    
    -- Notification Details
    notification_type TEXT NOT NULL,
    subject TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('sent', 'failed', 'pending')),
    details TEXT,
    
    -- Timestamp
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_notification_logs_user ON notification_logs(user_id);
CREATE INDEX idx_notification_logs_timestamp ON notification_logs(created_at DESC);
CREATE INDEX idx_notification_logs_status ON notification_logs(status);

-- =====================================================
-- SECURITY EVENTS TABLE
-- Security-related events (failed logins, password changes, etc.)
-- =====================================================
CREATE TABLE IF NOT EXISTS security_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    username TEXT NOT NULL,
    details TEXT,
    severity TEXT NOT NULL DEFAULT 'info' CHECK (severity IN ('info', 'warning', 'critical')),
    ip_address TEXT,
    
    -- Timestamp
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_security_events_type ON security_events(event_type);
CREATE INDEX idx_security_events_username ON security_events(username);
CREATE INDEX idx_security_events_timestamp ON security_events(created_at DESC);
CREATE INDEX idx_security_events_severity ON security_events(severity);

-- =====================================================
-- PENDING REBALANCES TABLE
-- Stores pending rebalance recommendations
-- =====================================================
CREATE TABLE IF NOT EXISTS pending_rebalances (
    pending_id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    
    -- Recommendation Details
    recommendations_json TEXT NOT NULL,  -- JSON array of trade recommendations
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    expires_at TEXT,
    
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX idx_pending_rebalances_portfolio ON pending_rebalances(portfolio_id);

-- =====================================================
-- BACKUPS METADATA TABLE
-- Track database backups for restore capability
-- =====================================================
CREATE TABLE IF NOT EXISTS backups_metadata (
    backup_id INTEGER PRIMARY KEY AUTOINCREMENT,
    backup_filename TEXT NOT NULL UNIQUE,
    backup_path TEXT,
    backup_size INTEGER,
    backup_type TEXT NOT NULL DEFAULT 'manual' CHECK (backup_type IN ('manual', 'auto', 'pre_migration')),
    created_by TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    notes TEXT
);

CREATE INDEX idx_backups_timestamp ON backups_metadata(created_at DESC);
CREATE INDEX idx_backups_type ON backups_metadata(backup_type);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- Optimized read queries for frequently accessed data
-- =====================================================

-- View: Complete user profile with settings
CREATE VIEW IF NOT EXISTS v_users_complete AS
SELECT 
    u.user_id,
    u.username,
    u.email,
    u.role,
    u.display_name,
    u.created_at,
    u.last_login,
    u.is_active,
    us.email_rebalance_alerts,
    us.email_rebalance_confirmation,
    us.email_deployment_alerts,
    us.preferred_currency
FROM users u
LEFT JOIN user_settings us ON u.user_id = us.user_id;

-- View: Portfolio summary with asset counts
CREATE VIEW IF NOT EXISTS v_portfolios_summary AS
SELECT 
    p.portfolio_id,
    p.user_id,
    u.username,
    p.portfolio_name,
    p.principal,
    p.start_date,
    p.currency,
    p.yearly_goal_pct,
    p.drift_threshold,
    p.asset_mix_locked,
    p.last_rebalanced,
    COUNT(DISTINCT a.asset_id) as asset_count,
    SUM(a.current_units) as total_units,
    AVG(a.allocated_pct) as avg_allocation_pct
FROM portfolios p
INNER JOIN users u ON p.user_id = u.user_id
LEFT JOIN assets a ON p.portfolio_id = a.portfolio_id
WHERE p.is_active = 1
GROUP BY p.portfolio_id;

-- View: Asset details with purchase history
CREATE VIEW IF NOT EXISTS v_assets_with_purchases AS
SELECT 
    a.asset_id,
    a.portfolio_id,
    a.ticker,
    a.fund_name,
    a.target_pct,
    a.current_units,
    a.allocated_pct,
    COUNT(pur.purchase_id) as purchase_count,
    SUM(pur.amount) as total_invested,
    MIN(pur.purchase_date) as first_purchase_date,
    MAX(pur.purchase_date) as last_purchase_date
FROM assets a
LEFT JOIN purchases pur ON a.asset_id = pur.asset_id
GROUP BY a.asset_id;

-- =====================================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- Maintain data integrity and timestamps
-- =====================================================

-- Trigger: Update metadata on any data change
CREATE TRIGGER IF NOT EXISTS trg_update_metadata_on_change
AFTER INSERT ON portfolios
BEGIN
    UPDATE metadata 
    SET save_count = save_count + 1,
        last_save_timestamp = datetime('now'),
        version = version + 1
    WHERE id = 1;
END;

-- Trigger: Update portfolio updated_at on asset change
CREATE TRIGGER IF NOT EXISTS trg_update_portfolio_on_asset_change
AFTER UPDATE ON assets
BEGIN
    UPDATE portfolios 
    SET updated_at = datetime('now')
    WHERE portfolio_id = NEW.portfolio_id;
END;

-- Trigger: Update asset updated_at on purchase
CREATE TRIGGER IF NOT EXISTS trg_update_asset_on_purchase
AFTER INSERT ON purchases
BEGIN
    UPDATE assets 
    SET updated_at = datetime('now')
    WHERE asset_id = NEW.asset_id;
END;

-- Trigger: Recalculate asset current_units on purchase insert
CREATE TRIGGER IF NOT EXISTS trg_recalc_units_on_purchase_insert
AFTER INSERT ON purchases
BEGIN
    UPDATE assets
    SET current_units = (
        SELECT COALESCE(SUM(units), 0)
        FROM purchases
        WHERE asset_id = NEW.asset_id
    )
    WHERE asset_id = NEW.asset_id;
END;

-- Trigger: Recalculate asset current_units on purchase delete
CREATE TRIGGER IF NOT EXISTS trg_recalc_units_on_purchase_delete
AFTER DELETE ON purchases
BEGIN
    UPDATE assets
    SET current_units = (
        SELECT COALESCE(SUM(units), 0)
        FROM purchases
        WHERE asset_id = OLD.asset_id
    )
    WHERE asset_id = OLD.asset_id;
END;

-- =====================================================
-- SCHEMA COMPLETE
-- Database is ready for use
-- =====================================================
