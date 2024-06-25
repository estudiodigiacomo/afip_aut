import tkinter as tk
from gui.my_voucher_wind import open_my_vouchers_window
from gui.online_voucher_wind import open_online_vouchers_window
from read_sheet_afip import get_clients_from_sheets
from gui.monotributist_wind import monostributist_wind
from gui.autonomous_wind import autnomous_wind
from gui.agropecuary_wind import agropecuary_wind
from gui.ccma_gui import ccma_gui

def main_window():
    selection_window = tk.Tk()
    selection_window.title('Automatizacion de AFIP - Estudio Contable Di Giacomo')
    selection_window.geometry('400x200')

    all_clients = get_clients_from_sheets()
    clients_var = tk.StringVar(selection_window)

    #Filtra la lista de clientes según el tipo de automatización seleccionado
    def update_client_options(*args):
        automation_type = automation_var.get()
        if automation_type == 'Agropecuarios':
            filtered_clients = [client['name'] for client in all_clients if client['proc_agro'] == 'Agropecuarios']
        elif automation_type == 'Monotributo':
            filtered_clients = [client['name'] for client in all_clients if client['proc_monotri'] == 'Monotributo']
        elif automation_type == 'Autonomo':
            filtered_clients = [client['name'] for client in all_clients if client['proc_auto'] == 'Autonomo']
        else:
            filtered_clients = [client['name'] for client in all_clients]
        
        if not filtered_clients:
            filtered_clients = ["No hay clientes disponibles"]
        
        clients_var.set(filtered_clients[0])
        client_menu['menu'].delete(0, 'end')
        for client in filtered_clients:
            client_menu['menu'].add_command(label=client, command=tk._setit(clients_var, client))

    automation_types = ['Mis Comprobantes', 'Comprobantes en Línea', 'Monotributo', 'Autonomo', 'Agropecuarios', 'CCMA']
    automation_var = tk.StringVar(selection_window)
    automation_var.set(automation_types[0])
    tk.Label(selection_window, text='Selecciona el tipo de automatización:').pack()
    #Vincula la función update_client_options a los cambios en automation_var
    automation_var.trace('w', update_client_options)
    tk.OptionMenu(selection_window, automation_var, *automation_types).pack()

    tk.Label(selection_window, text='Selecciona un cliente:').pack()
    client_menu = tk.OptionMenu(selection_window, clients_var, '')
    client_menu.pack()

    def start_automation():
        client_name = clients_var.get()
        automation_type = automation_var.get()
        open_voucher_window(client_name, automation_type)

    tk.Button(selection_window, text='Siguiente', command=start_automation).pack(pady=10)

    update_client_options()
    selection_window.mainloop()

def open_voucher_window(client_name, automation_type):

    if automation_type == 'Mis Comprobantes':
        open_my_vouchers_window(client_name)
    elif automation_type == 'Comprobantes en Línea':
        open_online_vouchers_window(client_name)
    elif automation_type == 'Monotributo':
        monostributist_wind(client_name)
    elif automation_type == 'Autonomo':
        autnomous_wind(client_name)
    elif automation_type == 'Agropecuarios':
        agropecuary_wind(client_name)
    elif automation_type == 'CCMA':
        ccma_gui(client_name)
    else:
        print("Tipo de automatización no reconocido:", automation_type)

if __name__ == "__main__":
    main_window()
