# 업로드 경로 A안 · B안 — 5쪽을 5-A로 바꾸고 5-B(그림)·5-C(비교)를 더한다. deck_v24.py → userflow.py 다음에 돈다
P = 'smart-dock-slide-asis-tobe.html'
s = open(P, encoding='utf-8').read()
exec(open('flow_fn.py', encoding='utf-8').read())


def sub1(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


def section(sid):
    i = s.index(f'<section class="slide" id="{sid}">')
    return i, s.index('</section>', i)


# 5-A: 기존 5쪽 제목·쪽 번호
sub1('<header class="hd"><h1><span class="no">5.</span>시간 순서별 네트워크 길과 데이터 이동 (개선 B)</h1></header>',
     '<header class="hd"><h1><span class="no">5-A.</span>네트워크 길과 데이터 이동 · A안 (Wi-Fi 모듈이 핫스팟 접속)</h1></header>')
i, j = section('s4n')
s = s[:i] + s[i:j].replace('<span>5</span></footer>', '<span>5-A</span></footer>', 1) + s[j:]

page_b = f'''<!-- 5-B. 네트워크 길과 데이터 이동 · B안 -->
<div class="frame">
<section class="slide" id="s4nb">
  <header class="hd"><h1><span class="no">5-B.</span>네트워크 길과 데이터 이동 · B안 (SBC가 핫스팟 직접 접속)</h1></header>
  <div class="body" style="margin-top:16px">
    {flow_svg('B')}
  </div>
  <footer class="ft"><span>FITOGETHER 하드웨어팀 | 사내 한정</span><span>5-B</span></footer>
</section>
</div>

'''

page_c = '''<!-- 5-C. 업로드 경로 A안 · B안 비교 -->
<div class="frame">
<section class="slide" id="s4nc">
  <header class="hd"><h1><span class="no">5-C.</span>업로드 경로 A안 · B안 비교 (팀 논의용)</h1></header>
  <p class="msg">두 안 모두 성립하며 차이는 핫스팟에 붙는 기기(모듈 또는 SBC)이고, 공통 실기 시험 4항목으로 확정함</p>
  <div class="body" style="margin-top:14px">
    <table class="t sm tight xt" style="table-layout:fixed">
      <colgroup><col style="width:150px"><col><col></colgroup>
      <thead><tr><th>구분</th><th>A안 · Wi-Fi 모듈이 핫스팟 접속 (5-A쪽)</th><th>B안 · SBC가 핫스팟 직접 접속 (5-B쪽)</th></tr></thead>
      <tbody>
        <tr><th>핫스팟 손님</th><td>Wi-Fi 모듈 (공유기 + 손님 겸용)</td><td>SBC 자체 Wi-Fi</td></tr>
        <tr><th>모듈 역할</th><td>셀·폰 AP + 핫스팟 중계</td><td>셀·폰 AP 전용</td></tr>
        <tr><th>필요 조건</th><td>모듈 라디오 2개 (AP · 손님 분리) · 자동 재접속 펌웨어 · SBC가 모듈 설정을 바꿀 통로</td><td>SBC Wi-Fi 내장 또는 추가 (5 GHz) · 안테나 케이스 밖 배치</td></tr>
        <tr><th>자동 재접속</th><td>모듈 펌웨어 기능 (OpenWrt travelmate 등)</td><td>리눅스 기본 기능 (저장된 Wi-Fi 자동 접속)</td></tr>
        <tr><th>연결 상태 파악</th><td>SBC가 모듈에 조회</td><td>SBC가 직접 확인</td></tr>
        <tr><th>⑧ 업로드 중 조작</th><td>어려움 — SBC가 모듈 뒤 (포트 전달 · 이름 알림 중계 설정 필요)</td><td>쉬움 — SBC가 핫스팟 망에 직접 참여</td></tr>
        <tr><th>무선 · 안테나</th><td>모듈 1개 · 안테나 1벌</td><td>모듈 + SBC · 안테나 2벌 · 상호 간섭 검토</td></tr>
        <tr><th>소프트웨어</th><td>모듈 펌웨어 + SBC (2곳)</td><td>SBC (1곳)</td></tr>
        <tr><th>주요 위험</th><td>한 라디오 겸용 시 핫스팟 탐색 중 AP 중단 → 셀 연결 끊김</td><td>금속 케이스 내 SBC 신호 · 부품 추가</td></tr>
        <tr><th>기존 이력</th><td>1C 기판 공유기 모듈 자리 (BL-M7628AR4 · 2.4 GHz 추정 · 미실장)</td><td>1B 기판 라즈베리파이 제로 2 W 실장 (Wi-Fi 내장 · 2.4 GHz)</td></tr>
        <tr class="rec"><th>검토 의견</th><td>하드웨어 단순 — 라디오 2개 모듈 확보 시 유효</td><td class="ac">소프트웨어 · ⑧ 단순 — 우선 시험 권고</td></tr>
      </tbody>
    </table>
    <div class="kw" style="margin-top:12px">
      <p><span class="k">논의 사항</span>① 업로드 중 폰 조작(⑧) 필요 여부 · ② SBC 기종과 Wi-Fi 내장 여부 · ③ 모듈 후보 (라디오 2개 · OpenWrt) · ④ 안테나 배치</p>
      <p><span class="k">실기 시험</span>핫스팟 ON 후 자동 접속 시간 (iPhone · Android) · 접속 중 셀 AP 유지 (A안) · smartdock.local 접근 (⑧) · 업로드 속도</p>
      <p><span class="k">공통</span>코치 조작 · 사용자 플로우 동일 (6쪽) · 핫스팟 정보 저장 위치만 다름 (A안 모듈 · B안 SBC) · 2.4 GHz 전용이면 iPhone '호환성 최대화' 필요</p>
    </div>
  </div>
  <footer class="ft"><span>FITOGETHER 하드웨어팀 | 사내 한정</span><span>5-C</span></footer>
</section>
</div>

'''

k = s.index('<!-- 6. 스마트폰 사용자 플로우 -->')
s = s[:k] + page_b + page_c + s[k:]

# 다른 쪽의 참조 정리
sub1('<span class="note">(5쪽 ①~⑥ · 조작 4회 · 대기 2회)</span>', '<span class="note">(5-A · 5-B쪽 ①~⑥ · 조작 4회 · 대기 2회 · 두 안 동일)</span>')
sub1('<h1><span class="no">7.</span>동작 시나리오 (개선 B · 핫스팟 업로드)</h1>', '<h1><span class="no">7.</span>동작 시나리오 (개선 B · 핫스팟 업로드 · A안 기준)</h1>')
sub1('<p><span class="k">개선 A</span>iPad가', '<p><span class="k">B안</span>3·4단계의 핫스팟 접속·업로드를 SBC 자체 Wi-Fi가 수행 · 모듈은 셀·폰 AP만 유지 (5-B쪽)</p>\n      <p><span class="k">개선 A</span>iPad가')
sub1('<li>핫스팟 업로드 실기 (5~7쪽)</li>', '<li>업로드 경로 A·B안 실기 (5-A~5-C쪽)</li>')
open(P, 'w', encoding='utf-8').write(s)
print('ab ok')
