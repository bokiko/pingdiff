"""
PingDiff GUI
Modern, professional interface with sleek design
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
import math
from typing import List, Optional

from config import COLORS, REGIONS, REGION_NAMES, APP_VERSION
from ping_tester import test_all_servers, get_best_server, get_connection_quality, PingResult
from api_client import APIClient


class ModernButton(tk.Canvas):
    """Modern flat button with hover effects"""

    def __init__(self, parent, text, command, width=200, height=44,
                 bg_color=None, hover_color=None, text_color="#ffffff",
                 font_size=11, **kwargs):
        super().__init__(parent, width=width, height=height,
                        bg=COLORS["bg"], highlightthickness=0, **kwargs)

        self.bg_color = bg_color or COLORS["accent"]
        self.hover_color = hover_color or COLORS["accent_hover"]
        self.text_color = text_color
        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.font_size = font_size
        self._disabled = False

        self._draw()

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _draw(self, hover=False):
        self.delete("all")
        color = self.hover_color if hover and not self._disabled else self.bg_color
        if self._disabled:
            color = COLORS["text_dim"]

        # Draw rounded rectangle
        radius = 8
        self._round_rect(2, 2, self.width-2, self.height-2, radius, color)

        # Draw text
        self.create_text(
            self.width // 2, self.height // 2,
            text=self.text,
            fill=self.text_color if not self._disabled else COLORS["text_muted"],
            font=("Segoe UI Semibold", self.font_size)
        )

    def _round_rect(self, x1, y1, x2, y2, radius, color):
        """Draw a rounded rectangle"""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        self.create_polygon(points, fill=color, smooth=True)

    def _on_enter(self, event):
        if not self._disabled:
            self._draw(hover=True)
            self.config(cursor="hand2")

    def _on_leave(self, event):
        self._draw(hover=False)
        self.config(cursor="")

    def _on_click(self, event):
        if not self._disabled and self.command:
            self.command()

    def set_disabled(self, disabled):
        self._disabled = disabled
        self._draw()


class CircularProgress(tk.Canvas):
    """Modern circular progress indicator with glow effect"""

    def __init__(self, parent, size=200, **kwargs):
        super().__init__(parent, width=size, height=size,
                        bg=COLORS["bg"], highlightthickness=0, **kwargs)
        self.size = size
        self.progress = 0
        self.status_text = "Ready"
        self.sub_text = "Select region & run test"
        self.ping_value = ""
        self._draw()

    def _draw(self):
        self.delete("all")

        center = self.size // 2
        radius = (self.size - 40) // 2
        thickness = 8

        # Background track (dark)
        self._draw_arc(center, radius, thickness, 360, COLORS["border"])

        # Progress arc with gradient effect
        if self.progress > 0:
            extent = 3.6 * self.progress

            # Determine color based on completion
            if self.progress >= 100:
                color = COLORS["success"]
            else:
                color = COLORS["accent"]

            self._draw_arc(center, radius, thickness, extent, color, start=90)

            # Glow effect
            if self.progress < 100:
                glow_color = COLORS["accent_light"]
                self.create_oval(
                    center - radius - 2, center - radius - 2,
                    center + radius + 2, center + radius + 2,
                    outline=glow_color, width=1
                )

        # Center content
        if self.ping_value:
            # Large ping value
            self.create_text(
                center, center - 15,
                text=self.ping_value,
                fill=COLORS["text"],
                font=("Segoe UI", 28, "bold")
            )
            # "ms" label
            self.create_text(
                center, center + 20,
                text="ms",
                fill=COLORS["text_muted"],
                font=("Segoe UI", 12)
            )
        else:
            # Status text
            self.create_text(
                center, center - 8,
                text=self.status_text,
                fill=COLORS["text"],
                font=("Segoe UI", 14, "bold")
            )

        # Sub text
        if self.sub_text:
            self.create_text(
                center, center + 45,
                text=self.sub_text,
                fill=COLORS["text_muted"],
                font=("Segoe UI", 9)
            )

    def _draw_arc(self, center, radius, thickness, extent, color, start=90):
        """Draw an arc"""
        self.create_arc(
            center - radius, center - radius,
            center + radius, center + radius,
            start=start, extent=-extent,
            outline=color, width=thickness, style="arc"
        )

    def set_progress(self, value: float, status: str = "", sub_text: str = "", ping: str = ""):
        self.progress = min(100, max(0, value))
        if status:
            self.status_text = status
        if sub_text is not None:
            self.sub_text = sub_text
        self.ping_value = ping
        self._draw()

    def reset(self):
        self.progress = 0
        self.status_text = "Ready"
        self.sub_text = "Select region & run test"
        self.ping_value = ""
        self._draw()


class ModernCard(tk.Frame):
    """Modern card container with border"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["card"], **kwargs)
        self.configure(highlightbackground=COLORS["border"],
                      highlightthickness=1)


class PingDiffApp:
    """Main application window"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"PingDiff")
        self.root.geometry("480x700")
        self.root.minsize(420, 600)
        self.root.resizable(True, True)
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
        self.dashboard_url = None

        self._setup_styles()
        self._create_widgets()
        self._load_initial_data()

    def _setup_styles(self):
        """Configure ttk styles for modern dark theme"""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure(".", background=COLORS["bg"], foreground=COLORS["text"])
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"])

        # Modern combobox
        style.configure("TCombobox",
                       fieldbackground=COLORS["card"],
                       background=COLORS["card"],
                       foreground=COLORS["text"],
                       arrowcolor=COLORS["text_muted"],
                       borderwidth=0,
                       padding=8)

        style.map("TCombobox",
                 fieldbackground=[("readonly", COLORS["card"])],
                 selectbackground=[("readonly", COLORS["accent"])],
                 selectforeground=[("readonly", COLORS["text"])])

        # Scrollbar
        style.configure("TScrollbar",
                       background=COLORS["card"],
                       troughcolor=COLORS["bg"],
                       borderwidth=0,
                       arrowsize=0)

    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=COLORS["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=20)

        # Header section
        self._create_header(main_frame)

        # ISP Info Card
        self._create_isp_card(main_frame)

        # Region selector
        self._create_region_selector(main_frame)

        # Progress section
        self._create_progress_section(main_frame)

        # Run button
        self._create_run_button(main_frame)

        # Results section (scrollable)
        self._create_results_section(main_frame)

        # Footer
        self._create_footer(main_frame)

    def _create_header(self, parent):
        """Create header with logo and title"""
        header = tk.Frame(parent, bg=COLORS["bg"])
        header.pack(fill=tk.X, pady=(0, 20))

        # Title row
        title_row = tk.Frame(header, bg=COLORS["bg"])
        title_row.pack(fill=tk.X)

        # Logo/Title
        title = tk.Label(title_row, text="PingDiff",
                        font=("Segoe UI", 26, "bold"),
                        bg=COLORS["bg"], fg=COLORS["text"])
        title.pack(side=tk.LEFT)

        # Version badge
        version_frame = tk.Frame(title_row, bg=COLORS["accent"], padx=8, pady=2)
        version_frame.pack(side=tk.LEFT, padx=(12, 0), pady=(8, 0))

        tk.Label(version_frame, text=f"v{APP_VERSION}",
                font=("Segoe UI", 8, "bold"),
                bg=COLORS["accent"], fg="#ffffff").pack()

        # Subtitle
        subtitle = tk.Label(header, text="Game Server Connection Tester",
                           font=("Segoe UI", 11),
                           bg=COLORS["bg"], fg=COLORS["text_muted"])
        subtitle.pack(anchor=tk.W, pady=(4, 0))

    def _create_isp_card(self, parent):
        """Create ISP information card"""
        card = ModernCard(parent, padx=16, pady=12)
        card.pack(fill=tk.X, pady=(0, 16))

        # ISP row
        isp_row = tk.Frame(card, bg=COLORS["card"])
        isp_row.pack(fill=tk.X)

        tk.Label(isp_row, text="ISP",
                font=("Segoe UI", 9),
                bg=COLORS["card"], fg=COLORS["text_dim"]).pack(side=tk.LEFT)

        self.isp_label = tk.Label(isp_row, text="Detecting...",
                                  font=("Segoe UI", 10, "bold"),
                                  bg=COLORS["card"], fg=COLORS["text"])
        self.isp_label.pack(side=tk.RIGHT)

        # Separator
        sep = tk.Frame(card, bg=COLORS["border"], height=1)
        sep.pack(fill=tk.X, pady=8)

        # Location row
        loc_row = tk.Frame(card, bg=COLORS["card"])
        loc_row.pack(fill=tk.X)

        tk.Label(loc_row, text="Location",
                font=("Segoe UI", 9),
                bg=COLORS["card"], fg=COLORS["text_dim"]).pack(side=tk.LEFT)

        self.location_label = tk.Label(loc_row, text="...",
                                       font=("Segoe UI", 10),
                                       bg=COLORS["card"], fg=COLORS["text_secondary"])
        self.location_label.pack(side=tk.RIGHT)

    def _create_region_selector(self, parent):
        """Create region selection dropdown"""
        region_frame = tk.Frame(parent, bg=COLORS["bg"])
        region_frame.pack(fill=tk.X, pady=(0, 16))

        tk.Label(region_frame, text="Server Region",
                font=("Segoe UI", 10, "bold"),
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor=tk.W, pady=(0, 8))

        # Combobox with region names
        self.region_var = tk.StringVar(value="EU")
        region_display = [f"{r} - {REGION_NAMES.get(r, r)}" for r in REGIONS]

        self.region_combo = ttk.Combobox(region_frame,
                                         textvariable=self.region_var,
                                         values=REGIONS,
                                         state="readonly",
                                         font=("Segoe UI", 10),
                                         width=20)
        self.region_combo.pack(anchor=tk.W)

    def _create_progress_section(self, parent):
        """Create progress indicator section"""
        progress_frame = tk.Frame(parent, bg=COLORS["bg"])
        progress_frame.pack(pady=16)

        self.progress_gauge = CircularProgress(progress_frame, size=180)
        self.progress_gauge.pack()

    def _create_run_button(self, parent):
        """Create the run test button"""
        self.test_button = ModernButton(
            parent,
            text="Run Test",
            command=self._start_test,
            width=200,
            height=48,
            font_size=12
        )
        self.test_button.pack(pady=(8, 20))

    def _create_results_section(self, parent):
        """Create scrollable results section"""
        # Results header
        results_header = tk.Frame(parent, bg=COLORS["bg"])
        results_header.pack(fill=tk.X, pady=(0, 8))

        tk.Label(results_header, text="Results",
                font=("Segoe UI", 12, "bold"),
                bg=COLORS["bg"], fg=COLORS["text"]).pack(side=tk.LEFT)

        self.results_count = tk.Label(results_header, text="",
                                      font=("Segoe UI", 10),
                                      bg=COLORS["bg"], fg=COLORS["text_muted"])
        self.results_count.pack(side=tk.RIGHT)

        # Results container with scrollbar
        results_wrapper = tk.Frame(parent, bg=COLORS["bg"])
        results_wrapper.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(results_wrapper, bg=COLORS["bg"],
                          highlightthickness=0, height=200)
        scrollbar = ttk.Scrollbar(results_wrapper, orient="vertical",
                                  command=canvas.yview)

        self.results_frame = tk.Frame(canvas, bg=COLORS["bg"])
        self.results_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Initial empty state
        self.no_results_label = tk.Label(self.results_frame,
                                         text="Run a test to see results",
                                         font=("Segoe UI", 10),
                                         bg=COLORS["bg"], fg=COLORS["text_dim"])
        self.no_results_label.pack(pady=30)

    def _create_footer(self, parent):
        """Create footer with links"""
        footer = tk.Frame(parent, bg=COLORS["bg"])
        footer.pack(fill=tk.X, pady=(16, 0))

        # Left side - Dashboard button
        self.dashboard_btn = ModernButton(
            footer,
            text="Open Dashboard",
            command=self._open_dashboard,
            width=140,
            height=36,
            bg_color=COLORS["card"],
            hover_color=COLORS["card_hover"],
            font_size=10
        )
        self.dashboard_btn.pack(side=tk.LEFT)

        # GitHub button
        github_btn = ModernButton(
            footer,
            text="GitHub",
            command=lambda: webbrowser.open("https://github.com/bokiko/pingdiff"),
            width=80,
            height=36,
            bg_color=COLORS["card"],
            hover_color=COLORS["card_hover"],
            font_size=10
        )
        github_btn.pack(side=tk.LEFT, padx=(8, 0))

        # Right side - Game label
        tk.Label(footer, text="Overwatch 2",
                font=("Segoe UI", 9),
                bg=COLORS["bg"], fg=COLORS["text_dim"]).pack(side=tk.RIGHT)

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

        self.isp_label.config(text=isp)
        self.location_label.config(text=f"{city}, {country}")

    def _start_test(self):
        """Start the ping test in a background thread"""
        if self.is_testing:
            return

        self.is_testing = True
        self.test_button.set_disabled(True)
        self.progress_gauge.set_progress(0, "Testing...", "Connecting to servers...")

        region = self.region_var.get()
        servers = self.servers.get(region, [])

        if not servers:
            messagebox.showerror("Error", f"No servers found for region: {region}")
            self.is_testing = False
            self.test_button.set_disabled(False)
            self.progress_gauge.reset()
            return

        def run_test():
            def progress_callback(current, total, result):
                progress = (current / total) * 100
                if result.packet_loss < 100:
                    status = f"{current}/{total}"
                    sub = f"Testing {result.server_location}..."
                else:
                    status = f"{current}/{total}"
                    sub = f"{result.server_location}: Failed"

                self.root.after(0, lambda: self.progress_gauge.set_progress(
                    progress, status, sub
                ))

            self.results = test_all_servers(servers, callback=progress_callback)
            self.root.after(0, self._show_results)

        thread = threading.Thread(target=run_test, daemon=True)
        thread.start()

    def _show_results(self):
        """Display test results"""
        self.is_testing = False
        self.test_button.set_disabled(False)

        # Update gauge with best result
        best = get_best_server(self.results)
        if best:
            quality = get_connection_quality(best)
            self.progress_gauge.set_progress(
                100, "", f"Best: {best.server_location}",
                ping=f"{best.ping_avg:.0f}"
            )
        else:
            self.progress_gauge.set_progress(100, "Failed", "All servers unreachable")

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not self.results:
            tk.Label(self.results_frame,
                    text="No results available",
                    font=("Segoe UI", 10),
                    bg=COLORS["bg"], fg=COLORS["text_dim"]).pack(pady=30)
            return

        # Update results count
        successful = len([r for r in self.results if r.packet_loss < 100])
        self.results_count.config(text=f"{successful}/{len(self.results)} servers")

        # Sort results (successful first, then by ping)
        sorted_results = sorted(self.results,
                               key=lambda r: (r.packet_loss >= 100, r.ping_avg))

        # Display each result
        for i, result in enumerate(sorted_results):
            self._create_result_row(result, i == 0 and result.packet_loss < 100)

        # Submit results to API
        self._submit_results()

    def _create_result_row(self, result: PingResult, is_best: bool = False):
        """Create a single result row"""
        is_failed = result.packet_loss >= 100

        # Card background
        bg = COLORS["card"] if not is_best else "#1a3a2a"
        border = COLORS["border"] if not is_best else COLORS["success"]

        row = tk.Frame(self.results_frame, bg=bg,
                      highlightbackground=border, highlightthickness=1)
        row.pack(fill=tk.X, pady=4, padx=2)

        inner = tk.Frame(row, bg=bg, padx=12, pady=10)
        inner.pack(fill=tk.X)

        # Left side - Server info
        left = tk.Frame(inner, bg=bg)
        left.pack(side=tk.LEFT, fill=tk.Y)

        # Best badge
        if is_best:
            badge = tk.Frame(left, bg=COLORS["success"], padx=6, pady=1)
            badge.pack(anchor=tk.W, pady=(0, 4))
            tk.Label(badge, text="BEST", font=("Segoe UI", 7, "bold"),
                    bg=COLORS["success"], fg="#ffffff").pack()

        # Server name
        name_color = COLORS["error"] if is_failed else COLORS["text"]
        tk.Label(left, text=result.server_location,
                font=("Segoe UI", 11, "bold"),
                bg=bg, fg=name_color).pack(anchor=tk.W)

        # Right side - Stats
        right = tk.Frame(inner, bg=bg)
        right.pack(side=tk.RIGHT, fill=tk.Y)

        if is_failed:
            tk.Label(right, text="FAILED",
                    font=("Segoe UI", 12, "bold"),
                    bg=bg, fg=COLORS["error"]).pack(anchor=tk.E)
        else:
            # Ping value
            quality = get_connection_quality(result)
            if quality in ["Excellent", "Good"]:
                ping_color = COLORS["success"]
            elif quality == "Fair":
                ping_color = COLORS["warning"]
            else:
                ping_color = COLORS["error"]

            ping_frame = tk.Frame(right, bg=bg)
            ping_frame.pack(anchor=tk.E)

            tk.Label(ping_frame, text=f"{result.ping_avg:.0f}",
                    font=("Segoe UI", 16, "bold"),
                    bg=bg, fg=ping_color).pack(side=tk.LEFT)
            tk.Label(ping_frame, text=" ms",
                    font=("Segoe UI", 10),
                    bg=bg, fg=COLORS["text_muted"]).pack(side=tk.LEFT, pady=(4, 0))

            # Jitter and packet loss
            stats = tk.Frame(right, bg=bg)
            stats.pack(anchor=tk.E)
            tk.Label(stats, text=f"{result.jitter:.1f}ms jitter",
                    font=("Segoe UI", 9),
                    bg=bg, fg=COLORS["text_dim"]).pack(side=tk.LEFT)

            if result.packet_loss > 0:
                tk.Label(stats, text=f" | {result.packet_loss:.0f}% loss",
                        font=("Segoe UI", 9),
                        bg=bg, fg=COLORS["warning"]).pack(side=tk.LEFT)

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

        thread = threading.Thread(target=submit, daemon=True)
        thread.start()

    def _open_dashboard(self):
        """Open the dashboard in browser"""
        if self.dashboard_url:
            # Ensure full URL (API returns relative path like /dashboard?result=...)
            if self.dashboard_url.startswith('/'):
                url = f"{self.api.base_url}{self.dashboard_url}"
            else:
                url = self.dashboard_url
            webbrowser.open(url)
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
