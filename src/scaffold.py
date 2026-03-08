import sys
from datetime import datetime
from pathlib import Path
from textwrap import dedent


EXAMPLE_CONF = '''\
project: "{name}"
author: "Tu nombre"
language: es
year: {year}
'''

EXAMPLE_INDEX = '''\
---
title: "{name}"
---

# {name}

## Apuntes e investigacion

::version: 1.0.0

Bienvenido. Edita los ficheros `.md` y ejecuta `python main.py build`.

:::toctree
intro/index: 1. Introduccion
contenido/index: 2. Contenido principal
:::

---

**Recursos adicionales:**

- [Markdown Guide](https://www.markdownguide.org/)
- [Python Docs](https://docs.python.org/)
'''

EXAMPLE_INTRO_INDEX = '''\
---
title: "1. Introduccion"
---

# 1. Introduccion

:::toctree
intro/bienvenida
intro/instalacion
:::
'''

EXAMPLE_INTRO_BIENVENIDA = '''\
---
title: "1.1. Bienvenida"
---

# Bienvenida

Este es tu primer apunte. Puedes usar **Markdown** libremente.

!!! note
    Los bloques de nota se generan automaticamente.

!!! tip
    Usa `:::toctree` para enlazar paginas entre si.

!!! warning
    Guarda siempre tus ficheros antes de compilar.

## Codigo

```python
def hola_mundo():
    print("Hola, mundo!")

hola_mundo()
```

## Tablas

| Columna A | Columna B | Columna C |
|-----------|-----------|-----------|
| Valor 1   | Valor 2   | Valor 3   |
| Valor 4   | Valor 5   | Valor 6   |
'''

EXAMPLE_INTRO_INSTALACION = '''\
---
title: "1.2. Instalacion"
---

# Instalacion

## Requisitos

- Python 3.11 o superior
- pip

## Pasos

1. Copia `main.py` en tu proyecto.
2. Instala las dependencias:

```bash
pip install markdown pyyaml pygments
```

3. Edita `conf.yaml` y los ficheros `.md`.
4. Ejecuta:

```bash
python main.py build
```
'''

EXAMPLE_CONTENIDO_INDEX = '''\
---
title: "2. Contenido principal"
---

# 2. Contenido principal

:::toctree
contenido/capitulo1
:::
'''

EXAMPLE_CONTENIDO_CAP1 = '''\
---
title: "2.1. Primer capitulo"
---

# Primer capitulo

Escribe aqui el contenido del primer capitulo.

## Seccion 1

Parrafo con *cursiva*, **negrita** y `codigo inline`.

> Cita en bloque.

## Seccion 2

- Elemento uno
- Elemento dos
- Elemento tres

!!! important
    Los detalles importan.
'''


def new_project(name: str, base_dir: Path):
    project_dir = base_dir / name
    if project_dir.exists():
        print(f"Error: ya existe el directorio {project_dir}")
        sys.exit(1)

    year = datetime.now().year
    files = {
        "conf.yaml":              EXAMPLE_CONF.format(name=name, year=year),
        "index.md":               EXAMPLE_INDEX.format(name=name),
        "intro/index.md":         EXAMPLE_INTRO_INDEX,
        "intro/bienvenida.md":    EXAMPLE_INTRO_BIENVENIDA,
        "intro/instalacion.md":   EXAMPLE_INTRO_INSTALACION,
        "contenido/index.md":     EXAMPLE_CONTENIDO_INDEX,
        "contenido/capitulo1.md": EXAMPLE_CONTENIDO_CAP1,
    }
    for rel, content in files.items():
        path = project_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(dedent(content).lstrip(), encoding="utf-8")

    print(f"Proyecto '{name}' creado en {project_dir}/")
    print(f"  cd {project_dir}")
    print(f"  python main.py build")
