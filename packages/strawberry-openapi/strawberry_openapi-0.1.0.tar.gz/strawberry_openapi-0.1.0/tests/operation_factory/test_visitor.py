from __future__ import annotations

import textwrap

import strawberry

from sourcetypes import graphql
from strawberry_openapi._operation_factory import OperationFactory


def test_creates_graph_response(schema: strawberry.Schema):
    factory = OperationFactory(
        schema=schema,
    )

    document: graphql = """
    query Hello @endpoint(url: "/hello", method: "GET") {
        hello
    }
    """

    operation = factory.from_document(document)

    assert operation.graph_response.status == 200
    assert operation.graph_response.path_to_root is None
    assert operation.graph_response.sub_responses == []
    assert operation.graph_response.schema
    assert operation.graph_response.schema.model_dump(
        exclude_unset=True, by_alias=True
    ) == {
        "type": "object",
        "properties": {"hello": {"type": "string"}},
        "required": ["hello"],
    }

    assert operation.graph_response.from_data({"hello": "world"}) == {
        "status": 200,
        "data": {"hello": "world"},
    }


def test_creates_graph_response_with_path_to_root(schema: strawberry.Schema):
    factory = OperationFactory(
        schema=schema,
    )

    document: graphql = """
    query User @endpoint(url: "/user", method: "GET") {
        user(id: 1) {
            id @root
        }
    }
    """

    operation = factory.from_document(document)

    assert (
        operation.document
        == textwrap.dedent(
            """
            query User {
              user(id: 1) {
                id
              }
            }
            """
        ).strip()
    )

    assert operation.graph_response.status == 200
    assert operation.graph_response.path_to_root
    assert operation.graph_response.path_to_root.fields == ["user", "id"]
    assert operation.graph_response.sub_responses == []
    assert operation.graph_response.schema
    assert operation.graph_response.schema.model_dump(
        exclude_unset=True, by_alias=True
    ) == {
        "type": "object",
        "properties": {"id": {"type": "string"}},
        "required": ["id"],
    }

    assert operation.graph_response.from_data({"user": {"id": "1"}}) == {
        "status": 200,
        "data": {"id": "1"},
    }


def test_union_without_status(schema: strawberry.Schema):
    factory = OperationFactory(
        schema=schema,
    )

    document: graphql = """
    query FeedItem @endpoint(url: "/user", method: "GET") {
        feedItem {
            ... on Article {
                id
            }
            ... on Photo {
                id
            }
        }
    }
    """

    operation = factory.from_document(document)

    assert (
        operation.document
        == textwrap.dedent(
            """
            query FeedItem {
              feedItem {
                ... on Article {
                  id
                }
                ... on Photo {
                  id
                }
              }
            }
            """
        ).strip()
    )

    assert operation.graph_response.status == 200
    assert operation.graph_response.path_to_typename is None
    assert operation.graph_response.sub_responses == []
    assert operation.graph_response.schema
    assert operation.graph_response.schema.model_dump(
        exclude_unset=True, by_alias=True
    ) == {
        "type": "object",
        "properties": {
            "feedItem": {
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                        "required": ["id"],
                    },
                    {
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                        "required": ["id"],
                    },
                ]
            }
        },
        "required": ["feedItem"],
    }

    assert operation.graph_response.from_data({"feedItem": {"id": "1"}}) == {
        "status": 200,
        "data": {"feedItem": {"id": "1"}},
    }


def test_creates_graph_response_with_path_to_typename(schema: strawberry.Schema):
    factory = OperationFactory(
        schema=schema,
    )

    document: graphql = """
    query FeedItem @endpoint(url: "/user", method: "GET") {
        feedItem {
            ... on Article @status(code: 200) {
                id
            }
            ... on Photo @status(code: 418) {
                id
            }
        }
    }
    """

    operation = factory.from_document(document)

    assert (
        operation.document
        == textwrap.dedent(
            """
            query FeedItem {
              feedItem {
                __typename
                ... on Article {
                  id
                }
                ... on Photo {
                  id
                }
              }
            }
            """
        ).strip()
    )

    assert operation.graph_response.status == 200
    assert operation.graph_response.path_to_typename
    assert operation.graph_response.path_to_typename.fields == [
        "feedItem",
        "__typename",
    ]
    assert operation.graph_response.schema is None
    sub_responses = operation.graph_response.sub_responses

    assert sub_responses[0].status == 200
    assert sub_responses[0].type_name == "Article"
    assert sub_responses[0].path_to_root is None
    assert sub_responses[0].schema
    assert sub_responses[0].schema.model_dump(exclude_unset=True, by_alias=True) == {
        "type": "object",
        "properties": {
            "feedItem": {
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"],
            }
        },
        "required": ["feedItem"],
    }
    assert sub_responses[1].status == 418
    assert sub_responses[1].type_name == "Photo"
    assert sub_responses[1].path_to_root is None
    assert sub_responses[1].schema
    assert sub_responses[1].schema.model_dump(exclude_unset=True, by_alias=True) == {
        "type": "object",
        "properties": {
            "feedItem": {
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"],
            }
        },
        "required": ["feedItem"],
    }

    assert operation.graph_response.from_data(
        {"feedItem": {"id": "1", "__typename": "Article"}}
    ) == {"status": 200, "data": {"feedItem": {"id": "1"}}}

    assert operation.graph_response.from_data(
        {"feedItem": {"id": "1", "__typename": "Photo"}}
    ) == {"status": 418, "data": {"feedItem": {"id": "1"}}}


def test_creates_graph_response_with_path_to_typename_and_path_to_root(
    schema: strawberry.Schema,
):
    factory = OperationFactory(
        schema=schema,
    )

    document: graphql = """
    query FeedItem @endpoint(url: "/user", method: "GET") {
        feedItem {
            ... on Article @status(code: 200) {
                id @root
            }
            ... on Photo @status(code: 418) {
                id @root
            }
        }
    }
    """

    operation = factory.from_document(document)

    assert (
        operation.document
        == textwrap.dedent(
            """
            query FeedItem {
              feedItem {
                __typename
                ... on Article {
                  id
                }
                ... on Photo {
                  id
                }
              }
            }
            """
        ).strip()
    )

    assert operation.graph_response.status == 200
    assert operation.graph_response.path_to_typename
    assert operation.graph_response.path_to_typename.fields == [
        "feedItem",
        "__typename",
    ]
    sub_responses = operation.graph_response.sub_responses

    assert sub_responses[0].status == 200
    assert sub_responses[0].type_name == "Article"
    assert sub_responses[0].path_to_root
    assert sub_responses[0].path_to_root.fields == ["feedItem", "id"]
    assert sub_responses[1].status == 418
    assert sub_responses[1].type_name == "Photo"
    assert sub_responses[1].path_to_root
    assert sub_responses[1].path_to_root.fields == ["feedItem", "id"]

    assert operation.graph_response.from_data(
        {"feedItem": {"id": "1", "__typename": "Article"}}
    ) == {"status": 200, "data": {"id": "1"}}

    assert operation.graph_response.from_data(
        {"feedItem": {"id": "1", "__typename": "Photo"}}
    ) == {"status": 418, "data": {"id": "1"}}
