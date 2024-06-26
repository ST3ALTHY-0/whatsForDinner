from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

import time
from datetime import date
from datetime import datetime

#Could use multi threading to get all menus at once, would need to open multiple browsers

class MenuItem:
    def __init__(self, name, calories, time_of_day, date):
        self.name = name
        self.calories = calories
        self.time_of_day = time_of_day
        self.date = date
    
    def __str__(self):
        return f"{self.name} - {self.calories} "
    
    def get_date(self):
        return self.date
    


def print_menu(menu):
    print("-------------------")
    current_date = lunch_menu[0].get_date()
    print(f"Menu Date: {current_date}")
    current_time_of_day = None
    
    for item in menu:
        if item.time_of_day != current_time_of_day:
            print(f"Time of Day: {item.time_of_day}")
            current_time_of_day = item.time_of_day
        print("Menu item - ", item)
    print("***************************")

    
def main():
    # Specify the URL of the website
    url = "https://dineoncampus.com/iui"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.set_preference('permissions.default.image', 2)

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
    dropdown_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "locations__BV_toggle_")))
    dropdown_button.click()

    dropdown_menu_items = WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".dropdown-menu.show a")))
    for item in dropdown_menu_items:
        if item.text.strip() == location_name:
            item.click()
            break

def select_menu_time(driver, time_name, filter_words=None):
    try:
        second_dropdown_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "periods__BV_toggle_")))
        second_dropdown_button.click()

        dropdown_menu_items = WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".dropdown-menu.show a")))
        for item in dropdown_menu_items:
            if item.text.strip() == time_name:
                driver.execute_script("arguments[0].scrollIntoView(true);", item)
                item.click()
                break
    
    except (StaleElementReferenceException, TimeoutException) as e:
        print(f"An error occurred: {str(e)}")

 #   time.sleep(1)
    return get_menu_items(driver, filter_words, time_name)

def get_menu_items(driver, filter_words=None, time_of_day=None):
    menu_items = []
    try:
        menu_items_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "row.menu-tile-item")))

        for menu_item_element in menu_items_elements:
            name = menu_item_element.find_element(By.CLASS_NAME, "col-9").text
            calories = menu_item_element.find_element(By.CLASS_NAME, "d-flex").text
            date = get_date_of_menu(driver)
            menu_item = MenuItem(name, calories, time_of_day, date)

            if not any(word in name for word in filter_words):
                menu_items.append(menu_item)

    except TimeoutException as e:
        print("Timeout occurred while fetching menu items:", e)
    except Exception as e:
        print("Error occurred while fetching menu items:", e)
   # time.sleep(1)
    
    return menu_items
def get_date_of_menu(driver):
    current_date = datetime.today().strftime('%d %B %Y')
    return current_date



def write_menu_to_file(filename, lunch_menu, dinner_menu, late_night_menu):
    try:
        with open(filename, 'r'):
            pass  # If the file exists, do nothing
    except FileNotFoundError:
        with open(filename, 'w'):
            pass  # Create an empty file if it doesn't exist

    with open(filename, 'a') as file:
        file.write(f"Date: {date.today()}\n")

        file.write("Menu item = Lunch Menu:\n")
        for item in lunch_menu:
            file.write(f"{item}\n")

        file.write(f"\nDate: {date.today()}\n")
        file.write("Menu item = Dinner Menu:\n")
        for item in dinner_menu:
            file.write(f"{item}\n")

        file.write(f"\nDate: {date.today()}\n")
        file.write("Late Night Menu:\n")
        for item in late_night_menu:
            file.write(f"Menu item = {item}\n")



if __name__ == "__main__":
    lunch_menu, dinner_menu, late_night_menu = main()
    #write_menu_to_file("/home/luke/whatsForDinner/public/menu.txt", lunch_menu, dinner_menu, late_night_menu)
    print_menu(lunch_menu)
    print_menu(dinner_menu)
    print_menu(late_night_menu)
