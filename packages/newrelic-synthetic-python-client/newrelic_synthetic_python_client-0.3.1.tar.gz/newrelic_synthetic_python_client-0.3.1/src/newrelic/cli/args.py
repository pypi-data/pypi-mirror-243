from dataclasses import dataclass
import pathlib
from typing import Sequence, Dict, Optional, List
import argparse
import abc

from newrelic.utils.log import log


class Arguments(abc.ABC):
    @abc.abstractmethod
    def to_dict(self) -> Dict:
        pass


@dataclass
class ScriptedBrowserArguments(Arguments):
    """
    Arguments class for the program.
    """

    monitor_name: str = ""
    status: str = "ENABLED"
    locations: str = "US_WEST_2,AP_NORTHEAST_1"
    period: str = "EVERY_15_MINUTES"
    enable_screenshot: bool = True
    script_content: Optional[List[str]] = None

    def to_dict(self) -> Dict:
        script_content = self.script_content
        if script_content is not None:
            script_content = self.merge_content()

        bool_maps = {
            True: "true",
            False: "false"
        }
        return {
            "monitor_name": self.monitor_name,
            "status": self.status.upper(),
            "locations": self.locations.split(",") if self.locations else [],
            "period": self.period.upper(),
            "enable_screenshot": bool_maps[self.enable_screenshot],
            "script_content": script_content,
        }

    def merge_content(self) -> str:
        final_script_content = []
        for script_content in self.script_content:
            assume_file = pathlib.Path(script_content)
            if assume_file.exists():
                log.debug("script content is in a file, reading its content")
                script_content = (
                    (f"{repr(assume_file.read_text())}")
                    .replace('"', '\\"')
                    .strip("'")
                )
            final_script_content.append(script_content)

        return "".join(final_script_content)


def parse_scripted_browser_args(
    command: Sequence[str],
) -> ScriptedBrowserArguments:
    parser = argparse.ArgumentParser(
        description="newrelic client",
    )
    args = ScriptedBrowserArguments()
    parser.add_argument(
        "--monitor-name",
        type=str,
        required=True,
        help="The Synthetic monitor name"
    )
    parser.add_argument(
        "--status",
        type=str,
        default=args.status,
        choices=["enabled", "disabled", "muted"],
        help="Specify the monitor status",
    )
    parser.add_argument(
        "--locations",
        type=str,
        default=args.locations,
        help="Specify the monitor locations, comma separated for multi values",
    )
    parser.add_argument(
        "--period",
        type=str,
        default=args.period,
        help="Specify the monitor period",
    )
    parser.add_argument(
        "--enable-screenshot",
        action="store_true",
        default=args.enable_screenshot,
        help="Whether take screenshot when failure",
    )
    parser.add_argument(
        "--script-content",
        type=str,
        action='append',
        help="The script content or file path",
    )
    parser.parse_args(args=command, namespace=args)
    return _post_scripted_browser_args_hook(args)


def _post_scripted_browser_args_hook(
    args: ScriptedBrowserArguments
) -> ScriptedBrowserArguments:
    """
    Extra validations for the arguments.
    """
    return args


@dataclass
class SecureCredentialArguments(Arguments):
    key: str = ""
    value: str = ""
    description: str = "NR PYTHON CLIENT AUTO GENERATED"

    def to_dict(self) -> Dict:
        return {
            "key": self.key,
            "value": self.value,
            "description": self.description
        }


def parse_secure_credential_args(
    command: Sequence[str]
) -> SecureCredentialArguments:
    parser = argparse.ArgumentParser(
        description="newrelic client",
    )
    args = SecureCredentialArguments()
    parser.add_argument(
        "--key", type=str, required=True,
        help="The Synthetic secure credential key"
    )
    parser.add_argument(
        "--value", type=str,
        help="The Synthetic secure credential value"
    )
    parser.add_argument(
        "--description", type=str,
        default=args.description,
        help="The Synthetic secure credential description"
    )
    parser.parse_args(args=command, namespace=args)
    return _post_secure_credential_args_hook(args)


def _post_secure_credential_args_hook(
    args: SecureCredentialArguments
) -> SecureCredentialArguments:
    """
    Extra validations for the arguments.
    """
    return args


@dataclass
class AlertPolicyArguments(Arguments):
    name: str = ""
    preference: str = ""
    policy_id: str = ""

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "preference": self.preference,
            "policy_id": self.policy_id
        }


def parse_policy_args(
    command: Sequence[str],
) -> AlertPolicyArguments:
    parser = argparse.ArgumentParser(
        description="newrelic client",
    )
    args = AlertPolicyArguments()
    parser.add_argument(
        "--name",
        type=str,
        help="The Alert policy name",
    )
    parser.add_argument(
        "--preference",
        type=str,
        choices=["PER_POLICY", "PER_INCIDENT", "PER_CONDITION"],
        help="The Alert policy incidentPreference",
    )
    parser.add_argument(
        "--policy-id",
        type=str,
        help="The Alert policy ID",
    )
    parser.parse_args(args=command, namespace=args)
    return _post_policy_args_hook(args)


def _post_policy_args_hook(
    args: AlertPolicyArguments,
) -> AlertPolicyArguments:
    """
    Extra validations for the arguments.
    """
    return args


@dataclass
class ConditionArguments(Arguments):
    policy_id: str = ""
    name: str = ""
    nrql: str = ("SELECT uniqueCount(host) FROM Transaction WHERE "
                 "appName='my-app-name'")
    condition_id: str = ""
    type: str = "static"
    baseline_direction: str = "UPPER_ONLY"
    window_duration: str = "60"
    streaming_method: str = "EVENT_FLOW"
    delay: str = "60"
    threshold: str = "0.9"
    threshold_duration: str = "60"
    threshold_occurrences: str = "AT_LEAST_ONCE"
    operator: str = "ABOVE_OR_EQUALS"
    priority: str = "CRITICAL"
    violation_time: str = "86400"

    def to_dict(self) -> Dict:
        return {
            "policy_id": self.policy_id,
            "name": self.name,
            "nrql": self.nrql,
            "direction": self.baseline_direction,
            "window_duration": self.window_duration,
            "streaming_method": self.streaming_method,
            "delay": self.delay,
            "threshold": self.threshold,
            "threshold_duration": self.threshold_duration,
            "threshold_occurrences": self.threshold_occurrences,
            "operator": self.operator,
            "priority": self.priority,
            "violation_time": self.violation_time,
            "type_": self.type,
            "condition_id": self.condition_id,
        }


def parse_condition_args(
    command: Sequence[str],
) -> ConditionArguments:
    parser = argparse.ArgumentParser(
        description="newrelic client",
    )
    args = ConditionArguments()
    parser.add_argument(
        "--name",
        type=str,
        help="The Alert condition name",
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["baseline", "static"],
        help='The Alert condition threshold type, default static type',
    )
    parser.add_argument(
        "--nrql",
        type=str,
        help="The condition nrql query",
    )
    parser.add_argument(
        "--delay",
        type=str,
        help="The delay of signal settings",
    )
    parser.add_argument(
        "--window-duration",
        type=str,
        help="The window duration of signal settings",
    )
    parser.add_argument(
        "--policy-id",
        type=str,
        help="The Alert policy ID",
    )
    parser.add_argument(
        "--threshold",
        type=str,
        help=("The Alert condition threshold, baseline type threshold must be "
              "Greater than or equal to 1 "),
    )
    parser.add_argument(
        "--threshold-duration",
        type=str,
        help=(
            "The Alert condition threshold duration, baseline type threshold "
            "duration must be Greater than or equal to 120s"
        ),
    )
    parser.add_argument(
        "--threshold-occurrences",
        type=str,
        choices=["AT_LEAST_ONCE", "ALL"],
        help=(
            "The Alert condition threshold occurrences"
        ),
    )
    parser.add_argument(
        "--operator",
        type=str,
        help="The Alert condition operator",
    )
    parser.add_argument(
        "--condition-id",
        type=str,
        help="The Alert condition ID",
    )
    parser.parse_args(args=command, namespace=args)
    return _post_condition_args_hook(args)


def _post_condition_args_hook(
    args: ConditionArguments,
) -> ConditionArguments:
    """
    Extra validations for the arguments.
    """
    return args


@dataclass
class AlertDestinationsArguments(Arguments):
    name: str = ""
    destination_id: str = ""
    email: str = "email@example.com"
    type: str = "EMAIL"

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "email": self.email,
            "destination_id": self.destination_id,
        }


def parse_destinations_args(
    command: Sequence[str],
) -> AlertDestinationsArguments:
    parser = argparse.ArgumentParser(
        description="newrelic client",
    )
    args = AlertDestinationsArguments()
    parser.add_argument(
        "--name",
        type=str,
        help="The Alert destinations name",
    )
    parser.add_argument(
        "--email",
        type=str,
        help="The Alert destinations email",
    )
    parser.add_argument(
        "--destination-id",
        type=str,
        help="The Alert destinations ID",
    )
    parser.parse_args(args=command, namespace=args)
    return _post_destinations_args_hook(args)


def _post_destinations_args_hook(
    args: AlertDestinationsArguments,
) -> AlertDestinationsArguments:
    """
    Extra validations for the arguments.
    """
    return args


@dataclass
class AlertChannelsArguments(Arguments):
    name: str = ""
    channel_id: str = ""
    destination_id: str = ""
    type: str = "EMAIL"
    product: str = "IINT"

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "channel_id": self.channel_id,
            "destination_id": self.destination_id,
            "type_": self.type,
            "product": self.product,
        }


def parse_channels_args(
    command: Sequence[str],
) -> AlertChannelsArguments:
    parser = argparse.ArgumentParser(
        description="newrelic client",
    )
    args = AlertChannelsArguments()
    parser.add_argument(
        "--name",
        type=str,
        help="The Alert channels name",
    )
    parser.add_argument(
        "--channel-id",
        type=str,
        help="The Alert channels ID",
    )
    parser.add_argument(
        "--destination-id",
        type=str,
        help="The Alert destination ID",
    )
    parser.add_argument(
        "--type",
        type=str,
        help="The Alert channels type",
    )
    parser.parse_args(args=command, namespace=args)
    return _post_channels_args_hook(args)


def _post_channels_args_hook(
    args: AlertChannelsArguments,
) -> AlertChannelsArguments:
    """
    Extra validations for the arguments.
    """
    return args


@dataclass
class AlertWorkflowsArguments(Arguments):
    name: str = ""
    policy_id: str = ""
    workflow_id: str = ""
    channel_id: str = ""
    attribute: str = "labels.policyIds"
    type: str = "EMAIL"
    operator: str = "EXACTLY_MATCHES"

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "policy_id": self.policy_id,
            "type_": self.type,
            "attribute": self.attribute,
            "operator": self.operator,
            "workflow_id": self.workflow_id,
            "channel_id": self.channel_id,
        }


def parse_workflows_args(
    command: Sequence[str],
) -> AlertWorkflowsArguments:
    parser = argparse.ArgumentParser(
        description="newrelic client",
    )
    args = AlertWorkflowsArguments()
    parser.add_argument(
        "--name",
        type=str,
        help="The Alert workflows name",
    )
    parser.add_argument(
        "--policy-id",
        type=str,
        help="The Alert policy ID",
    )
    parser.add_argument(
        "--type",
        type=str,
        help="The Alert workflows type",
    )
    parser.add_argument(
        "--workflow-id",
        type=str,
        help="The Alert workflows ID",
    )
    parser.add_argument(
        "--channel-id",
        type=str,
        help="The Alert channel ID",
    )
    parser.parse_args(args=command, namespace=args)
    return _post_workflows_args_hook(args)


def _post_workflows_args_hook(
    args: AlertWorkflowsArguments,
) -> AlertWorkflowsArguments:
    """
    Extra validations for the arguments.
    """
    return args


@dataclass
class ServiceLevelArguments(Arguments):
    guid: str = ""
    monitor_name: str = ""
    name: str = ""
    indicators_id: str = ""
    count: str = "7"
    target: str = "99.9"
    unit: str = "DAY"

    def to_dict(self) -> Dict:
        return {
            "guid": self.guid,
            "monitor_name": self.monitor_name,
            "name": self.name,
            "count": self.count,
            "unit": self.unit,
            "target": self.target,
            "indicators_id": self.indicators_id,
        }


def parse_service_level_args(
    command: Sequence[str],
) -> ServiceLevelArguments:
    parser = argparse.ArgumentParser(
        description="newrelic client",
    )
    args = ServiceLevelArguments()
    parser.add_argument(
        "--monitor-name",
        type=str,
        help="The synthetic monitor name",
    )
    parser.add_argument(
        "--name",
        type=str,
        help="The synthetic service level name",
    )
    parser.add_argument(
        "--count",
        type=str,
        choices=["1", "7", "28"],
        help="The synthetic service level time window count",
    )
    parser.add_argument(
        "--target",
        type=str,
        help="The synthetic service level target",
    )
    parser.add_argument(
        "--indicators-id",
        type=str,
        help="The synthetic service level indicators ID",
    )
    parser.parse_args(args=command, namespace=args)
    return _post_service_level_args_hook(args)


def _post_service_level_args_hook(
    args: ServiceLevelArguments,
) -> ServiceLevelArguments:
    """
    Extra validations for the arguments.
    """
    return args
