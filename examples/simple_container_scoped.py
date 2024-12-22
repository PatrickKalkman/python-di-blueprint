from di_framework import SimpleContainer
from di_framework import Lifetime
from uuid import uuid4


class UserContext:
    def __init__(self):
        self.request_id = str(uuid4())
        self.current_user = None


class AuditLogger:
    def __init__(self, context: UserContext):
        self.context = context

    def log_action(self, action: str):
        print(f"[Request {self.context.request_id}] "
              f"User {self.context.current_user}: {action}")


class UserService:
    def __init__(self, context: UserContext, logger: AuditLogger):
        self.context = context
        self.logger = logger

    def perform_action(self, action: str):
        self.logger.log_action(action)


# Configure container
container = SimpleContainer()
container.register(UserContext, Lifetime.SCOPED)
container.register(AuditLogger, Lifetime.SCOPED)
container.register(UserService, Lifetime.TRANSIENT)


# Simulate request handling
def handle_request(username: str, action: str):
    with container.create_scope():
        service = container.resolve(UserService)
        service.context.current_user = username
        service.perform_action(action)


# Simulate multiple requests
handle_request("alice", "view_profile")
handle_request("bob", "update_settings")
