class Graphql:
    @staticmethod
    def list(guid: str) -> str:
        return (
            """
        {
        actor {
            entity(guid: \""""
            + guid
            + """\") {
                guid
                    name
                        serviceLevel {
                            indicators {
                            createdAt
                            createdBy {
                                email
                            }
                            description
                            entityGuid
                            id
                            name
                            guid
                            objectives {
                                target
                                timeWindow {
                                rolling {
                                    count
                                    unit
                                    }
                                }
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
        **kwargs,
    ) -> str:
        return (
            """mutation {
            serviceLevelUpdate(
                id: \""""
            + kwargs["indicators_id"]
            + """\"
                indicator: {
                objectives: {
                    target: """
            + kwargs["target"]
            + """
                    timeWindow: { rolling: { count: """
            + kwargs["count"]
            + """, unit: """
            + kwargs["unit"]
            + """ } }
                }
                }
            ) {
                id
            }
        }
        """
        )

    @staticmethod
    def add(
        guid: str,
        name: str,
        account_id: str,
    ) -> str:
        return (
            """
        mutation {
            serviceLevelCreate(
                entityGuid: \""""
            + guid
            + """\"
                indicator: {
                name: \""""
            + name
            + """\"
                description: "NR PYTHON CLIENT AUTO GENERATED."
                events: {
                    validEvents: { from: "SyntheticCheck", where: "entityGuid = \'"""
            + guid
            + """\'" }
                    goodEvents: {
                    from: "SyntheticCheck"
                    where: "entityGuid = \'"""
            + guid
            + """\' and result='SUCCESS'"
                    }
                    accountId: """
            + account_id
            + """
                }
                objectives: {
                    target: 99.9
                    timeWindow: { rolling: { count: 7, unit: DAY } }
                }
                }
            ) {
                id
                description
            }
        }
        """
        )
