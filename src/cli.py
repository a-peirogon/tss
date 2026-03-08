import http.server
import os
import socketserver
import sys
from pathlib import Path

import yaml

from .project import build
from .scaffold import new_project


def load_conf(src_dir: Path) -> dict:
    conf_file = src_dir / "conf.yaml"
    if conf_file.exists():
        return yaml.safe_load(conf_file.read_text(encoding="utf-8")) or {}
    return {}


def serve(out_dir: Path, port: int = 8000):
    os.chdir(out_dir)
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"Sirviendo en http://localhost:{port}/  (Ctrl+C para detener)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__ or "apuntes.py build | new <nombre> | serve")
        sys.exit(0)

    cmd = args[0]

    if cmd == "build":
        src = Path(args[1]) if len(args) > 1 else Path(".")
        out = Path(args[2]) if len(args) > 2 else src / "_build" / "html"
        build(src, out, load_conf(src))

    elif cmd == "new":
        if len(args) < 2:
            print("Uso: python apuntes.py new <nombre>")
            sys.exit(1)
        new_project(args[1], Path("."))

    elif cmd == "serve":
        out = Path(args[1]) if len(args) > 1 else Path(".") / "_build" / "html"
        port = int(args[2]) if len(args) > 2 else 8000
        if not out.exists():
            print(f"Error: {out} no existe, ejecuta build primero.")
            sys.exit(1)
        serve(out, port)

    else:
        print(f"Comando desconocido: {cmd}")
        sys.exit(1)
