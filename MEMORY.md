# MEMORY.md — Vértice · VerticeLABS (sitio web)

> Última actualización: 2026-09-14 · Sesión: rediseño "vende sola" + conexión DonWeb

## Qué es

Landing de venta de VerticeLABS (marca: **Vértice** · tagline "IA . AUTOMATIZACIÓN . SaaS").
Repositorio: `github.com/Lucianog13/portfolio`. Vista previa: https://lucianog13.github.io/portfolio/
Dominio de producción: **www.verticelabs.com.ar** (DonWeb, hosting compartido, panel Ferozo).

## Estructura (modular, Ley 1 del protocolo)

| Archivo | Controla |
|---|---|
| `index.html` | Estructura + contenido (todas las secciones, copy de venta, meta/SEO/OG/JSON-LD). Logo del hero: prisma hexagonal isométrico SVG (caras superior/laterales con gradiente) que oscila en 3D |
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
      SSL Let's Encrypt activo, .htaccess fuerza https+www (verificado 301→200).
      FTP operativo vía .env + deploy.py. Rebrand VerticeLABS + efectos premium
      desplegados y verificados (ticker/contadores/wordmark nuevo).
- [ ] Optimizar peso de imágenes (super.png 710 KB, vitrina.png 608 KB → uv + Pillow)
- [ ] Auditoría responsive (skill auditoria-responsive-web)
- [ ] Confirmar con Lucho: número de WhatsApp en CTAs, clientes visibles en público,
      apellidos en JSON-LD, qué hacer con el WordPress instalado en public_html

## Deploy a DonWeb (cómo se usa — FTP ACTIVO)

```bash
python deploy.py   # lee .env (gitignored): DONWEB_HOST/USER/PASS, sube por FTPS
```
- FTP verificadado 15-09-2026: host a0190762.ferozo.com, usuario ftp@a0190762.ferozo.com,
  contraseña en .env local (NO commitear). FTPS explícito puerto 21 (FTP_TLS + prot_p).
- Ojo: varios intentos fallidos de login → el servidor devuelve timeouts (bloqueo
  temporal). No insistir.
- Alternativa si FTP falla: panel Ferozo → Mi Sitio Web → Subir mi sitio (ZIP,
  lo arma hacer_zip.py). El login del panel solo pasa en navegador visible de
  Lucho (Turnstile); Chrome headless no sirve para eso.
- fer_shots.py captura screenshots por CDP (headless=new, que es lo único que
  bindea el puerto de debug desde Chrome 153).
- SSL: ya emitido por Let's Encrypt (*.verticelabs.com.ar). No tocar salvo renovación.
- En public_html quedó un WordPress preinstalado + sitio.zip viejo + archivos
  captura-*.png legacy. Nuestro index.html tiene prioridad (verificado).

## Cambios pendientes / notas

- El JSON-LD declara fundadores "Luciano González / Martín González / Tomás" — confirmar apellidos con Lucho.
- En public_html quedó un WordPress instalado (venía con el hosting) + archivos captura-*.png
  legacy. No rompen nada (nuestro index.html tiene prioridad), pero conviene borrarlos
  cuando Lucho confirme que no los necesita.
- Cuenta de correo existente: marcelogonzalez@verticelabs.com.ar. Falta crear info@
  (panel → Email → Cuentas) cuando Lucho lo pida.
