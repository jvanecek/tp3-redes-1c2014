#!/bin/usr
# Script que abre un socket y lo conecta al puerto 6677 de localhost.

import time
from ptc import Socket, SHUT_WR

received = str()

sock2 = Socket() 
sock2.connect(('127.0.0.1', 6677))

while True:
	
	size_to_send = raw_input('Bytes a enviar: ')
	
	# aviso cuanto voy a mandar para que el server se prepare
	if type(size_to_send) != int or size_to_send < 1: 
		sock2.send( "0" )
		break

	size_to_send = int( size_to_send )
	to_send = "a"*size_to_send
		
	received = sock2.recv(3)

	# si el server nos contesto, significa que ya le podemos empezar a enviar.
	startTime = time.time()
	sock2.send( to_send )
	timeToServer = float( sock2.recv(12) )
	totalTime = time.time() - startTime
	
	print 'sock2 received: (%.10f, %.10f)' % (timeToServer, totalTime)

# Cerramos el stream de escritura pero podemos seguir recibiendo datos.
sock2.shutdown(SHUT_WR)
sock2.close()