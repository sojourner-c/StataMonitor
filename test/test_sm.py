"""Unit test for Stata Monitor"""

import unittest


class TestStataMonitor(unittest.TestCase):
	"""Test stata_monitor.py"""

	def setUp(self):
		self.path = r'C:\Users\sojourner_c\AppData\Local\Programs\Python\Personal Projects\Stata_Monitor\test\do'
		self.pass_file = 'pass_test.do'
		self.fail_file = 'fail_test.do'


	def test_no_rc(self):
		"""Description"""
		pass


	def test_rc(self):
		"""Description"""
		pass
