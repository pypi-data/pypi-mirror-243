from __future__ import annotations

import dataclasses
from typing import Any
from typing_extensions import Literal, NotRequired, TypedDict

from ._graph_response import GraphResponse
from ._openapi import (
    MediaType,
    Parameter,
    ParameterInType,
    Reference,
    RequestBody,
    Schema,
)
from ._openapi import Operation as OpenAPIOperation

StatusCode = str


@dataclasses.dataclass
class Placeholder:
    name: str
    type: str


@dataclasses.dataclass
class Path:
    value: str


@dataclasses.dataclass
class URL:
    parts: list[Path | Placeholder]

    def __str__(self):
        return "/" + "/".join(
            part.value if isinstance(part, Path) else f"${part.name}"
            for part in self.parts
        )

    def as_django_pattern(self) -> str:
        return "/".join(
            part.value if isinstance(part, Path) else f"<str:{part.name}>"
            for part in self.parts
        )

    def as_openapi(self) -> str:
        return "/" + "/".join(
            part.value if isinstance(part, Path) else f"{{{part.name}}}"
            for part in self.parts
        )

    @classmethod
    def from_string(cls, url: str, input_types: dict[str, Any]) -> URL:
        parts: list[Path | Placeholder] = []

        for part in url.split("/"):
            if not part:
                continue

            if part.startswith("$"):
                name = part[1:]
                # TODO: do we need the actual type here?
                type_ = "string"
                parts.append(Placeholder(name=name, type=type_))
            else:
                parts.append(Path(value=part))

        return cls(parts=parts)


@dataclasses.dataclass
class Variable:
    schema: Schema
    required: bool


@dataclasses.dataclass
class Operation:
    # TODO: remove these nones
    name: str | None = None
    url: URL | None = None
    method: Literal["get", "post", "delete", "patch"] | None = None
    document: str | None = None
    request_body_schema: Schema | None = None
    variables: dict[str, Variable] = dataclasses.field(default_factory=dict)
    schemas: dict[str, Schema] = dataclasses.field(default_factory=dict)
    graph_response: GraphResponse = dataclasses.field(default_factory=GraphResponse)

    @property
    def url_parameters(self) -> list[Parameter | Reference] | None:
        assert self.url

        parameters: list[Parameter | Reference] = []
        placeholders = (
            part for part in self.url.parts if isinstance(part, Placeholder)
        )

        for placeholder in placeholders:
            data = {
                "name": placeholder.name,
                "schema": {"type": "string"},
                "required": True,
                "in": ParameterInType.path,
            }

            parameters.append(Parameter.model_validate(data, strict=True))

        if not parameters:
            return None

        return parameters

    def as_openapi(self) -> OpenAPIOperation:
        class OpenAPIOperationExtra(TypedDict):
            parameters: NotRequired[list[Parameter | Reference]]
            requestBody: NotRequired[RequestBody]

        assert self.url

        extra: OpenAPIOperationExtra = {}

        if self.url_parameters:
            extra["parameters"] = self.url_parameters

        if self.request_body_schema:
            extra["requestBody"] = RequestBody(
                content={"application/json": MediaType(schema=self.request_body_schema)}
            )

        return OpenAPIOperation(
            operationId=self.name,
            responses=self.graph_response.as_openapi(),
            **extra,
        )
