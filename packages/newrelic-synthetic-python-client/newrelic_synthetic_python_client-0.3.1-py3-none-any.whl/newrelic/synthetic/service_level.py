from typing import Dict

from newrelic.nerdgraph.client import NewRelicModule
from newrelic.nerdgraph.synthetic import service_level
from newrelic.synthetic.scripted_browser import (
    ScriptedBrowserMonitors,
)


class ServiceLevel(NewRelicModule):
    def list(self, **kwargs) -> Dict:
        guid = ScriptedBrowserMonitors(self.client).find_by_name(
            monitor_name=kwargs["monitor_name"]
        )["guid"]
        graphql = service_level.Graphql.list(guid)
        return self.client.request(ql=graphql).json()

    def find_by_name(self, service_level_name: str, **kwargs) -> Dict:
        service_level = self.list(**kwargs)
        search = filter(
            lambda x: x["name"] == service_level_name,
            service_level["data"]["actor"]["entity"]["serviceLevel"][
                "indicators"
            ],
        )
        return next(search)

    def add(
        self,
        **kwargs,
    ) -> Dict:
        guid = ScriptedBrowserMonitors(self.client).find_by_name(
            monitor_name=kwargs["monitor_name"]
        )["guid"]
        graphql = service_level.Graphql.add(
            guid, name=kwargs["name"], account_id=self.client.account_id
        )
        return self.client.request(ql=graphql).json()

    def update(
        self,
        **kwargs,
    ) -> Dict:
        graphql = service_level.Graphql.update(**kwargs)
        return self.client.request(ql=graphql).json()
