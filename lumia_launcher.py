"""Launcher desktop do LumIA Web, empacotado com PyInstaller."""
from pathlib import Path
import os
import sys
import threading
import time
import webbrowser

# Mantém o banco de dados ao lado do executável, sem gravar na pasta temporária
# usada pelo PyInstaller no modo --onefile.
if getattr(sys, "frozen", False):
    application_dir = Path(sys.executable).resolve().parent
else:
    application_dir = Path(__file__).resolve().parent

os.environ["LUMIA_DATA_DIR"] = str(application_dir)

from werkzeug.serving import make_server
from app import app


def main():
    server = make_server("127.0.0.1", 0, app, threaded=True)
    port = server.server_port
    address = f"http://127.0.0.1:{port}"

    print("=" * 58)
    print("LumIA Web está em execução.")
    print(f"Endereço: {address}")
    print("O navegador será aberto automaticamente.")
    print("Para encerrar o sistema, feche esta janela ou pressione Ctrl+C.")
    print(f"Banco de dados: {application_dir / 'lumia.db'}")
    print("=" * 58)

    threading.Timer(1.0, lambda: webbrowser.open(address)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrando o LumIA Web...")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
