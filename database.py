"""
=====================================================
AlphaStream Wealth Master - SQLite Database Module
Version: 8.0.0
Date: 2026-02-05
=====================================================

This module provides a comprehensive database interface for the
portfolio management application, replacing Google Sheets storage
with SQLite for improved performance and reliability.

Features:
- Connection management with proper error handling
- All CRUD operations for users, portfolios, assets, purchases
- Transaction management for data integrity
- Backup/restore functionality
- Migration support from Google Sheets
- Thread-safe operations
- Prepared statements to prevent SQL injection

Usage:
    from database import Database
    
    db = Database('portfolio.db')
    user_id = db.create_user('john', 'john@email.com', 'password')
    portfolio_id = db.create_portfolio(user_id, 'TFSA', 100000.0, '2025-01-01')
"""

import sqlite3
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union
from contextlib import contextmanager
import os
import shutil
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Custom exception for database operations"""
    pass


class Database:
    """
    SQLite database interface for portfolio management.
    
    Provides comprehensive CRUD operations and maintains backward
    compatibility with the original Google Sheets/JSON structure.
    """
    
    def __init__(self, db_path: str = 'portfolio.db', schema_file: str = 'schema.sql'):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
            schema_file: Path to SQL schema file for initialization
        """
        self.db_path = db_path
        self.schema_file = schema_file
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """Initialize database schema if it doesn't exist"""
        try:
            # Create database if it doesn't exist
            if not os.path.exists(self.db_path):
                logger.info(f"Creating new database: {self.db_path}")
                
                # Load and execute schema
                if os.path.exists(self.schema_file):
                    with self.get_connection() as conn:
                        with open(self.schema_file, 'r') as f:
                            schema_sql = f.read()
                        conn.executescript(schema_sql)
                        conn.commit()
                    logger.info("Database schema initialized successfully")
                else:
                    logger.warning(f"Schema file not found: {self.schema_file}")
                    # Create tables programmatically if schema file missing
                    self._create_tables_programmatically()
            else:
                logger.info(f"Using existing database: {self.db_path}")
                # Ensure foreign keys are enabled
                with self.get_connection() as conn:
                    conn.execute("PRAGMA foreign_keys = ON")
        
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise DatabaseError(f"Database initialization failed: {e}")
    
    def _create_tables_programmatically(self) -> None:
        """
        Create essential tables programmatically if schema.sql is missing.
        This is a fallback method.
        """
        with self.get_connection() as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            
            # Create minimal required tables
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS metadata (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    version INTEGER NOT NULL DEFAULT 1,
                    last_save_timestamp TEXT NOT NULL,
                    last_save_by TEXT NOT NULL,
                    save_count INTEGER NOT NULL DEFAULT 0,
                    schema_version TEXT NOT NULL DEFAULT '8.0.0'
                );
                INSERT OR IGNORE INTO metadata VALUES (1, 1, datetime('now'), 'system', 0, '8.0.0');
                
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    password_salt TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user',
                    is_active INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL DEFAULT (datetime('now'))
                );
            """)
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        Ensures proper connection handling and cleanup.
        
        Usage:
            with db.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM users")
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise DatabaseError(f"Database operation failed: {e}")
        finally:
            if conn:
                conn.close()
    
    # =====================================================
    # METADATA OPERATIONS
    # =====================================================
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get database metadata"""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM metadata WHERE id = 1")
            row = cursor.fetchone()
            if row:
                return dict(row)
            return {}
    
    def update_metadata(self, username: str = "system") -> None:
        """Update metadata after data changes"""
        with self.get_connection() as conn:
            conn.execute("""
                UPDATE metadata 
                SET version = version + 1,
                    save_count = save_count + 1,
                    last_save_timestamp = datetime('now'),
                    last_save_by = ?
                WHERE id = 1
            """, (username,))
            conn.commit()
    
    # =====================================================
    # USER OPERATIONS
    # =====================================================
    
    def create_user(self, username: str, email: str, password: str, 
                   role: str = 'user', display_name: str = None) -> int:
        """
        Create a new user account.
        
        Args:
            username: Unique username
            email: User email address
            password: Plain text password (will be hashed)
            role: User role ('user' or 'admin')
            display_name: Optional display name
            
        Returns:
            user_id of created user
            
        Raises:
            DatabaseError: If user already exists or creation fails
        """
        # Hash password
        salt = secrets.token_hex(32)
        password_hash = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
        
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO users (username, email, password_hash, password_salt, role, display_name)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (username, email, password_hash, salt, role, display_name))
                
                user_id = cursor.lastrowid
                
                # Create default user settings
                conn.execute("""
                    INSERT INTO user_settings (user_id)
                    VALUES (?)
                """, (user_id,))
                
                conn.commit()
                logger.info(f"Created user: {username} (ID: {user_id})")
                return user_id
        
        except sqlite3.IntegrityError as e:
            raise DatabaseError(f"User '{username}' or email '{email}' already exists")
        except Exception as e:
            raise DatabaseError(f"Failed to create user: {e}")
    
    def authenticate_user(self, username: str, password: str) -> Optional[int]:
        """
        Authenticate user credentials.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            user_id if authentication successful, None otherwise
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT user_id, password_hash, password_salt, is_active 
                FROM users 
                WHERE username = ?
            """, (username,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            if not row['is_active']:
                logger.warning(f"Inactive user login attempt: {username}")
                return None
            
            # Verify password
            password_hash = hashlib.sha256(f"{password}{row['password_salt']}".encode()).hexdigest()
            
            if secrets.compare_digest(password_hash, row['password_hash']):
                # Update last login
                conn.execute("""
                    UPDATE users 
                    SET last_login = datetime('now'),
                        failed_login_attempts = 0
                    WHERE user_id = ?
                """, (row['user_id'],))
                conn.commit()
                
                logger.info(f"User authenticated: {username}")
                return row['user_id']
            else:
                # Increment failed attempts
                conn.execute("""
                    UPDATE users 
                    SET failed_login_attempts = failed_login_attempts + 1
                    WHERE user_id = ?
                """, (row['user_id'],))
                conn.commit()
                
                logger.warning(f"Failed login attempt for: {username}")
                return None
    
    def get_user(self, user_id: int = None, username: str = None) -> Optional[Dict[str, Any]]:
        """
        Get user by ID or username.
        
        Args:
            user_id: User ID
            username: Username (alternative to user_id)
            
        Returns:
            User dict or None if not found
        """
        with self.get_connection() as conn:
            if user_id:
                cursor = conn.execute("SELECT * FROM v_users_complete WHERE user_id = ?", (user_id,))
            elif username:
                cursor = conn.execute("SELECT * FROM v_users_complete WHERE username = ?", (username,))
            else:
                raise ValueError("Must provide user_id or username")
            
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM v_users_complete ORDER BY username")
            return [dict(row) for row in cursor.fetchall()]
    
    def update_user_settings(self, user_id: int, settings: Dict[str, Any]) -> None:
        """
        Update user settings.
        
        Args:
            user_id: User ID
            settings: Dict of settings to update
        """
        allowed_fields = {
            'email_rebalance_alerts', 
            'email_rebalance_confirmation',
            'email_deployment_alerts',
            'preferred_currency'
        }
        
        # Filter to allowed fields only
        update_fields = {k: v for k, v in settings.items() if k in allowed_fields}
        
        if not update_fields:
            return
        
        set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
        values = list(update_fields.values()) + [user_id]
        
        with self.get_connection() as conn:
            conn.execute(f"""
                UPDATE user_settings 
                SET {set_clause}, updated_at = datetime('now')
                WHERE user_id = ?
            """, values)
            conn.commit()
    
    def change_password(self, user_id: int, new_password: str) -> None:
        """Change user password"""
        salt = secrets.token_hex(32)
        password_hash = hashlib.sha256(f"{new_password}{salt}".encode()).hexdigest()
        
        with self.get_connection() as conn:
            conn.execute("""
                UPDATE users 
                SET password_hash = ?, password_salt = ?
                WHERE user_id = ?
            """, (password_hash, salt, user_id))
            conn.commit()
    
    # =====================================================
    # PORTFOLIO OPERATIONS
    # =====================================================
    
    def create_portfolio(self, user_id: int, portfolio_name: str, principal: float,
                        start_date: str, currency: str = 'USD', 
                        yearly_goal_pct: float = 10.0, drift_threshold: float = 5.0,
                        inception_date: str = None) -> int:
        """
        Create a new portfolio.
        
        Args:
            user_id: Owner user ID
            portfolio_name: Portfolio name (unique per user)
            principal: Initial investment amount
            start_date: Portfolio start date (YYYY-MM-DD)
            currency: 'USD' or 'CAD'
            yearly_goal_pct: Yearly return goal percentage
            drift_threshold: Drift threshold for rebalancing alerts
            inception_date: Optional inception date
            
        Returns:
            portfolio_id of created portfolio
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO portfolios 
                    (user_id, portfolio_name, principal, start_date, inception_date,
                     currency, yearly_goal_pct, drift_threshold)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, portfolio_name, principal, start_date, inception_date,
                      currency, yearly_goal_pct, drift_threshold))
                
                portfolio_id = cursor.lastrowid
                conn.commit()
                self.update_metadata()
                
                logger.info(f"Created portfolio: {portfolio_name} (ID: {portfolio_id})")
                return portfolio_id
        
        except sqlite3.IntegrityError:
            raise DatabaseError(f"Portfolio '{portfolio_name}' already exists for this user")
        except Exception as e:
            raise DatabaseError(f"Failed to create portfolio: {e}")
    
    def get_portfolios(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get all portfolios for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of portfolio dicts
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM v_portfolios_summary 
                WHERE user_id = ? 
                ORDER BY portfolio_name
            """, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_portfolio(self, portfolio_id: int) -> Optional[Dict[str, Any]]:
        """Get single portfolio by ID"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM portfolios WHERE portfolio_id = ?
            """, (portfolio_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_portfolio_by_name(self, user_id: int, portfolio_name: str) -> Optional[Dict[str, Any]]:
        """Get portfolio by user and name"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM portfolios 
                WHERE user_id = ? AND portfolio_name = ?
            """, (user_id, portfolio_name))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_portfolio(self, portfolio_id: int, updates: Dict[str, Any]) -> None:
        """
        Update portfolio fields.
        
        Args:
            portfolio_id: Portfolio ID
            updates: Dict of fields to update
        """
        allowed_fields = {
            'portfolio_name', 'principal', 'start_date', 'inception_date',
            'currency', 'yearly_goal_pct', 'drift_threshold', 
            'asset_mix_locked', 'last_rebalanced', 'is_active'
        }
        
        update_fields = {k: v for k, v in updates.items() if k in allowed_fields}
        
        if not update_fields:
            return
        
        set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
        values = list(update_fields.values()) + [portfolio_id]
        
        with self.get_connection() as conn:
            conn.execute(f"""
                UPDATE portfolios 
                SET {set_clause}, updated_at = datetime('now')
                WHERE portfolio_id = ?
            """, values)
            conn.commit()
            self.update_metadata()
    
    def lock_portfolio(self, portfolio_id: int, locked: bool = True) -> None:
        """Lock or unlock portfolio asset mix"""
        with self.get_connection() as conn:
            conn.execute("""
                UPDATE portfolios 
                SET asset_mix_locked = ?, updated_at = datetime('now')
                WHERE portfolio_id = ?
            """, (1 if locked else 0, portfolio_id))
            conn.commit()
    
    def delete_portfolio(self, portfolio_id: int) -> None:
        """Delete portfolio (cascades to assets, purchases, logs)"""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM portfolios WHERE portfolio_id = ?", (portfolio_id,))
            conn.commit()
            self.update_metadata()
            logger.info(f"Deleted portfolio ID: {portfolio_id}")
    
    # =====================================================
    # BENCHMARK OPERATIONS
    # =====================================================
    
    def add_benchmark(self, portfolio_id: int, ticker: str) -> None:
        """Add benchmark ticker to portfolio"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO portfolio_benchmarks (portfolio_id, ticker)
                    VALUES (?, ?)
                """, (portfolio_id, ticker.upper()))
                conn.commit()
        except sqlite3.IntegrityError:
            logger.warning(f"Benchmark {ticker} already exists for portfolio {portfolio_id}")
    
    def get_benchmarks(self, portfolio_id: int) -> List[str]:
        """Get all benchmark tickers for a portfolio"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT ticker FROM portfolio_benchmarks 
                WHERE portfolio_id = ?
                ORDER BY ticker
            """, (portfolio_id,))
            return [row['ticker'] for row in cursor.fetchall()]
    
    def remove_benchmark(self, portfolio_id: int, ticker: str) -> None:
        """Remove benchmark from portfolio"""
        with self.get_connection() as conn:
            conn.execute("""
                DELETE FROM portfolio_benchmarks 
                WHERE portfolio_id = ? AND ticker = ?
            """, (portfolio_id, ticker.upper()))
            conn.commit()
    
    # =====================================================
    # ASSET OPERATIONS
    # =====================================================
    
    def add_asset(self, portfolio_id: int, ticker: str, fund_name: str,
                 target_pct: float, allocated_pct: float = 0.0) -> int:
        """
        Add asset to portfolio.
        
        Args:
            portfolio_id: Portfolio ID
            ticker: Asset ticker symbol
            fund_name: Full fund name
            target_pct: Target allocation percentage
            allocated_pct: Current allocated percentage
            
        Returns:
            asset_id of created asset
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO assets 
                    (portfolio_id, ticker, fund_name, target_pct, allocated_pct)
                    VALUES (?, ?, ?, ?, ?)
                """, (portfolio_id, ticker.upper(), fund_name, target_pct, allocated_pct))
                
                asset_id = cursor.lastrowid
                conn.commit()
                self.update_metadata()
                
                logger.info(f"Added asset: {ticker} to portfolio {portfolio_id}")
                return asset_id
        
        except sqlite3.IntegrityError:
            raise DatabaseError(f"Asset '{ticker}' already exists in this portfolio")
    
    def get_assets(self, portfolio_id: int) -> List[Dict[str, Any]]:
        """Get all assets for a portfolio"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM assets 
                WHERE portfolio_id = ?
                ORDER BY ticker
            """, (portfolio_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_asset(self, asset_id: int) -> Optional[Dict[str, Any]]:
        """Get single asset by ID"""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM assets WHERE asset_id = ?", (asset_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_asset_by_ticker(self, portfolio_id: int, ticker: str) -> Optional[Dict[str, Any]]:
        """Get asset by portfolio and ticker"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM assets 
                WHERE portfolio_id = ? AND ticker = ?
            """, (portfolio_id, ticker.upper()))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_asset(self, asset_id: int, updates: Dict[str, Any]) -> None:
        """Update asset fields"""
        allowed_fields = {'fund_name', 'target_pct', 'current_units', 'allocated_pct'}
        update_fields = {k: v for k, v in updates.items() if k in allowed_fields}
        
        if not update_fields:
            return
        
        set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
        values = list(update_fields.values()) + [asset_id]
        
        with self.get_connection() as conn:
            conn.execute(f"""
                UPDATE assets 
                SET {set_clause}, updated_at = datetime('now')
                WHERE asset_id = ?
            """, values)
            conn.commit()
            self.update_metadata()
    
    def delete_asset(self, asset_id: int) -> None:
        """Delete asset (cascades to purchases)"""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM assets WHERE asset_id = ?", (asset_id,))
            conn.commit()
            self.update_metadata()
    
    # =====================================================
    # PURCHASE OPERATIONS
    # =====================================================
    
    def add_purchase(self, asset_id: int, purchase_date: str, units: float,
                    price: float, amount: float, deploy_pct: float = 0.0,
                    notes: str = None) -> int:
        """
        Record an asset purchase.
        
        Args:
            asset_id: Asset ID
            purchase_date: Purchase date (YYYY-MM-DD)
            units: Number of units purchased
            price: Price per unit
            amount: Total purchase amount
            deploy_pct: Deployment percentage
            notes: Optional notes
            
        Returns:
            purchase_id
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO purchases 
                (asset_id, purchase_date, units, price, amount, deploy_pct, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (asset_id, purchase_date, units, price, amount, deploy_pct, notes))
            
            purchase_id = cursor.lastrowid
            conn.commit()
            self.update_metadata()
            
            logger.info(f"Added purchase: {units} units @ ${price} for asset {asset_id}")
            return purchase_id
    
    def get_purchases(self, asset_id: int) -> List[Dict[str, Any]]:
        """Get all purchases for an asset"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM purchases 
                WHERE asset_id = ?
                ORDER BY purchase_date DESC
            """, (asset_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_all_purchases_for_portfolio(self, portfolio_id: int) -> List[Dict[str, Any]]:
        """Get all purchases across all assets in a portfolio"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT p.*, a.ticker, a.fund_name
                FROM purchases p
                JOIN assets a ON p.asset_id = a.asset_id
                WHERE a.portfolio_id = ?
                ORDER BY p.purchase_date DESC
            """, (portfolio_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_purchase(self, purchase_id: int) -> None:
        """Delete a purchase (triggers will update asset units)"""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM purchases WHERE purchase_id = ?", (purchase_id,))
            conn.commit()
            self.update_metadata()
    
    # =====================================================
    # REBALANCE LOG OPERATIONS
    # =====================================================
    
    def add_rebalance_log(self, portfolio_id: int, event_description: str,
                         event_type: str = 'rebalance', trades_json: str = None) -> int:
        """Add rebalance log entry"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO rebalance_logs 
                (portfolio_id, event_type, event_description, trades_json)
                VALUES (?, ?, ?, ?)
            """, (portfolio_id, event_type, event_description, trades_json))
            
            log_id = cursor.lastrowid
            conn.commit()
            return log_id
    
    def get_rebalance_logs(self, portfolio_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get rebalance logs for a portfolio"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM rebalance_logs 
                WHERE portfolio_id = ?
                ORDER BY event_timestamp DESC
                LIMIT ?
            """, (portfolio_id, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    # =====================================================
    # LOGGING OPERATIONS
    # =====================================================
    
    def log_activity(self, username: str, action: str, details: str = "",
                    ip_address: str = "", user_id: int = None) -> None:
        """Log user activity"""
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO activity_logs (user_id, username, action, details, ip_address)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, username, action, details, ip_address))
            conn.commit()
    
    def log_system_event(self, event_type: str, message: str, 
                        severity: str = 'info', user_id: int = None) -> None:
        """Log system event"""
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO system_logs (event_type, message, severity, user_id)
                VALUES (?, ?, ?, ?)
            """, (event_type, message, severity, user_id))
            conn.commit()
    
    def log_notification(self, user_id: int, username: str, notification_type: str,
                        subject: str, status: str, details: str = "") -> None:
        """Log email notification"""
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO notification_logs 
                (user_id, username, notification_type, subject, status, details)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, username, notification_type, subject, status, details))
            conn.commit()
    
    def log_security_event(self, event_type: str, username: str, details: str = "",
                          severity: str = 'info', ip_address: str = "") -> None:
        """Log security event"""
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO security_events 
                (event_type, username, details, severity, ip_address)
                VALUES (?, ?, ?, ?, ?)
            """, (event_type, username, details, severity, ip_address))
            conn.commit()
    
    # =====================================================
    # GLOBAL SETTINGS OPERATIONS
    # =====================================================
    
    def get_global_settings(self) -> Dict[str, Any]:
        """Get global application settings"""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM global_settings WHERE id = 1")
            row = cursor.fetchone()
            return dict(row) if row else {}
    
    def update_global_settings(self, settings: Dict[str, Any]) -> None:
        """Update global settings"""
        allowed_fields = {
            'allow_registration', 'require_email_verification',
            'default_drift_tolerance', 'default_growth_goal',
            'email_notifications_enabled', 'smtp_server', 'smtp_port',
            'smtp_username', 'smtp_password', 'smtp_from_name',
            'ai_assistant_enabled', 'ai_assistant_api_key'
        }
        
        update_fields = {k: v for k, v in settings.items() if k in allowed_fields}
        
        if not update_fields:
            return
        
        set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
        values = list(update_fields.values())
        
        with self.get_connection() as conn:
            conn.execute(f"""
                UPDATE global_settings 
                SET {set_clause}, updated_at = datetime('now')
                WHERE id = 1
            """, values)
            conn.commit()
    
    # =====================================================
    # PENDING REBALANCE OPERATIONS
    # =====================================================
    
    def store_pending_rebalance(self, portfolio_id: int, recommendations_json: str) -> None:
        """Store pending rebalance recommendations"""
        with self.get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO pending_rebalances 
                (portfolio_id, recommendations_json, expires_at)
                VALUES (?, ?, datetime('now', '+7 days'))
            """, (portfolio_id, recommendations_json))
            conn.commit()
    
    def get_pending_rebalance(self, portfolio_id: int) -> Optional[Dict[str, Any]]:
        """Get pending rebalance for portfolio"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM pending_rebalances 
                WHERE portfolio_id = ?
            """, (portfolio_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def clear_pending_rebalance(self, portfolio_id: int) -> None:
        """Clear pending rebalance"""
        with self.get_connection() as conn:
            conn.execute("""
                DELETE FROM pending_rebalances WHERE portfolio_id = ?
            """, (portfolio_id,))
            conn.commit()
    
    # =====================================================
    # ANALYTICS OPERATIONS
    # =====================================================
    
    def get_analytics_data(self) -> Dict[str, Any]:
        """
        Get comprehensive analytics data for admin dashboard.
        Replaces the get_analytics_data function from the original app.
        """
        with self.get_connection() as conn:
            # Total users
            total_users = conn.execute("SELECT COUNT(*) FROM users WHERE is_active = 1").fetchone()[0]
            
            # Total portfolios
            total_portfolios = conn.execute("SELECT COUNT(*) FROM portfolios WHERE is_active = 1").fetchone()[0]
            
            # Recent activity count
            activity_24h = conn.execute("""
                SELECT COUNT(*) FROM activity_logs 
                WHERE created_at >= datetime('now', '-1 day')
            """).fetchone()[0]
            
            # Failed logins
            failed_logins_24h = conn.execute("""
                SELECT COUNT(*) FROM security_events 
                WHERE event_type = 'failed_login' 
                AND created_at >= datetime('now', '-1 day')
            """).fetchone()[0]
            
            return {
                'total_users': total_users,
                'total_portfolios': total_portfolios,
                'activity_24h': activity_24h,
                'failed_logins_24h': failed_logins_24h
            }
    
    # =====================================================
    # BACKUP OPERATIONS
    # =====================================================
    
    def create_backup(self, backup_dir: str = 'backups', 
                     backup_type: str = 'manual', 
                     created_by: str = 'system',
                     notes: str = None) -> str:
        """
        Create database backup.
        
        Args:
            backup_dir: Directory to store backups
            backup_type: 'manual', 'auto', or 'pre_migration'
            created_by: Username who created backup
            notes: Optional backup notes
            
        Returns:
            Path to backup file
        """
        # Create backup directory if it doesn't exist
        Path(backup_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"portfolio_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        try:
            # Copy database file
            shutil.copy2(self.db_path, backup_path)
            
            # Get file size
            backup_size = os.path.getsize(backup_path)
            
            # Record backup in metadata table
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO backups_metadata 
                    (backup_filename, backup_path, backup_size, backup_type, created_by, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (backup_filename, backup_path, backup_size, backup_type, created_by, notes))
                conn.commit()
            
            logger.info(f"Created backup: {backup_path} ({backup_size} bytes)")
            return backup_path
        
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            raise DatabaseError(f"Failed to create backup: {e}")
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all backups"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM backups_metadata 
                ORDER BY created_at DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def restore_from_backup(self, backup_path: str) -> None:
        """
        Restore database from backup.
        
        Args:
            backup_path: Path to backup file
        
        Warning: This will replace the current database!
        """
        if not os.path.exists(backup_path):
            raise DatabaseError(f"Backup file not found: {backup_path}")
        
        try:
            # Create safety backup of current database
            safety_backup = self.create_backup(backup_type='auto', 
                                             created_by='system',
                                             notes='Pre-restore safety backup')
            
            # Replace current database with backup
            shutil.copy2(backup_path, self.db_path)
            
            logger.info(f"Restored database from: {backup_path}")
            logger.info(f"Safety backup created: {safety_backup}")
        
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            raise DatabaseError(f"Failed to restore from backup: {e}")


# =====================================================
# UTILITY FUNCTIONS FOR BACKWARD COMPATIBILITY
# =====================================================

def export_to_json_format(db: Database, username: str) -> Dict[str, Any]:
    """
    Export database to original JSON/Google Sheets format.
    Useful for backward compatibility and migration testing.
    
    Args:
        db: Database instance
        username: Username to export (or 'all' for all users)
        
    Returns:
        Dict in original nested format
    """
    result = {
        "metadata": db.get_metadata(),
        "users": {},
        "global_settings": db.get_global_settings(),
        "system_logs": []
    }
    
    # Get users to export
    if username == 'all':
        users = db.get_all_users()
    else:
        user = db.get_user(username=username)
        users = [user] if user else []
    
    # Build nested structure
    for user in users:
        user_data = {
            "password": user['password_hash'],
            "salt": user['password_salt'],
            "email": user['email'],
            "role": user['role'],
            "settings": {
                "email_rebalance_alerts": bool(user.get('email_rebalance_alerts', 1)),
                "email_rebalance_confirmation": bool(user.get('email_rebalance_confirmation', 1))
            },
            "profiles": {}
        }
        
        # Get portfolios for user
        portfolios = db.get_portfolios(user['user_id'])
        
        for portfolio in portfolios:
            portfolio_data = {
                "principal": portfolio['principal'],
                "start_date": portfolio['start_date'],
                "inception_date": portfolio.get('inception_date'),
                "currency": portfolio['currency'],
                "yearly_goal_pct": portfolio['yearly_goal_pct'],
                "drift_threshold": portfolio['drift_threshold'],
                "asset_mix_locked": bool(portfolio['asset_mix_locked']),
                "last_rebalanced": portfolio.get('last_rebalanced'),
                "benchmarks": db.get_benchmarks(portfolio['portfolio_id']),
                "assets": {},
                "rebalance_stats": []
            }
            
            # Get assets
            assets = db.get_assets(portfolio['portfolio_id'])
            for asset in assets:
                asset_data = {
                    "fund_name": asset['fund_name'],
                    "target": asset['target_pct'],
                    "units": asset['current_units'],
                    "allocated_pct": asset['allocated_pct'],
                    "purchases": []
                }
                
                # Get purchases
                purchases = db.get_purchases(asset['asset_id'])
                for purchase in purchases:
                    asset_data["purchases"].append({
                        "date": purchase['purchase_date'],
                        "units": purchase['units'],
                        "price": purchase['price'],
                        "amount": purchase['amount'],
                        "deploy_pct": purchase['deploy_pct']
                    })
                
                portfolio_data["assets"][asset['ticker']] = asset_data
            
            # Get rebalance logs
            logs = db.get_rebalance_logs(portfolio['portfolio_id'])
            portfolio_data["rebalance_stats"] = [
                f"{log['event_timestamp']} - {log['event_description']}" 
                for log in logs
            ]
            
            user_data["profiles"][portfolio['portfolio_name']] = portfolio_data
        
        result["users"][user['username']] = user_data
    
    return result


# =====================================================
# MODULE INITIALIZATION
# =====================================================

if __name__ == "__main__":
    # Test database initialization
    print("Testing Database Module...")
    
    db = Database('test_portfolio.db')
    print(f"✓ Database initialized: {db.db_path}")
    
    metadata = db.get_metadata()
    print(f"✓ Metadata: version {metadata.get('version')}, schema {metadata.get('schema_version')}")
    
    print("\n✓ Database module ready for use!")
