import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import allure
from testdata.DataProvider import DataProvider
from pages.authPage import AuthPage
from pages.apiPage import ApiPage
from pages.subForm import MyPage
from configurations.ConfigProvider import ConfigProvider

@pytest.fixture(scope="session")
def browser():
    with allure.step('Open and configure browser'):
        timeout = ConfigProvider().getint("ui", "timeout")
        yor_browser = ConfigProvider().get("ui","your_browser")
        if yor_browser == 'Chrome':
            #browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            browser = webdriver.Chrome()
        else:
            browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        browser.implicitly_wait(timeout)
        browser.maximize_window()
        yield browser
    with allure.step('Close browser'):
        browser.quit()

@pytest.fixture(scope="module")
def log_in(browser) -> AuthPage:
    log_page = AuthPage(browser)
    with allure.step("Open page"):
        log_page.get_login(
            base_url=ConfigProvider().ui_url(), log_path=DataProvider().get("log_path")
        )
    with allure.step("Autorization on the page"):
        log_page.enter_email("user", DataProvider().e_mail())
        log_page.submit_form("login")
        log_page.enter_password("password", DataProvider().password())
        log_page.submit_form("login-submit")
        log_page.set_cookie()
    yield browser

@pytest.fixture
def ui_page(browser) -> MyPage:
    return MyPage(browser)

@pytest.fixture
def api_client() -> ApiPage:
    return ApiPage(ConfigProvider().api_url(), DataProvider().get_token())

@pytest.fixture
def board_path() -> str:
    return DataProvider().get("boards_path")

@pytest.fixture
def card_path() -> str:
    return DataProvider().get("card_path")

@pytest.fixture
def list_path() -> str:
    return DataProvider().get("list_path")

@pytest.fixture
def work_path(board_path) -> str:
    org = DataProvider().get("work")
    orgId = DataProvider().get("orgID")
    return f"{org}{orgId}{board_path}"

@pytest.fixture
@allure.step("Create a test-board for UI")
def add_dummy_board(board_path) -> str:
    api = ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
    body = {
        "name": DataProvider().get("dummy_name"),
        "defaultLists": True,
        "token": DataProvider().get("token")
    }
    resp = api.add_item(board_path, body).get("name")
    return resp

@pytest.fixture
@allure.step("Create a test-board for API")
def add_dummy_api(board_path) -> str:
    api = ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
    body = {
        "name": DataProvider().get("dummy_name"),
        "defaultLists": True,
        "token": DataProvider().get("token")
    }
    resp = api.add_item(board_path, body).get("id")
    return resp

@pytest.fixture(scope='function')
def add_delete_board(board_path) -> str:
    with allure.step("Create a test-board"):
        api = ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
        body = {
            "name": DataProvider().get("dummy_name"),
            "defaultLists": True,
            "token": DataProvider().get("token")
        }
        resp = api.add_item(board_path, body).get("id")
    yield resp
    with allure.step("Delete test-board"):
        api.delete_item_by_id(board_path, resp)

@pytest.fixture
def lists_path(board_path, add_delete_board, list_path) -> str:
    return f"{board_path}{add_delete_board}{list_path}"

@pytest.fixture
@allure.step("Defining list ID")
def get_lists(lists_path) -> dict:
    api = ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
    resp = api.get_item_list(lists_path)
    return resp

@pytest.fixture
@allure.step("Create a test-card for UI")
def dummy_card(card_path, get_lists: dict):
    body = {
        "name": DataProvider().get("dummy_name"),
        "idList": get_lists[0].get("id"),
        "token": DataProvider().get("token")
    }
    api = ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
    resp = api.add_item(card_path, body)
    return resp.get("name")

@pytest.fixture
@allure.step("Create a test-card for API")
def api_dummy_card(card_path, get_lists: dict):
    body = {
        "name": DataProvider().get("dummy_name"),
        "idList": get_lists[0].get("id"),
        "token": DataProvider().get("token")
    }
    api = ApiPage(ConfigProvider().api_url(), DataProvider().get_token())
    resp = api.add_item(card_path, body)
    return resp.get("id")
            
@pytest.fixture
def api_anonym() -> ApiPage:
    return ApiPage(ConfigProvider().api_url(), "")

####################################################

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
def cards_path(board_path, add_delete_board, card_path) -> str:
    return f"{board_path}{add_delete_board}{card_path}"

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