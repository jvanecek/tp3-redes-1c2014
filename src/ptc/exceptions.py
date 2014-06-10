# -*- coding: utf-8 -*-

############################################################
#          Trabajo Práctico 3: Capa de Transporte          #
#         Manejo de Conexiones usando Raw Sockets          #
#               Teoría de las Comunicaciones               #
#                        FCEN - UBA                        #
#                Primer cuatrimestre de 2014               #
############################################################

############################################################
# Definición de una excepción genérica (PTCError).
# Representa errores del protocolo o de uso inválido del mismo.
# El constructor recibe un string como argumento que permite 
# indicar con mayor detalle qué fue lo que realmente ocurrió.
############################################################

class PTCError(Exception):
    
    pass
