
SERVER_MSG_OK = "ok"
LEN_SERVER_MSG_OK = 2

NULL_SIZE = 0

CONNECTION_IP = '127.0.0.1'
CONNECTION_PORT = 6678
CONNECTION_DIR = (CONNECTION_IP, CONNECTION_PORT)

REPEAT_SEND = 50

MAX_BUFFER = 512

SIZES = [i for i in range(1,5000) if i % 100 == 0] 

FILE_FMT = "resultados/%s_d%s_p%s_n%s_b%s.txt" # % ('server', delay, perdida, cant_paquetes, buffer)
