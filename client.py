
"""Con este programa creamos socket para la comunicacion cliente servidor."""

import socket
import sys

try:
    (Programa, Metodo, Direccion) = sys.argv
except ValueError:
     sys.exit("Usage: python3 client.py method receiver@IP:SIPport")
try:
    METODO = Metodo.upper()
    NAME = Direccion.split('@')[0]
    SERVER = Direccion.split('@')[1].split(':')[0]
    PORT = int(Direccion.split('@')[1].split(':')[1])
except IndexError:
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")

ENVIAR = METODO + ' sip:' + Direccion + ' SIP/2.0'

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))
    print(" METODO: " + METODO + '\n', "NOMBRE: " + NAME + '\n', "SERVER: " +
          SERVER + '\n', "PORT: " + str(PORT) + '\n')
    print("Enviando: " + ENVIAR)
    my_socket.send(bytes(ENVIAR, 'utf-8') + b'\r\n')
    try:
        data = my_socket.recv(1024)
    except ConnectionRefusedError:
        sys.exit("No Connection")
    print('Recibido -- ', data.decode('utf-8'))
    if METODO == 'INVITE':
        supuestos = ["SIP/2.0 100 Trying\r\n\r\n",
                     "SIP/2.0 180 Ringing\r\n\r\n", "SIP/2.0 200 OK\r\n\r\n"]
        recibidos = data.decode('utf-8').split(',')
        ENVIAR2 = Direccion.split(':')[0]
        if recibidos == supuestos:
            print("Enviando ACK...", 'ACK sip:' + ENVIAR2 + ' SIP/2.0')
            my_socket.send(bytes('ACK sip:' + ENVIAR2 + ' SIP/2.0', 'utf-8') +
                           b'\r\n')
    if METODO == 'BYE':
        print("Terminando socket...")
        print("Fin")
