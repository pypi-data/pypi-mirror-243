from omegaconf import OmegaConf
import os
import firebase_admin
from firebase_admin import credentials


class Config:
    def __init__(self, user_config_path=None, merge_config=True):
        # Load the default configuration
        default_config_path = os.path.join(os.path.dirname(__file__), 'default_config.yaml')
        self.default_config = OmegaConf.load(default_config_path) if os.path.exists(default_config_path) else OmegaConf.create()

        # Load the user configuration if provided
        self.user_config = OmegaConf.load(user_config_path) if user_config_path and os.path.exists(user_config_path) else OmegaConf.create()

        # Merge configurations
        self.config = OmegaConf.merge(self.default_config, self.user_config) if merge_config else self.user_config

    def get(self, key, default=None):
        return self.config.get(key, default)

# Global shared configuration instance
_shared_config = Config()


def set_config(config):
    global _shared_config
    _shared_config = config

def get_config():
    global _shared_config
    return _shared_config

def initialize_firebase():
    shared_config = get_config()
    try:
        firebase_admin.get_app()
    except ValueError:
        cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', shared_config.get('firebase_credentials_path'))
        if not cred_path:
            raise ValueError("Firebase credentials path not provided.")

        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
