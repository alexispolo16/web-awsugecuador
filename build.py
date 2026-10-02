"""Genera index.html, eventos/, equipo/ y 404.html del sitio de AWS User Group Ecuador.

Uso: python3 build.py
"""
import re, json, os, glob, hashlib
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.awsugecuador.com'
home_ld = r'''{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.awsugecuador.com/#organization",
      "name": "AWS User Group Ecuador",
      "alternateName": [
        "AWS UG Ecuador",
        "AWS Ecuador",
        "Comunidad AWS Ecuador"
      ],
      "url": "https://www.awsugecuador.com/",
      "logo": "https://www.awsugecuador.com/img/icon-512.png",
      "image": "https://www.awsugecuador.com/img/og-awsugecuador.jpg",
      "description": "Comunidad de usuarios de Amazon Web Services (AWS) en Ecuador. Organiza meetups, talleres, retos de certificación y el AWS Community Day Ecuador.",
      "email": "hello@awsugecuador.com",
      "foundingDate": "2021-10-22",
      "areaServed": {
        "@type": "Country",
        "name": "Ecuador"
      },
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Guayaquil",
        "addressCountry": "EC"
      },
      "knowsAbout": [
        "Amazon Web Services",
        "Computación en la nube",
        "Certificaciones AWS",
        "Arquitectura en la nube",
        "Inteligencia artificial generativa",
        "Amazon Bedrock"
      ],
      "founder": {
        "@id": "https://www.awsugecuador.com/equipo/#alexis-polo"
      },
      "sameAs": [
        "https://www.meetup.com/aws-ecuador/",
        "https://www.linkedin.com/company/awsecuador",
        "https://www.facebook.com/ecuadoraws",
        "https://www.youtube.com/channel/UCgzEFlDd-KR0BL5rlOVY7KQ",
        "https://discord.gg/aUR9RNgm5j"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.awsugecuador.com/#website",
      "url": "https://www.awsugecuador.com/",
      "name": "AWS User Group Ecuador",
      "inLanguage": "es-EC",
      "publisher": {
        "@id": "https://www.awsugecuador.com/#organization"
      }
    },
    {
      "@type": "WebPage",
      "@id": "https://www.awsugecuador.com/#webpage",
      "url": "https://www.awsugecuador.com/",
      "name": "AWS User Group Ecuador | Comunidad de AWS en Ecuador",
      "isPartOf": {
        "@id": "https://www.awsugecuador.com/#website"
      },
      "about": {
        "@id": "https://www.awsugecuador.com/#organization"
      },
      "primaryImageOfPage": "https://www.awsugecuador.com/img/comunidad-auditorio-1600.webp",
      "inLanguage": "es-EC"
    },
    {
      "@type": "FAQPage",
      "@id": "https://www.awsugecuador.com/#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "¿Qué es AWS User Group Ecuador?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Es la comunidad de usuarios de Amazon Web Services en Ecuador. Reúne a desarrolladores, arquitectos, estudiantes y líderes de tecnología para aprender y compartir conocimiento sobre la nube de AWS en meetups, talleres y el AWS Community Day Ecuador. Es una comunidad independiente, organizada por voluntarios."
          }
        },
        {
          "@type": "Question",
          "name": "¿Necesito experiencia en AWS para unirme?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "No. La comunidad está abierta a quien da sus primeros pasos en la nube y a quien ya trabaja con AWS a diario. Cada evento indica su nivel para que elijas el que te sirve."
          }
        },
        {
          "@type": "Question",
          "name": "¿Dónde se realizan los eventos de AWS en Ecuador?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hacemos eventos presenciales en Guayaquil y Cuenca, y sesiones online abiertas a todo el país. Todos los eventos se publican en el grupo de Meetup de AWS User Group Ecuador."
          }
        },
        {
          "@type": "Question",
          "name": "¿La comunidad ayuda a obtener una certificación de AWS?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Sí. Organizamos retos y sesiones de estudio pensados para preparar las certificaciones de AWS, y puedes resolver dudas con personas que ya se certificaron."
          }
        },
        {
          "@type": "Question",
          "name": "¿Cómo puedo dar una charla en un meetup?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Escríbenos a hello@awsugecuador.com con el tema, un resumen corto y tu nivel de experiencia. Buscamos charlas de todos los niveles, especialmente casos reales construidos en AWS."
          }
        },
        {
          "@type": "Question",
          "name": "¿Cómo puede mi empresa patrocinar a la comunidad?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Escríbenos a hello@awsugecuador.com. Las empresas pueden apoyar con espacio para eventos, logística o patrocinio del AWS Community Day Ecuador."
          }
        }
      ]
    }
  ]
}'''

# ---------- pixel art ----------
def pixel_svg():
    P='#BF80FF'; P2='#AD5CFF'; D='#161D26'; K='#FF57E9'; O='#FF9900'; C='#3AB0FF'; G='#2BD47D'; W='#F9F9FA'
    px = {}
    def r(x0, x1, y, c):
        for x in range(x0, x1+1): px[(x, y)] = c
    for x in range(24): px[(x, 14)] = K
    r(11,12,2,P); r(10,13,3,P); r(10,13,4,K); r(10,13,5,P); r(11,12,6,P)
    for y in range(7,11): r(10,13,y,P2)
    for y in range(11,17): r(9,14,y,P2)
    for y in range(17,20): r(8,15,y,P2)
    for y in (9,12,15): r(11,12,y,D)
    r(5,18,20,P); r(4,19,21,P)
    main = ''.join(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{c}"/>' for (x,y),c in sorted(px.items(), key=lambda k:(k[0][1],k[0][0])))
    def plus(x,y,c): return ''.join(f'<rect x="{x+dx}" y="{y+dy}" width="1" height="1" fill="{c}"/>' for dx,dy in [(0,0),(1,0),(-1,0),(0,1),(0,-1)])
    sparks = [plus(3,4,O), plus(20,3,C), plus(20,18,G), plus(3,18,K)]
    dots = [(6,9,W),(17,8,O),(22,11,W),(1,11,C),(16,23,W),(7,23,G)]
    g = ''.join(f'<g class="spark s{i+1}">{s}</g>' for i,s in enumerate(sparks))
    g += '<g class="spark s2">' + ''.join(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{c}"/>' for x,y,c in dots[:3]) + '</g>'
    g += '<g class="spark s4">' + ''.join(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{c}"/>' for x,y,c in dots[3:]) + '</g>'
    return f'<svg class="pixel" viewBox="0 0 24 24" shape-rendering="crispEdges" role="img" aria-label="Ilustración pixel-art del monumento a la Mitad del Mundo atravesado por la línea ecuatorial">{main}{g}</svg>'

def pixel_five():
    rows=['11111','10000','11110','00001','00001','10001','01110']
    cells=''.join(f'<rect x="{x}" y="{y}" width="1" height="1"/>' for y,r in enumerate(rows) for x,c in enumerate(r) if c=='1')
    return f'<svg class="five" viewBox="0 0 5 7" shape-rendering="crispEdges" aria-hidden="true"><g fill="currentColor">{cells}</g></svg>'

MARK = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="mark" viewBox="0 0 48 48">
    <rect width="48" height="48" rx="8" fill="#AD5CFF"/>
    <g fill="#12091F"><rect x="21" y="8" width="6" height="6"/><rect x="21" y="16" width="6" height="6"/><rect x="18" y="22" width="12" height="10"/><rect x="12" y="34" width="24" height="4"/></g>
    <rect x="4" y="26" width="40" height="2" fill="#FF57E9"/>
  </symbol>
</svg>'''

FA = ''

def _min_css(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{};:,>])\s*', r'\1', css)
    return css.replace(';}', '}').replace('url(../', 'url(/').strip()
CSS = _min_css(open('css/styles.css', encoding='utf-8').read())

MEETUP = 'https://www.meetup.com/aws-ecuador/'

def header(current):
    items = [('/#comunidad','Nosotros'),('/eventos/','Eventos'),('/equipo/','Equipo'),('/#sponsors','Sponsors'),('/#preguntas','Preguntas')]
    lis = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==current else ""}>{t}</a></li>' for h,t in items)
    return f'''<a class="announce" href="/#aniversario"><span class="dot" aria-hidden="true"></span>Cumplimos 5 años el 10 de febrero de 2027<span class="go">celebra con nosotros <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span></a>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="/" aria-label="AWS User Group Ecuador, inicio">
      <img src="/img/logo-awsugecuador-320.webp" srcset="/img/logo-awsugecuador-160.webp 160w, /img/logo-awsugecuador-240.webp 240w, /img/logo-awsugecuador-320.webp 320w, /img/logo-awsugecuador-480.webp 480w" sizes="(min-width: 1024px) 157px, 138px" width="157" height="50" alt="AWS User Group Ecuador">
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="label">Menú</span><span class="bars" aria-hidden="true"></span></button>
    <nav class="site-nav" id="site-nav" aria-label="Principal">
      <ul>{lis}</ul>
      <a class="btn btn-purple" href="{MEETUP}" rel="noopener" target="_blank"><i class="fa-brands fa-meetup" aria-hidden="true"></i>Únete en Meetup</a>
    </nav>
  </div>
</header>'''

FOOTER = f'''<footer class="site-footer" id="unete">
  <div class="wrap">
    <div class="join-card">
      <div class="join-copy">
        <p class="prompt" aria-hidden="true"><span class="kw">await</span> comunidad.<span class="fn">join</span>(<span class="str">"tú"</span>)</p>
        <h2>Únete a la comunidad de AWS en Ecuador<span class="cursor" aria-hidden="true"></span></h2>
        <p class="join-lede">Entérate de cada meetup, taller y Community Day, y conoce a quienes construyen en la nube en el país.</p>
      </div>
      <div class="join-actions">
        <a class="btn" href="{MEETUP}" rel="noopener" target="_blank"><i class="fa-brands fa-meetup" aria-hidden="true"></i>Únete en Meetup</a>
        <a class="btn btn-dark" href="https://chat.whatsapp.com/CSTI8bsZY607nvg9o9U7fC?mode=gi_t" rel="noopener" target="_blank"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i>Únete al WhatsApp</a>
      </div>
    </div>

    <div class="footer-grid">
      <div class="footer-brand">
        <a href="/" aria-label="AWS User Group Ecuador, inicio"><img src="/img/logo-awsugecuador-480.webp" srcset="/img/logo-awsugecuador-240.webp 240w, /img/logo-awsugecuador-320.webp 320w, /img/logo-awsugecuador-480.webp 480w, /img/logo-awsugecuador-640.webp 640w" sizes="213px" width="213" height="68" loading="lazy" decoding="async" alt="AWS User Group Ecuador"></a>
        <p>Comunidad de usuarios de Amazon Web Services en Ecuador. La primera comunidad de AWS del Ecuador. Meetups, talleres y AWS Community Day en Quito, Guayaquil, Cuenca y online.</p>
        <ul class="social" aria-label="Redes sociales">
          <li><a class="icon-btn" href="https://www.linkedin.com/company/awsecuador" rel="noopener" target="_blank" aria-label="LinkedIn de AWS User Group Ecuador"><i class="fa-brands fa-linkedin-in" aria-hidden="true"></i></a></li>
          <li><a class="icon-btn" href="https://chat.whatsapp.com/CSTI8bsZY607nvg9o9U7fC?mode=gi_t" rel="noopener" target="_blank" aria-label="Grupo de WhatsApp de AWS User Group Ecuador"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i></a></li>
          <li><a class="icon-btn" href="https://www.youtube.com/@awsugecuador4610" rel="noopener" target="_blank" aria-label="YouTube de AWS User Group Ecuador"><i class="fa-brands fa-youtube" aria-hidden="true"></i></a></li>
          <li><a class="icon-btn" href="https://www.facebook.com/ecuadoraws" rel="noopener" target="_blank" aria-label="Facebook de AWS User Group Ecuador"><i class="fa-brands fa-facebook-f" aria-hidden="true"></i></a></li>
          <li><a class="icon-btn" href="https://www.tiktok.com/@awsecuador" rel="noopener" target="_blank" aria-label="TikTok de AWS User Group Ecuador"><i class="fa-brands fa-tiktok" aria-hidden="true"></i></a></li>
          <li><a class="icon-btn" href="https://www.instagram.com/ecuadoraws" rel="noopener" target="_blank" aria-label="Instagram de AWS User Group Ecuador"><i class="fa-brands fa-instagram" aria-hidden="true"></i></a></li>
          <li><a class="icon-btn" href="{MEETUP}" rel="noopener" target="_blank" aria-label="Meetup de AWS User Group Ecuador"><i class="fa-brands fa-meetup" aria-hidden="true"></i></a></li>
        </ul>
      </div>
      <nav class="footer-col" aria-labelledby="f-explora">
        <h2 id="f-explora">explora</h2>
        <ul>
          <li><a href="/">Inicio</a></li>
          <li><a href="/eventos/">Eventos</a></li>
          <li><a href="/equipo/">Equipo</a></li>
          <li><a href="/#community-day">AWS Community Day</a></li>
          <li><a href="/#momentos">Fotos y momentos</a></li>
          <li><a href="/#preguntas">Preguntas frecuentes</a></li>
        </ul>
      </nav>
      <nav class="footer-col" aria-labelledby="f-participa">
        <h2 id="f-participa">participa</h2>
        <ul>
          <li><a href="mailto:hello@awsugecuador.com?subject=Propuesta%20de%20charla">Proponer una charla</a></li>
          <li><a href="mailto:hello@awsugecuador.com?subject=Quiero%20ser%20voluntario">Ser voluntario</a></li>
          <li><a href="mailto:hello@awsugecuador.com?subject=Quiero%20ser%20sponsor%20de%20AWS%20User%20Group%20Ecuador">Ser sponsor</a></li>
          <li><a href="https://www.meetup.com/aws-ecuador/events/" rel="noopener" target="_blank">Próximos eventos</a></li>
        </ul>
      </nav>
      <div class="footer-col">
        <h2>contacto</h2>
        <ul>
          <li><a class="mail" href="mailto:hello@awsugecuador.com"><i class="fa-solid fa-envelope" aria-hidden="true"></i>hello@awsugecuador.com</a></li>
          <li><span class="plain"><i class="fa-solid fa-location-dot" aria-hidden="true"></i>Guayaquil, Ecuador</span></li>
        </ul>
      </div>
    </div>

    <div class="equator-bar" aria-hidden="true"><span>lat 0°00′00″</span><span>ecuador</span></div>
    <div class="footer-meta">
      <p>© <span data-year>2026</span> AWS User Group Ecuador · Hecho por la comunidad, en la mitad del mundo.</p>
      <p class="legal">Comunidad independiente organizada por voluntarios. Amazon Web Services, AWS y sus logotipos son marcas de Amazon.com, Inc. o sus filiales.</p>
    </div>
  </div>
</footer>'''

def _page(path, title, desc, ld, body, current, extra_head='', robots='index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1', canonical=True):
    url = SITE + path
    can = f'<link rel="canonical" href="{url}">\n<link rel="alternate" hreflang="es-EC" href="{url}">\n<link rel="alternate" hreflang="x-default" href="{url}">\n' if canonical else ''
    gsv = '<meta name="google-site-verification" content="0D5puLMknlgB2XljSiQkHi3rrwnQsV2sdyIEpAfnCNg">\n' if path == '/' else ''
    return f'''<!doctype html>
<html lang="es-EC">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="AWS User Group Ecuador, comunidad AWS Ecuador, AWS re:Invent Ecuador, AWS User Group Quito, AWS Women Ecuador, AWS Student Builder Group Ecuador, AWS Cloud Club Ecuador, primera comunidad de AWS en Ecuador, Alexis Polo, líder fundador AWS User Group Ecuador, Amazon Web Services Ecuador, AWS Community Day Ecuador, AWS Quito, AWS Guayaquil, AWS Cuenca, certificaciones AWS Ecuador, eventos de tecnología Ecuador, meetups cloud Ecuador, computación en la nube Ecuador">
<meta name="author" content="AWS User Group Ecuador · Alexis Polo">
{can}<meta name="robots" content="{robots}">
<meta name="theme-color" content="#161D26">
<meta name="color-scheme" content="dark">
{gsv}<meta property="og:type" content="website">
<meta property="og:locale" content="es_EC">
<meta property="og:site_name" content="AWS User Group Ecuador">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og-awsugecuador.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="La comunidad de AWS en Ecuador: AWS User Group Ecuador">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/img/og-awsugecuador.jpg">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/img/favicon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/fonts/geist-mono-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/fa-brands.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/fa-solid.woff2" as="font" type="font/woff2" crossorigin>{extra_head}
<style>{CSS}/*FA*/</style>
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<a class="skip" href="#contenido">Saltar al contenido</a>

{header(current)}

<main id="contenido">
{body}
</main>

{FOOTER}

<script src="/js/main.js" defer></script>
</body>
</html>
'''

def img(name, widths, w, h, alt, sizes, lazy=True, cls=''):
    srcset = ', '.join(f'/img/{name}-{x}.webp {x}w' for x in widths)
    mid = widths[1] if len(widths) > 1 else widths[0]
    load = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    return f'<img src="/img/{name}-{mid}.webp" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" {load} alt="{alt}"{cls}>'

def page(*a, **k):
    return _page(*a, **k)

# ---------- data ----------
EVENTS = [
  dict(d="2026-09-05T09:30:00-05:00", label="05 sep 2026", t="AWS Community Day Ecuador 2026", url="https://www.meetup.com/aws-ecuador/events/314902222/",
       place=("Universidad Politécnica Salesiana", "Cuenca"), img="community-day-ecuador-1600.webp", tags=["community-day","presencial"],
       desc="Jornada completa de charlas técnicas, talleres y networking sobre Amazon Web Services organizada por AWS User Group Ecuador."),
  dict(d="2026-07-26T12:00:00-05:00", label="26 jul 2026", t="Conoce y conversa con el ex creador del AWS Community Builders Program", url="https://www.meetup.com/aws-ecuador/events/315768925/",
       place=None, img="comunidad-auditorio-1600.webp", tags=["community-builders","carrera"],
       desc="Conversación online sobre el programa AWS Community Builders con quien lo creó."),
  dict(d="2026-06-03T20:00:00-05:00", label="03 jun 2026", t="Spec-Driven Development: software con IA y Amazon Bedrock", url="https://www.meetup.com/aws-ecuador/events/315064467/",
       place=None, img="comunidad-auditorio-1600.webp", tags=["amazon-bedrock","generative-ai"],
       desc="Sesión online sobre desarrollo guiado por especificaciones con inteligencia artificial generativa y Amazon Bedrock."),
  dict(d="2026-03-21T09:00:00-05:00", label="21 mar 2026", t="Inspirando futuras líderes extraordinarias", url="https://www.meetup.com/aws-ecuador/events/313531510/",
       place=("Universidad Católica de Santiago de Guayaquil", "Guayaquil"), img="comunidad-exterior-1600.webp", tags=["women-in-tech","presencial"],
       desc="Jornada de charlas, workshop y networking con destacadas speakers para inspirar y acompañar a mujeres en tecnología y en la nube."),
  dict(d="2026-02-07T09:00:00-05:00", label="07 feb 2026", t="AWS Security Day", url="https://www.flickr.com/photos/203738323@N04/albums/72177720331955045",
       place=("Universidad Politécnica Salesiana (UPS)", None), img="momentos/55089267957-1024.webp", tags=["security","+160 asistentes"],
       desc="Una jornada dedicada a la seguridad en la nube con más de 160 asistentes, charlas de expertos del sector y mucha comunidad."),
  dict(d="2025-10-25T09:00:00-05:00", label="25 oct 2025", t="AWS Community Day Ecuador 2025", url="https://www.flickr.com/photos/203738323@N04/albums/72177720329913935",
       place=("Universidad de las Américas (UDLA)", "Quito"), img="momentos/54882583284-1024.webp", tags=["community-day","3.ª edición"],
       desc="La tercera edición del AWS Community Day Ecuador en Quito: un encuentro para compartir conocimiento, experiencias e innovación en la nube."),
  dict(d="2024-10-05T09:00:00-05:00", label="05 oct 2024", t="AWS Community Day Ecuador 2024", url="https://www.meetup.com/aws-ecuador/events/",
       place=("Escuela Superior Politécnica del Litoral (ESPOL)", "Guayaquil"), img="community-day-2024-1600.webp", tags=["community-day","2.ª edición"],
       desc="La segunda edición del AWS Community Day Ecuador reunió a la comunidad en la ESPOL, en Guayaquil, con charlas, talleres y una foto grupal histórica."),
]

def event_items(with_desc, limit=None):
    out = ''
    for e in EVENTS[:limit]:
        where = (f'<span class="where"><i class="fa-solid fa-location-dot" aria-hidden="true"></i>{e["place"][1] or e["place"][0]}</span>' if e['place'] else '<span class="where"><i class="fa-solid fa-globe" aria-hidden="true"></i>Online</span>')
        tags = ''.join(f'<span class="tag"># {t}</span>' for t in e['tags'])
        desc = f'\n            <p>{e["desc"]}</p>' if with_desc else ''
        out += f'''
          <li class="event">
            <div class="top"><time datetime="{e['d'][:10]}">{e['label']}</time>{where}</div>
            <h3><a href="{e['url']}" rel="noopener" target="_blank">{e['t']}</a></h3>{desc}
            <div class="tags">{tags}</div>
          </li>'''
    return out

PEOPLE = [
  dict(id="alexis-polo", n="Alexis Polo", r="Líder fundador", extra="User Group Leader", img="alexis-polo", h=768,
       links=[("https://www.linkedin.com/in/alexispolo","fa-brands fa-linkedin-in","LinkedIn"),("https://www.instagram.com/aledpolo/","fa-brands fa-instagram","Instagram"),("https://www.alexispolo.com","fa-solid fa-globe","Sitio web")]),
  dict(id="vanessa-barreiro", n="Vanessa Barreiro", r="User Group Leader", extra=None, img="vanessa-barreiro", h=768, links=[]),
  dict(id="paul-rizo", n="Paul Rizo", r="User Group Leader", extra=None, img="paul-rizo", h=765,
       links=[("https://www.linkedin.com/in/paul-rizo","fa-brands fa-linkedin-in","LinkedIn"),("https://www.instagram.com/paull_rl/","fa-brands fa-instagram","Instagram")]),
]
def team_items(home):
    out = ''
    for i, p in enumerate(PEOPLE):
        links = p['links'] if not home else [l for l in p['links'] if 'globe' not in l[1]]
        soc = ''.join(f'<a class="icon-btn" href="{u}" rel="noopener" target="_blank" aria-label="{lab} de {p["n"]}"><i class="{ic}" aria-hidden="true"></i></a>' for u, ic, lab in links)
        badges = f'<span class="badge p">{p["r"]}</span>' + (f'<span class="badge">{p["extra"]}</span>' if p['extra'] else '')
        im = img(p['img'], [400, 768], 768, p['h'], f'Retrato de {p["n"]}', '(min-width: 768px) 30vw, 112px')
        out += f'''
        <li class="member{' lead' if i == 0 else ''}" id="{p['id']}">
          <figure>{im}</figure>
          <h3>{p['n']}</h3>
          <div class="badges">{badges}</div>
          {f'<div class="social">{soc}</div>' if soc else ''}
        </li>'''
    return out

MOMENTS = [
  ("54882583284","community-day","Cientos de asistentes del AWS Community Day Ecuador 2025 posan en las escaleras de la Universidad de las Américas en Quito","Community Day 2025",1024,683),
  ("54890831244","community-day","Alexis Polo, líder fundador de AWS User Group Ecuador, habla con el público en el AWS Community Day Ecuador 2025","Community Day 2025",1024,683),
  ("55516366381","community-day","Auditorio lleno durante la apertura del AWS Community Day Ecuador 2026 en Cuenca","Community Day 2026",1024,683),
  ("55090151586","security","Alexis Polo, fundador de AWS User Group Ecuador, da la bienvenida desde el podio del AWS Security Day","Security Day",1024,1024),
  ("reinvent-hero","reinvent","Alexis Polo, líder fundador de AWS User Group Ecuador, con un AWS Hero en AWS re:Invent","AWS re:Invent",1024,768),
  ("reinvent-expo","reinvent","Expo hall de AWS re:Invent con el gran letrero de AWS iluminado","AWS re:Invent",1024,1365),
  ("reinvent","reinvent","Réplica del monumento a la Mitad del Mundo de AWS Community Day Ecuador en Las Vegas durante AWS re:Invent","AWS re:Invent",1024,1024),
  ("reinvent-4","reinvent","Integrante de AWS User Group Ecuador sonríe con la réplica del monumento de AWS Community Day Ecuador en AWS re:Invent","AWS re:Invent",960,1200),
  ("reinvent-2","reinvent","Logo gigante de AWS iluminado en morado en el hall de AWS re:Invent en Las Vegas","AWS re:Invent",960,1200),
  ("reinvent-5","reinvent","Integrante de AWS User Group Ecuador posa con la réplica del monumento de AWS Community Day Ecuador en Las Vegas","AWS re:Invent",960,1200),
  ("reinvent-6","reinvent","Letrero de entrada a AWS re:Invent con luces de colores en Las Vegas","AWS re:Invent",898,672),
  ("reinvent-3","reinvent","Pantalla de AWS re:Invent en la zona de registro de badges, con asistentes haciendo fila","AWS re:Invent",960,1200),
  ("55163781546","mujeres","Foto grupal de Inspirando futuras líderes extraordinarias, el encuentro de mujeres en tecnología","Mujeres en tecnología",1024,768),
  ("54890810233","community-day","Alexis Polo entrega un premio a un asistente en el escenario del AWS Community Day Ecuador 2025","Community Day 2025",1024,683),
  ("hackathon","otros","Alexis Polo, líder de AWS User Group Ecuador, habla con los participantes de un hackathon","Hackathon",1024,683),
  ("55089267957","security","Asistentes del AWS Security Day posan en el auditorio de la UPS","Security Day",1024,683),
  ("54882580144","community-day","Alexis Polo, fundador de AWS User Group Ecuador, posa con un asistente en el AWS Community Day Ecuador 2025","Community Day 2025",1024,923),
  ("55089267912","security","Alexis Polo junto a speakers en una selfie del AWS Security Day","Security Day",1024,768),
  ("55516701379","community-day","Un speaker da su charla en el AWS Community Day Ecuador 2026","Community Day 2026",682,1024),
  ("cd-salto","community-day","Alexis Polo celebra con los asistentes frente al letrero de AWS Community Day Ecuador","Community Day",1024,576),
  ("54882338156","community-day","Asistentes se toman una selfie en el auditorio del AWS Community Day Ecuador 2025","Community Day 2025",1024,683),
  ("55162884362","mujeres","Una speaker comparte su experiencia en el encuentro de mujeres en tecnología","Mujeres en tecnología",1023,682),
  ("54882557068","community-day","Alexis Polo presenta a los speakers en el escenario del AWS Community Day Ecuador 2025","Community Day 2025",1024,740),
  ("55090417689","security","Foto grupal al aire libre de los asistentes del AWS Security Day","Security Day",1024,683),
  ("55516473143","community-day","El equipo de registro recibe a los participantes del AWS Community Day Ecuador 2026","Community Day 2026",1024,683),
  ("55090514405","security","La mascota de AWS sobre el podio del AWS Security Day","Security Day",746,1024),
  ("55162884322","mujeres","Speakers y organizadoras del encuentro de mujeres en tecnología","Mujeres en tecnología",1024,768),
  ("54890877840","community-day","Vista del auditorio lleno durante una charla del AWS Community Day Ecuador 2025","Community Day 2025",1024,683),
  ("55516648983","community-day","Un grupo de estudiantes posa en el photocall del AWS Community Day Ecuador 2026","Community Day 2026",1024,682),
  ("55090356113","security","Mesa de stickers y regalos para la comunidad en el AWS Security Day","Security Day",1024,682),
  ("54882579944","community-day","Un speaker presenta sobre agentes de IA en el AWS Community Day Ecuador 2025","Community Day 2025",1023,938),
  ("55515418927","community-day","Tres asistentes posan en el photocall del AWS Community Day Ecuador 2026","Community Day 2026",1024,682),
]
ALBUMS = [
  ("AWS Community Day 2026","Cuenca · 4.ª edición","460 fotos","https://www.flickr.com/photos/203738323@N04/albums/72177720335540214","55516366381"),
  ("AWS Community Day 2025","UDLA, Quito · 3.ª edición","153 fotos","https://www.flickr.com/photos/203738323@N04/albums/72177720329913935","54882583284"),
  ("AWS Security Day","UPS · +160 asistentes","36 fotos","https://www.flickr.com/photos/203738323@N04/albums/72177720331955045","55089267957"),
  ("Mujeres en tecnología","Inspirando futuras líderes","33 fotos","https://www.flickr.com/photos/203738323@N04/albums/72177720332674177","55163781546"),
]
def moments_html():
    out=''
    for pid,cat,alt,cap,w,h in MOMENTS:
        out+=f'''
          <figure class="moment" data-cat="{cat}"><img src="/img/momentos/{pid}-480.webp" srcset="/img/momentos/{pid}-480.webp 480w, /img/momentos/{pid}-1024.webp 1024w" sizes="(min-width: 1024px) 25vw, (min-width: 768px) 33vw, 50vw" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{alt}"><figcaption>{cap}</figcaption></figure>'''
    return out
def albums_html():
    return ''.join(f'''
        <li class="album"><a href="{u}" rel="noopener" target="_blank">
          <img src="/img/momentos/{c}-480.webp" width="480" height="320" loading="lazy" decoding="async" alt="">
          <span class="a-body"><span class="a-count">{n}</span><strong>{t}</strong><span class="a-meta">{m}</span></span>
        </a></li>''' for t,m,n,u,c in ALBUMS)

COMMUNITIES = [
  dict(n="AWS User Group Quito", t="User Group", city="Quito", sub="Comunidad de AWS en Quito", lead="Hernán Villavicencio, Bolívar Llerena, Steven Aizaga y Edison Panchi",
       meetup="https://www.meetup.com/aws-user-group-quito/", ig="awsugquito", tt="awsugquito", yt="https://www.youtube.com/@awsugquito", li="https://www.linkedin.com/company/awsugquito/", wa="https://chat.whatsapp.com/CKVja1AhL9e0x47GSIsLQc", web="https://www.awsugquito.com/"),
  dict(n="AWS Women Ecuador", t="User Group", city="Nacional", sub="Mujeres en la nube en todo el Ecuador", lead="Erika Vacacela, Rafaela Parra y Mavelin Ati",
       meetup="https://www.meetup.com/aws-women-ecuador/", ig="awswomenecuador", fb="https://www.facebook.com/groups/awswomenecuador", tt="awswomenec", yt="https://www.youtube.com/@AWSWomenEcuador", li="https://www.linkedin.com/company/aws-women-ecuador", wa="https://chat.whatsapp.com/LXb1Gg9TgEY3Dx6q0mtPJn", web="https://linktr.ee/awswomenecuador"),
  dict(n="AWS User Group Security Ecuador", t="User Group", city="Nacional", sub="Seguridad en la nube de AWS", lead="Willie Reyes, Xavier Llauca y Anthony Grijalva",
       meetup="https://www.meetup.com/aws-user-group-security-ecuador/", ig="awssecurityecuador", li="https://www.linkedin.com/company/awssecurityecuador/", wa="https://chat.whatsapp.com/LXPdwIo42qjA33MhOMcsbp", web="https://www.awssecurityecuador.com/"),
  dict(n="AWS Student Builder Group at ESPOL", t="Student Builder Group", city="Guayaquil", sub="Escuela Superior Politécnica del Litoral", lead="Derek Guevara y Kevin Maldonado",
       meetup="https://www.meetup.com/aws-sbg-at-escuela-superior-politecnica-del-litoral-espol", ig="aws.sbg.espol", tt="aws_sbg_espol", yt="https://www.youtube.com/@aws_sbg_espol", li="https://www.linkedin.com/company/student-builder-group-at-espol", wa="https://chat.whatsapp.com/Ek8cwkm5bzTHfHSKfUXvAg", web="https://linktr.ee/aws.sbg.espol"),
  dict(n="AWS Student Builder Group at UG", t="Student Builder Group", city="Guayaquil", sub="Universidad de Guayaquil", lead="Paul Rizo y Magno Barco",
       meetup="https://www.meetup.com/aws-sbg-at-universidad-de-guayaquil", ig="aws_sbg_ug", tt="aws_sbg_ug", li="https://www.linkedin.com/company/aws-sbg-at-universidad-de-guayaquil/", wa="https://chat.whatsapp.com/JcP04n8PYVkJtsconrsy0e", web="https://linktr.ee/awscloudclubgye"),
  dict(n="AWS Student Builder Group at ITB", t="Student Builder Group", city="Guayaquil", sub="Instituto Superior Universitario Bolivariano", lead="Marko Antonio Rojas Lozado",
       meetup="https://www.meetup.com/aws-sbg-at-instituto-superior-universitario-bolivariano/", ig="aws.itb", fb="https://www.facebook.com/profile.php?id=61590435900354", tt="aws_itb", yt="https://www.youtube.com/@aws-itb", li="https://www.linkedin.com/company/aws-student-builder-group-itb/", wa="https://chat.whatsapp.com/GDrxU8QQVdaEAhvET1fnwt", web="https://warkos27.github.io/awws-builders-itb/"),
  dict(n="AWS Student Builder Group at PUCE", t="Student Builder Group", city="Quito", sub="Pontificia Universidad Católica del Ecuador", lead="Jeyson Mueses",
       meetup="https://www.meetup.com/aws-sbg-at-pontifical-cath-univ-of-ecuador-quito-campus", ig="aws_puce", tt="aws_puce_", yt="https://www.youtube.com/@aws_puce", li="https://www.linkedin.com/company/awspuce/", wa="https://chat.whatsapp.com/JYSTxfAyMeYKGYeSHjbEqC", web="https://awspuce.com"),
  dict(n="AWS Student Builder Group at UDLA", t="Student Builder Group", city="Quito", sub="Universidad de las Américas, campus UDLA Park", lead="Michelle Reyes",
       meetup="https://www.meetup.com/aws-sbg-at-univ-of-the-americas-udla-park-campus"),
  dict(n="AWS Student Builder Group at UIDE", t="Student Builder Group", city="Quito", sub="Universidad Internacional del Ecuador", lead="Oscar Lara",
       meetup="https://www.meetup.com/aws-sbg-at-international-university-of-ecuador", ig="aws_sbg_uide", wa="https://chat.whatsapp.com/IBITRvbUiQZLWrEmJNlRgz"),
  dict(n="AWS Student Builder Group at UCuenca", t="Student Builder Group", city="Cuenca", sub="Universidad de Cuenca", lead="Nicolás Ambrosi",
       meetup="https://www.meetup.com/aws-cloud-club-at-universidad-de-cuenca/", ig="aws.ucuenca", tt="aws.ucuenca", li="https://www.linkedin.com/company/aws-student-builder-group-universidad-de-cuenca/", wa="https://chat.whatsapp.com/LqqNGmzy0Ti4seISeiV4Bi", web="https://linktr.ee/awsclub.ucuenca"),
  dict(n="AWS Student Builder Group at ULEAM", t="Student Builder Group", city="Manta", sub="Universidad Laica Eloy Alfaro de Manabí", lead="Miquel Muñiz, Cristopher Castro y Luis Figueroa",
       meetup="https://www.meetup.com/aws-sbg-at-universidad-laica-eloy-alfaro-de-manabi", ig="awssbglmanta", li="https://www.linkedin.com/in/aws-student-manta-620b65410/", wa="https://chat.whatsapp.com/CIRaJNPBoajLwlT60AzHYG", web="https://linktr.ee/awsmanta"),
]
def comm_links(c):
    L=[]
    if c.get('ig'): L.append((f"https://www.instagram.com/{c['ig']}/","fa-brands fa-instagram","Instagram"))
    if c.get('tt'): L.append((f"https://www.tiktok.com/@{c['tt']}","fa-brands fa-tiktok","TikTok"))
    if c.get('fb'): L.append((c['fb'],"fa-brands fa-facebook-f","Facebook"))
    if c.get('yt'): L.append((c['yt'],"fa-brands fa-youtube","YouTube"))
    if c.get('li'): L.append((c['li'],"fa-brands fa-linkedin-in","LinkedIn"))
    if c.get('wa'): L.append((c['wa'],"fa-brands fa-whatsapp","Grupo de WhatsApp"))
    if c.get('web'): L.append((c['web'],"fa-solid fa-globe","Sitio web"))
    return L
def communities_html():
    out=''
    for c in COMMUNITIES:
        t='User Group' if c['t']=='User Group' else 'Student Builder Group'
        out+=f'''
        <li><a href="{c['meetup']}" rel="noopener" target="_blank"><span class="cl-name">{c['n']}</span><span class="cl-meta">{t} · {c['city']}</span><i class="fa-brands fa-meetup" aria-hidden="true"></i><span class="sr-only">(Meetup)</span></a></li>'''
    return out
def communities_ld():
    items=[]
    for i,c in enumerate(COMMUNITIES,1):
        items.append({"@type":"ListItem","position":i,"item":{"@type":"Organization","name":c['n'],"url":c['meetup'],"areaServed":"Ecuador" if c['city']=='Nacional' else c['city']}})
    return {"@type":"ItemList","@id":SITE+"/#comunidades","name":"Comunidades de AWS en Ecuador: User Groups y Student Builder Groups","itemListElement":items}

FAQ = [
 ("¿Qué es AWS User Group Ecuador?", "Es la primera comunidad de usuarios de Amazon Web Services (AWS) en Ecuador. Reúne a desarrolladores, arquitectos, estudiantes y líderes de tecnología para aprender y compartir conocimiento sobre la nube de AWS en meetups, talleres y el AWS Community Day Ecuador. Es una comunidad independiente, organizada por voluntarios.", None),
 ("¿Quién fundó AWS User Group Ecuador?", "AWS User Group Ecuador fue fundado el 10 de febrero de 2022 por Alexis Polo, su líder fundador. Hoy lo lidera junto a Vanessa Barreiro y Paul Rizo y un equipo de voluntarios.",
  'AWS User Group Ecuador fue fundado el 10 de febrero de 2022 por <a href="/equipo/#alexis-polo">Alexis Polo</a>, su líder fundador. Hoy lo lidera junto a Vanessa Barreiro y Paul Rizo y un equipo de voluntarios.'),
 ("¿Cuál es la primera comunidad de AWS en Ecuador?", "AWS User Group Ecuador es la primera comunidad de AWS del Ecuador. Desde 2022 organiza meetups, talleres, retos de certificación y el AWS Community Day Ecuador, y en febrero de 2027 cumple 5 años.", None),
 ("¿Necesito experiencia en AWS para unirme?", "No. La comunidad está abierta a quien da sus primeros pasos en la nube y a quien ya trabaja con AWS a diario. Cada evento indica su nivel para que elijas el que te sirve.", None),
 ("¿Hay comunidad de AWS en Quito, Guayaquil y Cuenca?", "Sí. AWS User Group Ecuador hace eventos presenciales en Quito, Guayaquil y Cuenca, y sesiones online abiertas a todo el país. Todos los eventos se publican en el grupo de Meetup de AWS User Group Ecuador.",
  'Sí. AWS User Group Ecuador hace eventos presenciales en Quito, Guayaquil y Cuenca, y sesiones online abiertas a todo el país. Todos los eventos se publican en el <a href="https://www.meetup.com/aws-ecuador/" rel="noopener" target="_blank">grupo de Meetup de AWS User Group Ecuador</a>.'),
 ("¿Qué comunidades de AWS hay en Ecuador?", "Además de AWS User Group Ecuador, existen AWS User Group Quito, AWS Women Ecuador, AWS User Group Security Ecuador y Student Builder Groups en universidades como ESPOL, Universidad de Guayaquil, ITB, PUCE, UDLA, UIDE, Universidad de Cuenca y ULEAM en Manta.",
  'Además de AWS User Group Ecuador, existen AWS User Group Quito, AWS Women Ecuador, AWS User Group Security Ecuador y Student Builder Groups en universidades como ESPOL, Universidad de Guayaquil, ITB, PUCE, UDLA, UIDE, Universidad de Cuenca y ULEAM en Manta. <a href="/#comunidades">Ver sus Meetups</a>.'),
 ("¿Cuándo es el AWS Community Day Ecuador?", "El AWS Community Day Ecuador se realiza una vez al año y cambia de ciudad: la 2.ª edición fue en la ESPOL de Guayaquil (2024), la 3.ª en la UDLA de Quito (2025) y la 4.ª en la Universidad Politécnica Salesiana de Cuenca (2026). La próxima edición se anuncia en Meetup.", None),
 ("¿La comunidad ayuda a obtener una certificación de AWS?", "Sí. Organizamos retos y sesiones de estudio pensados para preparar las certificaciones de AWS, y puedes resolver dudas con personas que ya se certificaron.", None),
 ("¿Cómo puedo dar una charla en un meetup?", "Escríbenos a hello@awsugecuador.com con el tema, un resumen corto y tu nivel de experiencia. Buscamos charlas de todos los niveles, especialmente casos reales construidos en AWS.",
  'Escríbenos a <a href="mailto:hello@awsugecuador.com">hello@awsugecuador.com</a> con el tema, un resumen corto y tu nivel de experiencia. Buscamos charlas de todos los niveles, especialmente casos reales construidos en AWS.'),
 ("¿Cómo puede mi empresa patrocinar a la comunidad?", "Escríbenos a hello@awsugecuador.com. Las empresas pueden apoyar con espacio para eventos, logística o patrocinio del AWS Community Day Ecuador.",
  'Escríbenos a <a href="mailto:hello@awsugecuador.com">hello@awsugecuador.com</a>. Las empresas pueden apoyar con espacio para eventos, logística o patrocinio del AWS Community Day Ecuador.'),
]
faq_html = ''.join(f'''
        <details>
          <summary>{q}</summary>
          <div class="answer"><p>{h or a}</p></div>
        </details>''' for q, a, h in FAQ)

# ---------- HOME ----------
ld = json.loads(home_ld)
for n in ld['@graph']:
    if n['@type'] == 'Organization':
        n['sameAs'] += ["https://www.instagram.com/ecuadoraws", "https://www.flickr.com/photos/203738323@N04/"]
        n['sameAs'] = [u.replace('https://www.youtube.com/channel/UCgzEFlDd-KR0BL5rlOVY7KQ','https://www.youtube.com/@awsugecuador4610') for u in n['sameAs'] if 'discord' not in u] + ["https://www.tiktok.com/@awsecuador"]
        n['foundingDate'] = '2022-02-10'
        n['alternateName'] = ["AWS UG Ecuador", "AWS Ecuador", "Comunidad AWS Ecuador", "AWS User Group Quito", "AWS User Group Guayaquil", "AWS User Group Cuenca"]
        n['slogan'] = 'La primera comunidad de AWS del Ecuador'
        n['description'] = 'AWS User Group Ecuador es la primera comunidad de usuarios de Amazon Web Services (AWS) en Ecuador, fundada el 10 de febrero de 2022 por Alexis Polo. Organiza meetups, talleres, retos de certificación AWS y el AWS Community Day Ecuador en Quito, Guayaquil y Cuenca.'
        n['areaServed'] = [{"@type": "Country", "name": "Ecuador"}, {"@type": "City", "name": "Quito"}, {"@type": "City", "name": "Guayaquil"}, {"@type": "City", "name": "Cuenca"}]
        n['founder'] = {"@type": "Person", "@id": SITE + "/equipo/#alexis-polo", "name": "Alexis Polo", "jobTitle": "Líder fundador de AWS User Group Ecuador", "url": "https://www.alexispolo.com", "sameAs": ["https://www.linkedin.com/in/alexispolo", "https://www.instagram.com/aledpolo/", "https://www.alexispolo.com"]}
        n['member'] = [{"@id": SITE + "/equipo/#alexis-polo"}, {"@id": SITE + "/equipo/#vanessa-barreiro"}, {"@id": SITE + "/equipo/#paul-rizo"}]
        n['knowsAbout'] += ["AWS Community Day", "Serverless", "Seguridad en la nube", "DevOps"]
    if n['@type'] == 'WebPage': n['primaryImageOfPage'] = SITE + '/img/community-day-2024-1600.webp'
    if n['@type'] == 'WebPage': n['name'] = 'AWS User Group Ecuador | Comunidad de AWS en Ecuador'
    if n['@type'] == 'FAQPage': n['mainEntity'] = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a,_ in FAQ]
ld['@graph'].append(communities_ld())
home_ld = json.dumps(ld, ensure_ascii=False, indent=2)

home_body = f'''
  <section class="hero" aria-labelledby="hero-title">
    <div class="wrap hero-grid">
      <div>
        <p class="prompt" aria-hidden="true"><span class="kw">if</span> building: <span class="fn">start_here</span>(<span class="str">"ecuador"</span>)</p>
        <h1 id="hero-title">La comunidad de <span class="hl">AWS</span> en Ecuador<span class="cursor" aria-hidden="true"></span></h1>
        <p class="hero-lede"><strong>Somos AWS User Group Ecuador, la primera comunidad de AWS del país.</strong> Aquí aprendes Amazon Web Services junto a quienes construyen en la nube todos los días: meetups, talleres, retos de certificación y el AWS Community Day, en Quito, Guayaquil, Cuenca y online.</p>
        <div class="hero-actions">
          <a class="btn" href="{MEETUP}" rel="noopener" target="_blank"><i class="fa-brands fa-meetup" aria-hidden="true"></i>Únete en Meetup</a>
          <a class="btn btn-ghost" href="/eventos/">Ver eventos <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
        </div>
      </div>
      <div class="art">
        {pixel_svg()}
        <span class="art-label" aria-hidden="true">lat 0°00′00″</span>
        <span class="art-label r" aria-hidden="true">mitad_del_mundo.png</span>
      </div>
    </div>

    <div class="wrap">
      <dl class="stats">
        <div><dt>miembros_meetup</dt><dd>+1.400</dd></div>
        <div><dt>community_days</dt><dd>4</dd></div>
        <div><dt>fotos_de_eventos</dt><dd>+680</dd></div>
        <div><dt>ciudades</dt><dd class="t">Quito · Guayaquil · Cuenca</dd></div>
      </dl>
    </div>

    <div class="photo-band">
      <figure>
        <picture><source type="image/avif" srcset="/img/community-day-2024-640.avif 640w, /img/community-day-2024-828.avif 828w, /img/community-day-2024-1024.avif 1024w, /img/community-day-2024-1280.avif 1280w, /img/community-day-2024-1600.avif 1600w, /img/community-day-2024-2400.avif 2400w" sizes="100vw"><img src="/img/community-day-2024-1024.webp" srcset="/img/community-day-2024-640.webp 640w, /img/community-day-2024-828.webp 828w, /img/community-day-2024-1024.webp 1024w, /img/community-day-2024-1280.webp 1280w, /img/community-day-2024-1600.webp 1600w, /img/community-day-2024-2400.webp 2400w" sizes="100vw" width="2400" height="1800" fetchpriority="high" decoding="async" alt="Más de cien integrantes de AWS User Group Ecuador posan frente al letrero del AWS Community Day Ecuador 2024 en la ESPOL, Guayaquil"></picture>
        <figcaption><b>●</b> AWS Community Day Ecuador 2024 · ESPOL, Guayaquil · 5 de octubre de 2024</figcaption>
      </figure>
    </div>
  </section>

  <section class="section anniversary" id="aniversario" aria-labelledby="aniv-title">
    <div class="wrap">
      <div class="aniv-card">
        <div class="aniv-art">{pixel_five()}<span class="aniv-years mono">años</span></div>
        <div class="aniv-body">
          <p class="prompt" aria-hidden="true"><span class="kw">const</span> aniversario = <span class="str">"2027-02-10"</span></p>
          <h2 class="h2" id="aniv-title">Cumplimos 5 años de comunidad</h2>
          <p class="aniv-lede">El <strong><time datetime="2027-02-10">10 de febrero de 2027</time></strong> AWS User Group Ecuador cumple 5 años aprendiendo y construyendo juntos en la nube. Lo vamos a celebrar con toda la comunidad: muy pronto anunciaremos los detalles en Meetup.</p>
          <div class="countdown" role="timer" data-countdown="2027-02-10T00:00:00-05:00" aria-label="Cuenta regresiva para el aniversario">
            <div><span data-u="d">--</span><small>días</small></div>
            <div><span data-u="h">--</span><small>horas</small></div>
            <div><span data-u="m">--</span><small>min</small></div>
            <div><span data-u="s">--</span><small>seg</small></div>
          </div>
          <div class="hero-actions">
            <a class="btn" href="{MEETUP}" rel="noopener" target="_blank"><i class="fa-brands fa-meetup" aria-hidden="true"></i>Avísame en Meetup</a>
            <a class="btn btn-ghost" href="https://calendar.google.com/calendar/render?action=TEMPLATE&amp;text=5%20a%C3%B1os%20de%20AWS%20User%20Group%20Ecuador&amp;dates=20270210/20270211&amp;details=Celebramos%205%20a%C3%B1os%20de%20la%20comunidad%20de%20AWS%20en%20Ecuador.%20Detalles%20en%20https%3A%2F%2Fwww.awsugecuador.com%2F" rel="noopener" target="_blank"><i class="fa-solid fa-calendar-plus" aria-hidden="true"></i>Guardar la fecha</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="comunidad" aria-labelledby="comunidad-title">
    <div class="wrap">
      <div class="section-head split-head">
        <div>
          <span class="eyebrow">por qué unirte</span>
          <h2 id="comunidad-title">Aprender la nube es más fácil en comunidad</h2>
        </div>
        <p>AWS User Group Ecuador es la primera comunidad de Amazon Web Services del país: nació el 10 de febrero de 2022 y forma parte de la red global de AWS User Groups. Es independiente y la organizan voluntarios. Llegan desarrolladores, arquitectos cloud, estudiantes y líderes de tecnología de Quito, Guayaquil y Cuenca, desde quien abre su primera cuenta de AWS hasta quien opera cargas en producción.</p>
      </div>
      <ul class="bento">
        <li class="cell hi reveal"><span class="tag"># start_here</span><h3>De tu primera cuenta de AWS a producción.</h3><p>Aquí compartimos lo que funciona, lo que falló y lo que aprendimos en el camino.</p></li>
        <li class="cell reveal"><span class="tag"># networking</span><h3>Networking</h3><p>Conoce a profesionales y líderes de la nube en Ecuador, y a quienes resuelven los mismos problemas que tú.</p></li>
        <li class="cell reveal"><span class="tag"># learn</span><h3>Actualización continua</h3><p>Charlas y talleres sobre servicios de AWS, buenas prácticas y novedades, explicados por quienes los usan.</p></li>
        <li class="cell reveal"><span class="tag"># certificaciones</span><h3>Certificaciones</h3><p>Retos y sesiones de estudio para preparar tu certificación de AWS con acompañamiento.</p></li>
        <li class="cell reveal"><span class="tag"># speakers</span><h3>Visibilidad profesional</h3><p>Da tu primera charla, muestra tus proyectos y haz crecer tu perfil en el ecosistema AWS.</p></li>
        <li class="cell reveal"><span class="tag"># build</span><h3>Apoyo en proyectos</h3><p>Encuentra mentores, colaboradores o socios para lo que estás construyendo en AWS.</p></li>
      </ul>
    </div>
  </section>

  <section class="section" id="community-day" aria-labelledby="cd-title">
    <div class="wrap cd">
      <figure class="reveal"><img src="/img/momentos/cd-salto-1024.webp" srcset="/img/momentos/cd-salto-480.webp 480w, /img/momentos/cd-salto-1024.webp 1024w, /img/momentos/cd-salto-1600.webp 1600w" sizes="(min-width: 1024px) 55vw, 100vw" width="1600" height="900" loading="lazy" decoding="async" alt="Alexis Polo, líder fundador de AWS User Group Ecuador, celebra saltando junto a decenas de asistentes frente al letrero gigante de AWS Community Day Ecuador"></figure>
      <div>
        <span class="eyebrow">el evento del año</span>
        <h2 class="h2" id="cd-title">AWS Community Day Ecuador</h2>
        <p class="muted" style="margin-top:20px;max-width:46ch">Una jornada completa de charlas técnicas, talleres y networking con speakers nacionales e internacionales, organizada por la comunidad para la comunidad. El encuentro más grande del año para quienes trabajan con AWS en el país.</p>
        <dl class="meta">
          <dt>edición</dt><dd>4.ª · 2026</dd>
          <dt>fecha</dt><dd><time datetime="2026-09-05">5 de septiembre de 2026</time></dd>
          <dt>sede</dt><dd>Universidad Politécnica Salesiana, Cuenca</dd>
          <dt>ediciones</dt><dd>Guayaquil (ESPOL, 2024) · Quito (UDLA, 2025) · Cuenca (UPS, 2026)</dd>
        </dl>
        <div class="actions">
          <a class="btn btn-purple" href="https://www.meetup.com/aws-ecuador/events/314902222/" rel="noopener" target="_blank">Ver la edición 2026 <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="reinvent" aria-labelledby="reinvent-title">
    <div class="wrap reinvent">
      <div>
        <span class="eyebrow">aws re:invent · las vegas</span>
        <h2 class="h2" id="reinvent-title">De la Mitad del Mundo a AWS re:Invent</h2>
        <p class="muted" style="margin-top:20px;max-width:48ch">La comunidad también viaja. Llevamos un pedacito de la Mitad del Mundo hasta Las Vegas, a AWS re:Invent, la conferencia de nube más grande del mundo, para conectar con la comunidad global de AWS y traer de vuelta lo aprendido a Ecuador.</p>
        <div class="tags" style="margin-top:24px"><span class="tag"># reinvent</span><span class="tag"># las-vegas</span><span class="tag"># comunidad-global</span></div>
      </div>
      <figure class="reveal">
        <img src="/img/momentos/reinvent-1024.webp" srcset="/img/momentos/reinvent-480.webp 480w, /img/momentos/reinvent-1024.webp 1024w, /img/momentos/reinvent-1440.webp 1440w" sizes="(min-width: 1024px) 45vw, 100vw" width="1440" height="1440" loading="lazy" decoding="async" alt="Réplica del monumento a la Mitad del Mundo de AWS Community Day Ecuador frente a un hotel iluminado de Las Vegas durante AWS re:Invent">
        <figcaption><b>●</b> AWS re:Invent · Las Vegas</figcaption>
      </figure>
    </div>
    <div class="wrap">
      <div class="reinvent-strip" role="list" aria-label="Fotos de la comunidad en AWS re:Invent">
          <figure role="listitem" class="wide"><img src="/img/momentos/reinvent-hero-480.webp" srcset="/img/momentos/reinvent-hero-480.webp 480w, /img/momentos/reinvent-hero-960.webp 960w" sizes="(min-width: 1024px) 45vw, 60vw" width="2048" height="1536" loading="lazy" decoding="async" alt="Alexis Polo, líder fundador de AWS User Group Ecuador, se toma una selfie con un AWS Hero en AWS re:Invent"><figcaption>Con un AWS Hero</figcaption></figure>
          <figure role="listitem"><img src="/img/momentos/reinvent-2-480.webp" srcset="/img/momentos/reinvent-2-480.webp 480w, /img/momentos/reinvent-2-960.webp 960w" sizes="(min-width: 1024px) 22vw, 60vw" width="960" height="1200" loading="lazy" decoding="async" alt="Logo gigante de AWS iluminado en morado en el hall de AWS re:Invent en Las Vegas"><figcaption>AWS re:Invent</figcaption></figure>
          <figure role="listitem"><img src="/img/momentos/reinvent-3-480.webp" srcset="/img/momentos/reinvent-3-480.webp 480w, /img/momentos/reinvent-3-960.webp 960w" sizes="(min-width: 1024px) 22vw, 60vw" width="960" height="1200" loading="lazy" decoding="async" alt="Pantalla de AWS re:Invent en la zona de registro de badges, con asistentes haciendo fila"><figcaption>Badge pickup</figcaption></figure>
          <figure role="listitem"><img src="/img/momentos/reinvent-4-480.webp" srcset="/img/momentos/reinvent-4-480.webp 480w, /img/momentos/reinvent-4-960.webp 960w" sizes="(min-width: 1024px) 22vw, 60vw" width="1080" height="1350" loading="lazy" decoding="async" alt="Integrante de AWS User Group Ecuador sonríe con la réplica del monumento de AWS Community Day Ecuador en AWS re:Invent"><figcaption>Comunidad en re:Invent</figcaption></figure>
          <figure role="listitem"><img src="/img/momentos/reinvent-5-480.webp" srcset="/img/momentos/reinvent-5-480.webp 480w, /img/momentos/reinvent-5-960.webp 960w" sizes="(min-width: 1024px) 22vw, 60vw" width="1080" height="1350" loading="lazy" decoding="async" alt="Integrante de AWS User Group Ecuador posa con la réplica del monumento de AWS Community Day Ecuador en Las Vegas"><figcaption>Comunidad en re:Invent</figcaption></figure>
          <figure role="listitem"><img src="/img/momentos/reinvent-expo-480.webp" srcset="/img/momentos/reinvent-expo-480.webp 480w, /img/momentos/reinvent-expo-960.webp 960w" sizes="(min-width: 1024px) 22vw, 60vw" width="1536" height="2048" loading="lazy" decoding="async" alt="Expo hall de AWS re:Invent con el gran letrero de AWS iluminado y asistentes recorriendo los stands"><figcaption>Expo hall</figcaption></figure>
          <figure role="listitem"><img src="/img/momentos/reinvent-6-480.webp" srcset="/img/momentos/reinvent-6-480.webp 480w, /img/momentos/reinvent-6-960.webp 960w" sizes="(min-width: 1024px) 22vw, 60vw" width="898" height="672" loading="lazy" decoding="async" alt="Letrero de entrada a AWS re:Invent con luces de colores en Las Vegas"><figcaption>Entrada a re:Invent</figcaption></figure>
      </div>
    </div>
  </section>

  <section class="section" id="eventos" aria-labelledby="eventos-title">
    <div class="wrap">
      <div class="section-head split-head">
        <div>
          <span class="eyebrow">agenda</span>
          <h2 id="eventos-title">Eventos recientes</h2>
        </div>
        <p>Meetups presenciales y online sobre arquitectura, inteligencia artificial, certificaciones y carrera en la nube. Los próximos eventos se anuncian primero en Meetup.</p>
      </div>
      <ol class="feed">{event_items(False, 4)}
      </ol>
      <div class="events-foot">
        <a class="btn" href="https://www.meetup.com/aws-ecuador/events/" rel="noopener" target="_blank"><i class="fa-brands fa-meetup" aria-hidden="true"></i>Próximos eventos en Meetup</a>
        <a class="btn btn-ghost" href="/eventos/">Todos los eventos <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
      </div>
    </div>
  </section>

  <section class="section" id="momentos" aria-labelledby="momentos-title">
    <div class="wrap">
      <div class="section-head split-head">
        <div>
          <span class="eyebrow">momentos</span>
          <h2 id="momentos-title">Charlas, premios y reencuentros</h2>
        </div>
        <p>Más de 680 fotos de nuestros eventos: auditorios llenos, speakers de todo el país, el viaje a AWS re:Invent, premios, stickers y fotos grupales que no caben en un solo encuadre.</p>
      </div>
      <div class="filters" role="group" aria-label="Filtrar fotos por evento">
        <button type="button" class="chip" aria-pressed="true" data-filter="all"># todos</button>
        <button type="button" class="chip" aria-pressed="false" data-filter="community-day"># community-day</button>
        <button type="button" class="chip" aria-pressed="false" data-filter="security"># security-day</button>
        <button type="button" class="chip" aria-pressed="false" data-filter="mujeres"># mujeres-en-tech</button>
        <button type="button" class="chip" aria-pressed="false" data-filter="reinvent"># reinvent</button>
      </div>
      <div class="moments" id="moments-grid">{moments_html()}
      </div>
      <button type="button" class="btn btn-ghost more" aria-controls="moments-grid" aria-expanded="false"><i class="fa-solid fa-images" aria-hidden="true"></i>Ver más fotos</button>
      <h3 class="albums-title mono">// álbumes</h3>
      <ul class="albums">{albums_html()}
      </ul>
    </div>
  </section>

  <section class="section" id="equipo" aria-labelledby="equipo-title">
    <div class="wrap">
      <div class="section-head split-head">
        <div>
          <span class="eyebrow">quiénes organizan</span>
          <h2 id="equipo-title">Equipo voluntario</h2>
        </div>
        <p>Las personas que impulsan la comunidad, organizan cada evento y abren espacio a nuevas voces de la nube en Ecuador.</p>
      </div>
      <ul class="team">{team_items(True)}
      </ul>
      <p style="margin-top:32px"><a class="link" href="/equipo/">Conoce al equipo <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></p>
    </div>
  </section>

  <section class="section" id="sponsors" aria-labelledby="sponsors-title">
    <div class="wrap">
      <div class="section-head split-head">
        <div>
          <span class="eyebrow">gracias</span>
          <h2 id="sponsors-title">Sponsors y partners</h2>
        </div>
        <p>Empresas que hacen posible cada evento con espacio, logística y apoyo a la comunidad.</p>
      </div>
      <ul class="sponsors">
        <li><img src="/img/sponsor-gyetech.png" width="224" height="67" loading="lazy" alt="GYE Tech"></li>
        <li><img src="/img/sponsor-ondu-cloud.png" width="264" height="42" loading="lazy" alt="Ondú Cloud"></li>
        <li><img src="/img/sponsor-publifyer.png" width="265" height="46" loading="lazy" alt="Publifyer"></li>
      </ul>
      <div class="cta-card">
        <p>¿Tu empresa quiere llegar a la comunidad de AWS en Ecuador?</p>
        <a class="btn" href="mailto:hello@awsugecuador.com?subject=Quiero%20ser%20sponsor%20de%20AWS%20User%20Group%20Ecuador"><i class="fa-solid fa-envelope" aria-hidden="true"></i>Quiero ser sponsor</a>
      </div>
    </div>
  </section>

  <section class="section section-sm" id="comunidades" aria-labelledby="comunidades-title">
    <div class="wrap">
      <h2 class="h3-mono" id="comunidades-title">// otras comunidades AWS en Ecuador</h2>
      <p class="muted cl-intro">Busca el User Group o Student Builder Group más cercano a tu ciudad o universidad y únete a su Meetup.</p>
      <ul class="comm-list">{communities_html()}
      </ul>
    </div>
  </section>

  <section class="section" id="preguntas" aria-labelledby="faq-title">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">preguntas frecuentes</span>
        <h2 id="faq-title">Antes de tu primer meetup</h2>
      </div>
      <div class="faq">{faq_html}
      </div>
    </div>
  </section>
'''
preload = '\n<link rel="preload" as="image" type="image/avif" imagesrcset="/img/community-day-2024-640.avif 640w, /img/community-day-2024-828.avif 828w, /img/community-day-2024-1024.avif 1024w, /img/community-day-2024-1280.avif 1280w, /img/community-day-2024-1600.avif 1600w, /img/community-day-2024-2400.avif 2400w" imagesizes="100vw" fetchpriority="high">'
open('index.html','w',encoding='utf-8').write(page('/', 'AWS User Group Ecuador | Primera comunidad de AWS en Ecuador',
  'La primera comunidad de AWS en Ecuador, fundada por Alexis Polo. Meetups, talleres, certificaciones AWS y el AWS Community Day en Quito, Guayaquil y Cuenca.',
  home_ld, home_body, '/', preload))

# ---------- shared ld ----------
ORG = {"@type":"Organization","@id":SITE+"/#organization","name":"AWS User Group Ecuador","url":SITE+"/","logo":SITE+"/img/icon-512.png"}
def crumbs(name, path):
    return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":SITE+"/"},{"@type":"ListItem","position":2,"name":name,"item":SITE+path}]}
def crumbs_html(name):
    return f'<nav class="crumbs" aria-label="Ruta de navegación"><ol><li><a href="/">~/inicio</a></li><li aria-current="page">{name.lower()}</li></ol></nav>'
def dump(graph): return json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False, indent=2)

# ---------- EVENTOS ----------
ev_ld = []
for e in EVENTS:
    o = {"@type":"Event","name":e['t'],"startDate":e['d'],"description":e['desc'],"url":e['url'],"image":SITE+"/img/"+e['img'],
         "eventStatus":"https://schema.org/EventScheduled","organizer":{"@id":SITE+"/#organization"},"inLanguage":"es"}
    if e['place']:
        o["eventAttendanceMode"]="https://schema.org/OfflineEventAttendanceMode"
        addr={"@type":"PostalAddress","addressCountry":"EC"}
        if e['place'][1]: addr["addressLocality"]=e['place'][1]
        o["location"]={"@type":"Place","name":e['place'][0],"address":addr}
    else:
        o["eventAttendanceMode"]="https://schema.org/OnlineEventAttendanceMode"
        o["location"]={"@type":"VirtualLocation","url":e['url']}
    ev_ld.append(o)
ev_body = f'''
  <section class="page-hero" aria-labelledby="page-title">
    <div class="wrap">
      {crumbs_html("Eventos")}
      <h1 id="page-title">Eventos de AWS en Ecuador<span class="cursor" aria-hidden="true"></span></h1>
      <p class="lede">Meetups, talleres y el AWS Community Day Ecuador. Eventos presenciales en Quito, Guayaquil y Cuenca, y sesiones online para todo el país, organizados por la primera comunidad de AWS del Ecuador.</p>
      <div class="notice">
        <p>Los próximos eventos se publican primero en Meetup. Únete al grupo para recibir el aviso y reservar tu lugar.</p>
        <a class="btn btn-purple" href="https://www.meetup.com/aws-ecuador/events/" rel="noopener" target="_blank"><i class="fa-brands fa-meetup" aria-hidden="true"></i>Ver próximos eventos</a>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="pasados-title">
    <div class="wrap">
      <div class="section-head split-head">
        <div>
          <span class="eyebrow">archivo</span>
          <h2 id="pasados-title">Eventos realizados</h2>
        </div>
        <p>Una muestra de lo que hacemos durante el año: arquitectura, inteligencia artificial con Amazon Bedrock, carrera profesional y comunidad.</p>
      </div>
      <ol class="feed">{event_items(True)}
      </ol>
    </div>
  </section>

  <section class="section" aria-labelledby="cd-title">
    <div class="wrap cd">
      <figure class="reveal">{img("community-day-equipo", [640,1024,1600], 1600, 1200, "Organizadores de AWS User Group Ecuador junto al letrero de AWS Community Day Ecuador", "(min-width: 1024px) 55vw, 100vw")}</figure>
      <div>
        <span class="eyebrow">una vez al año</span>
        <h2 class="h2" id="cd-title">AWS Community Day Ecuador</h2>
        <p class="muted" style="margin-top:20px;max-width:46ch">El AWS Community Day es un evento técnico organizado por comunidades de AWS en todo el mundo. En Ecuador lo organiza AWS User Group Ecuador, con charlas de la comunidad, talleres y espacio para conocer a quienes construyen en la nube en el país.</p>
        <dl class="meta">
          <dt>última edición</dt><dd><time datetime="2026-09-05">5 de septiembre de 2026</time></dd>
          <dt>sede</dt><dd>Universidad Politécnica Salesiana, Cuenca</dd>
        </dl>
        <a class="link" href="mailto:hello@awsugecuador.com?subject=AWS%20Community%20Day%20Ecuador">Patrocina o colabora en la próxima edición <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="albums-title">
    <div class="wrap">
      <div class="section-head split-head">
        <div>
          <span class="eyebrow">galería</span>
          <h2 id="albums-title">Fotos de nuestros eventos</h2>
        </div>
        <p>Revive cada edición en los álbumes de fotos de la comunidad.</p>
      </div>
      <ul class="albums">{albums_html()}
      </ul>
    </div>
  </section>

  <section class="section" aria-labelledby="charla-title">
    <div class="wrap">
      <div class="cta-card" style="margin-top:0">
        <div>
          <span class="mono" style="display:block;margin-bottom:10px;font-size:.875rem">// call_for_speakers</span>
          <h2 class="h2" id="charla-title" style="font-size:clamp(1.5rem,4.4vw,2.5rem)">¿Construiste algo en AWS? Cuéntalo en un meetup.</h2>
          <p style="font:400 1rem/1.55 var(--sans);letter-spacing:0;margin-top:14px;max-width:52ch">Buscamos charlas de todos los niveles: tu primera arquitectura serverless, una migración real, cómo preparaste tu certificación o lo que aprendiste al llevar IA generativa a producción. Si es tu primera vez, te ayudamos a prepararla.</p>
        </div>
        <a class="btn" href="mailto:hello@awsugecuador.com?subject=Propuesta%20de%20charla"><i class="fa-solid fa-microphone" aria-hidden="true"></i>Proponer una charla</a>
      </div>
    </div>
  </section>
'''
graph = [ORG, {"@type":"CollectionPage","@id":SITE+"/eventos/#webpage","url":SITE+"/eventos/","name":"Eventos de AWS en Ecuador","inLanguage":"es-EC","isPartOf":{"@id":SITE+"/#website"}}, crumbs("Eventos","/eventos/")] + ev_ld
open('eventos/index.html','w',encoding='utf-8').write(page('/eventos/', 'Eventos de AWS en Ecuador: meetups y Community Day',
  'Eventos de AWS en Ecuador: meetups, talleres y AWS Community Day en Quito, Guayaquil y Cuenca, organizados por AWS User Group Ecuador.',
  dump(graph), ev_body, '/eventos/'))

# ---------- EQUIPO ----------
person_ld = []
for p in PEOPLE:
    o = {"@type":"Person","@id":f"{SITE}/equipo/#{p['id']}","name":p['n'],"jobTitle":p['r'] + (' de AWS User Group Ecuador' if p['id']=='alexis-polo' else ''),"image":f"{SITE}/img/{p['img']}-768.webp","memberOf":{"@id":SITE+"/#organization"}}
    if p['links']: o["sameAs"] = [u for u,_,_ in p['links']]
    if p['id'] == 'alexis-polo':
        o["url"] = "https://www.alexispolo.com"
        o["description"] = "Líder fundador de AWS User Group Ecuador, la primera comunidad de AWS del Ecuador, fundada el 10 de febrero de 2022."
        o["knowsAbout"] = ["Amazon Web Services", "Comunidades tecnológicas"]
    person_ld.append(o)
eq_body = f'''
  <section class="page-hero" aria-labelledby="page-title">
    <div class="wrap">
      {crumbs_html("Equipo")}
      <h1 id="page-title">El equipo detrás de la comunidad<span class="cursor" aria-hidden="true"></span></h1>
      <p class="lede">AWS User Group Ecuador, la primera comunidad de AWS del Ecuador, nació en 2022 y la organizan voluntarios. Preparamos cada meetup, buscamos speakers, conseguimos espacios y abrimos la puerta a quien quiera aprender AWS en Ecuador.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="leaders-title">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">user group leaders</span>
        <h2 id="leaders-title">Quienes lideran</h2>
      </div>
      <ul class="team">{team_items(False)}
      </ul>
      <div class="in-action">
        <span class="eyebrow">en acción</span>
        <h2 class="h2">Así se vive la comunidad</h2>
        <div class="action-grid">
          <figure><img src="/img/momentos/54890831244-1024.webp" srcset="/img/momentos/54890831244-480.webp 480w, /img/momentos/54890831244-1024.webp 1024w" sizes="(min-width: 768px) 50vw, 100vw" width="1024" height="683" loading="lazy" decoding="async" alt="Alexis Polo, líder fundador de AWS User Group Ecuador, habla con el público en el AWS Community Day Ecuador 2025 en Quito"><figcaption>Community Day 2025</figcaption></figure>
          <figure><img src="/img/momentos/55090151586-480.webp" srcset="/img/momentos/55090151586-480.webp 480w, /img/momentos/55090151586-1024.webp 1024w" sizes="(min-width: 768px) 25vw, 50vw" width="1024" height="1024" loading="lazy" decoding="async" alt="Alexis Polo, fundador de AWS User Group Ecuador, da la bienvenida desde el podio del AWS Security Day"><figcaption>Security Day</figcaption></figure>
          <figure><img src="/img/momentos/54882557068-480.webp" srcset="/img/momentos/54882557068-480.webp 480w, /img/momentos/54882557068-1024.webp 1024w" sizes="(min-width: 768px) 25vw, 50vw" width="1024" height="740" loading="lazy" decoding="async" alt="Alexis Polo presenta a los speakers en el escenario del AWS Community Day Ecuador 2025"><figcaption>Community Day 2025</figcaption></figure>
          <figure><img src="/img/momentos/cd-salto-1024.webp" srcset="/img/momentos/cd-salto-480.webp 480w, /img/momentos/cd-salto-1024.webp 1024w" sizes="(min-width: 768px) 50vw, 100vw" width="1024" height="576" loading="lazy" decoding="async" alt="Alexis Polo, líder de AWS User Group Ecuador, celebra con los asistentes frente al letrero de AWS Community Day Ecuador"><figcaption>Community Day</figcaption></figure>
        </div>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="vol-title">
    <div class="wrap split">
      <div>
        <span class="eyebrow">voluntariado</span>
        <h2 class="h2" id="vol-title">Súmate al equipo y ayuda a crecer la comunidad</h2>
      </div>
      <div class="body">
        <p>No necesitas ser experto en AWS. Necesitamos manos para organizar eventos, diseñar piezas, cubrir redes sociales, apoyar el AWS Community Day y recibir a quienes llegan por primera vez.</p>
        <ul class="list">
          <li><h3># eventos</h3><p>Logística, registro de asistentes y coordinación con sedes en Quito, Guayaquil y Cuenca.</p></li>
          <li><h3># contenido</h3><p>Diseño, fotografía, video y publicaciones para las redes de la comunidad.</p></li>
          <li><h3># speakers</h3><p>Buscar, acompañar y preparar a quienes dan su primera charla.</p></li>
        </ul>
        <p style="margin-top:28px"><a class="btn btn-purple" href="mailto:hello@awsugecuador.com?subject=Quiero%20ser%20voluntario"><i class="fa-solid fa-envelope" aria-hidden="true"></i>Quiero ser voluntario</a></p>
      </div>
    </div>
  </section>
'''
graph = [ORG, {"@type":"AboutPage","@id":SITE+"/equipo/#webpage","url":SITE+"/equipo/","name":"Equipo de AWS User Group Ecuador","inLanguage":"es-EC","isPartOf":{"@id":SITE+"/#website"}}, crumbs("Equipo","/equipo/")] + person_ld
open('equipo/index.html','w',encoding='utf-8').write(page('/equipo/',
  'Alexis Polo, líder fundador | Equipo AWS User Group Ecuador',
  'Alexis Polo es el líder fundador de AWS User Group Ecuador, la primera comunidad de AWS del país. Conoce al equipo: Alexis Polo, Vanessa Barreiro y Paul Rizo.',
  dump(graph), eq_body, '/equipo/'))

# ---------- 404 ----------
nf_body = '''
  <section class="page-hero" style="min-height:62svh" aria-labelledby="page-title">
    <div class="wrap">
      <p class="prompt"><span class="kw">error</span> 404: <span class="str">"página fuera de la línea ecuatorial"</span></p>
      <h1 id="page-title">Esta página no existe<span class="cursor" aria-hidden="true"></span></h1>
      <p class="lede">Puede que el enlace haya cambiado con el nuevo sitio. Vuelve al inicio o revisa los próximos eventos.</p>
      <div class="hero-actions">
        <a class="btn" href="/">Ir al inicio</a>
        <a class="btn btn-ghost" href="/eventos/">Ver eventos <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
      </div>
    </div>
  </section>
'''
open('404.html','w',encoding='utf-8').write(page('/404', 'Página no encontrada | AWS User Group Ecuador', 'La página que buscas no existe.', dump([ORG]), nf_body, '', robots='noindex, follow', canonical=False))

# ---------- Font Awesome (auto-hospedado y recortado) ----------
# Detecta los íconos usados en las páginas, recorta las fuentes de Font Awesome Free
# a solo esos glifos (requiere: pip install fonttools brotli) e incrusta su CSS mínimo.
PAGES = ['index.html', 'eventos/index.html', 'equipo/index.html', '404.html']
FA_DIR = 'tools/fontawesome'
html = {f: open(f, encoding='utf-8').read() for f in PAGES}
used = sorted(set(re.findall(r'\bfa-(solid|brands) fa-([a-z0-9-]+)', ' '.join(html.values()))))
fa_src = open(f'{FA_DIR}/all.css', encoding='utf-8').read()
codes = {}
for kind, name in used:
    m = re.search(r'\.fa-' + re.escape(name) + r' \{\s*--fa: "\\([0-9a-f]+)"', fa_src)
    if not m:
        raise SystemExit(f'Ícono no encontrado en Font Awesome Free: fa-{name}')
    codes[(kind, name)] = m.group(1)

try:
    from fontTools import subset as ft_subset
    for kind, src in (('solid', 'fa-solid-900.woff2'), ('brands', 'fa-brands-400.woff2')):
        cps = [int(c, 16) for (k, _), c in codes.items() if k == kind]
        opts = ft_subset.Options(); opts.flavor = 'woff2'; opts.layout_features = []; opts.name_IDs = ['*']; opts.notdef_outline = False
        font = ft_subset.load_font(f'{FA_DIR}/{src}', opts)
        sub = ft_subset.Subsetter(opts); sub.populate(unicodes=cps); sub.subset(font)
        tmp = f'fonts/fa-{kind}.tmp.woff2'
        ft_subset.save_font(font, tmp, opts)
        digest = hashlib.sha1(open(tmp, 'rb').read()).hexdigest()[:8]
        for old in glob.glob(f'fonts/fa-{kind}-*.woff2'):
            os.remove(old)
        os.replace(tmp, f'fonts/fa-{kind}-{digest}.woff2')
except ImportError:
    print('Aviso: fonttools no está instalado; se usan las fuentes recortadas existentes en fonts/. Si agregaste íconos nuevos: pip install fonttools brotli')

# nombres con huella de contenido (permiten caché de 1 año sin servir versiones viejas)
FA_FILES = {k: '/' + sorted(glob.glob(f'fonts/fa-{k}-*.woff2'))[-1] for k in ('solid', 'brands')}

fa_css = (
    '@font-face{font-family:"Font Awesome 6 Free";font-style:normal;font-weight:900;font-display:swap;src:url(' + FA_FILES['solid'] + ') format("woff2")}'
    '@font-face{font-family:"Font Awesome 6 Brands";font-style:normal;font-weight:400;font-display:swap;src:url(' + FA_FILES['brands'] + ') format("woff2")}'
    '.fa-solid,.fa-brands{display:inline-block;min-width:1em;text-align:center;line-height:1;font-style:normal;font-variant:normal;text-rendering:auto;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}'
    '.fa-solid{font-family:"Font Awesome 6 Free";font-weight:900}'
    '.fa-brands{font-family:"Font Awesome 6 Brands";font-weight:400}'
    '.fa-solid::before,.fa-brands::before{content:var(--fa)}'
    + ''.join(f'.fa-{n}{{--fa:"\\{c}"}}' for (k, n), c in sorted(codes.items(), key=lambda x: x[0][1]))
)
for f, h in html.items():
    h = h.replace('/*FA*/', fa_css).replace('/fonts/fa-solid.woff2', FA_FILES['solid']).replace('/fonts/fa-brands.woff2', FA_FILES['brands'])
    open(f, 'w', encoding='utf-8').write(h)
print(f'ok · {len(codes)} íconos de Font Awesome')

