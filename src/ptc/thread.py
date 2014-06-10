# -*- coding: utf-8 -*-

############################################################
#          Trabajo Práctico 3: Capa de Transporte          #
#         Manejo de Conexiones usando Raw Sockets          #
#               Teoría de las Comunicaciones               #
#                        FCEN - UBA                        #
#                Primer cuatrimestre de 2014               #
############################################################

import threading
import socket
import time

from constants import CLOCK_TICK


class PTCThread(threading.Thread):
    
    def __init__(self, protocol):
        threading.Thread.__init__(self)
        self.protocol = protocol
        self.setDaemon(False)
        self.keep_running = True
        
    def run(self):
        while self.should_run():
            self.do_run()
            
    def should_run(self):
        return self.keep_running
    
    def stop(self):
        self.keep_running = False
        
    def do_run(self):
        raise NotImplementedError
    
########################################################
# Clock
#   Simula el clock del sistema. Cada CLOCK_TICK segundos (definido
#   por defecto en 0.1) invocará al método tick del protocolo.
########################################################

class Clock(PTCThread):
        
    def do_run(self):
        self.wait()
        self.tick()
        
    def wait(self):
        time.sleep(CLOCK_TICK)
        
    def tick(self):
        self.protocol.tick()
    
########################################################
# PacketReceiver
#   Monitorea el socket subyacente y recibe los paquetes.
#   Al detectar la llegada de uno, se invocará el método handle_incoming
#   del protocolo (que a su vez se apoyará en el handler mencionado más
#   arriba).
########################################################

class PacketReceiver(PTCThread):
    
    TIMEOUT = 0.5
    
    def do_run(self):
        try:
            packet = self.protocol.socket.receive(timeout=self.TIMEOUT)
            self.protocol.handle_incoming(packet)
        except socket.timeout:
            pass
        
#################################################################
# PacketSender
#   Envía los paquetes de datos y eventualmente el FIN
#   mediante el método handle_outgoing del protocolo. Éste es ejecutado
#   en el contexto de este thread cada vez que ocurre algún evento que
#   podría motivar el envío de nuevos datos (e.g., llegada de ACKs o
#   invocaciones a send por parte del usuario).
#################################################################

class PacketSender(PTCThread):
    
    def __init__(self, protocol):
        PTCThread.__init__(self, protocol)
        self.condition = threading.Condition()
        self.notified = False
    
    def wait(self):
        with self.condition:
            if not self.notified:
                self.condition.wait()
            self.notified = False
    
    def notify(self):
        with self.condition:
            self.condition.notify()
            self.notified = True
    
    def do_run(self):
        self.wait()
        self.protocol.handle_outgoing()
