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

def notificationSlack():
    agents = Slack(owner_chat='@otavio.souza', owner_explorer="@vanessa.araujo", owner_support="@pablo.lemos")
    dice_zendesk = agents.monitoriaZendesk()
    try:
        for results in dice_zendesk:
            proprietario = str(results['Proprietário']).replace('[','').replace(']','').replace("'","")
            id = results['id']
            servico = results['Serviço']
            status = results['Status']
            impacto = results['Impacto']
            incidente = results['Incidentes ativos']
            chat_agent = results['Proprietário']
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
                                "text": f"<{proprietario}>\nID: `{id}`\n *Serviço:* `{servico}`\n *Status:* `{status}`\n *Impacto:* `{impacto}`\n *Incidente:* `{incidente}`"
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
    except print(error):
        print
    
        
schedule.every(30).minutes.do(notificationSlack)
# schedule.every(1).hour.do(notificationSlack)
while True:
    schedule.run_pending()
    time.sleep(1)
