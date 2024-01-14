import pytest
from pages.apiPage import ApiPage
from pages.subForm import MyPage
from testdata.DataProvider import DataProvider
from configurations.ConfigProvider import ConfigProvider
import allure

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("UI tests")
@allure.title("Test create a board")
def test_add_board(log_in, ui_page: MyPage, api_client: ApiPage, work_path: str, board_path: str):
    with allure.step("Get list of boards before"):
        list_before = ui_page.get_item_list(DataProvider().get("ui_board_list"))
    with allure.step("Click on 'Create new board'"):
        ui_page.open_editor(DataProvider().get("ui_new_board"))
    with allure.step("Enter board name"):
        ui_page.create_item(DataProvider().get("ui_enter_board_name"), DataProvider().get("board_name"))
    with allure.step("Click button 'Create'"):
        ui_page.submit(DataProvider().get("ui_submit_board"))
    with allure.step("Get list of boards after"):
        ui_page.get_page(ConfigProvider().ui_url())
        list_after = ui_page.get_item_list(DataProvider().get("ui_board_list"))
        added_board = list_after[0]
    with allure.step("Delete board from Data Base"):
        new_board = api_client.get_item_list(work_path)[0]
        api_client.delete_item_by_id(board_path, new_board.get("id"))

    with allure.step("Check of added board"):
         assert len(list_after) - len(list_before) == 1
    with allure.step("Check  name of added board"):    
        assert new_board.get("name") == added_board

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("UI tests")
@allure.title("Test delete board")
def test_delete_board(add_dummy_board: str, log_in, ui_page: MyPage):
    with allure.step("Get list of boards before"):
        ui_page.get_page(ConfigProvider().ui_url())
        list_before = ui_page.get_item_list(DataProvider().get("ui_board_list"))
    with allure.step(f"Open board {add_dummy_board}(click)"):
        ui_page.get_item(DataProvider().get("ui_open_board"), add_dummy_board)
    with allure.step("Open Menu"):
        ui_page.open_editor(DataProvider().get("ui_board_menu"))
    with allure.step("Click on 'Close'"):
        ui_page.open_editor(DataProvider().get("ui_close_board"))
        with allure.step("Submit 'Close'"):
            ui_page.submit(DataProvider().get("ui_submit_close"))
    with allure.step("Click on 'permanently delete'"):
        ui_page.open_editor(DataProvider().get("ui_delete_board"))
        with allure.step("Submit 'Delete'"):
            ui_page.submit(DataProvider().get("ui_submit_del_board"))
    with allure.step("Get list of boards after"):
        ui_page.get_page(ConfigProvider().ui_url())
        list_after = ui_page.get_item_list(DataProvider().get("ui_board_list"))

    with allure.step("Check of deleted board"):
        assert len(list_before) - len(list_after) == 1
    with allure.step(f"Check board {add_dummy_board} is removed from boards-list"):
        assert add_dummy_board not in list_after       

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("UI tests")
@allure.title("Test create a card")
def test_add_card(add_delete_board, log_in, ui_page: MyPage):
    ui_page.get_page(ConfigProvider().ui_url())
    board = ui_page.get_item_list(DataProvider().get("ui_board_list"))[0]
    with allure.step(f"Open board {board}"):
        ui_page.get_item(DataProvider().get("ui_open_board"), board)
    with allure.step("Get list of cards before"):
        list_before = ui_page.get_item_list(DataProvider().get("ui_card_list"))
    with allure.step("On the 'ToDo' list click 'Add a card'"):
        ui_page.open_editor(DataProvider().get("ui_add_card"))
    with allure.step("Enter Card name"):
        ui_page.create_item(DataProvider().get("ui_new_card"), DataProvider().get("card_name"))
        with allure.step("Click button 'Add card'"):
            ui_page.submit(DataProvider().get("ui_submit_card"))
    with allure.step("Get list of cards after"):
        list_after = ui_page.get_item_list(DataProvider().get("ui_card_list"))

    with allure.step("Check of added card"):
        assert len(list_after) - len(list_before) == 1
    with allure.step(f"Check  name {list_after[0]} of added card"):
        list_after[0]  == DataProvider().get("card_name")

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("UI tests")
@allure.title("Test ediditing name of card")
def test_edit_card(add_delete_board, dummy_card: str, log_in, ui_page: MyPage):
    ui_page.get_page(ConfigProvider().ui_url())
    board = ui_page.get_item_list(DataProvider().get("ui_board_list"))[0]
    with allure.step(f"Open board {board}"):
        ui_page.get_item(DataProvider().get("ui_open_board"), board)
    with allure.step(f"Open the card with click a card {dummy_card}"):
        ui_page.open_editor(DataProvider().get("ui_card_menu"))
        with allure.step("Enter new Card name"):
            ui_page.edit_field(DataProvider().get("ui_edit_card"))
            ui_page.create_item(DataProvider().get("ui_edit_card"), DataProvider().get("card_new"))
        with allure.step("Click button 'X' close"):
            ui_page.submit(DataProvider().get("ui_close_edit"))
    edited_card = ui_page.get_item_list(DataProvider().get("ui_card_list"))[0]

    with allure.step(f"Check of added card {dummy_card}"):
        dummy_card == "DUMMY"
    with allure.step(f"Check new name {edited_card} of added card"):
        edited_card == DataProvider().get("card_new")

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("UI tests")
@allure.title("Test Moving a card to another list")
def test_move_card(add_delete_board, dummy_card: str, log_in, ui_page: MyPage):
    ui_page.get_page(ConfigProvider().ui_url())
    board = ui_page.get_item_list(DataProvider().get("ui_board_list"))[0]
    with allure.step(f"Open board {board}"):
        ui_page.get_item(DataProvider().get("ui_open_board"), board)
    with allure.step(f"Open the card with click a card {dummy_card}"):
        ui_page.open_editor(DataProvider().get("ui_card_menu"))
        current_list = ui_page.get_item_list(DataProvider().get("ui_current_list"))[0]
        with allure.step("Click button 'Move' in actions-menu"):    
            ui_page.open_editor(DataProvider().get("ui_move_card"))
        with allure.step("Select another list('Doing')"):
            ui_page.open_editor(DataProvider().get("ui_select_list"))
        with allure.step("Submit move card"):
            ui_page.submit(DataProvider().get("ui_submit_move"))    
    new_list = ui_page.get_item_list(DataProvider().get("ui_current_list"))[0]
       
    with allure.step(f"Check  name {current_list} of current list"):    
        assert current_list == 'To Do'
    with allure.step(f"Check  name {new_list} of new current list"):    
        assert new_list == 'Doing'

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("UI tests")
@allure.title("Test delete card")
def test_delete_card(add_delete_board, dummy_card: str, log_in, ui_page: MyPage):
    ui_page.get_page(ConfigProvider().ui_url())
    board = ui_page.get_item_list(DataProvider().get("ui_board_list"))[0]
    with allure.step(f"Open board {board}"):
        ui_page.get_item(DataProvider().get("ui_open_board"), board)
    with allure.step("Get list of cards before"):
        list_before = ui_page.get_item_list(DataProvider().get("ui_card_list"))
    with allure.step(f"Open the card with click a card {dummy_card}"):
        ui_page.open_editor(DataProvider().get("ui_card_menu"))
        with allure.step("Click button 'Archive' in actions-menu"):
            ui_page.open_editor(DataProvider().get("ui_archive_card"))
        with allure.step("Click button 'Delete' in actions-menu"):
            ui_page.open_editor(DataProvider().get("ui_delete_card"))
            ui_page.load_item(DataProvider().get("ui_submit_delete"))       
        with allure.step("Click button 'Delete'"):
            ui_page.submit(DataProvider().get("ui_submit_delete"))    
    with allure.step("Get list of cards after"):    
        list_after = ui_page.get_item_list(DataProvider().get("ui_card_list"))
    
    with allure.step("Check of deleted card"):
        assert len(list_before) - len(list_after) == 1    
    with allure.step(f"Check card {dummy_card} is removed from cards-list"):
        assert dummy_card not in list_after

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("UI tests")
@allure.title("Test Moving a card with mouse")
def test_move_card_mouse(add_delete_board, dummy_card: str, log_in, ui_page: MyPage):
    ui_page.get_page(ConfigProvider().ui_url())
    board = ui_page.get_item_list(DataProvider().get("ui_board_list"))[0]
    with allure.step(f"Open board {board}"):
        ui_page.get_item(DataProvider().get("ui_open_board"), board)
        ui_page.open_editor(DataProvider().get("dragg_card"))
        ui_page.load_item(DataProvider().get("ui_card_header"))
        current_list = ui_page.get_item_list(DataProvider().get("ui_current_list"))[0]
        with allure.step(f"Current List is {current_list}"):    
            ui_page.submit(DataProvider().get("ui_close_edit"))
    with allure.step(f"Drag card {dummy_card} and drop to another list"):
        ui_page.drag_and_drop_item(DataProvider().get("dragg_card"), DataProvider().get("drop_lists"))
        ui_page.open_editor(DataProvider().get("dragg_card"))
        ui_page.load_item(DataProvider().get("ui_card_header"))
        new_list = ui_page.get_item_list(DataProvider().get("ui_current_list"))[0]
        with allure.step(f"New List is {new_list}"):    
            ui_page.submit(DataProvider().get("ui_close_edit"))

    with allure.step(f"Check  name {current_list} of current list"):    
        assert current_list == 'To Do'
    with allure.step(f"Check  name {new_list} of new current list"):    
        assert new_list == 'Doing'