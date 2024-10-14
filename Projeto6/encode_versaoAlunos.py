
#importe as bibliotecas
# from suaBibSignal import signalMeu
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys
from scipy import signal
from scipy.fftpack import fft, fftshift

#funções caso queriram usar para sair...
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def get_freq (tecla) -> tuple:
    frequencias = {
        '1':[1209, 679],
        '2':[1336, 679],
        '3':[1477, 679],
        '4':[1209, 770],
        '5':[1336, 770],
        '6':[1477, 770],
        '7':[1209, 825],
        '8':[1336, 825],
        '9':[1477, 825],
        'A':[679, 1633],
        'B':[770, 1633],
        'C':[825, 1633],
        'D':[941, 1633],
        'X':[941, 1209],
        '0':[941, 1336],
        '#':[941, 1477]
    }
    return frequencias[tecla][0], frequencias[tecla][1]

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
    plt.title('Fourier')

def generate_signal(freq1, freq2, taxa_amostragem):
    t_inicial = 0
    t_final = 0.5 #aumentando o tempo para poder tocar
    tamanho_intervalo = (1/taxa_amostragem)
    t = np.arange(t_inicial,t_final,tamanho_intervalo)

    w1 = 2*np.pi*freq1
    w2 = 2*np.pi*freq2
    sen1 = np.sin(w1*t)
    sen2 = np.sin(w2*t)

    signal = sen1 + sen2
    plt.plot(t[:500], signal[:500])
    plt.title('Signal')
    plt.ylabel('y')
    plt.xlabel('t')

    return signal
    

def main():
    
   
    #********************************************instruções*********************************************** 
    # Seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada, conforme tabela DTMF.
#OK # Então, inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF. 
#OK # De posse das duas frequeências, agora voce tem que gerar, por alguns segundos suficientes para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada.
#OK # Essas senoides têm que ter taxa de amostragem de 44100 amostras por segundo, sendo assim, voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
#OK # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t).
#OK # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
#OK # Some as duas senoides. A soma será o sinal a ser emitido.
#OK # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Você pode gravar o som com seu celular ou qualquer outro microfone para o lado receptor decodificar depois. Ou reproduzir enquanto o receptor já capta e decodifica.
    
#OK # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado, como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    # Escolhendo tecla
    tecla = 'X'

    #Obtendo frequencias da tecla
    freq1, freq2 = get_freq(tecla)

    #Gerando senoide resultante
    taxa_amostragem = 44100
    signal = generate_signal(freq1, freq2, taxa_amostragem)

    sd.play(signal, taxa_amostragem) #nao toca
    # aguarda fim do audio
    sd.wait()
    
    plotFFT(signal, taxa_amostragem) #nao entendi fourier
    # Exibe gráficos
    plt.show()
    

if __name__ == "__main__":
    main()
