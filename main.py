import requests, json, os
from dotenv import load_dotenv

load_dotenv()

baseApi = os.getenv('baseApi_zendesk')

class Slack:
    def __init__(self, owner_chat, owner_explorer, owner_support):
        self.owner_chat = owner_chat
        self.owner_explorer = owner_explorer
        self.owner_support = owner_support
        
    def monitoriaZendesk(self):
        funcao_setor = ['Explore', 'Chat', 'Support']
        new_values = []
    
        for areas in funcao_setor:
            session = requests.Session()
            endpoint = f"/api/components/{areas}?domain=opsmagalu.zendesk.com"
            url = baseApi + endpoint

            response = session.get(url)
            res = json.loads(response.text)
            
            incidentes_ativos = res['active_incidents']
            # se explorer for diferente de vazio, retorne apenas o explorer, sucessivamente para ambos
            
            # alteração das Words para pt-br
            impacto = res['impact']
            if impacto == "no impact":
                impacto = "Nenhum impacto"
                
            operacional = res['status']
            if operacional == "operational":
                operacional = "Operacional"
            
            sistema = res['name']
            if sistema == "name":
                sistema = "Sistema"
            
            user = []
            # modelo payload 
            payload = {
                    'Proprietário' : user,
                    'id' : res['id'],
                    'Serviço' : res['name'],
                    'Status' : operacional,
                    'Impacto' : impacto,
                    "Incidentes ativos" : incidentes_ativos
                }
            # validação
            try:
                if incidentes_ativos != [] and sistema == "Chat":
                    new_values.append(payload)
                    user.append(self.owner_chat)       
                elif incidentes_ativos != [] and sistema == "Support":
                    new_values.append(payload)
                    user.append(self.owner_support)
                elif incidentes_ativos != [] and sistema == "Explore":
                    new_values.append(payload)
                    user.append(self.owner_explorer)
            except TypeError:
                return TypeError
    
        return new_values

# def importClass():
#     agent_chat = Slack('@otavio.souza')
#     value = agent_chat.monitoriaZendesk()
#     return value

# importClass()
