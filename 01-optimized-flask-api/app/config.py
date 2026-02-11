"""
Flask Application Configuration
Loads configuration from environment variables with secure defaults
"""

import os


class Config:
    """Base configuration"""
    
    # Application
    VERSION = os.getenv('APP_VERSION', '1.0.0')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Server
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    
    # Security
    API_KEY = os.getenv('API_KEY', 'CHANGE_ME_IN_PRODUCTION')
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.getenv('LOG_FORMAT', 'json')  # 'json' or 'text'
    
    # Performance
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max request size
    
    # CORS (if needed)
    CORS_ENABLED = os.getenv('CORS_ENABLED', 'False').lower() == 'true'
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    @staticmethod
    def validate():
        """Validate critical configuration"""
        if Config.API_KEY == 'CHANGE_ME_IN_PRODUCTION' and Config.ENVIRONMENT == 'production':
            raise ValueError("API_KEY must be set in production!")
        
        if Config.PORT < 1024 and os.getuid() != 0:
            raise ValueError(f"Port {Config.PORT} requires root privileges")


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENVIRONMENT = 'development'
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENVIRONMENT = 'production'
    LOG_LEVEL = 'INFO'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    ENVIRONMENT = 'testing'
    LOG_LEVEL = 'DEBUG'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}