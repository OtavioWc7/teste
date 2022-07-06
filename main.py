import requests, json, os
import numpy as np
from datetime import date, time, datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

baseApi = os.getenv('baseApi_zendesk')

class Slack:
    def __init__(self, owner_chat, owner_explorer, owner_support):
        self.owner_chat = owner_chat
        self.owner_explorer = owner_explorer
        self.owner_support = owner_support
        
    def _monitoriaZendesk(self):
        funcao_setor = ['Explore', 'Chat', 'Support']
        ids = []
        for areas in funcao_setor:
            session = requests.Session()
            endpoint = f"/api/components/{areas}?domain=opsmagalu.zendesk.com"
            url = baseApi + endpoint
            response = session.get(url)
            res = json.loads(response.text)
            for activeIncidents in res['active_incidents']:
                ids.append(
                    {
                        'id service' : res['id'],
                        'name_service' : res['name'],
                        'status_service' : res['status'],
                        'impact_service' : res['impact'],
                        'id' : activeIncidents['id'],
                        'name' : activeIncidents['name'],
                        'status' : activeIncidents['status'],
                        'impacto' : activeIncidents['impact'],
                        'inicou' : activeIncidents['started_at'],
                        'incidentes_active' : res['active_incidents']
                    }
                )
        return ids
    
    def createPayload(self):
        payload = self._monitoriaZendesk()
        new_values = []
        list_array = []
        for values in payload:
            id = values['id']
            nome_servico = values['name_service']
            status_servico = values['status_service']
            impacto_servico = values['impact_service']
            servico_id = values['id service']
            nome = values['name']
            status = values['status']
            impacto = values['impacto']
            inicio = values['inicou']
            incidentes_ativos = values['incidentes_active']
            
        #/________________________________READ TXT____________________________________/
        
            reading = np.loadtxt('id_incidents.txt', dtype=str)
            value = reading.tolist()
            list_array.append(value)
        
        #/______________________________________________________________________________/
            if str(id) == value[-1]:
                print('os valores são iguais', id)
            else:
                #/________________________________CREATE TXT_____________________________________/
                with open('id_incidents.txt', 'a', newline="") as file: # criar o arquivo txt
                    convert_id = str(id)
                    lines = str(convert_id + '\n')
                    file.write(lines)
                    file.close()
                #/______________________________________________________________________________/
                        
            #     # se explorer for diferente de vazio, retorne apenas o explorer, sucessivamente para ambos
            
            #     # alteração das Words para pt-br
                _impacto_ = impacto_servico
                if _impacto_ == "no impact":
                    _impacto_ = "Nenhum impacto"
                    
                operacional = status_servico
                if operacional == "operational":
                    operacional = "Operacional"
                
                sistema = nome_servico
                if sistema == "name":
                    sistema = "Sistema"
                
                format_data = str(inicio)[0:19].replace('T', ' ')
                
                user = []
                # modelo payload 
                payload = {
                        'proprietario' : user,
                        'id' : servico_id,
                        'servico' : nome_servico,
                        'status' : operacional,
                        'impacto_do_servico' : _impacto_,
                        'descricao' : nome,
                        'status_em_andamento' : status,
                        'impacto_em_andamento' : impacto,
                        'inicio' : format_data
                    }
                # validação
                
                try:
                    if operacional == "Operacional" and _impacto_ != "Nenhum impacto":
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