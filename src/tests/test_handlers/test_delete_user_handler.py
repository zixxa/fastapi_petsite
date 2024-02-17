from uuid import uuid4


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "John",
        "surname": "Doe",
        "email": "aaa@bbb.com",
        "is_active": True,
    }
    await create_user_in_database(**user_data)
    resp = client.delete(f"/user/?user_id={user_data['user_id']}")
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]


async def test_delete_user_not_found(client):
    uuid = uuid4()
    resp = client.delete(f"/user/?user_id={uuid}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "User not found"


async def test_delete_user_by_id_validation_error(client):
    resp = client.delete(f"/user/?user_id=1")
    assert resp.status_code == 422
    assert resp.json()["detail"] == [
        {
            "loc": ["query", "user_id"],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid",
        }
    ]
