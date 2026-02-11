"""
Utility functions for Flask API
"""

import logging
import sys
import json
import ipaddress
from datetime import datetime


def setup_logging():
    """
    Configure structured logging
    Supports both JSON and text formats
    """
    from .config import Config
    
    # Create logger
    logger = logging.getLogger('flask_api')
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # Set format based on configuration
    if Config.LOG_FORMAT == 'json':
        # JSON formatter for production (easier to parse)
        formatter = JSONFormatter()
    else:
        # Standard formatter for development
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging
    Compatible with ELK Stack, Datadog, CloudWatch, etc.
    """
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        
        return json.dumps(log_data)


def validate_ip_address(ip_string):
    """
    Validate IP address format (IPv4 or IPv6)
    
    Args:
        ip_string (str): IP address to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False


def sanitize_input(input_string, max_length=255):
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        input_string (str): Input to sanitize
        max_length (int): Maximum allowed length
    
    Returns:
        str: Sanitized input
    """
    if not input_string:
        return ""
    
    # Truncate to max length
    sanitized = str(input_string)[:max_length]
    
    # Remove dangerous characters (customize based on needs)
    dangerous_chars = ['<', '>', '&', '"', "'", '`', '|', ';']
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()


def generate_response(success, message=None, data=None, status_code=200):
    """
    Generate standardized API response
    
    Args:
        success (bool): Success status
        message (str): Response message
        data (dict): Response data
        status_code (int): HTTP status code
    
    Returns:
        tuple: (response_dict, status_code)
    """
    response = {
        'success': success,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if message:
        response['message'] = message
    
    if data:
        response['data'] = data
    
    return response, status_code