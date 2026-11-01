#!/usr/bin/env python3
"""Local nhipdung entry point; works from any working directory."""
from pathlib import Path
import runpy

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).resolve().parent / 'skills/nhipdung/scripts/nhipdung.py'), run_name='__main__')
