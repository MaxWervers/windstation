from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time

from functions import Get_Current_Data

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')  # Helps with limited resources
# options.add_argument('--disable-dev-shm-usage')  # Helps with limited resources
# options.add_argument('--disable-gpu')  # Disable GPU for headless operation
# driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)

try:
    # Open the Windguru page
    driver.get("https://www.windguru.cz/station/521")

    # Allow time for the page to load
    time.sleep(5)  # Adjust sleep time as needed or use WebDriverWait for more control

    while True:

        # Get the current data
        (
            current_wind_speed,
            current_wind_gust_speed,
            current_wind_direction,
            current_temperature,
        ) = Get_Current_Data(driver)

        print(f"Wind speed: {current_wind_speed} knots")
        print(f"Wind gust speed: {current_wind_gust_speed} knots")
        print(f"Wind direction: {current_wind_direction}")
        print(f"Temperature: {current_temperature}°C")
        time.sleep(60)


finally:
    # Close the driver
    driver.quit()
