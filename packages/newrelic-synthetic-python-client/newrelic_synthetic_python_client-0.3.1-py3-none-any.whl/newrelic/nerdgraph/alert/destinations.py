class Graphql:
    @staticmethod
    def list(account_id: str) -> str:
        return (
            """
            {
            actor {
                account(id: """
            + account_id
            + """) {
                    aiNotifications {
                        destinations(filters: {type: EMAIL}) {
                            entities {
                                id
                                name
                                }
                            totalCount
                            }
                        }
                    }
                }
            }
            """
        )

    @staticmethod
    def add(account_id: str, email: str, **kwargs) -> str:
        return (
            """
            mutation {
                aiNotificationsCreateDestination(accountId: """
            + account_id
            + """, destination: {
                    type: EMAIL,
                    name: "Destination Name",
                    properties: [
                    {
                        key: "email",
                        value: \""""
            + email
            + """\"
                    }
                    ]
                }) {
                    destination {
                    id
                    name
                    }
                }
            }

        """
        )

    @staticmethod
    def update(
        account_id: str,
        destination_id: str,
        name: str,
        **kwargs,
    ) -> str:
        return (
            """
            mutation {
                aiNotificationsUpdateDestination(accountId: """
            + account_id
            + """, destinationId: \""""
            + destination_id
            + """\", destination: {
                    name: \""""
            + name
            + """\"
                }) {
                    destination {
                        id
                        name
                    }
                }
            }
            """
        )

    @staticmethod
    def delete(
        account_id: str,
        destination_id: str,
    ) -> str:
        return (
            """
            mutation {
                aiNotificationsDeleteDestination(accountId: """
            + account_id
            + """, destinationId: \""""
            + destination_id
            + """\") {
                    ids
                    error {
                    details
                    }
                }
            }
            """
        )
