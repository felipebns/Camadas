#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2022
# Aplicação
####################################################

from enlace import *
import time
import numpy as np
from crc import Calculator, Crc16

serialName = "/dev/ttyACM0"

HEAD_SIZE = 12
PAYLOAD_SIZE = 50
EOP = b"\xFF\xFF\xFF"

def write_log(is_envio, type_package, len_package, package_num, total_packages, crc):

    with open("log.txt", "a") as log:
        date = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
        if is_envio:
            log.write(f'{date} / envio / {type_package} / {len_package} / {package_num} / {total_packages} / {crc}\n')
        else:
            log.write(f'{date} / receb / {type_package} / {len_package}\n')

def create_datagram(type, error_type, pacote_num, total_packages, payload_size, payload):
    # Cria o cabeçalho do pacote
    # HEAD: type[1]|type_of_error[1]|pacote_num[3]|total_of_packages[3]|payload_size[4]
    
    # type: 0-handshake, 1-data, 2-error, 3-ack
    # error_type: 0-no error, 1-timeout, 2-wrong package, 3-wrong EOP
    
    head = type.to_bytes(1, byteorder='big') + error_type.to_bytes(1, byteorder='big') + pacote_num.to_bytes(3, byteorder='big') + total_packages.to_bytes(3, byteorder='big') + payload_size.to_bytes(4, byteorder='big')
    datagram = head + payload + EOP
    
    return datagram

def prepare_package(head):
    tipo = head[0]
    tipo_erro = head[1]
    n_do_pacote = int.from_bytes(head[2:5], byteorder="big")
    total_pacotes = int.from_bytes(head[5:8], byteorder="big")
    len_payload = int.from_bytes(head[8:10], byteorder="big")
    crc = int.from_bytes(head[10:12], byteorder="big")
    
    return tipo, tipo_erro, n_do_pacote, total_pacotes, len_payload, crc

def main():
    try:
        print("Iniciou o main\n")
        com1 = enlace(serialName)
        com1.enable()
        time.sleep(.1)
        
        print('=======================================================')

        print("\nAbriu a comunicação")

        while True:
            if com1.rx.getBufferLen() > 0:
                handshake, _ = com1.getData(15)
                head = handshake[0:12]

                write_log(False, 0, 0, 0, 0, 0)

                print(handshake)
                if head[0] == 0:
                    print('\nHandshake recebido!')
                    print('\n=======================================================')
                    print('\nEnviando de volta')
                    handshake = create_datagram(0,0,0,0,0,b'')
                    com1.sendData(handshake)

                    write_log(True, 0, 0, 0, 0, 0)

                    break
                else:
                    print(f'\nNão foi handshake. Foi: {head[0]}')
                    return

        print('\nSucesso no handshake')
        print('\n=======================================================\n\n')

        print('\nIniciando a recepção dos dados')

        print('\n=======================================================\n\n')    

        # Primeiro HEAD, vai definir TOTAL_PACOTES
        recebido = []
        head, _ = com1.getData(12)

        calculator = Calculator(Crc16.XMODEM)

        if head[0] == 1:
            tipo, tipo_erro, n_do_pacote, total_pacotes, len_payload, crc = prepare_package(head)

            # Se só tiver um pacote:
            if total_pacotes == 1:
                payload, _ = payload, _ = com1.getData(len_payload)
                eop, _ = com1.getData(3)

                write_log(False, 1, len_payload+15, 0, 0, 0)

                expected = calculator.checksum(payload)
            
                if expected == crc:

                    if eop != EOP:
                        print('EOP TA ERRADO')
                        return

                    # Confirmando recebimento de pacote:
                    recebido.append(payload)
                    msg = create_datagram(3, 0, n_do_pacote, total_pacotes, 0, b'')
                    com1.sendData(msg)


                    write_log(True, 1, 15, 1, 1, expected)

            else:
                # Pegando o resto do pacote, e confirmando o recebimento:
                i = 2


                payload, _ = com1.getData(len_payload)
                eop, _ = com1.getData(3)

                write_log(False, 1, len_payload+15, 0, 0, 0)
                expected = calculator.checksum(payload)
                
                print(expected)
                print(crc)
                print('AAAAAAAAAAAAAAAAAAAAAA')

                ##### CONTINUAR DAQUI!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                if eop != EOP:
                    print('EOP TA ERRADO')
                    return
                
                if expected == crc:
                    recebido.append(payload)
                    msg = create_datagram(3, 0, n_do_pacote, total_pacotes, 0, b'')
                    com1.sendData(msg)

                    write_log(True, 3, 15, n_do_pacote, total_pacotes, expected)
                
                # Pegando o resto dos pacotes:
                while i <= (total_pacotes):
                    # Tratamento caso seja o ultimo pacote
                    if i == total_pacotes:
                        head, _ = com1.getData(12)
                        tipo, tipo_erro, n_do_pacote, total_pacotes, crc, len_payload = prepare_package(head)

                        expected = calculator.checksum(payload)

                        if expected == crc:

                            write_log(False, 1, len_payload+15, 0, 0, 0)

                            resto, _ = com1.getData(len_payload + 3)
                            payload = resto[:-3]
                            eop = resto[-3:]

                            if eop != EOP:
                                print('EOP TA ERRADO')
                                return
                            
                            recebido.append(payload)
                            msg = create_datagram(3, 0, n_do_pacote, total_pacotes, 0, b'')
                            com1.sendData(msg)


                            write_log(True, 3, 15, n_do_pacote, total_pacotes, expected)

                            i += 1
               
                    else:
                        print(f'\n\nNOVO PACOTE')
                        full_package, _ = com1.getData(65)
                        head = full_package[0:12]
                        payload = full_package[12:-3]
                        eop = full_package[-3:]
                        tipo, tipo_erro, n_do_pacote, total_pacotes, crc, len_payload = prepare_package(head)

                        write_log(False, 1, len_payload+15, 0, 0, 0)

                        expected = calculator.checksum(payload)

                        if crc == expected:

                            print(f"Número do pacote: {n_do_pacote}\n")

                            if eop == EOP and n_do_pacote == i and len_payload == len(payload):
                                recebido.append(payload)
                                msg = create_datagram(3, 0, n_do_pacote, total_pacotes, 0, b'')
                                com1.sendData(msg)


                                write_log(True, 3, 15, n_do_pacote, total_pacotes, expected)

                                i += 1
                            else:
                                print(f'Repetindo o pacote {i}')
                                recebido.pop(-1)
                                msg = create_datagram(2, 0, i, total_pacotes, 0, b'')
                                com1.sendData(msg)

                                write_log(True, 2, 15, n_do_pacote, total_pacotes, expected)

                                i -= 1

        print('\n=======================================================\n')
        
        print('\nRecepção de dados finalizada')
        # print(f'Mensagem: {recebido}')
        with open('arquivo_recebido.txt', 'wb') as file:
            for el in recebido:
                file.write(el)
        
        # Encerra comunicação
        print('\n=======================================================')
        print("Comunicação encerrada")
        print('\n=======================================================')
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


#so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao 
if __name__ == "__main__":
    main()
