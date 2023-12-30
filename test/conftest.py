import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import allure
from testdata.DataProvider import DataProvider
from pages.authPage import AuthPage
from pages.apiPage import ApiPage
from configurations.ConfigProvider import ConfigProvider

@pytest.fixture()
def browser():
    with allure.step('Open and configure browser'):
        timeout = ConfigProvider().getint("ui", "timeout")
        yor_browser = ConfigProvider().get("ui","your_browser")
        if yor_browser == 'Chrome':
            browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        else:
            browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        browser.implicitly_wait(timeout)
        browser.maximize_window()
        yield browser
    with allure.step('Close browser'):
        browser.quit()

@pytest.fixture
def token(browser):
        auth = AuthPage(browser)
        auth.get_login()
        auth.enter_email("user", DataProvider().e_mail())
        auth.submit_form("login")
        auth.enter_password("password", DataProvider().password)
        auth.submit_form("login-submit")
        cookie = auth.set_cookie()
        #return cookie

@pytest.fixture
def api_client() -> ApiPage:
    return ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
            
@pytest.fixture
def api_anonym() -> ApiPage:
    return ApiPage(ConfigProvider().api_url(), "")

@pytest.fixture
def board_path():
    return DataProvider().get("boards_path")

@pytest.fixture
def card_path():
    return DataProvider().get("card_path")

@pytest.fixture
def list_path():
    return DataProvider().get("list_path")

@pytest.fixture
def work_path(board_path) -> str:
    org = DataProvider().get("work")
    orgId = DataProvider().get("orgID")
    return f"{org}{orgId}{board_path}"

@pytest.fixture
def get_boards(work_path) -> list:
    api = ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
    resp = api.get_item_list(work_path)
    yield resp
    return resp

@pytest.fixture
def board_body() -> list:
    body = {
        "name": DataProvider().get("board_name"),
        "defaultLists": True,
        "token": DataProvider().get("token")
    }
    yield body
    return body

@pytest.fixture
@allure.step("Create a test-board")
def add_dummy_board(board_path) -> str:
    api = ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
    body = {
        "name": DataProvider().get("dummy_name"),
        "defaultLists": True,
        "token": DataProvider().get("token")
    }
    resp = api.add_item(board_path, body).get("id")
    return resp  

@pytest.fixture
def delete_board(board_path) -> str:
    dictionary = {}
    yield dictionary
    api = ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
    api.delete_item_by_id(board_path, dictionary.get("id"))

@pytest.fixture
def cards_path(board_path, add_dummy_board, card_path) -> str:
    return f"{board_path}{add_dummy_board}{card_path}"

@pytest.fixture
def get_cards(cards_path) -> dict:
    api = ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
    resp = api.get_item_list(cards_path)
    return resp

@pytest.fixture
def body_card() -> dict:
    dictionary = {}
    body = {
        "name": DataProvider().get("card_name"),
        "idList": dictionary.get("id"),
        "token": DataProvider().get("token")
    }
    yield body
    return body

@pytest.fixture
@allure.step("Create a test-card")
def dummy_card(card_path, get_lists: dict):
    body = {
        "name": DataProvider().get("dummy_name"),
        "idList": get_lists[0].get("id"),
        "token": DataProvider().get("token")
    }
    api = ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
    resp = api.add_item(card_path, body)
    return resp.get("id")
    

@pytest.fixture
def card_edit() -> None:
    dictionary = {}
    body = {
        "name": DataProvider().get("card_new"),
        "idList": dictionary.get("id"),
        "token": DataProvider().get("token")
    }
    yield body
    return body

@pytest.fixture
def card_move() -> None:
    dictionary = {}
    body = {
        "idList": dictionary.get("id"),
        "token": DataProvider().get("token")
    }
    yield body
    return body

@pytest.fixture
def delete_card(card_path) -> str:
    dictionary = {'id': ""}
    yield dictionary
    api = ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
    api.delete_item_by_id(card_path, dictionary.get("id"))

@pytest.fixture
def lists_path(board_path, add_dummy_board, list_path) -> str:
    return f"{board_path}{add_dummy_board}{list_path}"

@pytest.fixture
@allure.step("Defining list ID")
def get_lists(lists_path):
    api = ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
    resp = api.get_item_list(lists_path)
    return resp