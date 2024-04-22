import tkinter as tk
from login_afip import login_afip
from vouchers import vouchers_download
from nav_preferences import setup_nav_preferences

def open_my_vouchers_window(client_name):
    my_vouchers_window = tk.Tk()
    my_vouchers_window.title('Mis Comprobantes')
    my_vouchers_window.geometry('400x200')

    # Seleccion tipo de comprobante
    voucher = tk.StringVar(value='emitidos')

    selection_type = tk.Label(my_vouchers_window, text='Seleccione que tipo de comprobante desea descargar:')
    selection_type.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')

    # Radiobuttons
    issued_radiobutton = tk.Radiobutton(my_vouchers_window, text='Combrobantes Emitidos', variable=voucher, value='emitidos')
    issued_radiobutton.grid(row=2, column=0, padx=5, pady=5, sticky='w')

    received_radiobutton = tk.Radiobutton(my_vouchers_window, text='Comprobantes Recibidos', variable=voucher, value='recibidos')
    received_radiobutton.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    btn_login = tk.Button(my_vouchers_window, text='Iniciar automatizacion', command=lambda: login_and_open_vouchers(client_name, voucher.get()))
    btn_login.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='w')

    my_vouchers_window.mainloop()
    return client_name, voucher

def login_and_open_vouchers(client_name, type_voucher):
    setup_nav_preferences(type_voucher)
    login_afip(client_name)
    vouchers_download(client_name, type_voucher)
    