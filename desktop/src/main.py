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

from gui import PingDiffApp


def main():
    """Main entry point"""
    try:
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
