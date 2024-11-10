from selenium.webdriver.common.by import By
import requests
import xml.etree.ElementTree as ET


def get_current_WG_data(driver):
    """
    Retrieves current wind and temperature data from a web page using a Selenium WebDriver.
    Args:
        driver (selenium.webdriver): The Selenium WebDriver instance used to interact with the web page.
    Returns:
        tuple: A tuple containing the current wind speed, wind gust speed, wind direction, and temperature as strings.
    """

    current_wind_speed_element = driver.find_element(By.CLASS_NAME, "wgs_wind_avg_value")
    current_wind_speed = current_wind_speed_element.text
    
    current_wind_gust_speed_element = driver.find_element(By.CLASS_NAME, "wgs_wind_max_value")
    current_wind_gust_speed = current_wind_gust_speed_element.text

    current_wind_direction_element = driver.find_element(By.CLASS_NAME, "wgs_wind_dir_numvalue")
    current_wind_direction = current_wind_direction_element.text

    current_temperature_element = driver.find_element(By.CLASS_NAME, "wgs_temp_value")
    current_temperature = current_temperature_element.text

    return current_wind_speed, current_wind_gust_speed, current_wind_direction, current_temperature


def get_current_watertemp(location):
    """
    Fetches the current water temperature for a given location.
    This function sends a GET request to the waterinfo.rws.nl API to retrieve the latest water temperature measurements.
    It then searches for the specified location within the response data and returns the current water temperature.
    Parameters:
    location (str): The name of the location to fetch the water temperature for.
    Returns:
    float: The current water temperature for the specified location, if found.
    None: If the location is not found or an error occurs during the request.
    Raises:
    requests.RequestException: If there is an issue with the network request.
    """
    url = "https://waterinfo.rws.nl/api/point/latestmeasurement?parameterId=watertemperatuur"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        # Find "Amerongen boven" in the response data
        for feature in data["features"]:
            if feature["properties"]["name"] == location:
                measurement = feature["properties"]["measurements"][0]
                current_watertemp = measurement["latestValue"]
                
                return current_watertemp

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")





def extract_tides_for_day(xml_file, target_date):
    """
    Extracts high and low tide data for a given date from an XML file.

    Parameters:
    - xml_file (str): Path to the XML file.
    - target_date (str): Date to filter tides for, in 'YYYYMMDD' format.

    Returns:
    - list of dict: A list containing dictionaries with time, tide type, and value.
    """
    # Load the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # List to store high and low tide data for the target date
    tide_data = []

    # Iterate over each tide entry
    for value in root.findall('.//value'):
        # Extract datetime, tide type, and value
        datetime_text = value.find('datetime').text.strip()
        tide_type = value.find('tide').text.strip()
        tide_value = value.find('val').text.strip()
        
        # Check if the date part of datetime matches the target date
        if datetime_text.startswith(target_date):
            # Append to tide_data if it's HW or LW
            if tide_type in ('HW', 'LW'):
                tide_data.append({
                    'time': datetime_text[8:12],  # Extract time as HHMM
                    'type': tide_type,
                    'value': tide_value
                })

    return tide_data