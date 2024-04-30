#Descarga de mis comprobantes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from datetime import datetime
from login_afip import login_afip
import os
import time

def vouchers_download(client_name, type_voucher):
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

        # Selección de primera ventana 
        windows_to_select = driver.window_handles
        driver.switch_to.window(windows_to_select[0])
        # Cierre de ventana mis comprobantes
        driver.close()
        # Cambio de foco a la primera ventana
        driver.switch_to.window(windows_to_select[1])
        
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

        # Mes pasado
        last_month = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/ul/li[7]")))
        last_month.click()

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

        if type_voucher == 'emitidos':
            download_dir = r"c:\comprobantes-emitidos"
        else:
            download_dir = r"c:\comprobantes-recibidos"

        #Verificar si el comprobante esta vacio
        if 'No existe información para los filtros ingresados' in driver.page_source:
            default_content = "Contenido del archivo predeterminado"
            default_file_path = os.path.join(download_dir, "default_vacio.txt")
            with open(default_file_path, "w") as file:
                file.write(default_content)
                # Espera para que se complete la descarga
                time.sleep(10)

        else:
            # Descargar pdf
            time.sleep(10)
            download_pdf = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tablaDataTables_wrapper"]/div[1]/div[1]/div/button[2]')))
            
            download_pdf.click()
            # Espera para que se complete la descarga
            time.sleep(10)

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

    except Exception as e:
        print('Error al procesar comprobantes:', str(e))
    finally:
        driver.quit()
        os._exit(0)