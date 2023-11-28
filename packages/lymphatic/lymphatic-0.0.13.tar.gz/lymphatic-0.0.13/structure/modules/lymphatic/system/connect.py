

'''
	import lymphatic.system.connect as ly_connect
	[ r, c ] = ly_connect.start ()
'''

'''
	[ r, c ] = ly_connect.now (
		connect.parameters (
			loops = 5
		)
	)
'''

from rethinkdb import RethinkDB

import lymphatic.system.climate as climate
import botanical.cycle as cycle

class parameters:
	def __init__ (this, ** keywords):
		print ("keywords:", keywords)
	
		if ("loops" in keywords):
			this.loops = keywords ['loops']
		else:
			this.loops = 10
		
		this.delay = 1


def now (
	params = parameters ()
):
	print ("lymphatic system connect params:", params.loops, params.delay)

	connection_attempt = 1;
	def connect (* positionals, ** keywords):
		print ('connecting')
	
		ports = climate.find ("ports")
		print ("ports", ports)
		
		driver_port = ports ["driver"]
	
		nonlocal connection_attempt;
		print (
			f"Attempting rethink connection on port: { driver_port }, attempt", 	
			connection_attempt
		)
		
		connection_attempt += 1
		
		r = RethinkDB ()
		
		'''	
			conn = r.connect (
				host = 'localhost',
				port = 28015,
				ssl = {
					'ca_certs': '/path/to/ca.crt'
				}
			)
		'''
		c = r.connect (
			host = 'localhost',
			port = driver_port
		)

		print ('rethink connection established')

		return [ r, c ];
		
		

	connection = cycle.loops (
		connect, 
		cycle.presents ([]),
		
		loops = params.loops,
		delay = params.delay,
		
		records = 0
	)
	
	return connection;
	
	
start = now