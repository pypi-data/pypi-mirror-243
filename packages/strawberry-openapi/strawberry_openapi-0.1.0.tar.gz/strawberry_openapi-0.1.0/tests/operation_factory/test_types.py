from __future__ import annotations

import textwrap

import strawberry

from sourcetypes import graphql
from strawberry_openapi._operation import URL, Path
from strawberry_openapi._operation_factory import OperationFactory


def test_scalars(schema: strawberry.Schema):
    document: graphql = """
    query Hello @endpoint(url: "/hello", method: "GET") {
        hello
        float
        int
        bool
        optional
        json
        listOfInts
        listOfListsOfInts
        optionalListOfInts
        listOfOptionalInts
        date
        datetime
        time
    }
    """

    operation = OperationFactory(schema=schema).from_document(document)

    stripped: graphql = """
        query Hello {
          hello
          float
          int
          bool
          optional
          json
          listOfInts
          listOfListsOfInts
          optionalListOfInts
          listOfOptionalInts
          date
          datetime
          time
        }
    """

    assert str(operation.url) == "/hello"
    assert operation.url == URL([Path(value="hello")])

    assert operation.method == "get"
    assert operation.document == textwrap.dedent(stripped).strip()
    assert operation.name == "Hello"

    assert operation.graph_response.schema
    assert operation.graph_response.schema.model_dump(
        exclude_unset=True, by_alias=True
    ) == {
        "type": "object",
        "properties": {
            "hello": {"type": "string"},
            "float": {"type": "number"},
            "int": {"type": "integer"},
            "bool": {"type": "boolean"},
            "optional": {"type": "string"},
            "json": {"type": "object", "additionalProperties": True},
            "listOfInts": {"type": "array", "items": {"type": "integer"}},
            "listOfListsOfInts": {
                "type": "array",
                "items": {"type": "array", "items": {"type": "integer"}},
            },
            "optionalListOfInts": {
                "type": "array",
                "items": {"type": "integer"},
            },
            "listOfOptionalInts": {
                "type": "array",
                "items": {
                    "oneOf": [{"type": "integer"}, {"type": "null"}],
                },
            },
            "date": {"type": "string", "format": "date"},
            "datetime": {"type": "string", "format": "date-time"},
            "time": {"type": "string", "format": "time"},
        },
        "required": [
            "hello",
            "float",
            "int",
            "bool",
            "json",
            "listOfInts",
            "listOfListsOfInts",
            "listOfOptionalInts",
            "date",
            "datetime",
            "time",
        ],
    }


def test_object_types(schema: strawberry.Schema):
    document: graphql = """
    query Hello @endpoint(url: "/root-user", method: "GET") {
        user(id: 1) {
            id
            name
            age
        }
    }
    """

    operation = OperationFactory(schema=schema).from_document(document)

    stripped: graphql = """
        query Hello {
          user(id: 1) {
            id
            name
            age
          }
        }
    """

    assert str(operation.url) == "/root-user"
    assert operation.url == URL([Path(value="root-user")])

    assert operation.method == "get"
    assert operation.document == textwrap.dedent(stripped).strip()
    assert operation.name == "Hello"
    # assert operation.responses["200"].schema.model_dump(exclude_unset=True) == {
    #     "type": "object",
    #     "properties": {
    #         "user": {
    #             "type": "object",
    #             "properties": {
    #                 "id": {"type": "string"},
    #                 "name": {"type": "string"},
    #                 "age": {"type": "integer"},
    #             },
    #             "required": ["id", "name"],
    #         }
    #     },
    #     "required": [],
    # }


def test_list_of_object_types(schema: strawberry.Schema):
    document: graphql = """
    query Hello @endpoint(url: "/root-users", method: "GET") {
        users {
            id
            name
            age
        }
    }
    """

    operation = OperationFactory(schema=schema).from_document(document)

    stripped: graphql = """
        query Hello {
          users {
            id
            name
            age
          }
        }
    """

    assert str(operation.url) == "/root-users"
    assert operation.url == URL([Path(value="root-users")])

    assert operation.method == "get"
    assert operation.document == textwrap.dedent(stripped).strip()
    assert operation.name == "Hello"
    # assert operation.responses["200"].schema.model_dump(exclude_unset=True) == {
    #     "type": "object",
    #     "properties": {
    #         "users": {
    #             "type": "array",
    #             "items": {
    #                 "oneOf": [
    #                     {
    #                         "type": "object",
    #                         "properties": {
    #                             "id": {"type": "string"},
    #                             "name": {"type": "string"},
    #                             "age": {"type": "integer"},
    #                         },
    #                         "required": ["id", "name"],
    #                     },
    #                     {"type": "null"},
    #                 ]
    #             },
    #         }
    #     },
    #     "required": [],
    # }
