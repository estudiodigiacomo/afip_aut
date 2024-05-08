from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from login_afip import login_afip
from datetime import datetime
from pdfkit import from_url
import pdfkit
import os
import time 
import shutil


def monotributist(client_name, constancy):

    try:
        driver = login_afip(client_name)
        driver.get('https://portalcf.cloud.afip.gob.ar/portal/app/')

        download_dir = r'c:\default' 

        # Configura la ruta de descarga
        prefs = {
            "download.prompt_for_download": False,
            "download.default_directory": download_dir,
        }
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        driver.execute("send_command", params)

        #Tipeo monotributo
        input_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "buscadorInput")))
        input_search.send_keys('monotributo')
        time.sleep(5)
        #Selección de monotributo
        monotribut_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/section/div/div/div[2]/div/div/div[1]/div/div/ul/li[1]/a/div/div/div[1]/div/p")))
        monotribut_element.click()

        #Cambio de iframe (ventana)
        time.sleep(5)
        window_to_select = driver.window_handles
        driver.switch_to.window(window_to_select[0])
        driver.close()
        driver.switch_to.window(window_to_select[1])

        #Sesion contancia
        section_constancy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/form/main/section/div/div/aside/nav/ul/div[1]/li[4]/a')))
        section_constancy.click()

        if constancy != 'Credencial de pago':
            constancy_cuit(driver, client_name, constancy)
        elif constancy == 'Credencial de pago':
            credentials_pay(driver, client_name)
        else:
            print('Error al llamar la funcion constancy')
        time.sleep(10)

    except Exception as e:
        print('Error al procesar constancias:', str(e))
    finally:
        driver.quit()
        os._exit(0)


def constancy_cuit(driver, client_name, constancy):

    if constancy == 'Constancia de CUIT':
        #Voy a la pagina a imprimir
        click_constancy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/form/main/section/div/div/div/div[1]/div/div/div[3]/button')))
        click_constancy.click()
        time.sleep(5)
        windows_to_select = driver.window_handles
        driver.switch_to.window(windows_to_select[-1])
        time.sleep(10)

        # URL de la página web que contiene la tabla
        url_pagina_web = driver.current_url
        time.sleep(3)
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        # Obtener cookies de la sesión
        cookies = driver.get_cookies()

        # Generar archivo de cookies
        with open('cookies.txt', 'w') as f:
            for cookie in cookies:
                f.write(f"{cookie['name']}={cookie['value']};\n")

        # Configuración de pdfkit
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

        # Generar PDF con la opción --cookie-file
        from_url(url_pagina_web, 'resultado.pdf', configuration=config, options={'cookie-file': 'cookies.txt'})

    elif constancy == 'Formulario 184':
        click_form = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/form/main/section/div/div/div/div[2]/div/div/div[3]/a')))
        click_form.click()
    else:
            print('No se selecciono constancia ')

    # Fecha emisión
    date_now = datetime.now().date()
    date_emision = date_now.strftime("%d-%m-%Y")
    name_folder_emision = f'Emisión {date_emision}'

    #camelCase para identificar las carpetas de cliente
    name_client_may = client_name
    words = name_client_may.split()
    camel_case_words = [word.capitalize() for word in words]
    client_name_camel = ' '.join(camel_case_words)
    #Ingreso nombre del cliente en la ruta
    route_base = r'D:\Clientes\{}\Reporte'
    route_format = route_base.format(client_name_camel)
    route_completed = os.path.join(route_format, name_folder_emision)

    #Verifico si ya existe la carpeta de ese periodo, si no existe la creo
    if not name_folder_emision in os.listdir(route_format):
        os.makedirs(route_completed)
    time.sleep(10)
    # Ruta del archivo descargado
    if constancy == 'Constancia de CUIT':
        download_default = r'c:\default\Formulario de Impresión de Constancia de Monotributo.pdf'
    elif constancy == 'Formulario 184':
        download_default = r'c:\default\AFIP _ Formulario 184.pdf'
    else:
        print('Error en download_route ')
    # Ruta del directorio de destino
    shutil.move(download_default, route_completed)
    # Verificar que el archivo se haya movido correctamente
    ruta_destino = os.path.join(download_default, os.path.basename(route_completed))
    if os.path.exists(ruta_destino):
        print("El archivo se movió correctamente")

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
    if constancy == 'Constancia de CUIT':
        name_voucher = f'Constancia de inscripción - Monotributistas - AFIP - {client_name} - {name_folder_emision}'
    elif constancy == 'Formulario 184':
        name_voucher = f'Formulario N°184 - Monotributistas - AFIP - {client_name} - {name_folder_emision}'
    else:
        print('No se selecciono constancia ')
    
    new_file_path = os.path.join(route_completed, f"{name_voucher}.pdf")
    os.rename(latest_file, new_file_path)
    print("Archivo descargado y renombrado correctamente.")
    time.sleep(5)


def credentials_pay(driver, client_name):
    try:
        click_constancy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/main/section/div/div/div/div[3]/div/div/div[3]/a')))
        click_constancy.click()

        # Esperar un momento para que se complete la descarga
        time.sleep(10)

        # Obtener la ruta de descarga predeterminada
        download_default = r'c:\default'  # Ruta de descarga predeterminada en este caso

        # Configurar la ruta de destino
        date_now = datetime.now().date()
        date_emision = date_now.strftime("%d-%m-%Y")
        name_folder_emision = f'Emisión {date_emision}'

        # CamelCase para identificar las carpetas de cliente
        name_client_may = client_name
        words = name_client_may.split()
        camel_case_words = [word.capitalize() for word in words]
        client_name_camel = ' '.join(camel_case_words)

        # Ingresar el nombre del cliente en la ruta
        route_base = r'D:\Clientes\{}\Reporte'
        route_format = route_base.format(client_name_camel)
        route_completed = os.path.join(route_format, name_folder_emision)

        # Obtener la lista de archivos en el directorio de descarga
        files_in_download = os.listdir(download_default)

        # Encontrar el archivo más reciente basado en su fecha de creación
        latest_file = max(files_in_download, key=lambda f: os.path.getctime(os.path.join(download_default, f)))

        # Mover el archivo más reciente al directorio de destino
        shutil.move(os.path.join(download_default, latest_file), route_completed)

        # Verificar que el archivo se haya movido correctamente
        ruta_destino = os.path.join(route_completed, latest_file)

        name_file = f'Credencial de pago - AFIP - {client_name} - {name_folder_emision}.pdf'

        new_file_path = os.path.join(route_completed, name_file)
        os.rename(os.path.join(route_completed, latest_file), new_file_path)

        if os.path.exists(ruta_destino):
            print("El archivo se movió correctamente")

    except Exception as e:
        print('Error al procesar monotributo:', str(e))


