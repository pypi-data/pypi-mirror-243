
# Common utility APIs

## events_util
This package contains methods to log k8s events that will be displayed in the pod logs. This is very useful during validations and mutations. To introduce a delay before the event is logged, set the environment variable, EVENT_LAG_SECONDS. Delays are useful for e.g. when an object is mutated and it takes a small bit of time for kubernetes to receive the response.

export EVENT_LAG_SECONDS=2 (or any value >= 0 if needed)

events_util.**log_event**(reporting_component,
    reporting_instance,
    reporting_ns,
    event_message,
    event_reason="Unspecified",
    event_type="Normal",
    action="Unspecified",
    owner_name=None,
    owner_ns=None,
    owner_kind=None,)

* reporting_component: "domsed",
* reporting_instance: getenv("POD_NAME")
* reporting_ns: Namespace of the reporting_instance
* event_message: "Some message truncated after 1024 chars"
* event_reason: "Started","Scheduled", "Pulled" etc.
* event_type: "Normal", "Urgent" etc.
* action: "Mutation", "Validation" etc.
* owner_name: e.g. the name of the Deployment or higher level object that spawned this pod
* owner_ns: the corresponding namespace (must match the reporting_ns above)
* owner_kind: Deployment etc. 

## mongo_util
This package contains methods to create a connection to the Mongo DB.

mongo_util.**create_database_connection**(
    username,
    password,
    host=None,
    platform_namespace,
    db_name,
)

* username: 
* password: 
* host: uses default port of 27017
* platform_namespace:
* db_name:

mongo_util.**MONGO_DATABASE**
Creates a database connection using environment variablesas parameters to the create functions above

* username: quote_plus(os.environ.get("MONGO_USERNAME", "admin"))
* password: quote_plus(os.environ["MONGO_PASSWORD"])
* host: os.environ.get("MONGO_HOST", None)
* platform_namespace=os.environ.get("PLATFORM_NAMESPACE", "domino-platform")
* db_name=quote_plus(os.environ.get("MONGO_DB_NAME", "domino"))

## keycloak_util
This package contains methods to create a connection to the keycloak service

keycloak_util.**create_keycloak_connection**(username, password, host)

* username: 
* password: 
* host:

keycloak_util.**KEYCLOAK_CONNECTION**
Creates a keycloak connection using environment variablesas parameters to the create functions above

* username: os.getenv("KEYCLOAK_USERNAME", "keycloak")
* password: os.getenv("KEYCLOAK_PASSWORD")
* host: os.getenv("KEYCLOAK_HOST")

## Build, deployment and usage

```
python3 -m pip install build
python3 -m pip install python-keycloak
python3 -m pip install pymongo

cd /path/to/domino-field-commons
python3 -m build
python -m pip install .

from field_commons import events_util
events_util.log_event("domsed","nucleus-frontend-8569bf6b8-7w9l5","domino-platform","Log a test event")

from field_commons.keycloak_util import KEYCLOAK_CONNECTION as kc
kc.create_user({"email": "example@example.com",
                "username": "example@example.com",
                "enabled": True,
                "firstName": "Example",
                "lastName": "Example"})

from field_commons.mongo_util import MONGO_DATABASE as md
md.runs.find_one(...)
```



