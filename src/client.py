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
			f.write("%d\t%.5f\t%d\t%.10f\t%.10f\n" % (
				time['delay'],
				time['perdida'],
				time['size'],
				time['timeServer'],
				time['totalTime']
			))
		f.close()

def start_sending(delay, perdida, sizes_to_send):
	print 'perdida: ', perdida, ' - delay: ', delay
	times = []
	print "Vas a mandar paquetes de tamano: ", sizes_to_send
	received = str()

	with Socket(delay, perdida) as sock2:
		sock2.connect( CONNECTION_DIR )

		for size_to_send in sizes_to_send:
			# si no es un size valido salgo
			if not size_to_send.isdigit() or int(size_to_send) < 1: 
				break

			timeToServerPromedio = 0
			totalTimePromedio = 0
			for i in range(REPEAT_SEND):
				# aviso cuanto voy a mandar para que el server se prepare y espero a q me confirme si esta listo
				#sock2.send( size_to_send )
				#received = sock2.recv(LEN_SERVER_MSG_OK)

				# empiezo a mandar
				to_send = "a"*int(size_to_send)

				# si el server nos contesto, significa que ya le podemos empezar a enviar.
				startTime = time.time()
				print "Envio"
				sock2.send( to_send )				
				#timeToServer = float( sock2.recv(12) )
				totalTime = time.time() - startTime

				#timeToServerPromedio += timeToServer / REPEAT_SEND
				totalTimePromedio += totalTime / REPEAT_SEND

			#print 'sock2 received: (%.10f, %.10f)' % (timeToServerPromedio, totalTimePromedio)

			times.append({
				'delay' : delay,
				'perdida' : perdida,
				'size' : int(size_to_send), 
				#'timeServer' : timeToServerPromedio,
				'totalTime' : totalTimePromedio
			})
			
			time.sleep(1)
			
		# aviso al server que termino todo
		sock2.send( NULL_SIZE )

		# Cerramos el stream de escritura pero podemos seguir recibiendo datos.
		sock2.shutdown(SHUT_WR)
		sock2.close()

		save_result("resultados/d%s_p%s_n%s.txt"%(delay, perdida, len(sizes_to_send)), times)

if __name__ == "__main__":
	delay = 0 if not len(sys.argv) > 1 else float(sys.argv[1])
	perdida = 0 if not len(sys.argv) > 2 else float(sys.argv[2])

	# por ahora los sizes_to_send los harcodeo para facilitar la generacion de graficos
	#sizes_to_send = []
	#for i in range(3, len(sys.argv)):
	#	sizes_to_send.append( sys.argv[i] )

	#start_sending(delay, perdida, [str(i) for i in range(10000,6000) if i % 500 == 0] )
	start_sending(delay, perdida, [str(10000)] )
