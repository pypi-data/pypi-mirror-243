

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
		
	if (
		type (positionals [0]) == str and
		type (positionals [1]) == dict and
		len (positionals) == 2
	):
		print (positionals [0], json.dumps (positionals [1], indent = 4))