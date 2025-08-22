"""
Simple .env file loader for Bug Voice Assistant
"""

import os

def load_env(env_file=".env"):
    """Load environment variables from .env file"""
    if not os.path.exists(env_file):
        return
    
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value
    except Exception as e:
        print(f"Warning: Could not load .env file: {e}")

# Load environment variables when this module is imported
load_env()
