# -*- coding: utf-8 -*-
"""Descarga fotos de stock de Pexels por CDP (fetch desde el contexto de la página)."""
import base64
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.environ["LOCALAPPDATA"], "hermes", "skills", "whatsapp-web-cdp", "scripts"))
from wa_cdp import WS, attach, evaluate

SALIDA = r"C:\Users\Luchi$\Desktop\portfolio\assets"
BUSQUEDAS = [
    ("profesional oficina escritorio", "audiencia-profesional"),
    ("tienda comercio local", "audiencia-comercio"),
    ("emprendedor laptop trabajar", "audiencia-emprendedor"),
    ("edificio municipal gobierno", "audiencia-institucion"),
]


def main():
    ws = WS(timeout=15)
    for q, nombre in BUSQUEDAS:
        url_q = "https://www.pexels.com/es-es/buscar/" + q.replace(" ", "%20") + "/"
        tab = ws.call("Target.createTarget", {"url": url_q})
        sid = attach(ws, tab["targetId"])
        time.sleep(9)
        urls = evaluate(ws, sid, """Array.from(document.querySelectorAll('img'))
            .map(i => i.currentSrc || i.src)
            .filter(s => s.includes('images.pexels.com/photos/'))
            .slice(0, 5)""")
        print(q, "→", (urls or ["(sin imgs)"])[:2])
        if not urls:
            print("  texto:", evaluate(ws, sid, "document.body.innerText.slice(0, 120)"))
            continue
        # reescribir parámetros para pedir alta resolución al CDN de Pexels
        url_grande = urls[0].split("?")[0] + "?auto=compress&cs=tinysrgb&w=1200&h=800&fit=crop"
        print("  url:", url_grande[:110])
        b64 = evaluate(ws, sid, "fetch(" + json.dumps(url_grande) + ").then(r=>r.blob()).then(b=>new Promise(res=>{const fr=new FileReader(); fr.onload=()=>res(fr.result.split(',')[1]); fr.readAsDataURL(b);}))",
                       await_promise=True, timeout=90)
        ruta = os.path.join(SALIDA, nombre + ".jpg")
        with open(ruta, "wb") as f:
            f.write(base64.b64decode(b64))
        print("  guardado:", ruta, len(b64), "chars b64")
    ws.close()


if __name__ == "__main__":
    main()
