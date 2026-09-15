# -*- coding: utf-8 -*-
"""Loguea en el panel Ferozo (Chrome headless) con usuario/contraseña."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.environ["LOCALAPPDATA"], "hermes", "skills", "whatsapp-web-cdp", "scripts"))
from wa_cdp import WS, find_page, attach, evaluate

USUARIO = "a0190762"
CLAVE = "RomaIsabella1219@"


def main():
    ws = WS(timeout=15)
    tab = find_page(ws, "ferozo.host")
    sid = attach(ws, tab["targetId"])

    # llenar con setter nativo + eventos (React/Angular)
    evaluate(ws, sid, """(() => {
      const set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
      const u = document.querySelector('input[name=_username]');
      const p = document.querySelector('input[name=_password]');
      set.call(u, '""" + USUARIO + """');
      u.dispatchEvent(new Event('input', {bubbles: true}));
      set.call(p, '""" + CLAVE + """');
      p.dispatchEvent(new Event('input', {bubbles: true}));
      return 'llenado';
    })()""")
    time.sleep(2)

    # click en el botón de ingresar (submit)
    r = evaluate(ws, sid, """(() => {
      const b = Array.from(document.querySelectorAll('button, input[type=submit]'))
        .find(x => (x.innerText||x.value||'').trim().toLowerCase().includes('ingresar'));
      if (!b) return 'NO BOTON';
      b.click();
      return 'CLICK';
    })()""")
    print("submit:", r)

    for i in range(10):
        time.sleep(6)
        url = evaluate(ws, sid, "location.href")
        print("intento", i + 1, "URL:", url)
        if "/login" not in url:
            txt = evaluate(ws, sid, "document.body.innerText.slice(0, 300)")
            print("LOGUEADO:", txt[:200])
            break
    else:
        txt = evaluate(ws, sid, "document.body.innerText.slice(0, 400)")
        print("SIGUE EN LOGIN. Texto:", txt[:300])
    ws.close()


if __name__ == "__main__":
    main()
