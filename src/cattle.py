from login_afip import login_afip
from utils.folders_cattle import folders_cattle_issue
from utils.folders_cattle import folders_cattle_receiver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import os
import shutil
from datetime import datetime
import sys

#Ingreso hasta pagina de hacienda
def cattle(client_name, date_from, date_to):
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

        time.sleep(5)
        #Hacienda y Carnes
        cattle_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/table/tbody/tr[8]/td/a/span[2]")))
        cattle_btn.click()

        #Abrir ventana de hacienda (error de afip) a la primera falla, cierro y abro nuevamente
        time.sleep(5)
        window_to_select = driver.window_handles
        driver.switch_to.window(window_to_select[1])
        driver.close()
        driver.switch_to.window(window_to_select[0])

        #Hacienda y Carnes
        cattle_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/table/tbody/tr[8]/td/a/span[2]")))
        cattle_btn.click()

        #Cambio de iframe (ventana)
        time.sleep(5)
        window_to_select = driver.window_handles
        driver.switch_to.window(window_to_select[0])
        driver.close()
        driver.switch_to.window(window_to_select[1])

        person_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/form/table/tbody/tr/td/input[2]')))
        person_btn.click()

        principal_cattle(client_name, date_from, date_to, driver)

    except Exception as e:
        print('Error:', str(e))


#Controlador de procesos
def principal_cattle(client_name, date_from, date_to, driver):
    try:
        #Datos emitidos
        name_file_pdf = 'emitidos_pdf'
        resume_name = 'emitidos_resume'
        section = '//ul[@class="nav sidebar-nav menuBotones"]//a[contains(text(), "Consulta y ajuste de Liquidaciones - Por Emisor")]'
        type_issued = 'issued'
        vouchers_cattle(client_name, date_from, date_to, driver, section, name_file_pdf, resume_name, type_issued)

        #Datos para operacion de receptor
        name_file_pdf = 'receptor_pdf'
        resume_name = 'receptor_resume'
        section = '//ul[@class="nav sidebar-nav menuBotones"]//a[contains(text(), "Consulta y ajuste de Liquidaciones - Por Receptor")]'
        type_receiver = 'receiver'
        vouchers_cattle(client_name, date_from, date_to, driver, section, name_file_pdf, resume_name, type_receiver)

    except Exception as e:
        print('Error:', str(e))


#Proceso segun tipo de voucher
def vouchers_cattle(client_name, date_from, date_to, driver, section, name_file_pdf, resume_name, type):
    try:
        route_base = r"c:\default"
        hamburger_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/button')))
        hamburger_btn.click()

        transmitter_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, section)))
        transmitter_btn.click()

        # Fecha desde
        date_from_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fechaDesde")))
        driver.execute_script("arguments[0].value = '';", date_from_input)
        driver.execute_script("arguments[0].value = arguments[1];", date_from_input, date_from)

        # Fecha hasta
        date_to_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fechaHasta")))
        driver.execute_script("arguments[0].value = '';", date_to_input)
        driver.execute_script("arguments[0].value = arguments[1];", date_to_input, date_to)

        btn_consult = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. ID, 'btnConsultar')))
        btn_consult.click()

        pages = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[3]/div[1]/span/select/option[5]')))
        pages.click()

        #Formateo fecha periodo
        period_date = date_from[3:]
        new_period_date = period_date.replace('/', '-')
        name_folder_period = f'Periodo {new_period_date}'
        #Formateo nombre de cliente a capitalize
        client_name_formated = client_name.title() 
        time.sleep(3)
        if type == 'issued':
            folder_period = folders_cattle_issue(client_name_formated, name_folder_period)
            #Llamo a funcion que verifica y crea carpetas
            folders_cattle_issue(client_name_formated, name_folder_period)
        elif type == 'receiver':
            folder_period = folders_cattle_receiver(client_name_formated, name_folder_period)
            #Llamo a funcion que verifica y crea carpetas
            folders_cattle_receiver(client_name_formated, name_folder_period)
            
        try:
            # Fecha emisión
            date_now = datetime.now().date()
            date_emision = date_now.strftime("%d-%m-%Y")

            # Verifico si existen comprobantes
            table_with_data = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'resultTable')))

            # Si existen datos descargo pdfs
            if table_with_data.text.strip():
                rows = table_with_data.find_elements(By.XPATH, '//*[@id="resultTable"]/tbody/tr')
                # Iterar sobre cada fila
                for row in rows:
                    try:
                        # Leer datos de el comprobante de las distintas columnas
                        cells = row.find_elements(By.TAG_NAME, 'td')
                        if len(cells) > 1:
                            cuit = cells[0].text
                            settlement_type = cells[1].text
                            type_voucher = cells[2].text
                            number_vocuher = cells[3].text
                            date_voucher = cells[4].text
                            date_of_issue = cells[5].text

                        # Btn descarga (última columna)
                        download_button = cells[7].find_element(By.CSS_SELECTOR, 'a.btnImprimir.glyphicon-file')
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
                            name_file = f'{name_file_pdf} {client_name} {cuit} {settlement_type} {type_voucher} {number_vocuher}'
                            new_file_path = os.path.join(folder_period, f"{name_file}.pdf")
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
                    #navHeader, 
                    .page-header,
                    #btnConsultar.
                    #formData,
                    .footer content {
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
                time.sleep(5)
                #Busco archivos en el directorio
                list_of_files = os.listdir(route_base)
                find_file = max(list_of_files, key=lambda f: os.path.getctime(os.path.join(route_base, f)))
                # Mover el archivo más reciente al directorio de destino
                shutil.move(os.path.join(route_base, find_file), folder_period)
                # Verificar que el archivo se haya movido correctamente
                name_file_resume = f'{resume_name} {client_name} {cuit} {settlement_type} {type_voucher} {number_vocuher}.pdf'
                rute_destiny = os.path.join(folder_period, find_file)
                new_file_path = os.path.join(folder_period, name_file_resume)
                os.rename(rute_destiny, new_file_path)
                if os.path.exists(new_file_path):
                    print("El archivo de resumen se movió correctamente")
            except Exception as e:
                print('Error al descargar resumen', {str(e)})           

        except Exception as e:
            print('Error:', str(e))
        

        time.sleep(20)

    except Exception as e:
        print('Error:', str(e))
