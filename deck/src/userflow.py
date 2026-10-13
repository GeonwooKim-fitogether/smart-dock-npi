# 신규 6쪽: 스마트폰 사용자 플로우 (개선 B) — deck_v24.py 결과물에 끼워 넣고 뒤쪽 번호를 하나씩 민다
import re
P = 'smart-dock-slide-asis-tobe.html'
s = open(P, encoding='utf-8').read()


def tx(x, y, t, cls='', anchor='start', size=None, extra=''):
    st = f' style="font-size:{size}px"' if size else ''
    c = f' class="{cls}"' if cls else ''
    return f'<text{c} x="{x:g}" y="{y:g}" text-anchor="{anchor}" dominant-baseline="central"{st}{extra}>{t}</text>'


PW_, PH_ = 76, 146          # 휴대폰 외곽
SX, SY, SW, SH = 4, 12, 68, 128   # 화면 (휴대폰 기준 상대 좌표)


def phone(x, y, pill, body):
    g = [f'<g transform="translate({x:g},{y:g})">',
         f'<rect x="0" y="0" width="{PW_}" height="{PH_}" rx="12" fill="var(--frame)" stroke="var(--ink)" stroke-width="1.3"/>',
         f'<rect x="{PW_ / 2 - 10:g}" y="4" width="20" height="4" rx="2" fill="var(--faint)"/>',
         f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="5" fill="var(--box)" stroke="var(--line)" stroke-width="1"/>']
    kind, label = pill
    if kind == 'hot':
        g.append(f'<rect x="{SX + 4}" y="{SY + 4}" width="{SW - 8}" height="13" rx="6.5" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.3"/>')
        g.append(tx(PW_ / 2, SY + 10.5, label, 'tac', 'middle', 7))
    elif kind == 'wifi':
        g.append(f'<rect x="{SX + 4}" y="{SY + 4}" width="{SW - 8}" height="13" rx="6.5" fill="var(--box)" stroke="var(--accent-line)" stroke-width="1"/>')
        g.append(tx(PW_ / 2, SY + 10.5, label, '', 'middle', None, ' style="font-size:7px;fill:var(--accent)"'))
    else:
        g.append(f'<rect x="{SX + 4}" y="{SY + 4}" width="{SW - 8}" height="13" rx="6.5" fill="var(--frame)" stroke="var(--line)" stroke-width="1"/>')
        g.append(tx(PW_ / 2, SY + 10.5, label, 'ts', 'middle', 7))
    g += body
    g.append('</g>')
    return '\n'.join(g)


# 화면 부품 (휴대폰 기준 좌표)
L0, R0 = SX + 5, SX + SW - 5


def title(y, t, size=8.5):
    return tx(L0, y, t, 'tb', 'start', size)


def small(y, t, cls='ts', anchor='start', x=None):
    return tx(L0 if x is None else x, y, t, cls, anchor, 7)


def field(y, t, h=13, ac=False):
    st = 'fill="var(--accent-tint)" stroke="var(--accent-line)"' if ac else 'fill="var(--frame)" stroke="var(--line)"'
    return f'<rect x="{L0 - 1}" y="{y}" width="{R0 - L0 + 2}" height="{h}" rx="2" {st} stroke-width="1"/>' + tx(L0 + 3, y + h / 2, t, 'tac' if ac else '', 'start', 7)


def button(y, t, h=12):
    return (f'<rect x="{L0 - 1}" y="{y}" width="{R0 - L0 + 2}" height="{h}" rx="3" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.2"/>'
            + tx(PW_ / 2, y + h / 2, t, 'tac', 'middle', 7.5))


def toggle(y, t, on=True):
    tx_ = small(y, t)
    if on:
        tg = (f'<rect x="{R0 - 15}" y="{y - 4.5}" width="15" height="9" rx="4.5" fill="var(--accent-line)"/>'
              f'<circle cx="{R0 - 4.5}" cy="{y}" r="3.2" fill="var(--box)"/>')
    else:
        tg = (f'<rect x="{R0 - 15}" y="{y - 4.5}" width="15" height="9" rx="4.5" fill="var(--line)"/>'
              f'<circle cx="{R0 - 10.5}" cy="{y}" r="3.2" fill="var(--box)"/>')
    return tx_ + tg


def addr(y=SY + 21):
    return (f'<rect x="{L0 - 1}" y="{y}" width="{R0 - L0 + 2}" height="11" rx="5.5" fill="var(--frame)" stroke="var(--line)" stroke-width="1"/>'
            + tx(PW_ / 2, y + 5.5, 'smartdock.local', 'ts', 'middle', 6.5))


def grid(y0, fail=(), cols=6, rows=4, dx=9.4, dy=15, cw=7.6, ch=12.6):
    out = []
    for r in range(rows):
        for c in range(cols):
            x = L0 + 0.5 + c * dx
            y = y0 + r * dy
            out.append(f'<use href="#cell-x-sm" class="cx" x="{x:g}" y="{y:g}" width="{cw:g}" height="{ch:g}"/>')
            if (r, c) in fail:
                out.append(tx(x + cw / 2, y + ch / 2, '✕', 'tb', 'middle', 7))
    return ''.join(out)


SCR = {
    'wifi_list': [
        title(SY + 28, 'Wi-Fi'),
        field(SY + 36, 'SmartDock-01  ✓', ac=True),
        small(SY + 57, 'Office'), small(SY + 70, 'Guest'),
        f'<line x1="{L0}" y1="{SY + 63.5}" x2="{R0}" y2="{SY + 63.5}" stroke="var(--line)"/>',
        small(SY + 86, '비밀번호'),
        field(SY + 92, '••••••••'),
        button(SY + 111, '연결'),
    ],
    'browser_home': [
        addr(),
        title(SY + 43, 'Smart Dock'),
        grid(SY + 51),
        button(SY + 113, '홈 화면에 추가'),
    ],
    'hot_register': [
        addr(),
        title(SY + 43, '핫스팟 등록', 8),
        small(SY + 55, '이름'),
        field(SY + 60, '김코치의 iPhone'),
        small(SY + 81, '비밀번호'),
        field(SY + 86, '••••••'),
        button(SY + 109, '저장'),
    ],
    'dock_home': [
        addr(),
        title(SY + 43, 'Smart Dock'),
        grid(SY + 53, dy=14, cw=7, ch=11.6),
        button(SY + 113, 'START'),
    ],
    'extract': [
        addr(),
        title(SY + 43, '추출 18 / 24'),
        f'<rect x="{L0}" y="{SY + 50}" width="{R0 - L0}" height="4" rx="2" fill="var(--line)"/>',
        f'<rect x="{L0}" y="{SY + 50}" width="{(R0 - L0) * .75:g}" height="4" rx="2" fill="var(--accent-line)"/>',
        grid(SY + 58, fail={(1, 4), (3, 1)}, dy=13.5, cw=7, ch=11.6),
        toggle(SY + 118, '자동 업로드'),
    ],
    'hot_on': [
        title(SY + 29, '개인용 핫스팟', 8),
        toggle(SY + 44, '연결 허용'),
        small(SY + 58, 'Wi-Fi 암호 ••••'),
        field(SY + 70, '연결된 기기 0', h=15),
    ],
    'hot_joined': [
        title(SY + 29, '개인용 핫스팟', 8),
        toggle(SY + 44, '연결 허용'),
        small(SY + 58, 'Wi-Fi 암호 ••••'),
        field(SY + 70, '연결된 기기 1', h=15, ac=True),
    ],
    'uploading': [
        f'<rect x="{L0 - 2}" y="{SY + 22}" width="{R0 - L0 + 4}" height="72" rx="3" fill="none" stroke="var(--accent)" stroke-width="1" stroke-dasharray="3 2"/>',
        f'<rect x="{L0 + 1}" y="{SY + 26}" width="{R0 - L0 - 2}" height="10" rx="5" fill="var(--frame)" stroke="var(--line)" stroke-width="1"/>',
        tx(PW_ / 2, SY + 31, 'smartdock.local', 'ts', 'middle', 6),
        small(SY + 46, '업로드 12 / 24', 'tac', 'middle', PW_ / 2),
        f'<rect x="{L0 + 3}" y="{SY + 54}" width="{R0 - L0 - 6}" height="4" rx="2" fill="var(--line)"/>',
        f'<rect x="{L0 + 3}" y="{SY + 54}" width="{(R0 - L0 - 6) * .5:g}" height="4" rx="2" fill="var(--accent-line)"/>',
        small(SY + 70, '⑧ 되면 보임', 'ts', 'middle', PW_ / 2), small(SY + 82, '(확인 필요)', 'ts', 'middle', PW_ / 2),
        small(SY + 108, '안 되면 화면 없음', 'ts', 'middle', PW_ / 2),
    ],
    'hot_off': [
        title(SY + 29, '개인용 핫스팟', 8),
        toggle(SY + 44, '연결 허용', on=False),
        field(SY + 60, '연결된 기기 0', h=15),
    ],
}


def caption(x, y, lines, conf):
    out = [tx(x, y + 8, lines[0], 'tb', 'start', 10.5)]
    yy = y + 25
    for t in lines[1:]:
        out.append(tx(x, yy, t, 'ts', 'start', 9)); yy += 13
    if conf:
        out.append(tx(x, yy + 4, conf, 'tac', 'start', 9))
    return '\n'.join(out)


SRC = {'web': ('Dock 웹 화면 (SBC)', True), 'os': ('폰 기본 설정 화면', False), 'led': ('Dock 표시등 (본체)', False)}


def src_chip(x, y, key):
    t, ac = SRC[key]
    w = sum(8.6 if '\uac00' <= ch <= '\ud7a3' else 2.6 if ch in ' ·' else 5 for ch in t) + 12
    if ac:
        r = f'<rect x="{x}" y="{y}" width="{w:.1f}" height="16" rx="3" fill="var(--accent-tint)" stroke="var(--accent-line)" stroke-width="1"/>'
        return r + tx(x + 6, y + 8, t, 'tac', 'start', 9)
    r = f'<rect x="{x}" y="{y}" width="{w:.1f}" height="16" rx="3" fill="var(--frame)" stroke="var(--line)" stroke-width="1"/>'
    return r + tx(x + 6, y + 8, t, 'tb', 'start', 9)


def badge(x, y, t, w):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="18" rx="3" fill="var(--accent-tint)" stroke="var(--accent-line)" stroke-width="1.2"/>'
            + tx(x + w / 2, y + 9, t, 'tac', 'middle', 11))


def act_chip(x, y, act):
    if act:
        return (f'<rect x="{x}" y="{y + 1}" width="34" height="16" rx="8" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.2"/>'
                + tx(x + 17, y + 9, '조작', 'tac', 'middle', 9))
    return (f'<rect x="{x}" y="{y + 1}" width="34" height="16" rx="8" fill="none" stroke="var(--faint)" stroke-width="1" stroke-dasharray="3 2"/>'
            + tx(x + 17, y + 9, '대기', 'ts', 'middle', 9))


def arrow(x1, x2, y):
    return f'<path class="ln" d="M{x1:g},{y:g} H{x2:g}" stroke-width="1.4" marker-end="url(#uf-a)"/>'


DEFS = ('<defs><marker id="uf-a" viewBox="0 0 8 8" refX="7.5" refY="4" markerWidth="6" markerHeight="6" orient="auto">'
        '<path class="ah" d="M0,0 L8,4 L0,8 z"/></marker></defs>')

# ── A. 최초 1회 ──
A_H = 170
a = [f'<svg class="dg" width="1168" height="{A_H}" viewBox="0 0 1168 {A_H}" role="img" aria-label="최초 1회 등록 3단계와 접속 정보 2가지">', DEFS]
A_CW, A_AG = 188, 18
A_STEPS = [
    ('가', 'Dock Wi-Fi 접속', ('off', '연결 전'), 'wifi_list',
     ['설정 > Wi-Fi', 'SmartDock-01 선택', '비밀번호 입력', '(Dock 라벨 표기)'], '폰이 기억', 'os',
     ["Android: '인터넷 없음'", "→ '연결 유지' 선택"]),
    ('나', 'Dock 화면 열기', ('wifi', 'Dock Wi-Fi 연결'), 'browser_home',
     ['브라우저 주소창에', 'smartdock.local 입력', '홈 화면에 추가'], 'Dock 아이콘 생김', 'web',
     ['앱 설치 없음', '(북마크 아이콘)']),
    ('다', '핫스팟 정보 등록', ('wifi', 'Dock Wi-Fi 연결'), 'hot_register',
     ['Dock 메뉴 > 핫스팟', '폰 핫스팟 이름·', '비밀번호 입력 · 저장'], 'Dock이 기억', 'web', []),
]
for i, (b, t, pill, scr, lines, conf, src, extra) in enumerate(A_STEPS):
    x = i * (A_CW + A_AG)
    a.append(badge(x, 0, b, 22))
    a.append(tx(x + 30, 9, t, 'tb', 'start', 11.5))
    a.append(phone(x, 24, pill, SCR[scr]))
    # 설명 (제목은 배지 옆에 이미 있으므로 모두 보통 글씨)
    yy = 40
    for ln in lines:
        a.append(tx(x + PW_ + 9, yy, ln, 'ts', 'start', 9)); yy += 13
    a.append(tx(x + PW_ + 9, yy + 5, '확인: ' + conf, 'tac', 'start', 9))
    yy += 24
    for ln in extra:
        a.append(tx(x + PW_ + 9, yy, ln, 'ts', 'start', 8.5)); yy += 12
    a.append(src_chip(x + PW_ + 9, 150, src))
    if i < 2:
        a.append(arrow(x + A_CW - 4, x + A_CW + A_AG - 3, 128))

# 접속 정보 2가지 (오른쪽)
IX = 3 * (A_CW + A_AG) + 8
a.append(f'<line x1="{IX - 14}" y1="4" x2="{IX - 14}" y2="{A_H - 4}" stroke="var(--line)" stroke-width="1"/>')
a.append(tx(IX, 9, '접속 정보 2가지 = 이름 + 비밀번호 한 쌍', 'tb', 'start', 11.5))
cols = [(IX, 150, '접속 정보'), (IX + 162, 104, '정하는 쪽'), (IX + 290, 150, '저장하는 쪽'), (IX + 452, 1168 - IX - 452, '쓰는 단계')]
for cx, cw, h in cols:
    a.append(tx(cx + 2, 32, h, 'ts', 'start', None, ' style="font-size:9.5px;font-weight:700"'))
a.append(f'<line x1="{IX}" y1="41" x2="1168" y2="41" stroke="var(--line)" stroke-width="1"/>')
ROWS = [
    (50, 'Dock Wi-Fi 정보', '예: SmartDock-01', 'Dock', '(라벨 표기)', ['코치 폰 (가)', '셀 24개 (USB · E1·E2)'], '① ② ⑥'),
    (108, '핫스팟 정보', '예: 김코치의 iPhone', '코치', '(폰 핫스팟 설정)', ['Dock (다)'], '④ ⑤'),
]
for y, k1, k2, d1, d2, st, use in ROWS:
    a.append(f'<rect class="bx ac" x="{IX}" y="{y}" width="150" height="44" rx="3"/>')
    a.append(tx(IX + 75, y + 15, k1, 'tac', 'middle', 11))
    a.append(tx(IX + 75, y + 31, k2, 'ts', 'middle', 9))
    a.append(arrow(IX + 152, IX + 160, y + 22))
    a.append(f'<rect class="bx" x="{IX + 162}" y="{y}" width="104" height="44" rx="3"/>')
    a.append(tx(IX + 214, y + 15, d1, 'tb', 'middle', 11))
    a.append(tx(IX + 214, y + 31, d2, 'ts', 'middle', 9))
    a.append(arrow(IX + 268, IX + 288, y + 22))
    a.append(f'<rect class="bx" x="{IX + 290}" y="{y}" width="150" height="44" rx="3"/>')
    if len(st) == 2:
        a.append(tx(IX + 365, y + 15, st[0], 'tb', 'middle', 10.5))
        a.append(tx(IX + 365, y + 31, st[1], 'ts', 'middle', 9))
    else:
        a.append(tx(IX + 365, y + 22, st[0], 'tb', 'middle', 11))
    a.append(tx(IX + 452 + 2, y + 22, use, 'tac', 'start', 11))
a.append(tx(IX, 164, '폰은 Dock Wi-Fi의 손님 · 핫스팟의 주인 → 둘을 동시에 못 함 (③ 전환의 이유)', 'ts', 'start', 9))
a.append('</svg>')

# ── B. 매 경기 ──
B_H = 176
b = [f'<svg class="dg" width="1168" height="{B_H}" viewBox="0 0 1168 {B_H}" role="img" aria-label="매 경기 6단계 스마트폰 화면과 코치 조작">', DEFS]
B_AG = 14
B_CW = (1168 - 5 * B_AG) / 6
B_STEPS = [
    ('① 준비', True, ('wifi', 'Dock Wi-Fi 연결'), 'dock_home', ['Dock 아이콘 누름', 'Wi-Fi 자동 연결', '(가에서 기억)'], '확인: 24칸 거치', 'web'),
    ('② 추출', True, ('wifi', 'Dock Wi-Fi 연결'), 'extract', ['START 누름', '약 10분 수신', '실패 칸 재시도'], '확인: 자동 업로드 ON', 'web'),
    ('③ 전환', True, ('hot', '핫스팟 켜짐'), 'hot_on', ['핫스팟 켬', 'Dock 웹 화면 멈춤 = 정상', 'Dock 접속까지', '이 설정 화면 유지'], '', 'os'),
    ('④ 접속', False, ('hot', '핫스팟 · 기기 1'), 'hot_joined', ['조작 없음', 'Dock이 저장된', '핫스팟 정보로 접속'], '확인: 연결된 기기 1', 'os'),
    ('⑤ 업로드', False, ('hot', '핫스팟 · 기기 1'), 'uploading', ['폰을 Dock 옆에', '핫스팟 유지 · 약 20분', '셀룰러 약 3 GB'], '확인: 표시등 업로드 중', 'led'),
    ('⑥ 완료', True, ('off', '핫스팟 꺼짐'), 'hot_off', ['핫스팟 끔', "표시등 '완료' 뒤", 'Dock은 충전 대기'], '확인: 연결된 기기 0', 'os'),
]
for i, (st, act, pill, scr, lines, conf, src) in enumerate(B_STEPS):
    x = i * (B_CW + B_AG)
    bw = 62 if len(st) > 4 else 54
    b.append(badge(x, 0, st, bw))
    b.append(act_chip(x + bw + 6, 0, act))
    b.append(phone(x, 26, pill, SCR[scr]))
    b.append(caption(x + PW_ + 8, 30, lines, conf))
    b.append(src_chip(x + PW_ + 8, 154, src))
    if i < 5:
        b.append(arrow(x + B_CW - 2, x + B_CW + B_AG - 2, 99))
b.append('</svg>')

page = f'''<!-- 6. 스마트폰 사용자 플로우 -->
<div class="frame">
<section class="slide" id="s4u">
  <header class="hd"><h1><span class="no">6.</span>스마트폰 사용자 플로우 (개선 B · 코치 기준)</h1></header>
  <p class="msg">접속 정보는 최초 1회만 등록하고, 매 경기 코치 조작은 화면 열기 · START · 핫스팟 켜기 · 끄기 4회로 한정함</p>
  <div class="body" style="margin-top:14px">
    <p class="sec">최초 1회<span class="note">(설치일 · 폰 교체 · 핫스팟 비밀번호 변경 시)</span></p>
    {chr(10).join(a)}
    <p class="sec" style="margin-top:12px">매 경기<span class="note">(5쪽 ①~⑥ · 조작 4회 · 대기 2회)</span></p>
    {chr(10).join(b)}
    <div class="kw" style="margin-top:6px">
      <p><span class="k">보는 곳</span>Dock 웹 = SBC가 만든 페이지를 폰 브라우저가 표시 (같은 망 + 주소 · 앱 없음) · 폰 기본 설정 = 폰이 직접 표시 · Dock 표시등 = 본체 불빛</p>
      <p><span class="k">어긋나면</span>④에서 '연결된 기기 0' 유지 (폰 이름·핫스팟 비밀번호 변경, 폰 교체) → 핫스팟 끄고 Dock Wi-Fi 재접속 → 다. 재등록</p>
      <p><span class="k">요구 · 주의</span>Dock 표시등 상태 표시 (설계 요구) · 핫스팟 켠 뒤 설정 화면 유지 (Apple 권고) · 셀룰러 약 3 GB/일 (실측 전)</p>
    </div>
  </div>
  <footer class="ft"><span>FITOGETHER 하드웨어팀 | 사내 한정</span><span>6</span></footer>
</section>
</div>

'''

k = s.index('<!-- 6. 동작 시나리오 -->')
s = s[:k] + page + s[k:]


# 뒤쪽 번호 +1
def bump(sec_id, head=True):
    global s
    i = s.index(f'<section class="slide" id="{sec_id}">'); j = s.index('</section>', i)
    blk = s[i:j]
    if head:
        blk = re.sub(r'<span class="no">(\d+)\.</span>', lambda m: f'<span class="no">{int(m.group(1)) + 1}.</span>', blk, count=1)
    blk = re.sub(r'<span>(\d+)</span></footer>', lambda m: f'<span>{int(m.group(1)) + 1}</span></footer>', blk, count=1)
    s = s[:i] + blk + s[j:]


for sid in ('s4s', 's5', 's5b', 's6', 's7'):
    bump(sid)
bump('s8', head=False)
s = s.replace('1셀 상용 배터리 (8쪽)', '1셀 상용 배터리 (9쪽)')
s = s.replace('크기·조달, 2안 가능 여부 (8쪽)', '크기·조달, 2안 가능 여부 (9쪽)')
s = s.replace('<li>핫스팟 업로드 실기 (5·6쪽)</li>', '<li>핫스팟 업로드 실기 (5~7쪽)</li>')
open(P, 'w', encoding='utf-8').write(s)
print('userflow ok')
