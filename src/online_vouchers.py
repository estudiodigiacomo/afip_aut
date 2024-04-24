from login_afip import login_afip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

def online_voucher(client_name, type_var, point_sale_var, date_from, date_to):
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
        if point_sale_var == '-' or 'seleccionar...':
            print('No existe punto de venta o se eligio seleccionar')
        elif point_sale_var != '-':
            element_sale_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/form/div/div/table/tbody/tr[5]/td/select')))
            dropdown_sale = Select(element_sale_dropdown)
            options_sale = [opt_sale.text for opt_sale in dropdown_sale.options]
            for opt_sale in options_sale:
                if opt_sale == point_sale_var:
                    dropdown_sale.select_by_visible_text(opt_sale)
                    break
        else:
              print('Error al seleccionar el punto de venta')      

        #Buscar comprobantes
        btn_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/table/tbody/tr/td/input[2]')))
        btn_search.click()

        

        time.sleep(15)
    except Exception as e:
        print('Error:', str(e))
    