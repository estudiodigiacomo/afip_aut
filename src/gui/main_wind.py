import tkinter as tk
from gui.my_voucher_wind import open_my_vouchers_window
from gui.online_voucher_wind import open_online_vouchers_window
from read_sheet_afip import get_clients_from_sheets
from gui.monotributist_wind import monostributist_wind
from gui.autonomous_wind import autnomous_wind
from gui.agropecuary_wind import primary_in_grains

def main_window():
    global selection_window
    selection_window = tk.Tk()
    selection_window.title('Automatizacion de AFIP - Estudio Contable Di Giacomo')
    selection_window.geometry('400x200')

    clients = [client['name'] for client in get_clients_from_sheets()]
    automation_types = ['Mis Comprobantes', 'Comprobantes en Línea', 'Monotributo', 'Autonomo', 'Agropecuarios']

    client_var = tk.StringVar(selection_window)
    client_var.set(clients[0])
    tk.Label(selection_window, text='Selecciona un cliente:').pack()
    tk.OptionMenu(selection_window, client_var, *clients).pack()

    automation_var = tk.StringVar(selection_window)
    automation_var.set(automation_types[0])
    tk.Label(selection_window, text='Selecciona el tipo de automatización:').pack()
    tk.OptionMenu(selection_window, automation_var, *automation_types).pack()

    def start_automation():
        client_name = client_var.get()
        automation_type = automation_var.get()
        open_voucher_window(client_name, automation_type)

    tk.Button(selection_window, text='Siguiente', command=start_automation).pack(pady= 10)

    selection_window.mainloop()

def open_voucher_window(client_name, automation_type):
    selection_window.destroy() 

    if automation_type == 'Mis Comprobantes':
        open_my_vouchers_window(client_name)
    elif automation_type == 'Comprobantes en Línea':
        open_online_vouchers_window(client_name)
    elif automation_type == 'Monotributo':
        monostributist_wind(client_name)
    elif automation_type == 'Autonomo':
        autnomous_wind(client_name)
    elif automation_type == 'Agropecuarios':
        primary_in_grains(client_name)
    else:
        print("Tipo de automatización no reconocido:", automation_type)
