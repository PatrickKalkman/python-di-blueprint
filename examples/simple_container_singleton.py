from di_framework import SimpleContainer
from di_framework import Lifetime


class DatabaseConnection:
    def __init__(self):
        # We'll use the object's memory address to prove singleton behavior
        self.connection_id = id(self)

    def get_connection_info(self):
        return f"Connection ID: {self.connection_id}"


class UserRepository:
    def __init__(self, db: DatabaseConnection):
        self.db = db


# Configure our container
container = SimpleContainer()
container.register(DatabaseConnection, Lifetime.SINGLETON)
container.register(UserRepository, Lifetime.TRANSIENT)

# Create multiple repositories
repository1 = container.resolve(UserRepository)
repository2 = container.resolve(UserRepository)

# Verify singleton behavior
print(repository1.db.get_connection_info())
print(repository2.db.get_connection_info())
print(repository1.db is repository2.db)
