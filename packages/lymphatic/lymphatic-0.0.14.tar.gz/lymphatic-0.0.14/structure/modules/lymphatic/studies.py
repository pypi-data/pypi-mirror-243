

'''
	use revenue instead
'''


'''
	https://stackoverflow.com/questions/42341039/remove-cache-in-a-python-http-server
'''
def OPEN_2 ():
	import http.server

	PORT = 47382

	class HANDLER (
		http.server.SimpleHTTPRequestHandler
	):
		def send_response_only (
			THIS, 
			code, 
			message = None
		):
			super ().send_response_only (code, message)
			THIS.send_header ('Cache-Control', 'no-store, must-revalidate')
			THIS.send_header ('Expires', '0')

	http.server.test(
		HandlerClass = HANDLER,
		port = PORT
	)


def OPEN ():	
	import pathlib
	from os.path import dirname, join, normpath
	import sys
	
	this_folder = pathlib.Path (__file__).parent.resolve ()	
	# normpath (join (this_folder, path))


	print ("python3 -m http.server 47382")

	
	


