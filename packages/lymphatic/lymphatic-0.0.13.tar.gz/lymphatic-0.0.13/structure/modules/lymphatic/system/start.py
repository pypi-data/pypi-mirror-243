





'''
import lymphatic.system.climate as ly_system_climate
ly_system_climate.change ("ports", {
	"driver": 18871,
	"cluster": 0,
	"http": 0	
})

import pathlib
import lymphatic.system.start as ly_system_start
ly = ly_system_start.now (
	process = {
		"cwd": pathlib.Path (__file__).parent.resolve ()
	},
	rethinkdb = [
		f"--daemon",
		f"--pid-file {}"
	],
	wait = True
)

# ly.process.wait ()

ly.stop ()
'''

'''
	steps:
		check to make sure can't connect
'''

'''
setsid
'''

import subprocess
import shlex

import lymphatic.system.climate as climate
import lymphatic.system.cannot_connect as cannot_connect
import lymphatic.system.connect as ly_connect
	
import atexit
import time
def now (
	rethink_params = [],
	** keywords
):
	#
	#	check if can connect,
	#	if it can, then there's already a rethinkdb process
	#	running
	#
	cannot_connect.ensure (
		loops = 2
	)

	# ports = params ["ports"]
	process_keys = keywords ["process"]
	
	if ("wait" in keywords):
		wait = keywords ["wait"]
	else:
		wait = False

	ports = climate.find ("ports")
	driver_port = str (ports ["driver"])
	cluster_port = str (ports ["cluster"])
	http_port = str (ports ["http"])

	script = " ".join ([
		"rethinkdb",
		f"--driver-port { driver_port }",
		f"--cluster-port { cluster_port }",
		f"--http-port { http_port }",
		
		* rethink_params
	])
	
	
	print ("script:", script)
	print ("rethink_params:", rethink_params)
	print ("keywords:", keywords)

	
	class ly:
		def __init__ (this, script):
			this.script = script;
			print ("this.script:", this.script)
			
			this.process = subprocess.Popen (
				shlex.split (script),
				** process_keys
			)
			
			print ("this.process:", this.process)

			[ r, c ] = ly_connect.start ()
			print ('A connection to the rethink node was made.')
			c.close ()

			atexit.register (this.stop)

			if (wait):
				print ()
				print ("The rethink process is waiting for an exit signal.")
				print ()
			
				try:
					this.process.wait ()	
				except Exception as E:
					print ("wait exception:", E)

		def stop (this):
			print ('stopping rethinkdb')
			
			time.sleep (1)
		
			try:
				this.process.kill ()	
			except Exception as E:
				print ("stoppage exception:", E)
		

	lymphatic = ly (script)

	
	return lymphatic