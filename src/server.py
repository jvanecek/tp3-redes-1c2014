#!/bin/usr
# Script que liga un socket al puerto 6677 de localhost.

from constants import *
import sys
import time
from ptc import Socket

def start_server(delay=0, perdida=0):
	with Socket(delay, perdida) as sock1:
		sock1.bind( CONNECTION_DIR )
		sock1.listen()
		sock1.accept()

		while True:
			# me dicen cuanto voy a recibir
			size_to_recv = sock1.recv(4)

			if size_to_recv == NULL_SIZE:
				break

			# contesto que puedo empezar a recibir
			sock1.send(SERVER_MSG_OK)

			startTime = time.time()
			str_recv = sock1.recv( int(size_to_recv) )
			totalTime = time.time() - startTime

			# le mando cuanto tardo en recibir
			sock1.send( "%.10f" % totalTime )	
			print 'size_to_recv = %s\nstr_recv = %s\nserverTime = %.10f' % (size_to_recv, str_recv, totalTime)

		sock1.close()

if __name__ == "__main__":
	delay = 0 if not len(sys.argv) > 1 else int(sys.argv[1])
	perdida = 0 if not len(sys.argv) > 2 else float(sys.argv[2])

	start_server(delay, perdida)