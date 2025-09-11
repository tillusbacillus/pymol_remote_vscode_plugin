# PyMOL Loader (VS Code Extension)

A VS Code extension to quickly load PDB/CIF structures (and `.gz` variants) into a running [PyMOL](https://pymol.org/) session via [`pymol-remote`](https://github.com/tristan0x/pymol-remote).

Right-click files or folders in the VS Code Explorer to send them to PyMOL.

---

## ✨ Features
- **Right-click on files** (`.pdb`, `.cif`, `.pdb.gz`, `.cif.gz`) → *Load in PyMOL*  
- **Right-click on folders** →  
  - *Load All in Folder (non-recursive)*  
  - *Load All in Folder (recursive)* _...for those pesky boltz predictions_
- **Settings toggle** for reinitializing the PyMOL session on each load  
- Works with multiple selected files or folders
- Lightweight wrapper script calls existing `load_structures` function
  - loading multiple files with the same name adds an index number (e.g. _2) to avoid overwriting files 

---

## ⚙️ Settings
In VS Code → Settings → **PyMOL Loader**:

- `pymolLoader.pythonPath` → path to Python interpreter (with `pymol_remote` and your helper module installed)  
- `pymolLoader.wrapperScript` → path to `tools/pymol_load_wrapper.py`  
- `pymolLoader.port` → PyMOL RPC port (default: 9123)  
- `pymolLoader.reinitializeOnLoad` → whether to reset PyMOL before loading (default: `true`)

---

## 🚀 Installation (local development)

1. Clone this repo and install dependencies:
   ```bash
   npm install
   npm run compile
