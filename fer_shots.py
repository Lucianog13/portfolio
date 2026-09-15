# -*- coding: utf-8 -*-
"""Captura screenshots con el Chrome del usuario (CDP) para tarjetas y OG."""
import base64
import os
import sys
import time

sys.path.insert(0, os.path.join(os.environ["LOCALAPPDATA"], "hermes", "skills", "whatsapp-web-cdp", "scripts"))
from wa_cdp import WS, attach

SALIDA = r"C:\Users\Luchi$\Desktop\portfolio\assets"

OBJETIVOS = [
    # (url, archivo, ancho, alto)  — og 1200x630, tarjetas 1280x800
    ("https://www.verticelabs.com.ar/", "og-verticelabs.png", 1200, 630),
    ("https://lucianog13.github.io/simpleat/", "simpleat.png", 1280, 800),
    ("https://lucianog13.github.io/abastece-demo/", "abastece.png", 1280, 800),
    ("https://lucianog13.github.io/bot-cash/", "bot-cash.png", 1280, 800),
]


def main():
    ws = WS(timeout=15)
    # una pestaña reusable para todas las capturas
    tab = ws.call("Target.createTarget", {"url": "about:blank"})
    tid = tab["targetId"]
    sid = attach(ws, tid)

    for url, archivo, ancho, alto in OBJETIVOS:
        print("capturando:", archivo, "<-", url)
        ws.call("Emulation.setDeviceMetricsOverride",
                {"width": ancho, "height": alto, "deviceScaleFactor": 1, "mobile": False},
                session_id=sid)
        ws.call("Page.enable", session_id=sid)
        ws.call("Page.navigate", {"url": url}, session_id=sid)
        time.sleep(11)  # deja renderizar fuentes/imágenes
        res = ws.call("Page.captureScreenshot", {"format": "png"}, session_id=sid)
        datos = base64.b64decode(res["data"])
        ruta = os.path.join(SALIDA, archivo)
        with open(ruta, "wb") as f:
            f.write(datos)
        print("  guardado:", ruta, len(datos), "bytes")
    ws.close()


if __name__ == "__main__":
    main()
