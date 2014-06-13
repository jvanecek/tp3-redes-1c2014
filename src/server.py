#!/bin/usr
# Script que liga un socket al puerto 6677 de localhost.

import time
from ptc import Socket

ip_port = ('127.0.0.1', 6677)

print "[Server] Server iniciado"
socket = Socket()
print "[Server] Socket iniciado"
socket.bind(ip_port)
print "[Server] Socket bind a puerto", ip_port
socket.listen()
print "[Server] Socket escuchando"
socket.accept()
print "[Server] Socket aceptando"
print "[Server] Empiezo a recibir"

size_to_recv = int(socket.recv(5))

while size_to_recv != 0:
	socket.send("Ready")

	print "[Server] Listo para recibir %s bytes" % size_to_recv
	startTime = time.time()
	socket.recv(size_to_recv)
	totalTime = time.time() - startTime
	print "[Server] Devuelvo el tiempo que tardo en recibir (%.15f)" % totalTime
	socket.send("%.15f" % (totalTime))

	size_to_recv = int(socket.recv(10))

print "[Server] Cerrando"
socket.close()