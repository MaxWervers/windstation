from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
from datetime import datetime

from functions import *

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

# Extract tide data for a specific date (or today)
target_date = datetime.now().strftime('%Y%m%d')
tides = extract_tides_for_day('2024getijGat8.xml', target_date)

for tide in tides:
    print(f"Time: {tide['time']}, Tide: {tide['type']}, Value: {tide['value']}")


try:
    # Open the Windguru page
    driver.get("https://www.windguru.cz/station/521")

    # Allow time for the page to load
    time.sleep(5)  # Adjust sleep time as needed or use WebDriverWait for more control

    # Set update intervals
    windguru_interval = 30  # Every 30 seconds
    watertemp_interval = 600  # Every 10 minutes (600 seconds)

    # Initialize variables
    last_windguru_update = 0
    last_watertemp_update = 0

    while True:
        current_time = time.time()

        # Update Windguru data if the interval has passed
        if current_time - last_windguru_update >= windguru_interval:
            (
                current_wind_speed,
                current_wind_gust_speed,
                current_wind_direction,
                current_temperature,
            ) = get_current_WG_data(driver)

        # Update water temperature every 10 minutes
        if current_time - last_watertemp_update >= watertemp_interval:
            current_watertemp = get_current_watertemp(
                location="Brouwershavense Gat 8 (b)"
            )

        print(f"Wind speed: {current_wind_speed} knots")
        print(f"Wind gust speed: {current_wind_gust_speed} knots")
        print(f"Wind direction: {current_wind_direction}")
        print(f"Temperature: {current_temperature}°C")
        print(f"Water temperature: {current_watertemp}°C")
        
        last_windguru_update = current_time
        last_watertemp_update = current_time

        # Brief sleep to prevent CPU overload
        time.sleep(5)


finally:
    # Close the driver
    driver.quit()
