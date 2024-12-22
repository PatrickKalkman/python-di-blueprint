# Python DI Blueprint

A hands-on implementation of a Dependency Injection container in Python, demonstrating core DI concepts through practical examples. This educational project explores three fundamental dimensions of Dependency Injection:
- Composition
- Lifecycle Management
- Interception

## Prerequisites

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Install uv using the official installer:

On Unix-based systems:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

Clone the repository and install dependencies:

```bash
# Clone the repository
git clone https://github.com/yourusername/python-di-blueprint.git
cd python-di-blueprint

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

## Usage Examples

The framework provides several components demonstrating different aspects of Dependency Injection. Here's a basic example showing composition:

```python
from di_framework import SimpleContainer
from di_framework.examples.basic_usage import Repository, Service

# Initialize container
container = SimpleContainer()

# Register dependencies
container.register(Repository)
container.register(Service)

# Resolve and use the service
service = container.resolve(Service)
data = service.get_data()
```

For lifecycle management, the framework supports different instance lifetimes:

```python
from di_framework import SimpleContainer, Lifetime
from di_framework.examples.lifecycle_demo import DatabaseConnection

# Configure container with lifecycle management
container = SimpleContainer()
container.register(DatabaseConnection, Lifetime.SINGLETON)
```

To run the complete examples:

```bash
# Lifecycle management Singleton
uv run ./examples/simple_container_singleton.py

# Lifecycle management Transient
uv run ./examples/simple_container_transient.py

# Interception patterns
uv run ./examples/simple_container_interceptor.py
```

## Project Structure

```
python-di-blueprint/
├── src/di_framework/      # Core implementation
├── tests/                 # Test suite
└── examples/              # Usage examples
```

## Documentation

This implementation accompanies a detailed article series about building a DI container from scratch. For comprehensive understanding of the concepts and implementation details, refer to:

- [Building your own DI framework in Python](your-article-link)
- [Understanding Dependency Injection Patterns](your-article-link)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.