import tkinter as tk
from ccma import ccma
from read_sheet_afip import get_clients_from_sheets

def ccma_gui(client_name):
    
    clients = get_clients_from_sheets()
    for client in clients:
        if client['name'] == client_name:
            cuil = client['cuil']

    ccma(client_name, cuil)