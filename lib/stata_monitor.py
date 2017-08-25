"""Runs .do File and Sends Email With Completion Status."""

import os
import re
import getpass
import subprocess

import win32com.client as win32


def _set_up(file):
	"""Return tuple with .log loc+name, do filename, then cds to log loc.

	`file` string with full path and  Stata .do file name with extension.
	"""

	log = re.sub('do$', 'log', file)
	i = file.rfind('\\')
	path = file[:i]
	os.chdir(path)
	do_filename = file[i+1:]
	log_name_tup = (log, do_filename)
	return log_name_tup


def _run_program(file, *params):
	"""Run .do file in batch mode and wait till completion.

	`file` string with full path and  Stata .do file name with extension.
	`params` are optional parameters for running .do in batch mode.
	"""

	cmd = [r'\\dc-stata\stata$\StataSE-64.exe', '/e', 'do', file]
	for param in params:
		cmd.append(param)
	a = subprocess.Popen(cmd, shell=True)
	a.wait()


def _send_email(log_name_tup, delete_log):
	"""Calls _scan_log and sends email with returned text as body.

	`log_name_tup` tuple with .log location + name and name of do file.
	"""

	# Get Email Address
	username = getpass.getuser()
	email = username.replace('_', '.')

	# Call Log Reader
	body = _scan_log(log_name_tup, delete_log)

	# Send Email
	outlook = win32.Dispatch('outlook.application')
	mail = outlook.CreateItem(0)
	mail.To = email + '@ei.com'
	mail.Subject = 'Stata Monitor'
	mail.Body = body
	if not delete_log:
		mail.Attachments.Add(log_name_tup[0])
	mail.Send()


def _scan_log(log_name_tup, delete_log):
	"""Returns string with .do completion status for body of email.

	`log_name_tup` tuple with .log location + name and name of do file.
	"""

	log = log_name_tup[0]
	filename = log_name_tup[1]
	# Stata error codes range from 1-999.
	with open(log, 'r') as f:
		for line in f:
			if re.search('r\([1-9][0-9]?[0-9]?[0-9]?\)', line):
				message = 'The program ' + filename + ' terminated due to errors.'
				break
		else:
			message = 'The program ' + filename + ' completed without errors.'
	if delete_log:
		os.remove(log)
	return message


def stata_monitor(file, *params, delete_log=False):
	"""Run .do file, scan log, send email with completion status.

	`file` string with full path and  Stata .do file name with extension.
	`params` are optional parameters for running .do in batch mode.
	"""

	current_cd = os.path.dirname(os.path.abspath(__file__))
	log_name_tup = _set_up(file)
	_run_program(file, *params)
	_send_email(log_name_tup, delete_log)
	os.chdir(current_cd)
