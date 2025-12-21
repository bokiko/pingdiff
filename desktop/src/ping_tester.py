"""
PingDiff Ping Tester
Core ping testing logic with packet loss and jitter calculation
Optimized for speed with parallel testing and hidden console
"""

import subprocess
import platform
import re
import statistics
import sys
import ipaddress
import logging
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger('PingDiff')


def validate_ip(ip: str) -> bool:
    """
    Validate that a string is a valid IPv4 or IPv6 address.
    Prevents command injection by ensuring only valid IPs are passed to ping.
    """
    if not ip or not isinstance(ip, str):
        return False

    try:
        # This will raise ValueError if ip is not valid
        ip_obj = ipaddress.ip_address(ip.strip())
        # Reject private/loopback for safety (optional, but good practice)
        # We allow these since game servers could be on various networks
        return True
    except ValueError:
        logger.warning(f"Invalid IP address rejected: {ip}")
        return False


# Windows-specific: hide console window for subprocesses
if sys.platform == 'win32':
    STARTUPINFO = subprocess.STARTUPINFO()
    STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    STARTUPINFO.wShowWindow = subprocess.SW_HIDE
    CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW
else:
    STARTUPINFO = None
    CREATE_NO_WINDOW = 0


@dataclass
class PingResult:
    """Result of a ping test to a single server"""
    server_id: str
    server_location: str
    ip_address: str
    ping_avg: float
    ping_min: float
    ping_max: float
    jitter: float
    packet_loss: float
    successful_pings: int
    total_pings: int
    raw_times: List[float]
    region: str = ""
    error: Optional[str] = None


def ping_server(ip: str, count: int = 10, timeout: int = 1) -> Dict:
    """
    Ping a server and return detailed statistics.
    Uses system ping command for reliability.
    Console window is hidden on Windows.

    Returns:
        Dict with ping_times, packet_loss, and any error
    """
    # Validate IP address to prevent command injection
    if not validate_ip(ip):
        logger.error(f"Rejected invalid IP: {ip}")
        return {
            "ping_times": [],
            "packet_loss": 100.0,
            "packets_sent": count,
            "packets_received": 0,
            "error": "Invalid IP address"
        }

    system = platform.system().lower()
    ping_times = []

    try:
        if system == "windows":
            # Windows ping command - reduced timeout for speed
            cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), ip]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=count * timeout + 5,
                startupinfo=STARTUPINFO,
                creationflags=CREATE_NO_WINDOW
            )
        else:
            # Linux/Mac ping command
            cmd = ["ping", "-c", str(count), "-W", str(timeout), ip]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=count * timeout + 5
            )

        output = result.stdout

        # Parse ping times from output
        if system == "windows":
            # Windows format: "Reply from x.x.x.x: bytes=32 time=25ms TTL=57"
            pattern = r"time[=<](\d+)ms"
        else:
            # Linux/Mac format: "64 bytes from x.x.x.x: icmp_seq=1 ttl=57 time=25.3 ms"
            pattern = r"time=(\d+\.?\d*)\s*ms"

        matches = re.findall(pattern, output)
        ping_times = [float(t) for t in matches]

        # Calculate packet loss
        packets_sent = count
        packets_received = len(ping_times)
        packet_loss = ((packets_sent - packets_received) / packets_sent) * 100

        return {
            "ping_times": ping_times,
            "packet_loss": packet_loss,
            "packets_sent": packets_sent,
            "packets_received": packets_received,
            "error": None
        }

    except subprocess.TimeoutExpired:
        return {
            "ping_times": ping_times,
            "packet_loss": 100.0,
            "packets_sent": count,
            "packets_received": len(ping_times),
            "error": "Request timed out"
        }
    except Exception as e:
        return {
            "ping_times": [],
            "packet_loss": 100.0,
            "packets_sent": count,
            "packets_received": 0,
            "error": str(e)
        }


def calculate_jitter(ping_times: List[float]) -> float:
    """
    Calculate jitter (variation in ping times).
    Jitter = average of absolute differences between consecutive pings.
    """
    if len(ping_times) < 2:
        return 0.0

    differences = []
    for i in range(1, len(ping_times)):
        diff = abs(ping_times[i] - ping_times[i-1])
        differences.append(diff)

    return round(statistics.mean(differences), 2)


def test_server(server: Dict, ping_count: int = 10, timeout: int = 1) -> PingResult:
    """
    Run a complete ping test on a server.

    Args:
        server: Dict with id, location, ip, port
        ping_count: Number of pings to send
        timeout: Timeout per ping in seconds

    Returns:
        PingResult with all statistics
    """
    ip = server["ip"]
    result = ping_server(ip, count=ping_count, timeout=timeout)

    ping_times = result["ping_times"]

    if ping_times:
        ping_avg = round(statistics.mean(ping_times), 2)
        ping_min = round(min(ping_times), 2)
        ping_max = round(max(ping_times), 2)
        jitter = calculate_jitter(ping_times)
    else:
        ping_avg = 0.0
        ping_min = 0.0
        ping_max = 0.0
        jitter = 0.0

    return PingResult(
        server_id=server["id"],
        server_location=server["location"],
        ip_address=ip,
        ping_avg=ping_avg,
        ping_min=ping_min,
        ping_max=ping_max,
        jitter=jitter,
        packet_loss=round(result["packet_loss"], 2),
        successful_pings=result["packets_received"],
        total_pings=result["packets_sent"],
        raw_times=ping_times,
        region=server.get("region", ""),
        error=result["error"]
    )


def test_all_servers(servers: List[Dict], ping_count: int = 10,
                     timeout: int = 1, callback: Optional[Callable] = None,
                     parallel: bool = True) -> List[PingResult]:
    """
    Test all servers in a list. Uses parallel testing for speed.

    Args:
        servers: List of server dicts
        ping_count: Pings per server
        timeout: Timeout per ping
        callback: Optional callback(server_index, total_servers, result) for progress
        parallel: Whether to test servers in parallel (much faster)

    Returns:
        List of PingResult objects
    """
    results = []
    total = len(servers)

    if parallel and total > 1:
        # Test servers in parallel for speed
        completed = 0
        with ThreadPoolExecutor(max_workers=min(total, 4)) as executor:
            future_to_server = {
                executor.submit(test_server, server, ping_count, timeout): server
                for server in servers
            }

            for future in as_completed(future_to_server):
                result = future.result()
                results.append(result)
                completed += 1

                if callback:
                    callback(completed, total, result)
    else:
        # Sequential testing
        for i, server in enumerate(servers):
            result = test_server(server, ping_count, timeout)
            results.append(result)

            if callback:
                callback(i + 1, total, result)

    return results


def get_best_server(results: List[PingResult]) -> Optional[PingResult]:
    """
    Find the best server based on ping and packet loss.
    Prioritizes low packet loss, then low ping.
    """
    # Filter out servers with 100% packet loss
    valid_results = [r for r in results if r.packet_loss < 100]

    if not valid_results:
        return None

    # Sort by packet loss first, then by ping
    sorted_results = sorted(valid_results, key=lambda r: (r.packet_loss, r.ping_avg))

    return sorted_results[0]


def get_connection_quality(result: PingResult) -> str:
    """
    Rate the connection quality based on ping and packet loss.

    Returns: "Excellent", "Good", "Fair", "Poor", "Bad"
    """
    if result.packet_loss > 5:
        return "Bad"
    if result.packet_loss > 2:
        return "Poor"

    ping = result.ping_avg

    if ping < 30:
        return "Excellent"
    elif ping < 60:
        return "Good"
    elif ping < 100:
        return "Fair"
    elif ping < 150:
        return "Poor"
    else:
        return "Bad"
