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
from pages.uiPage import MyPage
from configurations.ConfigProvider import ConfigProvider

@pytest.fixture(scope="session")
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
def ui_board_list(browser) -> dict:
    lst = MyPage(browser)
    with allure.step("Open boards list"):
        return lst.get_item_list(DataProvider().get("ui_board_list"))

@pytest.fixture
def get_add_ui_board(ui_page: MyPage) -> dict:
    new_board = ui_page
    with allure.step("Click on 'Create new board'"):
        new_board.open_editor(DataProvider().get("ui_new_board"))
    with allure.step("Enter board name"):
        new_board.create_item(
            DataProvider().get("ui_enter_board_name"),
            DataProvider().get("board_name")
        )
    with allure.step("Click button 'Create'"):
        new_board.submit(DataProvider().get("ui_submit_board"))
    return new_board.load_item(DataProvider().get("ui_board_content"))

@pytest.fixture
def update_list(ui_page: MyPage) -> dict:
    ui_page.get_page(ConfigProvider().ui_url())
    lst = ui_page.get_item_list(DataProvider().get("ui_board_list"))
    with allure.step("Update item list"):
        return lst[1:]

@pytest.fixture
def open_board(ui_page: MyPage, get_boards: list) -> MyPage:
    boards = ui_page
    board = get_boards[0]
    board_title = board.get("name")
    with allure.step(f"Open board {board_title}(click)"):
        boards.get_item(DataProvider().get("ui_open_board"), board_title)

@pytest.fixture
def ui_card_list(browser) -> dict:
    lst = MyPage(browser)
    with allure.step("Open cards list"):
        return lst.get_item_list(DataProvider().get("ui_card_list"))
    
@pytest.fixture
def ui_card_new_list(browser) -> dict:
    lst = MyPage(browser)
    with allure.step("Open cards list"):
        return lst.get_item_list(DataProvider().get("ui_card_list_id"))

@pytest.fixture
def get_add_ui_card(ui_page: MyPage) -> dict:
    new_card = ui_page
    with allure.step("On the 'ToDo' list click 'Add a card'"):
        new_card.open_editor(DataProvider().get("ui_add_card"))
    with allure.step("Enter Card name"):
        new_card.create_item(
            DataProvider().get("ui_new_card"),
            DataProvider().get("card_name")
        )
    with allure.step("Click button 'Add card'"):
        new_card.submit(DataProvider().get("ui_submit_card"))

@pytest.fixture
def edit_ui_card(ui_page: MyPage) -> dict:
    new_card = ui_page
    with allure.step("Open the card with click a card"):
        new_card.open_editor(DataProvider().get("ui_card_menu"))
    with allure.step("Enter new Card name"):
        new_card.edit_field(DataProvider().get("ui_edit_card"))
        new_card.create_item(
            DataProvider().get("ui_edit_card"),
            DataProvider().get("card_new")
        )
    with allure.step("Click button 'X' close"):
        new_card.submit(DataProvider().get("ui_close_edit"))

@pytest.fixture
def delete_ui_card(ui_page: MyPage) -> dict:
    new_card = ui_page
    with allure.step("Open the card with click a card"):
        new_card.open_editor(DataProvider().get("ui_card_menu"))
    with allure.step("Click button 'Archive' in actions-menu"):
        new_card.open_editor(DataProvider().get("ui_archive_card"))
    with allure.step("Click button 'Delete' in actions-menu"):
        new_card.open_editor(DataProvider().get("ui_delete_card"))       
    with allure.step("Click button 'Delete'"):
        new_card.submit(DataProvider().get("ui_close_edit"))

@pytest.fixture
def move_ui_card(ui_page: MyPage) -> dict:
    new_card = ui_page
    with allure.step("On the card with click a card"):
        new_card.open_editor(DataProvider().get("ui_card_menu"))
    with allure.step("Click button 'Move' in actions-menu"):
        c_lst = new_card.get_item_list(DataProvider().get("ui_current_list"))[0]
        #current =[c for c in lst]
        new_card.open_editor(DataProvider().get("ui_move_card"))
    with allure.step("Select another list('Doing')"):
        new_card.open_editor(DataProvider().get("ui_select_list"))
    with allure.step("Submit move card"):
        new_card.submit(DataProvider().get("ui_submit_move"))
        new_lst = new_card.get_item_list(DataProvider().get("ui_current_list"))[0]
    return c_lst, new_lst

@pytest.fixture
def move_mouse_card(ui_page: MyPage) -> dict:
    card = ui_page
    card.open_editor(DataProvider().get("ui_card_menu"))
    c_lst = card.get_item_list(DataProvider().get("ui_current_list"))[0]
    card.submit(DataProvider().get("ui_close_edit"))
    card.drag_and_drop_item(
        DataProvider().get("dragg_card"),
        DataProvider().get("drop_lists")
    )
    card.open_editor(DataProvider().get("ui_card_menu"))
    n_lst = card.get_item_list(DataProvider().get("ui_current_list"))[0]
    card.submit(DataProvider().get("ui_close_edit"))
    return c_lst, n_lst

@pytest.fixture
def delete_board_ui(ui_page: MyPage, open_board):
    with allure.step("Open board"):
        menu = ui_page
    with allure.step("Open Menu"):
        menu.open_editor(DataProvider().get("ui_board_menu"))
    with allure.step("Click on 'Close'"):
        menu.open_editor(DataProvider().get("ui_close_board"))
        with allure.step("Submit 'Close'"):
            menu.submit(DataProvider().get("ui_submit_close"))
    with allure.step("Click on 'permanently delete'"):
        menu.open_editor(DataProvider().get("ui_delete_board"))
        with allure.step("Submit 'Delete'"):
            menu.submit(DataProvider().get("ui_submit_del_board"))
        
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