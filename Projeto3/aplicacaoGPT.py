# Servidor

from enlace import *
import time

serialName = "COM4"  # Porta serial a ser utilizada

HEAD_SIZE = 12
PAYLOAD_MAX_SIZE = 2500
EOP = b'\xAA\xBB\xCC'  # Exemplo de EOP de 3 bytes

def main():
    try:
        com2 = enlace(serialName)

        print("-------------------------")
        print("Iniciou o main")
        
        com2.enable()
        print("Abriu a comunicação")
        print("-------------------------")
        
        print("\nEsperando 1 byte de sacrifício")
        rxBuffer, nRx = com2.getData(1)
        com2.rx.clearBuffer()
        time.sleep(.1)

        print("Servidor pronto")

        while True:
            if com2.rx.getBufferLen() > 0:
                handshake, _ = com2.getData(9)
                if handshake == b'handshake':
                    com2.sendData(b's')
                    print("Handshake realizado")
                    break

        pacote_num = 1
        received_data = b''

        while True:
            datagram, _ = com2.getData(HEAD_SIZE) # HEAD + PAYLOAD_MAX_SIZE + EOP
            head = datagram[:12]

            pacote_atual = int.from_bytes(head[:4], byteorder='big')
            total_pacotes = int.from_bytes(head[4:8], byteorder='big')
            payload_size = int.from_bytes(head[-4:], byteorder='big')

            datagram2, _ = com2.getData(payload_size + 3)
            # print(datagram)
            # print(datagram2)
            payload = datagram2[:payload_size]
            eop = datagram2[-3:]
            
            if eop == EOP and pacote_atual == pacote_num:
                received_data += payload
                com2.sendData(b's')
                print(f"Pacote {pacote_num} recebido com sucesso")
                pacote_num += 1
            else:
                com2.sendData(b'n')
                print("Erro na recepção, solicitando reenvio")

            if pacote_num > total_pacotes:
                break

        with open('arquivo_recebido.png', 'wb') as file:
            file.write(received_data)

        # print("Arquivo recebido com sucesso")
        com2.disable()

    except Exception as erro:
        print("Erro:", erro)
        com2.disable()

if __name__ == "__main__":
    main()