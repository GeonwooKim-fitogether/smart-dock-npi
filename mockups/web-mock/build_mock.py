# 시안 조립: 어두운 색 토큰(DataManager 색)을 두 자리에 넣고, Dock 제품 사진을 data URI로 박는다
import base64, pathlib
D = pathlib.Path(__file__).parent
IMG = pathlib.Path(__file__).resolve().parent / 'dock-x.png'
DARK = """
    --page:#151515; --frame:#000000; --chrome:#0E0E0E; --chrome-ink:#8A8A8A; --chrome-field:#1E1E1E; --chrome-text:#D6D6D6;
    --hdr:#F2F2F2; --hdr-ink:#1E1E1E; --hdr-ink-2:#9A9A9A; --hdr-line:#E2E2E2; --crest:#C4C4C4; --hdr-ok:#1C8E98; --hdr-warn:#A8690F;
    --logo:#3A3A3A; --logo-ink:#FFFFFF;
    --rail:#2E2E2E; --rail-ink:#A8A8A8; --rail-on:#252525; --rail-line:#3A3A3A;
    --main:#262626; --ink:#FFFFFF; --ink-2:#C8C8C8; --ink-3:#8C8C8C;
    --card:#333333; --card-line:#333333; --card-shadow:0 0 0 0 transparent;
    --next-ink:#8C8C8C; --next-line:#4E4E4E;
    --all:#141414; --all-ink:#FFFFFF; --all-ink-2:#8C8C8C;
    --cell-fill:#323232; --cell-line:#6A6A6A; --cell-line-2:#4A4A4A; --cell-ink:#F0F0F0; --cell-ink-2:#9A9A9A; --cell-empty:#666666;
    --shelf:#666666;
    --fault:#FF6B5B; --fault-bg:#3A2320; --warn:#F2B34A; --warn-bg:#382E1C; --info-bg:#203235;
    --c-up:#2DBFCB; --c-up-ink:#4FD3DE; --c-hr:#FF5C74; --c-hr-ink:#FF7D91;
    --c-ssid:#F2A93B; --c-ssid-ink:#F7BE63; --c-fw:#A07BEA; --c-fw-ink:#B999F2; --c-dock:#7FA8E0; --c-dock-ink:#9DBEEB;
    --on-acc:#161616;
    --a-ink:#E8E8E8; --a-ink-2:#B0B0B0; --a-ink-3:#7E7E7E; --a-line:#333333; --a-pill:#222222;
    --shade:rgba(0,0,0,.6); --sheet:#2A2A2A; --field:#262626;
    color-scheme:dark;
  """
src = (D / 'template.html').read_text(encoding='utf-8')
out = src.replace('__DARK__', DARK).replace('__DOCK_IMG__', 'data:image/png;base64,' + base64.b64encode(IMG.read_bytes()).decode())
assert '__' not in out.replace('__proto__', ''), 'placeholder left'
(D.parent / 'smart-dock-web-mock.html').write_text(out, encoding='utf-8')
print('ok', len(out))
