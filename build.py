import os
import subprocess
import sys
from pathlib import Path

def run(cmd, cwd=None):
    print(f"Running: {cmd}")
    subprocess.run(cmd, cwd=cwd, shell=True, check=True)

if __name__ == "__main__":
    root = Path(__file__).parent
    print("Building React Frontend...")
    run("npm run build", cwd=root / "frontend")
    print("Building Python Backend EXE...")
    run('python -m PyInstaller --noconfirm --onefile --windowed --clean --name="CodeLume-Bug-Hunter" --icon=assets/favicon.ico --add-data "frontend/dist;frontend/dist" --add-data "assets;assets" server.py', cwd=root)
    print("Done! EXE at dist/CodeLume-Bug-Hunter.exe")
    print("Now open installer.iss in Inno Setup to make Setup.exe")