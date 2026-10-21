"""npi_github.py 의 판정을 지키는 시험. 실행: python npi/test_npi_github.py (GitHub 를 부르지 않는다)"""
import re
import subprocess
import unittest
from pathlib import Path

import npi_github as n

REFERENCE = Path(__file__).parent.parent / "reference" / "fitstack-npi-reference.md"  # 커밋하지 않는 기준 자료

DATA = {
    "expect": {"phases": 2, "tasks": 5},
    "phases": [{"name": "Concept", "milestones": ["C-01", "C-03"]},
               {"name": "Planning", "milestones": ["P-01", "P-02"]}],
    "gate_rules": ["심사자는 PM"],
    "gate_github": ["열린 태스크 0건"],
    "grades": {"A": "Concept", "B": "Planning"},
}
TASKS = [
    {"id": "C-01", "phase": "Concept", "title": "목표", "role": "PM", "산출물": "목표서 | v1"},
    {"id": "C-02", "phase": "Concept", "title": "시장", "role": "", "산출물": ""},
    {"id": "C-03", "phase": "Concept", "title": "Concept 심사", "role": "", "산출물": ""},
    {"id": "P-01", "phase": "Planning", "title": "계획", "role": "HW", "산출물": "계획서"},
    {"id": "P-02", "phase": "Planning", "title": "Planning 심사", "role": "", "산출물": ""},
]


def titles(items, kind):
    return [t for k, t, _ in items if k == kind]


def arg(argv, flag):
    return argv[argv.index(flag) + 1]


def labels(argv):
    return [argv[i + 1] for i, x in enumerate(argv) if x == "--label"]


class Npi(unittest.TestCase):
    def test_complete_data_passes(self):
        self.assertEqual(n.problems(DATA, TASKS, "A"), [])

    def test_gaps_are_reported(self):
        bad = n.problems({**DATA, "gate_rules": []}, TASKS[:4] + [{**TASKS[4], "id": "C-01", "phase": "X"}], "Z")
        for words in ("겹친다", "'X'", "gate_rules", "'Z'"):
            self.assertTrue(any(words in p for p in bad), (words, bad))
        self.assertTrue(any("83" in p for p in n.problems({**DATA, "expect": {"phases": 2, "tasks": 83}}, TASKS, "A")))
        phases = [{"name": "Concept", "milestones": ["C-01", "P-01"]}, {"name": "Planning", "milestones": []}]
        bad = n.problems({**DATA, "phases": phases}, TASKS, "A")
        self.assertTrue(any(p.endswith(": P-01") for p in bad), bad)  # 다른 단계의 태스크
        self.assertTrue(any(p.startswith("Planning 의 마일스톤 태스크") for p in bad), bad)  # 게이트가 없다

    def test_grade_picks_start_phase(self):
        a, b = n.plan(DATA, TASKS, "A", "o/r"), n.plan(DATA, TASKS, "B", "o/r")
        self.assertEqual(titles(a, "milestone"), ["1. Concept", "2. Planning"])
        self.assertEqual(titles(a, "issue"), ["[C-01] 목표", "[C-02] 시장", "[C-03] Concept 심사",
                                              "[P-01] 계획", "[P-02] Planning 심사"])
        self.assertEqual(titles(b, "milestone"), ["2. Planning"])
        self.assertEqual(titles(b, "issue"), ["[P-01] 계획", "[P-02] Planning 심사"])
        self.assertEqual(titles(a, "label"), ["NPI 태스크", "Phase Review", "역할:HW", "역할:PM"])

    def test_last_milestone_is_the_phase_review(self):
        issues = {t: labels(v) for k, t, v in n.plan(DATA, TASKS, "A", "o/r") if k == "issue"}
        # 단계마다 하나이고, 게이트 태스크 말고 따로 더 만들지 않는다
        self.assertEqual([t for t, ls in issues.items() if "Phase Review" in ls],
                         ["[C-03] Concept 심사", "[P-02] Planning 심사"])
        # 심사 이슈에 NPI 태스크 라벨도 붙으면 '열린 NPI 태스크가 없다' 확인이 심사 이슈 자신 때문에 채워지지 않는다
        self.assertTrue(all(("Phase Review" in ls) != ("NPI 태스크" in ls) for ls in issues.values()))

    def test_issue_contents(self):
        argv = {t: v for _, t, v in n.plan(DATA, TASKS, "A", "o/r")}
        task = argv["[C-01] 목표"]
        self.assertEqual(arg(task, "--milestone"), "1. Concept")
        self.assertEqual(labels(task), ["NPI 태스크", "역할:PM"])
        self.assertIn("| 산출물 | 목표서 \\| v1 |", arg(task, "--body"))  # 표가 깨지지 않게 | 를 막는다
        self.assertIn("| 마일스톤 태스크 | ★", arg(task, "--body"))
        plain = arg(argv["[C-02] 시장"], "--body")
        self.assertNotIn("담당 역할", plain)
        self.assertNotIn("마일스톤 태스크", plain)
        gate = arg(argv["[C-03] Concept 심사"], "--body")
        for line in ("- [ ] [C-01] 목표", "- 심사자는 PM", "- [ ] 열린 태스크 0건"):
            self.assertIn(line, gate)
        self.assertNotIn("[C-02]", gate)  # ★ 가 아닌 태스크는 체크 항목이 아니다
        self.assertNotIn("[C-03]", gate)  # 게이트 자신도 아니다

    def test_apply_skips_what_exists(self):
        calls = []

        def fake_gh(argv, **_):
            calls.append(argv[1:])
            if "--paginate" in argv:
                out = "1. Concept\n"  # 마일스톤 하나는 이미 있다
            elif argv[1:3] == ["issue", "list"]:
                out = "[C-01] 제목을 사람이 고쳤다\n안건 이슈\n"  # 번호가 같으면 같은 태스크다
            else:
                out = "https://github.com/o/r/issues/9\n"
            return subprocess.CompletedProcess(argv, 0, out, "")

        n.apply(n.plan(DATA, TASKS, "A", "o/r"), "o/r", run=fake_gh, pause=0)
        made = [arg(c, "--title") for c in calls if c[:2] == ["issue", "create"]]
        made += [arg(c, "-f") for c in calls if c[:2] == ["api", "repos/o/r/milestones"]]
        self.assertEqual(sorted(made), sorted(["[C-02] 시장", "[C-03] Concept 심사", "[P-01] 계획",
                                               "[P-02] Planning 심사", "title=2. Planning"]))
        self.assertEqual(sum(c[:2] == ["label", "create"] for c in calls), 4)  # 라벨은 --force 로 늘 맞춘다

    def test_repo_data(self):
        data, tasks = n.load()
        for grade, milestones, issues in (("NPI-A", 5, 83), ("NPI-C", 3, 65)):
            self.assertEqual(n.problems(data, tasks, grade), [])
            items = n.plan(data, tasks, grade, "o/r")
            self.assertEqual((len(titles(items, "milestone")), len(titles(items, "issue"))), (milestones, issues))
        gates = [t for k, t, v in n.plan(data, tasks, "NPI-A", "o/r") if k == "issue" and "Phase Review" in labels(v)]
        self.assertEqual(gates, ["[6] Concept Phase Review", "[18] Planning Phase Review",
                                 "[53] Development Phase Review", "[72] Release to Manufacturing Review",
                                 "[83] Launch Product"])

    @unittest.skipUnless(REFERENCE.exists(), "기준 자료가 이 컴퓨터에 없다 (저장소에 커밋하지 않는 파일)")
    def test_repo_data_matches_reference(self):
        """npi.json + tasks.csv 로 기준 자료의 단계·태스크 줄을 다시 써서 원문과 한 줄씩 대조한다."""
        data, tasks = n.load()
        stars = {m for p in data["phases"] for m in p["milestones"]}
        rebuilt = []
        for p in data["phases"]:
            rebuilt.append(f"## {p['name']}")
            rebuilt += [f"{t['id']}. {'★ ' if t['id'] in stars else ''}{t['title']}"
                        for t in tasks if t["phase"] == p["name"]]
        original = [s for s in REFERENCE.read_text(encoding="utf-8").splitlines() if re.match(r"## |\d+\. ", s)]
        self.assertEqual(rebuilt, original)


if __name__ == "__main__":
    unittest.main()
