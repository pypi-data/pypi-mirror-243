from __future__ import annotations

import strawberry

from openapi_spec_validator import validate
from sourcetypes import graphql
from strawberry_openapi import StrawberryOpenAPI


def test_open_api(schema: strawberry.Schema):
    document: graphql = """
    query Hello @endpoint(url: "/hello", method: "GET") {
        helloWorld
    }
    """

    api = StrawberryOpenAPI(schema=schema, documents=[document])

    openapi_schema = api.openapi_schema.model_dump(exclude_unset=True, by_alias=True)

    validate(openapi_schema)  # type: ignore

    assert openapi_schema == {
        "info": {"title": "Strawberry API", "version": "1.0.0"},
        "openapi": "3.1.0",
        "servers": [],
        "paths": {
            "/hello": {
                "get": {
                    "operationId": "Hello",
                    "responses": {
                        "200": {
                            "description": "",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "helloWorld": {"type": "string"}
                                        },
                                        "required": ["helloWorld"],
                                    }
                                },
                            },
                        }
                    },
                }
            }
        },
    }


def test_open_api_input_types_in_path(schema: strawberry.Schema):
    document: graphql = """
    query User($id: ID!) @endpoint(url: "/users/$id", method: "GET") {
        user(id: $id) {
            id
        }
    }
    """

    api = StrawberryOpenAPI(schema=schema, documents=[document])

    openapi_schema = api.openapi_schema.model_dump(exclude_unset=True, by_alias=True)

    validate(openapi_schema)  # type: ignore

    assert openapi_schema == {
        "info": {"title": "Strawberry API", "version": "1.0.0"},
        "openapi": "3.1.0",
        "servers": [],
        "paths": {
            "/users/{id}": {
                "get": {
                    "operationId": "User",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"type": "string"},
                            "in": "path",
                            "name": "id",
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "user": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"}
                                                },
                                                "required": ["id"],
                                            },
                                        },
                                        "required": [],
                                    },
                                },
                            },
                        },
                    },
                }
            },
        },
    }


def test_input_types_request_body(schema: strawberry.Schema):
    document: graphql = """
    mutation SayHello($name: String!) @endpoint(url: "/users", method: "POST") {
        sayHello(name: $name)
    }
    """

    api = StrawberryOpenAPI(schema=schema, documents=[document])

    openapi_schema = api.openapi_schema.model_dump(exclude_unset=True, by_alias=True)

    validate(openapi_schema)  # type: ignore

    assert openapi_schema == {
        "info": {"title": "Strawberry API", "version": "1.0.0"},
        "openapi": "3.1.0",
        "servers": [],
        "paths": {
            "/users": {
                "post": {
                    "operationId": "SayHello",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                        }
                                    },
                                    "required": ["name"],
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {"sayHello": {"type": "string"}},
                                        "required": ["sayHello"],
                                    }
                                },
                            },
                        }
                    },
                }
            }
        },
    }


def test_open_api_with_status(schema: strawberry.Schema):
    document: graphql = """
    query User @endpoint(url: "/user", method: "GET") {
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

    api = StrawberryOpenAPI(schema=schema, documents=[document])

    openapi_schema = api.openapi_schema.model_dump(exclude_unset=True, by_alias=True)

    validate(openapi_schema)  # type: ignore

    assert openapi_schema == {
        "info": {"title": "Strawberry API", "version": "1.0.0"},
        "openapi": "3.1.0",
        "servers": [],
        "paths": {
            "/user": {
                "get": {
                    "operationId": "User",
                    "responses": {
                        "200": {
                            "description": "",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "feedItem": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"}
                                                },
                                                "required": ["id"],
                                            },
                                        },
                                        "required": ["feedItem"],
                                    }
                                },
                            },
                        },
                        "418": {
                            "description": "",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "feedItem": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"}
                                                },
                                                "required": ["id"],
                                            },
                                        },
                                        "required": ["feedItem"],
                                    }
                                },
                            },
                        },
                    },
                }
            }
        },
    }


def test_inputs_with_lists(schema: strawberry.Schema):
    document: graphql = """
    mutation Echo($input: [EchoInput!]!) @endpoint(url: "/echo", method: "POST") {
        echo(input: $input)
    }
    """

    api = StrawberryOpenAPI(schema=schema, documents=[document])

    openapi_schema = api.openapi_schema.model_dump(exclude_unset=True, by_alias=True)

    validate(openapi_schema)  # type: ignore

    assert openapi_schema == {
        "info": {"title": "Strawberry API", "version": "1.0.0"},
        "openapi": "3.1.0",
        "servers": [],
        "paths": {
            "/echo": {
                "post": {
                    "operationId": "Echo",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "input": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/EchoInput"
                                            },
                                        }
                                    },
                                    "required": ["input"],
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {"echo": {"type": "string"}},
                                        "required": ["echo"],
                                    }
                                },
                            },
                        }
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "EchoInput": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                    },
                    "required": ["text"],
                },
            }
        },
    }


def test_open_api_input_types_in_path_and_request_body(schema: strawberry.Schema):
    document: graphql = """
    mutation SayHelloToUser($id: ID!, $input: SayHelloInput!)
        @endpoint(url: "/users/$id/say-hello", method: "POST") {
        sayHelloToUser(id: $id, input: $input) {
            greeting
        }
    }
    """

    api = StrawberryOpenAPI(schema=schema, documents=[document])

    openapi_schema = api.openapi_schema.model_dump(exclude_unset=True, by_alias=True)

    validate(openapi_schema)  # type: ignore

    assert openapi_schema == {
        "info": {"title": "Strawberry API", "version": "1.0.0"},
        "openapi": "3.1.0",
        "servers": [],
        "paths": {
            "/users/{id}/say-hello": {
                "post": {
                    "operationId": "SayHelloToUser",
                    "parameters": [
                        {
                            "required": True,
                            "schema": {"type": "string"},
                            "in": "path",
                            "name": "id",
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "input": {
                                            "$ref": "#/components/schemas/SayHelloInput"
                                        }
                                    },
                                    "required": ["input"],
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "sayHelloToUser": {
                                                "type": "string",
                                            },
                                        },
                                        "required": ["sayHelloToUser"],
                                    },
                                },
                            },
                        },
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "SayHelloInput": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                    },
                    "required": ["name"],
                },
            }
        },
    }
