import tkinter as tk
from primary_in_grains import primary_in_grains
from online_vouchers import online_voucher
from tkcalendar import DateEntry
import babel.numbers

def agropecuary_wind(client_name):
    agropecuary_wind = tk.Tk()
    agropecuary_wind.title('Agropecuarios')
    agropecuary_wind.geometry('400x500')

    selecction = tk.Label(agropecuary_wind, text='Seleccione proceso agropecuario:')
    selecction.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')

    type_options = ['Liquidacion Primaria en granos']

    #Tipo de comprobante
    type_label = tk.Label(agropecuary_wind, text="Tipo:")
    type_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    type_var = tk.StringVar()
    type_var.set(type_options[0])
    type_menu = tk.OptionMenu(agropecuary_wind, type_var, *type_options)
    type_menu.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='w')

    #Fecha desde
    date_from_label = tk.Label(agropecuary_wind, text='Desde: ')
    date_from_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
    date_from_entry = DateEntry(agropecuary_wind, width=12, date_pattern="dd/mm/yyyy")
    date_from_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')
    #Fecha desde
    date_to_label = tk.Label(agropecuary_wind, text="Hasta:")
    date_to_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
    date_to_entry = DateEntry(agropecuary_wind, width=12, date_pattern="dd/mm/yyyy")
    date_to_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')

    #Inicio de automatizacion
    btn_login = tk.Button(agropecuary_wind, text='Iniciar automatizacion', command=lambda: login_and_open_vouchers(client_name, type_var.get(), date_from_entry.get(), date_to_entry.get()))

    btn_login.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='w')
    agropecuary_wind.mainloop()

def login_and_open_vouchers(client_name, type_var, point_sale_var, date_from, date_to, actividad):
    primary_in_grains(client_name, type_var, point_sale_var, date_from, date_to, actividad)