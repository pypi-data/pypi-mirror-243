import dataclasses
import datetime
import os
from enum import Enum
from typing import Any, Dict, List, Optional, Union, overload

import inflection
from typing_extensions import Literal

from airplane.api.entities import PromptReviewers, Run, User
from airplane.params import (
    SERIALIZED_DATE_FORMAT,
    SERIALIZED_DATETIME_FORMAT,
    SERIALIZED_DATETIME_MILLISECONDS_FORMAT,
    Constraints,
    ParamConfig,
    PromptParamTypes,
    SerializedParam,
    make_options,
    resolve_type,
    serialize_param,
    to_serialized_airplane_type,
)
from airplane.runtime.standard import (
    execute as standard_execute,
    get_prompt as standard_get_prompt,
    get_user as standard_get_user,
    prompt_background as standard_prompt_background,
    wait_for_prompt as standard_wait_for_prompt,
)
from airplane.types import ConfigVar, File

_AIRPLANE_RUNTIME_ENV_VAR = "AIRPLANE_RUNTIME"


class RuntimeKind(Enum):
    """Valid runtime kinds for Airplane runs."""

    DEV = "dev"
    STANDARD = ""
    WORKFLOW = "workflow"


def execute(
    slug: str,
    param_values: Optional[Dict[str, Any]] = None,
    allow_cached_max_age: Optional[int] = None,
) -> Run:
    """Executes an Airplane task, waits for execution, and returns run metadata.

    Args:
        slug: The slug of the task to run.
        param_values: Optional map of parameter slugs to values.
        allow_cached_max_age: Optional max age (in seconds) of cached run to return.

    Returns:
        The id, task id, param values, status and outputs of the executed run.

    Raises:
        HTTPError: If the task cannot be executed properly.
        RunTerminationException: If the run fails or is cancelled.
        NotImplementedError: For workflow runs.
    """
    return __execute_internal(slug, param_values, None, allow_cached_max_age)


def __execute_internal(
    slug: str,
    param_values: Optional[Dict[str, Any]] = None,
    resources: Optional[Dict[str, Any]] = None,
    allow_cached_max_age: Optional[int] = None,
) -> Run:
    runtime_kind = os.environ.get(_AIRPLANE_RUNTIME_ENV_VAR, RuntimeKind.STANDARD.value)

    if runtime_kind == RuntimeKind.WORKFLOW.value:
        raise NotImplementedError("Workflow run not supported yet by python sdk")

    return standard_execute(slug, param_values, resources, allow_cached_max_age)


@dataclasses.dataclass
class Prompt:
    """Representation of an Airplane prompt."""

    prompt_id: str
    parameters: List[SerializedParam]

    def wait(self) -> Dict[str, Any]:
        """Waits on an operator for prompt input.

        Raises:
            NotImplementedError: For workflow runs.

        Example:
            Prompt user to input a refund amount and reason::

                prompt = airplane.prompt(
                    {"amount": float, "reason": str},
                    background=True,
                )
                values = prompt.wait()
                # Access values as `values["amount"]` and `values["reason"]`
        """
        runtime_kind = os.environ.get(
            _AIRPLANE_RUNTIME_ENV_VAR, RuntimeKind.STANDARD.value
        )

        if runtime_kind == RuntimeKind.WORKFLOW.value:
            raise NotImplementedError("Workflow run not supported yet by python sdk")

        prompt_info = standard_wait_for_prompt(self.prompt_id)
        prompt_values = prompt_info["values"]
        for param in self.parameters:
            # If the user didn't provide a value for the parameter slug
            if param.slug not in prompt_values:
                # Fill in None values for optional parameters that aren't provided
                if param.constraints.optional:
                    prompt_values[param.slug] = None
                # We should never get here...
                continue

            if param.multi:
                prompt_values[param.slug] = [
                    _convert_prompt_param(param, value)
                    for value in prompt_values[param.slug]
                ]
            else:
                prompt_values[param.slug] = _convert_prompt_param(
                    param,
                    prompt_values[param.slug],
                )

        return prompt_values

    def submitter(self) -> Optional[User]:
        """Returns the user who submitted the prompt, if there is one."""
        runtime_kind = os.environ.get(
            _AIRPLANE_RUNTIME_ENV_VAR, RuntimeKind.STANDARD.value
        )

        if runtime_kind == RuntimeKind.WORKFLOW.value:
            raise NotImplementedError("Workflow run not supported yet by python sdk")

        prompt_info = standard_get_prompt(self.prompt_id)
        if prompt_info.get("submittedBy") is None:
            return None

        user_info = standard_get_user(prompt_info["submittedBy"])
        return User(
            id=user_info["userID"],
            email=user_info["email"],
            name=user_info["name"],
        )


def _convert_prompt_param(param: SerializedParam, value: Any) -> Any:
    if param.type == "date":
        return datetime.datetime.strptime(value, SERIALIZED_DATE_FORMAT).date()
    if param.type == "datetime":
        return datetime.datetime.strptime(
            value,
            SERIALIZED_DATETIME_MILLISECONDS_FORMAT
            if "." in value
            else SERIALIZED_DATETIME_FORMAT,
        )
    if param.type == "upload":
        return File(
            id=value["id"],
            url=value["url"],
        )
    if param.type == "configvar":
        return ConfigVar(
            name=value["name"],
            value=value["value"],
        )

    return value


@overload
def prompt(
    params: Optional[Dict[str, PromptParamTypes]] = None,
    *,
    reviewers: Optional[PromptReviewers] = None,
    confirm_text: Optional[str] = None,
    cancel_text: Optional[str] = None,
    description: Optional[str] = None,
    background: Literal[False] = False,
    notify: bool = True,
) -> Dict[str, Any]:
    ...


@overload
def prompt(
    params: Optional[Dict[str, PromptParamTypes]] = None,
    *,
    reviewers: Optional[PromptReviewers] = None,
    confirm_text: Optional[str] = None,
    cancel_text: Optional[str] = None,
    description: Optional[str] = None,
    background: Literal[True],
    notify: bool = True,
) -> Prompt:
    ...


def prompt(
    params: Optional[Dict[str, PromptParamTypes]] = None,
    *,
    reviewers: Optional[PromptReviewers] = None,
    confirm_text: Optional[str] = None,
    cancel_text: Optional[str] = None,
    description: Optional[str] = None,
    background: bool = False,
    notify: bool = True,
) -> Union[Dict[str, Any], Prompt]:
    """Prompts an operator for input.

    Each prompt contains a parameter form, similar to what you see when executing a task or runbook.
    When a prompt is created, the run pauses and waits for a response before continuing.
    By default, anyone who can access the associated run can also respond to the prompt,
    but this can be restricted by specifying reviewers in the prompt's options. As a convenience,
    you can use `confirm` to create prompts with no parameters.

    Args:
        params: Defines the parameter form as a mapping of slug to parameter.
            The values will be returned as an object that maps the parameter slug to the
            corresponding value. To learn more about parameters, see
            the [Parameter documentation](https://docs.airplane.dev/platform/parameters).
        reviewers: Reviewers that are allowed to approve the prompt. If no reviewers are provided,
            anyone that can see the active run is allowed to approved.
        confirm_text: Text of the confirmation button on the prompt dialog.
        cancel_text: Text of the cancellation button on the prompt dialog.
        description: Prompt description to display. Supports markdown.
        background: If true, the prompt will be created in the background and a
            `Prompt` object will be returned. To wait for the prompt to be submitted,
            call `prompt.wait()`.
        notify: If true, the prompt will send a notification to the reviewers.

    Raises:
        NotImplementedError: For workflow runs.

    Example:
        Prompt user to input a refund amount and reason::

            values = airplane.prompt({
                "amount": int,
                "reason": str,
            }, confirm_text="Accept refund")
            # Access values as `values["amount"]` and `values["reason"]`

         Prompt with a list of options to choose from. As a convenience, you can use
         `prompt_select` to create a prompt with a list of objects::

             values = airplane.prompt({
                "username": Annotated[
                    str,
                    prompt.options(["colin", "eric"])
                ],
             })
             # Access values as `values["username"]`
    """

    runtime_kind = os.environ.get(_AIRPLANE_RUNTIME_ENV_VAR, RuntimeKind.STANDARD.value)

    if runtime_kind == RuntimeKind.WORKFLOW.value:
        raise NotImplementedError("Workflow run not supported yet by python sdk")

    serialized_params = []
    for slug, param in (params or {}).items():
        param_info = resolve_type(slug, param)
        param_config = param_info.param_config
        if param_config is None:
            param_config = ParamConfig()

        default = param_config.default
        if default is not None:
            default = serialize_param(default)

        serialized_type, component = to_serialized_airplane_type(
            slug, param_info.resolved_type
        )
        slug = param_config.slug or slug
        serialized_params.append(
            SerializedParam(
                slug=slug,
                name=param_config.name or inflection.humanize(slug),
                type=serialized_type,
                component=component,
                desc=param_config.description,
                default=default,
                multi=param_info.is_multi,
                constraints=Constraints(
                    optional=param_info.is_optional,
                    options=make_options(param_config),
                    regex=param_config.regex,
                ),
            )
        )

    prompt_id = standard_prompt_background(
        serialized_params,
        reviewers=reviewers,
        confirm_text=confirm_text,
        cancel_text=cancel_text,
        description=description,
        notify=notify,
    )
    background_prompt = Prompt(prompt_id, serialized_params)

    if background:
        return background_prompt

    return background_prompt.wait()
