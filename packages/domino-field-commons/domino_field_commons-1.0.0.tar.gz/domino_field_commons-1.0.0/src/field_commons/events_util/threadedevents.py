from kubernetes import client, config  # type: ignore
from kubernetes.client.models import (  # type: ignore
    V1ObjectReference,
    V1ObjectMeta,
    CoreV1Event,
)
from datetime import datetime
from os import getenv
from time import sleep
import threading
import logging
import pytz
from dataclasses import dataclass, asdict


@dataclass(unsafe_hash=True)
class EventThread(threading.Thread):
    reporting_component: str
    reporting_instance: str
    reporting_ns: str
    event_message: str
    event_reason: str
    event_type: str
    action: str
    owner_name: str
    owner_ns: str
    owner_kind: str

    def __post_init__(self):
        super().__init__(
            group=None, target=None, name=self.reporting_component
        )
        return

    def run(self):
        logging.debug(f"running event handler with {asdict(self)}")
        self._generate_event()
        return

    def _generate_event(self):

        # Context dependent delay
        # e.g. time enough for k8s api to get a mutation response
        sleep(int(getenv("EVENT_LAG_SECONDS", 0)))
        logger = logging.getLogger("events_util")
        try:
            config.load_incluster_config()
        except Exception:
            print("Loading local k8s config")
            config.load_kube_config()

        event = client.CoreV1Api()

        meta = V1ObjectMeta(
            generate_name=self.reporting_component + "-event-",
            namespace=self.reporting_ns,
        )

        involved_reference = V1ObjectReference(
            name=self.owner_name,
            namespace=self.owner_ns if self.owner_ns else self.reporting_ns,
            kind=self.owner_kind,
        )

        # Max msg length is 1024, so string is truncated if it is longer
        event_body = CoreV1Event(
            api_version="v1",
            kind="Event",
            type=self.event_type,
            reporting_component=self.reporting_component,
            reporting_instance=self.reporting_instance,
            metadata=meta,
            action=self.action,
            event_time=datetime.now(pytz.utc),
            first_timestamp=datetime.now(pytz.utc),
            message=(
                (self.event_message[:1022] + "..")
                if len(self.event_message) > 1024
                else self.event_message
            ),
            reason=self.event_reason,
            involved_object=involved_reference,
        )
        logger.info(
            f"Adding k8s event for {involved_reference.kind} "
            f"{involved_reference.name}"
        )
        logger.debug(f"Creating event: {str(event_body)}")

        event.create_namespaced_event(
            namespace=self.reporting_ns, body=event_body
        )
