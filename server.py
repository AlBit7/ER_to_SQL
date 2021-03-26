import socket, threading, requests
from main import *
import os.path

PATH = os.path.dirname(__file__).replace("\\", "/")
PORT = 8080
SERVER = 'localhost'
ADDRESS = (SERVER , PORT)
FORMATO = 'utf-8'
BUFFER = 1024

soc = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
soc.bind(ADDRESS)
soc.listen(1)

print("server in ascolto su " + SERVER + ":" + str(PORT) + "...")

def serviCliente(connessione, richiesta, address):
    
    tmp = richiesta.split(" ", 2)

    paginaRichiesta = tmp[1]
    method = tmp[0]

    if paginaRichiesta == "/":
        paginaRichiesta = "/index.html"

    try:
        file = open(PATH + paginaRichiesta, 'r')
        html = file.read()
        file.close()
        header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
    
    except:
        header = 'HTTP/1.1 404 NOT FOUND\nContent-Type: text/html\n\n'
        html = "<p>Pagina '" + paginaRichiesta + "' non trovata</p>"
    
    if method == 'POST':

        try:
            nomeFile = richiesta.split("\r\n")[-1][2:]
            contenutoFile = open(nomeFile, 'r')
            print("contenuto: "+contenutoFile.read())
            er = ER(contenutoFile.read())
            html += "<p>" + er.displaySQL() + "</p>"
            contenutoFile.close()

        except:
            header = 'HTTP/1.1 500\nContent-Type: text/html\n\n'
            html += "<p>errore server</p>"

    risposta = header + html

    connessione.send(risposta.encode(FORMATO))
    connessione.close()

while True:

    connessione, address = soc.accept()
    richiestaBrowser = connessione.recv(BUFFER).decode(FORMATO)

    print(str(address[0]) + ":\n" + richiestaBrowser)

    thread = threading.Thread(target = serviCliente(connessione, richiestaBrowser, address))
    thread.deamon = True
    thread.start()

    print('\nconnessioni attive ' + str(threading.activeCount()) + '\n')