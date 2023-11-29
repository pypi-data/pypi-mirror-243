from __future__ import annotations

import json
import logging
from typing import Any

from strawberry_openapi import StrawberryOpenAPI
from strawberry_openapi._operation_factory import Operation

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseServerError,
    JsonResponse,
)
from django.urls import URLPattern, path
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


class DjangoOpenAPI(StrawberryOpenAPI):
    def _get_url(self, operation: Operation) -> str:
        # TODO: make so we don't need to assert
        assert operation.url

        return operation.url.as_django_pattern()

    @property
    def paths(self) -> list[URLPattern]:
        return [
            path(
                route=self._get_url(operation),
                view=self._view,
                kwargs={"operation": operation},
            )
            for operation in self.operations
        ] + [
            path(
                route="openapi.json",
                view=self._openapi_view,
            )
        ]

    def get_context(self, request: HttpRequest, response: HttpResponse) -> Any:
        return {
            "request": request,
        }

    def _openapi_view(self, request: HttpRequest) -> HttpResponse:
        return JsonResponse(
            self.openapi_schema.model_dump(exclude_unset=True, by_alias=True),
            safe=False,
        )

    @csrf_exempt
    def _view(
        self, request: HttpRequest, operation: Operation | None, **kwargs: Any
    ) -> HttpResponse:
        # TODO: we can probably remove this
        if operation is None:
            return HttpResponseNotFound()

        document = operation.document

        variables = kwargs

        if request.method == "POST":
            body = request.body.decode("utf-8")
            body = json.loads(body)

            variables = {**variables, **body}

        response = HttpResponse()

        result = self.schema.execute_sync(
            document,
            root_value=None,
            variable_values=variables,
            context_value=self.get_context(request, response),
        )

        if result.errors:
            logger.error(result.errors)

            return HttpResponseServerError(
                json.dumps({"errors": [error.message for error in result.errors]})
            )

        assert result.data is not None

        response = operation.graph_response.from_data(result.data)

        return JsonResponse(response["data"], status=response["status"])
