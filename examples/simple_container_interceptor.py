import time
from datetime import datetime
from di_framework import SimpleContainer
from di_framework import Lifetime
from di_framework import Interceptor


class PerformanceLoggingInterceptor(Interceptor):
    def __init__(self, instance):
        super().__init__(instance)
        self.before(self._log_start)
        self.after(self._log_end)
    
    def _log_start(self, instance, method_name, args, kwargs):
        self._start_time = time.time()
        print(f"[{datetime.now()}] Starting {instance.__class__.__name__}.{method_name}")
    
    def _log_end(self, instance, method_name, result, args, kwargs):
        duration = (time.time() - self._start_time) * 1000
        print(f"[{datetime.now()}] Completed {instance.__class__.__name__}.{method_name} "
              f"in {duration:.2f}ms")

class UserRepository:
    def get_user(self, user_id: str):
        # Simulate database query
        time.sleep(0.1)
        return {"id": user_id, "name": "Test User"}

# Configure container with interception
container = SimpleContainer()
container.register(UserRepository, Lifetime.SINGLETON)
container.register_interceptor(UserRepository, 
                             lambda instance: PerformanceLoggingInterceptor(instance))

# Use the intercepted repository
repo = container.resolve(UserRepository)
user = repo.get_user("123")