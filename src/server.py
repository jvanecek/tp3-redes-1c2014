#!/bin/usr
# Script que liga un socket al puerto 6677 de localhost.

import time
from ptc import Socket

sock1 = Socket() 
sock1.bind(('127.0.0.1', 6677))
sock1.listen()
sock1.accept()

while True:
	# me dicen cuanto voy a recibir
	size_to_recv = sock1.recv(10)

	if size_to_recv == "0":
		break

	# contesto que puedo empezar a recibir
	sock1.send("ok!")

	startTime = time.time()
	str_recv = sock1.recv( int(size_to_recv) )
	totalTime = time.time() - startTime

	# le mando cuanto tardo en recibir
	sock1.send( "%.10f" % totalTime )	
	print 'size_to_recv = %s\nstr_recv = %s\nserverTime = %.10f' % (size_to_recv, str_recv, totalTime)

sock1.close()
