from __future__ import annotations

from strawberry_openapi._graph_response import GraphResponse, GraphSubResponse
from strawberry_openapi._openapi import Schema
from strawberry_openapi._path import FieldSegment, Path


def test_basic():
    """{ hello }"""

    response = GraphResponse()

    data = {"hello": "world"}

    assert response.from_data(data) == {"status": 200, "data": {"hello": "world"}}


def test_multiple_statuses():
    """
    query {
        example {
            ... on A @status(code: 200) { a }
            ... on B @status(code: 418) { b }
        }
    }"""

    response = GraphResponse(
        path_to_typename=Path(
            segments=[FieldSegment("example"), FieldSegment("__typename")]
        ),
        sub_responses=[
            # status can only be on inline fragments
            GraphSubResponse(status=200, type_name="A", schema=Schema(type="object")),
            GraphSubResponse(status=418, type_name="B", schema=Schema(type="object")),
        ],
    )

    data = {"example": {"__typename": "A", "a": "a"}}

    assert response.from_data(data) == {
        "status": 200,
        "data": {"example": {"a": "a"}},
    }

    data = {"example": {"__typename": "B", "b": "b"}}

    assert response.from_data(data) == {
        "status": 418,
        "data": {"example": {"b": "b"}},
    }


def test_path_to_root():
    """
    query {
        example {
            a @root
        }
    }"""

    response = GraphResponse(
        path_to_root=Path(segments=[FieldSegment("example"), FieldSegment("a")])
    )

    data = {"example": {"a": "a"}}

    assert response.from_data(data) == {
        "status": 200,
        "data": {"a": "a"},
    }


def test_path_to_root_and_subresponse():
    """
    query {
        example {
            ... on A @status(code: 200) {
                a @root
            }
            ... on B @status(code: 418) {
                b @root
            }
        }
    }"""

    response = GraphResponse(
        path_to_typename=Path(
            segments=[FieldSegment("example"), FieldSegment("__typename")]
        ),
        sub_responses=[
            GraphSubResponse(
                status=200,
                type_name="A",
                path_to_root=Path(
                    segments=[FieldSegment("example"), FieldSegment("a")]
                ),
                schema=Schema(type="object"),
            ),
            GraphSubResponse(
                status=418,
                type_name="B",
                path_to_root=Path(
                    segments=[FieldSegment("example"), FieldSegment("b")]
                ),
                schema=Schema(type="object"),
            ),
        ],
    )

    data = {
        "example": {"__typename": "A", "a": "a"},
    }

    assert response.from_data(data) == {
        "status": 200,
        "data": {"a": "a"},
    }

    data = {
        "example": {"__typename": "B", "b": "b"},
    }

    assert response.from_data(data) == {
        "status": 418,
        "data": {"b": "b"},
    }
