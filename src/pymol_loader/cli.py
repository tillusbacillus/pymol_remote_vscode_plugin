from __future__ import annotations
import argparse
import os
from .core import launch_session, reinitialize, load_structures

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Load PDB/CIF files (and .gz) into a running PyMOL via pymol-remote."
    )
    ap.add_argument('--port', type=int, default=9123, help='PyMOL RPC port (default: 9123)')
    ap.add_argument('--recursive', action='store_true', help='Recurse into folders')
    ap.add_argument('--no-reinit', action='store_true', help='Do not reinitialize PyMOL before loading')
    ap.add_argument('paths', nargs='*', help='Files or folders to load')
    args = ap.parse_args(argv)

    cmd = launch_session(port=args.port)

    if not args.no_reinit:
        try:
            reinitialize(cmd)
        except Exception:
            # Keep going even if reinit fails
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

if __name__ == "__main__":
    raise SystemExit(main())