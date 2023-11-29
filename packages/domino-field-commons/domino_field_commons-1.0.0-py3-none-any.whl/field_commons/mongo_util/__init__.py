__all__ = ["create_database_connection", "MONGO_DATABASE"]

import os
import logging
from urllib.parse import quote_plus
from pymongo import MongoClient  # type: ignore

logger = logging.getLogger(__name__)
DEFAULT_PLATFORM_NAMESPACE = "domino-platform"


def create_database_connection(
    username,
    password,
    host=None,
    platform_namespace=DEFAULT_PLATFORM_NAMESPACE,
    db_name="domino",
):
    if not password:
        return []

    host = (
        f"mongodb-replicaset.{platform_namespace}.svc.cluster.local:27017"
        if not host
        else host
    )

    if username == "admin":
        path = ""
    else:
        path = "/{}".format(db_name)
    mongo_uri = "mongodb://{}:{}@{}{}".format(username, password, host, path)
    return MongoClient(mongo_uri)[db_name]


MONGO_DATABASE = create_database_connection(
    username=quote_plus(os.environ.get("MONGO_USERNAME", "admin")),
    password=quote_plus(os.environ.get("MONGO_PASSWORD", "")),
    host=os.environ.get(
        "MONGO_HOST",
        None,
    ),
    platform_namespace=os.environ.get(
        "PLATFORM_NAMESPACE", DEFAULT_PLATFORM_NAMESPACE
    ),
    db_name=quote_plus(os.environ.get("MONGO_DB_NAME", "domino")),
)
