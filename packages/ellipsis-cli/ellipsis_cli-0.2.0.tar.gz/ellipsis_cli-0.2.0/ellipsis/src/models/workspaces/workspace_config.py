from typing import List, Optional

from pydantic import BaseModel

from .command import AgentShellCommandYaml

WORKSPACE_CONFIG_YAML_FILE_NAME = ".code_generation.yaml"


class PrReviewBBYaml(BaseModel):
    auto_review: bool = False
    rules: List[str] = []

    # Agent will give its confidence in its review. Scores below this are rejected.
    sensitivity: float = 0.5

    # fix adjacent code, not just the code being changed.
    # TODO: maybe better as just a Rule instead of its own separate thing?
    boyscout_principle: bool = False
    # maybe later: token/cost limits


class RepoConfigYaml(BaseModel):
    """
    This should have sensible defaults for workspaces with no Ellipsis config.
    """

    # shell commands agent is allowed to run
    commands: List[AgentShellCommandYaml] = []

    # general info always applied to all agents
    about: List[str] = []

    # workflow-specific
    pr_review: Optional[PrReviewBBYaml] = None
