# -*- coding: utf-8 -*-

############################################################
#          Trabajo Práctico 3: Capa de Transporte          #
#         Manejo de Conexiones usando Raw Sockets          #
#               Teoría de las Comunicaciones               #
#                        FCEN - UBA                        #
#                Primer cuatrimestre de 2014               #
############################################################

############################################################
# Implementación de un buffer de bytes (DataBuffer) que es 
# usado por el bloque de control para definir los buffers 
# de entrada y de salida.
# Ofrece funcionalidad para reflejar el hecho de que los 
# datos pueden llegar potencialmente fuera de orden.
# Por ejemplo, el método add_chunk recibe un offset dentro 
# del buffer y los bytes a agregar a partir de dicho offset:
############################################################

import threading


class DataBuffer(object):
    
    def __init__(self, start_index=0):
        self.buffer = str()
        self.chunks = dict()
        lock = threading.RLock()
        self.condition = threading.Condition(lock)
        self.start_index = start_index
        self.last_index = start_index
        
    def flush(self):
        with self.condition:
            self.buffer = str()
            self.chunks = dict()
            self.last_index = self.start_index
        
    def get_last_index(self):
        return self.last_index
    
    def empty(self):
        with self.condition:
            return len(self.buffer) == 0
        
    def get(self, size):
        with self.condition:
            if not self.buffer:
                self.condition.wait()
            data = self.buffer[:size]
            self.buffer = self.buffer[size:]
            return data

    def put(self, data):
        if not data:
            return
        with self.condition:
            self.buffer += data
            self.last_index += len(data)
            self.merge_chunks()
            self.condition.notifyAll()
            
    def add_chunk(self, start, data):
        with self.condition:
            if start <= self.last_index:
                offset = self.last_index - start
                self.put(data[offset:])
            else:
                self.chunks[start] = data
            
    def merge_chunks(self):
        indices = sorted(self.chunks.keys())
        for start in indices:
            data = self.chunks[start]
            end = start + len(data)
            if start <= self.last_index and end > self.last_index:
                offset = self.last_index - start
                self.buffer += data[offset:]
                self.last_index = end
                del self.chunks[start]    
