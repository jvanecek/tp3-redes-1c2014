#!/bin/usr
# Script que liga un socket al puerto 6677 de localhost.

from constants import *
import sys
import time
from ptc import Socket

def start_server(delay=0, perdida=0):
	print 'perdida: ', perdida, ' - delay: ', delay

	with Socket(delay, perdida) as sock1:
		sock1.bind( CONNECTION_DIR )
		sock1.listen()
		sock1.accept()

		str_recv_acum = ""
		while True:
			# me dicen cuanto voy a recibir
			size_to_recv = sock1.recv( MAX_BUFFER )
			print "Size To R !", size_to_recv
			if size_to_recv == NULL_SIZE:
				break

			size_to_recv = int(size_to_recv)
			# contesto que puedo empezar a recibir
			sock1.send(SERVER_MSG_OK)

			startTime = time.time()
			while (size_to_recv > 0):
				str_recv = sock1.recv( MAX_BUFFER )
				str_recv_acum += str_recv
				size_to_recv -= len(str_recv)
				print 'faltan recibir: ', size_to_recv
			totalTime = time.time() - startTime

			# le mando cuanto tardo en recibir
			sock1.send( "%.10f" % totalTime )	
			print 'size_to_recv = %s\nstr_recv = %s\nserverTime = %.10f' % (size_to_recv, str_recv, totalTime)

		sock1.close()
		sock1.listen()

if __name__ == "__main__":
	delay = 0 if not len(sys.argv) > 1 else float(sys.argv[1])
	perdida = 0 if not len(sys.argv) > 2 else float(sys.argv[2])

	start_server(delay, perdida)
