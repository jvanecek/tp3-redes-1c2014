#!/bin/usr
# Script que liga un socket al puerto 6677 de localhost.

from constants import *
import numpy as np
import sys
import time
from ptc import Socket

FILE_FMT = "resultados/%s_d%s_p%s_n%s_b%s.txt" # % ('server', delay, perdida, cant_paquetes, buffer)

def save_result(file, delay, perdida, tiempos):
	with open(file, 'w') as f:
		f.write("delay\tperdida\tsize\ttiempo\titeraciones\n")
		for size in sorted(tiempos):
			f.write( '%.2f\t%.2f\t%d\t%.10f\t%d\n' % (delay, perdida, size, np.mean(tiempos[size]), len(tiempos[size])))
		f.close()

def start_server(delay, perdida):
	tiempo = {}
	print 'perdida: ', perdida, ' - delay: ', delay
	print "Vas a recibir paquetes de tamano: ", SIZES
	
	with Socket(delay, perdida) as sock1:
		sock1.bind( CONNECTION_DIR )
		sock1.listen()
		sock1.accept()

		for size_to_recv in SIZES:
			# chequeo que es un tamano valido
			if size_to_recv == NULL_SIZE:
				break

			for i in range(REPEAT_SEND):
				sock1.send(SERVER_MSG_OK) # le aviso de que empiece a mandar

				print '\nComienzo a recibir ',size_to_recv,' bytes ( iteracion ',i,')'

				startTime = time.time()
				str_recv = ""
				while (size_to_recv > len(str_recv)):
					str_recv += sock1.recv( MAX_BUFFER )
				totalTime = time.time() - startTime

				if not tiempo.has_key(size_to_recv): tiempo[size_to_recv] = []
				tiempo[size_to_recv].append( totalTime )

				print '\tRecibidos los %d bytes' % (size_to_recv)
				print '\tTiempo = %.10f' % (totalTime)

		sock1.close()

		save_result(FILE_FMT % ('server', str(delay), str(perdida), len(SIZES), MAX_BUFFER), delay, perdida, tiempo)

if __name__ == "__main__":
	delay = 0.0 if not len(sys.argv) > 1 else float(sys.argv[1])
	perdida = 0.0 if not len(sys.argv) > 2 else float(sys.argv[2])

	start_server(delay, perdida)
