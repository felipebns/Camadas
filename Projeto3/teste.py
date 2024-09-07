def detectar_acao(dicionario, stop):
    verbos = ['ar', 'er', 'ir', 'or']
    acoes_dict = {}

    for usuarios_dict, acoes in dicionario.items():
        acoes_dict[usuarios_dict] = []
        
        for data, frase in acoes.items():
            nova_frase = ''
            pegou_verbo = False
            for e in frase.split():
                if e[-2:] in verbos and e not in stop and not(pegou_verbo):
                    nova_frase += e
                    pegou_verbo = True
                elif pegou_verbo and e not in stop:
                    nova_frase += ' ' + e
                    pegou_verbo = False
            acoes_dict[usuarios_dict].append(nova_frase)

    for usuario, lista_acoes in acoes_dict.items():
        i = 0
        for e in lista_acoes:
            if e == '':
                lista_acoes.pop(i)
            i += 1
                

    return acoes_dict






print(detectar_acao({
    'zezin1': {
        '2020-11-05 08:15:30' : 'eita mundo velho sem fronteira',
        '2020-11-05 08:16:01' : 'no são joão vamos festejar juntos',
    },
    'mariarita': {
        '2020-10-01 05:05:00' : 'gostei',
        '2020-10-01 05:05:09' : 'do notebook, vou comprar outro pra minha empresa',
        '2020-10-01 05:08:39' : 'vai também?'
    },
    'juca123': {
        '2021-02-09 05:05:00' : 'não consigo parar de rir do comediante',
        '2021-02-09 05:05:09' : 'euaeuaeuaeuaeu'
    },
    'camila': {
        '2021-02-09 09:05:09' : 'alexa, como está o clima?'
    },
    'zelia': {
        '2021-02-09 09:05:09' : 'hoje quero nadar'
    }
}, [
    'do', 'da', 'de', 'já',  'a',
    'um', 'o', 'no', 'na', 'para',
    'uma', 'do', 'da', 'dos', 'das'
]))