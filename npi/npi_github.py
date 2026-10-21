#!/usr/bin/env python3
"""Fitstack NPI 등급별 태스크(npi.json + tasks.csv)를 GitHub 라벨·마일스톤·이슈로 옮긴다.

  python npi/npi_github.py --grade NPI-A                     미리 보기. GitHub 를 읽지도 쓰지도 않는다
  python npi/npi_github.py --grade NPI-A --out plan.txt      미리 보기를 파일로 (UTF-8)
  python npi/npi_github.py --grade NPI-A --apply OWNER/REPO  실제로 만든다 (gh 로그인 필요)

만드는 것: 라벨(NPI 태스크 · 역할:*), 등급이 거치는 단계마다 마일스톤, 등급에 깔리는 Fitstack 태스크
하나마다 이슈 하나. 단계 통과(Phase Review)와 게이트 승인은 Fitstack 에서만 하므로 심사 이슈는 만들지
않는다. 다시 실행하면 이미 있는 것은 건너뛴다(이슈는 제목 앞 [태스크 번호], 마일스톤은 제목으로 알아본다).
있는 이슈를 고치거나 지우지 않는다. 사용법: docs/how-to-work.md
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
TASK_LABEL = ("NPI 태스크", "1D76DB", "Fitstack NPI 태스크")
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
    names, want = data["phases"], data["expect"]
    out = []
    if len(tasks) != want["tasks"]:
        out.append(f"태스크가 {len(tasks)}개다. 기준 문서는 {want['tasks']}개")
    bad_ids = sorted(i for i, c in Counter(t["id"] for t in tasks).items() if c > 1 or not i)
    if bad_ids:
        out.append(f"태스크 번호가 비었거나 겹친다: {bad_ids}")
    out += [f"태스크 {t['id']} 의 단계 '{t['phase']}' 가 phases 에 없다" for t in tasks if t["phase"] not in names]
    out += [f"태스크 {t['id']} 의 역할 '{t.get('role', '')}' 이 roles 에 없다"
            for t in tasks if t.get("role") not in data["roles"]]
    for g, gates in data["grades"].items():
        out += [f"등급 {g} 의 단계 '{p}' 가 phases 에 없다" for p in gates if p not in names]
        count = sum(1 for t in tasks if t.get(g))
        if count != want["grades"].get(g):
            out.append(f"등급 {g} 의 태스크가 {count}개다. 기준 문서는 {want['grades'].get(g)}개")
    if grade not in data["grades"]:
        out.append(f"등급 '{grade}' 이 grades 에 없다. 있는 것: {', '.join(data['grades']) or '없음'}")
    return out


def plan(data, tasks, grade, repo):
    """만들 것을 순서대로: (종류, 제목, gh 인자). 미리 보기와 실제 실행이 이 목록 하나를 쓴다."""
    gates = data["grades"].get(grade, [])
    hide = {*FIXED, *data["grades"]}  # 등급 칸(O·인증시)은 본문 표에 그대로 싣지 않는다
    labels = [TASK_LABEL] + [(f"역할:{r}", ROLE_COLOR, f"담당 역할 {r}") for r in data["roles"]]
    items = [("label", n, ["label", "create", n, "--color", c, "--description", d, "--force", "-R", repo])
             for n, c, d in labels]
    for i, p in enumerate(data["phases"], 1):  # 앞 번호는 등급과 관계없는 고정 순번이다
        if p not in gates:
            continue
        ms = f"{i}. {p}"
        items.append(("milestone", ms, ["api", f"repos/{repo}/milestones", "-f", f"title={ms}",
                                        "-f", f"description=Fitstack NPI {p} 단계. 단계 통과(Phase Review)는 Fitstack 에서 한다"]))
        for t in tasks:
            # 소속 단계가 이 등급에 없으면 등급의 첫 단계로 내려온다 (Fitstack npi.ts tasksFor)
            if t.get(grade) and (t["phase"] if t["phase"] in gates else gates[0]) == p:
                role = [f"역할:{t['role']}"] if t.get("role") else []
                items.append(issue(f"[{t['id']}] {t['title']}", task_body(t, p, t[grade], hide),
                                   [TASK_LABEL[0], *role], ms, repo))
    return items


def issue(title, body, labels, milestone, repo):
    argv = ["issue", "create", "-R", repo, "--title", title, "--milestone", milestone, "--body", body]
    for label in labels:
        argv += ["--label", label]
    return ("issue", title, argv)


def cell(v):
    return v.replace("|", "\\|").replace("\n", "<br>")


def task_body(t, phase, mark="O", hide=FIXED):
    rows = [("태스크 번호", t["id"]), ("단계", phase), ("담당 역할", t.get("role", "")),
            ("해당 조건", "" if mark == "O" else mark)]  # 예: 인증시 = 인증이 필요한 프로젝트만
    rows += [(k, v) for k, v in t.items() if k not in hide]  # 기준 문서의 나머지 칸은 그대로 싣는다
    table = "\n".join(f"| {k} | {cell(v)} |" for k, v in rows if v)
    return ("Fitstack NPI 태스크\n\n| 항목 | 내용 |\n|---|---|\n" + table + "\n\n"
            "끝나면 산출물·근거(PDF, 시험 결과, 관련 이슈, Fitstack 링크)를 댓글로 남기고 이 이슈를 닫는다. "
            "이 프로젝트에 해당하지 않으면 **Close as not planned** 로 닫고 이유를 한 줄 남긴다. "
            "단계 통과(Phase Review)는 Fitstack 에서 한다.")


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
    ap.add_argument("--grade", required=True, help="등급 (npi.json 의 grades: NPI-A·NPI-B·NPI-C). 그 등급의 단계와 태스크만 만든다")
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
