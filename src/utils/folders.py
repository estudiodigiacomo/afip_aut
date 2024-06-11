import os
import datetime

def folders(client_name_formated, name_folder_period):
    #Verifico existencia de las carpetas necesarias
    try:
        date = datetime.datetime.now()
        formatted_folder = date.strftime("%d-%m-%Y %H.%M.%S")

        folder_clients = r'D:\Clientes'
        folder_client = os.path.join(folder_clients, client_name_formated)
        folder_primary_in_grains = os.path.join(folder_client, 'Liquidaciones Primarias de Grano')
        folder_consult_received = os.path.join(folder_primary_in_grains, 'Consulta Liquidaciones Recibidas')
        folder_period = os.path.join(folder_consult_received, name_folder_period)

        if not os.path.exists(folder_clients):
            os.makedirs(folder_clients)
            print(f'Creada la carpeta Clientes en el directorio {folder_clients}')
        if not os.path.exists(folder_client):
            os.makedirs(folder_client)
            print(f'Creada la carpeta {client_name_formated} en el directorio {folder_client}')
        if not os.path.exists(folder_primary_in_grains):
            os.makedirs(folder_primary_in_grains)
            print(f'Creada la carpeta Liquidaciones Primarias de Grano en el directorio {folder_primary_in_grains}')
        if not os.path.exists(folder_consult_received):
            os.makedirs(folder_consult_received)
            print(f'Creada la carpeta Consulta Liquidaciones Recibidas en el directorio {folder_consult_received}')
        if not os.path.exists(folder_period):
            os.makedirs(folder_period)
            print(f'Creada la carpeta {name_folder_period} en el directorio {folder_period}')
        return folder_period
    except Exception as e:
        print('Error al verificar o crear carpetas de directorio', str(e))
