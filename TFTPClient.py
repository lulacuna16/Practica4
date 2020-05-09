import socket

OpCodes = ['No Especificado','RRQ', 'WRQ','DATA','ACK','ERROR'] #Codigos de operación
Modes = ['netascii','octet','mail'] #Modos de transferencia
ErrorCodes=['No definido','Archivono encontrado','Violacion de permisos','Disco Lleno','Operacion Ilegal en TFTP',
            'Modo Desconocido','Archivo ya existente','Usuario inexistente']
def rrq(filename,modo,Client): #RRQ request
    """"
       +-----+---~~-----+---+--~~---+---+---~~-+---+---~~---+---+-------+---+---~~---+---+
       | opc | filename | 0 |  mode | 0 | opt1 | 0 | value1 | 0 | optN  | 0 | valueN | 0 |
       +-----+---~~-----+---+--~~---+---+---~~-+---+---~~---+---+-------+---+---~~---+---+
    """
    #dado que solo se va enviar bytes, el paquete debe ser enviado como un bytearray
    request=bytearray()
    #primeros dos bytes del paquete
    request.append(0)
    request.append(1) #Codigo para solicitud RRQ
    filename=bytearray(filename.encode())
    request+=filename #Se anexa el nombre del archivoal paquete
    request.append(0) #Valor por defecto del pquete
    modo=bytearray(modo.encode())
    request+=modo #Se agrega el modo
    request.append(0) #valor por defecto del paquete
    blksize=bytearray("blksize".encode())#Opcion del paquete
    request+=blksize
    request.append(0)
    tamB=tam.to_bytes(2,byteorder='big')
    request+=tamB#Valor de la opcion 1
    request.append(0)
    Client.sendto(request,Server_Address)
    oack,addres=Client.recvfrom(buffer_size) #Recibe el acuse oack
    if(error(oack)):
        exit(0)
    Lectura(Client,tam)
def ack(Client,numBlock):
    """"
     -------------------------
      | Opcode |   Block #  |
    --------------------------
    """
    ack=bytearray()
    ack.append(0)
    ack.append(4)
    ack.append(0)
    ack.append(numBlock)
    Client.sendto(ack,Server_Address)
def Lectura(Client,tam):
    ack(Client,0)
    data, addres = Client.recvfrom(buffer_size)
    if (error(data)):
        exit(0)
    content=data[4:].decode('utf-8')
    numBlock = int.from_bytes(data[2:4], byteorder='big')
    while len(content)<=tam:
        if len(content)!=tam:
            print("Ultimo, Paquete: {}".format(numBlock))
            print(content)
            print("\n¡No hay mas datos, enviando ultimo ack!")
            ack(Client, numBlock)
            print("\nTerminacion normal")
            break
        else:
            print("Paquete: {}".format(numBlock))
            print(content)
            ack(Client,numBlock)
            data, addres = Client.recvfrom(buffer_size)
            if (error(data)):
                exit(0)
            content = data[4:].decode('utf-8')
            numBlock = int.from_bytes(data[2:4], byteorder='big')

def wrq(filename,modo,Client): #WRQ request
    """"
       +-----+---~~-----+---+--~~---+---+---~~-+---+---~~---+---+-------+---+---~~---+---+
       | opc | filename | 0 |  mode | 0 | opt1 | 0 | value1 | 0 | optN  | 0 | valueN | 0 |
       +-----+---~~-----+---+--~~---+---+---~~-+---+---~~---+---+-------+---+---~~---+---+
    """
    #dado que solo se va enviar bytes, el paquete debe ser enviado como un bytearray
    request=bytearray()
    #primeros dos bytes del paquete
    request.append(0)
    request.append(2) #Codigo para solicitud WRQ
    filename=bytearray(filename.encode())
    request+=filename #Se anexa el nombre del archivoal paquete
    request.append(0) #Valor por defecto del pquete
    modo=bytearray(modo.encode())
    request+=modo #Se agrega el modo
    request.append(0) #valor por defecto del paquete
    blksize=bytearray("blksize".encode())#Opcion del paquete
    request+=blksize
    request.append(0)
    tamB=tam.to_bytes(2,byteorder='big')
    request+=tamB#Valor de la opcion 1
    request.append(0)
    Client.sendto(request,Server_Address)
    oack,addres=Client.recvfrom(buffer_size) #Recibe el acuse oack
    if (error(oack)):
        exit(0)
    Escritura(Client,tam)
def ultimoAck():
    ack, address = Client.recvfrom(buffer_size)
    if (error(ack)):
        exit(0)
    print("Recibi ultimo ACK")
    print("\nTerminacion normal\n")
def Escritura(Client,tam): #Escritura
    numBlock=0
    file = open("Hagamos un trato_ M. Benedetti.txt", 'r') #Archivo del cual se va a extraer el texto
    content= file.read(tam)
    while len(content)<=tam:
        #Construir paquete data
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
        Client.sendto(data, Server_Address)
        print("Enviando Paquete {}".format(numBlock + 1))
        if len(content)!=tam:
            ultimoAck()
            break
        else:
            ack, address = Client.recvfrom(buffer_size)
            if (error(ack)):
                exit(0)
            numBlock = int.from_bytes(ack[2:], byteorder='big')
            print("Recibi ACK del Paquete #{} ".format(numBlock))
            content=file.read(tam)
    file.close()

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
def menu(Client,case):
    if case==1:
        rrq("TFTP.txt", Modes[1], Client)
    elif case==2:
        wrq("Vacio.txt", Modes[1], Client)
Server_Address=("192.168.1.105",56432) #IP y puerto del servidor
buffer_size=512
tam=120 #Tamaño para los datos que van a ser enviados
with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as Client:
    # Send to server using created UDP socket
    seguir=True
    while (seguir):
        print("Menu de Solicitudes. Escoge un número:")
        print("1.Read request (RRQ)\n2.Write request (WRQ)")
        case = int(input("Opcion: "))
        menu(Client, case)
        Option = int(input("1.Continuar\n2.Salir\nElige una opcion:"))
        if Option == 1:
            seguir = True
            print("\n")
        else:
            seguir = False


