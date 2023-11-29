__all__ = ["create_keycloak_connection", "KEYCLOAK_CONNECTION"]

import logging
import os
from keycloak import KeycloakAdmin  # type: ignore

logger = logging.getLogger(__name__)


def create_keycloak_connection(username, password, host):
    if not (host and username and password):
        return []

    keycloak_server = f'http://{host}/auth/'

    admin_connection = KeycloakAdmin(
        server_url=keycloak_server,
        username=username,
        password=password,
        realm_name="DominoRealm",
        user_realm_name="master",
        verify=True,
    )

    return admin_connection


KEYCLOAK_CONNECTION = create_keycloak_connection(
    username=os.getenv("KEYCLOAK_USERNAME", "keycloak"),
    password=os.getenv("KEYCLOAK_PASSWORD"),
    host=os.getenv("KEYCLOAK_HOST"),
)
