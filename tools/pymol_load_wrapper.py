#!/usr/bin/env python
import argparse
import os
import sys
from pathlib import Path

# Adjust import to your package layout:
# e.g., if this script lives next to the package, ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from helpers_TG.pymol_remote_control import launch_pymol_session, load_structures, reinitialize_pymol

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', type=int, default=9123)
    ap.add_argument('--recursive', action='store_true')
    ap.add_argument('--no-reinit', action='store_true', help='Do not reinitialize PyMOL on connect')
    ap.add_argument('paths', nargs='*', help='Files or folders to load')
    args = ap.parse_args()

    cmd = launch_pymol_session(port=args.port)

    if not args.no_reinit:
        try:
            reinitialize_pymol(cmd)
        except Exception:
            pass

    any_loaded = False
    for p in args.paths:
        p = os.path.expanduser(p)
        try:
            if os.path.isdir(p):
                loaded = load_structures(cmd, p, recursive=args.recursive)
            else:
                loaded = load_structures(cmd, p)
            if not loaded:
                print(f"[WARN] Nothing loaded from: {p}")
            for fp, obj, fmt in loaded:
                print(f"[OK] {fp} -> {obj} ({fmt})")
                any_loaded = True
        except Exception as e:
            print(f"[ERR] {p}: {e}")

    return 0 if any_loaded else 1

if __name__ == '__main__':
    sys.exit(main())