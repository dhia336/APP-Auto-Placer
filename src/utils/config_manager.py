import json
from dataclasses import dataclass, asdict
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

@dataclass
class AppConfig:
    """Configuration for an application window."""
    shortcut_path: str
    position: Tuple[int, int]
    size: Tuple[int, int]

    def to_dict(self) -> dict:
        """Convert the config to a dictionary."""
        return {
            'shortcut_path': self.shortcut_path,
            'position': list(self.position),
            'size': list(self.size)
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AppConfig':
        """Create a config from a dictionary."""
        return cls(
            shortcut_path=data['shortcut_path'],
            position=tuple(data['position']),
            size=tuple(data['size'])
        )

class ConfigManager:
    """Manages saving and loading application configurations."""
    
    @staticmethod
    def save_configs(configs: List[AppConfig], filepath: str) -> None:
        """Save configurations to a JSON file."""
        try:
            data = [config.to_dict() for config in configs]
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            logger.info(f"Configurations saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save configurations: {e}")
            raise

    @staticmethod
    def load_configs(filepath: str) -> List[AppConfig]:
        """Load configurations from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return [AppConfig.from_dict(item) for item in data]
        except Exception as e:
            logger.error(f"Failed to load configurations: {e}")
            raise 