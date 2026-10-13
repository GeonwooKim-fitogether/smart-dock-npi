import pathlib, sys
from playwright.sync_api import sync_playwright
P = pathlib.Path('smart-dock-web-mock.html').resolve().as_uri()
errs = []
def page(b, w, h, scheme='dark'):
    ctx = b.new_context(viewport={'width': w, 'height': h}, color_scheme=scheme, device_scale_factor=1)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'fonts' not in m.text and 'ERR_' not in m.text else None)
    pg.goto(P); pg.wait_for_timeout(300)
    return pg
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = page(b, 1440, 1000)
    pg.screenshot(path='shots/d1-idle.png', full_page=False)
    pg.click('#b-up-start'); pg.wait_for_timeout(2600)
    pg.screenshot(path='shots/d2-running.png')
    pg.wait_for_timeout(33000)
    pg.screenshot(path='shots/d3-attention.png')
    pg.click('#b-up-files'); pg.wait_for_timeout(1800)
    pg.click('#c-net'); pg.wait_for_timeout(9000)
    pg.screenshot(path='shots/d4-done.png')
    pg.click('#nav-hr'); pg.click('#b-hr-start'); pg.wait_for_timeout(300); pg.screenshot(path='shots/d5-hr-ready.png')
    pg.click('#b-hr-task'); pg.wait_for_timeout(1500); pg.screenshot(path='shots/d6-hr-run.png')
    pg.click('#nav-fw'); pg.click('#c-power'); pg.click('#b-fw-start'); pg.wait_for_timeout(300); pg.screenshot(path='shots/d7-fw-battery.png')
    pg.click('#nav-dock'); pg.wait_for_timeout(300); pg.screenshot(path='shots/d8-dock.png')
    pg.click('#nav-upload'); pg.click('.slot[data-slot="3"]'); pg.wait_for_timeout(300); pg.screenshot(path='shots/d9-sheet.png')
    pg.keyboard.press('Escape')
    # 밝은 색
    pg.click('#c-theme'); pg.click('#c-reset'); pg.wait_for_timeout(200); pg.screenshot(path='shots/l1-idle.png')
    pg.click('#b-up-start'); pg.wait_for_timeout(9000); pg.screenshot(path='shots/l2-running.png')
    pg.click('#c-theme')
    # 휴대폰
    m = page(b, 390, 844)
    m.evaluate("localStorage.clear()"); m.reload(); m.wait_for_timeout(300)
    m.screenshot(path='shots/m1-idle.png')
    m.click('#b-up-start'); m.wait_for_timeout(9000); m.screenshot(path='shots/m2-running.png', full_page=True)
    m.click('#nav-fw'); m.wait_for_timeout(200); m.screenshot(path='shots/m3-fw.png')
    # 노트북에서 휴대폰 폭 미리보기
    pg.click('#c-width'); pg.click('#c-reset'); pg.wait_for_timeout(300); pg.screenshot(path='shots/d10-phonepreview.png')
    # 가로 넘침 검사
    for name, q in (('desk', pg), ('phone', m)):
        sw = q.evaluate("document.documentElement.scrollWidth"); cw = q.evaluate("document.documentElement.clientWidth")
        print(name, 'scrollWidth', sw, 'clientWidth', cw)
    b.close()
print('errors:', errs)
