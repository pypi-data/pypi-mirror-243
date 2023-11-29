from __future__ import annotations

import strawberry

from ._openapi import Components, Info, OpenAPI, PathItem, Reference, Schema, Server
from ._operation_factory import OperationFactory

# TODO: shall we make this abstract?


class StrawberryOpenAPI:
    def __init__(
        self,
        schema: strawberry.Schema,
        documents: list[str],
        servers: list[dict[str, str]] | None = None,
    ) -> None:
        self.servers = servers or []
        self.schema = schema
        self.documents = documents

        self.operations = [
            OperationFactory(schema=schema).from_document(document)
            for document in documents
        ]

    def _collect_paths(self) -> dict[str, PathItem]:
        paths: dict[str, PathItem] = {}

        for operation in self.operations:
            assert operation.url
            assert operation.method
            assert operation.name

            url = operation.url.as_openapi()

            method = operation.method

            params = {
                method: operation.as_openapi(),
            }

            paths[url] = PathItem.model_validate(params)

        return paths

    def _get_components(self) -> Components | None:
        schemas: dict[str, Schema | Reference] = {}

        for operation in self.operations:
            schemas.update(operation.schemas)

        if schemas:
            return Components(schemas=schemas)

        return None

    @property
    def openapi_schema(self) -> OpenAPI:
        extra = {}

        components = self._get_components()

        if components:
            extra["components"] = components

        return OpenAPI(
            openapi="3.1.0",
            info=Info(title="Strawberry API", version="1.0.0"),
            servers=[
                Server(url=server["url"], description=server["description"])
                for server in self.servers
            ],
            paths=self._collect_paths(),
            **extra,  # type: ignore
        )
