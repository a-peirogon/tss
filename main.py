#!/usr/bin/env python3
"""
Uso:
    python main.py build [src] [out]   construye el sitio
    python main.py new <nombre>        crea un proyecto de ejemplo
    python main.py serve [out] [port]  sirve el sitio en localhost
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.cli import main

if __name__ == "__main__":
    main()
