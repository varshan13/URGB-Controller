"""
Configuration Manager for RGB Control Application
Handles saving/loading profiles and application settings
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any


class ConfigManager:
    """Manages application configuration and RGB profiles"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.profiles_file = os.path.join(config_dir, "profiles.json")
        self.settings_file = os.path.join(config_dir, "settings.json")
        self.logger = logging.getLogger(__name__)
        
        # Create config directory if it doesn't exist
        os.makedirs(config_dir, exist_ok=True)
        
        # Initialize default files
        self._initialize_config_files()
        
    def _initialize_config_files(self):
        """Initialize default configuration files"""
        try:
            # Initialize profiles file
            if not os.path.exists(self.profiles_file):
                default_profiles = {
                    "profiles": {},
                    "last_modified": datetime.now().isoformat(),
                    "version": "1.0"
                }
                with open(self.profiles_file, 'w') as f:
                    json.dump(default_profiles, f, indent=2)
                    
            # Initialize settings file
            if not os.path.exists(self.settings_file):
                default_settings = {
                    "application": {
                        "auto_connect": True,
                        "minimize_to_tray": False,
                        "check_updates": True,
                        "theme": "dark"
                    },
                    "openrgb": {
                        "host": "localhost",
                        "port": 6742,
                        "auto_connect": True,
                        "scan_interval": 30
                    },
                    "razer": {
                        "auto_connect": True,
                        "sdk_timeout": 5000
                    },
                    "devices": {
                        "auto_sync": False,
                        "default_brightness": 100,
                        "default_speed": 50
                    },
                    "last_modified": datetime.now().isoformat(),
                    "version": "1.0"
                }
                with open(self.settings_file, 'w') as f:
                    json.dump(default_settings, f, indent=2)
                    
        except Exception as e:
            self.logger.error(f"Error initializing config files: {e}")
            
    def save_profile(self, name: str, profile_data: Dict) -> bool:
        """Save an RGB profile"""
        try:
            # Load existing profiles
            profiles = self._load_json_file(self.profiles_file, {})
            
            if "profiles" not in profiles:
                profiles["profiles"] = {}
                
            # Add timestamp and validation
            profile_data["created"] = datetime.now().isoformat()
            profile_data["version"] = "1.0"
            
            # Validate profile data
            if self._validate_profile(profile_data):
                profiles["profiles"][name] = profile_data
                profiles["last_modified"] = datetime.now().isoformat()
                
                # Save back to file
                with open(self.profiles_file, 'w') as f:
                    json.dump(profiles, f, indent=2)
                    
                self.logger.info(f"Profile '{name}' saved successfully")
                return True
            else:
                self.logger.error(f"Invalid profile data for '{name}'")
                return False
                
        except Exception as e:
            self.logger.error(f"Error saving profile '{name}': {e}")
            return False
            
    def load_profile(self, name: str) -> Optional[Dict]:
        """Load an RGB profile"""
        try:
            profiles = self._load_json_file(self.profiles_file, {})
            
            if "profiles" in profiles and name in profiles["profiles"]:
                profile_data = profiles["profiles"][name]
                self.logger.info(f"Profile '{name}' loaded successfully")
                return profile_data
            else:
                self.logger.warning(f"Profile '{name}' not found")
                return None
                
        except Exception as e:
            self.logger.error(f"Error loading profile '{name}': {e}")
            return None
            
    def get_profiles(self) -> List[str]:
        """Get list of saved profile names"""
        try:
            profiles = self._load_json_file(self.profiles_file, {})
            
            if "profiles" in profiles:
                return list(profiles["profiles"].keys())
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Error getting profile list: {e}")
            return []
            
    def delete_profile(self, name: str) -> bool:
        """Delete an RGB profile"""
        try:
            profiles = self._load_json_file(self.profiles_file, {})
            
            if "profiles" in profiles and name in profiles["profiles"]:
                del profiles["profiles"][name]
                profiles["last_modified"] = datetime.now().isoformat()
                
                with open(self.profiles_file, 'w') as f:
                    json.dump(profiles, f, indent=2)
                    
                self.logger.info(f"Profile '{name}' deleted successfully")
                return True
            else:
                self.logger.warning(f"Profile '{name}' not found for deletion")
                return False
                
        except Exception as e:
            self.logger.error(f"Error deleting profile '{name}': {e}")
            return False
            
    def save_settings(self, settings: Dict) -> bool:
        """Save application settings"""
        try:
            settings["last_modified"] = datetime.now().isoformat()
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
                
            self.logger.info("Application settings saved")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
            return False
            
    def load_settings(self) -> Dict:
        """Load application settings"""
        try:
            settings = self._load_json_file(self.settings_file, {})
            self.logger.info("Application settings loaded")
            return settings
            
        except Exception as e:
            self.logger.error(f"Error loading settings: {e}")
            return {}
            
    def get_setting(self, category: str, key: str, default: Any = None) -> Any:
        """Get a specific setting value"""
        try:
            settings = self.load_settings()
            
            if category in settings and key in settings[category]:
                return settings[category][key]
            else:
                return default
                
        except Exception as e:
            self.logger.error(f"Error getting setting {category}.{key}: {e}")
            return default
            
    def set_setting(self, category: str, key: str, value: Any) -> bool:
        """Set a specific setting value"""
        try:
            settings = self.load_settings()
            
            if category not in settings:
                settings[category] = {}
                
            settings[category][key] = value
            
            return self.save_settings(settings)
            
        except Exception as e:
            self.logger.error(f"Error setting {category}.{key}: {e}")
            return False
            
    def export_profiles(self, export_path: str) -> bool:
        """Export all profiles to a file"""
        try:
            profiles = self._load_json_file(self.profiles_file, {})
            
            export_data = {
                "export_date": datetime.now().isoformat(),
                "application": "RGB Control Center",
                "version": "1.0",
                "profiles": profiles.get("profiles", {})
            }
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
                
            self.logger.info(f"Profiles exported to {export_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting profiles: {e}")
            return False
            
    def import_profiles(self, import_path: str, overwrite: bool = False) -> bool:
        """Import profiles from a file"""
        try:
            if not os.path.exists(import_path):
                self.logger.error(f"Import file not found: {import_path}")
                return False
                
            import_data = self._load_json_file(import_path, {})
            
            if "profiles" not in import_data:
                self.logger.error("Invalid import file format")
                return False
                
            current_profiles = self._load_json_file(self.profiles_file, {})
            if "profiles" not in current_profiles:
                current_profiles["profiles"] = {}
                
            imported_count = 0
            
            for profile_name, profile_data in import_data["profiles"].items():
                if profile_name not in current_profiles["profiles"] or overwrite:
                    if self._validate_profile(profile_data):
                        current_profiles["profiles"][profile_name] = profile_data
                        imported_count += 1
                        
            if imported_count > 0:
                current_profiles["last_modified"] = datetime.now().isoformat()
                
                with open(self.profiles_file, 'w') as f:
                    json.dump(current_profiles, f, indent=2)
                    
                self.logger.info(f"Imported {imported_count} profiles")
                return True
            else:
                self.logger.warning("No profiles were imported")
                return False
                
        except Exception as e:
            self.logger.error(f"Error importing profiles: {e}")
            return False
            
    def _load_json_file(self, file_path: str, default: Dict) -> Dict:
        """Load JSON file with error handling"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            else:
                return default
                
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error loading JSON file {file_path}: {e}")
            return default
            
    def _validate_profile(self, profile_data: Dict) -> bool:
        """Validate profile data structure"""
        try:
            required_fields = ['color', 'effect']
            
            for field in required_fields:
                if field not in profile_data:
                    return False
                    
            # Validate color format
            color = profile_data['color']
            if not isinstance(color, (list, tuple)) or len(color) != 3:
                return False
                
            # Validate color values
            for value in color:
                if not isinstance(value, int) or value < 0 or value > 255:
                    return False
                    
            # Validate effect
            valid_effects = [
                'static', 'breathing', 'wave', 'rainbow', 
                'spectrum_cycle', 'reactive', 'comet', 'flash'
            ]
            
            if profile_data['effect'] not in valid_effects:
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating profile: {e}")
            return False
            
    def cleanup_old_profiles(self, days_old: int = 365) -> int:
        """Remove profiles older than specified days"""
        try:
            profiles = self._load_json_file(self.profiles_file, {})
            
            if "profiles" not in profiles:
                return 0
                
            current_time = datetime.now()
            removed_count = 0
            profiles_to_remove = []
            
            for profile_name, profile_data in profiles["profiles"].items():
                if "created" in profile_data:
                    created_time = datetime.fromisoformat(profile_data["created"])
                    age_days = (current_time - created_time).days
                    
                    if age_days > days_old:
                        profiles_to_remove.append(profile_name)
                        
            for profile_name in profiles_to_remove:
                del profiles["profiles"][profile_name]
                removed_count += 1
                
            if removed_count > 0:
                profiles["last_modified"] = datetime.now().isoformat()
                
                with open(self.profiles_file, 'w') as f:
                    json.dump(profiles, f, indent=2)
                    
                self.logger.info(f"Cleaned up {removed_count} old profiles")
                
            return removed_count
            
        except Exception as e:
            self.logger.error(f"Error cleaning up profiles: {e}")
            return 0