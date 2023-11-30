from enum import Enum

class WorkspaceType(Enum):
    VIRTUAL_FILE_SYSTEM = "virtual_file_system"
    GITPOD = "gitpod"
    GITHUB_CODESPACES = "github_codespaces"


DEFAULT_WORKSPACE_TYPE = WorkspaceType.VIRTUAL_FILE_SYSTEM
