#!/usr/bin/env python


from task import Task
import unittest


class TaskTestCase(unittest.TestCase):
    """
    Tests for `task.py`
    """

    def test_main_spec(self):
        """Test if main specification requisites are true"""
        zero_index = ['TR1', 4, 'CHR1', 7]
        df = list(Task.passing_tasks('main_spec'))
        condition = df == zero_index
        self.assertTrue(condition)

    def test_bells(self):
        zero_index = ['TR1', 4, 'CHR1', 1]
        df = list(Task.passing_tasks('bells_and_whistles'))
        condition = df == zero_index
        self.assertTrue(condition)


if __name__ == "__main__":
    unittest.main()