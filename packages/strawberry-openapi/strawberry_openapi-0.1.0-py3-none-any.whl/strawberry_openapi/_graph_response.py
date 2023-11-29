from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ._openapi import MediaType, Response, Schema
from ._path import Path


@dataclass
class GraphSubResponse:
    schema: Schema
    status: int
    type_name: str
    path_to_root: Path | None = None
    description: str | None = None


@dataclass
class GraphResponse:
    schema: Schema | None = None
    path_to_root: Path | None = None
    path_to_typename: Path | None = None
    status: int = 200
    sub_responses: list[GraphSubResponse] = field(default_factory=list)
    description: str | None = None

    def from_data(self, data: dict[str, Any]) -> dict[str, Any]:
        status = self.status
        path_to_root = self.path_to_root

        # if we have a path to typename, we need to find the current type
        current_type = None
        if self.path_to_typename:
            current_type = data

            for key in self.path_to_typename.fields:
                if key == "__typename":
                    current_type = current_type.pop(key)
                else:
                    current_type = current_type[key]

        if current_type:
            sub_response = next(
                sub_response
                for sub_response in self.sub_responses
                if sub_response.type_name == current_type
            )

            status = sub_response.status
            path_to_root = sub_response.path_to_root

        # if we have a path to root, we need to find the current root
        if path_to_root:
            key = None

            for key in path_to_root.fields:
                data = data[key]

            assert key is not None

            data = {key: data}

        return {"status": status, "data": data}

    def as_openapi(self) -> dict[str, Response]:
        responses: dict[str, Response] = {}

        for sub_response in self.sub_responses:
            responses[str(sub_response.status)] = Response(
                description=sub_response.description or "",
                content={
                    "application/json": MediaType(schema=sub_response.schema),
                },
            )

        if not self.sub_responses:
            assert self.schema

            responses[str(self.status)] = Response(
                description=self.description or "",
                content={
                    "application/json": MediaType(schema=self.schema),
                },
            )

        return responses
