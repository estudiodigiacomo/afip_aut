import tkinter as tk
from my_vouchers import vouchers_download
from tkcalendar import DateEntry
import babel.numbers

def open_my_vouchers_window(client_name):
    global my_vouchers_window
    my_vouchers_window = tk.Tk()
    my_vouchers_window.title('Mis Comprobantes')
    my_vouchers_window.geometry('400x200')

    vouchers_list = ['Comprobantes Emitidos', 'Comprobantes Recibidos']
    #Tipo de comprobante
    voucher_label = tk.Label(my_vouchers_window, text="Tipo de comprobante:")
    voucher_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    voucher_var = tk.StringVar()
    voucher_var.set(vouchers_list[0])
    voucher_menu = tk.OptionMenu(my_vouchers_window, voucher_var, *vouchers_list)
    voucher_menu.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='w')

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

    btn_login = tk.Button(my_vouchers_window, text='Iniciar automatizacion', command=lambda: login_and_open_vouchers(client_name, voucher_var.get(), date_from_entry.get(), date_to_entry.get()))
    btn_login.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='w')

    my_vouchers_window.mainloop()
    return client_name, voucher_var

def login_and_open_vouchers(client_name, type_voucher, date_from, date_to):
    my_vouchers_window.destroy()
    vouchers_download(client_name, type_voucher, date_from, date_to)
    