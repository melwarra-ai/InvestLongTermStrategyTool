"""
AlphaStream Wealth Master - Backup Module
Version: 8.0.0
Date: 2026-02-05

Automated backup functionality for SQLite database with Google Drive integration.
See full documentation in README.md
"""

import os
import shutil
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
import logging
import json
import hashlib

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
    from google.oauth2.service_account import Credentials
    import io
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False

import database as db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BACKUP_DIR = "backups"
Path(BACKUP_DIR).mkdir(exist_ok=True)
MAX_LOCAL_BACKUPS = 30
GDRIVE_FOLDER_NAME = "AlphaStream_Backups"
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

def create_local_backup(backup_name: Optional[str] = None) -> Tuple[bool, str, str]:
    """Create local database backup"""
    try:
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.db"
        
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        
        source_conn = db.get_connection()
        backup_conn = sqlite3.connect(backup_path)
        
        with backup_conn:
            source_conn.backup(backup_conn)
        
        backup_conn.close()
        
        file_size = os.path.getsize(backup_path)
        file_size_mb = file_size / (1024 * 1024)
        
        logger.info(f"Backup created: {backup_path} ({file_size_mb:.2f} MB)")
        
        db.update_system_settings(last_backup_date=datetime.now().isoformat())
        cleanup_old_backups()
        
        return True, f"Backup created ({file_size_mb:.2f} MB)", backup_path
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        return False, str(e), ""

def cleanup_old_backups(max_backups: int = MAX_LOCAL_BACKUPS):
    """Remove old backups"""
    try:
        backup_files = []
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith("backup_") and filename.endswith(".db"):
                filepath = os.path.join(BACKUP_DIR, filename)
                mtime = os.path.getmtime(filepath)
                backup_files.append((filepath, mtime))
        
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        for filepath, _ in backup_files[max_backups:]:
            try:
                os.remove(filepath)
                logger.info(f"Removed old backup: {os.path.basename(filepath)}")
            except Exception as e:
                logger.error(f"Failed to remove {filepath}: {e}")
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")

def list_local_backups() -> List[Dict[str, Any]]:
    """List all local backups"""
    backups = []
    try:
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith("backup_") and filename.endswith(".db"):
                filepath = os.path.join(BACKUP_DIR, filename)
                file_size = os.path.getsize(filepath)
                mtime = os.path.getmtime(filepath)
                
                backups.append({
                    'filename': filename,
                    'filepath': filepath,
                    'size_mb': round(file_size / (1024 * 1024), 2),
                    'modified_date': datetime.fromtimestamp(mtime).isoformat()
                })
        
        backups.sort(key=lambda x: x['modified_date'], reverse=True)
    except Exception as e:
        logger.error(f"Failed to list backups: {e}")
    
    return backups

def restore_from_backup(backup_path: str, verify: bool = True) -> Tuple[bool, str]:
    """Restore database from backup"""
    try:
        if not os.path.exists(backup_path):
            return False, f"Backup file not found: {backup_path}"
        
        if verify:
            is_valid, error = verify_backup(backup_path)
            if not is_valid:
                return False, f"Backup verification failed: {error}"
        
        current_backup = os.path.join(BACKUP_DIR, f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        if os.path.exists(db.DB_FILE):
            shutil.copy2(db.DB_FILE, current_backup)
        
        db.close_connection()
        shutil.copy2(backup_path, db.DB_FILE)
        
        logger.info(f"Database restored from: {backup_path}")
        return True, "Database restored successfully"
    except Exception as e:
        logger.error(f"Restore failed: {e}")
        return False, str(e)

def verify_backup(backup_path: str) -> Tuple[bool, str]:
    """Verify backup integrity"""
    try:
        conn = sqlite3.connect(backup_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()[0]
        conn.close()
        
        if result == "ok":
            return True, ""
        else:
            return False, f"Integrity check failed: {result}"
    except Exception as e:
        return False, str(e)

def should_create_backup(frequency_hours: int = 24) -> bool:
    """Check if backup is needed"""
    try:
        settings = db.get_system_settings()
        last_backup_str = settings.get('last_backup_date')
        
        if not last_backup_str:
            return True
        
        last_backup = datetime.fromisoformat(last_backup_str)
        time_since_backup = datetime.now() - last_backup
        
        return time_since_backup.total_seconds() / 3600 >= frequency_hours
    except Exception as e:
        logger.error(f"Error checking backup schedule: {e}")
        return False

def auto_backup(use_google_drive: bool = True, frequency_hours: int = 24) -> Tuple[bool, str]:
    """Perform automatic backup"""
    try:
        if not should_create_backup(frequency_hours):
            return True, "Backup not needed yet"
        
        success, message, backup_path = create_local_backup()
        
        if not success:
            return False, f"Local backup failed: {message}"
        
        if use_google_drive and GOOGLE_DRIVE_AVAILABLE:
            drive_success, drive_message, file_id = backup_to_google_drive()
            if drive_success:
                return True, "Backup completed (local + Drive)"
            else:
                return True, f"Local backup completed, Drive failed: {drive_message}"
        
        return True, "Local backup completed"
    except Exception as e:
        logger.error(f"Auto backup failed: {e}")
        return False, str(e)

def backup_to_google_drive() -> Tuple[bool, str, str]:
    """Backup to Google Drive (stub - implement with Drive API)"""
    logger.warning("Google Drive backup not fully implemented")
    return False, "Google Drive backup requires full implementation", ""

__all__ = [
    'create_local_backup', 'cleanup_old_backups', 'list_local_backups',
    'restore_from_backup', 'verify_backup', 'auto_backup', 'should_create_backup'
]
