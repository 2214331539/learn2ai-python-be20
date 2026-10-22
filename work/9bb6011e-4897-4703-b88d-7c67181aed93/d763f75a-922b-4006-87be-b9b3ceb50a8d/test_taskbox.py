"""标准库测试：检查重构后的行为、列表独立性和装饰器契约。"""

import inspect
import os
from pathlib import Path
import subprocess
import sys
import unittest

from taskbox import (
    Task, TaskNotFound, add_task, complete_task, count_pending,
    filter_tasks, find_task, format_tasks, log_call,
)


class TaskboxTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tasks: list[Task] = []
        add_task(self.tasks, "  学习 Python  ")
        add_task(self.tasks, "整理作业")

    def test_add_trims_title_and_rejects_blank_without_mutation(self) -> None:
        self.assertEqual(self.tasks[0], Task(id=1, title="学习 Python"))
        with self.assertLogs("taskbox", level="INFO"):
            with self.assertRaisesRegex(ValueError, "任务标题不能为空"):
                add_task(self.tasks, "   ")
        self.assertEqual(len(self.tasks), 2)

    def test_complete_and_missing_id_preserve_other_tasks(self) -> None:
        self.assertIs(complete_task(self.tasks, 2), find_task(self.tasks, 2))
        complete_task(self.tasks, 2)
        self.assertFalse(self.tasks[0].done)
        self.assertTrue(self.tasks[1].done)
        for task_id in (0, -1, 99):
            with self.subTest(task_id=task_id), self.assertLogs("taskbox", level="WARNING"):
                with self.assertRaisesRegex(TaskNotFound, f"找不到任务 {task_id}"):
                    complete_task(self.tasks, task_id)
        self.assertEqual(count_pending(self.tasks), 1)

    def test_filter_count_and_display_keep_previous_behavior(self) -> None:
        self.assertEqual(filter_tasks(self.tasks, " PYTHON "), [self.tasks[0]])
        add_task(self.tasks, "Straße")
        self.assertEqual(filter_tasks(self.tasks, "STRASSE"), [self.tasks[2]])
        self.assertEqual(filter_tasks(self.tasks, ""), self.tasks)
        self.assertIsNot(filter_tasks(self.tasks, ""), self.tasks)
        self.assertEqual(filter_tasks(self.tasks, "不存在"), [])
        self.assertEqual(format_tasks(filter_tasks(self.tasks, "作业")), "2. [ ] 整理作业")
        self.assertEqual(format_tasks([]), "暂无任务")
        self.assertEqual(count_pending([]), 0)
        self.assertEqual(count_pending(self.tasks), 3)
        for task_id in (1, 2, 3):
            complete_task(self.tasks, task_id)
        self.assertEqual(count_pending(self.tasks), 0)
        self.assertIn("1. [x] 学习 Python", format_tasks(self.tasks))

    def test_each_task_owns_its_default_tags(self) -> None:
        self.tasks[0].tags.append("Python")
        self.assertEqual(self.tasks[0].tags, ["Python"])
        self.assertEqual(self.tasks[1].tags, [])

    def test_input_tags_are_copied_instead_of_shared(self) -> None:
        source_tags = ["学习"]
        task = add_task(self.tasks, "写测试", source_tags)
        source_tags.append("后来添加")
        task.tags.append("任务专属")
        self.assertEqual(source_tags, ["学习", "后来添加"])
        self.assertEqual(task.tags, ["学习", "任务专属"])

    def test_decorator_preserves_name_docstring_annotations_and_signature(self) -> None:
        def example(value: int, step: int = 1) -> int:
            """供元信息检查的例子。"""
            return value + step

        wrapped = log_call(example)
        self.assertEqual(wrapped.__name__, example.__name__)
        self.assertEqual(wrapped.__doc__, example.__doc__)
        self.assertEqual(wrapped.__annotations__, example.__annotations__)
        self.assertEqual(inspect.signature(wrapped), inspect.signature(example))
        self.assertIs(wrapped.__wrapped__, example)

    def test_decorator_returns_original_result_and_logs_without_arguments(self) -> None:
        @log_call
        def echo(value: object) -> object:
            return value

        marker = object()
        with self.assertLogs("taskbox", level="INFO") as logs:
            result = echo(marker)
        self.assertIs(result, marker)
        self.assertEqual(logs.output, ["INFO:taskbox:echo: 开始", "INFO:taskbox:echo: 完成"])

    def test_decorator_reraises_same_exception_and_does_not_log_success(self) -> None:
        error = ValueError("用于验证的异常")

        @log_call
        def fail() -> None:
            raise error

        with self.assertLogs("taskbox", level="INFO") as logs:
            with self.assertRaises(ValueError) as caught:
                fail()
        self.assertIs(caught.exception, error)
        self.assertEqual(logs.output, ["INFO:taskbox:fail: 开始", "WARNING:taskbox:fail: 失败"])

    def test_cli_handles_bad_input_and_eof_without_crashing(self) -> None:
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
