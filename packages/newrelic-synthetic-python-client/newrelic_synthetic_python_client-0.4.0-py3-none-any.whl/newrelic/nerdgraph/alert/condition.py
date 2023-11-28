class Graphql:
    @staticmethod
    def add_baseline(account_id: str, **kwargs) -> str:
        return (
            """mutation {
                    alertsNrqlConditionBaselineCreate(accountId: """
            + account_id
            + """, policyId: """
            + kwargs["policy_id"]
            + """, condition: {
                        name: \""""
            + kwargs["name"]
            + """\"
                        baselineDirection: """
            + kwargs["direction"]
            + """   
                        enabled: true
                        nrql: { query: \""""
            + kwargs["nrql"]
            + """\"
                    }
                        signal: {
                    aggregationWindow: """
            + kwargs["window_duration"]
            + """
                    aggregationMethod: """
            + kwargs["streaming_method"]
            + """
                    aggregationDelay: """
            + kwargs["delay"]
            + """
                }
                terms: {
                    threshold: """
            + kwargs["threshold"]
            + """
                    thresholdDuration: """
            + kwargs["threshold_duration"]
            + """
                    thresholdOccurrences: """
            + kwargs["threshold_occurrences"]
            + """
                    operator: """
            + kwargs["operator"]
            + """
                    priority: """
            + kwargs["priority"]
            + """
                }
                        violationTimeLimitSeconds: """
            + kwargs["violation_time"]
            + """
                        }) {
                        id
                        name
                        baselineDirection
                    }
                }
            """
        )

    @staticmethod
    def add_static(account_id: str, **kwargs) -> str:
        return (
            """mutation {
                    alertsNrqlConditionStaticCreate(accountId: """
            + account_id
            + """, policyId: """
            + kwargs["policy_id"]
            + """, condition: {
                        name: \""""
            + kwargs["name"]
            + """\"
                        enabled: true
                        nrql: { query: \""""
            + kwargs["nrql"]
            + """\"
                    }
                        signal: {
                    aggregationWindow: """
            + kwargs["window_duration"]
            + """
                    aggregationMethod: """
            + kwargs["streaming_method"]
            + """
                    aggregationDelay: """
            + kwargs["delay"]
            + """
                }
                terms: {
                    threshold: """
            + kwargs["threshold"]
            + """
                    thresholdDuration: """
            + kwargs["threshold_duration"]
            + """
                    thresholdOccurrences: """
            + kwargs["threshold_occurrences"]
            + """
                    operator: """
            + kwargs["operator"]
            + """
                    priority: """
            + kwargs["priority"]
            + """
                }
                        valueFunction: SINGLE_VALUE
                        violationTimeLimitSeconds: """
            + kwargs["violation_time"]
            + """
                        }) {
                        id
                        name
                    }
                }
            """
        )

    @staticmethod
    def list(account_id) -> str:
        return (
            """
        {
            actor {
                account(id: """
            + account_id
            + """) {
                    alerts {
                        nrqlConditionsSearch {
                            nextCursor
                            nrqlConditions {
                                id
                                name
                                type
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
    def update_static(
        account_id: str,
        condition_id: str,
        **kwargs,
    ) -> str:
        return (
            """ mutation {
                    alertsNrqlConditionStaticUpdate(accountId: """
            + account_id
            + """, id: """
            + condition_id
            + """, condition: {
                    name: \""""
            + kwargs["name"]
            + """\"
                    nrql: { query: \""""
            + kwargs["nrql"]
            + """\"
                    }
                    signal: {
                    aggregationWindow: """
            + kwargs["window_duration"]
            + """
                    aggregationMethod: """
            + kwargs["streaming_method"]
            + """
                    aggregationDelay: """
            + kwargs["delay"]
            + """
                }
                terms: {
                    threshold: """
            + kwargs["threshold"]
            + """
                    thresholdDuration: """
            + kwargs["threshold_duration"]
            + """
                    thresholdOccurrences: """
            + kwargs["threshold_occurrences"]
            + """
                    operator: """
            + kwargs["operator"]
            + """
                    priority: """
            + kwargs["priority"]
            + """
                }
                        valueFunction: SINGLE_VALUE
                        violationTimeLimitSeconds: """
            + kwargs["violation_time"]
            + """
                    }) {
                            id
                            name
                        }
                    }
            """
        )

    @staticmethod
    def update_baseline(
        account_id: str,
        condition_id: str,
        **kwargs,
    ) -> str:
        return (
            """mutation {
                    alertsNrqlConditionBaselineUpdate(accountId: """
            + account_id
            + """, id: """
            + condition_id
            + """, condition: {
                        name: \""""
            + kwargs["name"]
            + """\"
                        baselineDirection: """
            + kwargs["direction"]
            + """   
                        enabled: true
                        nrql: { query: \""""
            + kwargs["nrql"]
            + """\"
                    }
                        signal: {
                    aggregationWindow: """
            + kwargs["window_duration"]
            + """
                    aggregationMethod: """
            + kwargs["streaming_method"]
            + """
                    aggregationDelay: """
            + kwargs["delay"]
            + """
                }
                terms: {
                    threshold: """
            + kwargs["threshold"]
            + """
                    thresholdDuration: """
            + kwargs["threshold_duration"]
            + """
                    thresholdOccurrences: """
            + kwargs["threshold_occurrences"]
            + """
                    operator: """
            + kwargs["operator"]
            + """
                    priority: """
            + kwargs["priority"]
            + """
                }
                        violationTimeLimitSeconds: """
            + kwargs["violation_time"]
            + """
                        }) {
                        id
                        name
                        baselineDirection
                    }
                }
            """
        )

    @staticmethod
    def delete(
        account_id: str,
        condition_id: str,
    ) -> str:
        return (
            """
        mutation {
                alertsConditionDelete(accountId: """
            + account_id
            + """, id: """
            + condition_id
            + """) {
                        id
                }
        }
        """
        )
