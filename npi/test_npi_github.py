"""npi_github.py 의 판정을 지키는 시험. 실행: python npi/test_npi_github.py (GitHub 를 부르지 않는다)"""
import subprocess
import unittest

import npi_github as n

DATA = {
    "expect": {"phases": 2, "tasks": 3},
    "phases": [{"name": "Concept", "gate": ["목표 확정"]}, {"name": "Planning", "gate": ["계획 확정"]}],
    "gate_rules": ["심사자는 PM"],
    "gate_github": ["열린 태스크 0건"],
    "grades": {"A": "Concept", "B": "Planning"},
}
TASKS = [
    {"id": "C-01", "phase": "Concept", "title": "목표", "role": "PM", "산출물": "목표서 | v1"},
    {"id": "C-02", "phase": "Concept", "title": "시장", "role": "", "산출물": ""},
    {"id": "P-01", "phase": "Planning", "title": "계획", "role": "HW", "산출물": "계획서"},
]


def titles(items, kind):
    return [t for k, t, _ in items if k == kind]


def arg(argv, flag):
    return argv[argv.index(flag) + 1]


class Npi(unittest.TestCase):
    def test_complete_data_passes(self):
        self.assertEqual(n.problems(DATA, TASKS, "A"), [])

    def test_gaps_are_reported(self):
        bad = n.problems({**DATA, "gate_rules": []}, TASKS[:2] + [{**TASKS[2], "id": "C-01", "phase": "X"}], "Z")
        for words in ("겹친다", "'X'", "gate_rules", "'Z'"):
            self.assertTrue(any(words in p for p in bad), (words, bad))
        self.assertTrue(any("83" in p for p in n.problems({**DATA, "expect": {"phases": 2, "tasks": 83}}, TASKS, "A")))

    def test_grade_picks_start_phase(self):
        a, b = n.plan(DATA, TASKS, "A", "o/r"), n.plan(DATA, TASKS, "B", "o/r")
        self.assertEqual(titles(a, "milestone"), ["1. Concept", "2. Planning"])
        self.assertEqual(titles(a, "issue"), ["[C-01] 목표", "[C-02] 시장", "Phase Review: 1. Concept",
                                              "[P-01] 계획", "Phase Review: 2. Planning"])
        self.assertEqual(titles(b, "milestone"), ["2. Planning"])
        self.assertEqual(titles(b, "issue"), ["[P-01] 계획", "Phase Review: 2. Planning"])
        self.assertEqual(titles(a, "label"), ["NPI 태스크", "Phase Review", "역할:HW", "역할:PM"])

    def test_issue_contents(self):
        argv = {t: v for _, t, v in n.plan(DATA, TASKS, "A", "o/r")}
        task = argv["[C-01] 목표"]
        self.assertEqual(arg(task, "--milestone"), "1. Concept")
        self.assertEqual([task[i + 1] for i, x in enumerate(task) if x == "--label"], ["NPI 태스크", "역할:PM"])
        self.assertIn("| 산출물 | 목표서 \\| v1 |", arg(task, "--body"))  # 표가 깨지지 않게 | 를 막는다
        self.assertNotIn("담당 역할", arg(argv["[C-02] 시장"], "--body"))
        gate = arg(argv["Phase Review: 1. Concept"], "--body")
        for line in ("- [ ] 목표 확정", "- 심사자는 PM", "- [ ] 열린 태스크 0건"):
            self.assertIn(line, gate)

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
        self.assertEqual(sorted(made), sorted(["[C-02] 시장", "Phase Review: 1. Concept", "[P-01] 계획",
                                               "Phase Review: 2. Planning", "title=2. Planning"]))
        self.assertEqual(sum(c[:2] == ["label", "create"] for c in calls), 4)  # 라벨은 --force 로 늘 맞춘다

    def test_repo_data_loads(self):
        data, tasks = n.load()
        n.problems(data, tasks, "NPI-A")
        n.plan(data, tasks, "NPI-A", "o/r")


if __name__ == "__main__":
    unittest.main()
