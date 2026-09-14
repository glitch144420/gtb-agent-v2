import json
import os
from typing import Dict, Any

class ConfigManager:
    """Manages user configuration."""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Return default config
        return {
            "llm_provider": "openai",
            "llm_api_key": "",
            "image_provider": "replicate",
            "image_api_key": "",
            "aws": {
                "region": "us-east-1",
                "access_key": "",
                "secret_key": "",
                "bucket_name": "project-forge-storage"
            }
        }
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        self.config = config
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config[key] = value
        self.save_config(self.config)
    
    def get_aws_config(self) -> Dict[str, Any]:
        """Get AWS configuration."""
        return self.config.get("aws", {})