"""
PingDiff GUI
Modern tkinter interface with visual progress gauge
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
import math
from typing import List, Optional

from config import COLORS, REGIONS, APP_VERSION
from ping_tester import test_all_servers, get_best_server, get_connection_quality, PingResult
from api_client import APIClient


class CircularProgress(tk.Canvas):
    """Circular progress gauge widget"""

    def __init__(self, parent, size=200, **kwargs):
        super().__init__(parent, width=size, height=size,
                        bg=COLORS["bg"], highlightthickness=0, **kwargs)
        self.size = size
        self.progress = 0
        self.status_text = "Ready"
        self.sub_text = ""
        self._draw()

    def _draw(self):
        self.delete("all")

        center = self.size // 2
        radius = (self.size - 20) // 2
        thickness = 12

        # Background circle (dark)
        self.create_oval(
            center - radius, center - radius,
            center + radius, center + radius,
            outline="#2a2a2a", width=thickness
        )

        # Progress arc
        if self.progress > 0:
            extent = -3.6 * self.progress  # Negative for clockwise

            # Color based on progress
            if self.progress < 100:
                color = COLORS["accent"]
            else:
                color = COLORS["success"]

            self.create_arc(
                center - radius, center - radius,
                center + radius, center + radius,
                start=90, extent=extent,
                outline=color, width=thickness, style="arc"
            )

        # Center text - status
        self.create_text(
            center, center - 15,
            text=self.status_text,
            fill=COLORS["text"],
            font=("Segoe UI", 14, "bold")
        )

        # Sub text
        if self.sub_text:
            self.create_text(
                center, center + 15,
                text=self.sub_text,
                fill=COLORS["text_muted"],
                font=("Segoe UI", 10)
            )

    def set_progress(self, value: float, status: str = "", sub_text: str = ""):
        self.progress = min(100, max(0, value))
        if status:
            self.status_text = status
        if sub_text is not None:
            self.sub_text = sub_text
        self._draw()

    def reset(self):
        self.progress = 0
        self.status_text = "Ready"
        self.sub_text = "Click Run Test to start"
        self._draw()


class PingDiffApp:
    """Main application window"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"PingDiff v{APP_VERSION}")
        self.root.geometry("480x700")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg"])

        # Try to set icon
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

        style.configure(".", background=COLORS["bg"], foreground=COLORS["text"])
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"])

        # Modern button
        style.configure("TButton",
                       background=COLORS["accent"],
                       foreground="white",
                       padding=(20, 12),
                       font=("Segoe UI", 11, "bold"))
        style.map("TButton",
                 background=[("active", "#2563eb"), ("disabled", "#4b5563")])

        style.configure("Card.TFrame", background=COLORS["card"])
        style.configure("Card.TLabel", background=COLORS["card"], foreground=COLORS["text"])
        style.configure("Muted.TLabel", foreground=COLORS["text_muted"])
        style.configure("Success.TLabel", foreground=COLORS["success"])
        style.configure("Warning.TLabel", foreground=COLORS["warning"])
        style.configure("Error.TLabel", foreground=COLORS["error"])

        style.configure("TCombobox",
                       fieldbackground=COLORS["card"],
                       background=COLORS["card"])

    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding=24)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 20))

        title = tk.Label(header, text="PingDiff",
                        font=("Segoe UI", 28, "bold"),
                        bg=COLORS["bg"], fg=COLORS["text"])
        title.pack(side=tk.LEFT)

        subtitle = tk.Label(header, text="Overwatch 2",
                           font=("Segoe UI", 12),
                           bg=COLORS["bg"], fg=COLORS["text_muted"])
        subtitle.pack(side=tk.LEFT, padx=(12, 0), pady=(12, 0))

        # ISP Info Card
        isp_card = tk.Frame(main_frame, bg=COLORS["card"], padx=16, pady=12)
        isp_card.pack(fill=tk.X, pady=(0, 16))

        self.isp_label = tk.Label(isp_card, text="Detecting ISP...",
                                  font=("Segoe UI", 11),
                                  bg=COLORS["card"], fg=COLORS["text"])
        self.isp_label.pack(anchor=tk.W)

        self.location_label = tk.Label(isp_card, text="",
                                       font=("Segoe UI", 10),
                                       bg=COLORS["card"], fg=COLORS["text_muted"])
        self.location_label.pack(anchor=tk.W)

        # Region Selection
        region_frame = ttk.Frame(main_frame)
        region_frame.pack(fill=tk.X, pady=(0, 16))

        tk.Label(region_frame, text="Region:",
                font=("Segoe UI", 11),
                bg=COLORS["bg"], fg=COLORS["text"]).pack(side=tk.LEFT)

        self.region_var = tk.StringVar(value="EU")
        self.region_combo = ttk.Combobox(region_frame,
                                         textvariable=self.region_var,
                                         values=REGIONS,
                                         state="readonly",
                                         width=12,
                                         font=("Segoe UI", 10))
        self.region_combo.pack(side=tk.LEFT, padx=(10, 0))

        # Progress Gauge
        gauge_frame = ttk.Frame(main_frame)
        gauge_frame.pack(pady=16)

        self.progress_gauge = CircularProgress(gauge_frame, size=180)
        self.progress_gauge.pack()
        self.progress_gauge.reset()

        # Test Button
        self.test_button = ttk.Button(main_frame,
                                      text="Run Test",
                                      command=self._start_test)
        self.test_button.pack(fill=tk.X, pady=(16, 0))

        # Results Frame
        self.results_frame = tk.Frame(main_frame, bg=COLORS["card"])
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=(16, 0))

        # Results header
        results_header = tk.Frame(self.results_frame, bg=COLORS["card"], padx=12, pady=8)
        results_header.pack(fill=tk.X)

        tk.Label(results_header, text="Results",
                font=("Segoe UI", 12, "bold"),
                bg=COLORS["card"], fg=COLORS["text"]).pack(anchor=tk.W)

        # Results container (scrollable)
        self.results_container = tk.Frame(self.results_frame, bg=COLORS["card"], padx=12, pady=8)
        self.results_container.pack(fill=tk.BOTH, expand=True)

        self.no_results_label = tk.Label(self.results_container,
                                         text="Results will appear here",
                                         font=("Segoe UI", 10),
                                         bg=COLORS["card"], fg=COLORS["text_muted"])
        self.no_results_label.pack(pady=20)

        # Footer
        footer = ttk.Frame(main_frame)
        footer.pack(fill=tk.X, pady=(16, 0))

        self.dashboard_button = ttk.Button(footer,
                                           text="Open Dashboard",
                                           command=self._open_dashboard)
        self.dashboard_button.pack(side=tk.LEFT)
        self.dashboard_button.configure(state=tk.DISABLED)

        version_label = tk.Label(footer, text=f"v{APP_VERSION}",
                                font=("Segoe UI", 9),
                                bg=COLORS["bg"], fg=COLORS["text_muted"])
        version_label.pack(side=tk.RIGHT)

    def _load_initial_data(self):
        """Load ISP info and servers on startup"""
        def load():
            self.isp_info = self.api.get_isp_info()
            self.root.after(0, self._update_isp_display)
            self.servers = self.api.get_servers(self.current_game)

        thread = threading.Thread(target=load, daemon=True)
        thread.start()

    def _update_isp_display(self):
        """Update ISP information display"""
        isp = self.isp_info.get("isp", "Unknown")
        country = self.isp_info.get("country", "Unknown")
        city = self.isp_info.get("city", "Unknown")

        self.isp_label.config(text=f"ISP: {isp}")
        self.location_label.config(text=f"{city}, {country}")

    def _start_test(self):
        """Start the ping test in a background thread"""
        if self.is_testing:
            return

        self.is_testing = True
        self.test_button.config(state=tk.DISABLED)
        self.progress_gauge.set_progress(0, "Testing...", "Starting...")

        region = self.region_var.get()
        servers = self.servers.get(region, [])

        if not servers:
            messagebox.showerror("Error", f"No servers found for region: {region}")
            self.is_testing = False
            self.test_button.config(state=tk.NORMAL)
            self.progress_gauge.reset()
            return

        def run_test():
            def progress_callback(current, total, result):
                progress = (current / total) * 100
                status = f"{result.ping_avg}ms" if result.packet_loss < 100 else "Failed"
                self.root.after(0, lambda: self.progress_gauge.set_progress(
                    progress,
                    f"{current}/{total}",
                    f"{result.server_location}: {status}"
                ))

            self.results = test_all_servers(servers, callback=progress_callback)
            self.root.after(0, self._show_results)

        thread = threading.Thread(target=run_test, daemon=True)
        thread.start()

    def _show_results(self):
        """Display test results"""
        self.is_testing = False
        self.test_button.config(state=tk.NORMAL)

        # Update gauge to complete
        best = get_best_server(self.results)
        if best:
            quality = get_connection_quality(best)
            self.progress_gauge.set_progress(100, f"{best.ping_avg}ms", f"{best.server_location} • {quality}")
        else:
            self.progress_gauge.set_progress(100, "No Result", "All servers failed")

        # Clear previous results
        for widget in self.results_container.winfo_children():
            widget.destroy()

        if not self.results:
            tk.Label(self.results_container,
                    text="No results available",
                    font=("Segoe UI", 10),
                    bg=COLORS["card"], fg=COLORS["text_muted"]).pack(pady=20)
            return

        # Sort results (successful first, then by ping)
        sorted_results = sorted(self.results,
                               key=lambda r: (r.packet_loss >= 100, r.ping_avg))

        # Display each result
        for result in sorted_results:
            self._create_result_row(result)

        # Submit results to API
        self._submit_results()

    def _create_result_row(self, result: PingResult):
        """Create a single result row"""
        is_failed = result.packet_loss >= 100

        row = tk.Frame(self.results_container, bg=COLORS["card"])
        row.pack(fill=tk.X, pady=4)

        # Server name
        name_color = COLORS["error"] if is_failed else COLORS["text"]
        tk.Label(row, text=result.server_location,
                font=("Segoe UI", 10),
                bg=COLORS["card"], fg=name_color,
                anchor=tk.W, width=20).pack(side=tk.LEFT)

        # Stats
        if is_failed:
            stats_text = "FAILED"
            stats_color = COLORS["error"]
        else:
            quality = get_connection_quality(result)
            if quality in ["Excellent", "Good"]:
                stats_color = COLORS["success"]
            elif quality == "Fair":
                stats_color = COLORS["warning"]
            else:
                stats_color = COLORS["error"]

            stats_text = f"{result.ping_avg}ms  •  {result.jitter}ms jitter  •  {result.packet_loss}% loss"

        tk.Label(row, text=stats_text,
                font=("Segoe UI", 9),
                bg=COLORS["card"], fg=stats_color,
                anchor=tk.E).pack(side=tk.RIGHT)

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
