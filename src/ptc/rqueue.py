# -*- coding: utf-8 -*-

############################################################
#          Trabajo Práctico 3: Capa de Transporte          #
#         Manejo de Conexiones usando Raw Sockets          #
#               Teoría de las Comunicaciones               #
#                        FCEN - UBA                        #
#                Primer cuatrimestre de 2014               #
############################################################

############################################################
# Implementación de la cola de retransmisión (RetransmissionQueue).
# Al encolarse, los paquetes se asocian con un timestamp que irá
# revisándose en cada tick del reloj (mediante el método tick, invocado
# por el método homónimo del protocolo).
# Cada vez que expira un timeout, el paquete respectivo se mueve a una
# lista interna de paquetes a retransmitir que luego es consumida por el
# protocolo.
# Al procesar un ACK, el método remove_acknowledged_by permite
# extraer de la cola todo paquete cuyo payload quede completamente
# cubierto por el #ACK contenido en el paquete.
############################################################

import threading
import time

from constants import RETRANSMISSION_TIMEOUT


class RetransmissionQueue(object):
    
    def __init__(self):
        self.queue = list()
        self.packets_to_retransmit = list()
        self.lock = threading.RLock()
        
    def empty(self):
        with self.lock:
            return len(self.queue) == 0 and\
                   len(self.packets_to_retransmit) == 0
        
    def tick(self):
        with self.lock:
            new_queue = list()
            for packet_tuple in self.queue:
                packet, enqueued_at, remaining_time = packet_tuple
                now = time.time()
                if now - enqueued_at >= remaining_time:
                    self.packets_to_retransmit.append(packet)
                else:
                    new_queue.append(packet_tuple)
            self.queue = new_queue
            
    def remove_acknowledged_by(self, ack_packet, snd_una, snd_nxt):
        with self.lock:
            new_queue = list()
            acknowledged_packets = list()
            for packet_tuple in self.queue:
                packet = packet_tuple[0]
                ack = ack_packet.get_ack_number()
                # Checkear que ack >= seq_lo y ack >= seq_hi simultáneamente,
                # teniendo en cuenta que son valores modulares.
                if self.ack_covers_packet(ack, packet, snd_una, snd_nxt):
                    acknowledged_packets.append(packet)
                    self.remove_packet_from_packets_to_retransmit(packet)
                else:
                    new_queue.append(packet_tuple)
            self.queue = new_queue
            return acknowledged_packets
        
    def put(self, packet):
        with self.lock:
            enqueued_at = time.time()
            remaining_time = RETRANSMISSION_TIMEOUT
            packet_tuple = (packet, enqueued_at, remaining_time)
            self.queue.append(packet_tuple)
            self.remove_packet_from_packets_to_retransmit(packet)
            
    def get_packets_to_retransmit(self):
        with self.lock:
            return list(self.packets_to_retransmit)
        
    def remove_packet_from_packets_to_retransmit(self, packet):
        # Método privado. Ya tenemos el lock.
        seq_numbers = map(lambda packet: packet.get_seq_number(),
                          self.packets_to_retransmit)
        try:
            index = seq_numbers.index(packet.get_seq_number())
        except ValueError:
            index = None
        if index is not None:
            del self.packets_to_retransmit[index]
            
    def ack_covers_packet(self, ack, packet, snd_una, snd_nxt):
        # Método privado para comparar correctamente el ACK contra los bytes
        # secuenciados por el paquete.
        _, seq_hi = packet.get_seq_interval()
        if snd_nxt > snd_una:
            # Cuandp SND_NXT > SND_UNA, no hay wrap-around.
            # Luego, el ACK provisto cubre el paquete sii
            # ack > seq_hi = número de secuencia del último byte.
            return ack >= seq_hi
        else:
            # Cuando SND_NXT <= SND_UNA, SND_NXT arrancó desde 0 al haber
            # superado el máximo valor. Existen dos posibilidades:
            #   * seq_hi y ack también lo hicieron, de manera que
            #     deberíamos tener que seq_hi <= ack <= snd_nxt
            #   * o tan solo ack superó el máximo, lo que significa que ya
            #     es más grande que seq_hi. 
            return (seq_hi <= ack <= snd_nxt) or\
                    snd_nxt < seq_hi
            
    def __enter__(self, *args, **kwargs):
        return self.lock.__enter__(*args, **kwargs)
    
    def __exit__(self, *args, **kwargs):
        return self.lock.__exit__(*args, **kwargs)
