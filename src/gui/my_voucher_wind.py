import tkinter as tk
from my_vouchers import vouchers_download
from tkcalendar import DateEntry
import babel.numbers

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

    #Fecha desde
    date_from_label = tk.Label(my_vouchers_window, text='Desde: ')
    date_from_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
    date_from_entry = DateEntry(my_vouchers_window, width=12, date_pattern="dd/mm/yyyy")
    date_from_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')
    #Fecha desde
    date_to_label = tk.Label(my_vouchers_window, text="Hasta:")
    date_to_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
    date_to_entry = DateEntry(my_vouchers_window, width=12, date_pattern="dd/mm/yyyy")
    date_to_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')

    btn_login = tk.Button(my_vouchers_window, text='Iniciar automatizacion', command=lambda: login_and_open_vouchers(client_name, voucher.get(), date_from_entry.get(), date_to_entry.get()))
    btn_login.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='w')

    my_vouchers_window.mainloop()
    return client_name, voucher

def login_and_open_vouchers(client_name, type_voucher, date_from, date_to):
    vouchers_download(client_name, type_voucher, date_from, date_to)
    