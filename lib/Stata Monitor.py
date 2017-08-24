"""Runs .do File and Sends Email With Completion Status."""

import os
import re
import subprocess

import getpass
import win32com.client as win32


def _run_program(FileName, *params):
    """Run .do file in batch mode."""

    cmd = [r'\\dc-stata\stata$\StataSE-64.exe', '/e', 'do', FileName]
    for param in params:
        cmd.append(param)
    a = subprocess.Popen(cmd, shell=True)
    a.wait()


def _send_email():
    """Get Email Address, Call Log Scanner, and Email Result."""

    # Get Email Address
    username = getpass.getuser()
    email = username.replace('_', '.')

    # Call Log Reader
    log = re.sub('do$', 'log', filename)
    cd = os.path.dirname(os.path.abspath(__file__))
    body =  _scan_log(os.path.join(cd, log))

    # Send Email
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = email + '@ei.com'
    mail.Subject = 'Stata Monitor'
    mail.Body = body
    mail.Send()


def _scan_log(logFileName):
    """Returns string with .do completion status for body of email.

	`logFileName` is a .log file in directory of the .do file.

	Opens log file, checks for Stata return code, deletes log.
	"""

    # Stata error codes range from 1-999.
    with open(logFileName, 'r') as f:
        for line in f:
            if re.search('r\([1-9][0-9]?[0-9]?[0-9]?\)', line):
                message = 'The program ' + filename + ' terminated due to errors.'
                break
        else:
            message = 'The program ' + filename + ' completed without errors.'
    os.remove(logFileName)
    return message


def stata_monitor(path, filename, *params):
    """Run .do file, scan log, send email with completion status.

	`path` is a string of the directory containing `filename`.
	`filename` is a Stata .do file including the extension.
	`params` are optional parameters for running .do in batch mode.
	"""

    _run_program(os.path.join(path, filename), *params)
    _send_email()
