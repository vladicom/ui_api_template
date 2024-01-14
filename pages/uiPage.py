import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains

class MyPage():

    def __init__(self, driver: WebDriver):
        self.__driver = driver

    @allure.step('*UI-Page: Open MyPage: {url}')       
    def get_page(self, url):
        """Open page"""
        self.__driver.get(url)
    
    @allure.step('*UI-Page: Update item list')
    def get_update_list(self, locator):
        """Update list of items(Click on menu with 'items')"""
        self.__driver.find_element(By.XPATH, locator).click()
    
    
    def get_item_list(self, locator):
        """Get list of items"""
        with allure.step('*UI-Page: Get item list'):
            lst = self.__driver.find_elements(By.XPATH, locator)
            items = [i.text for i in lst]
        allure.attach(
            str(items), 'List of items', allure.attachment_type.TEXT
            )
        return items
    
    def open_editor(self, locator):
        """Click a button(link) to editing(archive, delete and etc.)"""
        with allure.step('*UI-Page: Get to action'):
            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, locator))
            ).click()
    
    def edit_field(self, locator):
        """Clearing a field for enter value"""
        with allure.step('*UI-Page: Clear field'):
            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, locator))
            ).clear()
    
    def create_item(self, locator, item_title):
        """Creating an element with a name(value)"""
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, locator))
        ).send_keys(item_title)
        with allure.step(f'*UI-Page: Enter Title for new item {item_title}'):    
            WebDriverWait(self.__driver, 10).until(
                EC.text_to_be_present_in_element_value((By.XPATH, locator), item_title)
            )

    def submit(self, locator):
        """Click or submit button"""
        with allure.step('*UI-Page: Submit action'):
            WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, locator))
            ).click()
    
    def get_item(self, locator, item_title):
        """Get to item with text == value"""
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, locator))
        )
        items = self.__driver.find_elements(By.XPATH, locator)
        for item in items:
            if item_title in item.text:
                with allure.step(f'*UI-Page: Get item with Title: {item_title}'):
                    item.click()
    
    def load_item(self, locator):
        """Wait for the dinamic elements(page, new window, etc.) to load """
        with allure.step('*UI-Page: Wait for the element to load'):
            WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, locator))
        )

            
    def get_id(self, locator, item_title, attr):
        """Get a item ID with attribute"""
        items = self.__driver.find_elements(By.XPATH, locator)
        for item in items:
            item_id = item.get_attribute(f'{attr}')
            with allure.step('*UI-Page: Get ID for the element'):
                if item.text == item_title:
                    return item_id
            allure.attach(
            str(item_title, attr, item_id), 'Element ID', allure.attachment_type.TEXT
            )
        return None
            
    def drag_and_drop_item(self, draggable, droppable):
        source_item = WebDriverWait(self.__driver,10).until(
            EC.presence_of_element_located((By.XPATH, draggable))
        )
        target_item = WebDriverWait(self.__driver,10).until(
            EC.presence_of_element_located((By.XPATH, droppable))
        )
        action = ActionChains(self.__driver)
        action.drag_and_drop(source_item, target_item).perform()
        
    def get_lst(self, locator, text, attr):
        items = self.__driver.find_elements(By.XPATH, locator)
        for item in items:
            item_id = item.get_dom_attribute(f'{attr}')
            if item.find_element(By.XPATH, f'//*[contains(text(), "{text}")]'):
                return item_id