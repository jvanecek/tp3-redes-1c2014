#! /usr/bin/python
import matplotlib.pyplot as plt
import glob
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
	# permite hacer distintas curvas con distintos delays
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

	# permite hacer distintas curvas con distintas perdidas
	def tamano_vs_tiempo2(self, delay=0.0, perdidas=[0.0], n=20, buffer_size=1024):
		if len(perdidas) < 1: perdidas=[0.0]
		legends = []
		for p in perdidas:
			f = FILE_FMT % ('server', str(delay), str(p), n, buffer_size)

			tiempos = parse_archivo(f)
		
			legends.append( 'Perdida: %s' % (str(p)) )
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

	# permite graficar una sola curva de delay vs tiempo
	def delay_vs_tiempo(self, sizes=[500], perdida=0.0, n=9, buffer_size=1024):
		files = glob.glob('./resultados/server_d*_p%s_n%s_b%s.txt' % (perdida, n, buffer_size))

		xdelays = {}
		ytiempos = {}

		for f in files:
			ts = parse_archivo(f)

			for size in sizes: 
				if not xdelays.has_key(size): xdelays[size] = []
				if not ytiempos.has_key(size): ytiempos[size] = []

				#print [t['delay'] for t in ts if t['size'] == size][0]
				xdelays[size].append( [t['delay'] for t in ts if t['size'] == size][0] )
				ytiempos[size].append( [t['tiempo'] for t in ts if t['size'] == size][0] )

		legends = []
		for size in sizes:
			plt.plot(xdelays[size], ytiempos[size])
			legends.append("Tamano: %s" % (size))

		plt.xlabel('delay')
		plt.ylabel('ms')
		plt.legend(legends)
		plt.show()

if __name__ == "__main__":
	g = Graficador()
	g.tamano_vs_tiempo(delays=[0.0,0.05], n=9)
	g.tamano_vs_tiempo2(perdidas=[0.0, 0.1, 0.2, 0.5], n=9, buffer_size=500)
	g.delay_vs_tiempo(sizes=[500,1000,1500,2000])