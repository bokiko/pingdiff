"""
Unit tests for ping_tester.py — core ping logic.
No network calls are made; all tests use synthetic data.
"""

import sys
import os
import pytest

# Add desktop/src to path so we can import without packaging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ping_tester import (
    validate_ip,
    calculate_jitter,
    get_best_server,
    get_connection_quality,
    PingResult,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_result(
    server_id="sv1",
    location="Frankfurt",
    ip="1.2.3.4",
    ping_avg=50.0,
    ping_min=45.0,
    ping_max=60.0,
    jitter=3.0,
    packet_loss=0.0,
    successful_pings=10,
    total_pings=10,
    raw_times=None,
    region="EU",
    error=None,
) -> PingResult:
    return PingResult(
        server_id=server_id,
        server_location=location,
        ip_address=ip,
        ping_avg=ping_avg,
        ping_min=ping_min,
        ping_max=ping_max,
        jitter=jitter,
        packet_loss=packet_loss,
        successful_pings=successful_pings,
        total_pings=total_pings,
        raw_times=raw_times or [],
        region=region,
        error=error,
    )


# ---------------------------------------------------------------------------
# validate_ip
# ---------------------------------------------------------------------------

class TestValidateIp:
    def test_valid_ipv4(self):
        assert validate_ip("8.8.8.8") is True

    def test_valid_ipv6(self):
        assert validate_ip("2001:4860:4860::8888") is True

    def test_empty_string(self):
        assert validate_ip("") is False

    def test_none(self):
        assert validate_ip(None) is False

    def test_hostname_rejected(self):
        # Hostnames are not valid IP addresses
        assert validate_ip("google.com") is False

    def test_ip_with_port_rejected(self):
        assert validate_ip("8.8.8.8:53") is False

    def test_partial_ip_rejected(self):
        assert validate_ip("8.8.8") is False

    def test_injection_attempt_rejected(self):
        assert validate_ip("8.8.8.8; rm -rf /") is False

    def test_loopback_allowed(self):
        assert validate_ip("127.0.0.1") is True

    def test_broadcast_allowed(self):
        assert validate_ip("255.255.255.255") is True


# ---------------------------------------------------------------------------
# calculate_jitter
# ---------------------------------------------------------------------------

class TestCalculateJitter:
    def test_empty_list(self):
        assert calculate_jitter([]) == 0.0

    def test_single_element(self):
        assert calculate_jitter([50.0]) == 0.0

    def test_zero_jitter(self):
        # Identical pings → jitter = 0
        result = calculate_jitter([30.0, 30.0, 30.0, 30.0])
        assert result == 0.0

    def test_constant_increase(self):
        # [10, 20, 30] → diffs = [10, 10] → avg = 10
        result = calculate_jitter([10.0, 20.0, 30.0])
        assert result == 10.0

    def test_alternating(self):
        # [10, 20, 10, 20] → diffs = [10, 10, 10] → avg = 10
        result = calculate_jitter([10.0, 20.0, 10.0, 20.0])
        assert result == 10.0

    def test_high_jitter(self):
        # [1, 100, 1, 100] → diffs = [99, 99, 99] → avg = 99
        result = calculate_jitter([1.0, 100.0, 1.0, 100.0])
        assert result == 99.0

    def test_returns_float(self):
        result = calculate_jitter([10.0, 15.0])
        assert isinstance(result, float)


# ---------------------------------------------------------------------------
# get_best_server
# ---------------------------------------------------------------------------

class TestGetBestServer:
    def test_empty_list(self):
        assert get_best_server([]) is None

    def test_all_timeout(self):
        results = [
            make_result(server_id="s1", packet_loss=100.0),
            make_result(server_id="s2", packet_loss=100.0),
        ]
        assert get_best_server(results) is None

    def test_single_valid_server(self):
        r = make_result(server_id="s1", ping_avg=40.0, packet_loss=0.0)
        assert get_best_server([r]) is r

    def test_picks_lowest_ping(self):
        r1 = make_result(server_id="s1", ping_avg=80.0, packet_loss=0.0)
        r2 = make_result(server_id="s2", ping_avg=40.0, packet_loss=0.0)
        r3 = make_result(server_id="s3", ping_avg=120.0, packet_loss=0.0)
        best = get_best_server([r1, r2, r3])
        assert best.server_id == "s2"

    def test_packet_loss_beats_lower_ping(self):
        # s1 has lower ping but some packet loss → s2 should win
        r1 = make_result(server_id="s1", ping_avg=10.0, packet_loss=5.0)
        r2 = make_result(server_id="s2", ping_avg=50.0, packet_loss=0.0)
        best = get_best_server([r1, r2])
        assert best.server_id == "s2"

    def test_excludes_100_percent_loss(self):
        r1 = make_result(server_id="s1", ping_avg=10.0, packet_loss=100.0)
        r2 = make_result(server_id="s2", ping_avg=50.0, packet_loss=0.0)
        best = get_best_server([r1, r2])
        assert best.server_id == "s2"

    def test_mixed_loss_picks_lower_loss_first(self):
        r1 = make_result(server_id="s1", ping_avg=30.0, packet_loss=10.0)
        r2 = make_result(server_id="s2", ping_avg=25.0, packet_loss=2.0)
        best = get_best_server([r1, r2])
        assert best.server_id == "s2"


# ---------------------------------------------------------------------------
# get_connection_quality
# ---------------------------------------------------------------------------

class TestGetConnectionQuality:
    def test_excellent(self):
        r = make_result(ping_avg=20.0, packet_loss=0.0)
        assert get_connection_quality(r) == "Excellent"

    def test_good(self):
        r = make_result(ping_avg=50.0, packet_loss=0.0)
        assert get_connection_quality(r) == "Good"

    def test_fair(self):
        r = make_result(ping_avg=80.0, packet_loss=0.0)
        assert get_connection_quality(r) == "Fair"

    def test_poor_high_ping(self):
        r = make_result(ping_avg=130.0, packet_loss=0.0)
        assert get_connection_quality(r) == "Poor"

    def test_bad_very_high_ping(self):
        r = make_result(ping_avg=200.0, packet_loss=0.0)
        assert get_connection_quality(r) == "Bad"

    def test_bad_high_packet_loss(self):
        r = make_result(ping_avg=20.0, packet_loss=10.0)
        assert get_connection_quality(r) == "Bad"

    def test_poor_moderate_loss(self):
        r = make_result(ping_avg=20.0, packet_loss=3.0)
        assert get_connection_quality(r) == "Poor"

    def test_boundary_excellent_good(self):
        # 29ms → Excellent, 30ms → Good
        assert get_connection_quality(make_result(ping_avg=29.0, packet_loss=0.0)) == "Excellent"
        assert get_connection_quality(make_result(ping_avg=30.0, packet_loss=0.0)) == "Good"

    def test_boundary_good_fair(self):
        assert get_connection_quality(make_result(ping_avg=59.0, packet_loss=0.0)) == "Good"
        assert get_connection_quality(make_result(ping_avg=60.0, packet_loss=0.0)) == "Fair"

    def test_boundary_fair_poor(self):
        assert get_connection_quality(make_result(ping_avg=99.0, packet_loss=0.0)) == "Fair"
        assert get_connection_quality(make_result(ping_avg=100.0, packet_loss=0.0)) == "Poor"

    def test_boundary_poor_bad(self):
        assert get_connection_quality(make_result(ping_avg=149.0, packet_loss=0.0)) == "Poor"
        assert get_connection_quality(make_result(ping_avg=150.0, packet_loss=0.0)) == "Bad"
