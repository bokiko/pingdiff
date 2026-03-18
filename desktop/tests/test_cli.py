"""
Unit tests for cli.py — CLI logic, sorting, filtering, and output formatting.
No network calls; no GUI dependencies.
"""

import sys
import os
import io
import json
import csv

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ping_tester import PingResult
from cli import (
    sort_results,
    filter_by_max_ping,
    results_to_json,
    results_to_csv,
    Colors,
    colorize,
    format_ping,
    format_loss,
    build_parser,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_result(
    server_id="sv1",
    location="Frankfurt",
    region="EU",
    ping_avg=50.0,
    ping_min=45.0,
    ping_max=60.0,
    jitter=3.0,
    packet_loss=0.0,
    successful_pings=10,
    total_pings=10,
) -> PingResult:
    return PingResult(
        server_id=server_id,
        server_location=location,
        ip_address="1.2.3.4",
        ping_avg=ping_avg,
        ping_min=ping_min,
        ping_max=ping_max,
        jitter=jitter,
        packet_loss=packet_loss,
        successful_pings=successful_pings,
        total_pings=total_pings,
        raw_times=[],
        region=region,
        error=None,
    )


# ---------------------------------------------------------------------------
# sort_results
# ---------------------------------------------------------------------------

class TestSortResults:
    def _make_set(self):
        return [
            make_result(server_id="s1", location="Berlin",   region="EU", ping_avg=80.0, jitter=5.0, packet_loss=0.0),
            make_result(server_id="s2", location="Amsterdam", region="EU", ping_avg=30.0, jitter=2.0, packet_loss=0.0),
            make_result(server_id="s3", location="Tokyo",     region="ASIA", ping_avg=55.0, jitter=8.0, packet_loss=0.0),
        ]

    def test_sort_by_ping(self):
        results = self._make_set()
        sorted_r = sort_results(results, "ping")
        pings = [r.ping_avg for r in sorted_r]
        assert pings == sorted(pings)

    def test_sort_by_jitter(self):
        results = self._make_set()
        sorted_r = sort_results(results, "jitter")
        jitters = [r.jitter for r in sorted_r]
        assert jitters == sorted(jitters)

    def test_sort_by_location(self):
        results = self._make_set()
        sorted_r = sort_results(results, "location")
        locs = [r.server_location.lower() for r in sorted_r]
        assert locs == sorted(locs)

    def test_sort_by_region(self):
        results = self._make_set()
        sorted_r = sort_results(results, "region")
        regions = [r.region for r in sorted_r]
        assert regions == sorted(regions)

    def test_timeouts_sorted_last(self):
        r_ok = make_result(server_id="ok", ping_avg=200.0, packet_loss=0.0)
        r_timeout = make_result(server_id="to", ping_avg=10.0, packet_loss=100.0)
        sorted_r = sort_results([r_timeout, r_ok], "ping")
        assert sorted_r[0].server_id == "ok"
        assert sorted_r[-1].server_id == "to"

    def test_unknown_sort_key_defaults_to_ping(self):
        results = self._make_set()
        # Should not raise; falls back to ping sort
        sorted_r = sort_results(results, "nonexistent")
        pings = [r.ping_avg for r in sorted_r]
        assert pings == sorted(pings)


# ---------------------------------------------------------------------------
# filter_by_max_ping
# ---------------------------------------------------------------------------

class TestFilterByMaxPing:
    def test_all_pass(self):
        results = [make_result(ping_avg=50.0), make_result(ping_avg=80.0)]
        filtered = filter_by_max_ping(results, 200.0)
        assert len(filtered) == 2

    def test_none_pass(self):
        results = [make_result(ping_avg=150.0), make_result(ping_avg=200.0)]
        filtered = filter_by_max_ping(results, 100.0)
        assert filtered == []

    def test_excludes_timeouts_regardless(self):
        r_ok = make_result(server_id="ok", ping_avg=50.0, packet_loss=0.0)
        r_to = make_result(server_id="to", ping_avg=10.0, packet_loss=100.0)
        filtered = filter_by_max_ping([r_ok, r_to], 500.0)
        ids = [r.server_id for r in filtered]
        assert "ok" in ids
        assert "to" not in ids

    def test_boundary_inclusive(self):
        r = make_result(ping_avg=80.0, packet_loss=0.0)
        assert len(filter_by_max_ping([r], 80.0)) == 1

    def test_boundary_exclusive(self):
        r = make_result(ping_avg=80.1, packet_loss=0.0)
        assert len(filter_by_max_ping([r], 80.0)) == 0


# ---------------------------------------------------------------------------
# results_to_json
# ---------------------------------------------------------------------------

class TestResultsToJson:
    def test_returns_valid_json(self):
        results = [make_result()]
        output = results_to_json(results)
        data = json.loads(output)
        assert isinstance(data, list)

    def test_contains_expected_fields(self):
        r = make_result(server_id="s1", location="LA", region="NA", ping_avg=42.5)
        data = json.loads(results_to_json([r]))
        item = data[0]
        assert item["server"] == "LA"
        assert item["region"] == "NA"
        assert item["ping_avg"] == 42.5
        assert "quality" in item

    def test_best_only_returns_single_item(self):
        results = [
            make_result(server_id="s1", ping_avg=100.0, packet_loss=0.0),
            make_result(server_id="s2", ping_avg=30.0, packet_loss=0.0),
        ]
        data = json.loads(results_to_json(results, best_only=True))
        assert len(data) == 1
        assert data[0]["server_id"] == "s2"

    def test_no_reachable_servers_returns_error(self):
        results = [make_result(packet_loss=100.0)]
        data = json.loads(results_to_json(results, best_only=True))
        assert "error" in data

    def test_empty_list_returns_empty_array(self):
        data = json.loads(results_to_json([]))
        assert data == []


# ---------------------------------------------------------------------------
# results_to_csv
# ---------------------------------------------------------------------------

class TestResultsToCsv:
    def test_returns_parseable_csv(self):
        results = [make_result(location="NYC", region="NA", ping_avg=35.0)]
        output = results_to_csv(results)
        reader = csv.DictReader(io.StringIO(output))
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["server"] == "NYC"
        assert rows[0]["region"] == "NA"

    def test_header_row_present(self):
        output = results_to_csv([make_result()])
        first_line = output.split("\n")[0]
        assert "server" in first_line
        assert "ping_avg" in first_line

    def test_best_only_returns_one_row(self):
        results = [
            make_result(server_id="s1", ping_avg=100.0, packet_loss=0.0),
            make_result(server_id="s2", ping_avg=30.0, packet_loss=0.0),
        ]
        output = results_to_csv(results, best_only=True)
        reader = csv.DictReader(io.StringIO(output))
        rows = list(reader)
        assert len(rows) == 1

    def test_empty_on_no_best(self):
        results = [make_result(packet_loss=100.0)]
        output = results_to_csv(results, best_only=True)
        assert output == ""

    def test_multiple_rows(self):
        results = [make_result(location=f"Server{i}") for i in range(5)]
        output = results_to_csv(results)
        reader = csv.DictReader(io.StringIO(output))
        rows = list(reader)
        assert len(rows) == 5


# ---------------------------------------------------------------------------
# colorize / format helpers
# ---------------------------------------------------------------------------

class TestColorHelpers:
    def test_colorize_no_color_mode(self, monkeypatch):
        monkeypatch.setattr(Colors, "supports_color", staticmethod(lambda: False))
        assert colorize("hello", Colors.GREEN) == "hello"

    def test_format_ping_zero(self, monkeypatch):
        monkeypatch.setattr(Colors, "supports_color", staticmethod(lambda: False))
        assert format_ping(0) == "---"

    def test_format_ping_good(self, monkeypatch):
        monkeypatch.setattr(Colors, "supports_color", staticmethod(lambda: False))
        assert "25ms" in format_ping(25)

    def test_format_loss_zero(self, monkeypatch):
        monkeypatch.setattr(Colors, "supports_color", staticmethod(lambda: False))
        assert "0%" in format_loss(0)

    def test_format_loss_nonzero(self, monkeypatch):
        monkeypatch.setattr(Colors, "supports_color", staticmethod(lambda: False))
        output = format_loss(5.0)
        assert "5.0%" in output


# ---------------------------------------------------------------------------
# build_parser
# ---------------------------------------------------------------------------

class TestBuildParser:
    def test_defaults(self):
        parser = build_parser()
        args = parser.parse_args([])
        assert args.game == "overwatch-2"
        assert args.count == 10
        assert args.sort == "ping"
        assert args.interval == 30
        assert args.max_ping is None
        assert args.output is None

    def test_cli_flag(self):
        parser = build_parser()
        args = parser.parse_args(["--cli"])
        assert args.cli is True

    def test_region_choices(self):
        parser = build_parser()
        for region in ["EU", "NA", "ASIA", "SA", "ME"]:
            args = parser.parse_args(["--region", region])
            assert args.region == region

    def test_invalid_region_raises(self):
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["--region", "INVALID"])

    def test_sort_choices(self):
        parser = build_parser()
        for sort in ["ping", "jitter", "loss", "location", "region"]:
            args = parser.parse_args(["--sort", sort])
            assert args.sort == sort

    def test_max_ping_parsed_as_float(self):
        parser = build_parser()
        args = parser.parse_args(["--max-ping", "80"])
        assert args.max_ping == 80.0

    def test_output_flag(self):
        parser = build_parser()
        args = parser.parse_args(["--output", "results.json"])
        assert args.output == "results.json"
