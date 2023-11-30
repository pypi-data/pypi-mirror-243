import json
import os
import shlex
import subprocess
from typing import Mapping, Optional

import yaml
from diff_match_patch import diff_match_patch
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from loguru import logger

from ellipsis.src.models.workspaces.command import CommandOutput
from ellipsis.src.models.workspaces.constants import (
    EVENTS_URL_ROUTE,
    HEALTH_CHECK_URL_ROUTE,
    READ_FILE_URL_ROUTE,
    RUN_COMMAND_URL_ROUTE,
    WORKSPACE_AUTH_TOKEN,
    WRITE_FILE_URL_ROUTE,
)
from ellipsis.src.models.workspaces.models import (
    BaseWorkspaceRequest,
    FileChangeRequest,
    FileChangeResponse,
    FileReadRequest,
    FileReadResponse,
    FileWriteRequest,
    FileWriteResponse,
    RejectedResponse,
    RunCommandRequest,
    RunCommandResponse,
    WorkspaceRequestType,
)
from ellipsis.src.models.workspaces.workspace_config import (
    WORKSPACE_CONFIG_YAML_FILE_NAME,
    RepoConfigYaml,
)


class CloudDevEnvListener:
    
    def __init__(self, repo_root: str, auth_token: Optional[str] = None):
        self.repo_root = repo_root
        self.auth_token = auth_token
        logger.debug(f"Repo root is '{self.repo_root}'")
        self.config = self._load_config()
        # TODO(nick) might be better to make this idempotent
        os.chdir(self.repo_root)


    def _load_config(self):
        config_path = os.path.join(self.repo_root, WORKSPACE_CONFIG_YAML_FILE_NAME)
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f)
            config = RepoConfigYaml(**config_data)
            logger.debug(f"Loaded config: {config}")
            return config
        else:
            logger.debug(f"Config file '{config_path}' does not exist.")
            return None

    def create_fastapi_app(self):
        app = FastAPI()

        if self.auth_token is not None:
            logger.debug(f"Using auth token: {self.auth_token}")

            @app.middleware("http")
            async def validate_auth_header(request: Request, call_next):
                logger.debug(
                    f"Validating auth header for {request.url} with headers: {request.headers}"
                )
                auth_header = request.headers.get("Authorization")
                if auth_header is None or not auth_header.startswith("Bearer "):
                    return JSONResponse(
                        content={"detail": "Authorization header missing or incorrect"},
                        status_code=401,
                    )
                token = auth_header.split(" ", 1)[1]
                if token != self.auth_token:
                    return JSONResponse(
                        content={"detail": "Invalid token"},
                        status_code=401,
                    )
                response = await call_next(request)
                return response
        else:
            logger.debug("No auth token set, anyone can access the listener.")

        @app.get(HEALTH_CHECK_URL_ROUTE)
        async def health_check():
            return {
                "ok": True,
                'directory': self.repo_root,
                'pid': os.getpid(),
                "config": self.config.dict() if self.config else None
            }

        @app.post(READ_FILE_URL_ROUTE, response_model=FileReadResponse)
        async def read_file(req: FileReadRequest):
            effective_file_path = os.path.join(self.repo_root, req.path)
            if not os.path.exists(effective_file_path):
                logger.debug(f"File '{effective_file_path}' does not exist.")
                return FileReadResponse(contents=None)
            with open(effective_file_path, "r") as f:
                logger.debug(f"Found file at '{effective_file_path}'")
                contents = f.read()
                # logger.debug(f"Contents:\n```{effective_file_path}\n{contents}\n```")
                return FileReadResponse(contents=contents)

        @app.post(WRITE_FILE_URL_ROUTE, response_model=FileWriteResponse)
        async def write_file(req: FileWriteRequest):
            effective_file_path = os.path.join(self.repo_root, req.path)
            if not os.path.exists(effective_file_path):
                logger.info(f"File '{req.path}' does not exist, creating it.")
                os.makedirs(os.path.dirname(effective_file_path), exist_ok=True)
                with open(effective_file_path, "w") as f:
                    f.write("")
            with open(effective_file_path, "w") as f:
                f.write(req.contents)
            logger.info(f"File '{req.path}' updated successfully.")
            return FileWriteResponse()

        @app.post(RUN_COMMAND_URL_ROUTE, response_model=RunCommandResponse)
        async def run_command(req: RunCommandRequest):
            split_cmd = shlex.split(req.command_str)
            logger.debug(f"Running cmd from {self.repo_root}: $ {req.command_str}")
            result = subprocess.run(
                split_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            output = result.stdout
            return RunCommandResponse(
                ok=True,
                req=req,
                output=CommandOutput(
                    exit_code=result.returncode,
                    all_output=output,
                ),
            )
            # inner = self._handle_RunCommandRequest(req)
            # logger.debug(f"Returning response: {inner}")
            # return inner

        # TODO this isn't working yet
        @app.websocket(EVENTS_URL_ROUTE)
        async def websocket_endpoint(websocket: WebSocket):
            n_events = 0
            await websocket.accept()
            try:
                while True:
                    msg = await websocket.receive_text()
                    n_events += 1
                    if msg.lower() == "close":
                        await websocket.close()
                        break
                    else:
                        try:
                            event_json = json.loads(msg)
                        except json.JSONDecodeError:
                            logger.error(f"Failed to parse JSON: {msg}")
                            await websocket.send_json(
                                RejectedResponse(
                                    ok=False, reason=f"Failed to parse JSON: {msg}"
                                )
                            )
                            continue
                        req = BaseWorkspaceRequest.parse_obj(event_json)
                        if req.request_type == WorkspaceRequestType.FILE_CHANGE:
                            change_file_event: FileChangeRequest = (
                                FileChangeRequest.parse_obj(event_json)
                            )
                            await websocket.send_json(
                                self._handle_FileChangeRequest(change_file_event)
                            )
                        elif req.request_type == WorkspaceRequestType.RUN_COMMAND:
                            pass
                            # run_command_event: RunCommandRequest = (
                            #     RunCommandRequest.parse_obj(event_json)
                            # )
                            # await websocket.send_json(
                            #     self._handle_RunCommandRequest(run_command_event)
                            # )
                        else:
                            logger.info(
                                f"Event type {req.request_type} is not supported: {event_json}"
                            )
                            await websocket.send_json(
                                RejectedResponse(
                                    ok=False,
                                    reason=f"Event type {req.request_type} is not supported",
                                )
                            )
            except WebSocketDisconnect:
                logger.warning(f"Server disconnected after {n_events} events")

        return app

    def _handle_FileChangeRequest(self, e: FileChangeRequest) -> FileChangeResponse:
        effective_file_path = os.path.join(self.repo_root, e.path)
        if not os.path.exists(effective_file_path):
            logger.info(f"File {e.path} does not exist, creating it.")
            os.makedirs(os.path.dirname(effective_file_path), exist_ok=True)
            with open(effective_file_path, "w") as f:
                f.write("")
        with open(effective_file_path, "r") as f:
            text = f.read()
        dmp = diff_match_patch()
        patches = dmp.patch_fromText(e.diff)
        new_text, _ = dmp.patch_apply(patches, text)

        with open(effective_file_path, "w") as f:
            f.write(new_text)
        logger.info(f"File {e.path} updated successfully.")
        return FileChangeResponse(
            ok=True,
            req=e,
        )

    # TODO(nick) how to get stdout and stderr simultaneously?
    # def _handle_RunCommandRequest(
    #     self, event: RunCommandRequest
    # ) -> RunCommandResponse | RejectedResponse:
    #     """
    #     Runs a command and returns the response.
    #     """
    #     pwd = self.repo_root
    #     logger.info(f"Running command '{event.command_str}' in {pwd}")
    #     os.chdir(pwd)
    #     try:
    #         completed_process = run(event.command_str, shell=True, check=True)
    #     except CalledProcessError as err:
    #         logger.warning(f"Command '{event.command_str}' failed.")
    #         return RejectedResponse(
    #             ok=False, reason=f"Command '{event.command_str}' failed: {err}"
    #         )
    #     return RunCommandResponse(
    #         ok=True,
    #         req=event,
    #         output=CommandOutput(
    #             exit_code=completed_process.returncode,
    #             all_output="", # TODO
    #             stdout=str(completed_process.stdout)
    #             if completed_process.stdout
    #             else None,
    #             stderr=str(completed_process.stderr)
    #             if completed_process.stderr
    #             else None,
    #         ),
    #     )
    