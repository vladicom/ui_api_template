import allure
import pytest
from pages.apiPage import ApiPage
from testdata.DataProvider import DataProvider

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.suite("UI and API tests")
@allure.parent_suite("API tests")
@allure.title("Test create a board")
def test_add_board(
    api_client: ApiPage,         
        get_boards: dict, board_path: str, 
        board_body: dict, work_path: str, delete_board: dict):
    with allure.step("Create a Board"):
        list_before = get_boards
        resp = api_client.add_item(board_path, board_body)
        list_after = api_client.get_item_list(work_path)
    with allure.step("Delete test-board"):
        delete_board["id"] = resp.get("id")
    with allure.step("Checking that the bord has been added"):
        assert len(list_after) - len(list_before) == 1
    with allure.step("checking that the board name matches"):
        assert resp.get("name") == DataProvider().get("board_name")

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("API tests")
@allure.title("Test delete board")
def test_delete_board(
        api_client: ApiPage, 
        add_dummy_board: str, 
        get_boards: dict, board_path: str, work_path: str):
    with allure.step("Delete a Board"):
        list_before = get_boards
        api_client.delete_item_by_id(board_path, add_dummy_board)
        list_after = api_client.get_item_list(work_path)
    with allure.step("Board removal check"):
        assert len(list_before) - len(list_after) == 1

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("API tests")
@allure.title("Test create a card")
def test_add_card(
        api_client: ApiPage, 
        add_dummy_board: str, 
        get_cards: dict, get_lists: dict, 
        card_path, body_card, cards_path, delete_board):
    with allure.step("Create a Card"):
        list_before = get_cards
        body_card["idList"] = get_lists[0].get("id")
        card = api_client.add_item(card_path, body_card)
        list_after = api_client.get_item_list(cards_path)
    with allure.step("Delete test-board"):
        delete_board["id"] = add_dummy_board
    with allure.step("Checking that the card has been added"):
        assert len(list_after) - len(list_before) == 1
    with allure.step("checking that the card name matches"):
        assert card.get("name") == DataProvider().get("card_name")

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("API tests")
@allure.title("Test ediditing name of card")
def test_edit_card(
        api_client: ApiPage, 
        add_dummy_board: str, 
        get_cards: dict, dummy_card: str, 
        get_lists: dict, card_path: str, card_edit: dict, 
        cards_path: str, delete_board: str):
    with allure.step("Edit name from Card"):
        list_before = get_cards
        card_edit["idList"] = get_lists[0].get("id")
        card = api_client.edit_item_by_id(card_path, card_edit, dummy_card)
        list_after = api_client.get_item_list(cards_path)
    with allure.step("Delete test-board"):    
        delete_board["id"] = add_dummy_board
    with allure.step("Name change check"):
        assert len(list_after) - len(list_before) == 1
        assert card.get("name") == DataProvider().get("card_new")

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("API tests")
@allure.title("Test Moving a card to another list")
def test_move_card(
        api_client: ApiPage, 
        add_dummy_board: str, 
        dummy_card: str, get_cards: dict,
        get_lists: dict, card_path: str, card_move: dict, 
        cards_path: str, delete_board: str):
    with allure.step("Moving a card to another list"):
        list_before = get_cards
        resp = api_client.get_item(card_path, dummy_card)
        card_move["idList"] = get_lists[1].get("id")
        card = api_client.edit_item_by_id(card_path, card_move, dummy_card)
        list_after = api_client.get_item_list(cards_path)
    with allure.step("Delete test-board"):   
        delete_board["id"] = add_dummy_board

    with allure.step("Cards moving check"):
        assert len(list_after) == len(list_before)
        assert card.get("name") == resp.get("name")
        assert card.get("idList") != resp.get("idList")

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("API tests")
@allure.title("Test delete card")
def test_delete_card(
        api_client: ApiPage, 
        add_dummy_board: str, dummy_card: str, 
        get_cards: dict, card_path: str, 
        cards_path: str, delete_board: str):
    with allure.step("Delete a Card"):
        list_before = get_cards
        api_client.delete_item_by_id(card_path, dummy_card)
        list_after = api_client.get_item_list(cards_path)
    with allure.step("Delete a test-board"):    
        delete_board["id"] = add_dummy_board
    with allure.step("Card removal check"):
        assert len(list_before) - len(list_after) == 1