#Preferencias
from selenium.webdriver.chrome.options import Options

def setup_nav_preferences(type_voucher):
    options_nav = Options()
    options_nav.add_argument('--start-maximized')
    if type_voucher == 'emitidos':
        download_dir = r"c:\comprobantes-emitidos"
    elif type_voucher == 'recibidos':
        download_dir = r"c:\comprobantes-recibidos"
    elif type_voucher == 'en-linea':
        download_dir = r"c:\comprobantes-recibidos"
    else:
        print('No se recibio tipo de comprobante')

    options_nav.add_experimental_option('prefs', {
    "download.prompt_for_download": False, 
    "download.default_directory": download_dir
    })
    return options_nav