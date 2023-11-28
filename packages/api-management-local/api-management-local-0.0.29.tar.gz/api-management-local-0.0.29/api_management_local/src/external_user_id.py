

def get_extenal_user_id_by_api_type_id(api_type_id: int) -> int:
    external_user_ids = {
        1: 100,
        2: 200,
        4: 400,
    }
    return external_user_ids.get(api_type_id)
