#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)

        com1.enable()
        print("Abriu a comunicação")
        
        imageR = 'google1.png'

        imageW = 'recebidaCopia.png'

        print('Carregando imagem para transmissão :')
        print(" - {}".format(imageR))
        print("-------------------------")
        txBuffer = open(imageR, 'rb').read()
        
        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        
        com1.sendData(np.asarray(txBuffer))  

        while True:
            if not com1.tx.threadMutex:
                break
          
        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))

        txLen = len(txBuffer)
        rxBuffer, nRx = com1.getData(txLen)

        print('Salvando dados no arquivo :')
        print(" - {}".format(imageW))
        f = open(imageW, 'wb' )
        f.write(rxBuffer)

        f.close()

        print("recebeu {} bytes" .format(len(rxBuffer)))
        
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
