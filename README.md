# PyMOL Loader (VS Code Extension)

A VS Code extension to quickly load PDB/CIF structures (and `.gz` variants) from a remote connection into a locally running [PyMOL](https://pymol.org/) session via [`pymol-remote`](https://github.com/tristan0x/pymol-remote).

---

## ✨ Features

- In the VS Code file explorer...
  - Right-click on **files** (`.pdb`, `.cif`, `.pdb.gz`, `.cif.gz`) → *Load in PyMOL*
  - Right-click on **folders** →
    - *Load All in Folder (non-recursive)*
    - *Load All in Folder (recursive)*
- Multiple file or folder selection supported
- Setting to toggle whether PyMOL is reinitialized before load
- Loading files with the same name indexes them without overwriting them in PyMOL

---

## ⚙️ Installation

Setup is required on both your **local machine** (where PyMOL runs) and the **remote server** (HPC, where VS Code Remote-SSH and the loader run).

### 1) Local machine: set up PyMOL + pymol-remote

- Install PyMOL on your local machine.
- Install pymol-remote into the python interpreter that runs pymol
  ```
  pip install pymol-remote
  ```

For more information about the installation refer to the [pymol-remote](https://github.com/Croydon-Brixton/pymol-remote) GitHub.

### 2) Local machine: SSH port forwarding (reverse tunnel)

To let the remote HPC reach your **local** PyMOL, add a reverse tunnel to your local `~/.ssh/config`:

```ssh
Host <alias>
    HostName this.is.your.remote.server.adress
    User <your-username>
    # Expose REMOTE port that forwards to your LOCAL PyMOL at 127.0.0.1:9123
    RemoteForward <chosen-port-number> 127.0.0.1:9123
    ServerAliveInterval 30
    ServerAliveCountMax 4
```

Choose any alias you want.

The chosen port needs to be unused for the extension to work. Every user of pymol-remote on the same remote server needs a different port numbe*r.*

Now, **connect to the remote server using that host alias**. Doing so through VS Code ensures that the extension will always have the open port available while you are connected. Processes on the **remote** (HPC) can now connect to `127.0.0.1:9123`, which is forwarded to your **local** PyMOL.

### 3) Install the VS Code extension (remote)

- Download the `.vsix` file from the releases on GitHub.
- **VS Code Remote-SSH** (connected to \`\<alias>\`  ): Extensions → `…` → **Install from VSIX…**

### 4) Create the Python environment (remote)

On the remote server, clone the repo and run the installer \*\*to create/update the python environment\*\* for the extension:

```bash
git clone https://github.com/tillusbacillus/pymol_remote_vscode_plugin.git
cd pymol_remote_vscode_plugin
bash install.sh
```

This creates the Conda env `pymol-loader` and installs dependencies.

### 5) Configure the extension in VS Code (remote)

Set the interpreter path for the extension in the VS Code settings:

```bash
conda activate pymol-loader
which python
```

Copy the printed path and set it in the extension settings (Remote-SSH window):

- **Settings → PyMOL Loader: Python Path** → paste the path from `which python`
- **PyMOL Loader: Port** → your chosen port from step 2)
- **PyMOL Loader: Reinitialize On Load** → on/off to taste

---

## ▶️ Running Extension

- Open pymol\*remote on the local machine. Usually through `pymol_remote` in the terminal, while having activated the right python environment.
- Connect to the remote connection throught VS Code. The port should be forwarded as set in 2) of the installation.
- Use by right-clicking on files or folders and selecting one of the following:
  - *Load in PyMOL*
  - *Load All in Folder (non-recursive)*
  - *Load All in Folder (recursive)*
- The structures should pop up in the pymol instance running on you local machine.

---

## ✅ Verify Setup

To confirm everything works:

1. **Check PyMOL RPC server locally**:

   ```bash
   lsof -i :9123
   ```

   After launching `pymol_remote` locally, you should see PyMOL listening on your laptop.

2. **Check SSH tunnel**: after connecting with VS Code Remote-SSH, run on the **remote HPC**:

   ```bash
   nc -zv 127.0.0.1 9123
   ```

   Should report `succeeded!`.

3. **Check CLI loader** (remote HPC):

   ```bash
   conda activate pymol-loader
   python -m pymol_loader.cli --port <your-port> -- /path/to/file.pdb
   ```

   You should see `[OK] ... -> object (pdb)` in the output.

4. **Check VS Code extension**: right-click a `.pdb` file and choose *Load in PyMOL*. Structure should appear in your local PyMOL.

If all four checks succeed, your setup is correct.

---

## 🧑‍💻 Development

- TypeScript sources in `vscode-extension/src/`
- Compile with:
  ```bash
  npm install
  npm run compile
  npx @vscode/vsce package
  ```

---

## 📄 License

MIT

