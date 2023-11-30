from pydantic import BaseModel

# TODO unused for now
# class CommandType(Enum):
#     BUILD = "BUILD"
#     RUN_TESTS = "RUN_TESTS"


class AgentShellCommandYaml(BaseModel):
    """
    All commands are executed from the repo root.
    """

    # cmd_type: CommandType
    name: str  # TODO(nick) is it required to be one word?
    description: str
    command: str  # the prefix of the command, without args
    return_output_on_success: bool = True


class CommandOutput(BaseModel):
    exit_code: int
    all_output: str
    # stdout: Optional[str]
    # stderr: Optional[str]
