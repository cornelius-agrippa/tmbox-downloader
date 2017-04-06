# Basic printable colors for the CLI
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

# Based on https://www.djangoproject.com/, removes invalid filename characters
# Available in https://github.com/django/django/blob/master/django/utils/text.py
def getValidFilename(s):
	import re
	s = s.strip().replace(' ', '_')
	return re.sub(r'(?u)[^-\w.]', '', s)