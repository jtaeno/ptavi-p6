"""Pautas a seguir por servidor ante la informacion emitida por el cliente."""
import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """Recoge y organiza la informacion enviada por el cliente."""

    def handle(self):
        """Proceso a seguir dependiendo del tipo de mensaje enviado."""
        print(" SERVER: " + SERVER + '\n', "PORT: " + PORT + '\n',
              "RECURSO: " + RECURSO + '\n')
        while 1:
            recibido = self.rfile.read().decode('utf-8')
            print("El cliente nos manda " + recibido)
            METODO = recibido.split()[0]
            if METODO == 'INVITE':
                self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n,")
                self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n,")
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            elif METODO == 'ACK':
                print(RECURSO)
                aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + RECURSO
                print("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)
            elif METODO == 'BYE':
                self.wfile.write(b"SIP/2.0 200 OK \r\n\r\n")
            elif METODO != ['INVITE', 'ACK', ' BYE']:
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
            else:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")

            if not recibido or len(recibido):
                break


if __name__ == "__main__":
    try:
        (PROGRAMA, SERVER, PORT, RECURSO) = sys.argv
    except ValueError or IndexError:
        sys.exit("Usage: python3 server.py IP port audio_file")
    if RECURSO[-4:] != '.mp3':
        sys.exit("Usage: python server.py IP port audio_file")
    serv = socketserver.UDPServer((SERVER, int(PORT)), EchoHandler)
    print('Listening...' + '\n')

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print('\n' + "Finalizado servidor")
