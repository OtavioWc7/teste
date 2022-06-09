import requests, json, schedule, time, os
from email.mime import base
from main import monitoriaZendesk
from dotenv import load_dotenv

load_dotenv()

baseApi = os.getenv('baseApi_slack')
token = os.getenv('TOKEN')

def notificationSlack():
    for results in monitoriaZendesk():
        id = results['id']
        servico = results['Serviço']
        status = results['Status']
        impacto = results['Impacto']
        incidente = results['Incidentes ativos']
        
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
                            "text": f"<@otavio.souza>\nID: `{id}`\n *Serviço:* `{servico}`\n *Status:* `{status}`\n *Impacto:* `{impacto}`\n *Incidente:* `{incidente}`"
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

schedule.every(30).minutes.do(notificationSlack)

while True:
    schedule.run_pending()
    time.sleep(1)