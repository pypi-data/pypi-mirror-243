from enum import Enum, unique
from typing import Optional

from pydantic import BaseModel

from ellipsis.src.models.workspaces.command import CommandOutput


@unique
class WorkspaceRequestType(Enum):
    FILE_CHANGE = "file_change"
    FILE_READ = "file_read"
    FILE_WRITE = "file_write"
    RUN_COMMAND = "run_command"


class BaseWorkspaceRequest(BaseModel):
    request_type: WorkspaceRequestType  # used for websockets
    id: str

    # TODO just include CustomBaseModel
    class Config:
        orm_mode = True
        use_enum_values = True


class BaseWorkspaceResponse(BaseModel):
    ok: bool = True  # TODO remove, redundant

    class Config:
        orm_mode = True
        use_enum_values = True


class RejectedResponse(BaseWorkspaceResponse):
    ok: bool = False
    reason: str


# DEPRECATED use FileWriteRequest instead
class FileChangeRequest(BaseWorkspaceRequest):
    type: WorkspaceRequestType = WorkspaceRequestType.FILE_CHANGE
    path: str
    diff: str


# DEPRECATED use FileWriteRequest instead
class FileChangeResponse(BaseWorkspaceResponse):
    req: FileChangeRequest


class FileReadRequest(BaseWorkspaceRequest):
    request_type: WorkspaceRequestType = WorkspaceRequestType.FILE_READ
    path: str


class FileReadResponse(BaseModel):
    contents: Optional[str]


class FileWriteRequest(BaseWorkspaceRequest):
    request_type: WorkspaceRequestType = WorkspaceRequestType.FILE_WRITE
    path: str
    contents: str


class FileWriteResponse(BaseModel):
    pass


class RunCommandRequest(BaseWorkspaceRequest):
    request_type: WorkspaceRequestType = WorkspaceRequestType.RUN_COMMAND
    # command: AgentShellCommand
    command_str: str


class RunCommandResponse(BaseWorkspaceResponse):
    req: RunCommandRequest
    output: CommandOutput
