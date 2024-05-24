from pathlib import Path


from app.env import APP_DIR

import toml

def load_config():
    config_toml = toml.load(str(APP_DIR / "config" / "config.toml"))
    return config_toml


config = load_config()
