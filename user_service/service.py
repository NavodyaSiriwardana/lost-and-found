from datetime import datetime
from data_service import (
    get_all_users_db,
    get_user_by_id_db,
    create_user_db,
    update_user_db,
    delete_user_db,
    find_user_by_email
)

def fetch_all_users():
    return get_all_users_db()

def fetch_user_by_id(user_id: str):
    return get_user_by_id_db(user_id)

def register_new_user(user_data: dict):
    # Email එක දැනටමත් තිබේදැයි පරීක්ෂාව
    if find_user_by_email(user_data["email"]):
        return None  # නැතහොත් Exception එකක් යැවිය හැක
    
    user_data["created_at"] = datetime.utcnow()
    return create_user_db(user_data)

def edit_user(user_id: str, user_data: dict):
    # None අගයන් ඉවත් කිරීම
    update_dict = {k: v for k, v in user_data.items() if v is not None}
    return update_user_db(user_id, update_dict)

def remove_user(user_id: str):
    return delete_user_db(user_id)