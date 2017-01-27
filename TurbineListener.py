#!/usr/bin/env python
import socket, sys, thread, time
from socket import error as socket_error

class TurbineListener:
	serversocket = None 
	clientsocket = None
	go = True

	# create server to listen for Data Turbine connection
	def __init__(self):
		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.serversocket.bind(('', 12345))
		# listen for only one connection
		self.serversocket.listen(1)
		print "Wifi server started"

	# wait for a connection from the Data Turbine
	def waitForConnection(self):
		if self.clientsocket == None:
			connected = False
			while not connected:
				try:
					sys.stdout.write('Waiting for DataTurbine connection... ')
					sys.stdout.flush()
					(self.clientsocket, address) = self.serversocket.accept()
					connected = True
					print 'Turbine connected'
				except Exception as msg:
					print 'Client connection failed with message:'
					print msg
					print 'I will retry connecting in one second.'
					time.sleep(1)

	# reset the connection to the Data Turbine
	# This usually only happens after the DT has disconnected
	def resetClient(self):
		if self.clientsocket:
			self.clientsocket.close()
		self.clientsocket = None

	# handles the data coming from the Data Turbine and sends it to stdout
	# this would be a good place to modify if you wanted to handle the data with python
	def handleIncomingData(self):
		self.waitForConnection()
		while self.go:
			try:
				data = self.clientsocket.recv(4096)
			except socket_error as msg:
				self.resetClient()
				self.waitForConnection()
				continue
			if len(data) == 0:
				self.resetClient()
				self.waitForConnection()
			elif data != 0:
				print data	

	# returns data read from stdin
	# it will read data until it reaches a newline or null character 
	def readStdin(self):
		returnStr = ""
		a = sys.stdin.read(1)
		while a != '\0' and a != '\n':
			returnStr = returnStr+a
			a = sys.stdin.read(1)
		return returnStr

	# sends data from stdin to the Data Turbine
	def handleOutgoingData(self):
		while self.go:
			if self.clientsocket:
				line = self.readStdin()
				if len(line) > 0:
					print line
					if self.clientsocket:
						self.clientsocket.send(line)

	# close the program
	def exitGracefully(self):
		if self.clientsocket:
			self.clientsocket.close()
		if self.serversocket:
			self.serversocket.close()

	def run(self):
		try:
			t = thread.start_new_thread(self.handleIncomingData, ())
			while self.go:
				self.handleOutgoingData() 
				time.sleep(.01)
		except KeyboardInterrupt as msg:
			print "KeyboardInterrupt detected. TurbineListener is terminating"
			self.go = False
		finally:
			self.exitGracefully()

if __name__ == '__main__':
    t = TurbineListener()
    t.run()
