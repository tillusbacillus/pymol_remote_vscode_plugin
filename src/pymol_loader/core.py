from __future__ import annotations
import gzip, re
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from pymol_remote.client import PymolSession

def launch_session(port: int = 9123) -> PymolSession:
    return PymolSession(hostname="127.0.0.1", port=port)

def reinitialize(cmd: PymolSession) -> None:
    cmd.reinitialize()
    cmd.do('@~/.pymolrc')
    print("Reinitialized the session.")

def load_structures(
    cmd: PymolSession,
    path: str,
    *,
    recursive: bool = False,
    extensions: tuple[str, ...] = (".pdb", ".cif", ".pdb.gz", ".cif.gz"),
    fmt: Optional[str] = None,
    object_name: Optional[str] = None,
) -> List[Tuple[str, str, str]]:
    """
    Unified loader:
      - If `path` is a FILE: load exactly that file and return [(filepath, object_name, fmt)].
      - If `path` is a FOLDER: load all matching files (optionally recursive) and return a list of tuples.

    Notes
    -----
    - Uses string-based loading (`cmd.set_state`) to handle local buffers.
    - Supports .gz transparently.
    - Default object name for single-file mode is the filename stem unless `object_name` is provided.
    - In folder mode, names are derived from file stems and made unique by appending _2, _3, ... if needed.
    """
    root = Path(path).expanduser().resolve()

    def infer_fmt(p: Path, override: Optional[str]) -> str:
        if override is not None:
            f = override.lower()
            if f not in ("pdb", "cif"):
                raise ValueError("fmt must be 'pdb' or 'cif'")
            return f
        suffixes = [s.lower() for s in p.suffixes]
        if suffixes and suffixes[-1] == ".gz":
            suffixes = suffixes[:-1]
        for s in reversed(suffixes):
            if s in (".pdb", ".ent"):
                return "pdb"
            if s in (".cif", ".mmcif"):
                return "cif"
        raise ValueError(f"Could not infer format from filename: {p.name}")

    def read_text(p: Path) -> str:
        if p.suffix.lower() == ".gz":
            with gzip.open(p, "rt", encoding="utf-8", errors="replace") as fh:
                return fh.read()
        else:
            with open(p, "r", encoding="utf-8", errors="replace") as fh:
                return fh.read()

    def safe(name: str) -> str:
        n = re.sub(r"\W+", "_", name).strip("_")
        return n or "object"

    try:
        used = set(cmd.get_names("objects") or [])
    except Exception:
        used = set()

    def unique(base: str) -> str:
        name, i = base, 1
        while name in used:
            i += 1
            name = f"{base}_{i}"
        used.add(name)
        return name

    loaded: List[Tuple[str, str, str]] = []

    # ---- Single-file mode ----
    if root.is_file():
        fmt_use = infer_fmt(root, fmt)
        # derive name from filename if not provided
        if object_name is None:
            stem = root.stem
            if root.suffix.lower() == ".gz":
                stem = Path(stem).stem
            base = safe(stem)
        else:
            base = safe(object_name)
        obj = unique(base)

        buffer = read_text(root)
        try:
            cmd.set_state(buffer, format=fmt_use, object=obj)
        except TypeError:
            cmd.set_state(buffer, fmt_use, obj)
        loaded.append((str(root), obj, fmt_use))
        return loaded

    # ---- Folder mode ----
    if not root.is_dir():
        raise NotADirectoryError(f"Not a file or directory: {root}")

    allowed = {e.lower() for e in extensions}
    paths = root.rglob("*") if recursive else root.glob("*")

    files = [
        p for p in paths
        if p.is_file() and any("".join(p.suffixes).lower().endswith(ext) for ext in allowed)
    ]
    files.sort()

    for p in files:
        try:
            fmt_use = infer_fmt(p, None)
            stem = p.stem
            if p.suffix.lower() == ".gz":
                stem = Path(stem).stem
            base = safe(stem)
            obj = unique(base)

            buf = read_text(p)
            try:
                cmd.set_state(buf, format=fmt_use, object=obj)
            except TypeError:
                cmd.set_state(buf, fmt_use, obj)

            loaded.append((str(p), obj, fmt_use))
        except Exception as e:
            print(f"[WARN] Skipped {p}: {e}")

    return loaded