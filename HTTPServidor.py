from http.server import HTTPServer, BaseHTTPRequestHandler
import datetime

class Handler(BaseHTTPRequestHandler): #Clase que nos va a permitir manejar las solicitudes entrantes de acuerdo a cada tipo
    def enviar_codigo(self):
        #Todos los tipos de solicitudes ocupan la accion de enviar al cliente el codigo de estado de respuesta
        self.send_response(200)
        #Se envia el codigo 200 que indica que la solicitud ha procedido correctamente y se envia un mensaje al cliente
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
    def do_GET(self): #Manejar Get Request
        self.enviar_codigo()
        self.wfile.write("Peticion GET Recibida.".encode()) #Contiene el flujo de salida para regresarle una respuesta al cliente
    def do_HEAD(self):
        self.enviar_codigo() #Las peticiones Head solo envian el codigo de estado de la respuesta
    def do_POST(self):
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len) #Se agrega a la respuesta el mensaje que cliente envio
        self.enviar_codigo()
        msg="Peticion POST Recibida.\nRecibi: {}".format(post_body)
        self.wfile.write(msg.encode())
    def do_PUT(self):
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len)  # Se agrega a la respuesta el mensaje que cliente envio
        self.enviar_codigo()
        msg="Peticion PUT Recibida.\nRecibi: {}".format(post_body)
        self.wfile.write(msg.encode())
    def do_DELETE(self):
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len)  # Se agrega a la respuesta el mensaje que cliente envio
        self.enviar_codigo()
        msg="Peticion DELETE Recibida. Elemento Eliminado"
        self.wfile.write(msg.encode())
    def do_CONNECT(self):
        self.enviar_codigo()
        fecha=datetime.datetime.now()
        #Se imprime la fecha en que se establecio la conexion cliente-servidorpara fines ilustrativos
        msg="Peticion CONNECT Recibida. Conexion hecha el: {}/{}/{}".format(fecha.day,fecha.month,fecha.year)
        self.wfile.write(msg.encode())
    def do_OPTIONS(self):
        self.enviar_codigo()
        self.wfile.write("Peticion OPTIONS Recibida.".encode())
    def do_TRACE(self):
        self.enviar_codigo()
        self.wfile.write("Peticion TRACE Recibida.".encode())

HOST="192.168.1.64" #IP del servidor
PORT=56432 #Puerto

#La clase HTTPServer permite montar un servidor HTTP incluyendo el manejador de solicitudes, clase'Handler'
with HTTPServer((HOST,PORT),Handler) as Servidor:
    print("Servidor Listo.\nIP: {}\nPort: {}".format(HOST,PORT))
    Servidor.serve_forever()