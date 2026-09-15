# -*- coding: utf-8 -*-
"""Login Ferozo headless con espera del token Turnstile antes de enviar."""
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
    if not tab:
        nuevo = ws.call("Target.createTarget", {"url": "https://ferozo.host/login"})
        tid = nuevo["targetId"]
        time.sleep(8)
        tab = {"targetId": tid}
    sid = attach(ws, tab["targetId"])

    # recargar login limpio y esperar el token del captcha
    evaluate(ws, sid, "location.href = 'https://ferozo.host/login'")
    time.sleep(6)

    token = ""
    for i in range(8):
        token = evaluate(ws, sid, """(document.querySelector('input[name=cf-turnstile-response]')||{}).value || ''""") or ""
        if len(token) > 20:
            print("token turnstile OK (", len(token), "chars, intento", i + 1, ")")
            break
        print("esperando turnstile...", i + 1)
        time.sleep(5)
    if not token:
        print("TURNSTILE NO DIO TOKEN")

    # llenar y enviar
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
    print(evaluate(ws, sid, """(() => {
      const b = Array.from(document.querySelectorAll('button, input[type=submit]'))
        .find(x => (x.innerText||x.value||'').trim().toLowerCase().includes('ingresar'));
      if (!b) return 'NO BOTON';
      b.click();
      return 'CLICK';
    })()"""))

    for i in range(8):
        time.sleep(6)
        url = evaluate(ws, sid, "location.href")
        if "/login" not in url:
            print("LOGUEADO en", url)
            break
        print("intento", i + 1, ":", url)
    else:
        print("TEXTO:", evaluate(ws, sid, "document.body.innerText.slice(0, 300)"))
    ws.close()


if __name__ == "__main__":
    main()
