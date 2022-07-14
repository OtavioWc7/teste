
import requests, json, os, sqlite3, googletrans, time
from googletrans import Translator
import numpy as np
from datetime import date,datetime, timedelta
from dotenv import load_dotenv



load_dotenv()

baseApi = os.getenv('baseApi_zendesk')
db = sqlite3.connect('registros_ids_zendesk.db')

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
        cur = db.cursor()
        payload = self._monitoriaZendesk()
        new_values = []
        
        for values in payload:
            #/________________________________OBJ____________________________________/
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
            #/________________________________OBJ____________________________________/
            
            #/________________________________TRANSLATOR____________________________________/
            translator = Translator()
            #/________________________________TRANSLATOR____________________________________/
            
            #/________________________________TO VALIDATE BD AND CREATE____________________________________/
            
            
            select = "SELECT N_ID FROM id_registros_zendesk WHERE N_ID ='{}'".format(id)
            cur.execute(select)
            result = cur.fetchall()
            if len(result)!=0:
                print('id já registrado no banco', result)
            else:
                data_e_hora_atuais = datetime.now()
                data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')    
                cur.execute(f"INSERT INTO id_registros_zendesk (N_ID, H_REGISTRO) VALUES('{id}', '{data_e_hora_em_texto}')")
                db.commit()
                print('ID não existe, sendo criado no banco', id)
                time.sleep(2)
                
                _impacto_ = translator.translate(impacto_servico, dest='pt')
                _operacional_ = translator.translate(status_servico, dest='pt')
                _descricao_ = translator.translate(nome, dest='pt')
                
                _status_andamento_ = translator.translate(status, dest='pt')
                _impacto_andamento_ = translator.translate(impacto, dest='pt')
                
                
                format_data = str(inicio)[0:19].replace('T', ' ')
                
                user = []
                # modelo payload 
                payload = {
                        'proprietario' : user,
                        'id' : servico_id,
                        'servico' : nome_servico,
                        'status' : _operacional_.text,
                        'impacto_do_servico' : _impacto_.text,
                        'descricao' : _descricao_.text,
                        'status_em_andamento' : _status_andamento_.text,
                        'impacto_em_andamento' : _impacto_andamento_.text,
                        'inicio' : format_data
                    }
                # validação
                
                try:
                    if incidentes_ativos != [] and nome_servico == "Chat":
                        new_values.append(payload)
                        user.append(self.owner_chat)  
                    elif incidentes_ativos != [] and nome_servico == "Support":
                        new_values.append(payload)
                        user.append(self.owner_support)
                    elif incidentes_ativos != [] and nome_servico == "Explore":
                        new_values.append(payload)
                        user.append(self.owner_explorer)
                except TypeError:
                    return TypeError
                # se explorer for diferente de vazio, retorne apenas o explorer, sucessivamente para ambos
            
                # alteração das Words para pt-br
               
                
        return new_values
