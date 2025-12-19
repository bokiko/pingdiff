"""
PingDiff Configuration
Server IPs and API endpoints
"""

# API Configuration
API_BASE_URL = "https://pingdiff.com"
API_ENDPOINTS = {
    "servers": "/api/servers",
    "results": "/api/results",
    "isp": "http://ip-api.com/json/?fields=status,country,city,isp,query"
}

# App Version
APP_VERSION = "1.4.0"

# Ping Configuration
PING_COUNT = 10  # Number of pings per server (reduced for speed)
PING_TIMEOUT = 1  # Seconds (reduced for speed)

# UI Colors (matching website theme)
COLORS = {
    "bg": "#0a0a0a",
    "card": "#1a1a1a",
    "accent": "#3b82f6",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "text": "#ffffff",
    "text_muted": "#9ca3af"
}

# Game server regions
REGIONS = ["EU", "NA", "ASIA"]

# Default servers (fallback if API fails)
DEFAULT_SERVERS = {
    "overwatch-2": {
        "EU": [
            {"id": "eu-ams", "location": "Amsterdam", "ip": "185.60.112.157", "port": 26503},
            {"id": "eu-par", "location": "Paris", "ip": "185.60.114.159", "port": 26503}
        ],
        "NA": [
            {"id": "na-west", "location": "Los Angeles (US West)", "ip": "24.105.30.129", "port": 26503},
            {"id": "na-central", "location": "Chicago (US Central)", "ip": "24.105.62.129", "port": 26503},
            {"id": "na-east", "location": "New York (US East)", "ip": "24.105.94.129", "port": 26503}
        ],
        "ASIA": [
            {"id": "asia-sg", "location": "Singapore", "ip": "137.221.106.104", "port": 26503},
            {"id": "asia-kr", "location": "Seoul", "ip": "117.52.35.100", "port": 26503},
            {"id": "asia-au", "location": "Sydney", "ip": "103.4.115.100", "port": 26503}
        ]
    }
}
