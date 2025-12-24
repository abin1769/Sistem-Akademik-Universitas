"""
utils/logger.py
Centralized logging dan error handling untuk aplikasi.
"""

import logging
import os
from datetime import datetime


class SystemLogger:
    """Logger untuk sistem akademik"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """Singleton pattern untuk logger"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        """Initialize logger dengan format yang baik"""
        # Create logs directory jika tidak ada
        logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Setup logger
        self._logger = logging.getLogger('SistemAkademik')
        self._logger.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        log_file = os.path.join(logs_dir, f'sistem_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
    
    def info(self, message):
        """Log info message"""
        self._logger.info(message)
    
    def warning(self, message):
        """Log warning message"""
        self._logger.warning(message)
    
    def error(self, message, exception=None):
        """Log error message"""
        if exception:
            self._logger.error(f"{message}: {str(exception)}", exc_info=True)
        else:
            self._logger.error(message)
    
    def debug(self, message):
        """Log debug message"""
        self._logger.debug(message)
    
    def success(self, message):
        """Log success message (using info level)"""
        self._logger.info(f"[SUCCESS] {message}")


class ErrorHandler:
    """Centralized error handling"""
    
    @staticmethod
    def handle_service_error(error_obj, user_message="Terjadi kesalahan pada layanan"):
        """Handle service errors"""
        logger = SystemLogger()
        logger.error(user_message, error_obj)
        return f"{user_message}: {str(error_obj)}"
    
    @staticmethod
    def handle_database_error(error_obj, user_message="Terjadi kesalahan database"):
        """Handle database errors"""
        logger = SystemLogger()
        logger.error(user_message, error_obj)
        return f"{user_message}: {str(error_obj)}"
    
    @staticmethod
    def handle_validation_error(errors):
        """Handle validation errors"""
        logger = SystemLogger()
        logger.warning(f"Validation errors: {errors}")
        return errors
    
    @staticmethod
    def log_user_action(user_id, action, details=""):
        """Log user action untuk audit trail"""
        logger = SystemLogger()
        logger.info(f"User {user_id} performed action: {action}. Details: {details}")
    
    @staticmethod
    def log_data_modification(entity_type, operation, entity_id, details=""):
        """Log data modification"""
        logger = SystemLogger()
        logger.info(
            f"{entity_type} {operation} (ID: {entity_id}). Details: {details}"
        )


class AuditLog:
    """Audit logging untuk tracking perubahan data"""
    
    def __init__(self):
        self.logger = SystemLogger()
    
    def log_create(self, entity_type, entity_id, user_id, details=""):
        """Log create operation"""
        self.logger.info(
            f"CREATE - {entity_type} (ID: {entity_id}) by User {user_id}. {details}"
        )
    
    def log_update(self, entity_type, entity_id, user_id, old_values, new_values):
        """Log update operation"""
        changes = []
        for key in old_values:
            if old_values[key] != new_values.get(key):
                changes.append(f"{key}: {old_values[key]} -> {new_values.get(key)}")
        
        self.logger.info(
            f"UPDATE - {entity_type} (ID: {entity_id}) by User {user_id}. "
            f"Changes: {', '.join(changes)}"
        )
    
    def log_delete(self, entity_type, entity_id, user_id, reason=""):
        """Log delete operation"""
        self.logger.info(
            f"DELETE - {entity_type} (ID: {entity_id}) by User {user_id}. Reason: {reason}"
        )
    
    def log_access(self, user_id, resource, access_type):
        """Log resource access"""
        self.logger.debug(
            f"ACCESS - User {user_id} accessed {resource} ({access_type})"
        )


def setup_error_handlers():
    """Setup global error handlers"""
    import sys
    
    def handle_exception(exc_type, exc_value, exc_traceback):
        """Global exception handler"""
        logger = SystemLogger()
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logger.error(
            f"Uncaught exception: {exc_type.__name__}",
            exc_value
        )
    
    sys.excepthook = handle_exception
