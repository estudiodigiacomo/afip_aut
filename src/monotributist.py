from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from login_afip import login_afip
from selenium import webdriver
import os
import time 

def monotributist(client_name, constancy):
    try:
        driver = login_afip(client_name)
        driver.get('https://portalcf.cloud.afip.gob.ar/portal/app/')

        download_dir = r'c:\test'

        # Configura la ruta de descarga
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {
            'cmd': 'Page.setDownloadBehavior',
            'params': {'behavior': 'allow', 'downloadPath': download_dir}
        }

        # Agregar opciones al objeto driver
        driver.chrome_options = webdriver.ChromeOptions()
        driver.chrome_options.add_argument('--disable-gpu')
        driver.chrome_options.add_argument('--print-to-pdf')
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

        #Seccion contancia
        section_constancy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/form/main/section/div/div/aside/nav/ul/div[1]/li[4]/a')))
        section_constancy.click()

        if constancy == 'Constancia de CUIT':
            constancy_cuit(driver)
        elif constancy == 'Formulario 184':
            click_constancy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/form/main/section/div/div/div/div[2]/div/div/div[3]/a')))
            click_constancy.click()
        elif constancy == 'Credencial de pago':
            click_constancy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/form/main/section/div/div/div/div[3]/div/div/div[3]/a')))
            click_constancy.click()
        elif constancy == 'Formulario Nº 960 Data Fiscal':
            click_constancy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/form/main/section/div/div/div/div[4]/div/div/div[3]/button')))
            click_constancy.click()
        else:
            print('No se selecciono constancia ')

        time.sleep(15)

    except Exception as e:
        print('Error al procesar constancias:', str(e))
    finally:
        driver.quit()
        os._exit(0)

def constancy_cuit(driver):
    click_constancy = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/form/main/section/div/div/div/div[1]/div/div/div[3]/button')))
    click_constancy.click()

    # Selección de primera ventana 
    windows_to_select = driver.window_handles
    driver.switch_to.window(windows_to_select[0])
    # Cierre de ventana mis comprobantes
    driver.close()
    # Cambio de foco a la primera ventana
    driver.switch_to.window(windows_to_select[1])
    time.sleep(5)
    #Btn imprimir
    print_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/table[1]/tbody/tr/td[3]/table/tbody/tr/td/a')))
    print_btn.click()
    time.sleep(2)
    
    try:
        #Guardar como PDF
        dropdown_pdf = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='destinationSelect']/option[@value='Save as PDF/local/']")))
        # Hacer clic en la opción "Guardar como PDF"
        dropdown_pdf.click()
    except:
        print('FALLO AL ELEGIR PDF EN DROPDOWN')
    time.sleep(5)

    try:
        #Botón guardar
        save_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/print-preview-app//print-preview-sidebar//print-preview-button-strip//div/cr-button[1]')))
        save_button.click()
    except:
        print('FALLO AL PRESIONAR BOTON DE GUARDAR')
    