import sqlite3


banco = sqlite3.connect('registros_ids_zendesk.db')

cur = banco.cursor()


cur.execute("CREATE TABLE id_registros_zendesk(ID INTEGER PRIMARY KEY AUTOINCREMENT,N_ID TEXT NOT NULL, H_REGISTRO TEXT)")


banco.commit()