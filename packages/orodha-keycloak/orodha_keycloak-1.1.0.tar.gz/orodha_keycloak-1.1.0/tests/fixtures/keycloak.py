MOCK_DATA = {
    "add_user_request":
        {
            "email": "email@example.com",
            "username": "myuser",
            "firstName": "John",
            "lastName": "Doe",
            "credentials": [
                {
                        "value": "password",
                        "type": "password",
                }
            ],
        },
    "add_user_response": {
        "user_data": {
            "some_data": None
        },
        "code": 200
        },
    "delete_user_response": {
        "message": "user_deleted",
        "code": 200
        },
    "connection_args":
        {
            "ORODHA_KEYCLOAK_CLIENT_SERVER": "someurl/",
            "ORODHA_KEYCLOAK_REALM_NAME": "somerealm",
            "ORODHA_KEYCLOAK_CLIENT_ID": "clientID",
            "ORODHA_KEYCLOAK_CLIENT_SECRET_KEY": "secretkey",
            "ORODHA_KEYCLOAK_USERNAME": "someusername",
            "ORODHA_KEYCLOAK_PASSWORD": "somepassword",
        },
        "mock_public_key": "somemockpublickeyvalue",
        "mock_decoded_token": {"some_info": 100, "user_id": "some_user_id"},
        "get_user_response": {
            "email": "email@example.com",
            "username": "myuser",
            "firstName": "John",
            "lastName": "Doe",
            "credentials": [
                {
                        "value": "password",
                        "type": "password",
                }
            ],
        },
}
