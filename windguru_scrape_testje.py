from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--headless')
#options.add_experimental_option('detach', True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Open the Windguru page
    driver.get("https://www.windguru.cz/station/521")

    # Allow time for the page to load
    time.sleep(5)  # Adjust sleep time as needed or use WebDriverWait for more control

    for i in range(100):
        # Extract wind speed value from the element with class 'wgs_wind_avg_value'
        wind_speed_element = driver.find_element(By.CLASS_NAME, "wgs_wind_avg_value")
        wind_speed = wind_speed_element.text
        print(f"Wind Speed: {wind_speed}")
        time.sleep(20)


finally:
    # Close the driver
    driver.quit()