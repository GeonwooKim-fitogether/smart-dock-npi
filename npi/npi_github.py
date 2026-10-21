#!/usr/bin/env python3
"""Fitstack NPI 기준(npi.json + tasks.csv)을 GitHub 라벨·마일스톤·이슈로 옮긴다.

  python npi/npi_github.py --grade NPI-A                     미리 보기. GitHub 를 읽지도 쓰지도 않는다
  python npi/npi_github.py --grade NPI-A --out plan.txt      미리 보기를 파일로 (UTF-8)
  python npi/npi_github.py --grade NPI-A --apply OWNER/REPO  실제로 만든다 (gh 로그인 필요)

만드는 것: 라벨(NPI 태스크 · Phase Review · 역할:*), 등급의 시작 단계부터의 마일스톤,
단계마다 표준 태스크 이슈와 Phase Review 이슈 하나. 다시 실행하면 이미 있는 것은 건너뛴다
(이슈는 제목 앞 [태스크 번호], 마일스톤은 제목으로 알아본다). 있는 이슈를 고치거나 지우지 않는다.
사용법: docs/how-to-work.md
"""
import argparse
import csv
import json
import shlex
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
TASK_LABEL = ("NPI 태스크", "1D76DB", "Fitstack NPI 표준 태스크")
GATE_LABEL = ("Phase Review", "D93F0B", "단계 심사. 이 이슈가 닫히면 그 단계 통과")
ROLE_COLOR = "C5DEF5"
FIXED = ("id", "phase", "title", "role")


def load(folder=HERE):
    data = json.loads((folder / "npi.json").read_text(encoding="utf-8"))
    try:
        with open(folder / "tasks.csv", encoding="utf-8-sig", newline="") as f:
            rows = csv.DictReader(f)
            missing = {"id", "phase", "title"} - {h.strip() for h in rows.fieldnames or []}
            tasks = [{k.strip(): (v or "").strip() for k, v in r.items() if k} for r in rows]
    except UnicodeDecodeError:
        sys.exit("tasks.csv 를 UTF-8 로 저장해 주세요 (Excel 이면 'CSV UTF-8(쉼표로 분리)').")
    if missing:
        sys.exit(f"tasks.csv 첫 줄에 {sorted(missing)} 칸이 없다.")
    return data, tasks


def problems(data, tasks, grade):
    """--apply 를 막는 빈 곳·어긋남. 비어 있으면 옮겨도 된다."""
    names = [p["name"] for p in data["phases"]]
    want = data["expect"]
    out = []
    if len(names) != want["phases"]:
        out.append(f"단계가 {len(names)}개다. 기준 문서는 {want['phases']}개")
    if len(tasks) != want["tasks"]:
        out.append(f"표준 태스크가 {len(tasks)}개다. 기준 문서는 {want['tasks']}개")
    bad_ids = sorted(i for i, c in Counter(t["id"] for t in tasks).items() if c > 1 or not i)
    if bad_ids:
        out.append(f"태스크 번호가 비었거나 겹친다: {bad_ids}")
    out += [f"태스크 {t['id']} 의 단계 '{t['phase']}' 가 phases 에 없다" for t in tasks if t["phase"] not in names]
    out += [f"{p['name']} 의 통과 조건(gate)이 비어 있다" for p in data["phases"] if not p["gate"]]
    if not data["gate_rules"]:
        out.append("Phase Review 공통 규칙(gate_rules)이 비어 있다")
    out += [f"등급 {g} 의 시작 단계 '{p}' 가 phases 에 없다" for g, p in data["grades"].items() if p not in names]
    if grade not in data["grades"]:
        out.append(f"등급 '{grade}' 이 grades 에 없다. 있는 것: {', '.join(data['grades']) or '없음'}")
    return out


def plan(data, tasks, grade, repo):
    """만들 것을 순서대로: (종류, 제목, gh 인자). 미리 보기와 실제 실행이 이 목록 하나를 쓴다."""
    names = [p["name"] for p in data["phases"]]
    first = data["grades"].get(grade)
    start = names.index(first) if first in names else len(names)
    roles = sorted({t.get("role", "") for t in tasks} - {""})
    labels = [TASK_LABEL, GATE_LABEL] + [(f"역할:{r}", ROLE_COLOR, f"담당 역할 {r}") for r in roles]
    items = [("label", n, ["label", "create", n, "--color", c, "--description", d, "--force", "-R", repo])
             for n, c, d in labels]
    for i, p in enumerate(data["phases"][start:], start + 1):
        ms = f"{i}. {p['name']}"
        items.append(("milestone", ms, ["api", f"repos/{repo}/milestones", "-f", f"title={ms}",
                                        "-f", f"description=Fitstack NPI {i}단계. 심사 이슈: Phase Review: {ms}"]))
        for t in tasks:
            if t["phase"] == p["name"]:
                role = [f"역할:{t['role']}"] if t.get("role") else []
                items.append(issue(f"[{t['id']}] {t['title']}", task_body(t), [TASK_LABEL[0], *role], ms, repo))
        items.append(issue(f"Phase Review: {ms}", gate_body(p, data), [GATE_LABEL[0]], ms, repo))
    return items


def issue(title, body, labels, milestone, repo):
    argv = ["issue", "create", "-R", repo, "--title", title, "--milestone", milestone, "--body", body]
    for label in labels:
        argv += ["--label", label]
    return ("issue", title, argv)


def cell(v):
    return v.replace("|", "\\|").replace("\n", "<br>")


def task_body(t):
    rows = [("태스크 번호", t["id"]), ("단계", t["phase"]), ("담당 역할", t.get("role", ""))]
    rows += [(k, v) for k, v in t.items() if k not in FIXED]  # 기준 문서의 나머지 칸은 그대로 싣는다
    table = "\n".join(f"| {k} | {cell(v)} |" for k, v in rows if v)
    return ("Fitstack NPI 표준 태스크\n\n| 항목 | 내용 |\n|---|---|\n" + table + "\n\n"
            "끝나면 산출물·근거(PDF, 시험 결과, 관련 이슈)를 댓글로 남기고 이 이슈를 닫는다. "
            "이 프로젝트에 해당하지 않으면 **Close as not planned** 로 닫고 이유를 한 줄 남긴다.")


def gate_body(phase, data):
    todo = "(기준 문서에서 옮겨 올 것)"
    boxes = lambda xs: "\n".join(f"- [ ] {x}" for x in xs) or f"- [ ] {todo}"
    rules = "\n".join(f"- {r}" for r in data["gate_rules"]) or f"- {todo}"
    return (f"{phase['name']} 단계를 마치고 다음 단계로 넘어가도 되는지 심사한다. "
            "아래가 모두 체크되면 이 이슈를 닫는다. 닫힘이 곧 단계 통과다.\n\n"
            f"### 통과 조건 (Fitstack 기준)\n{boxes(phase['gate'])}\n\n"
            f"### Phase Review 규칙 (Fitstack 기준)\n{rules}\n\n"
            f"### GitHub 에서 확인할 것\n{boxes(data['gate_github'])}")


def key(title):
    """같은 이슈를 알아보는 열쇠. 표준 태스크는 제목 뒷부분을 고쳐도 [번호] 로 알아본다."""
    return title.split("]", 1)[0] + "]" if title.startswith("[") else title


def apply(items, repo, run=subprocess.run, pause=1.0):
    gh = lambda *a: run(["gh", *a], check=True, capture_output=True, text=True, encoding="utf-8").stdout
    # 먼저 읽는다. 저장소 이름이 틀리면 여기서 실패해 아무것도 만들지 않는다.
    have = {
        "milestone": set(gh("api", f"repos/{repo}/milestones?state=all&per_page=100", "--paginate",
                            "--jq", ".[].title").splitlines()),
        "issue": {key(t) for t in gh("issue", "list", "-R", repo, "--state", "all", "--limit", "5000",
                                     "--json", "title", "--jq", ".[].title").splitlines()},
    }
    for kind, title, argv in items:
        if key(title) in have.get(kind, ()):
            print("건너뜀 (이미 있음):", title)
            continue
        print("만듦:", title, gh(*argv).strip())
        time.sleep(pause)  # GitHub 은 연달아 만드는 요청에 1초 간격을 권한다 (보조 사용 한도)


def main():
    for stream in (sys.stdout, sys.stderr):  # Windows 에서 파일로 받아도 한글이 깨지지 않게
        stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--grade", required=True, help="등급 (npi.json 의 grades). 그 등급의 시작 단계부터 만든다")
    ap.add_argument("--apply", metavar="OWNER/REPO", help="이 저장소에 실제로 만든다. 없으면 미리 보기만 한다")
    # PowerShell 의 > 는 프로그램 출력을 시스템 코드페이지로 읽어 한글을 깨뜨린다. 파일은 여기서 직접 쓴다.
    ap.add_argument("--out", metavar="FILE", help="미리 보기 명령을 화면 대신 이 파일에 UTF-8 로 저장한다")
    a = ap.parse_args()
    data, tasks = load()
    items = plan(data, tasks, a.grade, a.apply or "OWNER/REPO")
    bad = problems(data, tasks, a.grade)
    if not a.apply:
        preview = "\n\n".join(shlex.join(["gh", *argv]) for _, _, argv in items) + "\n"
        if a.out:
            Path(a.out).write_text(preview, encoding="utf-8")
            print("미리 보기를 저장했다:", a.out)
        else:
            print(preview)
    n = Counter(kind for kind, _, _ in items)
    print(f"라벨 {n['label']}개 · 마일스톤 {n['milestone']}개 · 이슈 {n['issue']}개")
    if bad:
        print("\n기준 데이터에 빈 곳이 있어 --apply 는 실행하지 않는다:", *bad, sep="\n- ")
        sys.exit(1)
    if not a.apply:
        print("미리 보기만 했다. GitHub 는 건드리지 않았다. 만들려면 --apply OWNER/REPO 를 붙인다.")
        return
    try:
        apply(items, a.apply)
    except FileNotFoundError:
        sys.exit("gh 가 없다. 설치(Windows): winget install --id GitHub.cli → 새 창에서 gh auth login")
    except subprocess.CalledProcessError as e:
        sys.exit(f"gh 가 실패했다. 고친 뒤 다시 실행하면 이미 만든 것은 건너뛰고 이어서 한다.\n{e.stderr}")


if __name__ == "__main__":
    main()
