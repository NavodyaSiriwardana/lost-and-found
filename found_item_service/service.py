from data_service import (
    get_all_found_items,
    get_found_item_by_id,
    create_found_item,
    update_found_item,
    delete_found_item
)


def fetch_all_found_items():
    return get_all_found_items()


def fetch_found_item_by_id(item_id: str):
    return get_found_item_by_id(item_id)


def add_found_item(item_data: dict):
    return create_found_item(item_data)


def edit_found_item(item_id: str, item_data: dict):
    return update_found_item(item_id, item_data)


def remove_found_item(item_id: str):
    return delete_found_item(item_id)