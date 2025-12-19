"""
PingDiff GUI
Simple tkinter interface for running ping tests
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
from typing import List, Optional

from config import COLORS, REGIONS, APP_VERSION
from ping_tester import test_all_servers, get_best_server, get_connection_quality, PingResult
from api_client import APIClient


class PingDiffApp:
    """Main application window"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"PingDiff v{APP_VERSION}")
        self.root.geometry("550x750")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg"])

        # Set icon if available
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass

        self.api = APIClient()
        self.servers = {}
        self.current_game = "overwatch-2"
        self.results: List[PingResult] = []
        self.isp_info = {}
        self.is_testing = False

        self._setup_styles()
        self._create_widgets()
        self._load_initial_data()

    def _setup_styles(self):
        """Configure ttk styles for dark theme"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure dark theme colors
        style.configure(".", background=COLORS["bg"], foreground=COLORS["text"])
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"])
        style.configure("TButton",
                       background=COLORS["accent"],
                       foreground=COLORS["text"],
                       padding=(20, 10))
        style.map("TButton",
                 background=[("active", "#2563eb"), ("disabled", "#4b5563")])

        style.configure("Card.TFrame", background=COLORS["card"])
        style.configure("Card.TLabel", background=COLORS["card"], foreground=COLORS["text"])
        style.configure("Muted.TLabel", background=COLORS["bg"], foreground=COLORS["text_muted"])
        style.configure("Success.TLabel", background=COLORS["card"], foreground=COLORS["success"])
        style.configure("Warning.TLabel", background=COLORS["card"], foreground=COLORS["warning"])
        style.configure("Error.TLabel", background=COLORS["card"], foreground=COLORS["error"])

        # Combobox style
        style.configure("TCombobox",
                       fieldbackground=COLORS["card"],
                       background=COLORS["card"],
                       foreground=COLORS["text"])

        # Progressbar style
        style.configure("TProgressbar",
                       background=COLORS["accent"],
                       troughcolor=COLORS["card"])

    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        title_label = ttk.Label(header_frame, text="PingDiff",
                               font=("Segoe UI", 24, "bold"))
        title_label.pack(side=tk.LEFT)

        subtitle = ttk.Label(header_frame,
                            text="Overwatch 2 Connection Tester",
                            style="Muted.TLabel",
                            font=("Segoe UI", 10))
        subtitle.pack(side=tk.LEFT, padx=(10, 0), pady=(10, 0))

        # ISP Info Card
        isp_card = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        isp_card.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(isp_card, text="Your Connection",
                 style="Card.TLabel",
                 font=("Segoe UI", 11, "bold")).pack(anchor=tk.W)

        self.isp_label = ttk.Label(isp_card, text="Detecting...",
                                   style="Card.TLabel",
                                   font=("Segoe UI", 10))
        self.isp_label.pack(anchor=tk.W, pady=(5, 0))

        self.location_label = ttk.Label(isp_card, text="",
                                        style="Card.TLabel",
                                        font=("Segoe UI", 10))
        self.location_label.pack(anchor=tk.W)

        # Region Selection
        region_frame = ttk.Frame(main_frame)
        region_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(region_frame, text="Select Region:",
                 font=("Segoe UI", 11)).pack(side=tk.LEFT)

        self.region_var = tk.StringVar(value="EU")
        self.region_combo = ttk.Combobox(region_frame,
                                         textvariable=self.region_var,
                                         values=REGIONS,
                                         state="readonly",
                                         width=15)
        self.region_combo.pack(side=tk.LEFT, padx=(10, 0))

        # Test Button
        self.test_button = ttk.Button(main_frame,
                                      text="Run Test",
                                      command=self._start_test)
        self.test_button.pack(fill=tk.X, pady=(0, 15))

        # Progress
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=(0, 15))

        self.progress_label = ttk.Label(self.progress_frame,
                                       text="",
                                       style="Muted.TLabel")
        self.progress_label.pack(anchor=tk.W)

        self.progress_bar = ttk.Progressbar(self.progress_frame,
                                            mode="determinate",
                                            length=510)
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        self.progress_bar.pack_forget()  # Hide initially

        # Results Frame
        self.results_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=15)
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.results_frame, text="Results",
                 style="Card.TLabel",
                 font=("Segoe UI", 11, "bold")).pack(anchor=tk.W)

        # Results will be populated here
        self.results_container = ttk.Frame(self.results_frame, style="Card.TFrame")
        self.results_container.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.no_results_label = ttk.Label(self.results_container,
                                          text="Click 'Run Test' to check your connection",
                                          style="Card.TLabel")
        self.no_results_label.pack(pady=20)

        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(15, 0))

        self.dashboard_button = ttk.Button(footer_frame,
                                           text="View on Dashboard",
                                           command=self._open_dashboard,
                                           state=tk.DISABLED)
        self.dashboard_button.pack(side=tk.LEFT)

        version_label = ttk.Label(footer_frame,
                                 text=f"v{APP_VERSION}",
                                 style="Muted.TLabel")
        version_label.pack(side=tk.RIGHT)

    def _load_initial_data(self):
        """Load ISP info and servers on startup"""
        def load():
            # Get ISP info
            self.isp_info = self.api.get_isp_info()
            self.root.after(0, self._update_isp_display)

            # Get servers
            self.servers = self.api.get_servers(self.current_game)

        thread = threading.Thread(target=load, daemon=True)
        thread.start()

    def _update_isp_display(self):
        """Update ISP information display"""
        isp = self.isp_info.get("isp", "Unknown")
        country = self.isp_info.get("country", "Unknown")
        city = self.isp_info.get("city", "Unknown")

        self.isp_label.config(text=f"ISP: {isp}")
        self.location_label.config(text=f"Location: {city}, {country}")

    def _start_test(self):
        """Start the ping test in a background thread"""
        if self.is_testing:
            return

        self.is_testing = True
        self.test_button.config(state=tk.DISABLED)
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        self.progress_bar["value"] = 0

        region = self.region_var.get()
        servers = self.servers.get(region, [])

        if not servers:
            messagebox.showerror("Error", f"No servers found for region: {region}")
            self.is_testing = False
            self.test_button.config(state=tk.NORMAL)
            self.progress_bar.pack_forget()
            return

        def run_test():
            def progress_callback(current, total, result):
                progress = (current / total) * 100
                self.root.after(0, lambda: self._update_progress(current, total, result))

            self.results = test_all_servers(servers, callback=progress_callback)
            self.root.after(0, self._show_results)

        thread = threading.Thread(target=run_test, daemon=True)
        thread.start()

    def _update_progress(self, current: int, total: int, result: PingResult):
        """Update progress bar and label"""
        self.progress_bar["value"] = (current / total) * 100
        status = f"{result.ping_avg}ms" if result.packet_loss < 100 else "Failed"
        self.progress_label.config(
            text=f"Testing {current}/{total}: {result.server_location} - {status}"
        )

    def _show_results(self):
        """Display test results"""
        self.is_testing = False
        self.test_button.config(state=tk.NORMAL)
        self.progress_bar.pack_forget()
        self.progress_label.config(text="")

        # Clear previous results
        for widget in self.results_container.winfo_children():
            widget.destroy()

        if not self.results:
            ttk.Label(self.results_container,
                     text="No results available",
                     style="Card.TLabel").pack(pady=20)
            return

        # Best server recommendation
        best = get_best_server(self.results)
        if best:
            best_frame = ttk.Frame(self.results_container, style="Card.TFrame")
            best_frame.pack(fill=tk.X, pady=(0, 10))

            quality = get_connection_quality(best)
            quality_color = {
                "Excellent": "Success.TLabel",
                "Good": "Success.TLabel",
                "Fair": "Warning.TLabel",
                "Poor": "Warning.TLabel",
                "Bad": "Error.TLabel"
            }.get(quality, "Card.TLabel")

            ttk.Label(best_frame,
                     text=f"RECOMMENDED: {best.server_location}",
                     style="Success.TLabel",
                     font=("Segoe UI", 11, "bold")).pack(anchor=tk.W)

            # Detailed stats for best server
            stats_text = f"Ping: {best.ping_avg}ms (min: {best.ping_min}ms, max: {best.ping_max}ms)"
            ttk.Label(best_frame, text=stats_text,
                     style="Card.TLabel",
                     font=("Segoe UI", 9)).pack(anchor=tk.W, pady=(2, 0))

            stats_text2 = f"Jitter: {best.jitter}ms | Packet Loss: {best.packet_loss}% | Quality: {quality}"
            ttk.Label(best_frame, text=stats_text2,
                     style=quality_color,
                     font=("Segoe UI", 9)).pack(anchor=tk.W)

        # Separator
        ttk.Separator(self.results_container, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # All results header
        header_frame = ttk.Frame(self.results_container, style="Card.TFrame")
        header_frame.pack(fill=tk.X)

        ttk.Label(header_frame, text="All Servers:",
                 style="Card.TLabel",
                 font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)

        # Column headers
        col_header = ttk.Frame(self.results_container, style="Card.TFrame")
        col_header.pack(fill=tk.X, pady=(5, 2))

        tk.Label(col_header, text="Server", bg=COLORS["card"], fg=COLORS["text_muted"],
                font=("Segoe UI", 8), anchor=tk.W, width=18).pack(side=tk.LEFT)
        tk.Label(col_header, text="Ping", bg=COLORS["card"], fg=COLORS["text_muted"],
                font=("Segoe UI", 8), width=8).pack(side=tk.LEFT)
        tk.Label(col_header, text="Jitter", bg=COLORS["card"], fg=COLORS["text_muted"],
                font=("Segoe UI", 8), width=8).pack(side=tk.LEFT)
        tk.Label(col_header, text="Loss", bg=COLORS["card"], fg=COLORS["text_muted"],
                font=("Segoe UI", 8), width=8).pack(side=tk.LEFT)
        tk.Label(col_header, text="Status", bg=COLORS["card"], fg=COLORS["text_muted"],
                font=("Segoe UI", 8), width=10).pack(side=tk.LEFT)

        # Create scrollable frame for results
        canvas = tk.Canvas(self.results_container, bg=COLORS["card"],
                          highlightthickness=0, height=250)
        scrollbar = ttk.Scrollbar(self.results_container, orient=tk.VERTICAL,
                                  command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Card.TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Sort by ping (failed servers last)
        sorted_results = sorted(self.results,
                               key=lambda r: (r.packet_loss >= 100, r.ping_avg))

        for result in sorted_results:
            row = ttk.Frame(scrollable_frame, style="Card.TFrame")
            row.pack(fill=tk.X, pady=3)

            # Check if server failed
            is_failed = result.packet_loss >= 100

            # Color based on quality
            if is_failed:
                color = COLORS["error"]
                quality = "FAILED"
            else:
                quality = get_connection_quality(result)
                if quality in ["Excellent", "Good"]:
                    color = COLORS["success"]
                elif quality == "Fair":
                    color = COLORS["warning"]
                else:
                    color = COLORS["error"]

            # Server name
            name_label = tk.Label(row, text=result.server_location,
                                 bg=COLORS["card"], fg=COLORS["text"],
                                 font=("Segoe UI", 9), anchor=tk.W, width=18)
            name_label.pack(side=tk.LEFT)

            # Ping
            ping_text = f"{result.ping_avg}ms" if not is_failed else "---"
            ping_label = tk.Label(row, text=ping_text,
                                 bg=COLORS["card"], fg=color,
                                 font=("Segoe UI", 9, "bold"), width=8)
            ping_label.pack(side=tk.LEFT)

            # Jitter
            jitter_text = f"{result.jitter}ms" if not is_failed else "---"
            jitter_label = tk.Label(row, text=jitter_text,
                                   bg=COLORS["card"], fg=COLORS["text_muted"],
                                   font=("Segoe UI", 9), width=8)
            jitter_label.pack(side=tk.LEFT)

            # Packet loss
            loss_text = f"{result.packet_loss}%"
            loss_color = COLORS["success"] if result.packet_loss == 0 else COLORS["error"]
            loss_label = tk.Label(row, text=loss_text,
                                 bg=COLORS["card"], fg=loss_color,
                                 font=("Segoe UI", 9), width=8)
            loss_label.pack(side=tk.LEFT)

            # Status/Quality
            status_label = tk.Label(row, text=quality,
                                   bg=COLORS["card"], fg=color,
                                   font=("Segoe UI", 9, "bold"), width=10)
            status_label.pack(side=tk.LEFT)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Summary stats
        summary_frame = ttk.Frame(self.results_container, style="Card.TFrame")
        summary_frame.pack(fill=tk.X, pady=(10, 0))

        working_servers = [r for r in self.results if r.packet_loss < 100]
        failed_servers = [r for r in self.results if r.packet_loss >= 100]

        summary_text = f"Tested {len(self.results)} servers: {len(working_servers)} OK, {len(failed_servers)} failed"
        ttk.Label(summary_frame, text=summary_text,
                 style="Muted.TLabel",
                 font=("Segoe UI", 9)).pack(anchor=tk.W)

        # Submit results to API
        self._submit_results()

    def _submit_results(self):
        """Submit results to the API"""
        def submit():
            results_data = []
            for r in self.results:
                results_data.append({
                    "server_id": r.server_id,
                    "server_location": r.server_location,
                    "ping_avg": r.ping_avg,
                    "ping_min": r.ping_min,
                    "ping_max": r.ping_max,
                    "jitter": r.jitter,
                    "packet_loss": r.packet_loss,
                    "raw_times": r.raw_times
                })

            response = self.api.submit_results(results_data, self.isp_info)

            if response.get("success"):
                self.dashboard_url = response.get("dashboard_url")
                self.root.after(0, lambda: self.dashboard_button.config(state=tk.NORMAL))

        thread = threading.Thread(target=submit, daemon=True)
        thread.start()

    def _open_dashboard(self):
        """Open the dashboard in browser"""
        if hasattr(self, 'dashboard_url') and self.dashboard_url:
            webbrowser.open(self.dashboard_url)
        else:
            webbrowser.open(f"{self.api.base_url}/dashboard")

    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    app = PingDiffApp()
    app.run()


if __name__ == "__main__":
    main()
