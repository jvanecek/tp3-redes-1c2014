#!/bin/usr
# Script que abre un socket y lo conecta al puerto 6677 de localhost.

from constants import *
import sys
import time
from ptc import Socket, SHUT_WR	

def save_result(file, times):
	with open(file, 'w') as f:
		f.write("delay\tperdida\tsize\ttimeToServer\ttotalTime\n")
		for time in times:
			f.write("%d\t%.5f\t%d\t%.10f\n" % (
				time['delay'],
				time['perdida'],
				time['size'],
				time['totalTime']
			))
		f.close()

def start_sending(delay, perdida):
	print 'perdida: ', perdida, ' - delay: ', delay
	times = []
	print "Vas a mandar paquetes de tamano: ", SIZES
	received = str()

	with Socket(delay, perdida) as sock2:
		sock2.connect( CONNECTION_DIR )

		for size_to_send in SIZES:
			# si no es un size valido salgo
			if size_to_send == NULL_SIZE: 
				break

			for i in range(REPEAT_SEND):
				# espero a q el server me diga cuando empezar a mandar
				sock2.recv(MAX_BUFFER)
				
				# si el server nos contesto, significa que ya le podemos empezar a enviar.
				to_send = "a"*size_to_send

				# empiezo a mandar
				print "Envio ", size_to_send, ' bytes ( iteracion ', i,')'
				sock2.send( to_send )				

		# Cerramos el stream de escritura pero podemos seguir recibiendo datos.
		sock2.shutdown(SHUT_WR)
		sock2.close()

if __name__ == "__main__":
	delay = 0.0 if not len(sys.argv) > 1 else float(sys.argv[1])
	perdida = 0.0 if not len(sys.argv) > 2 else float(sys.argv[2])

	# por ahora los sizes_to_send los harcodeo para facilitar la generacion de graficos
	#sizes_to_send = []
	#for i in range(3, len(sys.argv)):
	#	sizes_to_send.append( sys.argv[i] )

	start_sending(delay, perdida)
