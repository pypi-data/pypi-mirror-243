from typing import Dict

from newrelic.nerdgraph.client import NewRelicModule
from newrelic.nerdgraph.alert import destinations


class Destinations(NewRelicModule):
    def list(self) -> Dict:
        graphql = destinations.Graphql.list(self.client.account_id)
        return self.client.request(ql=graphql).json()

    def add(
        self,
        **kwargs,
    ) -> Dict:
        graphql = destinations.Graphql.add(self.client.account_id, **kwargs)
        return self.client.request(ql=graphql).json()

    def delete(
        self,
        destination_id: str,
        **kwargs,
    ) -> Dict:
        graphql = destinations.Graphql.delete(self.client.account_id, destination_id)
        return self.client.request(ql=graphql).json()

    def update(
        self,
        destination_id: str,
        name: str,
        **kwargs,
    ) -> Dict:
        graphql = destinations.Graphql.update(self.client.account_id, destination_id, name, **kwargs)

        return self.client.request(ql=graphql).json()
