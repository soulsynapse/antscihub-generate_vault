import json
import os

def load_config():
    """Load configuration from config files with fallbacks."""
    # Default configuration (code folder based - used only when config.json is not present)
    default_config = {
        "database_path": "responses.db",
        "output_base_dir": "output",
        "commands_subdir": "Commands", 
        "index_filename": "Index.md"
    }
    
    config = default_config.copy()
    
    # Try to load from config.json (tracked, template config)
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                config.update(file_config)
            print(f"Loaded configuration from: {config_path}")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config.json: {e}")
    
    # Try to load from config.local.json (ignored, local overrides)
    local_config_path = os.path.join(os.path.dirname(__file__), "config.local.json")
    if os.path.exists(local_config_path):
        try:
            with open(local_config_path, 'r', encoding='utf-8') as f:
                local_config = json.load(f)
                config.update(local_config)
            print(f"Loaded local configuration overrides from: {local_config_path}")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config.local.json: {e}")
    
    return config

def get_paths():
    """Get all configured paths."""
    config = load_config()
    
    return {
        'database_path': config['database_path'],
        'output_base_dir': config['output_base_dir'],
        'commands_dir': os.path.join(config['output_base_dir'], config['commands_subdir']),
        'index_path': os.path.join(config['output_base_dir'], config['index_filename'])
    }
