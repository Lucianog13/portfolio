# -*- coding: utf-8 -*-
"""Sube sitio.zip por 'Subir mi sitio' de Ferozo y extrae en public_html."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.environ["LOCALAPPDATA"], "hermes", "skills", "whatsapp-web-cdp", "scripts"))
from wa_cdp import WS, find_page, attach, evaluate, CDPError

ZIP = r"C:\Users\Luchi$\Desktop\portfolio\sitio.zip"


def click_por_texto(ws, sid, texto, exacto=False):
    """Clickea un botón/enlace por su texto visible."""
    t = repr(texto)
    cond = f"b.innerText.trim()==={t}" if exacto else f"b.innerText.trim().includes({t})"
    return evaluate(ws, sid, f"""(() => {{
      const btns = Array.from(document.querySelectorAll('button, a'));
      const b = btns.find(b => {cond});
      if (!b) return 'NO ENCONTRADO';
      b.click();
      return 'CLICK: ' + b.innerText.trim();
    }})()""")


def main():
    ws = None
    for intento in range(8):
        try:
            ws = WS(timeout=15)
            break
        except Exception as e:
            print("WS intento", intento + 1, "falló:", type(e).__name__)
            time.sleep(12)
    if ws is None:
        raise SystemExit("No se pudo conectar al Chrome por CDP")
    tab = find_page(ws, "ferozo.host")
    if not tab:
        # headless no restaura pestañas: crear una y navegar (la sesión
        # está en las cookies del perfil)
        nuevo = ws.call("Target.createTarget", {"url": "https://ferozo.host/"})
        tid = nuevo["targetId"]
        time.sleep(8)
        tab = {"targetId": tid}
    sid = attach(ws, tab["targetId"])
    # asegurar que esté en la página de subida
    evaluate(ws, sid, "location.hash = '#/website/uploadsite'")
    time.sleep(5)

    # 1) adjuntar el zip al input file (sin abrir diálogo nativo)
    ws.call("DOM.enable", session_id=sid)
    doc = ws.call("DOM.getDocument", session_id=sid)
    raiz = doc["root"]["nodeId"]
    nodo = ws.call("DOM.querySelector", {"nodeId": raiz, "selector": "input[name=file]"}, session_id=sid)
    print("input file nodeId:", nodo)
    ws.call("DOM.setFileInputFiles", {"nodeId": nodo["nodeId"], "files": [ZIP]}, session_id=sid)
    print("zip adjuntado")

    time.sleep(2)
    print(click_por_texto(ws, sid, "Subir", exacto=True))

    # esperar a que el archivo aparezca como subido
    for i in range(10):
        time.sleep(5)
        texto = evaluate(ws, sid, "document.body.innerText")
        if "sitio.zip" in texto:
            print("archivo subido (intento", i + 1, ")")
            break
        print("esperando subida...", i + 1)
    else:
        print("TEXTO ACTUAL:", texto[:800])
        raise SystemExit("el zip no aparece como subido")

    # 2) destino: public_html
    print(click_por_texto(ws, sid, "Usar directorio raíz public_html"))

    # 3) extraer
    time.sleep(2)
    print(click_por_texto(ws, sid, "Extraer", exacto=True))

    # 4) verificar resultado
    for i in range(10):
        time.sleep(5)
        texto = evaluate(ws, sid, "document.body.innerText")
        if "extra" in texto.lower() and ("éxito" in texto.lower() or "correct" in texto.lower() or "ok" in texto.lower()):
            print("EXTRACCIÓN OK (intento", i + 1, ")")
            print(texto[:900])
            break
        print("esperando extracción...", i + 1)
    else:
        print("TEXTO FINAL:", texto[:900])
    ws.close()


if __name__ == "__main__":
    main()
