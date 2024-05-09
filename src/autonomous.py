from login_afip import login_afip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time
from pdfkit import from_url
from datetime import datetime
import pdfkit
import os

def autonomous(client_name):
    try:
        driver = login_afip(client_name)
        driver.get('https://portalcf.cloud.afip.gob.ar/portal/app/')
        #Tipeo sistema registral
        input_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. ID, 'buscadorInput')))
        input_search.send_keys('sistema registral')
        time.sleep(5)
        #Seleccion de sistema registral
        sistem_regist = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/section/div/div/div[2]/div/div/div[1]/div/div/ul/li[1]/a/div/div/div[1]/div/p")))
        sistem_regist.click()
        time.sleep(2)

        # Selección de primera ventana 
        windows_to_select = driver.window_handles
        driver.switch_to.window(windows_to_select[0])
        # Cierre de ventana mis comprobantes
        driver.close()
        # Cambio de foco a la primera ventana
        driver.switch_to.window(windows_to_select[1])

        #Constancias
        section_constancy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/span/div[1]/article/div[1]/div[1]/div[2]/div/div[2]/div/a/span')))
        section_constancy.click()

        #Constancia de incripcion
        constancy_insc = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/span/div[1]/article/div[3]/div[1]/div/div/div[2]/div[2]/div[2]/a')))
        constancy_insc.click()
        
        time.sleep(3)

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
        route_base = r'd:\Clientes\{}\Reporte'
        route_format = route_base.format(client_name_camel)
        route_completed = os.path.join(route_format, name_folder_emision)

        try:
            # Obtengo el HTML de la páginas
            html_content = driver.page_source

            path_wkhtmltopdf = r'c:\wkhtmltopdf\bin\wkhtmltopdf.exe'

            # Guardo el HTML en un archivo temporal con codificación UTF-8
            with open("temp.html", "w", encoding="utf-8") as file:
                file.write(html_content)

            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

            name_file = f"Constancia de inscripción - Autónomos - AFIP - {client_name} - {name_folder_emision}.pdf"

            pdfkit.from_file("temp.html", os.path.join(route_completed, name_file), configuration=config)    
            print("La constancia de CUIT se ha guardado como PDF.")

        except Exception as e:
            print('Error al procesar descarga de pdf:', str(e))
        
    except Exception as e:
        print('Error al procesar autonomos:', str(e))
    finally:
        driver.quit()
        os._exit(0)
