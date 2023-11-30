
'''
	import lymphatic.system.stop as ly_stop
	ly_stop.beautifully (pid_file_path)
'''

'''
	notes:
		rethinkdb removes the pid file when stopped
		like this.
'''

import lymphatic.system.cannot_connect as cannot_connect

import psutil

def beautifully (pid_file_path):
	FP = open (pid_file_path)
	P_ID = int (FP.read ().strip ())

	#print ("stopping process with ID:", P_ID)

	p = psutil.Process (P_ID)
	p.terminate ()
	
	cannot_connect.ensure (loops = 2)
	
	return;