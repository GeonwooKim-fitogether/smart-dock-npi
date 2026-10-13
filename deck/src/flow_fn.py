def flow_svg(var='A'):
    # var='A': Wi-Fi 모듈이 핫스팟에 접속 / var='B': SBC 자체 Wi-Fi가 핫스팟에 직접 접속
    # 4쪽 개선 B 그림을 시간 순서대로 6번 반복 — 단계마다 열린 통신선과 그 위의 데이터 이동을 표시
    o = ['<svg class="dg" width="1168" height="560" viewBox="0 0 1168 560" role="img" aria-label="시간 순서 6단계마다 개선 B 구성도에서 열린 네트워크 길과 데이터 이동">',
         '<defs>'
         '<marker id="f6k" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--ink)"/></marker>'
         '<marker id="f6ks" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" fill="var(--ink)"/></marker>'
         '<marker id="f6d" viewBox="0 0 8 8" refX="6.5" refY="4" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--accent-line)"/></marker>'
         '<marker id="f6h" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--accent)"/></marker>'
         '<marker id="f6hs" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" fill="var(--accent)"/></marker>'
         '<marker id="f6a" viewBox="0 0 8 8" refX="7.5" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="ah" d="M0,0 L8,4 L0,8 z"/></marker>'
         '</defs>']
    def tx(x, y, t, cls='', anchor='middle', size=None, extra=''):
        st = f' style="font-size:{size}px"' if size else ''
        c = f' class="{cls}"' if cls else ''
        return f'<text{c} x="{x:g}" y="{y:g}" text-anchor="{anchor}" dominant-baseline="central"{st}{extra}>{t}</text>'
    # ── 프레임 ──
    def line(pts, state, m_end=False, both=False):
        d = 'M' + ' L'.join(f'{x:g},{y:g}' for x, y in pts)
        if state == 'data':
            return f'<path d="{d}" fill="none" stroke="var(--accent-line)" stroke-width="3" stroke-linejoin="round" marker-end="url(#f6d)"/>'
        if state == 'on':
            me = ' marker-end="url(#f6k)"' if m_end else ''
            ms = ' marker-start="url(#f6ks)"' if both else ''
            return f'<path d="{d}" fill="none" stroke="var(--ink)" stroke-width="1.4"{ms}{me}/>'
        if state == 'hot':
            return f'<path d="{d}" fill="none" stroke="var(--accent)" stroke-width="1.4" stroke-dasharray="4 2.5" marker-start="url(#f6hs)" marker-end="url(#f6h)"/>'
        if state == 'pend':
            return f'<path d="{d}" fill="none" stroke="var(--muted)" stroke-width="1.2" stroke-dasharray="3 2.5"/>'
        # off · cut
        out = f'<path d="{d}" fill="none" stroke="var(--line)" stroke-width="1"/>'
        if state == 'cut':
            a, b = (pts[0], pts[1]) if len(pts) > 2 else (pts[0], pts[-1])
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            out += tx(mx, my, '✕', 'tb', size=12)
        return out
    def box(x, y, w, h, t, st='n', size=10.5, sub=None):
        cls = {'n': 'bx', 'ac': 'bx ac', 'dim': 'bx'}[st]
        op = ' opacity=".35"' if st == 'dim' else ''
        g = f'<g{op}><rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>'
        if sub:
            g += tx(x + w / 2, y + h / 2 - 5, t, 'tac' if st == 'ac' else '', size=size) + tx(x + w / 2, y + h / 2 + 7, sub, 'ts', size=8)
        else:
            g += tx(x + w / 2, y + h / 2, t, 'tac' if st == 'ac' else '', size=size)
        return g + '</g>'
    PW, PH, AG, RG = (1168 - 2 * 30) / 3, 242, 30, 28
    SC = (PW - 20) / 370
    def frame(ox, oy, F):
        g = [f'<g transform="translate({ox:g},{oy:g})">']
        # 단계 상자
        g.append(f'<rect x="0" y="0" width="{PW:g}" height="{PH}" rx="6" fill="var(--box)" stroke="var(--ink)" stroke-width="1.2"/>')
        g.append(f'<rect x="10" y="8" width="66" height="20" rx="3" fill="var(--accent-tint)" stroke="var(--accent-line)" stroke-width="1.2"/>')
        g.append(tx(43, 18, F['step'], 'tac', size=12))
        g.append(tx(84, 18, F['t1'], 'tb', anchor='start', size=11))
        g.append(tx(10, 38, F['t2'], 'ts', anchor='start', size=9.5))
        g.append(f'<line x1="10" y1="48" x2="{PW - 10:g}" y2="48" stroke="var(--line)" stroke-width="1"/>')
        g.append(f'<g transform="translate({(PW - 370 * SC) / 2:g},56) scale({SC:.4f})">')
        # Dock
        g.append('<rect class="fr" x="0" y="0" width="198" height="186" rx="6"/>')
        g.append(tx(192, 176, 'Dock', 'tb', anchor='end', size=9.5))
        for r in range(4):
            for c in range(6):
                g.append(f'<use href="#cell-x-sm" class="cx" x="{6 + c * 12}" y="{14 + r * 22}" width="10" height="17"/>')
        g.append(tx(41, 114, '셀 ×24', 'tb', size=9))
        L = F['L']
        # ① 셀 ↔ 모듈 (Wi-Fi)
        if L['cell'] == 'data_rev':
            g.append(line([(102, 23), (80, 23)], 'data'))
        else:
            g.append(line([(78, 23), (102, 23)], L['cell'], m_end=True))
        g.append(tx(90, 12, 'Wi-Fi', 'ts', size=7.5))
        g.append(box(104, 12, 90, 22, 'Wi-Fi 모듈', 'ac', 10.5))
        # ② 모듈 ↔ SBC (Ethernet)
        g.append(line([(140, 34), (140, 70)], L['eth_dn'], m_end=True))
        g.append(line([(158, 70), (158, 36)], L['eth_up'], m_end=True))
        g.append(tx(163, 52, 'Ethernet', 'ts', anchor='start', size=7.5))
        g.append(box(104, 72, 90, 22, 'SBC + Wi-Fi' if var == 'B' else 'SBC', 'ac', 10.5))
        # ③ SBC – MCU (UART) · ④ 셀 – MCU (Pogo)
        g.append(line([(149, 94), (149, 130)], 'on'))
        g.append(tx(153, 112, 'UART', 'ts', anchor='start', size=7.5))
        g.append(line([(78, 143), (104, 143)], 'on'))
        g.append(tx(91, 135, 'Pogo', 'ts', size=7.5))
        g.append(box(104, 132, 90, 22, 'MCU (ESP32)', 'n', 10))
        # 오른쪽 기기
        g.append(box(250, 8, 120, 30, '스마트폰', F['phone'], 10.5, sub=F['phone_sub']))
        g.append(box(250, 80, 120, 22, '스마트폰 핫스팟', F['hot'], 10))
        g.append(box(250, 146, 120, 22, '서버', F['srv'], 10.5))
        # ⑤ 조작: 모듈 ↔ 스마트폰
        g.append(line([(194, 20), (248, 20)], L['ctl'], m_end=True, both=True))
        # 라벨은 Dock 테두리(198)와 스마트폰 상자(250) 사이 빈칸에 두 줄로 둔다
        if L['ctl'] == 'hot':
            g.append(tx(224, 5, '조작', 'tac', size=7.5)); g.append(tx(224, 13, '확인 필요', 'tac', size=7.5))
        elif L['ctl'] == 'cut':
            g.append(tx(224, 9, F.get('ctl_lab', '조작 끊김'), 'ts', size=7.5))
        elif L['ctl'] == 'on':
            g.append(tx(224, 5, '조작', 'ts', size=7.5)); g.append(tx(224, 13, 'Wi-Fi · HTTP', 'ts', size=7.5))
        # 스마트폰과 핫스팟은 같은 기기
        if F.get('same'):
            g.append('<path d="M366,38 V80" fill="none" stroke="var(--muted)" stroke-width="1" stroke-dasharray="1.5 2"/>')
            g.append(tx(362, 66, '같은 스마트폰', 'ts', anchor='end', size=7.5))
        if var == 'B':
            # ⑥ SBC → 핫스팟 (SBC 자체 Wi-Fi가 손님)
            g.append(line([(194, 90), (248, 90)], L['sta'], m_end=True))
            g.append(tx(223, 99, 'Wi-Fi 5 GHz', 'ts', size=7.5))
            # ⑧ 핫스팟 망에서 스마트폰 ↔ SBC 직접
            if F.get('hot8'):
                g.append(line([(248, 32), (234, 32), (234, 74), (196, 74)], 'hot'))
                g.append(tx(238, 50, '조작 · 확인 필요', 'tac', anchor='start', size=7.5))
        else:
            # ⑥ 모듈 → 핫스팟 (Wi-Fi 클라이언트)
            g.append(line([(194, 30), (222, 30), (222, 91), (248, 91)], L['sta'], m_end=True))
            g.append(tx(226, 56, 'Wi-Fi', 'ts', anchor='start', size=7.5)); g.append(tx(226, 66, '5 GHz', 'ts', anchor='start', size=7.5))
        # ⑦ 핫스팟 → 서버 (셀룰러 · HTTPS)
        g.append(line([(310, 102), (310, 144)], L['cell_up'], m_end=True))
        g.append(tx(314, 123, '셀룰러 · HTTPS', 'ts', anchor='start', size=7.5))
        # 상태 꼬리표
        for x, y, t in F.get('tags', []):
            w = sum(7.8 if '\uac00' <= ch <= '\ud7a3' else 2.3 if ch in ' ·' else 4.6 for ch in t) + 6
            g.append(f'<rect x="{x - 2}" y="{y - 7}" width="{w:.1f}" height="14" rx="2" fill="var(--accent-tint)" stroke="var(--accent-line)" stroke-width="1"/>')
            g.append(tx(x + 1, y, t, 'tac', anchor='start', size=8))
        g.append('</g></g>')
        return '\n'.join(g)
    FR = [
        dict(step='① 준비', t1='코치 · 셀 켠 채 거치, 스마트폰 Dock Wi-Fi 접속', t2='열린 길: 스마트폰 ↔ 모듈 (Wi-Fi 5 GHz · HTTP) · 인터넷 없음',
             L=dict(cell='off', eth_dn='off', eth_up='off', ctl='on', sta='off', cell_up='off'), phone='n', phone_sub='Dock Wi-Fi 접속 · 웹 화면', hot='dim', srv='dim',
             tags=[(8, 128, '켜진 채 거치'), (254, 50, '핫스팟 정보 등록 (최초 1회)')]),
        dict(step='② 추출', t1='코치 START → Dock 자동 수신 (목표 10분)', t2='데이터: 셀 → 모듈 (Wi-Fi 2.4/5) → SBC (Ethernet) 저장',
             L=dict(cell='data', eth_dn='data', eth_up='off', ctl='on', sta='off', cell_up='off'), phone='n', phone_sub='진행 · 실패 칸 확인', hot='dim', srv='dim',
             tags=[(108, 60, '파일 저장'), (254, 50, '자동 업로드 예약')]),
        dict(step='③ 전환', t1='코치 · Dock Wi-Fi 해제 → 핫스팟 ON', t2='끊김: 조작 길 · 생김: 핫스팟 (셀룰러) · 데이터는 SBC 보관',
             L=dict(cell='off', eth_dn='off', eth_up='off', ctl='cut', sta='pend', cell_up='on'), phone='n', phone_sub='핫스팟 켜기', hot='ac', srv='n', same=True,
             ctl_lab='조작 끊김', tags=[(108, 60, '보관 중'), (254, 48, '지시 공백 · 자동 대기')]),
        dict(step='④ 접속', t1='Dock 자동 · 저장된 정보로 핫스팟 접속', t2='열린 길: 모듈 → 핫스팟 (Wi-Fi 5 GHz) → 인터넷 (셀룰러)',
             L=dict(cell='off', eth_dn='off', eth_up='off', ctl='hot', sta='on', cell_up='on'), phone='n', phone_sub='핫스팟 망에서 다시 접속', hot='ac', srv='n', same=True,
             ctl_lab='', tags=[(82, 60, '핫스팟 정보로 접속')]),
        dict(step='⑤ 업로드', t1='Dock 자동 · SBC 파일을 서버로', t2='데이터: SBC → 모듈 → 핫스팟 → 서버 (HTTPS)',
             L=dict(cell='off', eth_dn='off', eth_up='data', ctl='hot', sta='data', cell_up='data'), phone='n', phone_sub='진행 보기 · 다시 시도', hot='ac', srv='ac', same=True,
             ctl_lab='', tags=[]),
        dict(step='⑥ 완료', t1='서버 확인 → 셀 원본 삭제 · 코치 핫스팟 OFF', t2='닫힘: 핫스팟 길 · 남음: Dock AP (충전 대기) · 자동 종료',
             L=dict(cell='data_rev', eth_dn='off', eth_up='data', ctl='off', sta='cut', cell_up='off'), phone='n', phone_sub='핫스팟 끄기 · 표시등 확인', hot='dim', srv='n',
             ctl_lab='', tags=[(8, 128, '원본 삭제'), (254, 134, '도착 확인')]),
    ]
    if var == 'B':
        FR = [dict(F) for F in FR]
        FR[3].update(t1='SBC 자동 · 저장된 정보로 핫스팟 직접 접속', t2='열린 길: SBC → 핫스팟 (Wi-Fi 5 GHz) → 인터넷 (셀룰러)',
                     L=dict(cell='off', eth_dn='off', eth_up='off', ctl='off', sta='on', cell_up='on'), hot8=True,
                     phone_sub='핫스팟 망에서 SBC 직접 접속', tags=[(80, 108, '핫스팟 정보로 접속')])
        FR[4].update(t1='SBC 자동 · 파일을 서버로 (모듈 미경유)', t2='데이터: SBC → 핫스팟 → 서버 (HTTPS) · 모듈은 셀 AP만',
                     L=dict(cell='off', eth_dn='off', eth_up='off', ctl='off', sta='data', cell_up='data'), hot8=True)
    pos = []
    for i, F in enumerate(FR):
        r, c = divmod(i, 3)
        x, y = c * (PW + AG), r * (PH + RG)
        pos.append((x, y))
        o.append(frame(x, y, F))
    for i in (0, 1, 3, 4):
        x, y = pos[i]
        o.append(f'<line class="ln" x1="{x + PW + 2:g}" y1="{y + PH / 2:g}" x2="{x + PW + AG - 3:g}" y2="{y + PH / 2:g}" stroke-width="1.6" marker-end="url(#f6a)"/>')
    x3, y3 = pos[2]; x4, y4 = pos[3]
    ym = PH + RG / 2
    o.append(f'<path class="ln" d="M{x3 + PW / 2:g},{PH + 2} V{ym:g} H{x4 + PW / 2:g} V{y4 - 3:g}" stroke-width="1.6" marker-end="url(#f6a)"/>')
    # 범례
    ly = 2 * PH + RG + 22
    o.append(f'<line x1="0" y1="{ly}" x2="28" y2="{ly}" stroke="var(--line)" stroke-width="1"/>'); o.append(tx(34, ly, '연결 없음 · 대기', 'ts', anchor='start', size=10))
    o.append(f'<line x1="150" y1="{ly}" x2="178" y2="{ly}" stroke="var(--ink)" stroke-width="1.4"/>'); o.append(tx(184, ly, '연결됨 (길 열림)', 'ts', anchor='start', size=10))
    o.append(f'<line x1="300" y1="{ly}" x2="328" y2="{ly}" stroke="var(--accent-line)" stroke-width="3" marker-end="url(#f6d)"/>'); o.append(tx(336, ly, '데이터 이동', 'ts', anchor='start', size=10))
    o.append(tx(430, ly, '✕', 'tb', size=12)); o.append(tx(442, ly, '끊김', 'ts', anchor='start', size=10))
    o.append(f'<line x1="500" y1="{ly}" x2="528" y2="{ly}" stroke="var(--muted)" stroke-width="1.2" stroke-dasharray="3 2.5"/>'); o.append(tx(534, ly, '접속 중', 'ts', anchor='start', size=10))
    o.append(f'<line x1="610" y1="{ly}" x2="638" y2="{ly}" stroke="var(--accent)" stroke-width="1.4" stroke-dasharray="4 2.5"/>'); o.append(tx(644, ly, '핫스팟 망 경유 조작 (확인 필요)', 'ts', anchor='start', size=10))
    o.append(f'<line x1="828" y1="{ly}" x2="856" y2="{ly}" stroke="var(--muted)" stroke-width="1" stroke-dasharray="1.5 2"/>'); o.append(tx(862, ly, '같은 기기', 'ts', anchor='start', size=10))
    l2 = ly + 20
    o.append(tx(0, l2, '업로드 지시:', 'tb', anchor='start', size=10.5))
    o.append(tx(74, l2, '② 자동 업로드 예약 → ③ 조작 끊김 동안 Dock 자동 대기 → ④ 핫스팟 접속 즉시 업로드 시작 (지시 없이 진행)', 'ts', anchor='start', size=10.5))
    o.append(tx(1168, l2, '핫스팟 = 인터넷으로 가는 유일한 문 (③ 열림 · ⑥ 닫힘)', 'tb', anchor='end', size=10.5))
    o.append('</svg>')
    out = '\n      '.join(o)
    if var != 'A':
        out = out.replace('id="f6', f'id="f6{var}').replace('url(#f6', f'url(#f6{var}')
    return out

