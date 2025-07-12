import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL') or "https://discord.com/api/webhooks/1387057201931223110/zjX1FEcTkiErkZwAKKcANFmwgoFhnT2fov1qu9u9EFnu_sMp2CuFB83Z1_ygcOGDWolr"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    CORS_ORIGINS = ["http://localhost:3000", "https://emotion-dashboard-1-6kn0.onrender.com"]

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    CORS_ORIGINS = ["*"]  # Configure specific domains in production

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    CORS_ORIGINS = ["https://emotion-dashboard-1-6kn0.onrender.com"]

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}