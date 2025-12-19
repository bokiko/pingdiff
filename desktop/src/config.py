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
APP_VERSION = "1.7.0"

# Ping Configuration
PING_COUNT = 10  # Number of pings per server
PING_TIMEOUT = 1  # Seconds

# Apple-inspired UI Colors (macOS dark mode aesthetic)
COLORS = {
    # Backgrounds
    "bg": "#1c1c1e",
    "bg_secondary": "#2c2c2e",
    "bg_tertiary": "#3a3a3c",

    # Cards & Surfaces
    "card": "#2c2c2e",
    "card_hover": "#3a3a3c",
    "card_elevated": "#48484a",

    # Borders
    "border": "#3a3a3c",
    "border_light": "#48484a",

    # Accent (Apple Blue)
    "accent": "#0a84ff",
    "accent_hover": "#409cff",
    "accent_dim": "#0066cc",

    # Semantic Colors
    "success": "#30d158",
    "success_dim": "#248a3d",
    "warning": "#ff9f0a",
    "warning_dim": "#c77c00",
    "error": "#ff453a",
    "error_dim": "#d70015",

    # Text
    "text": "#ffffff",
    "text_secondary": "#ebebf5",
    "text_muted": "#8e8e93",
    "text_dim": "#636366",

    # Special
    "separator": "#38383a",
    "overlay": "#000000"
}

# Game server regions
REGIONS = ["EU", "NA", "ASIA", "SA", "ME"]

# Default servers (fallback if API fails)
DEFAULT_SERVERS = {
    "overwatch-2": {
        "EU": [
            {"id": "eu-ams", "location": "Amsterdam", "ip": "185.60.112.157", "port": 26503},
            {"id": "eu-par", "location": "Paris", "ip": "185.60.114.159", "port": 26503},
            {"id": "eu-fra", "location": "Frankfurt", "ip": "185.60.112.158", "port": 26503}
        ],
        "NA": [
            {"id": "na-west", "location": "Los Angeles", "ip": "24.105.30.129", "port": 26503},
            {"id": "na-central", "location": "Chicago", "ip": "24.105.62.129", "port": 26503},
            {"id": "na-east", "location": "New York", "ip": "24.105.94.129", "port": 26503}
        ],
        "ASIA": [
            {"id": "asia-sg", "location": "Singapore", "ip": "137.221.106.104", "port": 26503},
            {"id": "asia-kr", "location": "Seoul", "ip": "117.52.35.100", "port": 26503},
            {"id": "asia-jp", "location": "Tokyo", "ip": "34.84.155.100", "port": 26503},
            {"id": "asia-tw", "location": "Taiwan", "ip": "203.66.81.98", "port": 26503},
            {"id": "asia-au", "location": "Sydney", "ip": "103.4.115.100", "port": 26503}
        ],
        "SA": [
            {"id": "sa-br", "location": "São Paulo", "ip": "54.207.107.12", "port": 26503}
        ],
        "ME": [
            {"id": "me-bh", "location": "Bahrain", "ip": "157.175.45.1", "port": 26503},
            {"id": "me-ae", "location": "Dubai", "ip": "34.18.61.77", "port": 26503}
        ]
    }
}

# Region display names
REGION_NAMES = {
    "EU": "Europe",
    "NA": "North America",
    "ASIA": "Asia Pacific",
    "SA": "South America",
    "ME": "Middle East"
}
