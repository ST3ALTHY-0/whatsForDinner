from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

import time

class MenuItem:
    def __init__(self, name, calories, time_of_day):
        self.name = name
        self.calories = calories
        self.time_of_day = time_of_day
    
    def __str__(self):
        return f"{self.name} - {self.calories} "
    


def print_menu(menu):
    print("-------------------")
    current_time_of_day = None
    for item in menu:
        if item.time_of_day != current_time_of_day:
            print(f"Time of Day: {item.time_of_day}")
            current_time_of_day = item.time_of_day
        print(item)
    print("***************************")

    
def main():
    # Specify the URL of the website
    url = "https://dineoncampus.com/iui"

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options) 

    driver.get(url)

    try:
        filter_words = ["Pizza", "Crushed Red Pepper", "Dried Oregano", "Grated Parmesan Cheese", "Calzone"]
        select_menu_location(driver, "Tower Dining")
        
        lunch_menu = select_menu_time(driver, "Lunch", filter_words)
        dinner_menu = select_menu_time(driver, "Dinner", filter_words)
        late_night_menu = select_menu_time(driver, "Late Night", filter_words)

        return lunch_menu, dinner_menu, late_night_menu
        
    finally:
        driver.quit()

def select_menu_location(driver, location_name):
    dropdown_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "locations__BV_toggle_")))
    dropdown_button.click()

    dropdown_menu_items = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".dropdown-menu.show a")))
    for item in dropdown_menu_items:
        if item.text.strip() == location_name:
            item.click()
            break

def select_menu_time(driver, time_name, filter_words=None):
    try:
        second_dropdown_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "periods__BV_toggle_")))
        second_dropdown_button.click()

        dropdown_menu_items = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".dropdown-menu.show a")))
        for item in dropdown_menu_items:
            if item.text.strip() == time_name:
                driver.execute_script("arguments[0].scrollIntoView(true);", item)
                item.click()
                break
    
    except (StaleElementReferenceException, TimeoutException) as e:
        print(f"An error occurred: {str(e)}")

    time.sleep(1)
    return get_menu_items(driver, filter_words, time_name)

def get_menu_items(driver, filter_words=None, time_of_day=None):
    menu_items = []
    try:
        menu_items_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "row.menu-tile-item")))

        for menu_item_element in menu_items_elements:
            name = menu_item_element.find_element(By.CLASS_NAME, "col-9").text
            calories = menu_item_element.find_element(By.CLASS_NAME, "d-flex").text
            menu_item = MenuItem(name, calories, time_of_day)

            if not any(word in name for word in filter_words):
                menu_items.append(menu_item)

    except TimeoutException as e:
        print("Timeout occurred while fetching menu items:", e)
    except Exception as e:
        print("Error occurred while fetching menu items:", e)
    time.sleep(1)
    
    return menu_items

if __name__ == "__main__":
    lunch_menu, dinner_menu, late_night_menu = main()
    print_menu(lunch_menu)
    print_menu(dinner_menu)
    print_menu(late_night_menu)
