"""npi_github.py 의 판정을 지키는 시험. 실행: python npi/test_npi_github.py (GitHub 를 부르지 않는다)"""
import csv
import re
import subprocess
import unittest
from pathlib import Path

import npi_github as n

REFERENCE = Path(__file__).parent.parent / "reference" / "fitstack-npi-reference.md"  # 커밋하지 않는 기준 자료

DATA = {
    "expect": {"tasks": 4, "grades": {"A": 4, "B": 2, "C": 2}},
    "phases": ["Concept", "Planning", "Development"],
    "grades": {"A": ["Concept", "Planning", "Development"], "B": ["Concept", "Development"], "C": ["Development"]},
    "roles": ["PM", "HW"],
}
TASKS = [
    {"id": "1", "phase": "Concept", "title": "목표", "role": "PM", "A": "O", "B": "O", "C": "O", "산출물": "목표서 | v1"},
    {"id": "2", "phase": "Planning", "title": "인증 계획", "role": "PM", "A": "인증시", "B": "인증시", "C": "", "산출물": ""},
    {"id": "3", "phase": "Planning", "title": "요구사항", "role": "HW", "A": "O", "B": "", "C": "", "산출물": ""},
    {"id": "4", "phase": "Development", "title": "설계", "role": "HW", "A": "O", "B": "", "C": "O", "산출물": ""},
]
# 기준 자료 34줄 표의 게이트 칸 → tasks.csv 의 phase. 'first' 는 Concept 으로 적고 내려오기 규칙에 맡긴다(npi.json)
GATE = {"concept": "Concept", "planning": "Planning", "development": "Development",
        "rtm": "Release to Manufacturing", "launch": "Launch", "first(각 등급 첫 게이트)": "Concept"}


def titles(items, kind):
    return [t for k, t, _ in items if k == kind]


def arg(argv, flag):
    return argv[argv.index(flag) + 1]


def labels(argv):
    return [argv[i + 1] for i, x in enumerate(argv) if x == "--label"]


def milestone_of(items):
    return {t: arg(v, "--milestone") for k, t, v in items if k == "issue"}


class Npi(unittest.TestCase):
    def test_complete_data_passes(self):
        self.assertEqual(n.problems(DATA, TASKS, "A"), [])

    def test_gaps_are_reported(self):
        broken = TASKS[:3] + [{**TASKS[3], "id": "1", "phase": "Y", "role": "ZZ", "C": ""}]
        bad = n.problems({**DATA, "grades": {**DATA["grades"], "B": ["Concept", "X"]}}, broken, "Z")
        for words in ("겹친다", "'Y'", "'ZZ'", "'X'", "'Z'", "등급 C 의 태스크가 1개"):
            self.assertTrue(any(words in p for p in bad), (words, bad))
        self.assertTrue(any("34" in p for p in n.problems({**DATA, "expect": {**DATA["expect"], "tasks": 34}}, TASKS, "A")))

    def test_grade_picks_its_phases(self):
        a, b, c = (n.plan(DATA, TASKS, g, "o/r") for g in "ABC")
        self.assertEqual(titles(a, "milestone"), ["1. Concept", "2. Planning", "3. Development"])
        self.assertEqual(titles(a, "issue"), ["[1] 목표", "[2] 인증 계획", "[3] 요구사항", "[4] 설계"])
        # B 는 Planning 을 건너뛴다. Planning 소속인 2번은 B 의 첫 단계 Concept 으로 내려온다
        self.assertEqual(titles(b, "milestone"), ["1. Concept", "3. Development"])
        self.assertEqual(milestone_of(b), {"[1] 목표": "1. Concept", "[2] 인증 계획": "1. Concept"})
        # C 는 Development 하나다. Concept 소속인 1번은 Development 로 내려온다
        self.assertEqual(milestone_of(c), {"[1] 목표": "3. Development", "[4] 설계": "3. Development"})
        # 역할 라벨은 등급과 관계없이 roles 전부를 만든다
        self.assertEqual(titles(a, "label"), ["NPI 태스크", "역할:PM", "역할:HW"])
        self.assertEqual(titles(c, "label"), titles(a, "label"))

    def test_issue_contents(self):
        items = n.plan(DATA, TASKS, "A", "o/r")
        argv = {t: v for _, t, v in items}
        task = argv["[1] 목표"]
        self.assertEqual(arg(task, "--milestone"), "1. Concept")
        self.assertEqual(labels(task), ["NPI 태스크", "역할:PM"])
        body = arg(task, "--body")
        self.assertIn("| 산출물 | 목표서 \\| v1 |", body)  # 표가 깨지지 않게 | 를 막는다
        self.assertNotIn("해당 조건", body)
        self.assertNotIn("| A |", body)  # 등급 칸은 본문 표에 싣지 않는다
        self.assertIn("| 해당 조건 | 인증시 |", arg(argv["[2] 인증 계획"], "--body"))
        # 단계 통과(Phase Review)는 Fitstack 에서만 한다. GitHub 에는 심사 라벨도 심사 이슈도 없다
        self.assertEqual({l for _, _, v in items for l in labels(v)}, {"NPI 태스크", "역할:PM", "역할:HW"})

    def test_apply_skips_what_exists(self):
        calls = []

        def fake_gh(argv, **_):
            calls.append(argv[1:])
            if "--paginate" in argv:
                out = "1. Concept\n"  # 마일스톤 하나는 이미 있다
            elif argv[1:3] == ["issue", "list"]:
                out = "[1] 제목을 사람이 고쳤다\n안건 이슈\n"  # 번호가 같으면 같은 태스크다
            else:
                out = "https://github.com/o/r/issues/9\n"
            return subprocess.CompletedProcess(argv, 0, out, "")

        n.apply(n.plan(DATA, TASKS, "A", "o/r"), "o/r", run=fake_gh, pause=0)
        made = [arg(c, "--title") for c in calls if c[:2] == ["issue", "create"]]
        made += [arg(c, "-f") for c in calls if c[:2] == ["api", "repos/o/r/milestones"]]
        self.assertEqual(sorted(made), sorted(["[2] 인증 계획", "[3] 요구사항", "[4] 설계",
                                               "title=2. Planning", "title=3. Development"]))
        self.assertEqual(sum(c[:2] == ["label", "create"] for c in calls), 3)  # 라벨은 --force 로 늘 맞춘다

    def test_repo_data(self):
        data, tasks = n.load()
        for grade, milestones, issues in (("NPI-A", 5, 34), ("NPI-B", 3, 16), ("NPI-C", 2, 5)):
            self.assertEqual(n.problems(data, tasks, grade), [])
            items = n.plan(data, tasks, grade, "o/r")
            self.assertEqual([len(titles(items, k)) for k in ("label", "milestone", "issue")], [8, milestones, issues])
        self.assertEqual(titles(n.plan(data, tasks, "NPI-A", "o/r"), "milestone")[-1], "5. Launch")
        b, c = (milestone_of(n.plan(data, tasks, g, "o/r")) for g in ("NPI-B", "NPI-C"))
        self.assertEqual(b["[5] 인증 계획 확정"], "1. Concept")  # 기준 자료의 예: B급 인증 계획 확정 → Concept
        self.assertEqual(c["[3] 대상 제품 연결"], "3. Development")  # 각 등급의 첫 게이트

    @unittest.skipUnless(REFERENCE.exists(), "기준 자료가 이 컴퓨터에 없다 (저장소에 커밋하지 않는 파일)")
    def test_repo_data_matches_reference(self):
        """tasks.csv 를 기준 자료의 34줄 표(npi.ts NPI_TASK_SET)와 한 칸씩 대조한다."""
        _, tasks = n.load()
        rows = [[c.strip() for c in s.split("|")[1:-1]]
                for s in REFERENCE.read_text(encoding="utf-8").splitlines() if re.match(r"\| \d+ \|", s)]
        want = [{"id": r[0], "phase": GATE[r[1]], "title": r[2], "role": r[5],
                 **{g: "" if c == "–" else c for g, c in zip(("NPI-A", "NPI-B", "NPI-C"), r[6:9])}} for r in rows]
        self.assertEqual(tasks, want)

    @unittest.skipUnless(REFERENCE.exists(), "기준 자료가 이 컴퓨터에 없다 (저장소에 커밋하지 않는 파일)")
    def test_library_matches_reference(self):
        """83개 라이브러리를 기준 자료 첫 절(templates.ts)의 줄 모양으로 다시 써서 원문과 한 줄씩 대조한다."""
        with open(n.HERE / "task-library.csv", encoding="utf-8-sig", newline="") as f:
            lib = list(csv.DictReader(f))
        rebuilt = []
        for p in dict.fromkeys(t["phase"] for t in lib):
            rebuilt.append(f"## {p}")
            rebuilt += [f"{t['id']}. {t['milestone'] + ' ' if t['milestone'] else ''}{t['title']}"
                        for t in lib if t["phase"] == p]
        first = REFERENCE.read_text(encoding="utf-8").split("\n---\n")[0]
        self.assertEqual(rebuilt, [s for s in first.splitlines() if re.match(r"## |\d+\. ", s)])


if __name__ == "__main__":
    unittest.main()
