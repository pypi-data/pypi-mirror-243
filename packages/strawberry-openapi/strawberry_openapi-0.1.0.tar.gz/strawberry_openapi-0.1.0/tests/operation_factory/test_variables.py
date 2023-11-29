from __future__ import annotations

import textwrap

import strawberry

from sourcetypes import graphql
from strawberry_openapi._operation import URL, Parameter, Path, Placeholder
from strawberry_openapi._operation_factory import OperationFactory


def test_scalar_variable(schema: strawberry.Schema):
    document: graphql = """
    query User($id: ID!) @endpoint(url: "/users/$id", method: "GET") {
        user(id: $id) {
            id
        }
    }
    """

    operation = OperationFactory(schema=schema).from_document(document)

    stripped: graphql = """
        query User($id: ID!) {
          user(id: $id) {
            id
          }
        }
    """

    assert str(operation.url) == "/users/$id"
    assert operation.url == URL(
        [Path(value="users"), Placeholder(name="id", type="string")]
    )

    assert operation.method == "get"
    assert operation.document == textwrap.dedent(stripped).strip()
    assert operation.name == "User"
    assert operation.request_body_schema is None

    assert operation.url_parameters == [
        Parameter.model_validate(
            {
                "name": "id",
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
            }
        )
    ]

    # response = operation.responses["200"]

    # assert response.schema.model_dump(exclude_unset=True, by_alias=True) == {
    #     "type": "object",
    #     "properties": {
    #         "user": {
    #             "type": "object",
    #             "properties": {"id": {"type": "string"}},
    #             "required": ["id"],
    #         }
    #     },
    #     "required": [],
    # }

    # assert response.path_to_root is None


def test_scalar_variable_not_in_url(schema: strawberry.Schema):
    document: graphql = """
    query User($id: ID!) @endpoint(url: "/users", method: "GET") {
        user(id: $id) {
            id
        }
    }
    """

    operation = OperationFactory(schema=schema).from_document(document)

    stripped: graphql = """
        query User($id: ID!) {
          user(id: $id) {
            id
          }
        }
    """

    assert str(operation.url) == "/users"
    assert operation.url == URL([Path(value="users")])

    assert operation.method == "get"
    assert operation.document == textwrap.dedent(stripped).strip()
    assert operation.name == "User"
    assert operation.request_body_schema
    assert operation.request_body_schema.model_dump(
        exclude_unset=True, by_alias=True
    ) == {
        "type": "object",
        "properties": {"id": {"type": "string"}},
        "required": ["id"],
    }

    assert operation.graph_response.schema
    assert operation.graph_response.schema.model_dump(
        exclude_unset=True, by_alias=True
    ) == {
        "type": "object",
        "properties": {
            "user": {
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"],
            }
        },
        "required": [],
    }


def test_object_variable(schema: strawberry.Schema):
    document: graphql = """
    mutation CreateUser($input: UserInput!) @endpoint(url: "/users", method: "POST") {
        basicCreateUser(input: $input) {
            id
        }
    }
    """

    operation = OperationFactory(schema=schema).from_document(document)

    stripped: graphql = """
        mutation CreateUser($input: UserInput!) {
          basicCreateUser(input: $input) {
            id
          }
        }
    """

    assert str(operation.url) == "/users"
    assert operation.url == URL([Path(value="users")])

    assert operation.method == "post"
    assert operation.document == textwrap.dedent(stripped).strip()
    assert operation.name == "CreateUser"

    assert operation.url_parameters is None

    assert operation.request_body_schema
    assert operation.request_body_schema.model_dump(
        exclude_unset=True, by_alias=True
    ) == {
        "type": "object",
        "properties": {"input": {"$ref": "#/components/schemas/UserInput"}},
        "required": ["input"],
    }

    assert operation.schemas.keys() == {"UserInput"}

    assert operation.schemas["UserInput"].model_dump(
        exclude_unset=True, by_alias=True
    ) == {
        "type": "object",
        "properties": {
            "age": {"type": "integer"},
            "name": {"type": "string"},
        },
        "required": ["name"],
    }


def test_object_variable_different_name(schema: strawberry.Schema):
    document: graphql = """
    mutation CreateUser($data: UserInput!) @endpoint(url: "/users", method: "POST") {
        basicCreateUser(input: $input) {
            id
        }
    }
    """

    operation = OperationFactory(schema=schema).from_document(document)

    stripped: graphql = """
        mutation CreateUser($data: UserInput!) {
          basicCreateUser(input: $input) {
            id
          }
        }
    """

    assert str(operation.url) == "/users"
    assert operation.url == URL([Path(value="users")])

    assert operation.method == "post"
    assert operation.document == textwrap.dedent(stripped).strip()
    assert operation.name == "CreateUser"

    assert operation.url_parameters is None

    assert operation.request_body_schema
    assert operation.request_body_schema.model_dump(
        exclude_unset=True, by_alias=True
    ) == {
        "type": "object",
        "properties": {"data": {"$ref": "#/components/schemas/UserInput"}},
        "required": ["data"],
    }

    assert operation.schemas.keys() == {"UserInput"}

    assert operation.schemas["UserInput"].model_dump(
        exclude_unset=True, by_alias=True
    ) == {
        "type": "object",
        "properties": {
            "age": {"type": "integer"},
            "name": {"type": "string"},
        },
        "required": ["name"],
    }


def test_with_nested_inputs():
    global UserInput, NestedInput

    @strawberry.input
    class NestedInput:
        name: str

    @strawberry.input
    class UserInput:
        age: int
        nested: NestedInput

    @strawberry.type
    class Query:
        hello: str = "strawberry"

    @strawberry.type
    class Mutation:
        @strawberry.mutation
        def create_user(self, input: UserInput) -> str:
            return "ok"

    schema = strawberry.Schema(query=Query, mutation=Mutation)

    document: graphql = """
    mutation CreateUser($input: UserInput!) @endpoint(url: "/users", method: "POST") {
        createUser(input: $input)
    }
    """

    operation = OperationFactory(schema=schema).from_document(document)

    stripped: graphql = """
        mutation CreateUser($input: UserInput!) {
          createUser(input: $input)
        }
    """

    assert str(operation.url) == "/users"
    assert operation.url == URL([Path(value="users")])

    assert operation.method == "post"
    assert operation.document == textwrap.dedent(stripped).strip()
    assert operation.name == "CreateUser"

    assert operation.url_parameters is None

    assert operation.request_body_schema
    assert operation.request_body_schema.model_dump(
        exclude_unset=True, by_alias=True
    ) == {
        "type": "object",
        "properties": {"input": {"$ref": "#/components/schemas/UserInput"}},
        "required": ["input"],
    }

    assert operation.schemas.keys() == {"UserInput", "NestedInput"}

    assert operation.schemas["UserInput"].model_dump(
        exclude_unset=True, by_alias=True
    ) == {
        "type": "object",
        "properties": {
            "age": {"type": "integer"},
            "nested": {"$ref": "#/components/schemas/NestedInput"},
        },
        "required": ["age", "nested"],
    }

    assert operation.schemas["NestedInput"].model_dump(
        exclude_unset=True, by_alias=True
    ) == {
        "type": "object",
        "properties": {"name": {"type": "string"}},
        "required": ["name"],
    }

    del UserInput, NestedInput
