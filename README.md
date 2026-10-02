# AWS User Group Ecuador — sitio web

Sitio estático (HTML + CSS + JS, sin framework), mobile-first y optimizado para SEO. Reemplaza el sitio WordPress/Elementor de https://www.awsugecuador.com/.

## Diseño actual: v2 "Builder"

Inspirado en la línea gráfica de AWS Builder Center (builder.aws.com): fondo oscuro `#161D26`, morado `#AD5CFF`, rosa `#FF57E9`, títulos en Geist Mono con estilo de código, tags `# hashtag` y la Mitad del Mundo en pixel-art como pieza distintiva. La versión anterior (editorial clara) está en `_versiones/v1-editorial/` (no publicar).

## Logo y favicon

- Logo: `img/logo-awsugecuador*.png`, a partir de `portada-card.png` del sitio anterior, sin el fondo azul (transparente) y recortado sin márgenes sobrantes. Original en `originales-wordpress/portada-card.png`.
- Favicon: `favicon.ico` + `img/favicon-*.png`, a partir de `favicon.png` del sitio anterior, centrado. `apple-touch-icon` e `icon-192/512` llevan fondo oscuro.

## Cómo editar

Las páginas HTML se generan con `build.py` (textos, eventos, equipo, fotos, comunidades y datos estructurados están ahí).

1. Edita `build.py` (o `css/styles.css` / `js/main.js` para estilos y comportamiento).
2. Ejecuta `python3 build.py` para regenerar `index.html`, `eventos/`, `equipo/` y `404.html`.
3. Prueba en local: `python3 -m http.server 8080` y abre http://localhost:8080/

No edites los `.html` a mano: se sobrescriben en el siguiente build.

Íconos: el sitio usa **Font Awesome Free 6.7.2 auto-hospedado**. Usa las clases normales (`<i class="fa-brands fa-meetup" aria-hidden="true"></i>`); al ejecutar `build.py` se detectan los íconos usados y se recortan las fuentes de `tools/fontawesome/` a solo esos glifos (`fonts/fa-solid-<hash>.woff2`, `fonts/fa-brands-<hash>.woff2`, ~3 KB en total) con `font-display: swap`. Para recortar íconos nuevos hace falta `pip install fonttools brotli` (en un entorno virtual); sin eso el build usa las fuentes ya generadas.

Rendimiento: el CSS se incrusta minificado en cada página (sin solicitudes que bloqueen el render), la foto principal se sirve en AVIF con respaldo WebP y el logo en WebP con varios tamaños.

Para publicar, sube solo los archivos públicos (`index.html`, `404.html`, `eventos/`, `equipo/`, `css/`, `js/`, `img/`, `fonts/`, `favicon.ico`, `robots.txt`, `sitemap.xml`, `site.webmanifest`, `_redirects`, `_headers`), sin `originales-wordpress/`, `build.py` ni `README.md`.

## Estructura

```
index.html            Inicio (comunidad, Community Day, eventos, galería, equipo, sponsors, FAQ)
eventos/index.html    Eventos de AWS en Ecuador (con datos estructurados Event)
equipo/index.html     Líderes y voluntariado (con datos estructurados Person)
404.html              Página de error (noindex)
css/styles.css        Estilos (mobile-first, solo min-width)
js/main.js            Menú móvil, header, revelado de imágenes
fonts/                Geist + Geist Mono (alojadas localmente, woff2)
img/                  Imágenes WebP en varios tamaños, favicons, imagen OG 1200×630
robots.txt, sitemap.xml, site.webmanifest, favicon.ico
_redirects            301 desde las URLs viejas de WordPress (Cloudflare Pages / Netlify)
_headers              Cabeceras de seguridad y caché (Cloudflare Pages / Netlify)
originales-wordpress/ Fotos originales en alta resolución (fuente de las versiones WebP). NO publicar.
build.py              Generador de las páginas HTML
tools/fontawesome/    Fuentes completas de Font Awesome Free (fuente para el recorte). NO publicar.
```

## SEO incluido

- Title y meta description únicos por página, canonical, hreflang es-EC, Open Graph y Twitter Card.
- JSON-LD: Organization, WebSite, WebPage, FAQPage (inicio); Event × 4 y BreadcrumbList (eventos); Person × 3, AboutPage y BreadcrumbList (equipo).
- Un solo H1 por página, jerarquía de encabezados semántica, alt descriptivo en todas las imágenes.
- Sitemap con imágenes, robots.txt, verificación de Google Search Console conservada.
- Rendimiento: fuentes locales con preload, imagen LCP con preload + fetchpriority, WebP con srcset/sizes, lazy-load bajo el pliegue, Font Awesome cargado sin bloquear el render.
- Redirecciones 301 de `/teams/`, `/blog/`, posts y páginas basura de WordPress (`/sample-page/`, `/prueba/`, `/elementor-*`…) para no perder posicionamiento ni dejar 404.

## Fotos

- Hero: `img/community-day-2024-*.webp` (foto enviada por Alexis, 20241005_172148.jpg, 3,8 MB → 45–480 KB en WebP). Original en `originales-wordpress/`.
- Momentos: 22 fotos en `img/momentos/`, tomadas de los álbumes públicos de Flickr (https://www.flickr.com/photos/203738323@N04/albums/). Facebook e Instagram no permiten descargar sin sesión; si quieres fotos de ahí, ponlas en una carpeta y se integran.
- No se usa base64 para imágenes: aumenta el peso ~33 % y no se puede cachear ni servir por tamaño de pantalla.

## Datos confirmados (2 oct 2026)

- Fundada el 10 de febrero de 2022 por Alexis Polo (líder fundador). Primera comunidad de AWS del Ecuador. 5 años el 10/02/2027.
- Community Day: 2.ª ed. ESPOL Guayaquil (05/10/2024), 3.ª ed. UDLA Quito (25/10/2025), 4.ª ed. UPS Cuenca (05/09/2026).
- Ciudades: Quito, Guayaquil, Cuenca + online.

## Qué confirmar antes de publicar

- [ ] **Miembros en Meetup**: se muestra "+1.400" (Meetup indicaba 1.455 el 2 de octubre de 2026). Actualizar cuando cambie.
- [ ] **Redes de Vanessa Barreiro**: el sitio anterior no tenía sus enlaces; agregar LinkedIn si lo desea.
- [ ] **Sponsors**: GYE Tech, Ondú Cloud y Publifyer. ¿Siguen vigentes? ¿Se enlazan a sus sitios web?
- [ ] **FAQ**: no se afirma que los eventos sean gratuitos. Si lo son, conviene agregar esa pregunta (ayuda en búsquedas).
- [ ] **Instagram / TikTok / X de la comunidad**: no se encontraron cuentas oficiales; agregar si existen.
- [ ] **Aniversario**: cuando haya lugar y hora, actualizar la sección y crear el evento en Meetup.
- [ ] **Dominio**: el canonical usa `https://www.awsugecuador.com/`. Configurar la redirección del dominio sin www a www en el hosting.

## Después de publicar

1. En Google Search Console: enviar `https://www.awsugecuador.com/sitemap.xml` y pedir indexación de las 3 URLs.
2. Validar los datos estructurados en https://search.google.com/test/rich-results.
3. Medir con PageSpeed Insights (móvil).
4. Mantener `/eventos/` actualizado tras cada meetup: el contenido nuevo y frecuente es lo que más ayuda a posicionar.

## Créditos

Iconos: Font Awesome Free 6.7.2 (íconos CC BY 4.0, fuentes SIL OFL 1.1). Fuentes: Geist y Geist Mono (SIL Open Font License).
