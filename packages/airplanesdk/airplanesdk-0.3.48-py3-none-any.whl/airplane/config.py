import dataclasses
import datetime
import functools
import inspect
from collections import Counter
from typing import Any, Callable, Dict, List, Optional, Union

import inflection
import typing_extensions
from docstring_parser import parse
from typing_extensions import Literal, ParamSpec

from airplane._version import __version__
from airplane.api.entities import Run
from airplane.exceptions import (
    InvalidAnnotationException,
    InvalidTaskConfigurationException,
    UnsupportedDefaultTypeException,
)
from airplane.params import (
    SERIALIZED_DATE_FORMAT,
    SERIALIZED_DATETIME_FORMAT_WITH_TIMEZONE,
    SERIALIZED_DATETIME_MILLISECONDS_FORMAT,
    ParamConfig,
    ParamDefOptions,
    ParamDefTypes,
    ParamType,
    ParamTypes,
    make_options,
    resolve_type,
    serialize_param,
    to_airplane_type,
)
from airplane.runtime import execute
from airplane.types import ConfigVar, File, RuntimeType
from airplane.utils import make_slug

# Restrict task execution so it can only be called from other tasks or views.
TaskCaller = Literal["task", "view"]

DefaultRunPermission = Literal["task-viewers", "task-participants"]


@dataclasses.dataclass(frozen=True)
class Resource:
    """Airplane resource attachment.

    Resources in Airplane allow users to configure connections to external systems
    like databases and APIs and use them in tasks and runbooks.
    https://docs.airplane.dev/resources/overview

    Attributes:
        slug:
            Resource identifier.
        alias:
            Alias to reference the resource. Defaults to resource slug.
    """

    slug: str
    alias: Optional[str] = None


@dataclasses.dataclass(frozen=True)
class EnvVar:
    """Airplane environment variable.

    Environment variables allow users to configure constant values or reference
    config variables. They can be accessed via `os.getenv("MY_ENV_VAR_NAME")`.

    Attributes:
        name:
            Environment variable name.
        value:
            Set a constant value for the environment variable.
        config_var_name:
            Name of the config variable to use. Configs variables allow users
            to set team-wide values / secrets.
    """

    name: str
    value: Optional[str] = None
    config_var_name: Optional[str] = None

    def __post_init__(self) -> None:
        if "=" in self.name:
            raise InvalidTaskConfigurationException(
                f'Environment variable name {self.name} cannot contain "="'
            )
        if (self.config_var_name and self.value) or (
            not self.config_var_name and not self.value
        ):
            raise InvalidTaskConfigurationException(
                "Exactly one of `config_var_name` or `value` should be set"
            )


@dataclasses.dataclass(frozen=True)
class Schedule:
    """Airplane schedule definition.

    Schedules allow users to automatically run tasks on a recurring schedule.
    https://docs.airplane.dev/schedules/schedules

    Attributes:
        slug:
            Human-friendly identifier used for the schedule. Schedule slugs must be unique
            within an individual task / workflow.
        cron:
            Schedule cron expression, e.g.  "0 * * * *"
        name:
            Schedule name. Defaults to the slug.
        description:
            Schedule description displayed on the Airplane app.
        param_values:
            Dictionary of parameter name to parameter value used for the scheduled execution.
            All required parameters must be defined.
    """

    slug: str
    cron: str
    name: Optional[str] = None
    description: Optional[str] = None
    param_values: Optional[Dict[str, Optional[ParamTypes]]] = None


@dataclasses.dataclass(frozen=True)
class Webhook:
    """Airplane webhook definition.

    Webhooks allow users to trigger tasks via HTTP requests.

    Attributes:
        slug:
            Human-friendly identifier used for the webhook. Webhook slugs must be unique
            within an individual task / workflow.
        require_airplane_token:
            Require an Airplane API key to be passed in the `X-Airplane-API-Key` header.
            Defaults to False.
    """

    slug: str
    require_airplane_token: bool = False


@dataclasses.dataclass
class PermissionAssignees:
    """Airplane permission assignees.

    Attributes:
        users:
            Users to assign the permission to. Users are referenced via their emails.
        groups:
            Groups to assign the permission to. Groups are referenced via their slugs.
    """

    users: Optional[List[str]] = None
    groups: Optional[List[str]] = None


@dataclasses.dataclass(frozen=True)
class ExplicitPermissions:
    """Airplane explicit permissions.

    Explicit task permissions in Airplane allow users to configure granular group-based
    or user-based permissions for the task:
    https://docs.airplane.dev/platform/permissions#task-and-runbook-permissions

    Attributes:
        viewers:
            Groups and users who can see task information, but can't request or execute tasks.
        requesters:
            Groups and users who have all the permission of viewers, and can also request tasks.
        executers:
            Groups and users who have all the permissions of requesters, and can also execute
            tasks and other's requests.
        admins:
            Groups and users who have full access to the task, and can change task configurations
            and permissions.
    """

    viewers: Optional[PermissionAssignees] = None
    requesters: Optional[PermissionAssignees] = None
    executers: Optional[PermissionAssignees] = None
    admins: Optional[PermissionAssignees] = None


@dataclasses.dataclass(frozen=True)
class K8SPodSpecPatch:
    """Strategic merge patch to apply to Kubernetes runner pod specs.

    NOTE: This is an advanced feature that only applies for self-hosted
    agents running in Kubernetes.

    Attributes:
        patch:
            Patch contents as a Python dictionary.
    """

    patch: Dict[str, Any]


@dataclasses.dataclass(frozen=True)
class RunnerConfig:
    """Configuration for runners for instances of the task.

    NOTE: This is an advanced feature that only applies for self-hosted
    agents.

    Attributes:
        k8s_pod_spec_patch:
            Patch to apply to Kubernetes runner pod specs.
    """

    k8s_pod_spec_patch: Optional[K8SPodSpecPatch]


@dataclasses.dataclass(frozen=True)
class HrefAction:
    """Action that opens a link.

    Attributes:
        href:
            A string URL to navigate to when the action is clicked.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
        label:
            Label of the action.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
            If not set, the label will default to the entity being previewed.

    """

    href: str
    label: Optional[str] = None


ActionAs = Literal["side_peek", "center_peek", "full_page"]


@dataclasses.dataclass(frozen=True)
class TaskAction:
    """Action that opens a task.

    Attributes:
        task:
            Slug of the task to preview.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
        label:
            Label of the action.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
            If not set, the label will default to the entity being previewed.
        param_values:
            The parameter values when previewing the entity.
            Keys and values can be a JST that can reference the output of the task and
            the row of the output if using a row action.
        as_:
            Method of previewing the entitiy.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
            Defaults to "side_peek".
    """

    task: str
    label: Optional[str] = None
    param_values: Optional[Dict[str, Optional[ParamTypes]]] = None
    as_: Optional[ActionAs] = None


@dataclasses.dataclass(frozen=True)
class PageAction:
    """Action that opens a page.

    Attributes:
        page:
            Path of the page to preview.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
        label:
            Label of the action.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
            If not set, the label will default to the entity being previewed.
        param_values:
            The parameter values when previewing the entity.
            Keys and values can be a JST that can reference the output of the task and
            the row of the output if using a row action.
        as_:
            Method of previewing the entitiy.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
            Defaults to "side_peek".
    """

    page: str
    label: Optional[str] = None
    param_values: Optional[Dict[str, Optional[ParamTypes]]] = None
    as_: Optional[ActionAs] = None


@dataclasses.dataclass(frozen=True)
class ViewAction:
    """Action that opens a view.

    Attributes:
        view:
            Slug of the view to preview.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
        label:
            Label of the action.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
            If not set, the label will default to the entity being previewed.
        param_values:
            The parameter values when previewing the entity.
            Keys and values can be a JST that can reference the output of the task and
            the row of the output if using a row action.
        as_:
            Method of previewing the entitiy.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
            Defaults to "side_peek".
    """

    view: str
    label: Optional[str] = None
    param_values: Optional[Dict[str, Optional[ParamTypes]]] = None
    as_: Optional[ActionAs] = None


@dataclasses.dataclass(frozen=True)
class RunbookAction:
    """Action that opens a runbook.

    Attributes:
        runbook:
            Slug of the page to preview.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
        label:
            Label of the action.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
            If not set, the label will default to the entity being previewed.
        param_values:
            The parameter values when previewing the entity.
            Keys and values can be a JST that can reference the output of the task and
            the row of the output if using a row action.
        as_:
            Method of previewing the entitiy.
            Can be a JST that can reference the output of the task and
            the row of the output if using a row action.
            Defaults to "side_peek".
    """

    runbook: str
    label: Optional[str] = None
    param_values: Optional[Dict[str, Optional[ParamTypes]]] = None
    as_: Optional[ActionAs] = None


Action = Union[
    HrefAction,
    TaskAction,
    PageAction,
    ViewAction,
    RunbookAction,
]


@dataclasses.dataclass(frozen=True)
class StatisticOutputDisplay:
    """Airplane statistic output display.

    Setting the output display to a statistic means the task run's output will be displayed
    as a statistic.

    Attributes:
        value:
            Value of the display.
            The value can be a JST that can reference the output of the task.
            If not set, the value will be the output of the task.
        label:
            The statistic label.
        sublabel:
            The statistic sublabel.
        actions:
            Buttons to display alongside the output display. Can be used to open a link,
            task, page, view, or runbook.
            If more than 3 actions are provided, only the first 3 will be shown.

    """

    type: Literal["statistic"] = "statistic"
    value: Optional[str] = None
    label: Optional[str] = None
    sublabel: Optional[str] = None
    actions: Optional[List[Action]] = None


@dataclasses.dataclass(frozen=True)
class TextOutputDisplay:
    """Airplane text output display.

    Setting the output display to text means the task run's output will be displayed
    as text. Text also allows formatting with Markdown.

    Attributes:
        value:
            Value of the display.
            The value can be a JST that can reference the output of the task.
            If not set, the value will be the output of the task.
        actions:
            Buttons to display alongside the output display. Can be used to open a link,
            task, page, view, or runbook.
            If more than 3 actions are provided, only the first 3 will be shown.
    """

    type: Literal["text"] = "text"
    value: Optional[str] = None
    actions: Optional[List[Action]] = None


@dataclasses.dataclass(frozen=True)
class DescriptionListOutputDisplay:
    """Airplane description list output display.

    Setting the output display to a description list means the task run's output will be displayed
    as a description list.

    Attributes:
        value:
            Value of the display.
            The value should be a JST that evaluates to the expected format of a description list,
            which is a list of objects with `term` and `description` fields. The JST can reference
            the output of the task.
        actions:
            Buttons to display alongside the output display. Can be used to open a link,
            task, page, view, or runbook.
            If more than 3 actions are provided, only the first 3 will be shown.
    """

    type: Literal["descriptionList"] = "descriptionList"
    value: Optional[str] = None
    actions: Optional[List[Action]] = None


@dataclasses.dataclass(frozen=True)
class JSONOutputDisplay:
    """Airplane JSON output display.

    Setting the output display to JSON means the task run's output will be displayed
    as a JSON block.

    Attributes:
        actions:
            Buttons to display alongside the output display. Can be used to open a link,
            task, page, view, or runbook.
            If more than 3 actions are provided, only the first 3 will be shown.
    """

    type: Literal["json"] = "json"
    actions: Optional[List[Action]] = None


@dataclasses.dataclass(frozen=True)
class CodeOutputDisplay:
    """Airplane code output display.

    Setting the output display to code means the task run's output will be displayed
    as a code block.

    Attributes:
        language:
            Language of the code block.
        actions:
            Buttons to display alongside the output display. Can be used to open a link,
            task, page, view, or runbook.
            If more than 3 actions are provided, only the first 3 will be shown.
    """

    type: Literal["code"] = "code"
    language: Optional[str] = None
    actions: Optional[List[Action]] = None


@dataclasses.dataclass(frozen=True)
class FileOutputDisplay:
    """Airplane file output display.

    Setting the output display to file means the task run's output must be an Airplane
    file and will be displayed as a file preview.

    Attributes:
        actions:
            Buttons to display alongside the output display. Can be used to open a link,
            task, page, view, or runbook.
            If more than 3 actions are provided, only the first 3 will be shown.
    """

    type: Literal["file"] = "file"
    actions: Optional[List[Action]] = None


@dataclasses.dataclass(frozen=True)
class Column:
    """Airplane table output display column."""

    label: str
    accessor: str


@dataclasses.dataclass(frozen=True)
class TableOutputDisplay:
    """Airplane table output display.

    Setting the output display to table means the task run's output will be displayed
    as a table.

    Attributes:
        columns:
            Columns of the table.
            `label` is what's displayed as the column header. `accessor` indicates which field of
            the table value should be used for this column.
            If not set, the columns will be inferred from the output of the task.
        value:
            Value of the display.
            The value should be a JST that evaluates to the expected format of a table, which is a
            list of objects with fields corresponding to the columns. The JST can reference the
            output of the task.
            If not set, the value will be the output of the task.
        actions:
            Buttons to display alongside the output display. Can be used to open a link,
            task, page, view, or runbook.
            If more than 3 actions are provided, only the first 3 will be shown.
        row_actions:
            Buttons to display for each row of the table output display. Can be used to open a link,
            task, page, view, or runbook.
            If more than 1 row action is provided, they will be shown in a dropdown menu.
    """

    type: Literal["table"] = "table"
    columns: Optional[List[Column]] = None
    value: Optional[str] = None
    actions: Optional[List[Action]] = None
    row_actions: Optional[List[Action]] = None


OutputDisplay = Union[
    StatisticOutputDisplay,
    TextOutputDisplay,
    DescriptionListOutputDisplay,
    JSONOutputDisplay,
    CodeOutputDisplay,
    FileOutputDisplay,
    TableOutputDisplay,
]


P = ParamSpec("P")


def task(
    slug: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    require_requests: bool = False,
    allow_self_approvals: bool = True,
    restrict_callers: Optional[List[TaskCaller]] = None,
    default_run_permissions: Optional[DefaultRunPermission] = None,
    timeout: int = 3600,
    allow_cached_max_age: Optional[int] = None,
    concurrency_key: Optional[str] = None,
    concurrency_limit: Optional[int] = None,
    constraints: Optional[Dict[str, str]] = None,
    resources: Optional[List[Resource]] = None,
    schedules: Optional[List[Schedule]] = None,
    webhooks: Optional[List[Webhook]] = None,
    env_vars: Optional[List[EnvVar]] = None,
    permissions: Optional[Union[Literal["team_access"], ExplicitPermissions]] = None,
    runner_config: Optional[RunnerConfig] = None,
    output_display: Optional[OutputDisplay] = None,
) -> Callable[[Callable[P, Any]], Callable[P, Run]]:
    """Decorator used to define an Airplane task.

    This decorator inspects the decorated function to create an Airplane task. The task's parameters
    are deduced from the function's arguments and type hints.

    Additional parameter metadata can be provided by attaching an airplane.ParamConfig to a
    typing.Annotated typehint (for versions of Python prior to 3.9, typing_extensions.Annotated
    can be used).

    The following map enumerates the supported Python types and equivalent Airplane
    parameter types (Airplane parameter details https://docs.airplane.dev/platform/parameters)::

        str: short text
        airplane.LongText: long text
        airplane.SQL: SQL
        bool: boolean
        int: integer
        float: number
        airplane.File: file
        datetime.date: date
        datetime.datetime: datetime
        airplane.ConfigVar: config variable

    Example:
        Sample task::

            @airplane.task()
            def add_two_numbers(first_number: int, second_number: int) -> int:
                return first_number + second_number

        Sample task with parameter annotation::

            @airplane.task()
            def capitalize_string(
                input: Annotated[str, airplane.ParamConfig(name="User string")]
            ) -> str:
                return input.capitalize()
    Args:
        slug:
            Human-friendly identifier used to reference this task. Must be unique
            across tasks and workflows. Defaults to function name.
        name:
            Task name displayed on the Airplane app. Defaults to funcion name in sentence case.
        description:
            Task description displayed on the Airplane app. If not provided, the description
            will be pulled from the docstring of the decorated function.
        require_requests:
            Whether or not this task requires a request to execute.
        allow_self_approvals:
            Whether or not this task allows self approvals.
        restrict_callers:
            Restrict task execution to specific callers. This disables direct execution
            and hides the task in the UI.
        default_run_permissions:
            Manage who has permissions for new runs of this task. If not provided,
            defaults to "task-viewers".
        timeout:
            How long a task can run (in seconds) for before it is automatically cancelled.
        allow_cached_max_age:
            If set, runs with identical inputs within the configured age (in seconds) may get
            cached results.
        concurrency_key:
            Restricts runs with the same concurrency key from executing at the same time.
        concurrency_limit:
            If concurrency key is set, only allows this task's runs to start if the number of
            other active runs with the same key is below this limit.
        constraints:
            Constraints for which agents are allowed to execute this task's runs, only
            applicable for users with self hosted agents.
        resources:
            Resources to attach to this task. Resources can be accessed through environment
            variables or built-ins. Resources accessed by this task must be explicitly attached
            in the task's definition.
        schedules:
            Schedules to attach to this task. Schedules allow users to automatically run
            task on a recurring schedule.
        webhooks:
            Webhooks to attach to this task. Webhooks allow users to trigger tasks
            from external systems via HTTP request.
        env_vars:
            Enviornment variables to attach to this task. Environment variables allow users
            to configure constant values or reference config variables.
        permissions:
            Permissions determine the users and groups that can access the task. Permissions can
            be set to "team_access" to allow full access to anyone on your team or to explicit
            permissions to configure granular group-based or user-based permissions for the task.
        runner_config:
            Configuration for runners for instances of the task.
        output_display:
            Output display determines how the task's run's output is displayed.
            If not provided, the output will be displayed as a table.
    """

    def decorator(func: Callable[P, Any]) -> Callable[P, Run]:
        """Assigns an __airplane attribute to a function to mark it as an Airplane object"""

        config = TaskDef.build(
            func=func,
            runtime="",
            slug=slug,
            name=name,
            description=description,
            require_requests=require_requests,
            allow_self_approvals=allow_self_approvals,
            restrict_callers=restrict_callers,
            timeout=timeout,
            allow_cached_max_age=allow_cached_max_age,
            default_run_permissions=default_run_permissions,
            concurrency_key=concurrency_key,
            concurrency_limit=concurrency_limit,
            constraints=constraints,
            resources=resources,
            schedules=schedules,
            webhooks=webhooks,
            env_vars=env_vars,
            permissions=permissions,
            runner_config=runner_config,
            output_display=output_display,
        )

        @functools.wraps(func)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> Run:
            kwargs.update(zip(func.__code__.co_varnames, args))  # type: ignore
            return execute(config.slug, kwargs)

        # pylint: disable=protected-access
        wrapped.__airplane = config  # type: ignore
        return wrapped

    return decorator


@dataclasses.dataclass(frozen=True)
class ParamDef:
    """Parameter definition"""

    # Represents the original function's argument name.
    # We need this in order to be able to map slug -> arg_name in case they differ.
    arg_name: str
    slug: str
    name: str
    type: ParamType
    description: Optional[str]
    default: Optional[ParamDefTypes]
    required: Optional[bool]
    multi: Optional[bool]
    options: Optional[ParamDefOptions]
    regex: Optional[str]
    hidden: Optional[str]
    validate: Optional[str]
    secret: Optional[bool]


@dataclasses.dataclass(frozen=True)
class TaskDef:
    """Task definition"""

    func: Callable[..., Any]
    slug: str
    name: str
    runtime: RuntimeType
    entrypoint_func: str
    description: Optional[str]
    require_requests: Optional[bool]
    allow_self_approvals: Optional[bool]
    restrict_callers: Optional[List[TaskCaller]]
    timeout: Optional[int]
    allow_cached_max_age: Optional[int]
    concurrency_key: Optional[str]
    concurrency_limit: Optional[int]
    default_run_permissions: Optional[DefaultRunPermission]
    constraints: Optional[Dict[str, str]]
    resources: Optional[List[Resource]]
    schedules: Optional[List[Schedule]]
    parameters: Optional[List[ParamDef]]
    env_vars: Optional[List[EnvVar]]
    permissions: Optional[Union[Literal["team_access"], ExplicitPermissions]]
    output_display: Optional[OutputDisplay]
    sdk_version: str = dataclasses.field(default=__version__, init=False)
    webhooks: Optional[List[Webhook]]
    runner_config: Optional[RunnerConfig]

    def run(self, params: Dict[str, Any]) -> Any:
        """Execute task function from param dictionary"""
        func_args: Dict[str, Any] = {}
        for param in self.parameters or []:
            # If the user didn't provide a value for the parameter slug
            if param.slug not in params:
                # Fill in None values for optional parameters that aren't provided
                # and don't have a default value.
                if not param.required and param.default is None:
                    func_args[param.arg_name] = None
                # Otherwise, we fall back to the function default arguments.
                continue

            param_value = params[param.slug]
            if param_value is None:
                func_args[param.arg_name] = None
            elif param.multi:
                func_args[param.arg_name] = [
                    _convert_task_param(param, value) for value in param_value
                ]
            else:
                func_args[param.arg_name] = _convert_task_param(param, param_value)

        return self.func(**func_args)

    @classmethod
    def build(
        cls,
        func: Callable[P, Any],
        runtime: RuntimeType,
        slug: Optional[str],
        name: Optional[str],
        description: Optional[str],
        require_requests: bool,
        allow_self_approvals: bool,
        restrict_callers: Optional[List[TaskCaller]],
        timeout: int,
        allow_cached_max_age: Optional[int],
        concurrency_key: Optional[str],
        concurrency_limit: Optional[int],
        default_run_permissions: Optional[DefaultRunPermission],
        constraints: Optional[Dict[str, str]],
        resources: Optional[List[Resource]],
        schedules: Optional[List[Schedule]],
        webhooks: Optional[List[Webhook]],
        env_vars: Optional[List[EnvVar]],
        permissions: Optional[Union[Literal["team_access"], ExplicitPermissions]],
        runner_config: Optional[RunnerConfig],
        output_display: Optional[OutputDisplay],
    ) -> "TaskDef":
        """Construct a task definition from a function."""
        task_description = description
        if func.__doc__ is None:
            param_descriptions = {}
        else:
            docstring = parse(func.__doc__)
            param_descriptions = {
                param.arg_name: param.description for param in docstring.params
            }
            task_description = (
                description or docstring.long_description or docstring.short_description
            )
        type_hints = typing_extensions.get_type_hints(func, include_extras=True)
        sig = inspect.signature(func)
        parameters: List[ParamDef] = []
        for param in sig.parameters.values():
            type_hint = type_hints.get(param.name)
            if type_hint is None:
                raise InvalidAnnotationException(
                    prefix="Missing type annotation",
                    func_name=func.__name__,
                    param_name=param.name,
                )
            param_info = resolve_type(
                param.name,
                type_hint,
                func_name=func.__name__,
            )
            param_config = param_info.param_config
            if param_config is None:
                param_config = ParamConfig()

            if param.default is inspect.Signature.empty:
                default = None
            else:
                if isinstance(param.default, File):
                    raise UnsupportedDefaultTypeException(
                        "File defaults are not currently supported with inline code configuration."
                    )
                default = serialize_param(param.default)
            if param_config.default is not None and param_config.default != default:
                raise InvalidTaskConfigurationException(
                    f"Function {func.__name__} contains an invalid default value configuration "
                    f"for parameter {param.name}. Default values should be set via the Python "
                    "native default function parameter syntax, e.g. "
                    '`def my_task(my_param: str = "default")` instead of inside `ParamConfig`.'
                )

            default_slug = make_slug(param.name)
            parameters.append(
                ParamDef(
                    arg_name=param.name,
                    # Parameter slug is the parameter's name in snakecase
                    slug=param_config.slug or default_slug,
                    name=param_config.name or inflection.humanize(default_slug),
                    type=to_airplane_type(
                        param.name, param_info.resolved_type, func.__name__
                    ),
                    description=param_config.description
                    or param_descriptions.get(param.name),
                    required=not param_info.is_optional,
                    default=default,
                    multi=param_info.is_multi,
                    options=make_options(param_config),
                    regex=param_config.regex,
                    hidden=param_config.hidden,
                    validate=param_config.validate,
                    secret=param_config.secret,
                )
            )

        def _check_duplicates(counter: Counter, duplicate_type: str) -> None:
            duplicates = [slug for slug, count in counter.items() if count > 1]
            if duplicates:
                raise InvalidTaskConfigurationException(
                    f"Function {func.__name__} has duplicate {duplicate_type} {duplicates}"
                )

        _check_duplicates(Counter([p.slug for p in parameters]), "parameter slugs")
        _check_duplicates(Counter([s.slug for s in schedules or []]), "schedule slugs")
        _check_duplicates(Counter([e.name for e in env_vars or []]), "env var names")

        # Convert schedule param values to the correct default types
        for schedule in schedules or []:
            if schedule.param_values is not None:
                for param_name, param_value in schedule.param_values.items():
                    if param_value is not None:
                        schedule.param_values[param_name] = serialize_param(param_value)

        # pylint: disable=protected-access
        default_slug = make_slug(func.__name__)
        return cls(
            func=func,
            runtime=runtime,
            slug=slug or default_slug,
            name=name or inflection.humanize(default_slug),
            description=task_description,
            require_requests=require_requests,
            allow_self_approvals=allow_self_approvals,
            restrict_callers=restrict_callers,
            timeout=timeout,
            allow_cached_max_age=allow_cached_max_age,
            concurrency_key=concurrency_key,
            concurrency_limit=concurrency_limit,
            default_run_permissions=default_run_permissions,
            constraints=constraints,
            schedules=schedules,
            resources=resources,
            parameters=parameters,
            env_vars=env_vars,
            permissions=permissions,
            output_display=output_display,
            entrypoint_func=func.__name__,
            webhooks=webhooks,
            runner_config=runner_config,
        )


def _convert_task_param(param: ParamDef, value: Any) -> Any:
    if param.type == "date":
        return datetime.datetime.strptime(value, SERIALIZED_DATE_FORMAT).date()
    if param.type == "datetime":
        return datetime.datetime.strptime(
            value,
            SERIALIZED_DATETIME_MILLISECONDS_FORMAT
            if "." in value
            else SERIALIZED_DATETIME_FORMAT_WITH_TIMEZONE,
        )
    if param.type == "upload":
        value = File(
            id=value["id"],
            url=value["url"],
        )
    if param.type == "configvar":
        return ConfigVar(
            name=value["name"],
            value=value["value"],
        )

    return value
