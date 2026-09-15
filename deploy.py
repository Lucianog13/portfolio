# -*- coding: utf-8 -*-
"""
deploy.py — Sube el sitio de Vértice (VerticeLABS) al hosting de DonWeb.

Uso:
    export DONWEB_HOST=ftp.tudominio.com.ar   (o la IP del servidor)
    export DONWEB_USER=usuario
    export DONWEB_PASS=contraseña
    python deploy.py

Notas de DonWeb (hosting compartido):
    - Solo FTP/FTPS puerto 21 (TLS explícito obligatorio, sin SSH/SFTP).
    - Raíz pública: public_html.
    - Límite de transferencias simultáneas bajo: subimos de a un archivo, en orden.

No guarda credenciales: se leen solo de variables de entorno.
"""
import ftplib
import os
import sys
from pathlib import Path

# Cargar credenciales de .env local si existe (nunca se commitea)
_ENV = Path(__file__).resolve().parent / ".env"
if _ENV.exists():
    for _linea in _ENV.read_text(encoding="utf-8").splitlines():
        _linea = _linea.strip()
        if _linea and not _linea.startswith("#") and "=" in _linea:
            _k, _v = _linea.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

# Archivos y carpetas que componen el sitio (raíz del repo).
ARCHIVOS_SUELTOS = ["index.html"]
CARPETAS = ["css", "js", "assets"]


def conectar():
    host = os.environ.get("DONWEB_HOST")
    user = os.environ.get("DONWEB_USER")
    clave = os.environ.get("DONWEB_PASS")
    if not all([host, user, clave]):
        sys.exit("Faltan credenciales: definí DONWEB_HOST, DONWEB_USER y DONWEB_PASS.")
    ftp = ftplib.FTP_TLS(host, timeout=30)
    ftp.connect(host, 21)
    ftp.login(user, clave)
    ftp.prot_p()  # canal de datos cifrado
    return ftp


def subir_archivo(ftp, ruta_local, ruta_remota):
    with open(ruta_local, "rb") as f:
        ftp.storbinary("STOR " + ruta_remota, f)
    print("  ↑", ruta_remota)


def main():
    raiz = Path(__file__).resolve().parent
    ftp = conectar()
    try:
        # Raíz pública del hosting (existe en todo plan DonWeb).
        try:
            ftp.cwd("public_html")
        except ftplib.error_perm:
            sys.exit("No encontré la carpeta public_html en el servidor. Revisá el usuario FTP.")

        for nombre in ARCHIVOS_SUELTOS:
            local = raiz / nombre
            if local.exists():
                subir_archivo(ftp, local, nombre)

        for carpeta in CARPETAS:
            origen = raiz / carpeta
            if not origen.is_dir():
                continue
            try:
                ftp.mkd(carpeta)
            except ftplib.error_perm:
                pass  # ya existe
            for archivo in sorted(origen.iterdir()):
                if archivo.is_file():
                    subir_archivo(ftp, archivo, carpeta + "/" + archivo.name)

        # Verificación: listar raíz y contar archivos subidos.
        contenido = ftp.nlst()
        print("\nOK. Contenido de public_html:", len(contenido), "elementos:")
        for item in sorted(contenido):
            print("  ·", item)
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()


if __name__ == "__main__":
    main()
