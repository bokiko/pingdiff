"""
PingDiff CLI Mode
Command-line ping testing without the GUI — for power users and scripting.

Usage:
    python main.py --cli --game cs2 --region EU
    python main.py --cli --json --best
    python main.py --list-games
    python main.py --version
"""

import argparse
import csv
import io
import json
import os
import sys
import time
from datetime import datetime
from typing import List, Optional

from config import APP_VERSION, GAMES, DEFAULT_SERVERS, REGIONS, REGION_NAMES
from ping_tester import test_all_servers, get_best_server, get_connection_quality, PingResult


# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_RED = "\033[41m"

    @staticmethod
    def supports_color() -> bool:
        """Check if terminal supports ANSI colors."""
        if sys.platform == "win32":
            return "ANSICON" in os.environ or "WT_SESSION" in os.environ
        return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def colorize(text: str, color: str) -> str:
    """Apply ANSI color if terminal supports it."""
    if not Colors.supports_color():
        return text
    return f"{color}{text}{Colors.RESET}"


def quality_color(quality: str) -> str:
    """Get ANSI color for connection quality rating."""
    mapping = {
        "Excellent": Colors.GREEN,
        "Good": Colors.GREEN,
        "Fair": Colors.YELLOW,
        "Poor": Colors.RED,
        "Bad": Colors.RED,
    }
    return mapping.get(quality, Colors.WHITE)


def format_ping(value: float) -> str:
    """Format ping value with color based on threshold."""
    if value == 0:
        return colorize("---", Colors.DIM)
    if value < 30:
        return colorize(f"{value:.0f}ms", Colors.GREEN)
    elif value < 60:
        return colorize(f"{value:.0f}ms", Colors.GREEN)
    elif value < 100:
        return colorize(f"{value:.0f}ms", Colors.YELLOW)
    elif value < 150:
        return colorize(f"{value:.0f}ms", Colors.RED)
    else:
        return colorize(f"{value:.0f}ms", Colors.RED)


def format_loss(value: float) -> str:
    """Format packet loss with color."""
    if value == 0:
        return colorize("0%", Colors.GREEN)
    elif value < 2:
        return colorize(f"{value:.1f}%", Colors.YELLOW)
    else:
        return colorize(f"{value:.1f}%", Colors.RED)


def print_table(results: List[PingResult]) -> None:
    """Print results as a formatted table."""
    if not results:
        print("No results.")
        return

    # Sort by ping (best first), unreachable last
    results = sorted(results, key=lambda r: (r.packet_loss >= 100, r.ping_avg))

    # Column widths
    header = f"{'Server':<20} {'Region':<8} {'Avg':>7} {'Min':>7} {'Max':>7} {'Jitter':>7} {'Loss':>7} {'Quality':<10}"
    separator = "-" * 75

    print()
    print(colorize(header, Colors.BOLD))
    print(colorize(separator, Colors.DIM))

    for r in results:
        quality = get_connection_quality(r)
        qcolor = quality_color(quality)

        if r.packet_loss >= 100:
            line = f"{r.server_location:<20} {r.region:<8} {'---':>7} {'---':>7} {'---':>7} {'---':>7} {'100%':>7} {colorize('Timeout', Colors.RED):<10}"
        else:
            line = (
                f"{r.server_location:<20} "
                f"{r.region:<8} "
                f"{format_ping(r.ping_avg):>17} "
                f"{format_ping(r.ping_min):>17} "
                f"{format_ping(r.ping_max):>17} "
                f"{format_ping(r.jitter):>17} "
                f"{format_loss(r.packet_loss):>17} "
                f"{colorize(quality, qcolor):<10}"
            )

        print(line)

    print()


def print_best(results: List[PingResult]) -> None:
    """Print only the best server."""
    best = get_best_server(results)
    if not best:
        print("No reachable servers found.")
        return

    quality = get_connection_quality(best)
    print()
    print(colorize("Best Server", Colors.BOLD))
    print(colorize("-" * 40, Colors.DIM))
    print(f"  Server:      {best.server_location} ({best.region})")
    print(f"  Ping:        {best.ping_avg:.0f}ms (min {best.ping_min:.0f}, max {best.ping_max:.0f})")
    print(f"  Jitter:      {best.jitter:.1f}ms")
    print(f"  Packet Loss: {best.packet_loss:.1f}%")
    print(f"  Quality:     {colorize(quality, quality_color(quality))}")
    print()


def results_to_json(results: List[PingResult], best_only: bool = False) -> str:
    """Convert results to JSON string."""
    if best_only:
        best = get_best_server(results)
        if not best:
            return json.dumps({"error": "No reachable servers"}, indent=2)
        results = [best]

    data = []
    for r in results:
        data.append({
            "server": r.server_location,
            "server_id": r.server_id,
            "region": r.region,
            "ip": r.ip_address,
            "ping_avg": r.ping_avg,
            "ping_min": r.ping_min,
            "ping_max": r.ping_max,
            "jitter": r.jitter,
            "packet_loss": r.packet_loss,
            "quality": get_connection_quality(r),
            "successful_pings": r.successful_pings,
            "total_pings": r.total_pings,
            "error": r.error,
        })

    return json.dumps(data, indent=2)


def results_to_csv(results: List[PingResult], best_only: bool = False) -> str:
    """Convert results to CSV string."""
    if best_only:
        best = get_best_server(results)
        if not best:
            return ""
        results = [best]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "server", "region", "ip", "ping_avg", "ping_min", "ping_max",
        "jitter", "packet_loss", "quality", "successful_pings", "total_pings",
    ])
    for r in results:
        writer.writerow([
            r.server_location, r.region, r.ip_address,
            f"{r.ping_avg:.2f}", f"{r.ping_min:.2f}", f"{r.ping_max:.2f}",
            f"{r.jitter:.2f}", f"{r.packet_loss:.2f}",
            get_connection_quality(r), r.successful_pings, r.total_pings,
        ])
    return output.getvalue().rstrip("\n")


def progress_callback(completed: int, total: int, result: PingResult) -> None:
    """Show progress during testing."""
    bar_width = 30
    filled = int(bar_width * completed / total)
    bar = "█" * filled + "░" * (bar_width - filled)

    status = f"{result.server_location}: {result.ping_avg:.0f}ms" if result.ping_avg > 0 else f"{result.server_location}: timeout"

    sys.stdout.write(f"\r  [{bar}] {completed}/{total} — {status:<30}")
    sys.stdout.flush()

    if completed == total:
        sys.stdout.write("\n")


def list_games() -> None:
    """Print available games."""
    print()
    print(colorize("Available Games", Colors.BOLD))
    print(colorize("-" * 40, Colors.DIM))
    for slug, info in sorted(GAMES.items()):
        regions = list(DEFAULT_SERVERS.get(slug, {}).keys())
        server_count = sum(len(v) for v in DEFAULT_SERVERS.get(slug, {}).values())
        print(f"  {info['short']:<6} {info['name']:<22} {server_count:>3} servers  [{', '.join(regions)}]")
    print()
    print(f"Use: --game <slug>  (e.g. --game {list(GAMES.keys())[0]})")
    print()


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="pingdiff",
        description="PingDiff — Test your ping to game servers",
        epilog="Examples:\n"
               "  pingdiff --cli --game counter-strike-2 --region EU\n"
               "  pingdiff --cli --json --best\n"
               "  pingdiff --list-games\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--cli", action="store_true",
                        help="Run in CLI mode (no GUI)")
    parser.add_argument("--game", type=str, default="overwatch-2",
                        help="Game slug to test (default: overwatch-2)")
    parser.add_argument("--region", type=str, default=None,
                        choices=["EU", "NA", "ASIA", "SA", "ME"],
                        help="Filter by region")
    parser.add_argument("--count", type=int, default=10,
                        help="Number of pings per server (default: 10)")
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="Output results as JSON")
    parser.add_argument("--csv", action="store_true", dest="csv_output",
                        help="Output results as CSV")
    parser.add_argument("--best", action="store_true",
                        help="Show only the best server")
    parser.add_argument("--version", action="version",
                        version=f"PingDiff v{APP_VERSION}")
    parser.add_argument("--list-games", action="store_true",
                        help="List available games and exit")
    parser.add_argument("--no-color", action="store_true",
                        help="Disable colored output")
    parser.add_argument("--watch", action="store_true",
                        help="Continuously ping servers and refresh results (use --interval to set seconds, default 30)")
    parser.add_argument("--interval", type=int, default=30,
                        help="Seconds between updates in watch mode (default: 30)")

    return parser


def run_watch(game_info: dict, all_servers: list, args: argparse.Namespace) -> int:
    """Run continuous ping testing in watch mode. Returns exit code."""
    try:
        while True:
            os.system("clear" if os.name != "nt" else "cls")

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(colorize(f"PingDiff — {game_info['name']} [Watch Mode]", Colors.BOLD))
            print(colorize(f"Last update: {now}", Colors.DIM))
            print()

            results = test_all_servers(all_servers, ping_count=args.count, callback=progress_callback)

            print_table(results)

            best = get_best_server(results)
            if best:
                quality = get_connection_quality(best)
                print(f"  Recommended: {colorize(best.server_location, Colors.CYAN)} ({best.region}) — "
                      f"{colorize(f'{best.ping_avg:.0f}ms', quality_color(quality))} "
                      f"[{colorize(quality, quality_color(quality))}]")
                print()

            for remaining in range(args.interval, 0, -1):
                sys.stdout.write(f"\r  Next update in {remaining}s  [Ctrl+C to stop]  ")
                sys.stdout.flush()
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n  Watch mode stopped. Goodbye!")
        return 0


def run_cli(args: argparse.Namespace) -> int:
    """Execute CLI mode. Returns exit code."""

    if args.no_color:
        Colors.supports_color = staticmethod(lambda: False)

    if args.list_games:
        list_games()
        return 0

    # Validate game
    if args.game not in GAMES:
        print(f"Error: Unknown game '{args.game}'. Use --list-games to see options.")
        return 1

    game_info = GAMES[args.game]
    servers_by_region = DEFAULT_SERVERS.get(args.game, {})

    if not servers_by_region:
        print(f"Error: No servers configured for {game_info['name']}.")
        return 1

    # Filter by region
    if args.region:
        if args.region not in servers_by_region:
            print(f"Error: No {args.region} servers for {game_info['name']}.")
            available = ", ".join(servers_by_region.keys())
            print(f"Available regions: {available}")
            return 1
        servers_by_region = {args.region: servers_by_region[args.region]}

    # Flatten servers and tag with region
    all_servers = []
    for region, servers in servers_by_region.items():
        for s in servers:
            s_copy = dict(s)
            s_copy["region"] = region
            all_servers.append(s_copy)

    total = len(all_servers)
    region_label = args.region or "all regions"

    if args.watch:
        if args.json_output:
            print("Warning: --json is not supported with --watch, ignoring --json.")
            args.json_output = False
        if args.csv_output:
            print("Warning: --csv is not supported with --watch, ignoring --csv.")
            args.csv_output = False
        return run_watch(game_info, all_servers, args)

    if args.json_output and args.csv_output:
        print("Warning: --json and --csv both set, using --json.", file=sys.stderr)
        args.csv_output = False

    machine_output = args.json_output or args.csv_output

    if not machine_output:
        print()
        print(colorize(f"PingDiff v{APP_VERSION}", Colors.BOLD))
        print(f"Testing {colorize(game_info['name'], Colors.CYAN)} — {total} servers ({region_label})")
        print(f"Sending {args.count} pings per server...")
        print()

    # Run tests
    callback = progress_callback if not machine_output else None
    results = test_all_servers(all_servers, ping_count=args.count, callback=callback)

    # Output
    if args.json_output:
        print(results_to_json(results, best_only=args.best))
    elif args.csv_output:
        print(results_to_csv(results, best_only=args.best))
    elif args.best:
        print_best(results)
    else:
        print_table(results)

        # Also show best server summary
        best = get_best_server(results)
        if best:
            quality = get_connection_quality(best)
            print(f"  Recommended: {colorize(best.server_location, Colors.CYAN)} ({best.region}) — "
                  f"{colorize(f'{best.ping_avg:.0f}ms', quality_color(quality))} "
                  f"[{colorize(quality, quality_color(quality))}]")
            print()

    return 0
