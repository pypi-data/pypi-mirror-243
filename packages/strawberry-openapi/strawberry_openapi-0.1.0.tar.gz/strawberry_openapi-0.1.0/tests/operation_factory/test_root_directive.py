from __future__ import annotations

import textwrap

import strawberry

from sourcetypes import graphql
from strawberry_openapi._operation import URL, Path
from strawberry_openapi._operation_factory import OperationFactory


def test_object_types(schema: strawberry.Schema):
    document: graphql = """
    query UserId @endpoint(url: "/root-user-id", method: "GET") {
        user(id: 1) {
            id @root
        }
    }
    """

    operation = OperationFactory(schema=schema).from_document(document)

    stripped: graphql = """
        query UserId {
          user(id: 1) {
            id
          }
        }
    """

    assert str(operation.url) == "/root-user-id"
    assert operation.url == URL([Path(value="root-user-id")])

    assert operation.method == "get"
    assert operation.document == textwrap.dedent(stripped).strip()
    assert operation.name == "UserId"
    assert operation.url_parameters is None
    assert operation.request_body_schema is None

    assert operation.graph_response.schema
    assert operation.graph_response.schema.model_dump(exclude_unset=True) == {
        "type": "object",
        "properties": {"id": {"type": "string"}},
        "required": ["id"],
    }

    assert operation.graph_response.path_to_root
    assert operation.graph_response.path_to_root.fields == ["user", "id"]


def test_union_with_root_directive(schema: strawberry.Schema):
    document: graphql = """
    query Hello @endpoint(url: "/feed-item", method: "GET") {
        feedItem(id: 1) {
            ... on Article {
                id @root
            }
            ... on Photo {
                id
                url
            }
        }
    }
    """

    operation = OperationFactory(schema=schema).from_document(document)

    stripped: graphql = """
        query Hello {
          feedItem(id: 1) {
            ... on Article {
              id
            }
            ... on Photo {
              id
              url
            }
          }
        }
    """

    assert str(operation.url) == "/feed-item"
    assert operation.url == URL([Path(value="feed-item")])

    assert operation.method == "get"
    assert operation.document == textwrap.dedent(stripped).strip()
    assert operation.name == "Hello"
    # assert operation.responses["200"].schema.model_dump(exclude_unset=True) == {
    #     "type": "object",
    #     "properties": {
    #         "feedItem": {
    #             "oneOf": [
    #                 {"type": "string"},
    #                 {
    #                     "type": "object",
    #                     "properties": {
    #                         "id": {"type": "string"},
    #                         "url": {"type": "string"},
    #                     },
    #                     "required": ["id", "url"],
    #                 },
    #             ]
    #         }
    #     },
    #     "required": ["feedItem"],
    # }
