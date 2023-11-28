from typing import Dict

from newrelic.nerdgraph.client import NewRelicModule
from newrelic.nerdgraph.alert import channels


class Channels(NewRelicModule):
    def list(self) -> Dict:
        graphql = channels.Graphql.list(self.client.account_id)
        return self.client.request(ql=graphql).json()

    def add(
        self,
        **kwargs,
    ) -> Dict:
        graphql = channels.Graphql.add(self.client.account_id, **kwargs)
        return self.client.request(ql=graphql).json()

    def update(
        self,
        **kwargs,
    ) -> Dict:
        graphql = channels.Graphql.update(self.client.account_id, **kwargs)
        return self.client.request(ql=graphql).json()

    def delete(
        self,
        **kwargs,
    ) -> Dict:
        graphql = channels.Graphql.delete(self.client.account_id, **kwargs)
        return self.client.request(ql=graphql).json()
