#!/usr/bin/env python3
"""Copy the Liquid Glass themes into Vesktop's themes folder (finds it for you).

  python3 install.py             copy both themes
  python3 install.py --dry       only show what would be copied

Then enable ONE of them in Vesktop: Settings -> Themes.
"""
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATES = [
    "~/.var/app/dev.vencord.Vesktop/config/vesktop/themes",          # Linux, flatpak
    "~/.config/vesktop/themes",                                       # Linux
    "~/Library/Application Support/vesktop/themes",                   # macOS
    os.path.join(os.environ.get("APPDATA", "~"), "vesktop", "themes"),  # Windows
]


def main():
    dest = next((Path(os.path.expanduser(c)) for c in CANDIDATES if Path(os.path.expanduser(c)).parent.is_dir()), None)
    if dest is None:
        sys.exit("Vesktop folder not found: start Vesktop once, then run this again.")
    for f in sorted(HERE.glob("liquid-glass*.theme.css")):
        print(f"{f.name} -> {dest}")
        if "--dry" not in sys.argv:
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copy(f, dest / f.name)
    if "--dry" not in sys.argv:
        print("Now: Vesktop -> Settings -> Themes -> enable Liquid Glass or Liquid Glass Autumn (only one).")


main()
