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

    def __init__(self, parent, size=140, **kwargs):
        super().__init__(parent, width=size, height=size,
                        bg=COLORS["bg"], highlightthickness=0, **kwargs)
        self.size = size
        self.progress = 0
        self.center_text = ""
        self.sub_text = "Ready"
        self.ping_value = None
        self._draw()

    def _draw(self):
        self.delete("all")
        center = self.size // 2
        outer_radius = (self.size - 20) // 2
        thickness = 5

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
            self.create_text(center, center - 6,
                           text=str(int(self.ping_value)),
                           fill=COLORS["text"],
                           font=get_font(36, "bold"))
            self.create_text(center, center + 20,
                           text="ms",
                           fill=COLORS["text_muted"],
                           font=get_font(12))
        elif self.center_text:
            self.create_text(center, center,
                           text=self.center_text,
                           fill=COLORS["text"],
                           font=get_font(14, "bold"))

        # Subtitle below ring (only if not showing ping)
        if self.sub_text and self.ping_value is None:
            self.create_text(center, center + 38,
                           text=self.sub_text,
                           fill=COLORS["text_muted"],
                           font=get_font(10))

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
        self.sub_text = "Ready"
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

        # Server name with region
        is_failed = result.packet_loss >= 100
        name_color = COLORS["text_dim"] if is_failed else COLORS["text"]

        # Show location with region if available
        location_text = result.server_location
        if result.region:
            location_text = f"{result.server_location} ({result.region})"

        tk.Label(left, text=location_text,
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
        self.root.geometry("600x700")
        self.root.minsize(550, 650)
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
        # Main container with compact padding
        main = tk.Frame(self.root, bg=COLORS["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=24, pady=20)

        # Header with ISP info inline
        self._create_header(main)

        # Game & Region Selectors (compact)
        self._create_selectors_section(main)

        # Progress Ring + Test Button (centered)
        self._create_test_section(main)

        # Results (expandable)
        self._create_results_section(main)

        # Footer with settings inline
        self._create_footer(main)

    def _create_header(self, parent):
        header = tk.Frame(parent, bg=COLORS["bg"])
        header.pack(fill=tk.X, pady=(0, 16))

        # Title row with version
        title_row = tk.Frame(header, bg=COLORS["bg"])
        title_row.pack(fill=tk.X)

        tk.Label(title_row, text="PingDiff",
                font=get_font(28, "bold"),
                bg=COLORS["bg"], fg=COLORS["text"]).pack(side=tk.LEFT)

        version_badge = tk.Label(title_row, text=f"v{APP_VERSION}",
                                font=get_font(10),
                                bg=COLORS["bg_tertiary"], fg=COLORS["text_muted"],
                                padx=8, pady=2)
        version_badge.pack(side=tk.LEFT, padx=(12, 0), pady=(6, 0))

        # ISP info on the right side of header
        isp_frame = tk.Frame(title_row, bg=COLORS["bg"])
        isp_frame.pack(side=tk.RIGHT)

        self.isp_label = tk.Label(isp_frame, text="Detecting...",
                                  font=get_font(11),
                                  bg=COLORS["bg"], fg=COLORS["text_muted"])
        self.isp_label.pack(side=tk.RIGHT)

        tk.Label(isp_frame, text="ISP: ",
                font=get_font(11),
                bg=COLORS["bg"], fg=COLORS["text_dim"]).pack(side=tk.RIGHT)

        # Location below ISP
        self.location_label = tk.Label(header, text="",
                                       font=get_font(11),
                                       bg=COLORS["bg"], fg=COLORS["text_dim"])
        self.location_label.pack(anchor=tk.E)

    def _create_selectors_section(self, parent):
        """Game dropdown and region selectors"""
        section = tk.Frame(parent, bg=COLORS["bg"])
        section.pack(fill=tk.X, pady=(0, 16))

        # Game dropdown row
        game_row = tk.Frame(section, bg=COLORS["bg"])
        game_row.pack(fill=tk.X, pady=(0, 12))

        tk.Label(game_row, text="Game:",
                font=get_font(12, "bold"),
                bg=COLORS["bg"], fg=COLORS["text"]).pack(side=tk.LEFT, padx=(0, 12))

        # Create game name to id mapping
        self.game_name_to_id = {info["name"]: gid for gid, info in GAMES.items()}
        self.game_id_to_name = {gid: info["name"] for gid, info in GAMES.items()}
        game_names = list(self.game_name_to_id.keys())

        # Style the combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Game.TCombobox",
                       fieldbackground=COLORS["bg_secondary"],
                       background=COLORS["bg_tertiary"],
                       foreground=COLORS["text"],
                       arrowcolor=COLORS["text"],
                       borderwidth=0,
                       padding=8)
        style.map("Game.TCombobox",
                 fieldbackground=[('readonly', COLORS["bg_secondary"])],
                 selectbackground=[('readonly', COLORS["accent"])],
                 selectforeground=[('readonly', '#ffffff')])

        self.game_combo_var = tk.StringVar(value=self.game_id_to_name.get(self.current_game, "Overwatch 2"))
        self.game_combo = ttk.Combobox(
            game_row,
            textvariable=self.game_combo_var,
            values=game_names,
            state="readonly",
            style="Game.TCombobox",
            width=25,
            font=get_font(12)
        )
        self.game_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.game_combo.bind("<<ComboboxSelected>>", self._on_game_selected)
        # Set initial selection
        self.game_combo.set(self.game_id_to_name.get(self.current_game, "Overwatch 2"))

        # Server count label
        self.server_count_label = tk.Label(game_row, text="",
                                           font=get_font(11),
                                           bg=COLORS["bg"], fg=COLORS["text_muted"])
        self.server_count_label.pack(side=tk.RIGHT, padx=(12, 0))

        # Region checkboxes row
        region_row = tk.Frame(section, bg=COLORS["bg"])
        region_row.pack(fill=tk.X)

        tk.Label(region_row, text="Regions:",
                font=get_font(12, "bold"),
                bg=COLORS["bg"], fg=COLORS["text"]).pack(side=tk.LEFT, padx=(0, 12))

        # Container for region checkboxes
        self.region_container = tk.Frame(region_row, bg=COLORS["bg"])
        self.region_container.pack(side=tk.LEFT, fill=tk.X)

        # Region checkbox variables and widgets
        self.region_vars = {}
        self.region_checks = {}
        self._create_region_checkboxes()

    def _create_region_checkboxes(self):
        """Create region checkboxes based on available regions for current game"""
        # Clear existing checkboxes
        for widget in self.region_container.winfo_children():
            widget.destroy()
        self.region_vars.clear()
        self.region_checks.clear()

        # Get available regions for this game
        available_regions = list(self.servers.keys()) if self.servers else REGIONS

        for region in REGIONS:
            if region not in available_regions:
                continue

            # Count servers in this region
            server_count = len(self.servers.get(region, []))

            # Create checkbox variable (default: select first region)
            var = tk.BooleanVar(value=(region == available_regions[0] if available_regions else False))
            self.region_vars[region] = var

            # Create styled checkbox frame
            check_frame = tk.Frame(self.region_container, bg=COLORS["bg"])
            check_frame.pack(side=tk.LEFT, padx=(0, 8))

            # Custom checkbox look
            cb = tk.Checkbutton(
                check_frame,
                text=f"{region} ({server_count})",
                variable=var,
                font=get_font(11),
                bg=COLORS["bg"],
                fg=COLORS["text"],
                selectcolor=COLORS["bg_secondary"],
                activebackground=COLORS["bg"],
                activeforeground=COLORS["text"],
                highlightthickness=0,
                bd=0,
                cursor="hand2",
                command=self._on_region_changed
            )
            cb.pack()
            self.region_checks[region] = cb

    def _on_region_changed(self):
        """Handle region checkbox change"""
        self._update_selected_server_count()

    def _update_selected_server_count(self):
        """Update server count based on selected regions"""
        total = 0
        for region, var in self.region_vars.items():
            if var.get():
                total += len(self.servers.get(region, []))
        if total > 0:
            self.server_count_label.config(text=f"{total} servers selected")
        else:
            self.server_count_label.config(text="Select at least one region")

    def _on_game_selected(self, event=None):
        """Handle game dropdown selection"""
        if self.is_testing:
            return
        selected_name = self.game_combo.get()
        game_id = self.game_name_to_id.get(selected_name)
        if game_id:
            self.game_var.set(game_id)
            self.current_game = game_id
            self._reload_servers()

    def _update_server_count(self):
        """Update the server count label and refresh region checkboxes"""
        self._create_region_checkboxes()
        self._update_selected_server_count()

    def _reload_servers(self):
        def load():
            self.servers = self.api.get_servers(self.current_game)
            self.root.after(0, self._update_server_count)
        thread = threading.Thread(target=load, daemon=True)
        thread.start()

    def _get_selected_regions(self):
        """Get list of selected regions"""
        return [region for region, var in self.region_vars.items() if var.get()]

    def _create_test_section(self, parent):
        """Combined progress ring and test button"""
        section = tk.Frame(parent, bg=COLORS["bg"])
        section.pack(pady=12)

        # Smaller progress ring
        self.progress_ring = GlowingRing(section, size=140)
        self.progress_ring.pack()

        # Test button right below
        self.test_button = PillButton(
            section,
            text="Start Test",
            command=self._start_test,
            width=180,
            height=44,
            style="primary"
        )
        self.test_button.pack(pady=(12, 0))

    def _create_results_section(self, parent):
        section = tk.Frame(parent, bg=COLORS["bg"])
        section.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        # Header row
        header = tk.Frame(section, bg=COLORS["bg"])
        header.pack(fill=tk.X, pady=(0, 8))

        tk.Label(header, text="Results",
                font=get_font(14, "bold"),
                bg=COLORS["bg"], fg=COLORS["text"]).pack(side=tk.LEFT)

        self.results_count = tk.Label(header, text="",
                                      font=get_font(12),
                                      bg=COLORS["bg"], fg=COLORS["text_muted"])
        self.results_count.pack(side=tk.RIGHT)

        # Scrollable results - takes remaining space
        canvas_frame = tk.Frame(section, bg=COLORS["bg"])
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.results_canvas = tk.Canvas(canvas_frame, bg=COLORS["bg"],
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.results_canvas.yview)

        self.results_frame = tk.Frame(self.results_canvas, bg=COLORS["bg"])
        self.results_frame.bind("<Configure>",
                               lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all")))

        self.results_canvas.create_window((0, 0), window=self.results_frame, anchor="nw", width=540)
        self.results_canvas.configure(yscrollcommand=scrollbar.set)

        self.results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mouse wheel scroll
        def _scroll(event):
            self.results_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.results_canvas.bind_all("<MouseWheel>", _scroll)

        # Empty state
        self.empty_label = tk.Label(self.results_frame,
                                    text="Run a test to see results",
                                    font=get_font(13),
                                    bg=COLORS["bg"], fg=COLORS["text_dim"])
        self.empty_label.pack(pady=24)

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
        footer.pack(fill=tk.X, pady=(12, 0))

        # Left side - buttons
        left = tk.Frame(footer, bg=COLORS["bg"])
        left.pack(side=tk.LEFT)

        self.dashboard_btn = PillButton(
            left,
            text="Dashboard",
            command=self._open_dashboard,
            width=110,
            height=36,
            style="secondary"
        )
        self.dashboard_btn.pack(side=tk.LEFT)

        github_btn = PillButton(
            left,
            text="GitHub",
            command=lambda: webbrowser.open("https://github.com/bokiko/pingdiff"),
            width=80,
            height=36,
            style="secondary"
        )
        github_btn.pack(side=tk.LEFT, padx=(8, 0))

        folder_btn = PillButton(
            left,
            text="Data",
            command=self._open_data_folder,
            width=60,
            height=36,
            style="secondary"
        )
        folder_btn.pack(side=tk.LEFT, padx=(8, 0))

        # Right side - share toggle
        right = tk.Frame(footer, bg=COLORS["bg"])
        right.pack(side=tk.RIGHT)

        tk.Label(right, text="Share:",
                font=get_font(11),
                bg=COLORS["bg"], fg=COLORS["text_dim"]).pack(side=tk.LEFT, padx=(0, 8))

        self.share_toggle = AppleToggle(right, self.share_results_var,
                                        command=self._on_share_toggle)
        self.share_toggle.pack(side=tk.LEFT)

    def _load_data(self):
        def load():
            self.isp_info = self.api.get_isp_info()
            self.root.after(0, self._update_isp_display)
            self.servers = self.api.get_servers(self.current_game)
            self.root.after(0, self._update_server_count)

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

        # Get all selected regions
        selected_regions = self._get_selected_regions()

        if not selected_regions:
            messagebox.showerror("Error", "Please select at least one region")
            return

        # Combine all servers from selected regions
        all_servers = []
        for region in selected_regions:
            region_servers = self.servers.get(region, [])
            # Add region info to each server for display
            for server in region_servers:
                server_with_region = server.copy()
                server_with_region['region'] = region
                all_servers.append(server_with_region)

        if not all_servers:
            messagebox.showerror("Error", "No servers available for selected regions")
            return

        self.is_testing = True
        self.test_button.set_disabled(True)
        self.test_button.set_text("Testing...")
        self.progress_ring.set_progress(0, "Testing", f"Testing {len(all_servers)} servers...")

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

            self.results = test_all_servers(all_servers, callback=progress_callback)
            self.root.after(0, self._show_results)

        thread = threading.Thread(target=run_test, daemon=True)
        thread.start()

    def _show_results(self):
        self.is_testing = False
        self.test_button.set_disabled(False)
        self.test_button.set_text("Start Test")

        best = get_best_server(self.results)
        if best:
            best_text = f"Best: {best.server_location}"
            if best.region:
                best_text = f"Best: {best.server_location} ({best.region})"
            self.progress_ring.set_progress(100, "", best_text, ping=best.ping_avg)
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
