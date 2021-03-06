# -*- coding: utf-8 -*-

############################################################
#          Trabajo Práctico 3: Capa de Transporte          #
#         Manejo de Conexiones usando Raw Sockets          #
#               Teoría de las Comunicaciones               #
#                        FCEN - UBA                        #
#                Primer cuatrimestre de 2014               #
############################################################

############################################################
# Definición de diversas constantes utilizadas por el 
# protocolo, entre las que se encuentran, por ejemplo, los 
# estados.
############################################################

PROTOCOL_NUMBER = 202

RETRANSMISSION_TIMEOUT = 0.5
MAX_RETRANSMISSION_ATTEMPTS = 5

CLOCK_TICK = 0.1

MAX_SEQ = (1<<32) - 1
MAX_WND = (1<<16) - 1

SYN_SENT = 1
SYN_RCVD = 2
ESTABLISHED = 3
CLOSED = 6
LISTEN = 7
FIN_WAIT1 = 10
FIN_WAIT2 = 11
CLOSE_WAIT = 12
LAST_ACK = 13
CLOSING = 14

SHUT_RD = 0
SHUT_WR = 1
SHUT_RDWR = 2

NULL_ADDRESS = '0.0.0.0'

RECEIVE_BUFFER_SIZE = 1024

MSS = 2*1024*1024

MAX_DELAY = 2*RETRANSMISSION_TIMEOUT # maximo delay permitido en el protocolo