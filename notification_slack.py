from ast import Try
from logging import error
import requests, json, schedule, time, os
from email.mime import base
# from main import monitoriaZendesk
from dotenv import load_dotenv
from main import Slack

load_dotenv()

baseApi = os.getenv('baseApi_slack')
token = os.getenv('TOKEN')

print('### EXECUTANDO SCRIPT DE MONITORIA ZENDESK ###')
def notificationSlack():
    print('### CONEXÃO COM SLACK ###')
    agents = Slack(owner_chat='@otavio.souza', owner_explorer='@otavio.souza', owner_support="@pablo.lemos")
    dice_zendesk = agents.createPayload()
    try:
        for results in dice_zendesk:
            proprietario = str(results['proprietario']).replace('[','').replace(']','').replace("'","")
            id = results['id']
            servico = results['servico']
            status = results['status']
            impacto = results['impacto_do_servico']
            descricao = results['descricao']
            status_andamento = results['status_em_andamento']
            impacto_andamento = results['impacto_em_andamento']
            iniciou = results['inicio']
            #conexão
            endpoint = '/services/' + token 
            url = baseApi + endpoint 

            payload = json.dumps(
                {
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"<{proprietario}>\nID: `{id}`\n *Serviço:* `{servico}`\n *Status:* `{status}`\n *Impacto:* `{impacto}`\n *Descrição:* `{descricao}` \n *Status em andamento:* `{status_andamento}` \n *Impacto em andamento:* `{impacto_andamento}` \n *Iniciou às:* `{iniciou}` \n"
                            }
                        }
                    ]
                }
            )
            headers = {
                'Content-type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
    except TypeError:
                return TypeError
    
        
schedule.every(30).minutes.do(notificationSlack)
# schedule.every(1).hour.do(notificationSlack)
while True:
    schedule.run_pending()
    time.sleep(1)
