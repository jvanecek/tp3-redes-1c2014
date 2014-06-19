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
			plt.plot(sizes, times, '-x')

		for i in xrange(0,max(SIZES),buffer_size):
			plt.axvline(x=i, ls='--')

		plt.xlabel('Bytes')
		plt.ylabel('ms')
		plt.legend(legends, loc=2)
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
			plt.plot(sizes, times, '-o')

		for i in xrange(0,max(SIZES),buffer_size):
			plt.axvline(x=i, ls='--')

		plt.xlabel('Bytes')
		plt.ylabel('ms')
		plt.legend(legends, loc=2)
		plt.show()
		return 

	# permite graficar una sola curva de delay vs tiempo
	def delay_vs_tiempo(self, sizes=[500], perdida=0.0, n=9, buffer_size=1024):
		files = sorted(glob.glob('./resultados/server_d*_p%s_n%s_b%s.txt' % (perdida, n, buffer_size)))

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
			plt.plot(xdelays[size], ytiempos[size], '-o')
			legends.append("Tamano: %s" % (size))

		plt.xlabel('delay')
		plt.ylabel('ms')
		plt.legend(legends,loc=2)
		plt.show()

	def perdida_vs_tiempo(self, sizes=[500], delay=0.0, n=9, buffer_size=1024):
		files = sorted(glob.glob('./resultados/server_d%s_p*_n%s_b%s.txt' % (delay, n, buffer_size)))

		xperdida = {}
		ytiempos = {}

		for f in files:
			ts = parse_archivo(f)

			for size in sizes: 
				if not xperdida.has_key(size): xperdida[size] = []
				if not ytiempos.has_key(size): ytiempos[size] = []

				#print [t['delay'] for t in ts if t['size'] == size][0]
				xperdida[size].append( [t['perdida'] for t in ts if t['size'] == size][0] )
				ytiempos[size].append( [t['tiempo'] for t in ts if t['size'] == size][0] )

		legends = []
		for size in sizes:
			plt.plot(xperdida[size], ytiempos[size], '-o')
			legends.append("Tamano: %s" % (size))

		plt.xlabel('perdida')
		plt.ylabel('ms')
		plt.legend(legends,loc=2)
		plt.show()
		
	def retransmiciones_vs_delay(self):
		yretransmiciones = [0,0,1,11]
		xdelays = [0,0.25,0.50,0.75]
		
		plt.bar(xdelays,yretransmiciones,0.1,align='center');
		
		plt.xlabel('Delays')
		plt.ylabel('Retransmiciones')
		
		plt.show()
		
	def throughput_vs_tamano(self, delays=[0.0], perdida=0.0, n=20, buffer_size=1024):
		if len(delays) < 1: delays=[0.0]
		legends = []
		for d in delays:
			f = FILE_FMT % ('server', str(d), str(perdida), n, buffer_size)

			tiempos = parse_archivo(f)
		
			legends.append( 'Delay: %s' % (str(d)) )
			through = [tiempo['size']*8/tiempo['tiempo'] for tiempo in tiempos]
			size = [ tiempo['size'] for tiempo in tiempos]
			plt.plot(size, through, '-x')

		#~ for i in xrange(0,max(SIZES),buffer_size):
			#~ plt.axvline(x=i, ls='--')

		plt.ylabel('bits/seg')
		plt.xlabel('Bytes')
		plt.legend(legends, loc=2)
		plt.show()
		return 

if __name__ == "__main__":
	g = Graficador()
	#~ g.tamano_vs_tiempo(delays=[0.0,0.05,0.1], n=9)
	#~ g.tamano_vs_tiempo(delays=[0.00,0.01,0.03],n=49)
	#~ g.tamano_vs_tiempo2(perdidas=[0.0, 0.1, 0.2, 0.5], n=9, buffer_size=500)
	#~ g.tamano_vs_tiempo2(perdidas=[0.0, 0.1, 0.2, 0.5], n=49, buffer_size=1024)
	#~ g.delay_vs_tiempo(sizes=[500,1000,1500,2000,2500],n=49,buffer_size=1024)
	#~ g.perdida_vs_tiempo(sizes=[500,1000,1500,2000,2500],n=49,buffer_size=1024)
	#~ g.retransmiciones_vs_delay()
	g.throughput_vs_tamano(delays=[0.01,0.03,0.04,0.05],n=49)
