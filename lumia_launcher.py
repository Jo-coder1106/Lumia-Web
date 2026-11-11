"""Inicializador desktop do LumIA Web, empacotado com PyInstaller."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import threading
import webbrowser

try:
    import winreg
except ImportError:
    winreg = None

# O banco fica ao lado do executável, fora da pasta temporária do PyInstaller.
if getattr(sys, "frozen", False):
    APPLICATION_DIR = Path(sys.executable).resolve().parent
else:
    APPLICATION_DIR = Path(__file__).resolve().parent

os.environ["LUMIA_DATA_DIR"] = str(APPLICATION_DIR)

from werkzeug.serving import make_server
from app import app


BROWSERS = [
    ("Microsoft Edge", "msedge.exe", [
        Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")) / "Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/Edge/Application/msedge.exe",
    ]),
    ("Google Chrome", "chrome.exe", [
        Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")) / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/Application/chrome.exe",
    ]),
    ("Mozilla Firefox", "firefox.exe", [
        Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "Mozilla Firefox/firefox.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")) / "Mozilla Firefox/firefox.exe",
    ]),
    ("Brave", "brave.exe", [
        Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "BraveSoftware/Brave-Browser/Application/brave.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)")) / "BraveSoftware/Brave-Browser/Application/brave.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "BraveSoftware/Brave-Browser/Application/brave.exe",
    ]),
    ("Opera", "opera.exe", [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Opera/launcher.exe",
        Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "Opera/launcher.exe",
    ]),
    ("Vivaldi", "vivaldi.exe", [
        Path(os.environ.get("PROGRAMFILES", r"C:\Program Files")) / "Vivaldi/Application/vivaldi.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Vivaldi/Application/vivaldi.exe",
    ]),
]


def registry_browser_path(executable_name):
    """Resolve o executável por App Paths no Registro do Windows."""
    if winreg is None:
        return None

    registry_path = rf"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{executable_name}"
    roots = (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE)
    access_flags = (winreg.KEY_READ, winreg.KEY_READ | getattr(winreg, "KEY_WOW64_32KEY", 0))

    for root in roots:
        for access in access_flags:
            try:
                with winreg.OpenKey(root, registry_path, 0, access) as key:
                    value, _ = winreg.QueryValueEx(key, None)
                candidate = Path(os.path.expandvars(value.strip('"')))
                if candidate.is_file():
                    return candidate
            except (OSError, TypeError, ValueError):
                continue
    return None


def detect_browsers():
    """Retorna apenas navegadores cuja localização foi confirmada."""
    found = []
    for display_name, executable_name, common_paths in BROWSERS:
        candidate = registry_browser_path(executable_name)
        if candidate is None:
            command_names = [executable_name]
            if display_name == "Opera":
                command_names.append("launcher.exe")
            for command_name in command_names:
                located = shutil.which(command_name)
                if located:
                    candidate = Path(located)
                    break
        if candidate is None:
            candidate = next((path for path in common_paths if path.is_file()), None)
        if candidate and candidate.is_file():
            found.append((display_name, str(candidate)))
    return found


def choose_browser():
    """Mostra ao usuário uma lista de navegadores detectados no Windows."""
    if os.environ.get("LUMIA_NO_BROWSER") == "1":
        return None

    try:
        import tkinter as tk
        from tkinter import ttk

        detected = detect_browsers()
        options = [("Navegador padrão do Windows", None)] + detected

        root = tk.Tk()
        root.title("Abrir LumIA Web")
        root.resizable(False, False)
        root.attributes("-topmost", True)

        width, height = 440, 215
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = max((screen_width - width) // 2, 0)
        y = max((screen_height - height) // 2, 0)
        root.geometry(f"{width}x{height}+{x}+{y}")

        container = ttk.Frame(root, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Qual navegador deseja usar?",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 7))

        ttk.Label(
            container,
            text="O LumIA Web será aberto somente neste computador."
        ).pack(anchor="w", pady=(0, 12))

        labels = [item[0] for item in options]
        selected = tk.StringVar(value=labels[0])
        browser_list = ttk.Combobox(
            container,
            textvariable=selected,
            values=labels,
            state="readonly",
            width=47
        )
        browser_list.pack(fill="x", pady=(0, 17))

        result = {"path": None, "confirmed": False}

        def confirm():
            choice = selected.get()
            result["path"] = next((path for label, path in options if label == choice), None)
            result["confirmed"] = True
            root.destroy()

        def open_later():
            result["confirmed"] = True
            result["path"] = None
            root.destroy()

        buttons = ttk.Frame(container)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Abrir LumIA", command=confirm).pack(side="right")
        ttk.Button(buttons, text="Escolher depois", command=open_later).pack(side="right", padx=(0, 8))

        root.protocol("WM_DELETE_WINDOW", open_later)
        root.mainloop()

        if result["confirmed"]:
            return result["path"]
        return None
    except Exception as exc:
        # Em caso de ambiente sem interface gráfica, tenta o navegador padrão.
        print(f"Não foi possível abrir a janela de seleção do navegador: {exc}", flush=True)
        return None


def open_browser(url, browser_path):
    if os.environ.get("LUMIA_NO_BROWSER") == "1":
        return

    if browser_path:
        try:
            subprocess.Popen(
                [browser_path, url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )
            return
        except OSError as exc:
            print(f"Falha ao abrir o navegador selecionado: {exc}", flush=True)

    webbrowser.open(url)


def main():
    server = make_server("127.0.0.1", 0, app, threaded=True)
    address = f"http://127.0.0.1:{server.server_port}"

    print("=" * 58, flush=True)
    print("LumIA Web está em execução.", flush=True)
    print(f"Endereço: {address}", flush=True)
    print("Para encerrar o sistema, feche esta janela ou pressione Ctrl+C.", flush=True)
    print(f"Banco de dados: {APPLICATION_DIR / 'lumia.db'}", flush=True)
    print("=" * 58, flush=True)

    def launch():
        browser_path = choose_browser()
        if browser_path is None and os.environ.get("LUMIA_NO_BROWSER") == "1":
            return
        open_browser(address, browser_path)

    threading.Thread(target=launch, daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrando o LumIA Web...", flush=True)
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
