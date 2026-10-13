# Smart Dock NPI — 무선 추출 기획·논의 저장소

Smart Dock(DKPX-2 / DKPY-2)을 **LiveHub 없이 Dock 혼자 무선으로 추출·업로드하는 제품**으로 만드는 NPI 기획을 모으고 이어서 논의하는 곳입니다.
공식 기록(게이트 통과·증거)은 사내 시스템 Fitstack 의 NPI 게이트에 남기고, 이 저장소는 그 앞단의 **작업장**입니다.
GitHub · Fitstack · Claude 를 함께 쓰는 방법은 [`docs/working-model.md`](docs/working-model.md) 에 있습니다.

## 지금 어디까지 왔나 (2026-10-13 기준)

| 항목 | 상태 |
|---|---|
| NPI 단계 | 1 · Concept 진행 중 (통과 조건 4건 중 1건 충족) |
| 기획 덱 | v1 (16쪽) — [`exports/SmartDock_기획_2026-09-30.pdf`](exports/SmartDock_기획_2026-09-30.pdf) |
| 1차 미팅 | 2026-09-30 — [`meetings/2026-09-30.md`](meetings/2026-09-30.md) |
| 다음 미팅 | 미정 |
| 결정 기록 | [`decisions.md`](decisions.md) |

## 열린 안건 (다음 미팅에서 논의)

GitHub 이슈 하나가 안건 하나입니다. 의견은 이슈 댓글로 남겨 주세요.

1. [#2](../../issues/2) 업로드 경로 A안(Wi-Fi 모듈이 핫스팟 접속) vs B안(SBC가 직접 접속) — 덱 5-A~5-C쪽
2. [#3](../../issues/3) 업로드 결과 알림 방식 (4개 안의 조합) — 덱 7쪽
3. [#4](../../issues/4) 사용 환경 1안(실내 한정) / 2안(야외 포함) — 덱 12쪽
4. [#5](../../issues/5) 배터리 방식 (18650 권고 vs 셀 배터리 공용) — 덱 10쪽
5. [#6](../../issues/6) Dock Wi-Fi 이름 체계 (모든 Dock 공통 vs Dock별 고유, 예외 E1·E2) — 덱 12쪽·참고쪽
6. [#7](../../issues/7) 사용자 플로우 세부 (연결 즉시 Dock 화면 자동 표시 · 핫스팟 정보 저장 대수 · Android 대응) — 덱 6쪽
7. [#8](../../issues/8) 성공 기준 v3 승인 — 덱 12쪽

## 폴더

```
README.md        지금 상태 · 열린 안건 (이 파일)
decisions.md     결정 기록 — 언제 · 무엇을 · 왜. 뒤집을 때는 고치지 않고 새 줄로 추가
meetings/        미팅별 기록 (안건 · 정리된 방향 · 결정 · 할 일)
exports/         미팅에 쓴 PDF (Fitstack 게이트 증거로도 올림)
deck/            기획 덱 HTML 과 다시 만드는 스크립트 (deck/src)
mockups/         Dock 웹 화면 목업 (DataManager 스타일)
reference/       9/29 사전 검토 자료 (성공 기준 v2, CEO 브리프, 무선 추출 검토, KEE 감수)
assets/cell/     셀 X 외곽선 SVG (덱·목업에서 셀을 그릴 때 사용)
tests/           실기 시험 계획과 결과
```

`.claude/`, `.github/`, `docs/system-layer/`, `templates/`, `tools/` 등은 회사 공용 템플릿(Template-repository)에서 따라온 것입니다. Claude 가 일할 때 쓰는 규칙·도구이니 지우지 마세요.

## 미팅 한 번의 흐름

1. **미팅 전** — 열린 이슈 목록이 곧 안건입니다. 실기 시험 결과는 해당 이슈에 댓글로 남깁니다.
2. **미팅 중** — `meetings/날짜.md` 에 결정과 할 일을 적습니다.
3. **미팅 후** — 결정된 이슈를 닫고 `decisions.md` 에 한 줄 추가 → 덱 수정 → PDF 를 `exports/` 에 → 같은 PDF 를 Fitstack 게이트 증거로 올림 → 슬랙에 요약 공유.

## 덱·목업 다시 만들기

```bash
cd deck/src && sh build.sh                                     # deck/smart-dock-slide-asis-tobe.html
python3 make_pdf.py ../../exports/SmartDock_기획_YYYY-MM-DD.pdf  # PDF (Playwright 필요)
cd mockups/web-mock && python3 build_mock.py                    # mockups/smart-dock-web-mock.html
```
