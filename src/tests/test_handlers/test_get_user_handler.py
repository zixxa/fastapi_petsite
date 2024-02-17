from uuid import uuid4


async def test_get_user_by_id(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "John",
        "surname": "Doe",
        "email": "aaa@bbb.com",
        "is_active": True,
    }
    await create_user_in_database(**user_data)
    resp = client.get(f"/user/?user_id={user_data['user_id']}")
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["user_id"] == str(user_data["user_id"])
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["is_active"] == user_data["is_active"]
    assert data_from_resp["email"] == user_data["email"]


async def test_get_user_by_id_validation_error(
    client, create_user_in_database, get_user_from_database
):
    user_data = {
        "user_id": uuid4(),
        "name": "John",
        "surname": "Doe",
        "email": "aaa@bbb.com",
        "is_active": True,
    }
    await create_user_in_database(**user_data)
    resp = client.get(f"/user/?user_id=1")
    assert resp.status_code == 422
    data_from_resp = resp.json()
    assert data_from_resp["detail"] == [
        {
            "loc": ["query", "user_id"],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid",
        }
    ]


async def test_get_user_not_found(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "John",
        "surname": "Doe",
        "email": "aaa@bbb.com",
        "is_active": True,
    }
    wrong_uuid = uuid4()
    await create_user_in_database(**user_data)
    resp = client.get(f"/user/?user_id={wrong_uuid}")
    assert resp.status_code == 404
    data_from_resp = resp.json()
    assert data_from_resp["detail"] == f"User ID {wrong_uuid} not found"
