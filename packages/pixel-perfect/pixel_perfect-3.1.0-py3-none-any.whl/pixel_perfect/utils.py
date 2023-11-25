from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from pixel_perfect import image_similarity 

# it can give any property like font-size, font, background-color and  color
def get_property_by_xpath(driver, location, property):
    element_property = driver.find_element(
        By.XPATH, location).value_of_css_property(property)
    return element_property

def get_image_aspect_ratio(driver, location):
    image_element = driver.find_element(By.XPATH, location)

    # Attempt to get aspect ratio from the "aspect-ratio" attribute
    aspect_ratio = driver.execute_script('return arguments[0].getAttribute("aspect-ratio");', image_element)

    # Attempt to get computed aspect ratio from CSS
    aspect_ratio_script = 'return window.getComputedStyle(arguments[0]).getPropertyValue("aspect-ratio");'
    computed_aspect_ratio = driver.execute_script(aspect_ratio_script, image_element)

    # Check which aspect ratio is valid and in the correct format
    if aspect_ratio and aspect_ratio.strip().lower() not in ('none', 'auto'):
        return aspect_ratio
    elif computed_aspect_ratio:
        return computed_aspect_ratio.replace(" ", "")
    else:
        # Return a default value or raise an exception if both are missing
        return None
    
def get_element_by_xpath(driver, location):
    element = driver.find_element(
        By.XPATH, location)
    return element

def get_text_by_xpath(driver, location):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, location)))
        actual_text = element.text
        return actual_text
    except:
        # If the element is not found, scroll to it using JavaScript
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, location)))
        return element.text

def get_count(driver, location):
    elements = driver.find_elements(By.XPATH, location)
    return len(elements)

def get_image_offset_ratio(driver, css_selector):
    script = f"const image = document.querySelector('{css_selector}'); return image.offsetWidth / image.offsetHeight;"
    offset_ratio = driver.execute_script(script)
    return offset_ratio

def get_image_offset_ratio_xpath(driver, xpath_selector):
    script = f"const image = document.evaluate('{xpath_selector}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; return image.offsetWidth / image.offsetHeight;"
    offset_ratio = driver.execute_script(script)
    return offset_ratio

def click_element_by_xpath(driver, location):
    try:
        element = driver.find_element(By.XPATH, location)
        element.click()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def take_screenshots_by_xpath(url, elements_xpaths, componentName):
    for key, value in elements_xpaths.items():        
        take_screenshot_by_xpath(url, value, key, componentName)

def take_screenshot_by_xpath(url, element_xpath, element_name, componentName):
    try:
        baseline_tc_folder =  f"baseline/{componentName}/"
        os.makedirs(baseline_tc_folder, exist_ok=True)

        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
    
        driver = webdriver.Chrome(options=options)
        vars = {}
        driver.get(url)
        time.sleep(2)
        element = get_element_by_xpath(driver, element_xpath)
        web_page_height = driver.execute_script(
            "return Math.max("
            "document.body.scrollHeight, "
            "document.body.offsetHeight, "
            "document.documentElement.clientHeight, "
            "document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        driver.set_window_size(1920,web_page_height)

        time.sleep(2)
        element_screenshot = element.screenshot_as_png
        output_path = f"{baseline_tc_folder}/{element_name}_baseline.png"
 
        with open(output_path, 'wb') as file:
            file.write(element_screenshot)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

def assert_elements_screenshots(self, url, section_xpaths, element_name, componentName):
        
        root_folder = f"baseline/{componentName}/"
        self.driver.get(url)
        time.sleep(3)
 
        print(f"Verify {componentName} - {element_name}")

        expectedImage = f"{root_folder}/{element_name}_baseline.png"
        actual_image = f"{root_folder}/{element_name}_actual.png"

        contact_us_section = get_element_by_xpath(self.driver, section_xpaths[element_name])
        web_page_height = self.driver.execute_script(
            "return Math.max("
            "document.body.scrollHeight, "
            "document.body.offsetHeight, "
            "document.documentElement.clientHeight, "
            "document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        self.driver.set_window_size(1920,web_page_height)

        time.sleep(2)
        element_screenshot = contact_us_section.screenshot_as_png
        with open(actual_image, "wb") as file:
            file.write(element_screenshot)

        result = image_similarity(expectedImage, actual_image)
        assert result == True



def verify_element(url, elements_xpaths, element_name, component_name):
    assert_elements_screenshots(url, elements_xpaths, element_name, component_name)

def capture_baselines(url, elements_xpaths, component_name):
    print(f"Capture baseline screenshot for {component_name}")
    take_screenshots_by_xpath(url, elements_xpaths, component_name)