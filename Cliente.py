import http.client
def Get(conn):
    conn.request("GET", "/")
    response = conn.getresponse()
    while True:
        chunk = response.read(200)  # 200 bytes
        if not chunk:
            break
        print(repr(chunk))
    valCod(response)
def Head(conn):
    conn.request("HEAD", "/")
    response = conn.getresponse()
    valCod(response)
def Post(conn):
    headers={"Accept": "text"}
    conn.request("POST", "/","HOLA CON POST REQUEST",headers)
    response = conn.getresponse()
    while True:
        chunk = response.read(200)  # 200 bytes
        if not chunk:
            break
        print(str((chunk),'ascii'))
    valCod(response)
def Put(conn):
    headers = {"Accept": "text"}
    conn.request("PUT", "/","HOLA CON PUT REQUEST",headers)
    response = conn.getresponse()
    while True:
        chunk = response.read(200)  # 200 bytes
        if not chunk:
            break
        print(str(chunk,'ascii'))
    valCod(response)
def Delete(conn):
    headers = {"Accept": "text"}
    conn.request("DELETE", "/","HOLA CON DELETE REQUEST",headers)
    response = conn.getresponse()
    while True:
        chunk = response.read(200)  # 200 bytes
        if not chunk:
            break
        print(str(chunk,'ascii'))
    valCod(response)
def Connect(conn):
    conn.request("CONNECT", "/")
    response = conn.getresponse()
    while True:
        chunk = response.read(200)  # 200 bytes
        if not chunk:
            break
        print(repr(chunk))
    valCod(response)
def Options(conn):
    conn.request("OPTIONS", "/")
    response = conn.getresponse()
    while True:
        chunk = response.read(200)  # 200 bytes
        if not chunk:
            break
        print(repr(chunk))
    valCod(response)
def Trace(conn):
    conn.request("TRACE", "/")
    response = conn.getresponse()
    while True:
        chunk = response.read(200)  # 200 bytes
        if not chunk:
            break
        print(repr(chunk))
    valCod(response)
def valCod(response):
    code=response.status
    if code==100:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==101:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==200:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==202:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==203:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==204:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==205:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==206:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==300:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==301:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==302:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==303:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==304:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==305:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==307:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==400:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==401:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==404:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==403:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==404:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==405:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==406:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==407:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==408:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==409:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==410:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==411:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==412:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==413:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==414:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==415:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==416:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==417:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==426:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==500:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==501:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==502:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==503:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==504:
        print("Codigo: {}. {}".format(code,response.reason))
    elif code==505:
        print("Codigo: {}. {}".format(code,response.reason))
def menu(ClientConn,case):
    if case is 1:
        Get(ClientConn)
    elif case is 2:
        Head(Clientconn)
    elif case is 3:
        Post(Clientconn)
    elif case is 4:
        Put(Clientconn)
    elif case is 5:
        Delete(Clientconn)
    elif case is 6:
        Connect(Clientconn)
    elif case is 7:
        Options(Clientconn)
    elif case is 8:
        Trace(Clientconn)
    else:
        print("Opcion no valida\n")

def verMenu(Clientconn):
    seguir=True
    while(seguir):
        print("Menu de Solicitudes. Escoge un número:")
        print("1.GET\n2.HEAD\n3.POST\n4.PUT\n5.DELETE\n6.CONNECT\n7.OPTIONS\n8.TRACE")
        case = int(input("Opcion: "))
        menu(Clientconn,case)
        Option= int(input("1.Continuar\n2.Salir\nElige una opcion:"))
        if Option==1: seguir=True
        else: seguir=False
    Clientconn.close()

HOST = str(input("Ingrese IP del servidor: "))
PORT = int(input("Ingrese Puerto del servidor: "))
#HOST = "192.168.1.64"
#PORT = 56432
Clientconn=http.client.HTTPConnection(HOST,PORT)
verMenu(Clientconn)