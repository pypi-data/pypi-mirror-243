from typing import Dict

from newrelic.nerdgraph.client import NewRelicModule
from newrelic.nerdgraph.alert import condition


class Condition(NewRelicModule):
    def list(self) -> Dict:
        graphql = condition.Graphql.list(self.client.account_id)
        return self.client.request(ql=graphql).json()

    def add(
        self,
        type_: str,
        **kwargs,
    ) -> Dict:
        conditions = {
            "baseline": condition.Graphql.add_baseline,
            "static": condition.Graphql.add_static,
        }

        graphql = conditions[type_](self.client.account_id, **kwargs)
        return self.client.request(ql=graphql).json()

    def update(
        self,
        condition_id: str,
        type_: str,
        **kwargs,
    ) -> Dict:

        conditions = {
            "baseline": condition.Graphql.update_baseline,
            "static": condition.Graphql.update_static,
        }
        graphql = conditions[type_](self.client.account_id, condition_id, **kwargs)
        return self.client.request(ql=graphql).json()

    def delete(
        self,
        condition_id: str,
        **kwargs,
    ) -> Dict:
        graphql = condition.Graphql.delete(self.client.account_id, condition_id)
        return self.client.request(ql=graphql).json()
