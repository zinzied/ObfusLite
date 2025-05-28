"""
Configuration module for the test application
"""

import os

# Application configuration
APP_CONFIG = {
    "name": "Test Application",
    "version": "1.0.0",
    "debug": True,
    "max_items": 100
}

def get_config():
    """Get application configuration"""
    config = APP_CONFIG.copy()
    
    # Override with environment variables if available
    if os.getenv("APP_DEBUG"):
        config["debug"] = os.getenv("APP_DEBUG").lower() == "true"
    
    if os.getenv("APP_MAX_ITEMS"):
        try:
            config["max_items"] = int(os.getenv("APP_MAX_ITEMS"))
        except ValueError:
            pass
    
    return config

def get_database_url():
    """Get database URL from config"""
    return os.getenv("DATABASE_URL", "sqlite:///test.db")

def is_production():
    """Check if running in production mode"""
    return os.getenv("ENVIRONMENT", "development") == "production"
