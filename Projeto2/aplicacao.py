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
import struct
import random
import time


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
        print('----------------------')
        print("Iniciou o main")
        com1 = enlace(serialName)

        print("Abriu a comunicação para enviar o byte de sacrifício")
        com1.enable()
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
        print('----------------------\n')

        # Escolhendo os valores aleatoriamente
        valores = [
            round(random.uniform(-1*(10**10), 1*(10**10)), 6) 
            for _ in range(random.randint(5,15))
        ]

        # Colocas os valores float em IEEE 754 e encoda para mandar os bits
        encoded_v = [
            float_to_binary32(e).encode() 
            for e in valores
        ]

        # Completa a lista com 0's
        while len(encoded_v) < 15:
            encoded_v.append(float_to_binary32(0).encode())

        print('Iniciando o envio')
        txBuffer = encoded_v
        com1.sendData(np.asarray(txBuffer))  

        print(f'\nMeu array de bytes tem tamanho: {len(txBuffer)}')

        while True:
            if not com1.tx.threadMutex:
                break
        
        # Quantidade de bits enviados
        txSize = com1.tx.getStatus()
        print(f'Enviou = {txSize} bits')

        # Recebimento dos dados
        txLen = 32
        rxBuffer, nRx = com1.getData(txLen)

        print(f'Recebeu {len(rxBuffer)} bits')

        print(f'\n\nSoma calculada: {float_to_binary32(sum(valores))}')
        print(f'Soma recebida:{rxBuffer}')
        print(f'Valor em float calculado: {sum(valores)}')
        print(f'Valor em float recebido: {binary32_to_float(rxBuffer)}')
        dif = abs((1-(binary32_to_float(rxBuffer)/sum(valores)))*100)
        print(f'Diferença percentual: {dif:.10f} %')

        verifica(dif)
        
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

def verifica(dif):
    if dif > 0.001:
        print('Diferença muito grande, soma errada')
    else:
        print('Aceitavel')

def binary32_to_float(binary_str):
    """Converte uma string binária IEEE 754 (32 bits) para um número float."""
    # Converte a string binária de volta para inteiro
    int_value = int(binary_str, 2)
    # Converte o inteiro para bytes
    packed_value = int_value.to_bytes(4, byteorder='big')
    # Usa struct.unpack para desempacotar os bytes para float
    float_value = struct.unpack('>f', packed_value)[0]
    return float_value

def float_to_binary32(value):
    bits, = struct.unpack('!I', struct.pack('!f', value))
    return f'{bits:032b}'
        
#so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
