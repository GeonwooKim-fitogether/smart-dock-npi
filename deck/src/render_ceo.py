import os, ssl, sys, hashlib, urllib.request, json
from playwright.sync_api import sync_playwright

SCR = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(SCR, 'smart-dock-slide-asis-tobe.html')
CACHE = os.path.join(SCR, '_fontcache')
os.makedirs(CACHE, exist_ok=True)
_CA = '/root/.ccr/ca-bundle.crt'  # 클라우드 세션의 프록시 인증서. 없으면 시스템 기본값
ctx_ssl = ssl.create_default_context(cafile=_CA) if os.path.exists(_CA) else ssl.create_default_context()
UA = None

def fetch(url, ua):
    key = hashlib.sha1((url + ua).encode()).hexdigest()
    p = os.path.join(CACHE, key)
    if os.path.exists(p):
        with open(p, 'rb') as f:
            data = f.read()
        with open(p + '.ct') as f:
            ct = f.read()
        return data, ct
    req = urllib.request.Request(url, headers={'User-Agent': ua})
    with urllib.request.urlopen(req, context=ctx_ssl, timeout=30) as r:
        data = r.read(); ct = r.headers.get('Content-Type', 'application/octet-stream')
    with open(p, 'wb') as f: f.write(data)
    with open(p + '.ct', 'w') as f: f.write(ct)
    return data, ct

def handler(route, request):
    try:
        data, ct = fetch(request.url, request.headers.get('user-agent', 'Mozilla/5.0'))
        route.fulfill(status=200, body=data, headers={'Content-Type': ct, 'Access-Control-Allow-Origin': '*'})
    except Exception as e:
        print('font fetch fail', request.url[:80], e, file=sys.stderr)
        route.abort()

CHECK = r"""
() => {
  const out = [];
  document.querySelectorAll('.slide').forEach(s => {
    const sr = s.getBoundingClientRect();
    const scale = sr.width / 1280;
    const ft = s.querySelector('.ft');
    const limit = ft ? (ft.getBoundingClientRect().top - sr.top) / scale - 8 : 700;
    let maxBottom = 0, over = [];
    s.querySelectorAll('.body *, .msg, h1').forEach(el => {
      const r = el.getBoundingClientRect();
      if (!r.width && !r.height) return;
      const b = (r.bottom - sr.top) / scale, rt = (r.right - sr.left) / scale;
      if (b > maxBottom) maxBottom = b;
      if (rt > 1280 - 56 + 1) over.push(el.tagName + '.' + el.className + ' right=' + rt.toFixed(0));
    });
    // text overflow inside cells / boxes
    const clip = [];
    s.querySelectorAll('td, th, li, p, div').forEach(el => {
      if (el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflow !== 'visible') clip.push(el.className);
    });
    out.push({id: s.id, bodyBottom: +maxBottom.toFixed(0), limit: +limit.toFixed(0), overflowRight: over.slice(0,5), clip: clip.slice(0,5), msgH: s.querySelector('.msg') ? +(s.querySelector('.msg').getBoundingClientRect().height/scale).toFixed(0) : null});
  });
  return out;
}
"""

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=None)
        errors = []
        def shoot(width, scheme, prefix, per_slide, full=False):
            pg = b.new_page(viewport={'width': width, 'height': 900}, device_scale_factor=1 if width > 800 else 2)
            pg.on('pageerror', lambda e: errors.append(str(e)))
            pg.route('**/fonts.googleapis.com/**', handler)
            pg.route('**/fonts.gstatic.com/**', handler)
            pg.emulate_media(color_scheme=scheme)
            pg.goto('file://' + HTML)
            pg.wait_for_load_state('networkidle')
            pg.evaluate('document.fonts.ready')
            pg.wait_for_timeout(300)
            fam = pg.evaluate("document.fonts.check('700 16px \"Noto Sans KR\"')")
            info = pg.evaluate(CHECK)
            sw = pg.evaluate('[document.documentElement.scrollWidth, window.innerWidth]')
            if per_slide:
                for i, el in enumerate(pg.query_selector_all('.frame')):
                    el.screenshot(path=os.path.join(SCR, f'{prefix}{i}.png'))
            if full:
                pg.screenshot(path=os.path.join(SCR, f'{prefix}full.png'), full_page=True)
            pg.close()
            return fam, info, sw
        if mode in ('all', 'desk'):
            fam, info, sw = shoot(1440, 'light', 'ceo_s', True)
            print('desktop light font ok:', fam, 'scroll', sw)
            for r in info: print(json.dumps(r, ensure_ascii=False))
        if mode in ('all', 'dark'):
            fam, info, sw = shoot(1440, 'dark', 'ceo_dark_s', True)
            print('dark font ok:', fam, 'scroll', sw)
        if mode in ('all', 'phone'):
            fam, info, sw = shoot(390, 'light', 'ceo_phone_', False, full=True)
            print('phone font ok:', fam, 'scroll', sw)
        print('pageerrors:', errors)
        b.close()

main()
