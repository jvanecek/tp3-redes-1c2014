#!/bin/usr
# Script que liga un socket al puerto 6677 de localhost.

from constants import *
import sys
import time
from ptc import Socket

def start_server(delay, perdida, sizes_to_recv):
	tiempo = {}
	print 'perdida: ', perdida, ' - delay: ', delay
	
	print "Vas a recibir paquetes de tamano: ", sizes_to_recv
	
	with Socket(delay, perdida) as sock1:
		sock1.bind( CONNECTION_DIR )
		sock1.listen()
		sock1.accept()

		str_recv_acum = ""
		for size_to_recv in sizes_to_recv:
			# me dicen cuanto voy a recibir
			#size_to_recv = sock1.recv( MAX_BUFFER )
			print "Size To R !", size_to_recv
			if size_to_recv == NULL_SIZE:
				break

			size_to_recv = int(size_to_recv)
			for i in range(REPEAT_SEND):
				# contesto que puedo empezar a recibir
				#sock1.send(SERVER_MSG_OK)

				startTime = time.time()
				str_recv = ""
				while (size_to_recv > len(str_recv)):
					str_recv += sock1.recv( MAX_BUFFER )
					print str_recv
					print 'faltan recibir: ', size_to_recv-len(str_recv)
					
				totalTime = time.time() - startTime

				#if not tiempo.has_key(size_to_recv): tiempo[size_to_recv] = []
				#tiempo[size_to_recv].append( totalTime )

				# le mando cuanto tardo en recibir
				#sock1.send( "%.10f" % totalTime )	
				print 'size_to_recv = %s\nserverTime = %.10f' % (size_to_recv, totalTime)

		sock1.close()
		sock1.listen()

	print 'delay\tperdida\tsize\ttiempo\titeraciones'
	for size,tiempos in tiempo:
		print '%.2f\t%.2f\t%d\t%.10f\t%d' % (delay, perdida, size, numpy.mean(tiempos), len(tiempos))

if __name__ == "__main__":
	delay = 0 if not len(sys.argv) > 1 else float(sys.argv[1])
	perdida = 0 if not len(sys.argv) > 2 else float(sys.argv[2])

	start_server(delay, perdida, [str(10000)])
