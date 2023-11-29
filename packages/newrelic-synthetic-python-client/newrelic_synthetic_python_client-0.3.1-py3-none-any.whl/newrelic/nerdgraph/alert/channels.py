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
                    channels(filters: {type: EMAIL}) {
                        entities {
                            id
                            name
                            product
                            }
                        }
                    }
                }
            }
            }
            """
        )

    @staticmethod
    def add(account_id: str, **kwargs) -> str:
        return (
            """
        mutation {
            aiNotificationsCreateChannel(accountId: """
            + account_id
            + """, channel: {
                type: EMAIL,
                name: \""""
            + kwargs["name"]
            + """\",
                destinationId: \""""
            + kwargs["destination_id"]
            + """\",
                product: """
            + kwargs["product"]
            + """,
                properties: []
            }) {
                channel {
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
        **kwargs,
    ) -> str:
        return (
            """
            mutation {
                aiNotificationsUpdateChannel(accountId: """
            + account_id
            + """, channelId: \""""
            + kwargs["channel_id"]
            + """\", channel: {
                    name: \""""
            + kwargs["name"]
            + """\"
                }) {
                    channel {
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
        **kwargs,
    ) -> str:
        return (
            """
            mutation {
                aiNotificationsDeleteChannel(accountId: """
            + account_id
            + """, channelId: \""""
            + kwargs["channel_id"]
            + """\") {
                    ids
                    error {
                    details
                    }
                }
            }
            """
        )
