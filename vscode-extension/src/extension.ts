import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from 'path';

async function runLoader(targets: string[], recursive: boolean) {
  const config = vscode.workspace.getConfiguration('pymolLoader');
  const py = config.get<string>('pythonPath', 'python');
  const script = config.get<string>('wrapperScript', '');
  const port = config.get<number>('port', 9123);
  const reinit = config.get<boolean>('reinitializeOnLoad', true);

  const args = ['-m', 'pymol_loader.cli', '--port', String(port)];
  if (recursive) args.push('--recursive');
  if (!reinit) args.push('--no-reinit');
  args.push('--', ...targets);

  const channel = vscode.window.createOutputChannel('PyMOL Loader');
  channel.show(true);
  channel.appendLine(`Running: ${py} ${args.map(a => (a.includes(' ') ? `"${a}"` : a)).join(' ')}`);

  const cwd = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath; // optional improvement

  await vscode.window.withProgress(
    { location: vscode.ProgressLocation.Notification, title: 'Loading into PyMOL…', cancellable: false },
    () => new Promise<void>((resolve, reject) => {
      const proc = spawn(py, args, { cwd });
      proc.stdout.on('data', d => channel.append(d.toString()));
      proc.stderr.on('data', d => channel.append(d.toString()));
      proc.on('error', err => reject(err));
      proc.on('close', code => {
        if (code === 0) {
          vscode.window.showInformationMessage('Loaded structures into PyMOL.');
          resolve();
        } else {
          reject(new Error(`Wrapper exited with code ${code}`));
        }
      });
    })
  );
}

export function activate(context: vscode.ExtensionContext) {
  // file command
  context.subscriptions.push(vscode.commands.registerCommand(
    'pymolLoader.loadStructures',
    async (uri: vscode.Uri, selectedUris?: vscode.Uri[]) => {
      const uris = (selectedUris && selectedUris.length ? selectedUris : (uri ? [uri] : []))
        .filter(u => u.scheme === 'file' && !u.fsPath.endsWith(path.sep));
      const files = uris.map(u => u.fsPath);
      if (!files.length) {
        vscode.window.showWarningMessage('PyMOL Loader: No files selected.');
        return;
      }
      await runLoader(files, /*recursive*/ false);
    }
  ));

  // non-recursive folder command
  context.subscriptions.push(vscode.commands.registerCommand(
    'pymolLoader.loadFolder',
    async (uri: vscode.Uri, selectedUris?: vscode.Uri[]) => {
      const uris = (selectedUris && selectedUris.length ? selectedUris : (uri ? [uri] : []))
        .filter(u => u.scheme === 'file');
      const folders = uris.map(u => u.fsPath);
      if (!folders.length) {
        vscode.window.showWarningMessage('PyMOL Loader: No folders selected.');
        return;
      }
      await runLoader(folders, /*recursive*/ false);
    }
  ));

  // recursive folder command
  context.subscriptions.push(vscode.commands.registerCommand(
    'pymolLoader.loadFolderRecursive',
    async (uri: vscode.Uri, selectedUris?: vscode.Uri[]) => {
      const uris = (selectedUris && selectedUris.length ? selectedUris : (uri ? [uri] : []))
        .filter(u => u.scheme === 'file');
      const folders = uris.map(u => u.fsPath);
      if (!folders.length) {
        vscode.window.showWarningMessage('PyMOL Loader: No folders selected.');
        return;
      }
      await runLoader(folders, /*recursive*/ true);
    }
  ));
}

export function deactivate() {}