cat > README.md << 'EOF'
# PyMOL Loader (VS Code)

Right-click PDB/CIF files or folders in VS Code to load them into a running PyMOL (via pymol-remote).

## Commands
- **Load in PyMOL** (files)
- **Load All in Folder (non-recursive)**
- **Load All in Folder (recursive)**

## Settings
- `pymolLoader.pythonPath`
- `pymolLoader.wrapperScript`
- `pymolLoader.port`
- `pymolLoader.reinitializeOnLoad`

## Dev
```bash
npm install
npm run compile
npx @vscode/vsce package --allow-missing-repository