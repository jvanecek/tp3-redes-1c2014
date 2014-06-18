#! /usr/bin/python
import matplotlib.pyplot as plt

from ptc import Socket

class Graficador:

	def __init__(self):
        self.server = Socket()
        self.client = Socket()
 
    def __del__(self):
        self.server.close()
        self.client.close()

	def tiempo_send(self, tamano, to_send):
		return 

	def en_funcion_tamano_archivo(self, tamanos):
		return