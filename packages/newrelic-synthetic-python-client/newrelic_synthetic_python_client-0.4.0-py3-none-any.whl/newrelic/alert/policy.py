from typing import Dict

from newrelic.nerdgraph.client import NewRelicModule
from newrelic.nerdgraph.alert import policy


class Policy(NewRelicModule):
    def list(self) -> Dict:
        graphql = policy.Graphql.list(self.client.account_id)
        return self.client.request(ql=graphql).json()

    def add(
        self,
        preference: str,
        name: str,
        **kwargs,
    ) -> Dict:
        graphql = policy.Graphql.add(
            self.client.account_id, preference, name
        )
        return self.client.request(ql=graphql).json()

    def delete(
        self,
        policy_id: str,
        **kwargs,
    ) -> Dict:
        graphql = policy.Graphql.delete(
            self.client.account_id, policy_id
        )
        return self.client.request(ql=graphql).json()

    def update(
        self,
        policy_id: str,
        name: str,
        preference: str,
        **kwargs,
    ) -> Dict:
        graphql = policy.Graphql.update(
            self.client.account_id, policy_id, name, preference
        )
        return self.client.request(ql=graphql).json()
