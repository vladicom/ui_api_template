import allure
import pytest
from pages.apiPage import ApiPage
from testdata.DataProvider import DataProvider

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("API tests")
@allure.title("Test create a board")
def test_add_board(api_client: ApiPage, board_path: str, board_body: dict, work_path: str):
    list_before = api_client.get_item_list(work_path)
    with allure.step("Create a Board"):
        resp = api_client.add_item(board_path, board_body)
    list_after = api_client.get_item_list(work_path)
    with allure.step("Delete test-board"):
        api_client.delete_item_by_id(board_path, resp.get("id"))
        
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
def test_delete_board(api_client: ApiPage, add_dummy_api: str, board_path: str, work_path: str):
    list_before = api_client.get_item_list(work_path)
    with allure.step("Delete a Board"):
        api_client.delete_item_by_id(board_path, add_dummy_api)
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
    api_client: ApiPage, cards_path: str, get_lists: dict, card_path: str, body_card: dict):
    list_before = api_client.get_item_list(cards_path)
    with allure.step("Create a Card"):
        body_card["idList"] = get_lists[0].get("id")
        card = api_client.add_item(card_path, body_card)
    list_after = api_client.get_item_list(cards_path)
    
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
        api_client: ApiPage, get_lists: dict, api_dummy_card: str, card_path: str, card_edit: dict):
    with allure.step("Edit name from Card"):
        card_edit["idList"] = get_lists[0].get("id")
        card = api_client.edit_item_by_id(card_path, card_edit, api_dummy_card)

    with allure.step("Name change check"):
        assert card.get("name") == DataProvider().get("card_new")

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("API tests")
@allure.title("Test Moving a card to another list")
def test_move_card(
        api_client: ApiPage, get_lists: dict, api_dummy_card: str, card_path: str, card_move: dict):
    with allure.step("Moving a card to another list"):
        in_list_befor = api_client.get_item(card_path, api_dummy_card)
        card_move["idList"] = get_lists[1].get("id")
        in_list_after = api_client.edit_item_by_id(card_path, card_move, api_dummy_card)

    with allure.step("Cards moving check"):
        assert in_list_after.get("name") == in_list_befor.get("name")
        assert in_list_after.get("idList") != in_list_befor.get("idList")

@allure.epic("Automatization with Pyton")
@allure.feature("Framework architecture")
@allure.story("Testing Atlassian-Trello")
@allure.parent_suite("UI and API tests")
@allure.suite("API tests")
@allure.title("Test delete card")
def test_delete_card(
        api_client: ApiPage, get_lists: dict, api_dummy_card: str, cards_path: str, card_path: str):
    list_before = api_client.get_item_list(cards_path)
    with allure.step("Delete a Card"):    
        api_client.delete_item_by_id(card_path, api_dummy_card)
    list_after = api_client.get_item_list(cards_path)
    
    with allure.step("Card removal check"):
        assert len(list_before) - len(list_after) == 1