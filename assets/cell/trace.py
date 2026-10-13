import base64, json
from playwright.sync_api import sync_playwright
b64 = base64.b64encode(open('cell/cell-x.png','rb').read()).decode()
html = '<canvas id=c width=1000 height=1000></canvas>'
js = """
async (src) => {
  const img = new Image(); img.src = src; await img.decode();
  const c = document.getElementById('c'); const x = c.getContext('2d');
  x.drawImage(img, 0, 0); const d = x.getImageData(0,0,1000,1000).data;
  const lum = (i) => 0.299*d[i]+0.587*d[i+1]+0.114*d[i+2];
  const rows = [];
  for (let y=0; y<1000; y++) {
    let L=-1, R=-1;
    for (let xx=0; xx<1000; xx++) { const i=(y*1000+xx)*4; if (lum(i) < 110) { if (L<0) L=xx; R=xx; } }
    rows.push([L,R]);
  }
  // inner window: pixels in top region notably lighter than body (window is dark grey ~ #2a2a2a vs body ~#141414?)
  const prof = [];
  for (let y=180; y<500; y+=2) { const r=[]; for (let xx=320; xx<680; xx+=2) { r.push(Math.round(lum((y*1000+xx)*4))); } prof.push(r); }
  return {rows, prof};
}
"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.set_content(html)
    res = pg.evaluate(js, 'data:image/png;base64,'+b64)
    b.close()
json.dump(res, open('cell/trace.json','w'))
rows = res['rows']
ys = [y for y,(L,R) in enumerate(rows) if L>=0 and R-L>40]
print('top', ys[0], 'bottom', ys[-1])
for y in range(ys[0], ys[-1]+1, 20):
    print(y, rows[y])
