
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
from scipy import signal
from scipy.fftpack import fft, fftshift
from encode_versaoAlunos import main as encode


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def calcFFT(signal, fs):
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    #y  = np.append(signal, np.zeros(len(signal)*fs))
    N  = len(signal)
    T  = 1/fs
    xf = np.linspace(-1.0/(2.0*T), 1.0/(2.0*T), N)
    yf = fft(signal)
    return(xf, fftshift(yf))

def plotFFT(signal, fs):
    x,y = calcFFT(signal, fs)
    plt.figure()
    plt.plot(x, np.abs(y))
    plt.title('Fourier Ouvido')
    plt.ylabel('Magnitude')
    plt.xlabel('Frequência')
    plt.xlim(0, 25000) #não mostra as frequências negativas
    plt.show()

def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    taxa_de_amostragem = 44100
    numCanais = 1 # mono, não existe distinção entre esquerda e direita, é igual para os dois
    sd.default.samplerate = taxa_de_amostragem #taxa de amostragem
    sd.default.channels = numCanais #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas.

    #Muitas vezes a gravação retorna uma lista de listas. Você poderá ter que tratar o sinal gravado para ter apenas uma lista.

    duration = 1.5 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic   

    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisições) durante a gravação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = taxa_de_amostragem * duration

    #para gravar, utilize
    print('Gravando')
    # encode()

    audio = sd.rec(int(numAmostras), taxa_de_amostragem, channels=numCanais)

    sd.wait()
    print("...     FIM")
    #audio tem 1 colunas e 44100 linhas

    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, ou uma lista, ou ainda uma lista de listas (isso dependerá do seu sistema, drivers etc...).
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    dados = audio #tem apenas 1 coluna
    dados_db = []

    for i in range(len(dados)):
        dados_db.append(todB(dados[i]))

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.arange(0, duration, 1/taxa_de_amostragem)

    t_a = np.arange(0, 66150 , 1)

    plt.plot(t, dados)
    plt.title('A')
    plt.show()
    
    

    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
    # plt.plot(t[:500], [todB(dado) for dado in dados][:500])
    # plt.title('Sinal ouvido')
    # plt.ylabel('Magnitude')
    # plt.xlabel('t')
    # plt.show()
       
    ## Calcule e plote o Fourier do sinal audio. como saída tem-se a amplitude e as frequências.
    plotFFT(dados, taxa_de_amostragem)

    sd.play(audio, taxa_de_amostragem) 
    
    #Agora você terá que analisar os valores xf e yf e encontrar em quais frequências estão os maiores valores (picos de yf) de da transformada.
    #Encontrando essas frequências de maior presença (encontre pelo menos as 5 mais presentes, ou seja, as 5 frequências que apresentam os maiores picos de yf). 
    #Cuidado, algumas frequências podem gerar mais de um pico devido a interferências na tranmissão. Quando isso ocorre, esses picos estão próximos. Voce pode desprezar um dos picos se houver outro muito próximo (5 Hz). 
    #Alguns dos picos  (na verdade 2 deles) devem ser bem próximos às frequências do DTMF enviadas!
    #Para descobrir a tecla pressionada, você deve encontrar na tabela DTMF frquências que coincidem com as 2 das 5 que você selecionou.
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    
    #printe os picos encontrados! 
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    ## Exiba gráficos do fourier do som gravados 
    # plt.show()

if __name__ == "__main__":
    main()
