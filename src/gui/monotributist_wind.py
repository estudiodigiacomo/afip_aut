import tkinter as tk
from monotributist import monotributist

def monostributist_wind(client_name):
    global monotribustist_window
    monotribustist_window = tk.Tk()
    monotribustist_window.title('Monotributo')
    monotribustist_window.geometry('400x200')

    constancy_list = ['Constancia de CUIT', 'Formulario 184', 'Credencial de pago']
    #Tipo de comprobante
    constancy_label = tk.Label(monotribustist_window, text="Constancias:")
    constancy_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    constancy_var = tk.StringVar()
    constancy_var.set(constancy_list[0])
    constancy_menu = tk.OptionMenu(monotribustist_window, constancy_var, *constancy_list)
    constancy_menu.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='w')

    #Inicio de automatizacion
    btn_login = tk.Button(monotribustist_window, text='Iniciar automatizacion', command=lambda: login_and_open_vouchers(client_name, constancy_var.get()))

    btn_login.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='w')
    monotribustist_window.mainloop()

def login_and_open_vouchers(client_name, constancy):
    monotribustist_window.destroy()
    monotributist(client_name, constancy)