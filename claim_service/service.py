from data_service import (
    get_all_claims_db,
    get_claim_by_id_db,
    create_claim_db,
    update_claim_db,
    delete_claim_db
)

def fetch_all_claims():
    return get_all_claims_db()

def fetch_claim_by_id(claim_id: str):
    return get_claim_by_id_db(claim_id)

def add_claim(claim_data: dict):
    if "status" not in claim_data:
        claim_data["status"] = "Pending"
    return create_claim_db(claim_data)

def edit_claim(claim_id: str, claim_data: dict):
    return update_claim_db(claim_id, claim_data)

def remove_claim(claim_id: str):
    return delete_claim_db(claim_id)