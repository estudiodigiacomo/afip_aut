#main
from gui.main_wind import main_window
from login_afip import login_afip
import sys

if __name__ == "__main__":
    client_name = main_window()
    driver = login_afip(client_name)
    if driver:
        driver.quit()
sys.exit()