from di_framework import SimpleContainer, Lifetime


class RequestContext:
    def __init__(self):
        self.context_id = id(self)
        self.data = {}

    def set_data(self, key: str, value: str):
        self.data[key] = value

    def get_context_info(self):
        return f"Context ID: {self.context_id}, Data: {self.data}"


class UserService:
    def __init__(self, context: RequestContext):
        self.context = context


# Configure our container
container = SimpleContainer()
container.register(RequestContext, Lifetime.TRANSIENT)
container.register(UserService, Lifetime.TRANSIENT)

# Create multiple services
service1 = container.resolve(UserService)
service2 = container.resolve(UserService)

# Demonstrate isolation
service1.context.set_data("user", "Alice")
service2.context.set_data("user", "Bob")

print(service1.context.get_context_info())
print(service2.context.get_context_info())
print(service1.context is service2.context)  # Will print False
