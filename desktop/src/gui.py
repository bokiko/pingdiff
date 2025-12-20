"""
PingDiff GUI
Apple-inspired modern interface with clean, minimal design
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
import os
import math
from typing import List, Optional

from config import COLORS, REGIONS, REGION_NAMES, APP_VERSION, GAMES
from ping_tester import test_all_servers, get_best_server, get_connection_quality, PingResult
from api_client import APIClient, Settings, get_app_data_dir


# Font configuration (SF Pro-like on Windows/Mac)
def get_font(size=13, weight="normal"):
    """Get system font similar to SF Pro"""
    family = "SF Pro Display" if os.name == "darwin" else "Segoe UI"
    return (family, size, weight)


class PillButton(tk.Canvas):
    """Modern pill-shaped button with smooth hover effect"""

    def __init__(self, parent, text, command, width=180, height=44,
                 style="primary", **kwargs):
        super().__init__(parent, width=width, height=height,
                        bg=COLORS["bg"], highlightthickness=0, **kwargs)

        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.style = style
        self._disabled = False
        self._hover = False

        self._setup_colors()
        self._draw()

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _setup_colors(self):
        if self.style == "primary":
            self.bg_color = COLORS["accent"]
            self.hover_color = COLORS["accent_hover"]
            self.text_color = "#ffffff"
        elif self.style == "secondary":
            self.bg_color = COLORS["bg_tertiary"]
            self.hover_color = COLORS["card_elevated"]
            self.text_color = COLORS["text"]
        else:  # ghost
            self.bg_color = "transparent"
            self.hover_color = COLORS["bg_secondary"]
            self.text_color = COLORS["accent"]

    def _draw(self):
        self.delete("all")

        if self._disabled:
            bg = COLORS["bg_tertiary"]
            fg = COLORS["text_dim"]
        else:
            bg = self.hover_color if self._hover else self.bg_color
            fg = self.text_color

        # Draw pill shape
        radius = self.height // 2
        if bg != "transparent":
            self._draw_pill(2, 2, self.width - 2, self.height - 2, radius, bg)

        # Draw text
        self.create_text(
            self.width // 2, self.height // 2,
            text=self.text,
            fill=fg,
            font=get_font(13, "bold" if self.style == "primary" else "normal")
        )

    def _draw_pill(self, x1, y1, x2, y2, radius, color):
        """Draw a pill/capsule shape"""
        # Left semicircle
        self.create_arc(x1, y1, x1 + radius * 2, y2, start=90, extent=180,
                       fill=color, outline="")
        # Right semicircle
        self.create_arc(x2 - radius * 2, y1, x2, y2, start=270, extent=180,
                       fill=color, outline="")
        # Center rectangle
        self.create_rectangle(x1 + radius, y1, x2 - radius, y2,
                             fill=color, outline="")

    def _on_enter(self, event):
        if not self._disabled:
            self._hover = True
            self._draw()
            self.config(cursor="hand2")

    def _on_leave(self, event):
        self._hover = False
        self._draw()
        self.config(cursor="")

    def _on_click(self, event):
        if not self._disabled and self.command:
            self.command()

    def set_disabled(self, disabled):
        self._disabled = disabled
        self._draw()

    def set_text(self, text):
        self.text = text
        self._draw()


class AppleToggle(tk.Canvas):
    """iOS-style toggle switch"""

    def __init__(self, parent, variable, command=None, **kwargs):
        super().__init__(parent, width=51, height=31,
                        bg=COLORS["card"], highlightthickness=0, **kwargs)

        self.variable = variable
        self.command = command
        self._animation_id = None

        self._draw()
        self.bind("<Button-1>", self._toggle)

    def _draw(self):
        self.delete("all")
        is_on = self.variable.get()

        # Track
        track_color = COLORS["success"] if is_on else COLORS["bg_tertiary"]
        self._draw_pill(0, 0, 51, 31, 15, track_color)

        # Knob with subtle shadow effect
        knob_x = 35 if is_on else 16
        # Shadow
        self.create_oval(knob_x - 12, 4, knob_x + 14, 28,
                        fill=COLORS["overlay"], outline="")
        # Knob
        self.create_oval(knob_x - 11, 3, knob_x + 13, 27,
                        fill="#ffffff", outline="")

    def _draw_pill(self, x1, y1, x2, y2, radius, color):
        self.create_arc(x1, y1, x1 + radius * 2, y2, start=90, extent=180,
                       fill=color, outline="")
        self.create_arc(x2 - radius * 2, y1, x2, y2, start=270, extent=180,
                       fill=color, outline="")
        self.create_rectangle(x1 + radius, y1, x2 - radius, y2,
                             fill=color, outline="")

    def _toggle(self, event=None):
        self.variable.set(not self.variable.get())
        self._draw()
        if self.command:
            self.command()


class GlowingRing(tk.Canvas):
    """Modern circular progress with glow effect"""

    def __init__(self, parent, size=220, **kwargs):
        super().__init__(parent, width=size, height=size,
                        bg=COLORS["bg"], highlightthickness=0, **kwargs)
        self.size = size
        self.progress = 0
        self.center_text = ""
        self.sub_text = "Ready to test"
        self.ping_value = None
        self._draw()

    def _draw(self):
        self.delete("all")
        center = self.size // 2
        outer_radius = (self.size - 30) // 2
        thickness = 6

        # Background ring
        self._draw_ring(center, outer_radius, thickness, COLORS["bg_tertiary"])

        # Progress ring
        if self.progress > 0:
            extent = 3.6 * self.progress
            color = COLORS["success"] if self.progress >= 100 else COLORS["accent"]
            self._draw_ring(center, outer_radius, thickness, color, extent)

        # Center content
        if self.ping_value is not None:
            # Large ping number
            self.create_text(center, center - 10,
                           text=str(int(self.ping_value)),
                           fill=COLORS["text"],
                           font=get_font(48, "bold"))
            self.create_text(center, center + 30,
                           text="ms",
                           fill=COLORS["text_muted"],
                           font=get_font(16))
        elif self.center_text:
            self.create_text(center, center - 5,
                           text=self.center_text,
                           fill=COLORS["text"],
                           font=get_font(18, "bold"))

        # Subtitle
        if self.sub_text:
            self.create_text(center, center + 55,
                           text=self.sub_text,
                           fill=COLORS["text_muted"],
                           font=get_font(12))

    def _draw_ring(self, center, radius, thickness, color, extent=360):
        self.create_arc(
            center - radius, center - radius,
            center + radius, center + radius,
            start=90, extent=-extent,
            outline=color, width=thickness, style="arc"
        )

    def set_progress(self, value, center_text="", sub_text=None, ping=None):
        self.progress = min(100, max(0, value))
        self.center_text = center_text
        if sub_text is not None:
            self.sub_text = sub_text
        self.ping_value = ping
        self._draw()

    def reset(self):
        self.progress = 0
        self.center_text = ""
        self.sub_text = "Ready to test"
        self.ping_value = None
        self._draw()


class ModernCard(tk.Frame):
    """Elevated card with subtle styling"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["card"], **kwargs)


class RegionPicker(tk.Frame):
    """Segmented control for region selection"""

    def __init__(self, parent, variable, regions, **kwargs):
        super().__init__(parent, bg=COLORS["bg"], **kwargs)

        self.variable = variable
        self.buttons = {}

        container = tk.Frame(self, bg=COLORS["bg_secondary"])
        container.pack(pady=2)

        for i, region in enumerate(regions):
            btn = tk.Label(
                container,
                text=region,
                font=get_font(12, "bold"),
                bg=COLORS["bg_secondary"],
                fg=COLORS["text_muted"],
                padx=20, pady=10,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT)
            btn.bind("<Button-1>", lambda e, r=region: self._select(r))
            self.buttons[region] = btn

        self._update_selection()

    def _select(self, region):
        self.variable.set(region)
        self._update_selection()

    def _update_selection(self):
        selected = self.variable.get()
        for region, btn in self.buttons.items():
            if region == selected:
                btn.config(bg=COLORS["accent"], fg="#ffffff")
            else:
                btn.config(bg=COLORS["bg_secondary"], fg=COLORS["text_muted"])


class ServerResultCard(tk.Frame):
    """Clean result card for each server"""

    def __init__(self, parent, result, is_best=False, **kwargs):
        bg = COLORS["card"]
        super().__init__(parent, bg=bg, **kwargs)

        self.configure(highlightthickness=0)

        inner = tk.Frame(self, bg=bg, padx=24, pady=16)
        inner.pack(fill=tk.X)

        # Left side - server info
        left = tk.Frame(inner, bg=bg)
        left.pack(side=tk.LEFT, fill=tk.Y)

        # Best badge
        if is_best:
            badge = tk.Label(left, text="★ BEST",
                           font=get_font(10, "bold"),
                           bg=COLORS["success"], fg="#ffffff",
                           padx=10, pady=3)
            badge.pack(anchor=tk.W, pady=(0, 8))

        # Server name
        is_failed = result.packet_loss >= 100
        name_color = COLORS["text_dim"] if is_failed else COLORS["text"]
        tk.Label(left, text=result.server_location,
                font=get_font(16, "bold"),
                bg=bg, fg=name_color).pack(anchor=tk.W)

        # Right side - stats
        right = tk.Frame(inner, bg=bg)
        right.pack(side=tk.RIGHT, fill=tk.Y)

        if is_failed:
            tk.Label(right, text="Unreachable",
                    font=get_font(15),
                    bg=bg, fg=COLORS["error"]).pack(anchor=tk.E)
        else:
            # Ping value
            quality = get_connection_quality(result)
            if quality == "Excellent":
                ping_color = COLORS["success"]
            elif quality == "Good":
                ping_color = COLORS["success"]
            elif quality == "Fair":
                ping_color = COLORS["warning"]
            else:
                ping_color = COLORS["error"]

            ping_frame = tk.Frame(right, bg=bg)
            ping_frame.pack(anchor=tk.E)

            tk.Label(ping_frame, text=f"{result.ping_avg:.0f}",
                    font=get_font(24, "bold"),
                    bg=bg, fg=ping_color).pack(side=tk.LEFT)
            tk.Label(ping_frame, text=" ms",
                    font=get_font(13),
                    bg=bg, fg=COLORS["text_muted"]).pack(side=tk.LEFT, pady=(6, 0))

            # Jitter and packet loss
            stats_text = f"{result.jitter:.1f}ms jitter"
            if result.packet_loss > 0:
                stats_text += f" · {result.packet_loss:.0f}% loss"

            tk.Label(right, text=stats_text,
                    font=get_font(12),
                    bg=bg, fg=COLORS["text_dim"]).pack(anchor=tk.E)


class PingDiffApp:
    """Main application window"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PingDiff")
        self.root.geometry("580x820")
        self.root.minsize(520, 780)
        self.root.configure(bg=COLORS["bg"])

        # Try to set icon
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass

        # Initialize
        self.settings = Settings()
        self.api = APIClient(self.settings)
        self.servers = {}
        self.current_game = "overwatch-2"
        self.results: List[PingResult] = []
        self.isp_info = {}
        self.is_testing = False
        self.dashboard_url = None

        # Variables
        self.share_results_var = tk.BooleanVar(value=self.settings.share_results)
        self.region_var = tk.StringVar(value=self.settings.default_region)
        self.game_var = tk.StringVar(value=self.current_game)

        self._create_ui()
        self._load_data()

    def _create_ui(self):
        # Main container with padding (32px grid)
        main = tk.Frame(self.root, bg=COLORS["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)

        # Header
        self._create_header(main)

        # ISP Info
        self._create_isp_section(main)

        # Game Selector
        self._create_game_section(main)

        # Region Selector
        self._create_region_section(main)

        # Progress Ring
        self._create_progress_section(main)

        # Test Button
        self._create_test_button(main)

        # Results
        self._create_results_section(main)

        # Settings
        self._create_settings_section(main)

        # Footer
        self._create_footer(main)

    def _create_header(self, parent):
        header = tk.Frame(parent, bg=COLORS["bg"])
        header.pack(fill=tk.X, pady=(0, 24))

        # Title row
        title_row = tk.Frame(header, bg=COLORS["bg"])
        title_row.pack(fill=tk.X)

        tk.Label(title_row, text="PingDiff",
                font=get_font(32, "bold"),
                bg=COLORS["bg"], fg=COLORS["text"]).pack(side=tk.LEFT)

        # Version badge
        version_badge = tk.Label(title_row, text=f"v{APP_VERSION}",
                                font=get_font(11),
                                bg=COLORS["bg_tertiary"], fg=COLORS["text_muted"],
                                padx=12, pady=4)
        version_badge.pack(side=tk.LEFT, padx=(16, 0), pady=(8, 0))

        # Subtitle
        tk.Label(header, text="Game Server Connection Tester",
                font=get_font(14),
                bg=COLORS["bg"], fg=COLORS["text_muted"]).pack(anchor=tk.W, pady=(8, 0))

    def _create_isp_section(self, parent):
        card = ModernCard(parent, padx=24, pady=20)
        card.pack(fill=tk.X, pady=(0, 24))

        # ISP Row
        isp_row = tk.Frame(card, bg=COLORS["card"])
        isp_row.pack(fill=tk.X)

        tk.Label(isp_row, text="Your ISP",
                font=get_font(13),
                bg=COLORS["card"], fg=COLORS["text_dim"]).pack(side=tk.LEFT)

        self.isp_label = tk.Label(isp_row, text="Detecting...",
                                  font=get_font(14, "bold"),
                                  bg=COLORS["card"], fg=COLORS["text"])
        self.isp_label.pack(side=tk.RIGHT)

        # Separator
        tk.Frame(card, bg=COLORS["separator"], height=1).pack(fill=tk.X, pady=16)

        # Location Row
        loc_row = tk.Frame(card, bg=COLORS["card"])
        loc_row.pack(fill=tk.X)

        tk.Label(loc_row, text="Location",
                font=get_font(13),
                bg=COLORS["card"], fg=COLORS["text_dim"]).pack(side=tk.LEFT)

        self.location_label = tk.Label(loc_row, text="...",
                                       font=get_font(14),
                                       bg=COLORS["card"], fg=COLORS["text_secondary"])
        self.location_label.pack(side=tk.RIGHT)

    def _create_game_section(self, parent):
        section = tk.Frame(parent, bg=COLORS["bg"])
        section.pack(fill=tk.X, pady=(0, 16))

        tk.Label(section, text="Select Game",
                font=get_font(14, "bold"),
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor=tk.W, pady=(0, 12))

        # Game buttons container with wrap support
        btn_frame = tk.Frame(section, bg=COLORS["bg"])
        btn_frame.pack(fill=tk.X)

        self.game_buttons = {}
        for game_id, game_info in GAMES.items():
            btn = tk.Label(
                btn_frame,
                text=game_info["short"],  # Use short names to fit all games
                font=get_font(11, "bold"),
                bg=COLORS["bg_secondary"],
                fg=COLORS["text_muted"],
                padx=14, pady=10,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=(0, 8))
            btn.bind("<Button-1>", lambda e, g=game_id: self._select_game(g))
            self.game_buttons[game_id] = btn

        self._update_game_buttons()

    def _select_game(self, game_id):
        if self.is_testing:
            return
        self.game_var.set(game_id)
        self.current_game = game_id
        self._update_game_buttons()
        self._update_footer_label()
        # Reload servers for new game
        self._reload_servers()

    def _update_game_buttons(self):
        selected = self.game_var.get()
        for game_id, btn in self.game_buttons.items():
            if game_id == selected:
                btn.config(bg=COLORS["accent"], fg="#ffffff")
            else:
                btn.config(bg=COLORS["bg_secondary"], fg=COLORS["text_muted"])

    def _reload_servers(self):
        def load():
            self.servers = self.api.get_servers(self.current_game)
        thread = threading.Thread(target=load, daemon=True)
        thread.start()

    def _update_footer_label(self):
        game_name = GAMES.get(self.current_game, {}).get("name", "Unknown")
        if hasattr(self, 'game_label'):
            self.game_label.config(text=game_name)

    def _create_region_section(self, parent):
        section = tk.Frame(parent, bg=COLORS["bg"])
        section.pack(fill=tk.X, pady=(0, 24))

        tk.Label(section, text="Select Region",
                font=get_font(14, "bold"),
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor=tk.W, pady=(0, 12))

        # Region buttons
        btn_frame = tk.Frame(section, bg=COLORS["bg"])
        btn_frame.pack(fill=tk.X)

        self.region_buttons = {}
        for region in REGIONS:
            btn = tk.Label(
                btn_frame,
                text=region,
                font=get_font(12, "bold"),
                bg=COLORS["bg_secondary"],
                fg=COLORS["text_muted"],
                padx=20, pady=10,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=(0, 8))
            btn.bind("<Button-1>", lambda e, r=region: self._select_region(r))
            self.region_buttons[region] = btn

        self._update_region_buttons()

    def _select_region(self, region):
        self.region_var.set(region)
        self.settings.default_region = region
        self._update_region_buttons()

    def _update_region_buttons(self):
        selected = self.region_var.get()
        for region, btn in self.region_buttons.items():
            if region == selected:
                btn.config(bg=COLORS["accent"], fg="#ffffff")
            else:
                btn.config(bg=COLORS["bg_secondary"], fg=COLORS["text_muted"])

    def _create_progress_section(self, parent):
        section = tk.Frame(parent, bg=COLORS["bg"])
        section.pack(pady=16)

        self.progress_ring = GlowingRing(section, size=180)
        self.progress_ring.pack()

    def _create_test_button(self, parent):
        btn_frame = tk.Frame(parent, bg=COLORS["bg"])
        btn_frame.pack(pady=(8, 16))

        self.test_button = PillButton(
            btn_frame,
            text="Start Test",
            command=self._start_test,
            width=200,
            height=50,
            style="primary"
        )
        self.test_button.pack()

    def _create_results_section(self, parent):
        section = tk.Frame(parent, bg=COLORS["bg"])
        section.pack(fill=tk.BOTH, expand=True)

        # Header row
        header = tk.Frame(section, bg=COLORS["bg"])
        header.pack(fill=tk.X, pady=(0, 16))

        tk.Label(header, text="Results",
                font=get_font(16, "bold"),
                bg=COLORS["bg"], fg=COLORS["text"]).pack(side=tk.LEFT)

        self.results_count = tk.Label(header, text="",
                                      font=get_font(13),
                                      bg=COLORS["bg"], fg=COLORS["text_muted"])
        self.results_count.pack(side=tk.RIGHT)

        # Scrollable results
        canvas_frame = tk.Frame(section, bg=COLORS["bg"])
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(canvas_frame, bg=COLORS["bg"],
                          highlightthickness=0, height=140)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

        self.results_frame = tk.Frame(canvas, bg=COLORS["bg"])
        self.results_frame.bind("<Configure>",
                               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.results_frame, anchor="nw", width=500)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mouse wheel scroll
        def _scroll(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _scroll)

        # Empty state
        self.empty_label = tk.Label(self.results_frame,
                                    text="Run a test to see results",
                                    font=get_font(14),
                                    bg=COLORS["bg"], fg=COLORS["text_dim"])
        self.empty_label.pack(pady=32)

    def _create_settings_section(self, parent):
        card = ModernCard(parent, padx=24, pady=20)
        card.pack(fill=tk.X, pady=(16, 0))

        # Settings header
        tk.Label(card, text="Settings",
                font=get_font(14, "bold"),
                bg=COLORS["card"], fg=COLORS["text"]).pack(anchor=tk.W, pady=(0, 16))

        # Share toggle row
        share_row = tk.Frame(card, bg=COLORS["card"])
        share_row.pack(fill=tk.X)

        tk.Label(share_row, text="Share results anonymously",
                font=get_font(13),
                bg=COLORS["card"], fg=COLORS["text_secondary"]).pack(side=tk.LEFT)

        self.share_toggle = AppleToggle(share_row, self.share_results_var,
                                        command=self._on_share_toggle)
        self.share_toggle.pack(side=tk.RIGHT)

        # Data folder row
        tk.Frame(card, bg=COLORS["separator"], height=1).pack(fill=tk.X, pady=16)

        folder_row = tk.Frame(card, bg=COLORS["card"])
        folder_row.pack(fill=tk.X)

        tk.Label(folder_row, text="App data",
                font=get_font(13),
                bg=COLORS["card"], fg=COLORS["text_dim"]).pack(side=tk.LEFT)

        folder_link = tk.Label(folder_row, text="Open Folder",
                              font=get_font(13),
                              bg=COLORS["card"], fg=COLORS["accent"],
                              cursor="hand2")
        folder_link.pack(side=tk.RIGHT)
        folder_link.bind("<Button-1>", self._open_data_folder)

    def _on_share_toggle(self):
        self.settings.share_results = self.share_results_var.get()

    def _open_data_folder(self, event=None):
        folder = get_app_data_dir()
        if os.name == 'nt':
            os.startfile(folder)
        else:
            webbrowser.open(f'file://{folder}')

    def _create_footer(self, parent):
        footer = tk.Frame(parent, bg=COLORS["bg"])
        footer.pack(fill=tk.X, pady=(16, 0))

        # Dashboard button
        self.dashboard_btn = PillButton(
            footer,
            text="Open Dashboard",
            command=self._open_dashboard,
            width=150,
            height=40,
            style="secondary"
        )
        self.dashboard_btn.pack(side=tk.LEFT)

        # GitHub button
        github_btn = PillButton(
            footer,
            text="GitHub",
            command=lambda: webbrowser.open("https://github.com/bokiko/pingdiff"),
            width=100,
            height=40,
            style="secondary"
        )
        github_btn.pack(side=tk.LEFT, padx=(12, 0))

        # Game label (dynamic)
        game_name = GAMES.get(self.current_game, {}).get("name", "Unknown")
        self.game_label = tk.Label(footer, text=game_name,
                font=get_font(12),
                bg=COLORS["bg"], fg=COLORS["text_dim"])
        self.game_label.pack(side=tk.RIGHT)

    def _load_data(self):
        def load():
            self.isp_info = self.api.get_isp_info()
            self.root.after(0, self._update_isp_display)
            self.servers = self.api.get_servers(self.current_game)

        thread = threading.Thread(target=load, daemon=True)
        thread.start()

    def _update_isp_display(self):
        isp = self.isp_info.get("isp", "Unknown")
        country = self.isp_info.get("country", "Unknown")
        city = self.isp_info.get("city", "Unknown")

        self.isp_label.config(text=isp)
        self.location_label.config(text=f"{city}, {country}")

    def _start_test(self):
        if self.is_testing:
            return

        self.is_testing = True
        self.test_button.set_disabled(True)
        self.test_button.set_text("Testing...")
        self.progress_ring.set_progress(0, "Testing", "Connecting to servers...")

        region = self.region_var.get()
        servers = self.servers.get(region, [])

        if not servers:
            messagebox.showerror("Error", f"No servers available for {region}")
            self.is_testing = False
            self.test_button.set_disabled(False)
            self.test_button.set_text("Start Test")
            self.progress_ring.reset()
            return

        def run_test():
            def progress_callback(current, total, result):
                progress = (current / total) * 100
                status = f"{current}/{total}"
                if result.packet_loss < 100:
                    sub = f"Testing {result.server_location}"
                else:
                    sub = f"{result.server_location} unreachable"
                self.root.after(0, lambda: self.progress_ring.set_progress(
                    progress, status, sub))

            self.results = test_all_servers(servers, callback=progress_callback)
            self.root.after(0, self._show_results)

        thread = threading.Thread(target=run_test, daemon=True)
        thread.start()

    def _show_results(self):
        self.is_testing = False
        self.test_button.set_disabled(False)
        self.test_button.set_text("Start Test")

        best = get_best_server(self.results)
        if best:
            self.progress_ring.set_progress(
                100, "", f"Best: {best.server_location}", ping=best.ping_avg)
        else:
            self.progress_ring.set_progress(100, "Failed", "All servers unreachable")

        # Clear results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not self.results:
            tk.Label(self.results_frame, text="No results",
                    font=get_font(13),
                    bg=COLORS["bg"], fg=COLORS["text_dim"]).pack(pady=40)
            return

        # Count successful
        successful = len([r for r in self.results if r.packet_loss < 100])
        self.results_count.config(text=f"{successful}/{len(self.results)} servers")

        # Sort and display
        sorted_results = sorted(self.results, key=lambda r: (r.packet_loss >= 100, r.ping_avg))

        for i, result in enumerate(sorted_results):
            card = ServerResultCard(
                self.results_frame,
                result,
                is_best=(i == 0 and result.packet_loss < 100)
            )
            card.pack(fill=tk.X, pady=(0, 8))

        # Submit to API
        self._submit_results()

    def _submit_results(self):
        def submit():
            results_data = [{
                "server_id": r.server_id,
                "server_location": r.server_location,
                "ping_avg": r.ping_avg,
                "ping_min": r.ping_min,
                "ping_max": r.ping_max,
                "jitter": r.jitter,
                "packet_loss": r.packet_loss,
                "raw_times": r.raw_times
            } for r in self.results]

            response = self.api.submit_results(results_data, self.isp_info, self.current_game)
            if response.get("success"):
                self.dashboard_url = response.get("dashboard_url")

        thread = threading.Thread(target=submit, daemon=True)
        thread.start()

    def _open_dashboard(self):
        if self.dashboard_url:
            url = self.dashboard_url
            if url.startswith('/'):
                url = f"{self.api.base_url}{url}"
            webbrowser.open(url)
        else:
            webbrowser.open(f"{self.api.base_url}/dashboard")

    def run(self):
        self.root.mainloop()


def main():
    app = PingDiffApp()
    app.run()


if __name__ == "__main__":
    main()
