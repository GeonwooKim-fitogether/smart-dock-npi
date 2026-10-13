src = open('render_ceo.py', encoding='utf-8').read().replace('\nmain()', '\n')
ns = {'__file__': 'render_ceo.py', '__name__': 'pdf'}
exec(src, ns)
from playwright.sync_api import sync_playwright
PRINT_CSS = """
@page { size: 1280px 720px; margin: 0; }
:root { --s: 1 !important; }
html, body { margin: 0 !important; padding: 0 !important; background: #fff !important; }
.deck { max-width: none !important; padding: 0 !important; margin: 0 !important; display: block !important; }
.frame { width: 1280px !important; height: 720px !important; aspect-ratio: auto !important; box-shadow: none !important;
         break-after: page; page-break-after: always; }
.frame:last-child { break-after: auto; page-break-after: auto; }
"""
import sys, os
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'exports', 'SmartDock_기획.pdf')
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1280, 'height': 720}, color_scheme='light')
    pg.route('**/fonts.googleapis.com/**', ns['handler']); pg.route('**/fonts.gstatic.com/**', ns['handler'])
    pg.goto('file://' + ns['HTML'], timeout=90000)
    pg.evaluate('document.fonts.ready.then(() => true)')
    pg.wait_for_timeout(1500)
    pg.add_style_tag(content=PRINT_CSS)
    pg.emulate_media(media='print', color_scheme='light')
    pg.wait_for_timeout(500)
    print('fonts:', pg.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family).filter((v,i,a)=>a.indexOf(v)===i)"))
    pg.pdf(path=OUT, width='1280px', height='720px', print_background=True, margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
    b.close()
print('saved', OUT)
