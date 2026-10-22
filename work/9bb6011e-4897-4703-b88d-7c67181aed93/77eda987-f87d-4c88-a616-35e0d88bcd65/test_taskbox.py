"""使用标准库复现核心行为与错误边界：python -m unittest -v。"""

import os
import subprocess
import sys
import unittest
from pathlib import Path

import bugs
from taskbox import (
    TaskNotFound, add_task, complete_task, count_pending,
    filter_tasks, find_task, format_tasks,
)


class TaskboxTests(unittest.TestCase):
    def setUp(self):
        self.tasks = []
        add_task(self.tasks, "  学习 Python  ")
        add_task(self.tasks, "整理作业")

    def test_add_trims_title_and_rejects_blank_without_mutation(self):
        self.assertEqual(self.tasks[0], {"id": 1, "title": "学习 Python", "done": False})
        for title in ("", "   "):
            with self.assertRaisesRegex(ValueError, "任务标题不能为空"):
                add_task(self.tasks, title)
        self.assertEqual(len(self.tasks), 2)

    def test_missing_id_raises_custom_error_without_changing_tasks(self):
        for task_id in (0, -1, 99):
            with self.subTest(task_id=task_id):
                with self.assertRaisesRegex(TaskNotFound, f"找不到任务 {task_id}"):
                    complete_task(self.tasks, task_id)
        self.assertEqual(count_pending(self.tasks), 2)

    def test_complete_only_target_and_repeated_completion_is_safe(self):
        result = complete_task(self.tasks, 2)
        self.assertIs(result, find_task(self.tasks, 2))
        complete_task(self.tasks, 2)
        self.assertFalse(self.tasks[0]["done"])
        self.assertTrue(self.tasks[1]["done"])
        self.assertEqual(count_pending(self.tasks), 1)

    def test_filter_handles_case_unicode_empty_and_missing_keyword(self):
        self.assertEqual(filter_tasks(self.tasks, " PYTHON "), [self.tasks[0]])
        add_task(self.tasks, "Straße")
        self.assertEqual(filter_tasks(self.tasks, "STRASSE"), [self.tasks[2]])
        self.assertEqual(filter_tasks(self.tasks, ""), self.tasks)
        self.assertIsNot(filter_tasks(self.tasks, ""), self.tasks)
        self.assertEqual(filter_tasks(self.tasks, "不存在"), [])

    def test_count_handles_empty_all_pending_and_all_completed(self):
        self.assertEqual(count_pending([]), 0)
        self.assertEqual(count_pending(self.tasks), 2)
        complete_task(self.tasks, 1)
        complete_task(self.tasks, 2)
        self.assertEqual(count_pending(self.tasks), 0)

    def test_format_preserves_original_id_after_filtering(self):
        self.assertEqual(format_tasks([]), "暂无任务")
        self.assertEqual(format_tasks(filter_tasks(self.tasks, "作业")), "2. [ ] 整理作业")
        complete_task(self.tasks, 1)
        self.assertIn("1. [x] 学习 Python", format_tasks(self.tasks))

    def test_fixed_default_has_no_state_leak_and_accepts_explicit_list(self):
        first = bugs.append_fixed("A")
        second = bugs.append_fixed("B")
        self.assertEqual(first, ["A"])
        self.assertEqual(second, ["B"])
        target = ["原有"]
        self.assertIs(bugs.append_fixed("新增", target), target)
        self.assertEqual(target, ["原有", "新增"])

    def test_equal_content_does_not_require_same_identity(self):
        left, right = [1, 2], [1, 2]
        self.assertFalse(bugs.same_content_bad(left, right))
        self.assertTrue(bugs.same_content_fixed(left, right))
        self.assertFalse(bugs.same_content_fixed(left, [2, 1]))

    def test_cli_handles_bad_input_and_eof_without_crashing(self):
        script = Path(__file__).with_name("taskbox.py")
        for commands in ("", "list\ncount\ndone\nabc\nadd\n \nwrong\nquit\n"):
            with self.subTest(commands=commands):
                result = subprocess.run(
                    [sys.executable, str(script)], input=commands,
                    capture_output=True, text=True, encoding="utf-8", timeout=10,
                    env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1"),
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                if commands:
                    self.assertIn("暂无任务", result.stdout)
                    self.assertIn("未完成任务：0", result.stdout)
                    self.assertIn("输入错误", result.stdout)
                    self.assertIn("任务标题不能为空", result.stdout)
                    self.assertIn("未知命令", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
