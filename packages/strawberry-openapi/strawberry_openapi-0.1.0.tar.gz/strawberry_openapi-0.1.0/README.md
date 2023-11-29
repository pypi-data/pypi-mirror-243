<img src=".github/logo.png" width="124" />

# Strawberry OpenAPI

## 🍓 Introduction

Strawberry OpenAPI is a dynamic library that bridges the gap between GraphQL and
REST APIs. Leveraging Strawberry GraphQL, this library allows developers to
create REST APIs compliant with OpenAPI specifications using GraphQL operations
and schemas. Ideal for Python developers looking to combine the best of both
GraphQL and REST worlds.

## 🚀 Features

- **GraphQL to REST**: Easily convert GraphQL operations to RESTful endpoints.
- **OpenAPI Compliance**: Generates OpenAPI specs for your REST API, ensuring
  standardization and interoperability.
- **Strawberry Integration**: Seamlessly integrates with existing Strawberry
  GraphQL schemas.
- **Customizable**: Flexible enough to suit various project needs.
- **Supports multiple frameworks**: Supports Django, FastAPI, and more!

## 🔧 Installation

```bash
pip install strawberry-openapi
```

## 🛠️ Usage

### Basic Setup

```python
from strawberry_openapi import StrawberryOpenAPI

# Create your Strawberry GraphQL schema
schema = ...

# Initialize Strawberry OpenAPI
openapi = StrawberryOpenAPI(schema, operations="./operations/**/*.graphql")


app = openapi.as_django()
```

## 📚 Documentation

For more in-depth documentation, please visit our [official documentation](#).

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](#) for more
information.

## 📄 License

This project is licensed under the [MIT License](#).

---

Feel free to fork, star, and contribute! Let's make API development easier and
more efficient together! 🌟🚀🍓
