# 신규 7쪽: 결과 확인 방안 (추출 · 업로드 완료/실패 인지 · 팀 논의용) — ab_pages.py 다음에 돈다
import re
src = open('userflow.py', encoding='utf-8').read()
exec(src[:src.index('# ── A. 최초 1회 ──')])       # tx · phone · field · button · addr · grid · src_chip 등 휴대폰 그림 부품
P = 'smart-dock-slide-asis-tobe.html'
s = open(P, encoding='utf-8').read()


def sub1(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


# ── 추출 결과 화면 (Dock 웹) ──
EXTRACT_RESULT = [
    addr(),
    title(SY + 42, '추출 완료', 8),
    tx(PW_ / 2, SY + 57, '22 / 24', 'tb', 'middle', 11),
    small(SY + 71, '✕ 5번 · 17번 칸', 'tac', 'middle', PW_ / 2),
    button(SY + 79, '실패 칸 다시', h=11),
    f'<rect x="{L0 - 1}" y="{SY + 93}" width="{R0 - L0 + 2}" height="11" rx="3" fill="var(--frame)" stroke="var(--line)" stroke-width="1"/>'
    + tx(PW_ / 2, SY + 98.5, '이대로 진행', '', 'middle', 7),
    f'<line x1="{L0}" y1="{SY + 110}" x2="{R0}" y2="{SY + 110}" stroke="var(--line)"/>',
    small(SY + 118, '다음: 핫스팟 켜기', 'tac', 'middle', PW_ / 2),
]

H = 318
o = [f'<svg class="dg" width="1168" height="{H}" viewBox="0 0 1168 {H}" role="img" aria-label="추출 결과 화면과 업로드 결과 알림 4개 안">']

# 왼쪽: 추출 결과는 확정
o.append(tx(0, 9, '추출 결과 — Dock 웹 화면으로 확정', 'tb', 'start', 12.5))
o.append(tx(0, 28, '② 끝 · 폰이 아직 Dock Wi-Fi에 연결 · 두 경로 공통', 'ts', 'start', 9.5))
o.append(f'<g transform="translate(0,44) scale(1.4)">' + phone(0, 0, ('wifi', 'Dock Wi-Fi 연결'), EXTRACT_RESULT) + '</g>')
CX = 118
lines = [('tb', 11, '화면이 저절로 결과로 바뀜'), ('ts', 9.5, '몇 초마다 SBC에 상태를 물음'),
         ('tb', 11, '완료 칸 수 · 실패 칸 번호'), ('ts', 9.5, '22 / 24 · ✕ 5번 · 17번'),
         ('tb', 11, '그 자리에서 다시 시도'), ('ts', 9.5, '실패 칸 다시 / 이대로 진행'),
         ('tb', 11, '다음 할 일을 안내'), ('ts', 9.5, '"핫스팟을 켜세요"'), ('ts', 9.5, '→ ③ 시점 판단 불필요')]
yy = 62
for cls, size, t in lines:
    o.append(tx(CX, yy, t, cls, 'start', size))
    yy += 16 if cls == 'tb' else 17
o.append(src_chip(CX, yy + 4, 'web'))
o.append(f'<line x1="330" y1="4" x2="330" y2="{H - 4}" stroke="var(--line)" stroke-width="1"/>')

# 오른쪽: 업로드 결과 4개 안
RX = 348
RW = 1168 - RX
o.append(tx(RX, 9, '업로드 결과 — 알림 방식 4개 안 (팀 논의)', 'tb', 'start', 12.5))
o.append(tx(RX, 28, '⑤ ⑥ · 폰은 핫스팟의 주인 → Dock 웹 화면을 못 볼 수 있음 · 조합해서 선택', 'ts', 'start', 9.5))
CW_, CH_, GAP = (RW - 12) / 2, 132, 10
CARDS = [
    ('안 1', 'Dock 표시등 (본체 불빛 · 소리)', '두 경로 공통',
     [('보는 곳', 'Dock 본체'), ('알 수 있음', '업로드 중 · 완료 · 실패'), ('장점', '항상 동작 · 폰 조작 없음'),
      ('한계', '본체를 봐야 함 · 실패 원인은 모름'), ('필요', 'LED·부저 설계 · 상태 표시 로직')],
     [('확실성', '상'), ('상세', '하'), ('코치 수고', '적음'), ('개발', '적음')]),
    ('안 2', '핫스팟 망에서 Dock 웹 화면 (⑧)', 'B안 유리',
     [('보는 곳', '폰 브라우저 (핫스팟 켠 채)'), ('알 수 있음', '실시간 진행 · 결과 · 원인'), ('장점', '업로드 중에도 폰에서 확인 · 다시 시도'),
      ('한계', '실측 전 · A안은 모듈 뒤라 어려움'), ('필요', '⑧ 실기 확인 · (A안) 포트 전달·이름 중계')],
     [('확실성', '실측 전'), ('상세', '상'), ('코치 수고', '중'), ('개발', '중')]),
    ('안 3', '핫스팟 끈 뒤 재접속 결과 화면', '두 경로 공통',
     [('보는 곳', 'Dock Wi-Fi 재접속 → Dock 아이콘'), ('알 수 있음', '최종 결과 · 실패 원인 · 다시 시도'), ('장점', '⑧ 없이 상세 결과 · SBC가 결과 보관'),
      ('한계', '자동 재접속 보장 안 됨 · 아이콘 한 번 더'), ('필요', '결과 저장·표시 화면 · (선택) 자동 창')],
     [('확실성', '중'), ('상세', '상'), ('코치 수고', '중'), ('개발', '적음')]),
    ('안 4', '서버 알림 (문자 · 메일 · 플랫폼)', '두 경로 공통',
     [('보는 곳', '폰 문자·메일 · 플랫폼 세션 목록'), ('알 수 있음', '서버 도착 (최종 확인)'), ('장점', '가장 확실 · 앱 없이 폰 알림'),
      ('한계', "실패는 '무소식'으로만 드러남"), ('필요', '서버 알림 기능 · 코치 연락처 등록')],
     [('확실성', '상'), ('상세', '중'), ('코치 수고', '적음'), ('개발', '많음')]),
]
for n, (no, ttl, fit, rows, rate) in enumerate(CARDS):
    r, c = divmod(n, 2)
    x = RX + c * (CW_ + 12)
    y = 42 + r * (CH_ + GAP)
    o.append(f'<rect x="{x:g}" y="{y}" width="{CW_:g}" height="{CH_}" rx="5" fill="var(--box)" stroke="var(--ink)" stroke-width="1.1"/>')
    o.append(f'<rect x="{x + 10:g}" y="{y + 8}" width="40" height="18" rx="3" fill="var(--accent-tint)" stroke="var(--accent-line)" stroke-width="1.2"/>')
    o.append(tx(x + 30, y + 17, no, 'tac', 'middle', 11))
    o.append(tx(x + 58, y + 17, ttl, 'tb', 'start', 11.5))
    fw = sum(8.8 if '가' <= ch <= '힣' else 2.6 if ch in ' ·' else 5.2 for ch in fit) + 12
    ac = fit != '두 경로 공통'
    o.append(f'<rect x="{x + CW_ - 10 - fw:g}" y="{y + 9}" width="{fw:.1f}" height="16" rx="8" '
             + ('fill="var(--accent-tint)" stroke="var(--accent)"' if ac else 'fill="none" stroke="var(--faint)"') + ' stroke-width="1"/>')
    o.append(tx(x + CW_ - 10 - fw / 2, y + 17, fit, 'tac' if ac else 'ts', 'middle', 9))
    yy = y + 40
    for k, v in rows:
        o.append(tx(x + 12, yy, k, 'ts', 'start', None, ' style="font-size:9.5px;font-weight:700"'))
        o.append(tx(x + 76, yy, v, '', 'start', 10))
        yy += 15
    # 평가 줄
    o.append(f'<line x1="{x + 10:g}" y1="{y + CH_ - 20}" x2="{x + CW_ - 10:g}" y2="{y + CH_ - 20}" stroke="var(--line)" stroke-width="1"/>')
    rx_ = x + 12
    for k, v in rate:
        o.append(tx(rx_, y + CH_ - 10, k, 'ts', 'start', 9))
        kw_ = sum(8.4 if '가' <= ch <= '힣' else 2.5 for ch in k) + 4
        o.append(tx(rx_ + kw_, y + CH_ - 10, v, 'tac', 'start', 9.5))
        rx_ += (CW_ - 24) / 4
o.append('</svg>')

page = f'''<!-- 7. 결과 확인 방안 -->
<div class="frame">
<section class="slide" id="s4r">
  <header class="hd"><h1><span class="no">7.</span>결과 확인 방안 (추출 · 업로드 완료/실패 · 팀 논의용)</h1></header>
  <p class="msg">추출 결과는 Dock 웹 화면으로 확정하고, 업로드 결과 알림은 4개 안의 조합을 팀 논의로 결정함</p>
  <div class="body" style="margin-top:14px">
    {chr(10).join(o)}
    <div class="kw" style="margin-top:12px">
      <p><span class="k">조합 예시</span>최소 = 안 1 + 안 3 · B안 선택 시 + 안 2 · 서비스 확장 시 + 안 4</p>
      <p><span class="k">실패 시</span>파일은 SBC에 보관 → 다음 핫스팟에서 자동 이어 올림 · 원인 3종 (핫스팟 접속 실패 · 업로드 중단 · 서버 거부)</p>
      <p><span class="k">논의 사항</span>① 본체 LED·부저 추가 여부 · ② 코치가 업로드 끝까지 폰을 두고 기다려야 하나 · ③ 결과를 누가 알아야 하나 (코치 · 분석 담당)</p>
    </div>
  </div>
  <footer class="ft"><span>FITOGETHER 하드웨어팀 | 사내 한정</span><span>7</span></footer>
</section>
</div>

'''
k = s.index('<!-- 6. 동작 시나리오 -->')
s = s[:k] + page + s[k:]


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
sub1('1셀 상용 배터리 (9쪽)', '1셀 상용 배터리 (10쪽)')
sub1('크기·조달, 2안 가능 여부 (9쪽)', '크기·조달, 2안 가능 여부 (10쪽)')
sub1('<li>업로드 경로 A·B안 실기 (5-A~5-C쪽)</li>', '<li>업로드 경로 A·B안 · 결과 알림 (5-A~7쪽)</li>')

# 6쪽에서 7쪽으로 잇기
sub1('실패 칸 재시도', '결과 화면 (7쪽)')
sub1("표시등 '완료' 뒤", '결과 확인 (7쪽)')
sub1('Dock 표시등 상태 표시 (설계 요구)', '결과 알림 방식 (7쪽 · 팀 논의)')
open(P, 'w', encoding='utf-8').write(s)
print('result ok')
