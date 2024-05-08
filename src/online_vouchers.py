from login_afip import login_afip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import os
import zipfile
from datetime import datetime
import sys

def online_voucher(client_name, type_var, point_sale_var, date_from, date_to, actividad):
    try:
        driver = login_afip(client_name)
         #Tipeo comprobantes en linea
        input_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. ID, "buscadorInput")))
        input_search.send_keys('Comprobantes en Línea')
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
        elements_clients = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/form/table/tbody/tr[4]")))
        inputs_clients = elements_clients.find_elements(By.XPATH, ".//input")
        for input_element in inputs_clients:
            values_clients = input_element.get_attribute('value')
            if values_clients == client_name:
                break
        if values_clients == client_name:
            input_element.click()

        #Consultas
        queries_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/table/tbody/tr[2]/td/a/span[2]")))
        queries_btn.click()

        #Fecha desde
        date_from_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/form/div/div/table/tbody/tr[2]/td[1]/input[1]")))
        date_from_input.clear()
        date_from_input.send_keys(date_from)
        #Fecha hasta
        date_to_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/form/div/div/table/tbody/tr[2]/td[2]/input[1]")))
        date_to_input.clear()
        date_to_input.send_keys(date_to)

        #Tipo de comprobante
        if type_var == 'seleccionar...':
            element_select_null = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/form/div/div/table/tbody/tr[4]/td/select/option[1]")))
            element_select_null.click()
        elif type_var != 'seleccionar...':
            dropdown_element_type = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/form/div/div/table/tbody/tr[4]/td/select")))
            dropdown_type = Select(dropdown_element_type)
            # Recorro opciones de dropdown
            options_type = [option.text for option in dropdown_type.options]
            for option in options_type:
                if option == type_var:
                    dropdown_type.select_by_visible_text(option)
                    break
        else:
            print('Error al seleccionar tipo de comprobante')

        #Seleccionar punto de venta
        element_sale_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/form/div/div/table/tbody/tr[5]/td/select')))
        dropdown_sale = Select(element_sale_dropdown)
        options_sale = [opt_sale.text for opt_sale in dropdown_sale.options]
        for opt_sale in options_sale:
            if opt_sale == point_sale_var:
                dropdown_sale.select_by_visible_text(opt_sale)
                break      

        #Buscar comprobantes
        btn_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/table/tbody/tr/td/input[2]')))
        btn_search.click()

        try:
            #Formateo fecha periodo
            period_date = date_from[3:]
            new_period_date = period_date.replace('/', '-')
            name_folder_period = f'Periodo {new_period_date}'

            # Fecha emisión
            date_now = datetime.now().date()
            date_emision = date_now.strftime("%d-%m-%Y")

            #camelCase para identificar las carpetas de cliente
            name_client_may = client_name
            words = name_client_may.split()
            camel_case_words = [word.capitalize() for word in words]
            client_name_camel = ' '.join(camel_case_words)
            #Ingreso nombre del cliente en la ruta
            route_base = r'D:\Clientes\{}\Comprobante en linea'
            route_format = route_base.format(client_name_camel)
            route_completed = os.path.join(route_format, name_folder_period)
            
            #Verifico si ya existe la carpeta de ese periodo, si no existe la creo
            if not name_folder_period in os.listdir(route_format):
                os.makedirs(route_completed)
            
            # Configura la ruta de descarga
            prefs = {
                "download.default_directory": route_completed
            }
            driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': route_completed}}
            driver.execute("send_command", params)
            
            #Captura de pantalla
            screen_name = f'Resumen - Comprobantes en línea - Factura en línea - {new_period_date} - {date_emision}.png'
            screen_path = os.path.join(route_completed, screen_name)
            time.sleep(2)
            driver.save_screenshot(screen_path)

            #Verifico si existen comprobantes
            table_with_data = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/table/tbody/tr[2]')))

            if table_with_data.text.strip():
                rows = driver.find_elements(By.XPATH, '//table[@class="jig_table"]/tbody/tr')
                # Iterar sobre cada fila
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, 'td')
                    for cell in cells:
                        try:
                            #N° de comprobante
                            if cell.get_attribute("title") == "Nro. Comprobante":
                                number_voucher = cell.text
                            #Btn decarga
                            download_button = cell.find_element(By.XPATH, './/input[@value="Ver"]')
                            download_button.click()
                            time.sleep(5)

                            #Obtener una lista de todos los archivos en la carpeta
                            list_of_files = os.listdir(route_completed)
                            # Buscar el archivo más reciente
                            latest_file = None
                            latest_file_time = 0
                            for file_name in list_of_files:
                                file_path = os.path.join(route_completed, file_name)
                                if os.path.isfile(file_path):
                                    file_time = os.path.getctime(file_path)
                                if file_time > latest_file_time:
                                    latest_file_time = file_time
                                    latest_file = file_path
                            #Renombro el archivo
                            name_voucher = f'{client_name} - Factura  N°{number_voucher} - {actividad}'
                            new_file_path = os.path.join(route_completed, f"{name_voucher}.pdf")
                            os.rename(latest_file, new_file_path)
                            print("Archivo descargado y renombrado correctamente.")
                            time.sleep(5)
                            break
                        except NoSuchElementException:
                            continue
                time.sleep(2)
                #Descarga de RESULTADOS_BUSQUEDA.zip
                btn_zip = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/input[3]')))
                btn_zip.click()
                name_zip = r'RESULTADOS_BUSQUEDA.zip'
                file_zip = os.path.join(route_completed, name_zip)
                time.sleep(5)
                with zipfile.ZipFile(file_zip, 'r') as zip_ref:
                    zip_ref.extractall(route_completed)
                    time.sleep(2)

                #Renombrar ventas y alicuotas
                name_buys_new = f'Comprobantes en línea - Factura en línea - Ventas - {client_name} - Período {new_period_date} - {actividad} - Fecha de emisión {date_emision}.txt'
                name_buys_origin = 'VENTAS.txt'
                name_alicuotas_new = f'Comprobantes en línea - Factura en línea - Alicuotas - {client_name} - Período {new_period_date} - {actividad} - Fecha de emisión {date_emision}.txt'
                name_alicuotas_origin = 'ALICUOTAS.txt'
                #Ventas
                path_buy = os.path.join(route_completed, name_buys_origin)
                path_file_buys = os.path.join(route_completed, name_buys_origin)
                #Alicuotas
                path_alicuotas = os.path.join(route_completed, name_alicuotas_origin)
                path_file_alicuotas = os.path.join(route_completed, name_alicuotas_origin)
                try:
                    time.sleep(2)
                    os.rename(path_file_buys, os.path.join(route_completed, name_buys_new))
                    time.sleep(2)
                    os.rename(path_file_alicuotas, os.path.join(route_completed, name_alicuotas_new))
                except Exception as e: 
                    print('Error al renombrar archivo')

            else:
                #Captura de pantalla
                screen_name = f'Resumen - Comprobantes en línea - Factura en línea - {new_period_date} - {date_emision}.png'
                screen_path = os.path.join(route_completed, screen_name)
                time.sleep(2)
                driver.save_screenshot(screen_path)
        except Exception as e:
            print('Error:', str(e))
        time.sleep(15)
    except Exception as e:
        print('Error:', str(e))
    sys.exit()
