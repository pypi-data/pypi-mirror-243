

'''
	Description:
		This starts the system from internally.
'''


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
	rethink_params = [
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
		* This checks to make sure can't connect to those ports already.
		* The node is started.
		* 
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
	records = 1,
	** keywords
):
	if (records >= 1):
		print ()
		print ('The rethink system "start" course has started.');
		print ()
		
	course_name = "	rethink system start";

	#
	#	check if can connect,
	#	if it can, then there's already a rethinkdb process
	#	running
	#
	if (records >= 1):
		print (f"{ course_name }: Making sure can't connect to an already running process.")
		
	cannot_connect.ensure (loops = 1)

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
	
	if (records >= 1):
		print (f"{ course_name }:script:", script)
		print (f"{ course_name }:rethink_params:", rethink_params)
		print (f"{ course_name }:keywords:", keywords)

	
	class ly:
		def __init__ (this, script):
			this.script = script;
			
			if (records >= 1):
				print ("this.script:", this.script)
			
			this.process = subprocess.Popen (
				shlex.split (script),
				** process_keys
			)
			
			if (records >= 1):
				print ("this.process:", this.process)

			[ r, c ] = ly_connect.start (
				ly_connect.parameters (
					loops = 3
				)
			)
			db_list = r.db_list ().run (c)
			assert (db_list == ['rethinkdb', 'test'])
			
			if (records >= 1):
				print ('A connection to the rethink node was made.')
				
			c.close ()

			atexit.register (this.stop)

			if (wait):
				if (records >= 1):
					print ()
					print ("The rethink process is waiting for an exit signal.")
					print ()
			
				try:
					this.process.wait ()	
				except Exception as E:
					print ("wait exception:", E)

		def stop (this):
			if (records >= 1):
				print ('The rethink node is stopping.')
			
			#time.sleep (1)
		
			try:
				this.process.kill ()	
			except Exception as E:
				print ("stoppage exception:", E)
		

	lymphatic = ly (script)

	
	return lymphatic