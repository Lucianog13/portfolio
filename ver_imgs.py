# -*- coding: utf-8 -*-
"""Analiza las 2 imágenes de referencia con llava-phi3 (Ollama local)."""
import base64
import json
import urllib.request

IMG1 = r"C:\Users\Luchi$\AppData\Roaming\Hermes\composer-images\image_bf0841.png"
IMG2 = r"C:\Users\Luchi$\AppData\Roaming\Hermes\composer-images\image_5ea1d5.png"

PROMPTS = {
    "IMG1 (ejemplo SVGator)": (
        "Describe this image in detail: what 3D shape or object is shown, what are its "
        "colors and style (flat, gradient, 3D, isometric, neon), what text or logos "
        "appear, and what animation does it suggest? Be specific and factual."
    ),
    "IMG2 (pagina actual)": (
        "Describe this image in detail: what is the large main element in the upper "
        "center, what colors and shapes appear, is there any big 3D logo, and does "
        "anything look ugly or broken? Be specific and factual."
    ),
}


def analizar(path, prompt):
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    req = {
        "model": "llava-phi3",
        "prompt": prompt,
        "images": [b64],
        "stream": False,
        "options": {"num_predict": 170, "temperature": 0},
    }
    r = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps(req).encode(),
        headers={"Content-Type": "application/json"},
    )
    resp = json.loads(urllib.request.urlopen(r, timeout=600).read())
    return resp.get("response", "").strip()


for nombre, path in [("IMG1", IMG1), ("IMG2", IMG2)]:
    print("=" * 30, nombre, "=" * 30)
    print(analizar(path, PROMPTS[nombre + (" (ejemplo SVGator)" if nombre == "IMG1" else " (pagina actual)")]))
    print()
