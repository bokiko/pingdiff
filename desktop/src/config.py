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
APP_VERSION = "1.14.0"

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
    },
    "call-of-duty": {
        "EU": [
            {"id": "eu-ams", "location": "Amsterdam", "ip": "108.61.198.102", "port": 3074},
            {"id": "eu-lon", "location": "London", "ip": "108.61.196.101", "port": 3074},
            {"id": "eu-fra", "location": "Frankfurt", "ip": "108.61.210.117", "port": 3074},
            {"id": "eu-par", "location": "Paris", "ip": "108.61.209.127", "port": 3074},
            {"id": "eu-mad", "location": "Madrid", "ip": "208.76.222.30", "port": 3074}
        ],
        "NA": [
            {"id": "na-atl", "location": "Atlanta", "ip": "108.61.193.166", "port": 3074},
            {"id": "na-chi", "location": "Chicago", "ip": "107.191.51.12", "port": 3074},
            {"id": "na-dal", "location": "Dallas", "ip": "108.61.224.175", "port": 3074},
            {"id": "na-lax", "location": "Los Angeles", "ip": "108.61.219.200", "port": 3074},
            {"id": "na-mia", "location": "Miami", "ip": "104.156.244.232", "port": 3074},
            {"id": "na-nyc", "location": "New York", "ip": "108.61.149.182", "port": 3074},
            {"id": "na-sfo", "location": "San Francisco", "ip": "104.156.230.107", "port": 3074},
            {"id": "na-sea", "location": "Seattle", "ip": "108.61.194.105", "port": 3074}
        ],
        "ASIA": [
            {"id": "asia-tok", "location": "Tokyo", "ip": "108.61.201.151", "port": 3074},
            {"id": "asia-seo", "location": "Seoul", "ip": "141.164.34.61", "port": 3074},
            {"id": "asia-sgp", "location": "Singapore", "ip": "45.32.100.168", "port": 3074},
            {"id": "asia-syd", "location": "Sydney", "ip": "108.61.212.117", "port": 3074}
        ],
        "SA": [
            {"id": "sa-sao", "location": "São Paulo", "ip": "216.238.98.118", "port": 3074},
            {"id": "sa-scl", "location": "Santiago", "ip": "64.176.2.7", "port": 3074}
        ],
        "ME": [
            {"id": "me-tlv", "location": "Tel Aviv", "ip": "64.176.162.16", "port": 3074}
        ]
    },
    "counter-strike-2": {
        "EU": [
            {"id": "eu-lux", "location": "Luxembourg", "ip": "146.66.152.1", "port": 27015},
            {"id": "eu-sto", "location": "Stockholm", "ip": "146.66.156.1", "port": 27015},
            {"id": "eu-vie", "location": "Vienna", "ip": "146.66.155.1", "port": 27015},
            {"id": "eu-war", "location": "Warsaw", "ip": "155.133.240.1", "port": 27015},
            {"id": "eu-mad", "location": "Madrid", "ip": "155.133.246.1", "port": 27015}
        ],
        "NA": [
            {"id": "na-was", "location": "Washington DC", "ip": "208.78.164.1", "port": 27015},
            {"id": "na-atl", "location": "Atlanta", "ip": "162.254.199.1", "port": 27015},
            {"id": "na-sea", "location": "Seattle", "ip": "192.69.96.1", "port": 27015},
            {"id": "na-lax", "location": "Los Angeles", "ip": "162.254.194.1", "port": 27015}
        ],
        "ASIA": [
            {"id": "asia-sgp", "location": "Singapore", "ip": "103.28.54.1", "port": 27015},
            {"id": "asia-tok", "location": "Tokyo", "ip": "45.121.186.1", "port": 27015},
            {"id": "asia-hkg", "location": "Hong Kong", "ip": "155.133.244.1", "port": 27015},
            {"id": "asia-mum", "location": "Mumbai", "ip": "180.149.41.1", "port": 27015},
            {"id": "asia-syd", "location": "Sydney", "ip": "103.10.125.1", "port": 27015}
        ],
        "SA": [
            {"id": "sa-sao", "location": "São Paulo", "ip": "209.197.29.1", "port": 27015},
            {"id": "sa-scl", "location": "Santiago", "ip": "155.133.249.1", "port": 27015},
            {"id": "sa-lim", "location": "Lima", "ip": "143.137.146.1", "port": 27015}
        ],
        "ME": [
            {"id": "me-dub", "location": "Dubai", "ip": "185.25.183.1", "port": 27015}
        ]
    },
    "battlefield-6": {
        "EU": [
            {"id": "eu-lon", "location": "London", "ip": "35.71.111.102", "port": 25200},
            {"id": "eu-ire", "location": "Dublin", "ip": "35.71.75.100", "port": 25200},
            {"id": "eu-fra", "location": "Frankfurt", "ip": "35.71.105.10", "port": 25200},
            {"id": "eu-par", "location": "Paris", "ip": "35.71.101.129", "port": 25200},
            {"id": "eu-sto", "location": "Stockholm", "ip": "35.71.98.128", "port": 25200}
        ],
        "NA": [
            {"id": "na-vir", "location": "Virginia", "ip": "3.218.182.208", "port": 25200},
            {"id": "na-ohi", "location": "Ohio", "ip": "35.71.102.135", "port": 25200},
            {"id": "na-cal", "location": "California", "ip": "35.71.117.132", "port": 25200},
            {"id": "na-ore", "location": "Oregon", "ip": "35.71.66.124", "port": 25200}
        ],
        "ASIA": [
            {"id": "asia-tok", "location": "Tokyo", "ip": "52.94.8.118", "port": 25200},
            {"id": "asia-seo", "location": "Seoul", "ip": "35.71.109.128", "port": 25200},
            {"id": "asia-sgp", "location": "Singapore", "ip": "35.71.118.128", "port": 25200},
            {"id": "asia-syd", "location": "Sydney", "ip": "35.71.97.129", "port": 25200},
            {"id": "asia-mum", "location": "Mumbai", "ip": "35.71.100.130", "port": 25200}
        ],
        "SA": [
            {"id": "sa-sao", "location": "São Paulo", "ip": "35.71.106.104", "port": 25200}
        ],
        "ME": [
            {"id": "me-bhr", "location": "Bahrain", "ip": "35.71.99.128", "port": 25200}
        ]
    },
    "marvel-rivals": {
        "EU": [
            {"id": "eu-ire", "location": "Dublin", "ip": "52.94.76.1", "port": 443},
            {"id": "eu-lon", "location": "London", "ip": "52.94.77.1", "port": 443},
            {"id": "eu-par", "location": "Paris", "ip": "52.94.78.1", "port": 443},
            {"id": "eu-fra", "location": "Frankfurt", "ip": "52.94.79.1", "port": 443},
            {"id": "eu-sto", "location": "Stockholm", "ip": "52.94.80.1", "port": 443}
        ],
        "NA": [
            {"id": "na-vir", "location": "Virginia", "ip": "52.94.81.1", "port": 443},
            {"id": "na-ohi", "location": "Ohio", "ip": "52.94.82.1", "port": 443},
            {"id": "na-cal", "location": "California", "ip": "52.94.83.1", "port": 443},
            {"id": "na-ore", "location": "Oregon", "ip": "52.94.84.1", "port": 443}
        ],
        "ASIA": [
            {"id": "asia-tok", "location": "Tokyo", "ip": "52.94.85.1", "port": 443},
            {"id": "asia-seo", "location": "Seoul", "ip": "52.94.86.1", "port": 443},
            {"id": "asia-sgp", "location": "Singapore", "ip": "52.94.87.1", "port": 443},
            {"id": "asia-syd", "location": "Sydney", "ip": "52.94.88.1", "port": 443},
            {"id": "asia-mum", "location": "Mumbai", "ip": "52.94.89.1", "port": 443}
        ],
        "SA": [
            {"id": "sa-sao", "location": "São Paulo", "ip": "52.94.90.1", "port": 443}
        ],
        "ME": [
            {"id": "me-bhr", "location": "Bahrain", "ip": "52.94.91.1", "port": 443}
        ]
    },
    "valorant": {
        "EU": [
            {"id": "eu-lon", "location": "London", "ip": "104.160.141.3", "port": 443},
            {"id": "eu-par", "location": "Paris", "ip": "162.249.72.1", "port": 443},
            {"id": "eu-fra", "location": "Frankfurt", "ip": "162.249.73.1", "port": 443},
            {"id": "eu-sto", "location": "Stockholm", "ip": "162.249.74.1", "port": 443},
            {"id": "eu-war", "location": "Warsaw", "ip": "162.249.75.1", "port": 443}
        ],
        "NA": [
            {"id": "na-ash", "location": "Ashburn", "ip": "104.160.131.3", "port": 443},
            {"id": "na-chi", "location": "Chicago", "ip": "104.160.136.3", "port": 443},
            {"id": "na-dal", "location": "Dallas", "ip": "104.160.151.182", "port": 443},
            {"id": "na-lax", "location": "Los Angeles", "ip": "104.160.159.1", "port": 443},
            {"id": "na-atl", "location": "Atlanta", "ip": "104.160.156.1", "port": 443},
            {"id": "na-sea", "location": "Seattle", "ip": "104.160.158.1", "port": 443}
        ],
        "ASIA": [
            {"id": "asia-tok", "location": "Tokyo", "ip": "104.160.129.1", "port": 443},
            {"id": "asia-seo", "location": "Seoul", "ip": "104.160.142.1", "port": 443},
            {"id": "asia-sgp", "location": "Singapore", "ip": "151.106.248.1", "port": 443},
            {"id": "asia-hkg", "location": "Hong Kong", "ip": "104.160.144.1", "port": 443},
            {"id": "asia-mum", "location": "Mumbai", "ip": "151.106.246.1", "port": 443},
            {"id": "asia-syd", "location": "Sydney", "ip": "43.229.64.1", "port": 443}
        ],
        "SA": [
            {"id": "sa-sao", "location": "São Paulo", "ip": "104.160.152.1", "port": 443},
            {"id": "sa-scl", "location": "Santiago", "ip": "104.160.154.1", "port": 443}
        ],
        "ME": [
            {"id": "me-bhr", "location": "Bahrain", "ip": "104.160.146.1", "port": 443}
        ]
    },
    "fortnite": {
        "EU": [
            {"id": "eu-lon", "location": "London", "ip": "18.133.162.190", "port": 443},
            {"id": "eu-fra", "location": "Frankfurt", "ip": "3.66.90.29", "port": 443},
            {"id": "eu-par", "location": "Paris", "ip": "13.37.148.3", "port": 443},
            {"id": "eu-sto", "location": "Stockholm", "ip": "15.237.20.100", "port": 443}
        ],
        "NA": [
            {"id": "na-east", "location": "Virginia", "ip": "3.129.132.114", "port": 443},
            {"id": "na-east2", "location": "Ohio", "ip": "44.192.143.240", "port": 443},
            {"id": "na-west", "location": "Oregon", "ip": "44.237.247.68", "port": 443},
            {"id": "na-west2", "location": "California", "ip": "3.101.95.110", "port": 443}
        ],
        "ASIA": [
            {"id": "asia-tok", "location": "Tokyo", "ip": "35.72.18.106", "port": 443},
            {"id": "asia-syd", "location": "Sydney", "ip": "3.25.159.13", "port": 443}
        ],
        "SA": [
            {"id": "sa-sao", "location": "São Paulo", "ip": "15.228.25.140", "port": 443}
        ],
        "ME": [
            {"id": "me-bhr", "location": "Bahrain", "ip": "15.184.13.113", "port": 443}
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

# Supported games
GAMES = {
    "overwatch-2": {
        "name": "Overwatch 2",
        "short": "OW2"
    },
    "call-of-duty": {
        "name": "Call of Duty",
        "short": "CoD"
    },
    "counter-strike-2": {
        "name": "Counter-Strike 2",
        "short": "CS2"
    },
    "battlefield-6": {
        "name": "Battlefield 6",
        "short": "BF6"
    },
    "marvel-rivals": {
        "name": "Marvel Rivals",
        "short": "MR"
    },
    "valorant": {
        "name": "Valorant",
        "short": "VAL"
    },
    "fortnite": {
        "name": "Fortnite",
        "short": "FN"
    }
}
