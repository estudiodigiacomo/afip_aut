from login_afip import login_afip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from utils.folders_grain import folders_grain
import time
from datetime import datetime
import sys
import os
import shutil

def primary_in_grains(client_name, date_from, date_to):
    try:
        driver = login_afip(client_name)
        route_base = r"c:\default"
         #Tipeo comprobantes en linea
        input_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. ID, "buscadorInput")))
        input_search.send_keys('Liquidación primaria de granos')
        #Selecciono comprobantes en linea
        online_vouchers = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/section/div/div/div[2]/div/div/div[1]/div/div/ul/li/a/div/div/div[1]/div/p")))
        online_vouchers.click()

        #Cambio de iframe (ventana)
        time.sleep(5)
        window_to_select = driver.window_handles
        driver.switch_to.window(window_to_select[0])
        driver.close()
        driver.switch_to.window(window_to_select[1])

        #Busqueda y click de cliente
        elements_clients = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/center/div[1]/table[2]/tbody/tr/td/table[2]/tbody/tr[2]/td/div/form/table/tbody/tr[3]")))
        inputs_clients = elements_clients.find_elements(By.XPATH, ".//input")
        for input_element in inputs_clients:
            values_clients = input_element.get_attribute('value')
            if values_clients == client_name:
                break
        if values_clients == client_name:
            input_element.click()

        btn_primary_in_grains = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/center/div[2]/table/tbody/tr[2]/td/div[2]/div/form[2]/table/tbody/tr[2]/td/input')))
        btn_primary_in_grains.click()

        btn_received = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/center/div[2]/table/tbody/tr[2]/td/div[2]/div/form[2]/table/tbody/tr[4]/td/input')))
        btn_received.click()

        #Fecha desde
        date_from_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/center/div[2]/table/tbody/tr[2]/td/div[2]/div/form[2]/table[1]/tbody/tr[3]/td[1]/input[1]")))
        date_from_input.clear()
        date_from_input.send_keys(date_from)
        #Fecha hasta
        date_to_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/center/div[2]/table/tbody/tr[2]/td/div[2]/div/form[2]/table[1]/tbody/tr[3]/td[2]/input[1]")))
        date_to_input.clear()
        date_to_input.send_keys(date_to)

        btn_consult = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/center/div[2]/table/tbody/tr[2]/td/div[2]/div/form[2]/table[1]/tbody/tr[3]/td[6]/input')))
        btn_consult.click()

        #Formateo fecha periodo
        period_date = date_from[3:]
        new_period_date = period_date.replace('/', '-')
        name_folder_period = f'Periodo {new_period_date}'
        #Formateo nombre de cliente a capitalize
        client_name_formated = client_name.title() 
        time.sleep(3)
        folder_period = folders_grain(client_name_formated, name_folder_period)
         #Llamo a funcion que verifica y crea carpetas
        folders_grain(client_name_formated, name_folder_period)
        print(folder_period)
        try:
            # Fecha emisión
            date_now = datetime.now().date()
            date_emision = date_now.strftime("%d-%m-%Y")

            # Verifico si existen comprobantes
            table_with_data = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabla4"]')))

            # Si existen datos descargo pdfs
            if table_with_data.text.strip():
                rows = table_with_data.find_elements(By.XPATH, './/tbody/tr')
                # Iterar sobre cada fila
                for row in rows:
                    try:
                        # Leer número de COE para nombre del archivo (segunda columna)
                        cells = row.find_elements(By.TAG_NAME, 'td')
                        if len(cells) > 1:
                            coe_number = cells[1].text
                            print(coe_number)

                        # Btn descarga (última columna)
                        download_button = row.find_element(By.XPATH, './/img[@alt="Ver Liquidación"]')
                        download_button.click()
                        time.sleep(5)
                        # Obtener una lista de todos los archivos en la carpeta
                        list_of_files = os.listdir(route_base)
                        # Buscar el archivo más reciente
                        latest_file = None
                        latest_file_time = 0
                        for file_name in list_of_files:
                            file_path = os.path.join(route_base, file_name)
                            if os.path.isfile(file_path):
                                file_time = os.path.getctime(file_path)
                            if file_time > latest_file_time:
                                latest_file_time = file_time
                                latest_file = file_path
                        # Verificar que se encontró un archivo, mover y renombrar
                        if latest_file is not None:
                            destination_file = os.path.join(folder_period, os.path.basename(latest_file))
                            shutil.move(latest_file, destination_file)
                            # Renombrar el archivo movido
                            name_file_pdf = f'AFIP - Liquidaciones Primarias de Granos - Consulta Liquidaciones Recibidas - COE N {coe_number} - {new_period_date} - {client_name_formated} - Fecha de Emisión {date_emision}'
                            new_file_path = os.path.join(folder_period, f"{name_file_pdf}.pdf")
                            os.rename(destination_file, new_file_path)
                            print("Archivo descargado, movido y renombrado correctamente.")
                        else:
                            print("No se encontró ningún archivo para renombrar.")
                        time.sleep(5)
                    except NoSuchElementException:
                        continue
                time.sleep(2)
            else:
                print('No hay datos para imprimir')     

            #Descargo resumen como pdf
            try:
                # Inyectar CSS para ocultar elementos que no deben imprimirse
                css_to_hide_elements = """
                var style = document.createElement('style');
                style.id = 'hide-elements-style';
                style.innerHTML = `
                    #encabezado, 
                    #tabla3,
                    .botonVolverMenuPrincipal bordesRedondos textoGris sombraBlanca highlight {
                        display: none !important;
                    }
                `;
                document.head.appendChild(style);
                """
                driver.execute_script(css_to_hide_elements)
                time.sleep(5)
                driver.execute_script('window.print();')
                time.sleep(5)
                # Eliminar el estilo inyectado
                remove_css_to_hide_elements = """
                var styleElement = document.getElementById('hide-elements-style');
                if (styleElement) {
                    styleElement.parentNode.removeChild(styleElement);
                }
                """
                driver.execute_script(remove_css_to_hide_elements)
                #Nombre del resumen pdf
                resume_name = f'AFIP - Liquidaciones Primarias de Granos - Consulta Liquidaciones Recibidas - Resumen - Período {new_period_date} - {client_name} - Fecha de Emisión {date_emision}.pdf'
                time.sleep(5)
                #Busco archivos en el directorio
                list_of_files = os.listdir(route_base)
                find_file = max(list_of_files, key=lambda f: os.path.getctime(os.path.join(route_base, f)))
                # Mover el archivo más reciente al directorio de destino
                shutil.move(os.path.join(route_base, find_file), folder_period)
                # Verificar que el archivo se haya movido correctamente
                rute_destiny = os.path.join(folder_period, find_file)
                new_file_path = os.path.join(folder_period, resume_name)
                os.rename(rute_destiny, new_file_path)
                if os.path.exists(new_file_path):
                    print("El archivo de resumen se movió correctamente")
            except Exception as e:
                print('Error al descargar resumen', {str(e)})           

        except Exception as e:
            print('Error:', str(e))
        
    except Exception as e:
        print('Error:', str(e))

