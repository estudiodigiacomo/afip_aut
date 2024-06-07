from login_afip import login_afip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
import sys

def primary_in_grains(client_name, type_var, point_sale_var, date_from, date_to, actividad):
    try:
        print()
    except Exception as e:
        print('Error:', str(e))
    sys.exit()