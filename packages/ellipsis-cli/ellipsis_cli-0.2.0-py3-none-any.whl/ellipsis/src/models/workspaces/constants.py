LISTENER_PORT = 65455
EVENTS_URL_ROUTE = "/events"
HEALTH_CHECK_URL_ROUTE = "/healthcheck"  # Do NOT call this "/health" or else things don't work for reasons I don't understand
READ_FILE_URL_ROUTE = "/read_file"
WRITE_FILE_URL_ROUTE = "/write_file"
RUN_COMMAND_URL_ROUTE = "/run_command"

# TODO(nick) later this is going into env variables per-customer, eventually oauth
WORKSPACE_AUTH_TOKEN = "bb_32156e276c55073aa0a38d4abf4c92544e0962bebd6f828"
