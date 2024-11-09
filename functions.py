from selenium.webdriver.common.by import By



def Get_Current_Data(driver):
    # Extract wind speed value from the element with class 'wgs_wind_avg_value' and 'wgs_wind_gust_value' and 'wgs_wind_dir_value' and 'wgs_temperature_value'

    current_wind_speed_element = driver.find_element(By.CLASS_NAME, "wgs_wind_avg_value")
    current_wind_speed = current_wind_speed_element.text
    
    current_wind_gust_speed_element = driver.find_element(By.CLASS_NAME, "wgs_wind_max_value")
    current_wind_gust_speed = current_wind_gust_speed_element.text

    current_wind_direction_element = driver.find_element(By.CLASS_NAME, "wgs_wind_dir_numvalue")
    current_wind_direction = current_wind_direction_element.text

    current_temperature_element = driver.find_element(By.CLASS_NAME, "wgs_temp_value")
    current_temperature = current_temperature_element.text

    return current_wind_speed, current_wind_gust_speed, current_wind_direction, current_temperature