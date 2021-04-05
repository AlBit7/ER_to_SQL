import http.server, socketserver, os.path, cgi
from main import *

PORT = 8080
SERVER = '192.168.1.108'
FORMATO = 'utf-8'
PATH = os.path.dirname(__file__).replace("\\", "/")

class handler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        
        if self.path == "/":
            self.path = "/index.html"

        try:

            file = open(PATH + self.path, 'r')
            html = file.read()
            file.close()

            self.send_response(200)

        except:

            html = """<p>Pagina non trovata, ritorna a&nbsp;</p><a href="/">casa</a>"""
            
            self.send_response(404)
        
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(html.encode(FORMATO))

    def do_POST(self):

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE':self.headers['Content-Type']}
        )

        try:
            
            payload = form.getvalue("fileDaParsare").decode('utf-8-sig')
            er = ER(payload)
            output = er.displaySQL().replace("\n", "<br>").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
            
            file = open(PATH + "/output.html", 'r')
            html = file.read()
            file.close()

            html = html.replace("$$", output)
            self.send_response(200)
        
        except:

            self.send_response(500)
            html = "<p>errore server o file corrotto/mancante</p>"

        
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(html.encode(FORMATO))

def main():
    
    try:

        with socketserver.TCPServer((SERVER, PORT), handler) as httpd:
            print("server in ascolto su " + SERVER + ":" + str(PORT) + "...")
            httpd.serve_forever()

    except KeyboardInterrupt:
        
        print('spegnimento...')
        httpd.server_close()

if __name__ == '__main__':
    main()

"""
import socket, threading, os.path
from main import *

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

    # prova a leggere il file richiesto
    try:
        file = open(PATH + paginaRichiesta, 'r')
        html = file.read()
        file.close()
        header = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'

    except:
        header = 'HTTP/1.1 404 NOT FOUND\nContent-Type: text/html\n\n'
        html = "<p>Pagina non trovata</p><br><a href="/">casa</a>"

    if method == 'GET':
        pass

    if method == 'POST':

        header = 'HTTP/1.1 200\nContent-Type: text/html\n\n'
        html += "ciao"

        # try:
        #     # nomeFile = richiesta.split("\r\n")[-1][2:]
        #     # contenutoFile = 0# ??open(nomeFile, 'r').read()
        #     # print("contenuto: "+contenutoFile)
        #     # er = ER(contenutoFile)
        #     # html += "<p>" + er.displaySQL() + "</p>"
        #     # contenutoFile.close()
        #     header = 'HTTP/1.1 200\nContent-Type: text/html\n\n'
        #     html += "<p>ciao</p>"

        # except:
            
        #     header = 'HTTP/1.1 200\nContent-Type: text/html\n\n'
        #     html += "<p>errore server</p>"

    risposta = header + html

    connessione.sendall(risposta.encode(FORMATO))
    connessione.close()

while True:

    connessione, address = soc.accept()
    richiestaBrowser = connessione.recv(BUFFER).decode(FORMATO)

    if richiestaBrowser != "":

        print(str(address[0]) + ":\n" + richiestaBrowser)

        thread = threading.Thread(target = serviCliente(connessione, richiestaBrowser, address))
        thread.deamon = True
        thread.start()

        print('\nconnessioni attive ' + str(threading.activeCount()) + '\n')
"""
