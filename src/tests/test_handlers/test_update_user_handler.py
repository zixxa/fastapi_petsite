import json
from uuid import uuid4

import pytest


async def test_update_user_by_id(
    client, create_user_in_database, get_user_from_database
):
    user_data = {
        "user_id": uuid4(),
        "name": "John",
        "surname": "Doe",
        "email": "aaa@bbb.com",
        "is_active": True,
    }
    updated_data = {"name": "Richard", "surname": "Grey", "email": "bbb@aaa.com"}
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}", data=json.dumps(updated_data)
    )
    assert resp.status_code == 200
    data_from_resp = resp.json()
    assert data_from_resp["updated_user_id"] == str(user_data["user_id"])

    users_from_db = await get_user_from_database(data_from_resp["updated_user_id"])
    user_from_db = dict(users_from_db[0])
    assert updated_data["name"] == user_from_db["name"]
    assert updated_data["email"] == user_from_db["email"]
    assert updated_data["surname"] == user_from_db["surname"]
    assert user_data["is_active"] == user_from_db["is_active"]
    assert user_data["user_id"] == user_from_db["user_id"]


@pytest.mark.parametrize(
    "user_data_updated, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                "detail": "At least one parameter for user update into should be provided"
            },
        ),
        ({"name": "123"}, 422, {"detail": "Name should contains only letters"}),
        ({"surname": "123"}, 422, {"detail": "Surname should contains only letters"}),
        (
            {"email": "123"},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address",
                        "type": "value_error.email",
                    }
                ]
            },
        ),
        (
            {"email": ""},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address",
                        "type": "value_error.email",
                    }
                ]
            },
        ),
        (
            {"name": ""},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "name"],
                        "msg": "ensure this value has at least 1 characters",
                        "type": "value_error.any_str.min_length",
                        "ctx": {"limit_value": 1},
                    }
                ]
            },
        ),
        (
            {"surname": ""},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "surname"],
                        "msg": "ensure this value has at least 1 characters",
                        "type": "value_error.any_str.min_length",
                        "ctx": {"limit_value": 1},
                    }
                ]
            },
        ),
    ],
)
async def test_update_user_validation_error(
    client,
    create_user_in_database,
    get_user_from_database,
    user_data_updated,
    expected_status_code,
    expected_detail,
):
    user_data = {
        "user_id": uuid4(),
        "name": "John",
        "surname": "Doe",
        "email": "aaa@bbb.com",
        "is_active": True,
    }
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated)
    )
    assert resp.status_code == expected_status_code
    resp_data = resp.json()
    assert resp_data == expected_detail


async def test_update_user_id_validation_error(client):
    user_data = {
        "name": "John",
        "surname": "Doe",
        "email": "aaa@bbb.com",
    }
    resp = client.patch(f"/user/?user_id=123", data=json.dumps(user_data))
    assert resp.status_code == 422
    data_from_resp = resp.json()
    assert data_from_resp["detail"] == [
        {
            "loc": ["query", "user_id"],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid",
        }
    ]


async def test_update_not_found_error(client):
    user_data = {
        "name": "John",
        "surname": "Doe",
        "email": "aaa@bbb.com",
    }
    user_id = uuid4()
    resp = client.patch(f"/user/?user_id={user_id}", data=json.dumps(user_data))
    assert resp.status_code == 404
    data_from_resp = resp.json()
    assert data_from_resp["detail"] == f"User ID {user_id} not found"


async def test_update_user_dublicate_email_error(client, create_user_in_database):
    user_data_1 = {
        "user_id": uuid4(),
        "name": "John",
        "surname": "Doe",
        "email": "aaa@bbb.com",
        "is_active": True,
    }
    user_data_2 = {
        "user_id": uuid4(),
        "name": "Rick",
        "surname": "Blue",
        "email": "kek@bbb.com",
        "is_active": True,
    }
    user_dublicate_email = {"email": user_data_2["email"]}

    for user_data in [user_data_1, user_data_2]:
        await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data_1['user_id']}",
        data=json.dumps(user_dublicate_email),
    )
    assert resp.status_code == 503
    assert (
        'duplicate key value violates unique constraint "users_email_key"'
        in resp.json()["detail"]
    )


async def test_update_user_only_one(
    client, create_user_in_database, get_user_from_database
):
    user_data_1 = {
        "user_id": uuid4(),
        "name": "John",
        "surname": "Doe",
        "email": "aaa@bbb.com",
        "is_active": True,
    }
    user_data_2 = {
        "user_id": uuid4(),
        "name": "Rick",
        "surname": "Grey",
        "email": "ddd@vvv.com",
        "is_active": True,
    }
    user_data_3 = {
        "user_id": uuid4(),
        "name": "Bob",
        "surname": "White",
        "email": "ccc@fff.com",
        "is_active": True,
    }
    updated_data = {"name": "Ben", "surname": "Kek", "email": "test@complete.com"}

    for user_data in [user_data_1, user_data_2, user_data_3]:
        await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data_1['user_id']}", data=json.dumps(updated_data)
    )
    assert resp.status_code == 200
    data_from_resp = resp.json()

    assert data_from_resp["updated_user_id"] == str(user_data_1["user_id"])

    user_1 = await get_user_from_database(user_data_1["user_id"])
    data_from_database_user_1 = dict(user_1[0])
    assert data_from_database_user_1["user_id"] == user_data_1["user_id"]
    assert data_from_database_user_1["name"] == updated_data["name"]
    assert data_from_database_user_1["surname"] == updated_data["surname"]
    assert data_from_database_user_1["email"] == updated_data["email"]
    assert data_from_database_user_1["is_active"] == user_data_1["is_active"]

    user_2 = await get_user_from_database(user_data_2["user_id"])
    data_from_database_user_2 = dict(user_2[0])
    assert data_from_database_user_2["user_id"] == user_data_2["user_id"]
    assert data_from_database_user_2["name"] == user_data_2["name"]
    assert data_from_database_user_2["surname"] == user_data_2["surname"]
    assert data_from_database_user_2["email"] == user_data_2["email"]
    assert data_from_database_user_2["is_active"] == user_data_2["is_active"]

    user_3 = await get_user_from_database(user_data_3["user_id"])
    data_from_database_user_3 = dict(user_3[0])
    assert data_from_database_user_3["user_id"] == user_data_3["user_id"]
    assert data_from_database_user_3["name"] == user_data_3["name"]
    assert data_from_database_user_3["surname"] == user_data_3["surname"]
    assert data_from_database_user_3["email"] == user_data_3["email"]
    assert data_from_database_user_3["is_active"] == user_data_3["is_active"]
