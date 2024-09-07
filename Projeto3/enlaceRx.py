#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Threads
import threading

# Class
class RX(object):
  
    def __init__(self, fisica):
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024

    def thread(self): 
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp  
                time.sleep(0.01)

    def threadStart(self):       
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        self.threadStop = True

    def threadPause(self):
        self.threadMutex = False

    def threadResume(self):
        self.threadMutex = True

    def getIsEmpty(self):
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self): #pega tamanho
        return(len(self.buffer))

    def getAllBuffer(self): #esse len é um erro!, pega tudo
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData): # pega até uma certa posição
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNData(self, size, timeout=20): #apenas uma abstração para trabalhos futuros, tem a mesma funcionalidade do get buffer
        while(self.getBufferLen() < size):
            time.sleep(0.05)
            timeout -= 0.05         
            if timeout <= 0:
                raise Exception('TimeOut')
        return(self.getBuffer(size))
    
    # def getNData(self, size, timeout=5):
    #     data = b''  # Buffer para armazenar os dados recebidos
    #     start_time = time.time()  # Tempo de início para controle do timeout

    #     while len(data) < size:
    #         if self.getBufferLen() > 0:
    #             # Calcula o tamanho de dados que ainda precisamos receber
    #             missing_data_size = size - len(data)
                
    #             # Garante que não tentaremos pegar mais do que o disponível no buffer
    #             data_chunk = self.getBuffer(min(missing_data_size, self.getBufferLen()))
    #             data += data_chunk  # Adiciona o pedaço recebido ao buffer total
    #         else:
    #             # Verifica se o timeout foi atingido
    #             if (time.time() - start_time) > timeout:
    #                 raise Exception('Timeout: Não foi possível receber todos os dados')
    #             time.sleep(0.05)  # Espera antes de verificar o buffer novamente

    #     return data


    def clearBuffer(self):
        self.buffer = b""


