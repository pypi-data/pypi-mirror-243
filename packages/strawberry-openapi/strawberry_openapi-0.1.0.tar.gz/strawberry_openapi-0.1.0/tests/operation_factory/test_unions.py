from __future__ import annotations

import textwrap

import strawberry

from sourcetypes import graphql
from strawberry_openapi._operation import URL, Path
from strawberry_openapi._operation_factory import OperationFactory


def test_union_types(schema: strawberry.Schema):
    document: graphql = """
    query Hello @endpoint(url: "/feed-item", method: "GET") {
        feedItem(id: 1) {
            ... on Article {
                id
                title
                content
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
              title
              content
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
    #                 {
    #                     "type": "object",
    #                     "properties": {
    #                         "id": {"type": "string"},
    #                         "title": {"type": "string"},
    #                         "content": {"type": "string"},
    #                     },
    #                     "required": ["id", "title", "content"],
    #                 },
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


def test_list_unions(schema: strawberry.Schema):
    document: graphql = """
    query Hello @endpoint(url: "/feed", method: "GET") {
        feed {
            ... on Article {
                id
                title
                content
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
          feed {
            ... on Article {
              id
              title
              content
            }
            ... on Photo {
              id
              url
            }
          }
        }
    """

    assert str(operation.url) == "/feed"
    assert operation.url == URL([Path(value="feed")])

    assert operation.method == "get"
    assert operation.document == textwrap.dedent(stripped).strip()
    assert operation.name == "Hello"
    # assert operation.responses["200"].schema.model_dump(exclude_unset=True) == {
    #     "type": "object",
    #     "properties": {
    #         "feed": {
    #             "type": "array",
    #             "items": {
    #                 "oneOf": [
    #                     {
    #                         "type": "object",
    #                         "properties": {
    #                             "id": {"type": "string"},
    #                             "title": {"type": "string"},
    #                             "content": {"type": "string"},
    #                         },
    #                         "required": ["id", "title", "content"],
    #                     },
    #                     {
    #                         "type": "object",
    #                         "properties": {
    #                             "id": {"type": "string"},
    #                             "url": {"type": "string"},
    #                         },
    #                         "required": ["id", "url"],
    #                     },
    #                     {"type": "null"},
    #                 ]
    #             },
    #         }
    #     },
    #     "required": [],
    # }
