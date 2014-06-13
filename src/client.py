#!/bin/usr
# Script que abre un socket y lo conecta al puerto 6677 de localhost.

import subprocess
import time
from ptc import Socket, SHUT_WR

class Client:
	def __init__(self, ip_port):
		print "[Cliente] Cliente iniciado"
		self.socket = Socket()
		print "[Cliente] Socket creado"
		self.socket.connect(ip_port)
		print "[Cliente] Socket conectado"

	def __del__(self):
		self.socket.close()

	def time_to_send(self, tamano):
		#subprocess.Popen(["sudo python","server.py", tamano])

		print "[Cliente] Aviso q voy a mandar %d bytes" % tamano
		self.socket.send(str(tamano))

		if tamano == 0: 
			return (0,0)

		print "[Cliente] Esperando confirmacion"
		self.socket.recv(10) 

		print "[Cliente] Empiezo a mandar los %s bytes" % tamano
		to_send = 'a'*tamano
		startTime = time.time()
		self.socket.send(to_send)
		timeToServer = self.socket.recv(10)
		totalTime = time.time() - startTime

		#self.socket.close() 
		print "[Cliente] recibida la respuesta"
		return (timeToServer, totalTime)