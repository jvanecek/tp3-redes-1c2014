#!/bin/usr
# Script que abre un socket y lo conecta al puerto 6677 de localhost.

from constants import *
import sys
import time
from ptc import Socket, SHUT_WR

times = []

def start_sending(delay, perdida, sizes_to_send):
	print "Vas a mandar paquetes de tamano: ", sizes_to_send
	received = str()

	with Socket(delay, perdida) as sock2:
		sock2.connect(  CONNECTION_DIR  )

		for size_to_send in sizes_to_send:
			# si no es un size valido salgo
			if not size_to_send.isdigit() or int(size_to_send) < 1: 
				break

			timeToServerPromedio = 0
			totalTimePromedio = 0
			for i in range(REPEAT_SEND):
				# aviso cuanto voy a mandar para que el server se prepare y espero a q me confirme si esta listo
				sock2.send( size_to_send )
				received = sock2.recv(LEN_SERVER_MSG_OK)

				# empiezo a mandar
				to_send = "a"*int(size_to_send)

				# si el server nos contesto, significa que ya le podemos empezar a enviar.
				startTime = time.time()
				sock2.send( to_send )
				timeToServer = float( sock2.recv(12) )
				totalTime = time.time() - startTime

				timeToServerPromedio += timeToServer / REPEAT_SEND
				totalTimePromedio += totalTime / REPEAT_SEND

			print 'sock2 received: (%.10f, %.10f)' % (timeToServerPromedio, totalTimePromedio)

			times.append({
				'size' : size_to_send, 
				'timeServer' : timeToServerPromedio,
				'totalTime' : totalTimePromedio
			})

		# aviso al server que termino todo
		sock2.send( NULL_SIZE )

		# Cerramos el stream de escritura pero podemos seguir recibiendo datos.
		sock2.shutdown(SHUT_WR)
		sock2.close()

		print times

if __name__ == "__main__":
	delay = 0 if not len(sys.argv) > 1 else int(sys.argv[1])
	perdida = 0 if not len(sys.argv) > 2 else float(sys.argv[2])

	sizes_to_send = []
	for i in range(3, len(sys.argv)):
		sizes_to_send.append( sys.argv[i] )

	start_sending(delay, perdida, sizes_to_send)