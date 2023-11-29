from newrelic.nerdgraph.client import NerdGraphClient
from newrelic.alert.policy import Policy
from newrelic.alert.condition import Condition
from newrelic.alert.destinations import Destinations
from newrelic.alert.channels import Channels
from newrelic.alert.workflows import Workflows


class Alert:
    def __init__(self, client: NerdGraphClient) -> None:
        self.client = client
        self._policy = None
        self._condition = None
        self._destinations = None
        self._channels = None
        self._workflows = None

    @property
    def policy(self):
        if self._policy is None:
            self._policy = Policy(client=self.client)
        return self._policy

    @property
    def condition(self):
        if self._condition is None:
            self._condition = Condition(client=self.client)
        return self._condition

    @property
    def destinations(self):
        if self._destinations is None:
            self._destinations = Destinations(client=self.client)
        return self._destinations

    @property
    def channels(self):
        if self._channels is None:
            self._channels = Channels(client=self.client)
        return self._channels

    @property
    def workflows(self):
        if self._workflows is None:
            self._workflows = Workflows(client=self.client)
        return self._workflows
