from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar

from airplane.types import JSONType


class RunStatus(Enum):
    """Valid statuses during a run's lifecycle."""

    NOT_STARTED = "NotStarted"
    QUEUED = "Queued"
    ACTIVE = "Active"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    CANCELLED = "Cancelled"

    def is_terminal(self) -> bool:
        """Returns whether the status is terminal.

        Returns:
            Whether the status is terminal.
        """

        return self in [self.SUCCEEDED, self.FAILED, self.CANCELLED]


JSONTypeT = TypeVar(
    "JSONTypeT",
    bound=JSONType,
)


@dataclass
class BuiltInRun(Generic[JSONTypeT]):
    """Representation of an Airplane built-in run.

    Attributes:
        id: The id of the run.
        param_values: The param values the run was provided.
        status: The current status of the run.
        output: The outputs (if any) of the run.
        is_cached: Whether the run result was cached. Only set when executing a run.
    """

    id: str
    param_values: Dict[str, Any]
    status: RunStatus
    output: JSONTypeT
    is_cached: Optional[bool]


@dataclass
class Run:
    """Representation of an Airplane run.

    Attributes:
        id: The id of the run.
        task_id: The task id associated with the run (None for builtin tasks).
        param_values: The param values the run was provided.
        status: The current status of the run.
        output: The outputs (if any) of the run.
        is_cached: Whether the run result was cached. Only set when executing a run.
    """

    id: str
    task_id: Optional[str]
    param_values: Dict[str, Any]
    status: RunStatus
    output: JSONType
    is_cached: Optional[bool]


@dataclass
class ExecuteTaskResponse:
    """Response from executing a task.

    Attributes:
        run_id: The id of the run created by executing the task.
        is_cached: Whether the run result was cached.
    """

    run_id: str
    is_cached: Optional[bool]


@dataclass
class PromptReviewers:
    """Reviewers that are allowed to approve the prompt.

    Args:
        groups: List of groups allowed to approve the prompt. Groups are
            referenced via their slugs.
        users: List of users allowed to approve the prompt. Users are
            referenced via their emails.
        allow_self_approvals: Whether or not the run creator is allowed to approve
            their own prompt.
    """

    groups: Optional[List[str]] = None
    users: Optional[List[str]] = None
    allow_self_approvals: bool = True


@dataclass
class TaskReviewer:
    """Reviewers that are allowed to approve the task.

    Args:
        group_id: The ID of the group allowed to approve the task.o
        user_id: The ID of the user allowed to approve the task.
    """

    group_id: Optional[str] = None
    user_id: Optional[str] = None


@dataclass
class Sleep:
    """Airplane sleep object."""

    id: str
    run_id: str
    created_at: str
    until: str
    duration_ms: int
    skipped_at: Optional[str]
    skipped_by: Optional[str]


@dataclass
class User:
    """Airplane user."""

    id: str
    email: str
    name: str
