from typing import Dict

from newrelic.nerdgraph.client import NewRelicModule
from newrelic.nerdgraph.alert import workflows


class Workflows(NewRelicModule):
    def list(self, **kwargs) -> Dict:
        graphql = workflows.Graphql.list(self.client.account_id, **kwargs)
        return self.client.request(ql=graphql).json()

    def add(
        self,
        **kwargs,
    ) -> Dict:
        graphql = workflows.Graphql.add(self.client.account_id, **kwargs)
        return self.client.request(ql=graphql).json()

    def delete(
        self,
        **kwargs,
    ) -> Dict:
        graphql = workflows.Graphql.delete(self.client.account_id, **kwargs)
        return self.client.request(ql=graphql).json()

    def update(
        self,
        **kwargs,
    ) -> Dict:
        graphql = workflows.Graphql.update(self.client.account_id, **kwargs)
        return self.client.request(ql=graphql).json()
