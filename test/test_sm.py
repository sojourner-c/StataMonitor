"""Unit test for Stata Monitor"""

import os
import unittest

from lib import stata_monitor


class TestStataMonitor(unittest.TestCase):
	"""Test stata_monitor.py"""

	def setUp(self):
		self.path = os.path.dirname(os.path.abspath(__file__)) + '\\do'
		self.pass_file = self.path + '\\' + 'pass_test.do'
		self.fail_file = self.path + '\\' + 'fail_test.do'
		self.pass_body = 'The program pass_test.do completed without errors.'
		self.fail_body = 'The program fail_test.do terminated due to errors.'


	def test_stata_monitor(self):
		"""Test that stata_monitor runs without errors."""
		stata_monitor.stata_monitor(self.pass_file)
		stata_monitor.stata_monitor(self.fail_file)


	def test_body_no_rc(self):
		"""Test _set_up, _run_program, and _scan_log run with good .do file."""
		self.log_name_tup = stata_monitor._set_up(self.pass_file)
		stata_monitor._run_program(self.pass_file)
		body = stata_monitor._scan_log(self.log_name_tup, True)
		self.assertEqual(body, self.pass_body)


	def test_body_rc(self):
		"""Test _set_up, _run_program, and _scan_log run with bad .do file."""
		self.log_name_tup = stata_monitor._set_up(self.fail_file)
		stata_monitor._run_program(self.fail_file)
		body = stata_monitor._scan_log(self.log_name_tup, True)
		self.assertEqual(body, self.fail_body)
