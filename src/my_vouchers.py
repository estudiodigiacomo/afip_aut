#Descarga de mis comprobantes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from datetime import datetime
from login_afip import login_afip
import os
import time
import zipfile

def vouchers_download(client_name, type_voucher, date_from, date_to):
    try:
        driver = login_afip(client_name)
        driver.get('https://portalcf.cloud.afip.gob.ar/portal/app/')
        # Tipeo mis comprobantes
        input_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "buscadorInput")))
        input_search.send_keys('Mis Comprobantes')
        # Selección de mis comprobantes
        my_receipts = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "rbt-menu-item-0")))
        my_receipts.click()
        time.sleep(5)
        
        print('FECHA DESDE: ', date_from)
        print('FECHA HASTA: ', date_to)

        # Selección de primera ventana 
        windows_to_select = driver.window_handles
        driver.switch_to.window(windows_to_select[0])
        # Cierre de ventana mis comprobantes
        driver.close()
        # Cambio de foco a la primera ventana
        driver.switch_to.window(windows_to_select[1])

        if type_voucher == 'emitidos':
            download_dir = r"c:\comprobantes-emitidos"
        else:
            download_dir = r"c:\comprobantes-recibidos"

                # Configura la ruta de descarga
        prefs = {
            "download.default_directory": download_dir
        }
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        driver.execute("send_command", params)
        
        #En caso de existir ventana de respesentante entramos al condicional 
        if 'Elegí una persona para ingresar' in driver.page_source:
            #Selectores XPATH
            #Reepresentante
            element_name_represent = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/form/main/div/div/div[2]/div/a/div/div[2]/h2")))
            name_represent = element_name_represent.text.strip()
            #Representados
            representaded_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/form/main/div/div/div[2]/div/div[1]/div/a/div/div[2]/h3")))

            #Si el nombre del seleccionado es igual al nombre del representante ingresar al primer elemento
            if name_represent == client_name:
                element_name_represent.click()

            #Si el nombre del seleccionado es igual a representado ingresar a ese elemento con mismo nombre (empresa)
            else:
                found_represented = False 
                time.sleep(5)
                for representaded_element in representaded_elements:
                    representaded_name = representaded_element.text.split('\n')[0].strip()
                    
                    if representaded_name == client_name:
                        representaded_element.click()
                        found_represented = True
                        break
                if not found_represented:
                    print('No se encontró el representado')
        # Calendario
        if type_voucher == 'emitidos':
            print('emitidos')
            driver.get('https://fes.afip.gob.ar/mcmp/jsp/comprobantesEmitidos.do')
        elif type_voucher == 'recibidos':
            print('recibidos')
            driver.get('https://fes.afip.gob.ar/mcmp/jsp/comprobantesRecibidos.do')
        else:
            print('Error: No se encontro la ruta de mis comprobantes')


        issued = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fechaEmision")))
        issued.click()

        #Fecha desde
        date_select_from = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/div[1]/input")))
        date_select_from.clear()
        date_select_from.send_keys(date_from)
        time.sleep(5)
        #Fecha hasta
        date_select_to = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[1]/input")))
        date_select_to.clear()
        date_select_to.send_keys(date_to)
        time.sleep(5)

        # Buscar comprobantes
        search_proof = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'buscarComprobantes')))
        search_proof.click()
        time.sleep(10)

        # Tomo fecha periodo
        if type_voucher == 'emitidos':
            date_start_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/section/div[1]/div/div[2]/div[2]/div[1]/div[2]/ul/li[1]/b[1]")))

        elif type_voucher == 'recibidos':
            date_start_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div/section/div/div/div[2]/div[3]/div[1]/div[2]/ul/li[1]/b[1]")))
        else:
            print('Error en boton de descarga, tipo de comprobante')

        # Obtener el texto de las etiquetas <b> que contienen las fechas
        date_value_start = date_start_element.text.strip().split(" ")[-1]  

        # Limpiar las fechas para eliminar el día y reemplazar las barras inclinadas
        date_modified_start = date_value_start[date_value_start.find("/") + 1:].replace("/", "-")

        # Fecha emisión
        date_now = datetime.now().date()
        date_emision = date_now.strftime("%d-%m-%Y")

        #Verificar si el comprobante esta vacio
        if 'No existe información para los filtros ingresados' in driver.page_source:
            default_content = "Contenido del archivo predeterminado"
            default_file_path = os.path.join(download_dir, "default_vacio.pdf")
            with open(default_file_path, "w") as file:
                file.write(default_content)
                # Espera para que se complete la descarga
                time.sleep(10)
        else:
            # Descargar pdf
            time.sleep(5)
            download_pdf = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[2]')))
            download_pdf.click()
            time.sleep(5)
            # Obtener una lista de todos los archivos en la carpeta de descargas
            list_of_files = os.listdir(download_dir)
            # Buscar el archivo más reciente
            latest_file = None
            latest_file_time = 0
            for file_name in list_of_files:
                file_path = os.path.join(download_dir, file_name)
                if os.path.isfile(file_path):
                    file_time = os.path.getctime(file_path)
                if file_time > latest_file_time:
                    latest_file_time = file_time
                    latest_file = file_path

            # Verificar si se encontró un archivo más reciente
            if latest_file:
                if type_voucher == 'emitidos':
                    nombre_archivo = f'AFIP - Mis Comprobantes Emitidos - Período {date_modified_start} - {client_name} - Fecha de Emisión {date_emision}'
                elif type_voucher == 'recibidos':
                    nombre_archivo = f'AFIP - Mis Comprobantes Recibidos - Período {date_modified_start} - {client_name} - Fecha de Emisión {date_emision}'
                else:
                    print('Error al designar el nombre del archivo, no se proporciona tipo de comprobante')
                new_file_path = os.path.join(download_dir, f"{nombre_archivo}.pdf")
                # Renombrar el archivo
                os.rename(latest_file, new_file_path)
                print("Archivo descargado y renombrado correctamente.")
            else:
                print("No se encontraron archivos en la carpeta de descargas.")
            # Espera para que se renombre
            time.sleep(10)
            
            # Verificar si se encontró un archivo más reciente
            if type_voucher == 'emitidos':
                download_excel_emi = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/section/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/button[1]')))
                download_excel_emi.click()
            elif type_voucher == 'recibidos':
                download_excel_reci = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/section/div/div/div[2]/div[3]/div[2]/div[1]/div[1]/div/button[1]')))
                download_excel_reci.click()
            else:
                print('Error al presionar boton para decsarga de excel')

            time.sleep(5)
            # Obtener una lista de todos los archivos en la carpeta de descargas
            list_of_files = os.listdir(download_dir)
            # Buscar el archivo más reciente
            latest_file = None
            latest_file_time = 0
            for file_name in list_of_files:
                file_path = os.path.join(download_dir, file_name)
                if os.path.isfile(file_path):
                    file_time = os.path.getctime(file_path)
                if file_time > latest_file_time:
                    latest_file_time = file_time
                    latest_file = file_path

            # Verificar si se encontró un archivo más reciente
            if latest_file:
                if type_voucher == 'emitidos':
                    nombre_archivo = f'AFIP - Mis Comprobantes Emitidos - Período {date_modified_start} - {client_name} - Fecha de Emisión {date_emision}'
                elif type_voucher == 'recibidos':
                    nombre_archivo = f'AFIP - Mis Comprobantes Recibidos - Período {date_modified_start} - {client_name} - Fecha de Emisión {date_emision}'
                else:
                    print('Error al designar el nombre del archivo, no se proporciona tipo de comprobante')
                new_file_path = os.path.join(download_dir, f"{nombre_archivo}.xlsx")
                # Renombrar el archivo
                os.rename(latest_file, new_file_path)
                print("Archivo descargado y renombrado correctamente.")
            else:
                print("No se encontraron archivos en la carpeta de descargas.")
            # Espera para que se renombre
            time.sleep(10)

            # Verificar si se encontró un archivo más reciente
            if type_voucher == 'emitidos':
                download_csv_emi = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/section/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/button[1]')))
                download_csv_emi.click()
            elif type_voucher == 'recibidos':
                download_csv_reci = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/section/div/div/div[2]/div[3]/div[2]/div[1]/div[1]/div/button[1]')))
                download_csv_reci.click()
            else:
                print('Error al presionar boton para decsarga de excel')
            time.sleep(5)
            list_of_files = os.listdir(download_dir)
            # Buscar el archivo ZIP dentro del directorio de descargas
            zip_file_path = None
            for file_name in list_of_files:
                if file_name.endswith('.zip'):
                    zip_file_path = os.path.join(download_dir, file_name)
                    break
            # Verificar si se encontró el archivo ZIP
            if zip_file_path:
                # Extraer el contenido del archivo ZIP
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(download_dir)
                print("Archivo ZIP descomprimido correctamente.")
            else:
                print("No se encontró ningún archivo ZIP en el directorio de descargas.")
            time.sleep(5)
                        # Obtener una lista de todos los archivos en la carpeta de descargas
            list_of_files = os.listdir(download_dir)
            # Buscar el archivo más reciente
            latest_file = None
            latest_file_time = 0
            for file_name in list_of_files:
                file_path = os.path.join(download_dir, file_name)
                if os.path.isfile(file_path):
                    file_time = os.path.getctime(file_path)
                if file_time > latest_file_time:
                    latest_file_time = file_time
                    latest_file = file_path

            # Verificar si se encontró un archivo más reciente
            if latest_file:
                if type_voucher == 'emitidos':
                    nombre_archivo = f'AFIP - Mis Comprobantes Emitidos - Período {date_modified_start} - {client_name} - Fecha de Emisión {date_emision}'
                elif type_voucher == 'recibidos':
                    nombre_archivo = f'AFIP - Mis Comprobantes Recibidos - Período {date_modified_start} - {client_name} - Fecha de Emisión {date_emision}'
                else:
                    print('Error al designar el nombre del archivo, no se proporciona tipo de comprobante')
                new_file_path = os.path.join(download_dir, f"{nombre_archivo}.csv")
                # Renombrar el archivo
                os.rename(latest_file, new_file_path)
                print("Archivo descargado y renombrado correctamente.")
            else:
                print("No se encontraron archivos en la carpeta de descargas.")
           

            
    except Exception as e:
        print('Error al procesar comprobantes:', str(e))
    finally:
        driver.quit()
        os._exit(0)