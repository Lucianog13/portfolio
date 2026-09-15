# MEMORY.md — Vértice · VerticeLABS (sitio web)

> Última actualización: 2026-09-14 · Sesión: rediseño "vende sola" + conexión DonWeb

## Qué es

Landing de venta de VerticeLABS (marca: **Vértice** · tagline "IA . AUTOMATIZACIÓN . SaaS").
Repositorio: `github.com/Lucianog13/portfolio`. Vista previa: https://lucianog13.github.io/portfolio/
Dominio de producción: **www.verticelabs.com.ar** (DonWeb, hosting compartido, panel Ferozo).

## Estructura (modular, Ley 1 del protocolo)

| Archivo | Controla |
|---|---|
| `index.html` | Estructura + contenido (todas las secciones, copy de venta, meta/SEO/OG/JSON-LD) |
| `css/estilos.css` | TODO el diseño: variables de paleta, fondo, nav, hero 3D, secciones, responsive, reduced-motion |
| `js/main.js` | Nav con blur, scroll reveal 3D, tilt de tarjetas, parallax del logo, partículas canvas |
| `assets/favicon.svg` | Favicon hexágono (logo) |
| `assets/*.png` | Capturas de productos (super, atende, vitrina) + legacy (captura-*, sin uso en cards) |
| `deploy.py` | Subida FTPS a DonWeb (public_html). Credenciales por variables de entorno, NUNCA en el repo |
| `MEMORY.md` | Este archivo (Ley 5) |

## Decisiones tomadas

- **Hosting**: se sube a DonWeb (aprovechar lo pagado: SSL gratis, mail info@, panel Ferozo).
  GitHub queda como fuente + preview. DNS ya apunta a DonWeb (200.58.111.131) — lo armó DonWeb solo.
- **Paleta de marca**: azul noche `#0a1128` + gradiente azul→violeta→fucsia + fuente Sora.
  El viejo `css/style.css` (navy+gold) era del portfolio personal y se eliminó.
- **WhatsApp de ventas**: wa.me/543434065289 (número de Luciano). PENDIENTE confirmar con Lucho.
- **Sections nuevas** (no existían): Servicios, Proceso+clientes, FAQ, Contacto real, nav CTA "Hablemos".
- **Clientes nombrados** en "Proceso": distribuidora mayorista, concejo municipal, comercios/servicios.
  PENDIENTE confirmar con Lucho qué puede hacerse público (147 Digital es sensible).

## Estado de bloques (protocolo Ley 4)

- [x] Bloque 1: estructura modular (CSS/JS separados, viejo CSS eliminado)
- [x] Bloque 2: hero de venta (CTA WhatsApp primario, línea de confianza)
- [x] Bloque 3: servicios (4, con links wa.me prellenados)
- [x] Bloque 4: tarjetas de productos con capturas (3 con foto real, 3 con emoji — capturar faltantes)
- [x] Bloque 5: proceso + clientes reales
- [x] Bloque 6: contacto real + FAQ
- [x] Bloque 7: SEO/OG/favicon/canonical/JSON-LD
- [ ] Capturas faltantes: simpleat, abastece-demo, bot-cash (tarjetas) + og-verticelabs.png
- [ ] Optimizar peso de imágenes (super.png 710 KB, vitrina.png 608 KB → uv + Pillow)
- [ ] Auditoría responsive (skill auditoria-responsive-web)
- [ ] Deploy a DonWeb: falta usuario/contraseña de Ferozo o FTP (pedir a Lucho)
- [ ] En panel Ferozo: SSL gratis + "Forzar https" + redirección root→www

## Deploy a DonWeb (cómo se usa)

```bash
export DONWEB_HOST=... DONWEB_USER=... DONWEB_PASS=...
python deploy.py
```
Sube index.html + css/ + js/ + assets/ a `public_html` por FTPS (puerto 21, TLS explícito,
que es lo que exige DonWeb; sin SSH). El hosting NO usa ramas ni build: el sitio es estático.
Después de la primera subida: activar SSL en Ferozo → Dominios → Forzar https.

## Cambios pendientes / notas

- El JSON-LD declara fundadores "Luciano González / Martín González / Tomás" — confirmar apellidos con Lucho.
- DonWeb NO da SSH/SFTP en hosting compartido: solo FTP/FTPS puerto 21. Para cambiar algo del
  sitio: editar local → `python deploy.py` (o push a GitHub para el preview).
- No borrar `assets/captura-*.png` hasta decidir si se usan para og-image o se descartan.
