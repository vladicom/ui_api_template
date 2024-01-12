import allure
import requests

class ApiPage:
    def __init__(self, base_url: str, token: str) -> None:
        self.__url = base_url
        self.__token = token
        
    @allure.step('*API: Get item list')
    def get_item_list(self, path) -> dict:
        """Gettting a list of items(objects)""" 
        full_path = f"{self.__url}{path}"
        with allure.step(f"Get url: {full_path} with method 'GET'"):
            cookie = {'token': self.__token}
        with allure.step(f"Insert in to Headers 'Cookies': {cookie}"):
            resp = requests.get(full_path, cookies=cookie)
        allure.attach(
            str(resp.request.url), 'GET', allure.attachment_type.TEXT
            )
        return resp.json()
    
    @allure.step('*API: Get item')
    def get_item(self, path, item_id) -> dict:
        """Gettting a info of items(objects)""" 
        full_path = f"{self.__url}{path}{item_id}"
        with allure.step(f"Get url: {full_path} with method 'GET'"):
            cookie = {'token': self.__token}
        with allure.step(f"Insert in to Headers 'Cookies': {cookie}"):
            resp = requests.get(full_path, json=cookie, cookies=cookie)
        allure.attach(
            str(resp.request.url), 'GET', allure.attachment_type.TEXT
            )
        allure.attach(str(resp.request.body), 'BODY', allure.attachment_type.JSON)
        return resp.json()

    @allure.step('*API: Get nested_item list')
    def get_nested_list(self, path, item_id, end_path) -> dict:
        """Gettting a nested list of items(objects)""" 
        full_path = f"{self.__url}{path}{item_id}{end_path}"
        with allure.step(f"Get url: {full_path} with method 'GET'"):
            cookie = {'token': self.__token}
        with allure.step(f"Insert in to Headers 'Cookies': {cookie}"):
            body = {'token': self.__token}
        with allure.step(f"Insert in to Body: JSON: {body}"):
            resp = requests.get(full_path, json=body, cookies=cookie)
        allure.attach(
            str(resp.request.url), 'GET', allure.attachment_type.TEXT
            )
        allure.attach(str(resp.request.body), 'BODY', allure.attachment_type.JSON)
        return resp.json() 
    
    @allure.step('*API: Add new item')
    def add_item(self, path, test_data) -> dict:
        """Creation of new item"""
        full_path = f"{self.__url}{path}"
        with allure.step(f"Method: POST with url: {full_path}"):
            cookie = {'token': self.__token}
        with allure.step(f"Insert in to Headers: Cookies: {cookie}"):
            body = test_data
        with allure.step(f"Insert in to Body: JSON: {body}"):
            resp = requests.post(full_path, json=body, cookies=cookie)
        allure.attach(str(resp.request.url), 'POST', allure.attachment_type.TEXT)
        allure.attach(str(resp.request.body), 'BODY', allure.attachment_type.JSON)
        return resp.json()
    
    @allure.step('*API: Delete item')
    def delete_item_by_id(self, path, item_id) -> dict:
        """Delete item with ID:'value'"""
        full_path = f"{self.__url}{path}{item_id}"
        with allure.step(f"Method: DELETE with url: {full_path}"):
            cookie = {'token': self.__token}
        with allure.step(f"Insert in to Headers: Cookies: {cookie}"):
            body = {'token': self.__token}
        with allure.step(f"Insert in to Body: JSON: {body}"):
            resp = requests.delete(full_path, json=body, cookies=cookie)
        allure.attach(str(resp.request.url), 'DELETE', allure.attachment_type.TEXT)
        allure.attach(str(resp.request.body), 'BODY', allure.attachment_type.JSON)
        return resp.json()
    
    @allure.step('*API: Edit or move item')
    def edit_item_by_id(self, path, test_data, item_id) -> dict:
        """Edit item with ID:'value'"""
        full_path = f"{self.__url}{path}{item_id}"
        with allure.step(f"Method: PUT with url: {full_path}"):
            cookie = {'token': self.__token}
        with allure.step(f"Insert in to Headers: Cookies: {cookie}"):
            body = test_data
        with allure.step(f"Insert in to Body: JSON: {body}"):
            resp = requests.put(full_path, json=body, cookies=cookie)
        allure.attach(str(resp.request.url), 'PUT', allure.attachment_type.TEXT)
        allure.attach(str(resp.request.body), 'BODY', allure.attachment_type.JSON)
        return resp.json()