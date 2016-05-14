from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import sys
import importlib
import os
import json


#This class will handle incoming requests
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		path = urllib.parse.unquote(self.path)
		print('Request Path: {}'.format(path))
		path_list = []
		response = 'No Such File\n'
		if '?' in path:
			path_list = path.split('?')
		else:
			path_list.append(path)
		target_file = '{}{}'.format(os.getcwd(),path_list[0])
		print('Target File: {}'.format(target_file))
		if os.path.exists(target_file):
			response = target_file
			import_dir = target_file.replace(target_file.split('/')[-1],'')
			print('Import Dir: {}'.format(import_dir))
			import_file = target_file.split('/')[-1].replace('.py','')
			if not target_file.replace(target_file.split('/')[-1],'') in sys.path:
				sys.path.append(target_file.replace(target_file.split('/')[-1],''))
			#print('SysPath: {}'.format(sys.path))
			foo = importlib.import_module('{}.{}'.format(import_file,import_file))
			info_dict = {}
			if len(path_list) == 2:
				argument_list = path_list[1].split('&')
				for entry in argument_list:
					response += ' {}'.format(entry)
					info_dict[entry.split('=')[0]] = entry.split('=')[1]
				print(info_dict)
				if 'class' in info_dict:
					foo = getattr(foo,info_dict['class'])()
				if 'method' in info_dict:
					foo = getattr(foo,info_dict['method'])()
					response_dict = {}
					response_dict['output'] = foo
					json_response = json.dumps(response_dict)
					print(json_response)
				print(response)
		response += '\n'
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()
		# send the html message
		self.wfile.write(bytes(json_response,'utf-8'))
		return

if __name__ == '__main__':

	PORT_NUMBER = 8000
	BASE_DIR = os.getcwd()
	if len(sys.argv) == 2:
		PORT_NUMBER = int(sys.argv[1])
	try:
		print('{} {}'.format(BASE_DIR, str(PORT_NUMBER)))
		server = HTTPServer(('',PORT_NUMBER), myHandler)
		print('Started the server on port {}'.format(PORT_NUMBER))
		server.serve_forever()
	except KeyboardInterrupt:
		print('^C  received, shutting down webserver')
		server.socket.close()
