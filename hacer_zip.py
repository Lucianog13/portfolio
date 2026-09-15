# -*- coding: utf-8 -*-
"""Crea sitio.zip con los archivos del sitio para 'Subir mi sitio' de Ferozo."""
import zipfile
from pathlib import Path

raiz = Path(__file__).resolve().parent
incluir = ["index.html", ".htaccess"]
carpetas = ["css", "js", "assets"]
excluir = {"captura-desktop.png", "captura-movil.png"}  # legacy sin uso

with zipfile.ZipFile(raiz / "sitio.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for nombre in incluir:
        p = raiz / nombre
        if p.exists():
            z.write(p, nombre)
    for carpeta in carpetas:
        for p in sorted((raiz / carpeta).iterdir()):
            if p.is_file() and p.name not in excluir:
                z.write(p, str(p.relative_to(raiz)))

z = zipfile.ZipFile(raiz / "sitio.zip")
print("ZIP OK:", len(z.namelist()), "archivos")
for n in z.namelist():
    print(" ", n)
