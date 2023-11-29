class Graphql:
    @staticmethod
    def add(account_id: str, preference: str, name: str) -> str:
        return (
            """mutation {
                alertsPolicyCreate(accountId: """
            + account_id
            + """, policy: {
                    name: \""""
            + name
            + """\"
                    incidentPreference: """
            + preference
            + """
                }) {
                    id
                    name
                    incidentPreference
                }
            }"""
        )

    @staticmethod
    def list(account_id: str) -> str:
        return (
            """
        {
            actor {
                account(id: """
            + account_id
            + """) {
                    alerts {
                        policiesSearch {
                            policies {
                                id
                                name
                                incidentPreference
                            }
                        }
                    }
                }
            }
        }
        """
        )

    @staticmethod
    def update(
        account_id: str,
        policy_id: str,
        name: str,
        preference: str,
    ) -> str:
        return (
            """mutation {
        alertsPolicyUpdate(accountId: """
            + account_id
            + """, id: """
            + policy_id
            + """, policy: {
                name: \""""
            + name
            + """\"
                incidentPreference: """
            + preference
            + """
        }) {
            id
            name
            incidentPreference
            }
        }
        """
        )

    @staticmethod
    def delete(
        account_id: str,
        policy_id: str,
    ) -> str:
        return (
            """
            mutation {
                alertsPolicyDelete(accountId: """
            + account_id
            + """, id: """
            + policy_id
            + """) {
                    id
                }
            }
            """
        )
