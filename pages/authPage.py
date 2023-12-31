import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
import pytest
from configurations.ConfigProvider import ConfigProvider
from testdata.DataProvider import DataProvider

class AuthPage:
    
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver
        
    def get_login(self):
        """Open web-page"""
        url = f"{ConfigProvider().ui_url()}{DataProvider().login()}"
        with allure.step('*UI-Page: Open Webpage: {url}'):
            self.__driver.get(url)

    @allure.step('*UI-Page: Enter your Login(E-Mail): {locator} - {text}')
    def enter_email(self, locator, text):
        """Enter Login(E-Mail)"""
        field = self.__driver.find_element(By.ID, locator)
        field.send_keys(text)

    @allure.step('*UI-Page: Click button: {locator}')
    def submit_form(self, locator):
        """Submit Authorization"""
        self.__driver.find_element(By.ID, locator).submit()

    @allure.step('*UI-Page: Enter your Password: {locator} - {text}')
    def enter_password(self, locator, text):
        """Enter Password"""
        WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_all_elements_located((By.ID, locator))
        )
        field = self.__driver.find_element(By.ID, locator)
        field.send_keys(text)

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