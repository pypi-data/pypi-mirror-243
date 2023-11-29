class Graphql:
    @staticmethod
    def add(account_id: str, **kwargs) -> str:
        return (
            """
            mutation {
            aiWorkflowsCreateWorkflow(accountId: """
            + account_id
            + """, createWorkflowData: {
                destinationsEnabled: true, workflowEnabled: true, name: \""""
            + kwargs["name"]
            + """\",
                issuesFilter: {
                    name: "team specific issues",
                    predicates: 
                        [{
                            attribute: \""""
            + kwargs["attribute"]
            + """\",
                            operator: """
            + kwargs["operator"]
            + """,
                            values:[
                                \""""
            + kwargs["policy_id"]
            + """\"
                            ]
                        }], 
                        type: FILTER
                    }, 
                    destinationConfigurations: {
                        channelId: \""""
            + kwargs["channel_id"]
            + """\"
                        },
                        enrichmentsEnabled: true, enrichments: {nrql: []},
                        , mutingRulesHandling: DONT_NOTIFY_FULLY_MUTED_ISSUES}) {
                    workflow {
                    id
                    name
                    destinationConfigurations {
                        channelId
                        name
                        type
                    }
                    enrichmentsEnabled
                    destinationsEnabled
                    issuesFilter {
                        accountId
                        id
                        name
                        predicates {
                        attribute
                        operator
                        values
                        }
                        type
                    }
                    lastRun
                    workflowEnabled
                    mutingRulesHandling
                    }
                    errors {
                    description
                    type
                    }
                }
            }
            """
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
                aiWorkflows {
                    workflows(filters: {destinationType: EMAIL}) {
                    entities {
                        id
                        name
                        destinationConfigurations {
                        type
                        }
                        }
                        nextCursor
                        totalCount
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
        **kwargs,
    ) -> str:
        return (
            """
            mutation {
                aiWorkflowsUpdateWorkflow(
                    accountId: """
            + account_id
            + """
                    updateWorkflowData: {
                        name: \""""+kwargs["name"]+"""\",
                        id: \""""+kwargs["workflow_id"]+"""\"
                    }
                ) {
                    workflow {
                    id
                    name
                    destinationConfigurations {
                        channelId
                        name
                        type
                    }
                    enrichmentsEnabled
                    destinationsEnabled
                    issuesFilter {
                        accountId
                        id
                        name
                        predicates {
                        attribute
                        operator
                        values
                        }
                        type
                    }
                    lastRun
                    workflowEnabled
                    mutingRulesHandling
                    }
                    errors {
                    description
                    type
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
                aiWorkflowsDeleteWorkflow(id: \""""
            + kwargs["workflow_id"]
            + """\", accountId: """
            + account_id
            + """) {
                    id
                    errors {
                    description
                    type
                    }
                }
            }
            """
        )
