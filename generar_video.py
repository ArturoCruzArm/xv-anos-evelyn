#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video de XV Años — Evelyn Estefanía
Tema: La Bella y la Bestia  |  15 de Marzo 2026
~2:00 min  |  1920x1080  |  30fps

Secuencia:
  1. Producciones Foro 7          8s
  2. Apertura oscura              3.5s
  3. Título principal            14s
  4-8. Fotos con Ken Burns        9s x5 = 45s
  9.  Familia & Madrina          12s
  10. Ceremonia religiosa         8s
  11. Recepción / Salón Laja      8s
  12. Cierre cinematográfico      13s
  13. Fundido a negro             3.5s
  ─────────────────────────────── 119s ≈ 1:59
"""
import os, sys, subprocess, glob as _glob, urllib.request, re
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
PROYECTO  = 'D:/eventos/xv-anos-evelyn'
WORK      = PROYECTO
OUTPUT    = f'{WORK}/invitacion_evelyn_xv.mp4'
FOTOS_DIR = f'{PROYECTO}/imagenes'
WF        = 'C:/Windows/Fonts'
BODA_VID  = 'C:/Users/foro7/boda-video'

_mp3s  = _glob.glob(f'{PROYECTO}/*.mp3')
MUSICA = _mp3s[0] if _mp3s else ''
print('Musica:', MUSICA or '(ninguna)')

W, H = 1920, 1080
FPS  = 30

# ──────────────────────────────────────────────
# PALETA — La Bella y la Bestia (azul + dorado + rosa)
# ──────────────────────────────────────────────
DARK      = ( 15,  23,  42)   # azul muy oscuro
DARK2     = ( 20,  30,  65)   # azul oscuro
BLUE      = ( 30,  58, 138)   # azul principal
BLUE_M    = ( 45,  85, 175)   # azul medio
BLUE_L    = ( 96, 145, 220)   # azul claro
GOLD      = (178, 138,  22)   # dorado base
GOLD_L    = (230, 185,  58)   # dorado claro
GOLD_D    = (115,  90,  12)   # dorado oscuro
ROSE      = (155,  18,  52)   # rosa/burdeos
ROSE_L    = (218,  80, 108)   # rosa claro
WHITE     = (255, 253, 244)   # blanco cálido
CREAM     = (253, 248, 228)   # crema
CREAM_D   = (238, 230, 208)   # crema oscuro
TAUPE     = (148, 128, 108)   # neutro

# ──────────────────────────────────────────────
# FUENTES
# ──────────────────────────────────────────────
def download_font(font_name, css_url, save_path):
    if os.path.exists(save_path):
        return save_path
    try:
        req = urllib.request.Request(css_url, headers={
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1)'
        })
        with urllib.request.urlopen(req, timeout=10) as r:
            css = r.read().decode('utf-8')
        urls = re.findall(r'src:\s*url\(([^)]+)\)', css)
        if urls:
            freq = urllib.request.Request(urls[0], headers={
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1)'
            })
            with urllib.request.urlopen(freq, timeout=10) as r:
                data = r.read()
            with open(save_path, 'wb') as f:
                f.write(data)
            print(f'  ✓ {font_name} descargada')
            return save_path
    except Exception as e:
        print(f'  ! {font_name}: {e}')
    return None

print('Configurando fuentes...')
GVIBES = download_font(
    'Great Vibes',
    'https://fonts.googleapis.com/css?family=Great+Vibes',
    f'{WORK}/GreatVibes.ttf'
)
CINZEL = download_font(
    'Cinzel',
    'https://fonts.googleapis.com/css?family=Cinzel:400',
    f'{WORK}/Cinzel.ttf'
)
# Fallbacks del proyecto de boda
MRD  = f'{BODA_VID}/MrDeHaviland.ttf'
CORM = f'{BODA_VID}/CormorantGaramond.ttf'

def best(candidates, size):
    for c in candidates:
        if c and os.path.exists(c):
            try: return ImageFont.truetype(c, size)
            except: pass
    return ImageFont.load_default()

def F(name, size):
    return {
        'script':  best([GVIBES, MRD,  f'{WF}/Gabriola.ttf', f'{WF}/Inkfree.ttf'],       size),
        'serif':   best([CINZEL, CORM, f'{WF}/georgia.ttf',   f'{WF}/pala.ttf'],          size),
        'serifb':  best([CINZEL, f'{WF}/georgiab.ttf',  f'{WF}/palab.ttf'],               size),
        'italic':  best([CORM, f'{WF}/georgiai.ttf', f'{WF}/palai.ttf',
                         f'{WF}/Candarai.ttf'],                                            size),
        'sans':    best([f'{WF}/Candara.ttf',  f'{WF}/corbel.ttf',  f'{WF}/calibril.ttf'],size),
        'light':   best([f'{WF}/Candaral.ttf', f'{WF}/calibril.ttf'],                     size),
    }[name]

fSCRIPT_XL = F('script', 132)
fSCRIPT_LG = F('script',  92)
fSCRIPT_MD = F('script',  66)
fSCRIPT_SM = F('script',  50)
fSERIF_XL  = F('serif',   78)
fSERIF_LG  = F('serif',   56)
fSERIF_MD  = F('serif',   42)
fSERIF_SM  = F('serif',   32)
fITALIC    = F('italic',  38)
fITALIC_SM = F('italic',  30)
fITALIC_XS = F('italic',  24)
fSANS_LG   = F('sans',    38)
fSANS_MD   = F('sans',    28)
fSANS_SM   = F('sans',    22)
fSANS_XS   = F('sans',    18)
fLIGHT     = F('light',   26)

# ──────────────────────────────────────────────
# IMÁGENES DECORATIVAS: bella 1, bella 2, bella 3
# ──────────────────────────────────────────────
print('Cargando decoraciones...')
_BELLAS = {}
for n in [1, 2, 3]:
    bpath = os.path.join(FOTOS_DIR, f'bella {n}.png')
    if os.path.exists(bpath):
        try:
            _BELLAS[n] = Image.open(bpath).convert('RGBA')
            print(f'  ✓ bella {n}.png  ({_BELLAS[n].size[0]}x{_BELLAS[n].size[1]})')
        except Exception as e:
            print(f'  ! bella {n}.png: {e}')
    else:
        print(f'  ! No encontrada: {bpath}')

def add_bella(img, num=1, size=None, alpha=1.0, pos='bottom-right'):
    src = _BELLAS.get(num)
    if src is None: return
    sz  = size or (340, 340)
    dec = src.resize(sz, Image.LANCZOS).copy()
    if alpha < 1.0:
        ac = dec.split()[3].point(lambda p: int(p * alpha))
        dec.putalpha(ac)
    sw, sh = sz
    positions = {
        'bottom-right': (W - sw + 40,  H - sh + 40),
        'bottom-left':  (-40,           H - sh + 40),
        'top-right':    (W - sw + 40,  -40),
        'top-left':     (-40,          -40),
        'center':       ((W - sw)//2,  (H - sh)//2),
    }
    px, py = positions.get(pos, (W - sw + 40, H - sh + 40))
    img.paste(dec, (px, py), dec)

# ──────────────────────────────────────────────
# EASING / UTIL
# ──────────────────────────────────────────────
def clamp(v, lo=0.0, hi=1.0): return max(lo, min(hi, v))
def ease_io(t): t = clamp(t); return t*t*(3-2*t)
def ease_out(t): t = clamp(t); return 1-(1-t)**3
def lerp(a, b, t): return a + (b-a)*clamp(t)
def sub_t(t, s, e): return clamp((t-s)/(e-s)) if e > s else (1.0 if t >= s else 0.0)

# ──────────────────────────────────────────────
# PRIMITIVAS DE DIBUJO
# ──────────────────────────────────────────────
def tw(font, text):
    bb = font.getbbox(text); return bb[2]-bb[0]

def draw_text(img, text, x, y, font, color, alpha=1.0,
              shadow=True, sh_off=2, sh_alpha=0.18):
    if alpha <= 0.01: return
    draw = ImageDraw.Draw(img, 'RGBA')
    a = int(alpha*255)
    if shadow and a > 20:
        draw.text((x+sh_off, y+sh_off), text, font=font,
                  fill=(*DARK, int(a*sh_alpha)))
    draw.text((x, y), text, font=font, fill=(*color, a))

def draw_center(img, text, y, font, color, alpha=1.0, shadow=True, sh_off=2):
    x = (W - tw(font, text)) // 2
    draw_text(img, text, x, y, font, color, alpha, shadow, sh_off)

def draw_center_dx(img, text, y, font, color, alpha=1.0, dx=0, shadow=True, sh_off=2):
    x = (W - tw(font, text)) // 2 + dx
    draw_text(img, text, x, y, font, color, alpha, shadow, sh_off=sh_off)

def line_grow(img, y, progress, color, alpha=1.0, max_half=700, w=1):
    if progress <= 0: return
    draw = ImageDraw.Draw(img, 'RGBA')
    cx = W//2
    h  = int(max_half * ease_out(progress))
    draw.line([(cx-h, y), (cx+h, y)], fill=(*color, int(alpha*255)), width=w)

def ornament(img, y, progress, color=None, alpha=1.0):
    if progress <= 0: return
    color = color or GOLD
    draw  = ImageDraw.Draw(img, 'RGBA')
    p_d   = ease_out(sub_t(progress, 0.0, 0.4))
    p_l   = ease_out(sub_t(progress, 0.3, 1.0))
    cx, s = W//2, 10
    a = int(alpha*p_d*230)
    if a > 0:
        pts = [(cx, y-s), (cx+s*2, y), (cx, y+s), (cx-s*2, y)]
        draw.polygon(pts, fill=(*color, a))
        draw.polygon(pts, outline=(*GOLD_D, a//2))
    h  = int(200*p_l); la = int(alpha*p_l*140)
    if la > 0:
        draw.line([(cx-s*2-5-h, y), (cx-s*2-5, y)], fill=(*GOLD_D, la), width=1)
        draw.line([(cx+s*2+5,   y), (cx+s*2+5+h, y)], fill=(*GOLD_D, la), width=1)

def rose_ornament(img, y, progress, alpha=1.0):
    """Ornamento de rosa estilizada para el tema Bella y la Bestia"""
    if progress <= 0: return
    draw = ImageDraw.Draw(img, 'RGBA')
    a    = int(alpha * ease_out(progress) * 220)
    if a <= 0: return
    cx = W//2
    # Diamante principal en dorado
    s = 8
    pts = [(cx, y-s), (cx+s*2, y), (cx, y+s), (cx-s*2, y)]
    draw.polygon(pts, fill=(*GOLD, a))
    # Puntos laterales pequeños en rosa
    sr = 4
    for dx in [-60, 60]:
        pts2 = [(cx+dx, y-sr), (cx+dx+sr*2, y), (cx+dx, y+sr), (cx+dx-sr*2, y)]
        draw.polygon(pts2, fill=(*ROSE_L, int(a*0.7)))
    # Líneas extendidas
    h = int(220 * ease_out(sub_t(progress, 0.3, 1.0)))
    la = int(alpha * ease_out(sub_t(progress, 0.3, 1.0)) * 130)
    if la > 0:
        draw.line([(cx-s*2-70-h, y), (cx-s*2-70, y)], fill=(*GOLD_D, la), width=1)
        draw.line([(cx+s*2+70, y),   (cx+s*2+70+h, y)], fill=(*GOLD_D, la), width=1)

def gold_frame(img, progress, alpha=0.70, on_dark=True):
    if progress <= 0: return
    draw = ImageDraw.Draw(img, 'RGBA')
    col  = GOLD_L if on_dark else GOLD_D
    a    = int(alpha*255)
    mx, my = 55, 85
    segs = [(mx,my,W-mx,my),(W-mx,my,W-mx,H-my),
            (W-mx,H-my,mx,H-my),(mx,H-my,mx,my)]
    lens = [W-2*mx, H-2*my, W-2*mx, H-2*my]
    rem  = int(sum(lens)*ease_out(progress))
    for (x1,y1,x2,y2), sl in zip(segs, lens):
        if rem <= 0: break
        fr = min(1.0, rem/sl)
        ex = int(x1+(x2-x1)*fr); ey = int(y1+(y2-y1)*fr)
        draw.line([(x1,y1),(ex,ey)], fill=(*col, a), width=1)
        rem -= sl
    if progress > 0.85:
        ca = int(ease_out(sub_t(progress, 0.85, 1.0))*alpha*255)
        for cx, cy, sx, sy in [(mx,my,1,1),(W-mx,my,-1,1),
                                (mx,H-my,1,-1),(W-mx,H-my,-1,-1)]:
            draw.line([(cx,cy),(cx+sx*26,cy)], fill=(*col, ca), width=2)
            draw.line([(cx,cy),(cx,cy+sy*26)], fill=(*col, ca), width=2)

def letterbox(img, bars=54):
    draw = ImageDraw.Draw(img, 'RGBA')
    draw.rectangle([0,0,W,bars],   fill=(0,0,0,255))
    draw.rectangle([0,H-bars,W,H], fill=(0,0,0,255))

def vignette_dark(img, strength=0.55):
    vig = Image.new('L',(W,H),0); dv = ImageDraw.Draw(vig)
    for i in range(70):
        t=i/70; a=int(255*ease_io(t))
        px=int(W*.5*(1-t)); py=int(H*.5*(1-t))
        dv.ellipse([px,py,W-px,H-py], fill=a)
    blk = Image.new('RGB',(W,H),(0,0,0))
    inv = vig.point(lambda p: int((255-p)*strength))
    rgb = img.convert('RGB'); rgb.paste(blk, mask=inv)
    return rgb.convert('RGBA')

def vignette_light(img, strength=0.12):
    vig = Image.new('L',(W,H),0); dv = ImageDraw.Draw(vig)
    for i in range(70):
        t=i/70; a=int(255*ease_io(t))
        px=int(W*.5*(1-t)); py=int(H*.5*(1-t))
        dv.ellipse([px,py,W-px,H-py], fill=a)
    blk = Image.new('RGB',(W,H),(180,160,130))
    inv = vig.point(lambda p: int((255-p)*strength))
    rgb = img.convert('RGB'); rgb.paste(blk, mask=inv)
    return rgb.convert('RGBA')

# ──────────────────────────────────────────────
# FONDOS PRE-RENDERIZADOS
# ──────────────────────────────────────────────
print('Pre-renderizando fondos...')

def make_gradient(c1, c2):
    img = Image.new('RGBA',(W,H)); draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y/H
        r = int(c1[0]+t*(c2[0]-c1[0]))
        g = int(c1[1]+t*(c2[1]-c1[1]))
        b = int(c1[2]+t*(c2[2]-c1[2]))
        draw.line([(0,y),(W,y)], fill=(r,g,b,255))
    return img

BG_DARK  = make_gradient(DARK,   DARK2)
BG_BLUE  = make_gradient((20,35,80),  (10,18,45))
BG_CREAM = make_gradient(CREAM,  CREAM_D)
print('  OK')

# ──────────────────────────────────────────────
# ESCENAS KEN BURNS — bella 1, bella 2, bella 3
# ──────────────────────────────────────────────
print('Preparando escenas bella...')

def bella_scene(num, zoom_in=True, pan_dx=0, pan_dy=0):
    """
    Escena Ken Burns usando bella N como imagen principal centrada
    sobre fondo oscuro borroso.
    """
    src = _BELLAS.get(num)
    if src is None:
        def _blank(t):
            img = BG_DARK.copy(); letterbox(img); return img
        return _blank

    sw, sh = src.size

    # Fondo: escalar la misma imagen para cubrir el frame y aplicar blur
    bg_scale = max(W/sw, H/sh)
    bg_w = int(sw * bg_scale)
    bg_h = int(sh * bg_scale)
    bg = src.convert('RGB').resize((bg_w, bg_h), Image.LANCZOS)
    cx_bg = (bg_w - W) // 2
    cy_bg = (bg_h - H) // 2
    bg = bg.crop((cx_bg, cy_bg, cx_bg+W, cy_bg+H))
    bg = bg.filter(ImageFilter.GaussianBlur(30))
    dark_ov = Image.new('RGBA', (W, H), (0, 0, 0, 175))
    bg_rgba = bg.convert('RGBA')
    bg_rgba.paste(dark_ov, mask=dark_ov.split()[3])

    # Imagen principal: ajustar a la altura manteniendo ratio, margen KB 8%
    ph_scale = H / sh
    ph_w     = int(sw * ph_scale)
    kb_w     = int(ph_w * 1.08)
    kb_h     = int(H    * 1.08)
    photo_kb = src.convert('RGBA').resize((kb_w, kb_h), Image.LANCZOS)

    def scene(t):
        canvas = bg_rgba.copy()
        z = lerp(1.08, 1.00, ease_io(t)) if zoom_in else lerp(1.00, 1.08, ease_io(t))
        extra = int((kb_w - ph_w) * (1.0 - (z - 1.0) / 0.08))
        left  = max(0, (kb_w - ph_w)//2 - extra//2 + int(pan_dx * ease_io(t)))
        top   = max(0, (kb_h - H)//2    + int(pan_dy * ease_io(t)))
        left  = min(left, max(0, kb_w - ph_w))
        top   = min(top,  max(0, kb_h - H))
        crop  = photo_kb.crop((left, top, left + ph_w, top + H))
        px    = (W - ph_w) // 2
        canvas.paste(crop, (px, 0), crop)
        canvas = vignette_dark(canvas, strength=0.38)
        letterbox(canvas)
        return canvas

    return scene

_bella_scenes = [
    bella_scene(1, zoom_in=True,  pan_dy= 40),   # bella 1 — zoom out, pan abajo
    bella_scene(2, zoom_in=False, pan_dy=-40),   # bella 2 — zoom in,  pan arriba
    bella_scene(3, zoom_in=True,  pan_dx= 30),   # bella 3 — zoom out, pan lateral
]
print('  OK — 3 escenas bella listas')

# ══════════════════════════════════════════════
# ESCENAS
# ══════════════════════════════════════════════

def scene_producciones(t):
    """Tarjeta Producciones Foro 7"""
    img = BG_DARK.copy()
    letterbox(img)
    fade = ease_io(1.0 - sub_t(t, 0.80, 1.0))
    a1 = ease_out(sub_t(t, 0.08, 0.34)) * fade
    a2 = ease_out(sub_t(t, 0.24, 0.50)) * fade
    a3 = ease_out(sub_t(t, 0.36, 0.60)) * fade
    a4 = ease_out(sub_t(t, 0.50, 0.72)) * fade

    gold_frame(img, sub_t(t, 0.04, 0.55), alpha=0.30, on_dark=True)
    draw_center(img, 'P  R  E  S  E  N  T  A',
                415, fSANS_XS, TAUPE, alpha=a1*0.65, shadow=False)
    ornament(img, 460, ease_out(sub_t(t, 0.18, 0.44))*fade, GOLD, 0.80)
    draw_center(img, 'Producciones',  478, fSERIF_MD, GOLD_L, alpha=a2*0.88)
    draw_center(img, 'Foro 7',        530, fSCRIPT_LG, GOLD, alpha=a3, sh_off=3)
    line_grow(img, 640, a4, GOLD_D, alpha=0.28, max_half=500)
    return img


def scene_open(t):
    """Apertura oscura dramática"""
    img = BG_DARK.copy()
    letterbox(img)
    draw = ImageDraw.Draw(img, 'RGBA')
    a_line = ease_out(sub_t(t, 0.25, 0.75)) * ease_io(1.0 - sub_t(t, 0.80, 1.0)) * 0.22
    if a_line > 0.01:
        al = int(a_line*255)
        draw.line([(W//2, H//2-180), (W//2, H//2+180)], fill=(*BLUE_L, al), width=1)
        draw.line([(W//2-120, H//2), (W//2+120, H//2)], fill=(*GOLD_D, al), width=1)
    a1 = ease_out(sub_t(t, 0.20, 0.60)) * ease_io(1.0 - sub_t(t, 0.78, 1.0))
    a2 = ease_out(sub_t(t, 0.38, 0.80)) * ease_io(1.0 - sub_t(t, 0.85, 1.0))
    if a1 > 0.01:
        draw_center(img, 'Mis XV Años',
                    H//2 - 45, fSCRIPT_MD, GOLD_L, alpha=a1*0.80, shadow=True, sh_off=3)
    if a2 > 0.01:
        draw_center(img, 'XV  *  AÑOS',
                    H//2 + 30, fLIGHT, BLUE_L, alpha=a2*0.45, shadow=False)
    return img


def scene_title(t):
    """Título principal: XV Años de Evelyn Estefanía"""
    img = BG_DARK.copy()
    add_bella(img, num=1, size=(380,380), alpha=ease_out(sub_t(t,0.0,0.50))*0.55, pos='bottom-right')
    add_bella(img, num=2, size=(280,280), alpha=ease_out(sub_t(t,0.0,0.50))*0.30, pos='bottom-left')
    img = vignette_dark(img, 0.45)
    letterbox(img)
    gold_frame(img, sub_t(t, 0.0, 0.65), alpha=0.68, on_dark=True)

    a_pre  = ease_out(sub_t(t, 0.06, 0.34))
    dy_pre = int(lerp(-14, 0, sub_t(t, 0.06, 0.34)))
    a_ln1  = ease_out(sub_t(t, 0.14, 0.40))
    a_n1   = ease_out(sub_t(t, 0.20, 0.48))
    dx_n1  = int(lerp(-85, 0, sub_t(t, 0.20, 0.48)))
    a_xv   = ease_out(sub_t(t, 0.38, 0.58))
    a_n2   = ease_out(sub_t(t, 0.44, 0.66))
    dx_n2  = int(lerp( 85, 0, sub_t(t, 0.44, 0.66)))
    a_ln2  = ease_out(sub_t(t, 0.58, 0.76))
    a_date = ease_out(sub_t(t, 0.66, 0.84))
    a_loc  = ease_out(sub_t(t, 0.74, 0.94))

    draw_center(img, 'Sus XV Años', 168+dy_pre, fITALIC, TAUPE,
                alpha=a_pre*0.86, shadow=False)
    line_grow(img, 218, a_ln1, BLUE_L, alpha=0.40, max_half=680)
    draw_center_dx(img, 'Evelyn', 232, fSCRIPT_XL, GOLD_L, alpha=a_n1, dx=dx_n1, sh_off=4)
    rose_ornament(img, 403, ease_out(sub_t(t, 0.36, 0.60)))
    draw_center(img, 'XV', 412, fSCRIPT_MD, GOLD, alpha=a_xv*0.75)
    draw_center_dx(img, 'Estefanía', 438, fSCRIPT_XL, GOLD_L, alpha=a_n2, dx=dx_n2, sh_off=4)
    line_grow(img, 585, a_ln2, BLUE_L, alpha=0.40, max_half=680)
    draw_center(img, '15  *  III  *  2026', 601, fSERIF_MD, WHITE,
                alpha=a_date*0.92)
    draw_center(img, 'León de los Aldama, Guanajuato', 651, fSANS_SM, TAUPE,
                alpha=a_loc*0.70, shadow=False)
    return img


def scene_family(t):
    """Familia: padres y madrina"""
    img = BG_DARK.copy()
    add_bella(img, num=3, size=(300,300), alpha=ease_out(sub_t(t,0.0,0.45))*0.42, pos='bottom-right')
    img = vignette_dark(img, 0.40)
    letterbox(img)
    gold_frame(img, sub_t(t, 0.0, 0.55), 0.62, on_dark=True)

    a0  = ease_out(sub_t(t, 0.04, 0.28));  dy0 = int(lerp(-12,0,sub_t(t,0.04,0.28)))
    a1  = ease_out(sub_t(t, 0.14, 0.42));  dx1 = int(lerp(-88,0,sub_t(t,0.14,0.42)))
    a2  = ease_out(sub_t(t, 0.25, 0.50));  dx2 = int(lerp(-88,0,sub_t(t,0.25,0.50)))
    a3  = ease_out(sub_t(t, 0.38, 0.60));  dx3 = int(lerp( 88,0,sub_t(t,0.38,0.60)))
    a4  = ease_out(sub_t(t, 0.50, 0.70));  dx4 = int(lerp( 88,0,sub_t(t,0.50,0.70)))
    a5  = ease_out(sub_t(t, 0.62, 0.82));  dx5 = int(lerp( 88,0,sub_t(t,0.62,0.82)))

    draw_center(img, 'Con el amor de sus padres', 158+dy0,
                fITALIC, TAUPE, alpha=a0*0.80, shadow=False)
    line_grow(img, 205, a0, BLUE_L, alpha=0.35, max_half=660)

    ornament(img, 240, ease_out(sub_t(t, 0.10, 0.38)), GOLD)
    draw_center_dx(img, 'Sus papás', 258, fSANS_SM, TAUPE,
                   alpha=a1*0.58, dx=dx1, shadow=False)
    draw_center_dx(img, 'Abril Berenice Romero García', 296,
                   fSERIF_SM, WHITE, alpha=a2, dx=dx2)
    draw_center_dx(img, '&  Luis Alberto Villa Gómez', 340,
                   fSERIF_SM, WHITE, alpha=a2*0.95, dx=dx2)

    line_grow(img, 400, ease_out(sub_t(t, 0.46, 0.64)), GOLD_D,
              alpha=0.25, max_half=520)

    ornament(img, 432, ease_out(sub_t(t, 0.48, 0.68)), ROSE_L)
    draw_center_dx(img, 'Su madrina', 450, fSANS_SM, TAUPE,
                   alpha=a3*0.58, dx=dx3, shadow=False)
    draw_center_dx(img, 'Erika Guadalupe Romero García', 488,
                   fSERIF_SM, WHITE, alpha=a4, dx=dx4)

    line_grow(img, 550, ease_out(sub_t(t, 0.62, 0.82)), BLUE_L,
              alpha=0.28, max_half=500)
    draw_center(img, 'La más bella historia de amor comienza hoy', 568,
                fITALIC_XS, ROSE_L, alpha=a5*0.65, shadow=False)
    return img


def scene_ceremony(t):
    """Ceremonia religiosa"""
    img = BG_BLUE.copy()
    add_bella(img, num=2, size=(280,280), alpha=ease_out(sub_t(t,0.0,0.42))*0.38, pos='bottom-right')
    img = vignette_dark(img, 0.50)
    letterbox(img)
    gold_frame(img, sub_t(t,0,0.55), alpha=0.70, on_dark=True)

    a1 = ease_out(sub_t(t, 0.05, 0.34)); dy1=int(lerp(-16,0,sub_t(t,0.05,0.34)))
    a2 = ease_out(sub_t(t, 0.18, 0.46))
    a3 = ease_out(sub_t(t, 0.30, 0.58))
    a4 = ease_out(sub_t(t, 0.46, 0.70))
    a5 = ease_out(sub_t(t, 0.60, 0.85))

    draw_center(img, 'Ceremonia Religiosa', 193+dy1, fSERIF_LG, GOLD_L, alpha=a1)
    rose_ornament(img, 268, ease_out(sub_t(t,0.14,0.44)), 0.85)
    draw_center(img, 'Domingo 15 de Marzo de 2026', 285, fSERIF_MD, WHITE, alpha=a2*0.92)
    draw_center(img, 'León de los Aldama, Gto.', 335, fSANS_MD, GOLD_L,
                alpha=a3*0.75, shadow=False)
    line_grow(img, 400, a4, GOLD, alpha=0.35, max_half=540)
    draw_center(img, '2 : 0 0  P M', 420, fSANS_LG, GOLD_L,
                alpha=a5*0.90, shadow=False)
    return img


def scene_reception(t):
    """Recepción — Salón Laja"""
    img = BG_DARK.copy()
    add_bella(img, num=1, size=(320,320), alpha=ease_out(sub_t(t,0.0,0.40))*0.50, pos='bottom-right')
    img = vignette_dark(img, 0.42)
    letterbox(img)
    gold_frame(img, sub_t(t,0,0.55), alpha=0.68, on_dark=True)

    a1 = ease_out(sub_t(t, 0.05, 0.34)); dy1=int(lerp(-16,0,sub_t(t,0.05,0.34)))
    a2 = ease_out(sub_t(t, 0.18, 0.46))
    a3 = ease_out(sub_t(t, 0.30, 0.58))
    a4 = ease_out(sub_t(t, 0.46, 0.70))
    a5 = ease_out(sub_t(t, 0.60, 0.85))
    a6 = ease_out(sub_t(t, 0.72, 0.92))

    draw_center(img, 'Recepción  &  Festejo', 193+dy1, fSERIF_LG, GOLD_L, alpha=a1)
    rose_ornament(img, 268, ease_out(sub_t(t,0.14,0.44)))
    draw_center(img, 'Salón de Eventos Laja', 285, fSERIF_MD, WHITE, alpha=a2*0.92)
    draw_center(img, 'Blvd. Campestre 79, Peñitas', 335, fSANS_MD, GOLD_L,
                alpha=a3*0.75, shadow=False)
    draw_center(img, 'León de los Aldama, Gto.', 375, fSANS_SM, TAUPE,
                alpha=a3*0.65, shadow=False)
    line_grow(img, 430, a4, GOLD, alpha=0.35, max_half=540)
    draw_center(img, '3 : 3 0  P M  —  recepción', 450, fSANS_MD, GOLD_L,
                alpha=a5*0.88, shadow=False)
    draw_center(img, 'Vestimenta  F O R M A L', 495, fITALIC_SM, ROSE_L,
                alpha=a6*0.72, shadow=False)
    return img


def scene_finale(t):
    """Cierre cinematográfico"""
    img = BG_DARK.copy()
    a_d = ease_out(sub_t(t, 0.0, 0.42))
    add_bella(img, num=1, size=(420,420), alpha=a_d*0.65, pos='bottom-right')
    add_bella(img, num=3, size=(300,300), alpha=a_d*0.32, pos='bottom-left')
    img = vignette_dark(img, 0.38)
    letterbox(img)
    gold_frame(img, sub_t(t, 0.0, 0.52), alpha=0.78, on_dark=True)

    a1 = ease_out(sub_t(t, 0.06, 0.38))
    a2 = ease_out(sub_t(t, 0.28, 0.56))
    a3 = ease_out(sub_t(t, 0.50, 0.72))
    a4 = ease_out(sub_t(t, 0.62, 0.82))
    a5 = ease_out(sub_t(t, 0.75, 0.95))

    line_grow(img, 202, a1, BLUE_L, alpha=0.50, max_half=690)
    draw_center(img, 'Evelyn', 216, fSCRIPT_XL, GOLD_L, alpha=a1, sh_off=4)
    rose_ornament(img, 393, ease_out(sub_t(t,0.24,0.54)))
    draw_center(img, 'XV',      397, fSCRIPT_MD, GOLD,  alpha=a2*0.70)
    draw_center(img, 'Estefanía', 422, fSCRIPT_XL, GOLD_L, alpha=a2, sh_off=4)
    line_grow(img, 566, a3, BLUE_L, alpha=0.50, max_half=690)
    draw_center(img, '15  *  III  *  2026', 582, fSERIF_MD, WHITE, alpha=a3*0.90)
    draw_center(img, 'León de los Aldama, Guanajuato', 632, fSANS_SM, TAUPE,
                alpha=a4*0.74, shadow=False)
    draw_center(img, 'Mis XV Años', 658, fSCRIPT_SM, ROSE_L,
                alpha=a5*0.62, shadow=True, sh_off=2)
    return img


def scene_fade_out(t):
    """Fundido final a negro"""
    img = BG_DARK.copy()
    a   = ease_io(1.0 - t)
    if a > 0.02:
        fin = scene_finale(1.0).convert('RGBA')
        ov  = Image.new('RGBA',(W,H),(0,0,0,int((1-a)*255)))
        fin.paste(ov, mask=ov.split()[3])
        img.paste(fin.convert('RGB'))
    return img


# ──────────────────────────────────────────────
# SECUENCIA COMPLETA
# ──────────────────────────────────────────────
SCENES = [
    (scene_producciones,    8.0, False),   # 1.  Foro 7
    (scene_open,            3.5, False),   # 2.  Apertura
    (scene_title,          14.0, True ),   # 3.  Título principal
    (_bella_scenes[0],     11.0, True ),   # 4.  bella 1 — Ken Burns
    (_bella_scenes[1],     11.0, True ),   # 5.  bella 2 — Ken Burns
    (_bella_scenes[2],     11.0, True ),   # 6.  bella 3 — Ken Burns
    (scene_family,         12.0, True ),   # 7.  Familia & Madrina
    (scene_ceremony,        8.0, True ),   # 8.  Ceremonia
    (scene_reception,       8.0, True ),   # 9.  Recepción / Salón Laja
    (scene_finale,         13.0, True ),   # 10. Cierre cinematográfico
    (scene_fade_out,        3.5, False),   # 11. Fundido a negro
]

FADE_F    = int(0.85 * FPS)
total_dur = sum(d for _,d,_ in SCENES)
total_frm = int(total_dur * FPS)
mins = int(total_dur)//60; secs = int(total_dur)%60
print(f'\nVideo: {total_dur:.1f}s ({mins}:{secs:02d} min)  |  {total_frm} frames  |  {W}x{H} @ {FPS}fps')
print(f'Salida: {OUTPUT}\n')

# ──────────────────────────────────────────────
# PIPE A FFMPEG
# ──────────────────────────────────────────────
cmd = [
    'ffmpeg', '-y',
    '-f','rawvideo','-vcodec','rawvideo',
    '-s',f'{W}x{H}','-pix_fmt','rgba','-r',str(FPS),'-i','pipe:0',
] + (['-i', MUSICA] if MUSICA else []) + [
    '-vf','format=yuv420p',
    '-vcodec','libx264','-preset','medium','-crf','17',
    '-profile:v','high','-movflags','+faststart',
] + ([
    '-c:a','aac','-b:a','192k',
    '-af', f'afade=t=out:st={total_dur-3.0:.1f}:d=3.0',
    '-shortest',
] if MUSICA else ['-an']) + [OUTPUT]

proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

fn = 0
for si, (scene_fn, dur, has_fade) in enumerate(SCENES):
    n     = int(dur * FPS)
    label = getattr(scene_fn, '__name__', f'foto_{si-2}')
    for f in range(n):
        t     = f / max(1, n-1)
        frame = scene_fn(t).convert('RGBA')

        if has_fade and f < FADE_F:
            fi = f / FADE_F
            ov = Image.new('RGBA',(W,H),(0,0,0,int((1-ease_out(fi))*255)))
            frame.paste(ov, mask=ov.split()[3])

        if si < len(SCENES)-1 and f >= n-FADE_F:
            fo = (f-(n-FADE_F)) / FADE_F
            ov = Image.new('RGBA',(W,H),(0,0,0,int(ease_io(fo)*255)))
            frame.paste(ov, mask=ov.split()[3])

        proc.stdin.write(frame.convert('RGBA').tobytes())
        fn += 1

        if fn % FPS == 0:
            pct = fn/total_frm*100
            m = fn//FPS//60; s=(fn//FPS)%60
            print(f'  [{pct:5.1f}%] {m:02d}:{s:02d}  '
                  f'Escena {si+1}/{len(SCENES)}: {label}   ',
                  end='\r', flush=True)

proc.stdin.close()
ret = proc.wait()

if ret == 0:
    sz = os.path.getsize(OUTPUT)/1024/1024
    print(f'\n\n✅ VIDEO LISTO!')
    print(f'   {OUTPUT}')
    print(f'   {sz:.1f} MB  |  {total_dur:.0f}s ({mins}:{secs:02d} min)  |  1920x1080')
    if not MUSICA:
        print(f'\n💡 Para agregar música:')
        print(f'   ffmpeg -i invitacion_evelyn_xv.mp4 -i musica.mp3 \\')
        print(f'          -c:v copy -shortest -map 0:v -map 1:a evelyn_con_musica.mp4')
else:
    print(f'\n❌ Error FFmpeg (código {ret})')
    print(f'   Verifica que ffmpeg esté instalado: ffmpeg -version')
