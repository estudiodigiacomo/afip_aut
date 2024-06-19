import os
import datetime
from utils.config import folder_clients

def folders_cattle_issue(client_name_formated, name_folder_period):
    #Verifico existencia de las carpetas necesarias
    try:
        date = datetime.datetime.now()
        formatted_folder = date.strftime("%d-%m-%Y %H.%M.%S")

        folder_client = os.path.join(folder_clients, client_name_formated)
        folder_cattle = os.path.join(folder_client, 'Hacienda y Carnes')
        folder_consult_received = os.path.join(folder_cattle, 'Consulta y Ajuste De Liquidaciones por Emisor')
        folder_period = os.path.join(folder_consult_received, name_folder_period)

        if not os.path.exists(folder_clients):
            os.makedirs(folder_clients)
            print(f'Creada la carpeta Clientes en el directorio {folder_clients}')
        if not os.path.exists(folder_client):
            os.makedirs(folder_client)
            print(f'Creada la carpeta {client_name_formated} en el directorio {folder_client}')
        if not os.path.exists(folder_cattle):
            os.makedirs(folder_cattle)
            print(f'Creada la carpeta Hacienda y Carnes en el directorio {folder_cattle}')
        if not os.path.exists(folder_consult_received):
            os.makedirs(folder_consult_received)
            print(f'Creada la carpeta Consulta y Ajuste De Liquidaciones por Emisor en el directorio {folder_consult_received}')
        if not os.path.exists(folder_period):
            os.makedirs(folder_period)
            print(f'Creada la carpeta {name_folder_period} en el directorio {folder_period}')
        return folder_period
    except Exception as e:
        print('Error al verificar o crear carpetas de directorio', str(e))


def folders_cattle_receiver(client_name_formated, name_folder_period):
    #Verifico existencia de las carpetas necesarias
    try:
        date = datetime.datetime.now()
        formatted_folder = date.strftime("%d-%m-%Y %H.%M.%S")

        folder_clients = r'd:\Clientes'
        folder_client = os.path.join(folder_clients, client_name_formated)
        folder_cattle = os.path.join(folder_client, 'Hacienda y Carnes')
        folder_consult_received = os.path.join(folder_cattle, 'Consulta y Ajuste De Liquidaciones por Receptor')
        folder_period = os.path.join(folder_consult_received, name_folder_period)

        if not os.path.exists(folder_clients):
            os.makedirs(folder_clients)
            print(f'Creada la carpeta Clientes en el directorio {folder_clients}')
        if not os.path.exists(folder_client):
            os.makedirs(folder_client)
            print(f'Creada la carpeta {client_name_formated} en el directorio {folder_client}')
        if not os.path.exists(folder_cattle):
            os.makedirs(folder_cattle)
            print(f'Creada la carpeta Hacienda y Carnes en el directorio {folder_cattle}')
        if not os.path.exists(folder_consult_received):
            os.makedirs(folder_consult_received)
            print(f'Creada la carpeta Consulta Y Ajuste De Liquidaciones por Receptor en el directorio {folder_consult_received}')
        if not os.path.exists(folder_period):
            os.makedirs(folder_period)
            print(f'Creada la carpeta {name_folder_period} en el directorio {folder_period}')
        return folder_period
    except Exception as e:
        print('Error al verificar o crear carpetas de directorio', str(e))
