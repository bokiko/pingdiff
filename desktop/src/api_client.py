"""
PingDiff API Client
Handles communication with the PingDiff server, ISP detection, and settings
"""

import requests
import hashlib
import json
import os
import logging
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime

from config import API_BASE_URL, API_ENDPOINTS, DEFAULT_SERVERS, APP_VERSION

# Fixed salt for IP hashing (not secret, just for consistency)
IP_HASH_SALT = "pingdiff-v1-2024"


def get_app_data_dir() -> Path:
    """Get the application data directory"""
    if os.name == 'nt':  # Windows
        app_data = os.environ.get('APPDATA', os.path.expanduser('~'))
        app_dir = Path(app_data) / 'PingDiff'
    else:  # Linux/Mac
        app_dir = Path.home() / '.pingdiff'

    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


def setup_logging() -> logging.Logger:
    """Set up file and console logging"""
    app_dir = get_app_data_dir()
    log_dir = app_dir / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create log file with date
    log_file = log_dir / f'pingdiff_{datetime.now().strftime("%Y%m%d")}.log'

    # Create logger
    logger = logging.getLogger('PingDiff')
    logger.setLevel(logging.DEBUG)

    # Clear existing handlers
    logger.handlers = []

    # File handler - detailed logging
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler - info and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.info(f"PingDiff v{APP_VERSION} started")
    logger.info(f"Log file: {log_file}")

    return logger


# Initialize logging
logger = setup_logging()


class Settings:
    """Manage application settings"""

    DEFAULT_SETTINGS = {
        "share_results": True,
        "default_region": "EU",
        "ping_count": 10,
        "first_run": True
    }

    def __init__(self):
        self._settings_path = get_app_data_dir() / 'settings.json'
        self._settings = self._load()

    def _load(self) -> Dict:
        """Load settings from file"""
        if self._settings_path.exists():
            try:
                with open(self._settings_path, 'r') as f:
                    saved = json.load(f)
                    # Merge with defaults (in case new settings are added)
                    return {**self.DEFAULT_SETTINGS, **saved}
            except Exception as e:
                logger.warning(f"Error loading settings: {e}")
        return self.DEFAULT_SETTINGS.copy()

    def _save(self):
        """Save settings to file"""
        try:
            with open(self._settings_path, 'w') as f:
                json.dump(self._settings, f, indent=2)
            logger.debug("Settings saved")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")

    def get(self, key: str, default=None):
        """Get a setting value"""
        return self._settings.get(key, default)

    def set(self, key: str, value):
        """Set a setting value"""
        self._settings[key] = value
        self._save()
        logger.info(f"Setting changed: {key} = {value}")

    @property
    def share_results(self) -> bool:
        return self._settings.get("share_results", True)

    @share_results.setter
    def share_results(self, value: bool):
        self.set("share_results", value)

    @property
    def default_region(self) -> str:
        return self._settings.get("default_region", "EU")

    @default_region.setter
    def default_region(self, value: str):
        self.set("default_region", value)


class APIClient:
    """Client for PingDiff API and external services"""

    def __init__(self, settings: Settings = None):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": f"PingDiff/{APP_VERSION}"
        })
        self._user_id = None
        self._config_path = get_app_data_dir() / 'config.json'
        self.settings = settings or Settings()

    def _load_config(self) -> Dict:
        """Load local config file"""
        if self._config_path.exists():
            try:
                with open(self._config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error loading config: {e}")
        return {}

    def _save_config(self, config: Dict):
        """Save local config file"""
        try:
            with open(self._config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")

    def _hash_ip(self, ip: str) -> str:
        """Hash IP address with salt for privacy"""
        if not ip:
            return ""
        salted = f"{IP_HASH_SALT}:{ip}"
        return hashlib.sha256(salted.encode()).hexdigest()

    def get_user_id(self) -> str:
        """Get or create a unique user ID for anonymous tracking"""
        if self._user_id:
            return self._user_id

        config = self._load_config()
        if 'user_id' in config:
            self._user_id = config['user_id']
        else:
            import uuid
            self._user_id = str(uuid.uuid4())
            config['user_id'] = self._user_id
            self._save_config(config)
            logger.info(f"Generated new user ID")

        return self._user_id

    def get_isp_info(self) -> Dict:
        """Get ISP information from ip-api.com"""
        logger.debug("Fetching ISP info...")
        try:
            response = self.session.get(
                API_ENDPOINTS["isp"],
                timeout=5
            )
            data = response.json()

            if data.get("status") == "success":
                ip = data.get("query", "")
                info = {
                    "country": data.get("country", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "isp": data.get("isp", "Unknown"),
                    "ip": ip,
                    "ip_hash": self._hash_ip(ip)
                }
                logger.info(f"ISP detected: {info['isp']} ({info['city']}, {info['country']})")
                return info
        except requests.Timeout:
            logger.warning("Timeout getting ISP info")
        except requests.RequestException as e:
            logger.warning(f"Network error getting ISP info: {e}")
        except Exception as e:
            logger.error(f"Unexpected error getting ISP info: {e}")

        return {
            "country": "Unknown",
            "city": "Unknown",
            "isp": "Unknown",
            "ip": "",
            "ip_hash": ""
        }

    def get_servers(self, game_slug: str = "overwatch-2") -> Dict[str, List[Dict]]:
        """Get server list from API, fallback to defaults if unavailable"""
        logger.debug(f"Fetching servers for {game_slug}...")
        try:
            response = self.session.get(
                f"{self.base_url}{API_ENDPOINTS['servers']}?game={game_slug}",
                timeout=10
            )
            if response.status_code == 200:
                servers = response.json()
                total = sum(len(v) for v in servers.values())
                logger.info(f"Loaded {total} servers from API")
                return servers
            else:
                logger.warning(f"Server returned {response.status_code}")
        except requests.Timeout:
            logger.warning("Timeout getting servers")
        except requests.RequestException as e:
            logger.warning(f"Network error getting servers: {e}")
        except Exception as e:
            logger.error(f"Unexpected error getting servers: {e}")

        logger.info("Using default servers as fallback")
        return DEFAULT_SERVERS.get(game_slug, {})

    def submit_results(self, results: List[Dict], isp_info: Dict,
                       game_slug: str = "overwatch-2",
                       user_token: Optional[str] = None) -> Dict:
        """Submit test results to the API (if sharing is enabled)"""

        # Check if sharing is enabled
        if not self.settings.share_results:
            logger.info("Result sharing is disabled - not submitting")
            return {
                "success": False,
                "error": "Sharing disabled",
                "sharing_disabled": True
            }

        logger.info(f"Submitting {len(results)} results to API...")

        payload = {
            "game": game_slug,
            "results": results,
            "isp": isp_info.get("isp", "Unknown"),
            "country": isp_info.get("country", "Unknown"),
            "city": isp_info.get("city", "Unknown"),
            "ip_hash": isp_info.get("ip_hash", ""),
            "client_version": APP_VERSION,
            "anonymous_id": self.get_user_id()
        }

        headers = {}
        if user_token:
            headers["Authorization"] = f"Bearer {user_token}"

        try:
            response = self.session.post(
                f"{self.base_url}{API_ENDPOINTS['results']}",
                json=payload,
                headers=headers,
                timeout=15
            )

            if response.status_code in [200, 201]:
                data = response.json()
                logger.info(f"Results submitted successfully: {data.get('id')}")
                return {
                    "success": True,
                    "result_id": data.get("id"),
                    "dashboard_url": data.get("url", "/dashboard")
                }
            elif response.status_code == 429:
                logger.warning("Rate limit exceeded")
                return {
                    "success": False,
                    "error": "Rate limit exceeded. Please try again later."
                }
            else:
                logger.warning(f"Server returned {response.status_code}")
                return {
                    "success": False,
                    "error": f"Server returned {response.status_code}"
                }
        except requests.Timeout:
            logger.warning("Timeout submitting results")
            return {"success": False, "error": "Request timed out"}
        except requests.RequestException as e:
            logger.warning(f"Network error submitting results: {e}")
            return {"success": False, "error": "Network error"}
        except Exception as e:
            logger.error(f"Unexpected error submitting results: {e}")
            return {"success": False, "error": str(e)}

    def get_recommendations(self, isp: str, region: str,
                           game_slug: str = "overwatch-2") -> Dict:
        """Get server recommendations based on ISP and region"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/recommendations",
                params={"isp": isp, "region": region, "game": game_slug},
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.warning(f"Failed to get recommendations: {e}")

        return {"best_server": None, "avg_ping": None, "players_tested": 0}

    @staticmethod
    def get_log_directory() -> Path:
        """Get the log directory path"""
        return get_app_data_dir() / 'logs'

    @staticmethod
    def get_app_directory() -> Path:
        """Get the app data directory path"""
        return get_app_data_dir()
