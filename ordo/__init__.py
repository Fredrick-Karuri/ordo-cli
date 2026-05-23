from pathlib import Path
import sys

def _read_version() -> str:
    # Running as PyInstaller bundle
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).parent.parent
    return (base / "VERSION").read_text().strip()

__version__ = _read_version()