# 1쪽 설계 변경 · 5쪽 네트워크 흐름 검증(신규) · 6쪽 전원 · 7쪽 배터리 선정(신규) · 9쪽 의사결정
P = 'smart-dock-slide-asis-tobe.html'
s = open('base-v23.html', encoding='utf-8').read()
def sub1(a, b):
    global s
    assert s.count(a) == 1, ('not unique', s.count(a), a[:90])
    s = s.replace(a, b)
def T(x, y, t, cls='', anchor='middle', extra=''):
    c = f' class="{cls}"' if cls else ''
    a = f' text-anchor="{anchor}"' if anchor else ''
    return f'<text{c} x="{x:g}" y="{y:g}"{a} dominant-baseline="central"{extra}>{t}</text>'

# ── 공용 CSS ──
sub1('.dg .ts.tl { font-size: 8px; }', '.dg .ts.tl { font-size: 8px; }\n.dg .tag { font-size: 11.5px; font-weight: 700; fill: var(--accent); }\n.t .ac-h { color: var(--accent); }')
sub1('.ov .t td, .ov .t th { padding-top: 9px; padding-bottom: 9px; }', '.ov .t td, .ov .t th { padding-top: 4px; padding-bottom: 4px; }')
sub1('.it { border: 1px solid var(--line); padding: 11px 14px; background: var(--paper); }', '.it { border: 1px solid var(--line); padding: 8px 14px; background: var(--paper); }')
sub1('.it + .it { margin-top: 12px; }', '.it + .it { margin-top: 8px; }')
sub1('.it.goal { border: 1.8px solid var(--accent-line); background: var(--accent-tint); text-align: center; padding: 22px 14px; }',
     '.it.goal { border: 1.8px solid var(--accent-line); background: var(--accent-tint); text-align: center; padding: 14px 14px; }')
sub1('.ovsub { margin: 16px 0 8px;', '.ovsub { margin: 10px 0 6px;')

# ── 1쪽 ──
sub1('<p class="msg">LiveHub 미보유 고객을 위해 Dock 단독 무선 추출 체계를 구축하여, 추출 10분 이내·PC 제거·배터리 1/8 축소를 달성함</p>\n  <div class="body">', '<p class="msg">LiveHub 미보유 고객을 위해 Dock 단독 무선 추출 체계를 구축하여, 추출 10분 이내·PC 제거·배터리 1/8 축소를 달성함</p>\n  <div class="body" style="margin-top:14px">')
sub1('<p class="msg">LiveHub 미보유 고객을 위해 Dock 단독 무선 추출 체계를 구축하여, 추출 10분 이내·PC 제거·배터리 1/8 축소를 달성함</p>',
     '<p class="msg">LiveHub 미보유 고객을 위해 Dock 단독 무선 추출 체계를 구축하고, Dock 하드웨어를 단순화하여 PC·전용 충전기 의존을 제거함</p>')
sub1('<tr><th>내장 배터리</th><td>약 100 Wh</td><td><b class="k" style="margin:0">12 Wh 이하</b></td></tr>',
     '<tr><th>내장 배터리</th><td>약 100 Wh</td><td><b class="k" style="margin:0">12 Wh 이하</b></td></tr>\n'
     '            <tr><th>충전기</th><td>자사 100 W 어댑터</td><td><b class="k" style="margin:0">시판 USB-C</b> <span class="m">45 W 이하 (추정)</span></td></tr>')
sub1('<tr><th>추출 시간<br><span class="m" style="font-weight:400">셀 24대</span></th><td>유선 추출</td><td><b class="k" style="margin:0">10분 이내</b><br><span class="m">LiveHub 5분 수준</span></td></tr>',
     '<tr><th>추출 시간 (24대)</th><td>유선 추출</td><td><b class="k" style="margin:0">10분 이내</b> <span class="m">(LiveHub 5분)</span></td></tr>')
old = s[s.index('    <table class="t scope sm">'):]
old = old[:old.index('</table>') + 8]
sub1(old, '''    <p class="sec" style="margin-top:12px">Dock 하드웨어 변경</p>
    <table class="t sm tight xt">
      <colgroup><col style="width:130px"><col style="width:270px"><col style="width:250px"><col></colgroup>
      <thead><tr><th>항목</th><th>현행</th><th>변경</th><th>사유</th></tr></thead>
      <tbody>
        <tr><th>MCU</th><td>STM32F103C8T6</td><td><b class="k" style="margin:0">ESP32 계열 (셀과 동일)</b></td><td>개발 환경·부품 공용화</td></tr>
        <tr><th>셀 충전</th><td>24개 동시</td><td><b class="k" style="margin:0">6개 단위 순차</b></td><td>고출력 전용 충전기 불필요</td></tr>
        <tr><th>USB-C PD 칩</th><td>TI TPS25750 (고기능·설정 필요)</td><td><b class="k" style="margin:0">단순 수전 칩</b></td><td>원가·설정 작업 축소</td></tr>
        <tr><th>내장 배터리</th><td>3S 팩 약 100 Wh</td><td><b class="k" style="margin:0">1셀 상용 배터리 (8쪽)</b></td><td>맞춤 팩 MOQ 회피, 충전·게이지 칩도 1셀용으로 단순화</td></tr>
      </tbody>
    </table>
    <div class="row lines" style="margin-top:6px">
      <p class="col" style="flex:1.45"><span class="k">범위</span>DKPX-2 / DKPY-2 Dock 하드웨어, Dock 웹 화면 (개선 B)</p>
      <p class="col" style="flex:1"><span class="k">제외</span>셀 펌웨어 변경, LTE·유선 LAN</p>
    </div>''')

# ── 4쪽: MCU 표기 ──
i4 = s.index('<section class="slide" id="s4">'); j4 = s.index('</section>', i4)
blk = s[i4:j4].replace('>MCU</text>', '>MCU (ESP32)</text>')
blk = blk.replace('<tr><th>MCU</th><td>충전 · 슬롯 전원 · 온도 (현행 구조)</td>', '<tr><th>MCU (ESP32)</th><td>충전 · 슬롯 전원 · 온도 (셀과 MCU 통일)</td>')
s = s[:i4] + blk + s[j4:]

exec(open('net_block.py', encoding='utf-8').read())

# ── 6쪽: 전원 설계 ──
sub1('<header class="hd"><h1><span class="no">5.</span>전원 설계</h1></header>', '<header class="hd"><h1><span class="no">7.</span>전원 설계</h1></header>')
sub1('<p class="msg">내장 배터리의 역할을 셀 충전에서 제어부 비상 전원으로 변경하여, 용량을 현행 대비 1/8 이하로 축소함</p>',
     '<p class="msg">배터리는 제어부 비상 전원으로, 셀 충전은 어댑터 연결 시 6개 단위로 수행하여 배터리 1/8 이하·충전기 45 W 이하로 축소함</p>')
sub1('<text x="710" y="20" text-anchor="middle" dominant-baseline="central">셀 충전 (슬롯 24개)</text>',
     '<text x="710" y="20" text-anchor="middle" dominant-baseline="central">셀 충전 (6개 단위 순차)</text>')
sub1('<text class="ts" x="470" y="12" text-anchor="middle">어댑터 연결 시</text>',
     '<text class="ts" x="470" y="12" text-anchor="middle">어댑터 연결 시</text>\n      <text class="ts" x="388" y="56" text-anchor="start" dominant-baseline="central">어댑터 직결 — 배터리 없이 제어부 구동 (신규 · 현행은 배터리 경유 추정)</text>')
sub1('<p class="sec" style="margin-top:26px">용량 비교</p>', '<p class="sec" style="margin-top:18px">용량 비교</p>')
sub1('<tr><th>용량</th><td>약 100 Wh (11.1 V, 9,000 mAh)</td><td>슈퍼커패시터 수준</td><td>약 12 Wh (18650 셀 1개)</td></tr>',
     '<tr><th>용량</th><td>약 100 Wh (11.1 V, 9,000 mAh)</td><td>최소 (약 0.1 Wh)</td><td>약 12 Wh (18650 셀 1개)</td></tr>')
sub1('''    <div class="kw" style="margin-top:20px">
      <p><span class="k">산정 (2안)</span>50분 × 9 W ÷ 0.8 (수명) ÷ 0.8 (저온) ≈ 12 Wh</p>
      <p><span class="k">50분</span>추출 최대 20분 + 준비 10분 + 재시도 20분 (일 1회)</p>
      <p><span class="k">9 W (추정)</span>MCU 0.5 W + SBC 3 W + Wi-Fi 모듈 5 W = 8.5 W → 여유 포함 9 W / 모듈 사양 따라 최대 1.5배</p>
      <p><span class="k">2안 대안</span>시판 USB-C PD 보조배터리 구동 (고객 지참)</p>
    </div>''', '''    <div class="kw" style="margin-top:14px">
      <p><span class="k">산정 (2안)</span>50분 × 9 W ÷ 0.8 (수명) ÷ 0.8 (저온) ≈ 12 Wh · 50분 = 추출 최대 20분 + 준비 10분 + 재시도 20분</p>
      <p><span class="k">9 W (추정)</span>MCU 계통 0.5 W (칩 0.1~0.2 W + 주변 칩) + SBC 3 W + 모듈 5 W = 8.5 W → 여유 포함 9 W · 모듈 사양 따라 최대 1.5배</p>
      <p><span class="k">충전 전력</span>6개 × 2~3 W + 제어부 9 W ≈ 21~27 W → 시판 USB-C 충전기 (45 W 이하)</p>
      <p><span class="k">충전 시간</span>6개 단위 4회 · 그룹당 약 1.5~2시간 → 전체 약 6~8시간 (추정, 야간 충전)</p>
      <p><span class="k">2안 대안</span>시판 USB-C PD 보조배터리 구동 (고객 지참)</p>
    </div>''')
i5 = s.index('<section class="slide" id="s5">'); j5 = s.index('</section>', i5)
s = s[:i5] + s[i5:j5].replace('<footer class="ft"><span>FITOGETHER 하드웨어팀 | 사내 한정</span><span>5</span></footer>', '<footer class="ft"><span>FITOGETHER 하드웨어팀 | 사내 한정</span><span>7</span></footer>') + s[j5:]

# ── 신규 7쪽: 배터리 선정 검토 ──
bat_page = '''<!-- 7. 배터리 선정 검토 -->
<div class="frame">
<section class="slide" id="s5b">
  <header class="hd"><h1><span class="no">8.</span>배터리 선정 검토</h1></header>
  <p class="msg">맞춤 배터리 팩은 MOQ로 제외하고, 1셀 상용 원통형(18650)을 기본안으로 셀 배터리 공용안과 비교하여 사용 환경(1·2안) 결정 시 확정함</p>
  <div class="body" style="margin-top:16px">
    <p class="sec">필요 조건</p>
    <div class="kw">
      <p><span class="k">1안</span>정상 종료 — 9 W × 30초 ≈ 0.1 Wh</p>
      <p><span class="k">2안</span>추출 1회 — 약 12 Wh (모듈 전력 1.5배 시 약 18 Wh)</p>
      <p><span class="k">공통</span>순간 전류 약 2.5 A (9 W ÷ 3.7 V, 1셀 기준)</p>
    </div>
    <p class="sec" style="margin-top:14px">후보 비교</p>
    <table class="t sm tight xt">
      <colgroup><col style="width:130px"><col><col><col></colgroup>
      <thead><tr><th>구분</th><th>셀 배터리 공용</th><th class="ac-h">원통형 18650 (권고)</th><th>원통형 21700 (참고)</th></tr></thead>
      <tbody>
        <tr><th>규격</th><td>GRP753427 (셀 Y) · 750 mAh · 2.89 Wh</td><td>3,000~3,500 mAh · 약 11~12.6 Wh</td><td>4,000~5,000 mAh · 약 14~18 Wh</td></tr>
        <tr><th>크기·무게</th><td>약 7.5 × 34 × 27 mm (형번 기준 추정)</td><td>ø18 × 65 mm · 약 47 g</td><td>ø21 × 70 mm · 약 70 g</td></tr>
        <tr><th>1안 정상 종료</th><td>에너지 충족 · 방전 전류 확인 필요 (약 3.3C)</td><td>충족</td><td>충족</td></tr>
        <tr><th>2안 약 12 Wh</th><td>4~5개 필요 → 다셀 팩 제작 (MOQ 재발)</td><td>3,500 mAh급 충족 · 1.5배 시 부족</td><td>1.5배 (약 18 Wh)까지 충족</td></tr>
        <tr><th>조달</th><td>기존 부품·공급사</td><td>상용 표준품 (다수 제조사)</td><td>상용 표준품</td></tr>
        <tr><th>공용화</th><td>셀과 동일 배터리·충전 회로</td><td>1셀 충전 회로 공용</td><td>1셀 충전 회로 공용</td></tr>
        <tr class="rec"><th>판단</th><td>1안 한정 시 대안</td><td class="ac">권고 (1·2안 공통)</td><td>모듈 전력 확정 후 선택</td></tr>
      </tbody>
    </table>
    <div class="kw" style="margin-top:12px">
      <p><span class="k">크기 참고</span>현행 11.1 V · 9,000 mAh 팩 = 18650 (3,000 mAh) 9개 구성과 수치 일치 (추정) → 18650 1개 ≈ 현행의 1/9</p>
      <p><span class="k">설계 영향</span>1셀 3.0~4.2 V → SBC 5 V · 모듈 입력용 승압 회로 필요</p>
      <p><span class="k">확인 필요</span>GRP753427 허용 방전 전류 · 셀 X6 배터리 GRP693027은 500 mAh (CLBX-6B 지도) — 공용 대상 형번 확정</p>
    </div>
  </div>
  <footer class="ft"><span>FITOGETHER 하드웨어팀 | 사내 한정</span><span>8</span></footer>
</section>
</div>

'''
k = s.index('<!-- 6. 웹 화면 개발 계획 -->')
s = s[:k] + bat_page + s[k:]

# ── 8쪽 웹 · 9쪽 의사결정 · 참고 쪽 번호 ──
sub1('<header class="hd"><h1><span class="no">6.</span>웹 화면 개발 계획</h1></header>', '<header class="hd"><h1><span class="no">9.</span>웹 화면 개발 계획</h1></header>')
i6 = s.index('<section class="slide" id="s6">'); j6 = s.index('</section>', i6)
s = s[:i6] + s[i6:j6].replace('<span>6</span></footer>', '<span>9</span></footer>') + s[j6:]
sub1('<header class="hd"><h1><span class="no">7.</span>의사결정 요청 및 향후 계획</h1></header>', '<header class="hd"><h1><span class="no">10.</span>의사결정 요청 및 향후 계획</h1></header>')
i7 = s.index('<section class="slide" id="s7">'); j7 = s.index('</section>', i7)
s = s[:i7] + s[i7:j7].replace('<span>7</span></footer>', '<span>10</span></footer>') + s[j7:]
i8 = s.index('<section class="slide" id="s8">'); j8 = s.index('</section>', i8)
s = s[:i8] + s[i8:j8].replace('<span>8</span></footer>', '<span>11</span></footer>') + s[j8:]
sub1('<p class="msg">사용 환경 범위와 Dock Wi-Fi 이름 체계 결정 후, 성공 기준 v3를 확정하여 모듈 선정에 착수함</p>',
     '<p class="msg">사용 환경 범위·Dock Wi-Fi 이름 체계·배터리 방식 결정 후, 성공 기준 v3를 확정하여 모듈 선정과 네트워크 실기 검증에 착수함</p>')
sub1('''<tr><td class="c">3</td><th>성공 기준 v3</th><td>2.4 / 5 GHz 동시, 핫스팟 한정<br>배터리 역할 변경</td><td>개발 착수 기준</td><td class="c ac">승인 요청</td></tr>''',
     '''<tr><td class="c">3</td><th>배터리 방식</th><td>원통형 18650 (권고)<br>셀 배터리 공용</td><td>크기·조달, 2안 가능 여부 (8쪽)</td><td class="c">1번과 연동</td></tr>
        <tr><td class="c">4</td><th>성공 기준 v3</th><td>2.4 / 5 GHz 동시, 핫스팟 한정<br>배터리 역할 변경</td><td>개발 착수 기준</td><td class="c ac">승인 요청</td></tr>''')
sub1('''      <li>Kinexon의 LiveHub 활용 방식</li>
    </ul>''', '''      <li>Kinexon의 LiveHub 활용 방식</li>
      <li>핫스팟 업로드 실기 (5·6쪽)</li>
      <li>셀 켜짐 조건 (Dock은 셀을 켤 수 없음)</li>
      <li>현행 Dock 무배터리 동작</li>
      <li>파일 크기 실측 (M2)</li>
    </ul>''')
sub1('<p class="sec" style="margin-top:22px">확인 필요 사항</p>', '<p class="sec" style="margin-top:16px">확인 필요 사항</p>')
sub1('<p class="sec" style="margin-top:22px">향후 계획</p>', '<p class="sec" style="margin-top:16px">향후 계획</p>')
sub1('<text x="484.4" y="22" text-anchor="middle" dominant-baseline="central">Wi-Fi 모듈 선정·시험</text>', '<text x="484.4" y="22" text-anchor="middle" dominant-baseline="central">모듈 선정·네트워크 실기</text>')
sub1('<text x="683.6" y="22" text-anchor="middle" dominant-baseline="central">웹 화면 P1–P2</text>', '<text x="683.6" y="22" text-anchor="middle" dominant-baseline="central">배터리·전원 확정</text>')
sub1('<text x="882.8" y="22" text-anchor="middle" dominant-baseline="central">셀 연동 P3</text>', '<text x="882.8" y="22" text-anchor="middle" dominant-baseline="central">웹 화면 P1–P3</text>')
open(P, 'w', encoding='utf-8').write(s)
print('ok')
