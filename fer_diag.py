# -*- coding: utf-8 -*-
"""Diagnóstico: qué muestra la pestaña de Ferozo en el Chrome headless."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.environ["LOCALAPPDATA"], "hermes", "skills", "whatsapp-web-cdp", "scripts"))
from wa_cdp import WS, find_page, attach, evaluate


def main():
    ws = WS(timeout=15)
    tab = find_page(ws, "ferozo.host")
    if not tab:
        print("NO hay pestaña de ferozo")
        return
    sid = attach(ws, tab["targetId"])
    print("URL:", evaluate(ws, sid, "location.href"))
    print("TITULO:", evaluate(ws, sid, "document.title"))
    txt = evaluate(ws, sid, "document.body.innerText.slice(0, 500)")
    print("TEXTO:", txt)
    print("INPUTS:", evaluate(ws, sid, "Array.from(document.querySelectorAll('input')).map(i=>i.type+':'+(i.name||i.placeholder||'')).slice(0,8)"))
    ws.close()


if __name__ == "__main__":
    main()
