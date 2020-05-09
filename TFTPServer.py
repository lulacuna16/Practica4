#Protocolo TFTP se monta sobre un protocolo UDP dado que no es orientado a conexion
import socket
ErrorCodes=['No definido','Archivono encontrado','Violacion de permisos','Disco Lleno','Operacion Ilegal en TFTP',
            'Modo Desconocido','Archivo ya existente','Usuario inexistente']
def rrq(Server,data,address):
    """"
    +-----+---~~-----+---+--~~---+---+---~~-+---+---~~---+---+-------+---+---~~---+---+
    | opc | filename | 0 |  mode | 0 | opt1 | 0 | value1 | 0 | optN  | 0 | valueN | 0 |
    +-----+---~~-----+---+--~~---+---+---~~-+---+---~~---+---+-------+---+---~~---+---+

    """
    if (error(data)):
        exit(0)
    print("Recibi una RRQ de {}".format(str(address)))
    x = 2
    name = ""
    while data[x] != 0:
        name += chr(data[x])
        x += 1
    mode = ""
    x+=1
    while data[x] != 0:
        mode += chr(data[x])
        x += 1
    #print(mode)
    option=""
    x += 1
    while data[x] != 0:
        option += chr(data[x])
        x += 1
    #print(option)
    tam = ""
    x += 1
    tam= int.from_bytes(data[x:-1],byteorder='big')
    #print(type(tam),str(tam))
    oack=bytearray() #Hay que construir OACK ya que el pquete recibido vino con opciones
    oack.append(0)
    oack.append(6)
    option=bytearray(option.encode())
    oack+=option
    oack.append(0)
    tamB = tam.to_bytes(2, byteorder='big')
    oack += tamB  # Valor de la opcion 1 en Bytes
    oack.append(0)
    Server.sendto(oack,address)
    Lectura(name,tam)
def ultimoAck(address):
    ack, address = Server.recvfrom(buffer_size)
    if (error(ack)):
        exit(0)
    print("Recibi ultimo ACK")
def Lectura(name,tam): #Lectura
    file = open(""+name+"", 'r')
    content=  file.read(tam)
    while len(content)>0:
        ack, address = Server.recvfrom(buffer_size)
        if (error(ack)):
            exit(0)
        numBlock = int.from_bytes(ack[2:], byteorder='big')
        print("Recibi ACK del Paquete #{} ".format(numBlock))
        """"
          ----------------------------------
          | Opcode |   Block #  |   Data   |
          ----------------------------------
          """
        data = bytearray()
        data.append(0)
        data.append(3)
        data.append(0)
        data.append(numBlock + 1)
        data+=bytearray(content.encode('utf-8'))
        Server.sendto(data, address)
        print("Enviando Paquete {}".format(numBlock + 1))
        content=file.read(tam)
    file.close()
    ultimoAck(address)
def wrq(Server,data,address):
    """"
    +-----+---~~-----+---+--~~---+---+---~~-+---+---~~---+---+-------+---+---~~---+---+
    | opc | filename | 0 |  mode | 0 | opt1 | 0 | value1 | 0 | optN  | 0 | valueN | 0 |
    +-----+---~~-----+---+--~~---+---+---~~-+---+---~~---+---+-------+---+---~~---+---+

    """
    if (error(data)):
        exit(0)
    print("Recibi una WRQ de {}".format(str(address)))
    x = 2
    name = ""
    while data[x] != 0:
        name += chr(data[x])
        x += 1
    mode = ""
    x+=1
    while data[x] != 0:
        mode += chr(data[x])
        x += 1
    #print(mode)
    option=""
    x += 1
    while data[x] != 0:
        option += chr(data[x])
        x += 1
    #print(option)
    tam = ""
    x += 1
    tam= int.from_bytes(data[x:-1],byteorder='big')
    #print(type(tam),str(tam))
    oack=bytearray() #Hay que construir OACK ya que el pquete recibido vino con opciones
    oack.append(0)
    oack.append(6)
    option=bytearray(option.encode())
    oack+=option
    oack.append(0)
    tamB = tam.to_bytes(2, byteorder='big')
    oack += tamB  # Valor de la opcion 1 en Bytes
    oack.append(0)
    Server.sendto(oack,address)
    Escritura(name,tam)
def Escritura(name,tam):
    file = open("" + name + "", 'w') #Abrir archivo donde se escribirá la informacion que el cliente envíe
    data, addres = Server.recvfrom(buffer_size)
    if (error(data)):
        exit(0)
    content = data[4:].decode('utf-8')
    numBlock = int.from_bytes(data[2:4], byteorder='big')
    while len(content) <= tam:
        if len(content) != tam:
            print("Ultimo, Paquete: {}".format(numBlock))
            file.write(content)
            print("\n¡No hay mas datos, enviando ultimo ack!")
            ack(address, numBlock)
            break
        else:
            print("Paquete: {}".format(numBlock))
            file.write(content)
            ack(address, numBlock)
            data, addres = Server.recvfrom(buffer_size)
            if (error(data)):
                exit(0)
            content = data[4:].decode('utf-8')
            numBlock = int.from_bytes(data[2:4], byteorder='big')
    file.close()
def ack(Client,numBlock):
    """"
    ---------------------------
      | Opcode |   Block #  |
    ---------------------------
    """
    ack=bytearray()
    ack.append(0)
    ack.append(4)
    ack.append(0)
    ack.append(numBlock)
    Server.sendto(ack,Client)
def error(paquete): #Paquete de error
    """
               2 bytes     2 bytes      string    1 byte
               -----------------------------------------
              | Opcode |  ErrorCode |   ErrMsg   |   0  |
               -----------------------------------------
    """
    OpCode=int.from_bytes(paquete[:2], byteorder='big')
    if OpCode==5:
        print("Terminacion Prematura.\nError ")
        ErrorCode=int.from_bytes(paquete[2:4], byteorder='big')
        print("{}. {}".format(ErrorCode,ErrorCodes(ErrorCode)))
        return True
HOST="192.168.1.105"
PORT=56432
buffer_size=1024

with  socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as Server:
    Server.bind((HOST, PORT))

    print("Servidor TFTP Listo y esperando en el puerto: {}".format(PORT))
    # Listen for incoming datagrams

    while True:
        data,address = Server.recvfrom(buffer_size)
        opc=int.from_bytes(data[0:2],byteorder='big')
        if opc == 1:
            rrq(Server,data,address)
            print("\n")
            #break
        elif opc == 2:
            wrq(Server, data, address)
            print("\n")
            #break
        elif opc == 5:
            error(data)
            break