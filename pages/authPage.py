import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

class AuthPage:
    
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver

    @allure.step('*UI-Page: Open Webpage: {base_url}{log_path}')    
    def get_login(self, base_url, log_path):
        """Open web-page"""
        full_path = f"{base_url}{log_path}"
        self.__driver.get(full_path)

    @allure.step('*UI-Page: Enter your Login(E-Mail): {locator} - {e_mail}')
    def enter_email(self, locator, e_mail):
        """Enter Login(E-Mail)"""
        self.__driver.find_element(By.ID, locator).send_keys(e_mail)

    @allure.step('*UI-Page: Click button: {locator}')
    def submit_form(self, locator):
        """Submit Authorization"""
        self.__driver.find_element(By.ID, locator).submit()

    @allure.step('*UI-Page: Enter your Password: {locator} - {password}')
    def enter_password(self, locator, password):
        """Enter Password"""
        WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_all_elements_located((By.ID, locator))
        )
        self.__driver.find_element(By.ID, locator).send_keys(password)

    def get_current_url(self):
        """Get current web-page"""
        return self.__driver.current_url
    
    @allure.step('*UI-Page: OpenPage as authorized user')
    def set_cookie(self):
        """Set token as Cookie"""
        WebDriverWait(self.__driver, 4).until(
            EC.visibility_of_all_elements_located((By.ID, "content"))
        )
        cookie = self.__driver.get_cookies()
        return cookie
    
    def content(self):
        WebDriverWait(self.__driver, 4).until(
            EC.presence_of_all_elements_located((By.ID, "content"))
        )