import pytest
from selenium.webdriver.chrome.webdriver import WebDriver
from pages.authPage import AuthPage
from pages.uiPage import MyPage
from pages.apiPage import ApiPage
from testdata.DataProvider import DataProvider
import allure

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.suite("UI and API tests")
@allure.parent_suite("UI tests")
@allure.title("Test create a board")
def test_add_board(log_in, ui_board_list: list, 
        get_add_ui_board: dict, update_list: dict, 
        api_client: ApiPage, get_boards: dict, delete_board):
    with allure.step("Get list of boards before"):
        list_before = ui_board_list
    with allure.step("Get list of boards after"):    
        list_after = update_list
    with allure.step("New board"):    
        ui_board = update_list[0]
    with allure.step("New board on Data Base"):
        new_board = get_boards[0]
    with allure.step("Delete board from Data Base"):
        delete_board["id"] = new_board.get("id")
    
    with allure.step("Check of added board"):
        assert len(list_after) - len(list_before) == 1
    with allure.step("Check  name of added board"):    
        assert new_board.get("name") == ui_board

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("UI tests")
@allure.title("Test delete board")
def test_delete_board(log_in,
        api_client: ApiPage, add_dummy_board: str, 
        get_boards: dict, delete_board_ui, ui_board_list: dict):
    with allure.step("Get list of boards before"):
        list_before = get_boards
        board = get_boards[0]
    with allure.step("Get list of boards after"):    
        list_after = ui_board_list[1:]

    with allure.step("Check of deleted board"):
        assert len(list_before) - len(list_after) == 1
    board_name = board.get("name")    
    with allure.step(f"Check board {board_name} is removed from boards-list"):
        assert board_name not in ui_board_list   

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("UI tests")
@allure.title("Test create a card")
def test_add_card(log_in, api_client: ApiPage, add_dummy_board: str, open_board, 
        ui_card_list: list, get_add_ui_card: dict, 
        ui_card_new_list: dict, get_cards: dict, get_boards: dict, delete_board):
    with allure.step("Get list of cards before"):
        list_before = ui_card_list
    with allure.step("Get list of cards after"):    
        list_after = ui_card_new_list
    with allure.step("Added card"):    
        new_card = get_cards[0]
    with allure.step("Delete board from Data Base"):
        new_board = get_boards[0]
        delete_board["id"] = new_board.get("id")
    
    with allure.step("Check of added card"):
        assert len(list_after) - len(list_before) == 1
    ui_card = ui_card_new_list[0]    
    with allure.step(f"Check  name {ui_card} of added card"):    
        assert new_card.get("name") == ui_card

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("UI tests")
@allure.title("Test ediditing name of card")
def test_edit_card(log_in, api_client: ApiPage, add_dummy_board: str, dummy_card: str, open_board, 
        ui_card_list: list, edit_ui_card: dict, 
        ui_card_new_list: dict, get_cards: dict, get_boards: dict, delete_board):
    with allure.step("Added dummy-card"):    
        new_card = ui_card_list[0]
    with allure.step("Edited card name"):    
        edited_card = ui_card_new_list[0]
    with allure.step("Delete board from Data Base"):
        new_board = get_boards[0]
        delete_board["id"] = new_board.get("id")
    
    with allure.step("Check of added card"):
        assert new_card == 'DUMMY'    
    with allure.step(f"Check new name {edited_card} of added card"):    
        assert DataProvider().get("card_new") == edited_card

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("UI tests")
@allure.title("Test Moving a card to another list")
def test_move_card(log_in, api_client: ApiPage, add_dummy_board: str, dummy_card: str, open_board, 
        ui_card_list: list, move_ui_card: dict, 
        ui_card_new_list: dict, get_cards: dict, get_boards: dict, delete_board):
    with allure.step("Added dummy-card"):    
        new_card = ui_card_list[0]
    with allure.step("Current List"):    
        current_list = move_ui_card[0]
    with allure.step("New List"):    
        new_list = move_ui_card[1]
    with allure.step("Delete board from Data Base"):
        new_board = get_boards[0]
        delete_board["id"] = new_board.get("id")
    
    with allure.step("Check of added card"):
        assert new_card == 'DUMMY'    
    with allure.step(f"Check  name {current_list} of current list"):    
        assert current_list == 'To Do'
    with allure.step(f"Check  name {new_list} of new current list"):    
        assert new_list == 'Doing'

allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("UI tests")
@allure.title("Test delete card")
def test_delete_card(log_in, api_client: ApiPage, add_dummy_board: str, dummy_card: str, open_board, 
        ui_card_list: list, delete_ui_card: dict, 
        ui_card_new_list: dict, get_boards: dict, delete_board):
    with allure.step("Get list of cards before"):
        list_before = ui_card_list
        card_name = ui_card_list[0]
    with allure.step("Get list of cards after"):    
        list_after = ui_card_new_list
    with allure.step("Delete board from Data Base"):
        new_board = get_boards[0]
        delete_board["id"] = new_board.get("id")
    
    with allure.step("Check of added card"):
        assert len(list_before) - len(list_after) == 1    
    with allure.step(f"Check card {card_name} is removed from cards-list"):
        assert card_name not in ui_card_new_list

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("UI tests")
@allure.title("Test Moving a card with mouse")
def test_move_card_mouse(
        log_in, api_client: ApiPage, add_dummy_board: str, 
        dummy_card: str, open_board, move_mouse_card: dict, 
        get_boards: dict, delete_board):
    with allure.step("Current List"):    
        current_list = move_mouse_card[0]
    with allure.step("New List"):    
        new_list = move_mouse_card[1]
    with allure.step("Delete board from Data Base"):
        new_board = get_boards[0]
        delete_board["id"] = new_board.get("id")

    with allure.step(f"Check  name {current_list} of current list"):    
        assert current_list == 'To Do'
    with allure.step(f"Check  name {new_list} of new current list"):    
        assert new_list == 'Doing'