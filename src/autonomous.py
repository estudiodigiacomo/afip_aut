from login_afip import login_afip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time
import pyautogui

def autonomous(client_name):
    try:
        driver = login_afip(client_name)
        driver.get('https://portalcf.cloud.afip.gob.ar/portal/app/')
        #Tipeo sistema registral
        input_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, 'buscadorInput')))
        input_search.click()
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

        #Consulta
        section_consult = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/span/div[1]/aside/nav/ul/li[2]/a')))
        section_consult.click()

        #Ingresar
        get_into = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/span/div[1]/article/div[3]/div[1]/div/div/div[2]/div[2]/div[2]/a')))
        get_into.click()

        #Exportar
        export = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/span/div[1]/article/div[3]/div[1]/div/div/div[2]/div[2]/div[2]/a')))
        export.click()

        time.sleep(10)
        for _ in range(8):
            pyautogui.press('tab')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(20)
        
        
    except Exception as e:
        print('Error al procesar autonomos:', str(e))