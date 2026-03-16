"""
PingDiff Desktop Application
Main entry point
"""

import sys
import os

# Add src directory to path for imports
if getattr(sys, 'frozen', False):
    # Running as compiled
    application_path = os.path.dirname(sys.executable)
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

from cli import build_parser, run_cli


def main():
    """Main entry point — routes to CLI or GUI mode based on arguments."""
    parser = build_parser()

    # Check if any CLI flags are present (without consuming them for GUI mode)
    args, remaining = parser.parse_known_args()

    if args.cli or args.list_games:
        # CLI mode
        args = parser.parse_args()
        sys.exit(run_cli(args))

    # Check for --version (argparse handles it, but just in case)
    if "--version" in sys.argv:
        from config import APP_VERSION
        print(f"PingDiff v{APP_VERSION}")
        sys.exit(0)

    # GUI mode
    try:
        from gui import PingDiffApp
        app = PingDiffApp()
        app.run()
    except Exception as e:
        import traceback
        error_msg = f"Error starting PingDiff:\n\n{str(e)}\n\n{traceback.format_exc()}"

        # Try to show error in GUI
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("PingDiff Error", error_msg)
        except:
            print(error_msg)

        sys.exit(1)


if __name__ == "__main__":
    main()
