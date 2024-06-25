from login_afip import login_afip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.folder_report import folders_report
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import sys
import os
import shutil

def ccma(client_name, cuil):
    try:
        driver = login_afip(client_name)
        route_base = r"c:\default"
         #Tipeo comprobantes en linea
        input_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. ID, "buscadorInput")))
        input_search.send_keys('CCMA - CUENTA CORRIENTE DE CONTRIBUYENTES MONOTRIBUTISTAS Y AUTONOMOS')
        #Selecciono comprobantes en linea
        online_vouchers = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/section/div/div/div[2]/div/div/div[1]/div/div/ul/li/a/div/div/div[1]/div/p")))
        online_vouchers.click()

        #Cambio de iframe (ventana)
        time.sleep(5)
        window_to_select = driver.window_handles
        driver.switch_to.window(window_to_select[0])
        driver.close()
        driver.switch_to.window(window_to_select[1])

        # Si encuentra elemento para seleccionar CUIT lo procesa
        try:
            element_cuit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div[1]/b/font")))
            
            select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "selectCuit")))
            options = select_element.find_elements(By.TAG_NAME, "option")
            
            cuil_found = False
            for option in options:
                if option.get_attribute("value") == cuil:
                    cuil_found = True
                    option.click()
                    break

            select_cuit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div[2]/form/div[2]/input')))
            select_cuit.click()

            if not cuil_found:
                print(f"CUIL {cuil} no encontrado en las opciones.")

        except TimeoutException:
            print("Elemento no encontrado, continuar con la otra lógica.")

        btn_consult = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/form/table/tbody/tr[4]/td/div/input[3]')))
        btn_consult.click()

        debit_balance = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/table[2]/tbody/tr[2]/td[2]/form/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td[1]')))
        debit_balance_text = debit_balance.text

        print(debit_balance_text)

        #Formateo nombre de cliente a capitalize
        client_name_formated = client_name.title()
        #Ruta de al directorio de descarga 
        folder_date_emision = folders_report(client_name_formated)

        file_path = os.path.join(folder_date_emision, f"Saldo deudor - {client_name} - Cuenta Corriente para Contribuyentes Autonomos - Monotributistas.txt")
        with open(file_path, "w") as file_create:
            file_create.write(debit_balance_text)
        
        driver.execute_script('window.print();')
        time.sleep(5)

        #Busco archivos en el directorio
        list_of_files = os.listdir(route_base)
        find_file = max(list_of_files, key=lambda f: os.path.getctime(os.path.join(route_base, f)))
        # Mover el archivo más reciente al directorio de destino
        shutil.move(os.path.join(route_base, find_file), folder_date_emision)
        # Verificar que el archivo se haya movido correctamente
        name_file_pdf = f'CCMA - {client_name} - Cuenta Corriente para Contribuyentes Autonomos - Monotributistas.pdf'
        rute_destiny = os.path.join(folder_date_emision, find_file)
        new_file_path = os.path.join(folder_date_emision, name_file_pdf)
        os.rename(rute_destiny, new_file_path)
        if os.path.exists(new_file_path):
            print("El archivo de ccma se movió correctamente")

    except Exception as e:
        print('Error:', str(e))

