#login_afip
from selenium import webdriver
from read_sheet_afip import get_clients_from_sheets
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tkinter import messagebox

def login_afip(client_name):
    options_nav = Options()
    options_nav.add_argument('--start-maximized')
    options_nav.add_experimental_option('prefs', {
    "download.prompt_for_download": False, 
    "download.default_directory": r"c:\default"
    })
    driver = webdriver.Chrome(options= options_nav)
    #Login
    try:
        # Obtener los datos del cliente desde Google Sheets
        clients = get_clients_from_sheets()
        for client in clients:
            if client['name'] == client_name:
                cuil, password = client['cuil'], client['password']
                try:
                    driver.get('https://auth.afip.gob.ar/contribuyente_/login.xhtml')
                    # Esperar a que los elementos estén presentes
                    cuil_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "F1:username")))
                    # Completar el campo CUIT/CUIL
                    cuil_field.send_keys(cuil)
                    btn_cuil_after = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "F1:btnSiguiente")))
                    btn_cuil_after.click()
                    # Completar el campo contraseña
                    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "F1:password")))
                    password_field.send_keys(password)
                    btn_get_into = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "F1:btnIngresar")))
                    btn_get_into.click()
                    return driver
                except Exception as e:
                    messagebox.showerror("Error de ejecución, inicio de sesion: ", str(e))
    except Exception as e:
        print('Error:', str(e))
    finally:
        return driver
        driver.quit()
