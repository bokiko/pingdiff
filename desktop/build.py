"""
PingDiff Build Script
Creates Windows executable using PyInstaller
"""

import PyInstaller.__main__
import os
import shutil

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(SCRIPT_DIR, "src")
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")
DIST_DIR = os.path.join(SCRIPT_DIR, "dist")
BUILD_DIR = os.path.join(SCRIPT_DIR, "build")

# Clean previous builds
for dir_path in [DIST_DIR, BUILD_DIR]:
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

# PyInstaller arguments
args = [
    os.path.join(SRC_DIR, "main.py"),
    "--name=PingDiff",
    "--onefile",
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

# Add icon if exists
icon_path = os.path.join(ASSETS_DIR, "icon.ico")
if os.path.exists(icon_path):
    args.append(f"--icon={icon_path}")

print("Building PingDiff...")
print(f"Source: {SRC_DIR}")
print(f"Output: {DIST_DIR}")

PyInstaller.__main__.run(args)

print("\nBuild complete!")
print(f"Executable: {os.path.join(DIST_DIR, 'PingDiff.exe')}")
