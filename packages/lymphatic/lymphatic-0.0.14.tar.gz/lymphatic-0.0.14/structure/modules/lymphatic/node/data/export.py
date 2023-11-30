

'''
	http://www.rethinkdb.com/docs/install-drivers/python/
	
	rethinkdb export -d 2 -c 127.0.0.1:33018
'''



'''
	rethinkdb dump 
	[-c HOST:PORT] 
	[-p] [--password-file FILENAME] 
	[--tls-cert FILENAME] 
	[-f FILE] 
	[--clients NUM] 
	[-e (DB | DB.TABLE)]
'''

'''
	???
		rethinkdb dump
'''

import subprocess
import shlex

def vividly ():	
	script = " ".join ([
		"rethinkdb export -d 2 -c 127.0.0.1:33018"
	])

	this.process = subprocess.Popen (
		shlex.split (script),
		** process_keys
	)