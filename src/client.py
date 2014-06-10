#!/bin/usr
# Script que abre un socket y lo conecta al puerto 6677 de localhost.

from ptc import Socket, SHUT_WR

to_send = 'Hola server!'
received = str()

with Socket() as sock2:
	sock2.connect(('127.0.0.1', 6677))
	sock2.send(to_send)
	received += sock2.recv(10)
	# Cerramos el stream de escritura pero podemos seguir recibiendo datos.
	sock2.shutdown(SHUT_WR)
	received += sock2.recv(20)

print 'sock2 received: %s' % received
