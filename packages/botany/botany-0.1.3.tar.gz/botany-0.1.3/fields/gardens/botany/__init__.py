

'''
	botany
'''

import json


def show (* positionals):
	if (
		type (positionals [0]) == dict and
		len (positionals) == 1
	):
		print (json.dumps (positionals [0], indent = 4))