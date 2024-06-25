import os
import datetime
from utils.config import folder_clients

def folders_report(client_name_formated):
    #Verifico existencia de las carpetas necesarias
    try:
        date = datetime.datetime.now()
        formatted_folder = date.strftime("%d-%m-%Y")

        folder_client = os.path.join(folder_clients, client_name_formated)
        folder_report = os.path.join(folder_client, 'Reporte')
        folder_date_emision = os.path.join(folder_report, f'Emisión {formatted_folder}')

        if not os.path.exists(folder_clients):
            os.makedirs(folder_clients)
            print(f'Creada la carpeta Clientes en el directorio {folder_clients}')
        if not os.path.exists(folder_client):
            os.makedirs(folder_client)
            print(f'Creada la carpeta {client_name_formated} en el directorio {folder_client}')
        if not os.path.exists(folder_report):
            os.makedirs(folder_report)
            print(f'Creada la carpeta Reporte en el directorio {folder_report}')
        if not os.path.exists(folder_date_emision):
            os.makedirs(folder_date_emision)
            print(f'Creada la carpeta Emision en el directorio {folder_date_emision}')
        return folder_date_emision
    except Exception as e:
        print('Error al verificar o crear carpetas de directorio', str(e))
