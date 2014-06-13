#! /usr/bin/python

import sys
from client import Client

def read_size():
	return int( raw_input('Bytes a enviar: ') )

c = Client(('127.0.0.1', 6677))

while True:
	size_to_send = read_size()
	print c.time_to_send(size_to_send)	

	if size_to_send == 0: 
		break

print "Terminado"