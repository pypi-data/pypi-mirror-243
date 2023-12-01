"""
This Module contains a function which provides a keycloak connection
set up as an admin for our main class.
"""
from keycloak import KeycloakAdmin, KeycloakOpenIDConnection


def create_admin_connection(
    server_url: str,
    realm_name: str,
    client_id: str,
    client_secret_key: str = None,
    username: str = None,
    password: str = None
):
    """
    Creates and returns keycloak admin connection with given args

    Args:
        server_url(str): The url of the server that our keycloak is hosted at
        realm_name(str): The name of the keycloak realm that we are attempting to access.
        client_id(str): The keycloak client_id that we are using for the connection.
        client_secret_key(str): The secret key of the keycloak client.
        username(str) - Optional: The username of the user being impersonated by python-keycloak
        password(str) - Optional: The password of the user being impersonated by python-keycloak

    Returns:
        keycloak_admin: This object is what holds our connection to the keycloak admin, through this
            we are able to manipulate users and other data depending on the keycloak permissions.
    """
    if client_secret_key:
        keycloak_connection = KeycloakOpenIDConnection(
            server_url=server_url,
            realm_name=realm_name,
            client_id=client_id,
            client_secret_key=client_secret_key,
            verify=True,
        )
    else:
        keycloak_connection = KeycloakOpenIDConnection(
            server_url=server_url,
            realm_name=realm_name,
            username=username,
            password=password
        )
    keycloak_admin = KeycloakAdmin(connection=keycloak_connection)
    return keycloak_admin
