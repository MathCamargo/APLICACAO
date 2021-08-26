import tweepy
from os import environ
from time import gmtime, sleep
import requests

# CONFIGURAÇÃO DE HORÁRIO #
hr_postar = 21
min_postar = 40

# CONFIGURAÇÃO TWEEPY #a
api_key = environ['api_key']
api_secret_key = environ['api_secret_key']
acess_key = environ['acess_key']
acess_secret = environ['acess_secret']
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(acess_key, acess_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def DadosENPE(data_atual):
    URL = f'https://apienpe.herokuapp.com/days/{data_atual}'
    get = requests.get(URL)
    dados = get.json()
    return dados

while True:
    get_data = gmtime()
    dia = get_data[2]
    mes = get_data[1]
    ano = get_data[0]
    hora = get_data[3]
    minuto = get_data[4]
    data_api = f'{dia}-{mes}-{ano}'
    data_formatada = f'{dia}/{mes}/{ano}'

    if hora == hr_postar and minuto == min_postar:
        
        dados = DadosENPE(data_api)
        DiasAula = dados['daulas']
        Ferias = dados['ferias']
        Porcentagem = dados['porcentagem']
        TotalDiasAula = dados['total']
        
        if Ferias > 0: 
            frase = f'Ainda temos {Ferias} dias de férias. O ENPE 2021/1 se inicia em 16 de Agosto de 2021.'
            api.update_status(frase)
            print()
            print(f'Atualizado em {data_formatada}.')
            sleep(60)

        elif Ferias > 0 and DiasAula > 0:
            frase = f'Curtam o recesso! O semestre está {Porcentagem}% completo.'
            api.update_status(frase)
            print(f'Atualizado em {data_formatada}')
            sleep(60)
        
        elif Ferias == 0 and DiasAula == 84:
            frase = f'Tudo que é bom dura pouco :/... Semestre volta com tudo amanhã! Ele ja está {Porcentagem}% completo.'
            api.update_status(frase)
            print(f'Atualizado em {data_formatada}')
            sleep(60)

        elif Ferias == 0 and DiasAula == 0:
            frase = f'As aulas do ENPE 2021/1 começam amanhã! tenham todos um ótimo semestre!'
            api.update_status(frase)
            print(f'Atualizado em {data_formatada}')
            sleep(60)
        
        elif DiasAula > 0:
            frase = f'Já completamos {DiasAula} dias de aula no ENPE 2021/1, completando {Porcentagem}% do total.'
            api.update_status(frase)
            print(f'Atualizado em {data_formatada}')
            sleep(60)
        
        elif DiasAula == TotalDiasAula:
            frase = f'O ENPE 2021/1 está 100% completo.'
            api.update_status(frase)
            print(f'Atualizado em {data_formatada}')
            exit()
    else:
        print('------ Nada a atualizar ------')
        print('Data: {} | Hora: {}:{}'.format(data_formatada, hora-3, minuto))
        print('------  ------  ------ ------')
        sleep(60)
