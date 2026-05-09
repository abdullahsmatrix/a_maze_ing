from config.config import Config
from typing import Dict, Optional

class ConfigError(Exception):
    """Custom Exception for configuration errors"""
    pass

def parse_config(config_path: str):
    raw_data: dict = {}
    try:
        with open(config_path, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                line = line.lower()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ConfigError(f"Line: {line_number}, '{line}' invalid format")
                key, value = line.split("=", 1)
                raw_data[key.strip()] = value.strip()
    except FileNotFoundError:
        raise ConfigError(f"Config file not found: {config_path}")
    
    
    #--- Validate Required Keys ---#
    required_keys: list[str] = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

    for key in required_keys:
        if key.lower() not in raw_data:
            raise ConfigError(f"Missing required key: {key}")
    
    return Config(**raw_data)


    





