# pyright: reportPrivateUsage=false
from __future__ import annotations

import strawberry

from sourcetypes import graphql
from strawberry_openapi.django import DjangoOpenAPI


def test_empty(schema: strawberry.Schema):
    api = DjangoOpenAPI(schema=schema, documents=[])

    assert len(api.paths) == 1

    url_path = api.paths[0]
    assert url_path.callback == api._openapi_view


def test_simple_path(schema: strawberry.Schema):
    operation: graphql = """
    query Hello @endpoint(url: "/hello", method: "GET") {
        helloWorld
    }
    """

    api = DjangoOpenAPI(schema=schema, documents=[operation])

    assert len(api.paths) == 2

    url_path = api.paths[0]

    assert url_path.callback == api._view
    assert url_path.default_args == {"operation": api.operations[0]}
    assert url_path.pattern._route == "hello"


def test_path_with_variables(schema: strawberry.Schema):
    operation: graphql = """
    query User($id: ID!) @endpoint(url: "/users/$id", method: "GET") {
        user(id: $id) {
            id
        }
    }
    """

    api = DjangoOpenAPI(schema=schema, documents=[operation])

    assert len(api.paths) == 2
    url_path = api.paths[0]

    assert url_path.callback == api._view
    assert url_path.default_args == {"operation": api.operations[0]}
    assert url_path.pattern._route == "users/<str:id>"
