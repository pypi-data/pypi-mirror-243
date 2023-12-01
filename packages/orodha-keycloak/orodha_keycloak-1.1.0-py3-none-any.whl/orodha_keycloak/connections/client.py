"""
This Module contains a function which provides a keycloak connection
set up as a non privileged user for our main class.
"""
from keycloak import KeycloakOpenID


def create_client_connection(server_url: str, realm_name: str, client_id: str, client_secret_key: str):
    """
    Creates and returns keycloak admin connection with given args

    Args:
        server_url(str): Url of the keycloak server.
        realm_name(str): The name of the keycloak realm that we are attempting to access.
        client_id(str): The keycloak client_id that we are using for the connection.
        client_secret_key(str): The secret key of the keycloak client.

    Returns:
        client_connection: This object is what holds our connection to the keycloak client, through this
            we are able to interact with decoding mechanisms for our jwt tokens.
    """

    client_connection = KeycloakOpenID(
        server_url=server_url,
        client_id=client_id,
        realm_name=realm_name,
        client_secret_key=client_secret_key,
        verify=True,
    )
    return client_connection
