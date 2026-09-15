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
- [x] Bloque 4: tarjetas de productos con capturas reales (las 6: super/atende/vitrina +
      simpleat/abastece/bot-cash capturadas por CDP)
- [x] Bloque 5: proceso + clientes reales
- [x] Bloque 6: contacto real + FAQ
- [x] Bloque 7: SEO/OG/favicon/canonical/JSON-LD + og-verticelabs.png
- [x] DEPLOY A DONWEB HECHO (15-09-2026): www.verticelabs.com.ar online,
      SSL Let's Encrypt activo, .htaccess fuerza https+www (verificado 301→200)
- [ ] Optimizar peso de imágenes (super.png 710 KB, vitrina.png 608 KB → uv + Pillow)
- [ ] Auditoría responsive (skill auditoria-responsive-web)
- [ ] Confirmar con Lucho: número de WhatsApp en CTAs, clientes visibles en público,
      apellidos en JSON-LD, qué hacer con el WordPress instalado en public_html

## Deploy a DonWeb (cómo se usa — CAMINO PROBADO)

FTP directo (deploy.py) NO funcionó al inicio: la contraseña FTP es distinta a la
del panel Ferozo (530 Login incorrect). El camino que SÍ funciona es el panel:

```bash
python hacer_zip.py            # arma sitio.zip con los archivos del sitio
python fer_subir.py            # entra por CDP al panel Ferozo (Chrome del usuario
                               # ya logueado) → Mi Sitio Web → Subir mi sitio →
                               # adjunta el zip → extrae en public_html
```
- fer_subir.py necesita el Chrome del usuario corriendo con CDP 9222 y la pestaña
  de ferozo.host logueada (usuario a0190762). Reusa wa_cdp.py (skill whatsapp-web-cdp).
- fer_shots.py captura screenshots por CDP (para tarjetas/og) con Emulation.setDeviceMetricsOverride.
- deploy.py (FTPS) queda listo por si algún día se consigue la contraseña FTP real
  (en el panel: Mi Sitio Web → FTP → Cambiar Contraseña).
- El panel Ferozo también tiene GIT (#/website/git) y Administrador de archivos,
  alternativas válidas si el zip fallara.
- SSL: ya emitido por Let's Encrypt (*.verticelabs.com.ar). No tocar salvo renovación.

## Cambios pendientes / notas

- El JSON-LD declara fundadores "Luciano González / Martín González / Tomás" — confirmar apellidos con Lucho.
- En public_html quedó un WordPress instalado (venía con el hosting) + archivos captura-*.png
  legacy. No rompen nada (nuestro index.html tiene prioridad), pero conviene borrarlos
  cuando Lucho confirme que no los necesita.
- Cuenta de correo existente: marcelogonzalez@verticelabs.com.ar. Falta crear info@
  (panel → Email → Cuentas) cuando Lucho lo pida.
