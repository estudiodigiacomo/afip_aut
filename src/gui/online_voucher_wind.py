import tkinter as tk
from read_sheet_afip import get_clients_from_sheets
from online_vouchers import online_voucher
from tkcalendar import DateEntry

def open_online_vouchers_window(client_name):
    online_vouchers_window = tk.Tk()
    online_vouchers_window.title('Comprobantes en Línea')
    online_vouchers_window.geometry('400x500')

    clients = get_clients_from_sheets()
    for client in clients:
        if client['name'] == client_name:
            pto_venta1, pto_venta2, pto_venta3, pto_venta4, actividad = client['pto_venta1'], client['pto_venta2'], client['pto_venta3'], client['pto_venta4'], client['actividad']

    selection_online = tk.Label(online_vouchers_window, text='Seleccione opciones para descarga de comprobante:')
    selection_online.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')

    type_options = ['seleccionar...', '  Factura A', '  Nota de Débito A', '  Nota de Crédito A', '  Recibo A', '  Factura B', '  Nota de Débito B', '  Nota de Crédito B', '  Recibo B', '  Factura C', '  Nota de Débito C', '  Nota de Crédito C', '  Recibo C', '  Factura de Exportación E', '  Nota de Débito por Operaciones con el Exterior E', '  Nota de Crédito por Operaciones con el Exterior E', '  Comprobante de Compra de Bienes Usados', '  Factura M', '  Nota de Débito M', '  Nota de Crédito M', '  Recibo M', '  Factura T', '  Nota de Débito T', '  Nota de Crédito T', '  Factura de Crédito Electrónica MiPyMEs (FCE) A', '  Nota de Débito Electrónica MiPyMEs (FCE) A', '  Nota de Crédito Electrónica MiPyMEs (FCE) A', '  Factura de Crédito Electrónica MiPyMEs (FCE) B', '  Nota de Débito Electrónica MiPyMEs (FCE) B', '  Nota de Crédito Electrónica MiPyMEs (FCE) B', '  Factura de Crédito Electrónica MiPyMEs (FCE) C', '  Nota de Débito Electrónica MiPyMEs (FCE) C', '  Nota de Crédito Electrónica MiPyMEs (FCE) C']

    #Tipo de comprobante
    type_label = tk.Label(online_vouchers_window, text="Tipo:")
    type_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    type_var = tk.StringVar()
    type_var.set(type_options[0])
    type_menu = tk.OptionMenu(online_vouchers_window, type_var, *type_options)
    type_menu.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='w')

    points_of_sale = ['seleccionar...', pto_venta1, pto_venta2, pto_venta3, pto_venta4]

    #Punto de venta
    point_sale_label = tk.Label(online_vouchers_window, text="Punto de Venta:")
    point_sale_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
    point_sale_var = tk.StringVar()
    point_sale_var.set(points_of_sale[0])
    sale_option_menu = tk.OptionMenu(online_vouchers_window, point_sale_var, *points_of_sale)
    sale_option_menu.grid(row=3, column=1, padx=5, pady=5, sticky='w')

    #Fecha desde
    date_from_label = tk.Label(online_vouchers_window, text='Desde: ')
    date_from_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
    date_from_entry = DateEntry(online_vouchers_window, width=12, date_pattern="dd/mm/yyyy")
    date_from_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')
    #Fecha desde
    date_to_label = tk.Label(online_vouchers_window, text="Hasta:")
    date_to_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
    date_to_entry = DateEntry(online_vouchers_window, width=12, date_pattern="dd/mm/yyyy")
    date_to_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')

    #Inicio de automatizacion
    btn_login = tk.Button(online_vouchers_window, text='Iniciar automatizacion', command=lambda: login_and_open_vouchers(client_name, type_var.get(), point_sale_var.get(), date_from_entry.get(), date_to_entry.get(), actividad))

    btn_login.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='w')
    online_vouchers_window.mainloop()

def login_and_open_vouchers(client_name, type_var, point_sale_var, date_from, date_to, actividad):
    online_voucher(client_name, type_var, point_sale_var, date_from, date_to, actividad)