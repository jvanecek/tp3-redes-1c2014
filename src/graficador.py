#! /usr/bin/python
import matplotlib.pyplot as plt
from constants import *
from ptc import Socket

def parse_archivo(archivo):
	tiempos = []
	f = open(archivo)
	lines = f.readlines()
	f.close()

	lineas = lines[1:]

	i = 1
	for linea in lineas:
		linea = linea.split("\t") #delay	perdida	size	timeToServer	totalTime

		tiempos.append({
			'delay' : float(linea[0]),
			'perdida' : float(linea[1]),
			'size' : int(linea[2]),
			'tiempo' : float(linea[3])
		})
		
	return tiempos

class Graficador:
	def tamano_vs_tiempo(self, delays=[0.0], perdida=0.0, n=20, buffer_size=1024):
		if len(delays) < 1: delays=[0.0]
		legends = []
		for d in delays:
			f = FILE_FMT % ('server', str(d), str(perdida), n, buffer_size)

			tiempos = parse_archivo(f)
		
			legends.append( 'Delay: %s' % (str(d)) )
			sizes = [tiempo['size'] for tiempo in tiempos]
			times = [tiempo['tiempo'] for tiempo in tiempos]
			plt.plot(sizes, times)

		for i in xrange(0,max(SIZES),buffer_size):
			plt.axvline(x=i, ls='--')

		plt.xlabel('Bytes')
		plt.ylabel('ms')
		plt.legend(legends)
		plt.show()
		return 

	def tamano_vs_tiempo2(self, delay=0.0, perdidas=[0.0], n=20, buffer_size=1024):
		if len(perdidas) < 1: perdidas=[0.0]
		legends = []
		for p in perdidas:
			f = FILE_FMT % ('server', str(delay), str(p), n, buffer_size)

			tiempos = parse_archivo(f)
		
			legends.append( 'Perdida: %s' % (str(p)) )
			sizes = [tiempo['size'] for tiempo in tiempos]
			times = [tiempo['tiempo'] for tiempo in tiempos]
			plt.bar(sizes, times, width=0.8)

		for i in xrange(0,max(SIZES),buffer_size):
			plt.axvline(x=i, ls='--')

		plt.xlabel('Bytes')
		plt.ylabel('ms')
		plt.legend(legends)
		plt.show()
		return 

if __name__ == "__main__":
	g = Graficador()
	g.tamano_vs_tiempo(delays=[0.0,0.05], n=9)
	#g.tamano_vs_tiempo2(perdidas=[0.0], n=99)