"""
PingDiff API Client
Handles communication with the PingDiff server and ISP detection
"""

import requests
import hashlib
import json
import os
from typing import Dict, List, Optional
from pathlib import Path

from config import API_BASE_URL, API_ENDPOINTS, DEFAULT_SERVERS, APP_VERSION


class APIClient:
    """Client for PingDiff API and external services"""

    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": f"PingDiff/{APP_VERSION}"
        })
        self._user_id = None
        self._config_path = self._get_config_path()

    def _get_config_path(self) -> Path:
        """Get path to local config file"""
        if os.name == 'nt':  # Windows
            app_data = os.environ.get('APPDATA', os.path.expanduser('~'))
            config_dir = Path(app_data) / 'PingDiff'
        else:  # Linux/Mac
            config_dir = Path.home() / '.pingdiff'

        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / 'config.json'

    def _load_config(self) -> Dict:
        """Load local config file"""
        if self._config_path.exists():
            try:
                with open(self._config_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_config(self, config: Dict):
        """Save local config file"""
        try:
            with open(self._config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except:
            pass

    def get_user_id(self) -> str:
        """Get or create a unique user ID for anonymous tracking"""
        if self._user_id:
            return self._user_id

        config = self._load_config()
        if 'user_id' in config:
            self._user_id = config['user_id']
        else:
            # Generate a new anonymous user ID
            import uuid
            self._user_id = str(uuid.uuid4())
            config['user_id'] = self._user_id
            self._save_config(config)

        return self._user_id

    def get_isp_info(self) -> Dict:
        """
        Get ISP information from ip-api.com

        Returns:
            Dict with country, city, isp, ip, etc.
        """
        try:
            response = self.session.get(
                API_ENDPOINTS["isp"],
                timeout=5
            )
            data = response.json()

            if data.get("status") == "success":
                return {
                    "country": data.get("country", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "isp": data.get("isp", "Unknown"),
                    "ip": data.get("query", ""),
                    "ip_hash": hashlib.sha256(data.get("query", "").encode()).hexdigest()[:16]
                }
        except Exception as e:
            print(f"Failed to get ISP info: {e}")

        return {
            "country": "Unknown",
            "city": "Unknown",
            "isp": "Unknown",
            "ip": "",
            "ip_hash": ""
        }

    def get_servers(self, game_slug: str = "overwatch-2") -> Dict[str, List[Dict]]:
        """
        Get server list from API, fallback to defaults if unavailable.

        Args:
            game_slug: Game identifier (e.g., "overwatch-2")

        Returns:
            Dict with regions as keys and server lists as values
        """
        try:
            response = self.session.get(
                f"{self.base_url}{API_ENDPOINTS['servers']}?game={game_slug}",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Failed to get servers from API: {e}")

        # Return default servers as fallback
        return DEFAULT_SERVERS.get(game_slug, {})

    def submit_results(self, results: List[Dict], isp_info: Dict,
                       game_slug: str = "overwatch-2",
                       user_token: Optional[str] = None) -> Dict:
        """
        Submit test results to the API.

        Args:
            results: List of ping test results
            isp_info: ISP information dict
            game_slug: Game identifier
            user_token: Optional auth token for logged-in users

        Returns:
            Dict with submission status and result ID
        """
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
                return {
                    "success": True,
                    "result_id": data.get("id"),
                    "dashboard_url": data.get("url", f"{self.base_url}/results/{data.get('id')}")
                }
            else:
                return {
                    "success": False,
                    "error": f"Server returned {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_recommendations(self, isp: str, region: str,
                           game_slug: str = "overwatch-2") -> Dict:
        """
        Get server recommendations based on ISP and region.

        Args:
            isp: User's ISP name
            region: Region code (EU, NA, ASIA)
            game_slug: Game identifier

        Returns:
            Dict with recommended servers and community data
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/recommendations",
                params={
                    "isp": isp,
                    "region": region,
                    "game": game_slug
                },
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Failed to get recommendations: {e}")

        return {
            "best_server": None,
            "avg_ping": None,
            "players_tested": 0
        }
