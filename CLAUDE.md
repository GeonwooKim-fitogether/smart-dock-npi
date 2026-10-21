# CLAUDE.md — 이 저장소에서 일하는 Claude 를 위한 안내

## 이 저장소가 뭔가
Smart Dock(DKPX-2/DKPY-2) 무선 추출 NPI 의 **기획·논의 작업장**이다. 코드 제품이 아니라 문서·덱·목업·실기 시험 기록이 산출물이다.
공식 기록은 사내 시스템 Fitstack 의 NPI 게이트가 맡는다. 여기서는 논의와 초안을 만들고, 확정본(PDF)과 3~5줄 요약만 게이트로 넘긴다.

## 시작할 때 읽는 순서
1. `README.md` — 지금 상태와 열린 안건
2. `decisions.md` — 이미 정한 것 (뒤집기 전에 반드시 확인)
3. 가장 최근 `meetings/*.md`
4. `docs/working-model.md` — GitHub · Fitstack · Claude 의 역할 분담과 정본 표 (무엇을 어디에 쓰나)

## 일하는 규칙
- **결정은 사람이 한다.** Claude 는 안(案)과 근거를 만들고, 결정 기록은 미팅에서 정해진 것만 `decisions.md` 에 적는다. 결정을 뒤집을 때는 앞 줄을 고치지 않고 새 줄을 추가한다.
- **안건 = 이슈 하나.** 새 논점이 생기면 이슈로 열고 README 의 열린 안건 목록을 함께 갱신한다.
- **덱은 원본 스크립트로 고친다.** `deck/smart-dock-slide-asis-tobe.html` 을 직접 고치지 않는다. `deck/src` 의 쪽별 스크립트를 고치고 `sh build.sh` 로 다시 만든다. 고친 뒤에는 `render_ceo.py desk` 로 쪽마다 넘침이 없는지 확인한다.
- **덱 표현 원칙** (1차 미팅까지 확정된 형식): 대기업 경영 보고 양식 — 키워드·도식 중심, 공식 용어, 설명 문장 최소. 셀은 사각형이 아니라 셀 X 외곽선(`assets/cell/cell-x-outline.svg`, 덱 안 `#cell-x` 심볼)으로 그린다.
- **미팅이 끝나면** PDF 를 `exports/SmartDock_기획_YYYY-MM-DD.pdf` 로 남기고 README 의 "지금 어디까지 왔나" 표를 갱신한다.
- 셀 펌웨어 변경과 LTE·유선 LAN 은 이 과제의 범위 밖이다(덱 1쪽).
- 자료는 사내 한정이다. 이 저장소는 비공개를 유지한다.

## 브랜치·PR
회사 공용 규칙(`.claude/rules/branch-pr-naming.md`)을 따른다. 문서 저장소라 PR 은 작업 단위로 묶어 적게 연다.
