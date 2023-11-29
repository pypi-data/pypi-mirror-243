# pyright: reportPrivateUsage=false

from __future__ import annotations

import json

import strawberry

from django.test import RequestFactory

from sourcetypes import graphql
from strawberry_openapi.django import DjangoOpenAPI


def test_returns_404(schema: strawberry.Schema, rf: RequestFactory):
    api = DjangoOpenAPI(schema=schema, documents=[])

    request = rf.get("/hello")

    response = api._view(request, operation=None)

    assert response.status_code == 404


def test_basic(schema: strawberry.Schema, rf: RequestFactory):
    operation: graphql = """
    query Hello @endpoint(url: "/hello", method: "GET") {
        helloWorld
    }
    """

    api = DjangoOpenAPI(schema=schema, documents=[operation])

    request = rf.get("/hello")

    response = api._view(request, operation=api.operations[0])

    assert response.status_code == 200
    assert json.loads(response.content) == {"helloWorld": "Hello, world!"}


def test_basic_with_variables_in_url(schema: strawberry.Schema, rf: RequestFactory):
    operation: graphql = """
    query User($id: ID!) @endpoint(url: "/users/$id", method: "GET") {
        user(id: $id) {
            id
        }
    }
    """

    api = DjangoOpenAPI(schema=schema, documents=[operation])

    request = rf.get("/users/1")

    response = api._view(request, operation=api.operations[0], id="1")

    assert response.status_code == 200
    assert json.loads(response.content) == {"user": {"id": "1"}}


def test_variables_in_request_body(schema: strawberry.Schema, rf: RequestFactory):
    operation: graphql = """
    mutation CreateUser($input: UserInput!) @endpoint(url: "/users", method: "POST") {
        basicCreateUser(input: $input) {
            id
            name
        }
    }
    """

    api = DjangoOpenAPI(schema=schema, documents=[operation])

    request = rf.post(
        "/users", data={"input": {"name": "Patrick"}}, content_type="application/json"
    )

    response = api._view(request, operation=api.operations[0])

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "basicCreateUser": {"id": "1", "name": "Patrick"}
    }


def test_root_in_mutation(schema: strawberry.Schema, rf: RequestFactory):
    operation: graphql = """
    mutation CreateUser($input: UserInput!) @endpoint(url: "/users", method: "POST") {
        basicCreateUser(input: $input) {
            id @root
        }
    }
    """

    api = DjangoOpenAPI(schema=schema, documents=[operation])

    request = rf.post(
        "/users", data={"input": {"name": "Patrick"}}, content_type="application/json"
    )

    response = api._view(request, operation=api.operations[0])

    assert response.status_code == 200
    assert json.loads(response.content) == {"id": "1"}


def test_union(schema: strawberry.Schema, rf: RequestFactory):
    operation: graphql = """
    mutation CreateUser($input: UserInput!) @endpoint(url: "/users", method: "POST") {
        createUser(input: $input) {
            ... on CreateUserSuccess {
                user {
                    id
                    name
                }
            }
            ... on CreateUserError {
                message
            }
        }
    }
    """

    api = DjangoOpenAPI(schema=schema, documents=[operation])

    request = rf.post(
        "/users", data={"input": {"name": "Patrick"}}, content_type="application/json"
    )

    response = api._view(request, operation=api.operations[0])

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "createUser": {
            "user": {"id": "1", "name": "Patrick"},
        }
    }


def test_error(schema: strawberry.Schema, rf: RequestFactory):
    operation: graphql = """
    query Hello @endpoint(url: "/hello", method: "GET") {
        thisRaisesAnError
    }
    """

    api = DjangoOpenAPI(schema=schema, documents=[operation])

    request = rf.get("/hello")

    response = api._view(request, operation=api.operations[0])

    assert response.status_code == 500
    assert json.loads(response.content) == {
        "errors": ["This is an error"],
    }
