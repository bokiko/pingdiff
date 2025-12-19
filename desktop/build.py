"""
PingDiff Build Script
Creates Windows executable using PyInstaller
Supports both standalone exe and folder mode for installer
"""

import PyInstaller.__main__
import os
import shutil
import sys

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(SCRIPT_DIR, "src")
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")
DIST_DIR = os.path.join(SCRIPT_DIR, "dist")
BUILD_DIR = os.path.join(SCRIPT_DIR, "build")

def build(onefile=False, version=None):
    """Build the application

    Args:
        onefile: If True, creates single exe. If False, creates folder (for installer)
        version: Version string to append to exe name
    """
    # Clean previous builds
    for dir_path in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    # App name
    app_name = "PingDiff"
    if version and onefile:
        app_name = f"PingDiff-{version}"

    # PyInstaller arguments
    args = [
        os.path.join(SRC_DIR, "main.py"),
        f"--name={app_name}",
        "--windowed",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR}",
        f"--specpath={SCRIPT_DIR}",
        # Add all source files
        f"--add-data={os.path.join(SRC_DIR, 'config.py')};.",
        f"--add-data={os.path.join(SRC_DIR, 'ping_tester.py')};.",
        f"--add-data={os.path.join(SRC_DIR, 'api_client.py')};.",
        f"--add-data={os.path.join(SRC_DIR, 'gui.py')};.",
        # Hidden imports
        "--hidden-import=tkinter",
        "--hidden-import=requests",
        # Exclude unnecessary modules to reduce size
        "--exclude-module=matplotlib",
        "--exclude-module=numpy",
        "--exclude-module=pandas",
        "--exclude-module=PIL",
    ]

    # Single file or folder mode
    if onefile:
        args.append("--onefile")
    else:
        args.append("--onedir")

    # Add icon if exists
    icon_path = os.path.join(ASSETS_DIR, "icon.ico")
    if os.path.exists(icon_path):
        args.append(f"--icon={icon_path}")

    print(f"Building PingDiff ({'onefile' if onefile else 'onedir'} mode)...")
    print(f"Source: {SRC_DIR}")
    print(f"Output: {DIST_DIR}")

    PyInstaller.__main__.run(args)

    if onefile:
        exe_path = os.path.join(DIST_DIR, f"{app_name}.exe")
    else:
        exe_path = os.path.join(DIST_DIR, app_name, f"{app_name}.exe")

    print("\nBuild complete!")
    print(f"Executable: {exe_path}")

    return exe_path

if __name__ == "__main__":
    # Parse command line args
    onefile = "--onefile" in sys.argv
    version = None
    for arg in sys.argv:
        if arg.startswith("--version="):
            version = arg.split("=")[1]

    build(onefile=onefile, version=version)
