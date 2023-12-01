import os
import pytest
from orodha_keycloak import OrodhaKeycloakClient, OrodhaCredentials
from orodha_keycloak.exceptions import InvalidConnectionException
from tests.conftest import MockEnvironment
from tests.fixtures.keycloak import MOCK_DATA

CONNECTION_ARGS = MOCK_DATA.get("connection_args")


def test_kwarg_credentials_with_password():
    credentials = OrodhaCredentials(
        client_server=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"],
        realm_name=CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"],
        client_id=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"],
        username=CONNECTION_ARGS["ORODHA_KEYCLOAK_USERNAME"],
        password=CONNECTION_ARGS["ORODHA_KEYCLOAK_PASSWORD"],
    )

    assert credentials.server_url == CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"]
    assert credentials.realm_name == CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"]
    assert credentials.client_id == CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"]
    assert credentials.username == CONNECTION_ARGS["ORODHA_KEYCLOAK_USERNAME"]
    assert credentials.password == CONNECTION_ARGS["ORODHA_KEYCLOAK_PASSWORD"]
    assert credentials.secret_key_available is False


def test_kwarg_credentials_with_secret_key():
    credentials = OrodhaCredentials(
        client_server=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"],
        realm_name=CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"],
        client_id=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"],
        client_secret_key=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SECRET_KEY"]
    )

    assert credentials.server_url == CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"]
    assert credentials.realm_name == CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"]
    assert credentials.client_id == CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"]
    assert credentials.client_secret_key == CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SECRET_KEY"]
    assert credentials.secret_key_available is True


def test_environment_credentials_with_password():
    arg_dict = {
        "ORODHA_KEYCLOAK_CLIENT_SERVER": CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"],
        "ORODHA_KEYCLOAK_REALM_NAME": CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"],
        "ORODHA_KEYCLOAK_CLIENT_ID": CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"],
        "ORODHA_KEYCLOAK_USERNAME": CONNECTION_ARGS["ORODHA_KEYCLOAK_USERNAME"],
        "ORODHA_KEYCLOAK_PASSWORD": CONNECTION_ARGS["ORODHA_KEYCLOAK_PASSWORD"]
    }

    with MockEnvironment(**arg_dict):
        credentials = OrodhaCredentials()

    assert credentials.server_url == CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"]
    assert credentials.realm_name == CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"]
    assert credentials.client_id == CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"]
    assert credentials.username == CONNECTION_ARGS["ORODHA_KEYCLOAK_USERNAME"]
    assert credentials.password == CONNECTION_ARGS["ORODHA_KEYCLOAK_PASSWORD"]
    assert credentials.secret_key_available is False


def test_environment_credentials_with_secret_key():
    arg_dict = {
        "ORODHA_KEYCLOAK_CLIENT_SERVER": CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"],
        "ORODHA_KEYCLOAK_REALM_NAME": CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"],
        "ORODHA_KEYCLOAK_CLIENT_ID": CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"],
        "ORODHA_KEYCLOAK_CLIENT_SECRET_KEY": CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SECRET_KEY"]
    }

    with MockEnvironment(**arg_dict):
        credentials = OrodhaCredentials()

    assert credentials.server_url == CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"]
    assert credentials.realm_name == CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"]
    assert credentials.client_id == CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"]
    assert credentials.client_secret_key == CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SECRET_KEY"]
    assert credentials.secret_key_available is True


def test_credentials_missing_required_args():
    with pytest.raises(InvalidConnectionException):
        OrodhaCredentials(
            client_id=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"],
            client_secret_key=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SECRET_KEY"]
        )


def test_credentials_no_credential_values():
    with pytest.raises(InvalidConnectionException):
        OrodhaCredentials(
            server_url=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"],
            realm_name=CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"],
            client_id=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"],
        )


def test_add_user_with_secret_key(
    mock_create_admin_connection,
    mock_create_client_connection
):
    user_request_args = MOCK_DATA.get("add_user_request")

    connection = OrodhaKeycloakClient(
        server_url=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"],
        realm_name=CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"],
        client_id=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"],
        client_secret_key=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SECRET_KEY"]
    )
    response = connection.add_user(
        email=user_request_args['email'],
        username=user_request_args['username'],
        firstName=user_request_args['firstName'],
        lastName=user_request_args['lastName'],
        password=user_request_args['credentials'][0]["value"]
    )
    assert response == MOCK_DATA.get("add_user_response")


def test_add_user_with_password(
    mock_create_admin_connection,
    mock_create_client_connection
):
    user_request_args = MOCK_DATA.get("add_user_request")

    connection = OrodhaKeycloakClient(
        server_url=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"],
        realm_name=CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"],
        client_id=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"],
        password=CONNECTION_ARGS["ORODHA_KEYCLOAK_USERNAME"],
        username=CONNECTION_ARGS["ORODHA_KEYCLOAK_PASSWORD"],
    )
    response = connection.add_user(
        email=user_request_args['email'],
        username=user_request_args['username'],
        firstName=user_request_args['firstName'],
        lastName=user_request_args['lastName'],
        password=user_request_args['credentials'][0]["value"]
    )
    assert response == MOCK_DATA.get("add_user_response")


def test_delete_user(
    mock_create_admin_connection,
    mock_create_client_connection
):
    connection = OrodhaKeycloakClient(
        server_url=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"],
        username=CONNECTION_ARGS["ORODHA_KEYCLOAK_USERNAME"],
        password=CONNECTION_ARGS["ORODHA_KEYCLOAK_PASSWORD"],
        realm_name=CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"],
        client_id=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"],
        client_secret_key=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SECRET_KEY"]
    )

    response = connection.delete_user("someid")
    assert response == MOCK_DATA.get("delete_user_response")


def test_get_user_with_token(
    mock_create_client_connection,
    mock_create_admin_connection
):
    connection = OrodhaKeycloakClient(
        server_url=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"],
        realm_name=CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"],
        client_id=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"],
        client_secret_key=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SECRET_KEY"]
    )
    user = connection.get_user(token={"access_token": "data"})

    assert user == MOCK_DATA["get_user_response"]


def test_get_user_with_id(
    mock_create_client_connection,
    mock_create_admin_connection
):
    connection = OrodhaKeycloakClient(
        server_url=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SERVER"],
        username=CONNECTION_ARGS["ORODHA_KEYCLOAK_USERNAME"],
        password=CONNECTION_ARGS["ORODHA_KEYCLOAK_PASSWORD"],
        realm_name=CONNECTION_ARGS["ORODHA_KEYCLOAK_REALM_NAME"],
        client_id=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_ID"],
        client_secret_key=CONNECTION_ARGS["ORODHA_KEYCLOAK_CLIENT_SECRET_KEY"]
    )
    user = connection.get_user(user_id="someid")

    assert user == MOCK_DATA["get_user_response"]
