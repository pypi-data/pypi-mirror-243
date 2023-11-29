from __future__ import annotations

from typing import Any, cast
from typing_extensions import NotRequired, TypedDict, TypeGuard

from strawberry.custom_scalar import ScalarDefinition, ScalarWrapper
from strawberry.field import StrawberryField
from strawberry.scalars import is_scalar
from strawberry.schema import Schema as StrawberrySchema
from strawberry.type import (
    StrawberryContainer,
    StrawberryList,
    StrawberryOptional,
    get_object_definition,
    has_object_definition,
)
from strawberry.types.types import StrawberryObjectDefinition
from strawberry.union import StrawberryUnion

from graphql import (
    DirectiveNode,
    DocumentNode,
    FieldNode,
    FragmentDefinitionNode,
    FragmentSpreadNode,
    InlineFragmentNode,
    IntValueNode,
    ListTypeNode,
    NamedTypeNode,
    NameNode,
    Node,
    NonNullTypeNode,
    OperationDefinitionNode,
    SelectionSetNode,
    StringValueNode,
    VariableDefinitionNode,
    parse,
    print_ast,
)

from ._graph_response import GraphResponse, GraphSubResponse
from ._openapi import (
    Schema,
    SchemaOrBool,
)
from ._operation import URL, Operation, Placeholder
from ._path import FragmentTypeSegment, Path


class PropertyType(TypedDict):
    type: str | PropertyType
    required: bool
    ofType: NotRequired[PropertyType]  # TODO: union


class OperationFactory:
    def __init__(self, schema: StrawberrySchema):
        self.schema = schema
        self.operation: Operation | None = None
        self.operation_type: str | None = None

    def from_document(self, document_text: str) -> Operation:
        self.operation = Operation()

        document: DocumentNode = parse(document_text)

        assert len(document.definitions) == 1

        definition = document.definitions[0]

        assert isinstance(definition, OperationDefinitionNode)
        assert definition.name

        self.operation_definition = definition
        self.operation_type = definition.operation.name
        self.operation.name = definition.name.value

        self._graph_response = GraphResponse()
        self._current_sub_response: GraphSubResponse | None = None

        self._visit(definition)
        self._visit_input_variables(definition)
        self._collect_schemas()

        stripped_document = print_ast(document)

        self.operation.document = stripped_document

        self.operation.graph_response = self._graph_response

        return self.operation

    def _get_type_from_schema(self, type_name: str) -> Any:
        return self.schema.get_type_by_name(type_name)

    def _get_properties_from_variables(
        self, variable_definitions: tuple[VariableDefinitionNode, ...]
    ) -> tuple[dict[str, SchemaOrBool], list[str]]:
        assert self.operation
        assert self.operation.url

        variables_used_in_url = {
            parameter.name
            for parameter in self.operation.url.parts
            if isinstance(parameter, Placeholder)
        }

        properties: dict[str, SchemaOrBool] = {}
        required_fields: list[str] = []

        for variable_definition in variable_definitions:
            required = False

            name = variable_definition.variable.name.value

            if name in variables_used_in_url:
                continue

            type_ = variable_definition.type

            if isinstance(type_, NonNullTypeNode):
                required = True
                type_ = type_.type

            # TODO: list of lists and lists of optionals :')
            if isinstance(type_, ListTypeNode):
                # TODO: we are assuming a lot of things here :)
                # let's be naive for now
                type_ = type_.type.type  #  type: ignore
                type_name = type_.name.value  # type: ignore
                strawberry_type = self._get_type_from_schema(type_name)  # type: ignore

                assert isinstance(strawberry_type, StrawberryObjectDefinition)
                self._collect_schema_for_input(strawberry_type)

                properties[name] = Schema(
                    type="array",
                    items=Schema.model_validate(
                        {"$ref": f"#/components/schemas/{type_name}"}
                    ),
                )

            elif isinstance(type_, NamedTypeNode):
                type_name = type_.name.value
                strawberry_type = self._get_type_from_schema(type_name)

                if self._is_scalar(strawberry_type):
                    properties[name] = self._get_scalar_schema(strawberry_type)

                elif self._is_list(strawberry_type):
                    items = self._collect_schema_for_input(strawberry_type.of_type)  # type: ignore

                    properties[name] = Schema(type="array", items=items)

                elif isinstance(strawberry_type, StrawberryObjectDefinition):
                    self._collect_schema_for_input(strawberry_type)

                    properties[name] = Schema.model_validate(
                        {"$ref": f"#/components/schemas/{type_name}"}
                    )

            if required:
                required_fields.append(name)

        return properties, required_fields

    def _collect_schema_for_input(self, type_: StrawberryObjectDefinition):
        assert type_.is_input

        properties: dict[str, SchemaOrBool] = {}
        required_fields: list[str] = []

        for field in type_.fields:
            required = True

            inner_type = field.type  # type: ignore

            if self._is_optional(inner_type):  # type: ignore
                required = False

                inner_type = inner_type.of_type  # type: ignore

            if self._is_list(inner_type):
                items = self._collect_schema_for_input(inner_type.of_type)  # type: ignore

                properties[field.name] = Schema(type="array", items=items)

            elif self._is_scalar(inner_type):
                properties[field.name] = self._get_scalar_schema(inner_type)

            elif self._is_object_type(inner_type):  # type: ignore
                strawberry_type = get_object_definition(inner_type, strict=True)

                self._collect_schema_for_input(strawberry_type)

                properties[field.name] = Schema.model_validate(
                    {"$ref": f"#/components/schemas/{strawberry_type.name}"}
                )
            else:
                raise NotImplementedError(f"Type type {type(inner_type)}")  # type: ignore

            if required:
                required_fields.append(field.name)

        assert self.operation

        if not self.operation.schemas:
            self.operation.schemas = {}

        if not self.operation.schemas.get(type_.name):
            self.operation.schemas[type_.name] = Schema(
                type="object",
                required=required_fields,
                properties=properties,
            )

    def _visit_input_variables(self, definition: OperationDefinitionNode):
        assert self.operation

        properties, required_fields = self._get_properties_from_variables(
            definition.variable_definitions
        )

        if not properties:
            return

        self.operation.request_body_schema = Schema(
            type="object",
            required=required_fields,
            properties=properties,
        )

    def _is_object_type(self, type_: Any) -> bool:
        return has_object_definition(type_)

    def _is_scalar(self, type_: Any) -> bool:
        return isinstance(type_, ScalarDefinition) or is_scalar(
            type_, self.schema.schema_converter.scalar_registry
        )

    def _get_scalar_schema(self, type_: Any) -> Schema:
        if not isinstance(type_, ScalarDefinition):
            if type_ in self.schema.schema_converter.scalar_registry:
                type_ = self.schema.schema_converter.scalar_registry[type_]

        graphql_to_openapi_type: dict[str, tuple[str, dict[str, Any]]] = {
            "ID": ("string", {}),
            "Int": ("integer", {}),
            "String": ("string", {}),
            "Boolean": ("boolean", {}),
            "Float": ("number", {}),
            "DateTime": ("string", {"format": "date-time"}),
            "Date": ("string", {"format": "date"}),
            "Time": ("string", {"format": "time"}),
            "JSON": ("object", {"additionalProperties": True}),
        }

        if isinstance(type_, ScalarWrapper):
            name = type_._scalar_definition.name  # type: ignore
        else:
            name = type_.name

        if name in graphql_to_openapi_type:
            type_, kwargs = graphql_to_openapi_type[name]

            return Schema(type=type_, **kwargs)

        raise NotImplementedError(f"Unknown scalar type {type_}")

    def _is_optional(self, type_: Any) -> TypeGuard[StrawberryOptional]:
        return isinstance(type_, StrawberryOptional)

    def _is_list(self, type_: Any) -> TypeGuard[StrawberryList]:
        return isinstance(type_, StrawberryList)

    def _is_union(self, type_: Any) -> TypeGuard[StrawberryUnion]:
        return isinstance(type_, StrawberryUnion)

    def _find_field(
        self, type_definition: StrawberryObjectDefinition, graphql_name: str
    ) -> StrawberryField:
        # TODO: ugly
        return next(
            field
            for field in type_definition.fields
            if self.schema.config.name_converter.get_graphql_name(field) == graphql_name
        )

    def _get_schema_for_union(
        self, union_type: StrawberryUnion, selection: FieldNode, optional: bool = False
    ) -> Schema:
        types = union_type.types

        assert selection.selection_set

        assert all(
            isinstance(selection, InlineFragmentNode)
            for selection in selection.selection_set.selections
        ), "Only inline fragments are supported for unions for now"

        schemas: list[SchemaOrBool] = []
        types_by_name: dict[str, StrawberryObjectDefinition] = {}

        for type_ in types:
            definition = get_object_definition(type_, strict=True)
            types_by_name[definition.name] = definition

        for selection in selection.selection_set.selections:  # type: ignore
            assert isinstance(selection, InlineFragmentNode)

            definition = types_by_name[selection.type_condition.name.value]

            assert selection.selection_set

            schemas.append(
                self._get_schema_for_object(
                    definition,
                    selection.selection_set,
                )
            )

        if optional:
            schemas.append(Schema(type="null"))

        return Schema(oneOf=schemas)

    def _get_schema_for_list(
        self, type_: StrawberryList, selection: FieldNode
    ) -> Schema:
        is_optional = False

        inner_type = type_.of_type

        if self._is_optional(inner_type):
            is_optional = True
            inner_type = inner_type.of_type  # type: ignore

        if self._is_list(inner_type):
            items = self._get_schema_for_list(
                inner_type,  # type: ignore
                selection,
            )

        elif self._is_scalar(inner_type):
            items = self._get_scalar_schema(inner_type)
        elif self._is_object_type(inner_type):  # type: ignore
            assert isinstance(selection.selection_set, SelectionSetNode)

            items = self._get_schema_for_object(
                get_object_definition(inner_type, strict=True), selection.selection_set
            )
        elif self._is_union(inner_type):
            items = self._get_schema_for_union(inner_type, selection, optional=True)
        else:
            raise NotImplementedError(f"Type type {type(inner_type)}")  # type: ignore

        # we handle optional unions as a special case
        if is_optional and not self._is_union(inner_type):
            items = Schema(oneOf=[items, Schema(type="null")])

        return Schema(type="array", items=items)

    def _get_schema_for_object(
        self, type_: StrawberryObjectDefinition, selection_set: SelectionSetNode
    ) -> Schema:
        properties, required_fields = self._get_properties_from_selection_set(
            type_, selection_set
        )

        return Schema(
            type="object",
            required=required_fields,
            properties=properties,
        )

    def _get_properties_from_selection_set(
        self,
        parent_type: StrawberryObjectDefinition,
        selection_set: SelectionSetNode,
        type_name: str | None = None,
    ) -> tuple[dict[str, SchemaOrBool], list[str]]:
        properties: dict[str, SchemaOrBool] = {}
        required_fields: list[str] = []

        for selection in selection_set.selections:
            required = True

            if not isinstance(selection, FieldNode):
                raise NotImplementedError(
                    f"Selection type {type(selection)} not implemented"
                )

            field_name = selection.name.value

            strawberry_field = self._find_field(parent_type, field_name)

            field_type = strawberry_field.type  # type: ignore

            if self._is_optional(field_type):
                required = False
                field_type = field_type.of_type  # type: ignore

            if self._is_list(field_type):
                properties[field_name] = self._get_schema_for_list(
                    field_type,  # type: ignore
                    selection=selection,
                    # TODO: ...
                    # type_name=type_name,
                )

            elif self._is_scalar(field_type):
                properties[field_name] = self._get_scalar_schema(field_type)
            elif self._is_object_type(field_type):  # type: ignore
                assert isinstance(selection.selection_set, SelectionSetNode)

                selection_set = selection.selection_set

                properties[field_name] = self._get_schema_for_object(
                    get_object_definition(field_type, strict=True), selection_set
                )
            elif self._is_union(field_type):
                if type_name:
                    field_type = next(
                        type_
                        for type_ in field_type.types
                        if get_object_definition(type_, strict=True).name == type_name
                    )

                    assert isinstance(selection.selection_set, SelectionSetNode)
                    selection_set = selection.selection_set

                    selection_set = next(
                        selection
                        for selection in selection_set.selections
                        if isinstance(selection, InlineFragmentNode)
                        and selection.type_condition.name.value == type_name
                    ).selection_set

                    properties[field_name] = self._get_schema_for_object(
                        get_object_definition(field_type, strict=True), selection_set
                    )
                else:
                    properties[field_name] = self._get_schema_for_union(
                        field_type, selection
                    )

            else:
                raise NotImplementedError(f"Type type {type(field_type)}")  # type: ignore

            if required:
                required_fields.append(field_name)

        return properties, required_fields

    def _get_root_type(self) -> StrawberryObjectDefinition:
        assert self.operation_type

        root_type = {  # type: ignore
            "QUERY": self.schema.query,  # type: ignore
            "MUTATION": self.schema.mutation,  # type: ignore
        }[self.operation_type]

        assert root_type

        return get_object_definition(root_type, strict=True)

    def _find_start(
        self, path_to_root: Path | None = None
    ) -> tuple[StrawberryObjectDefinition, SelectionSetNode]:
        assert self.operation_type

        root_type_definition = self._get_root_type()

        start = root_type_definition
        selection_set = self.operation_definition.selection_set

        if not path_to_root:
            return start, selection_set

        for index, segment in enumerate(path_to_root):
            # we don't support nested fragments for now, so we can safely assume
            # that this is the last segment
            if isinstance(segment, FragmentTypeSegment):
                break

            # skip the last one too because we need to find the field
            if index == len(path_to_root) - 1:
                break

            field = self._find_field(start, segment.name)
            field_type = field.type  # type: ignore

            assert selection_set
            selection_set = next(
                selection
                for selection in selection_set.selections
                if isinstance(selection, FieldNode)
                and selection.name.value == segment.name
            ).selection_set

            while isinstance(field_type, StrawberryContainer):
                field_type = field_type.of_type

            if isinstance(field_type, StrawberryUnion):
                next_segment = path_to_root[index + 1]
                assert isinstance(next_segment, FragmentTypeSegment)

                for type_ in field_type.types:
                    type_definition = get_object_definition(type_, strict=True)

                    if type_definition.name == next_segment.type_name:
                        start = type_definition

                        # finding the right selection set based on the type name

                        selection_set = next(
                            selection
                            for selection in selection_set.selections  # type: ignore
                            if isinstance(selection, InlineFragmentNode)
                            and selection.type_condition.name.value
                            == next_segment.type_name
                        ).selection_set

                        break
            else:
                start = get_object_definition(field_type, strict=True)

        assert start
        assert selection_set

        return start, selection_set

    def _collect_schema(
        self,
        path_to_root: Path | None = None,
        type_name: str | None = None,
    ):
        start, selection_set = self._find_start(path_to_root)

        properties, required_fields = self._get_properties_from_selection_set(
            start, selection_set, type_name
        )

        return Schema(
            type="object",
            required=required_fields,
            properties=properties,
        )

    def _collect_schemas(self):
        # this is the only place where we can collect schemas, because we need to
        # know the path to root and the path to typename

        # if we don't have any sub responses, we can just collect the schema
        # for the main response

        if not self._graph_response.sub_responses:
            self._graph_response.schema = self._collect_schema(
                self._graph_response.path_to_root
            )
            return

        # if we have sub responses, we need to collect schemas for each of them

        for sub_response in self._graph_response.sub_responses:
            sub_response.schema = self._collect_schema(
                sub_response.path_to_root, sub_response.type_name
            )

    def _handle_status_directive(
        self, arguments: dict[str, str], parent: Node, parents: list[Node]
    ):
        path_to_root = Path.from_nodes(parents)

        self._graph_response.path_to_typename = path_to_root.with_field("__typename")

        sub_response = GraphSubResponse(
            status=int(arguments["code"]),
            type_name=cast(str, parent.type_condition.name.value),  # type: ignore
            schema=None,  # type: ignore
        )

        self._current_sub_response = sub_response
        self._graph_response.sub_responses.append(sub_response)

        selection_parent = parents[-2]  # this is an assumption, fine for now
        assert isinstance(selection_parent, FieldNode)
        assert selection_parent.selection_set

        # add __typename, so we can use it in the view
        if not any(
            isinstance(selection, FieldNode) and selection.name.value == "__typename"
            for selection in selection_parent.selection_set.selections
        ):
            selection_parent.selection_set.selections = (
                FieldNode(name=NameNode(value="__typename")),
            ) + selection_parent.selection_set.selections

    def _handle_endpoint_directive(
        self, arguments: dict[str, str], parent: Node, parents: list[Node]
    ):
        assert self.operation

        self.operation.url = URL.from_string(arguments["url"], self.operation.variables)

        method = arguments["method"].lower()

        assert method in ("get", "post", "delete", "patch")

        self.operation.method = method

    def _handle_root_directive(
        self, arguments: dict[str, str], parent: Node, parents: list[Node]
    ):
        path_to_root = Path.from_nodes(parents)

        if self._current_sub_response:
            self._current_sub_response.path_to_root = path_to_root
        else:
            self._graph_response.path_to_root = path_to_root

    def _handle_directive(
        self, directive: DirectiveNode, parent: Node, parents: list[Node]
    ):
        arguments = get_directives_arguments(directive)
        assert self.operation

        if directive.name.value == "status":
            self._handle_status_directive(arguments, parent, parents)

        if directive.name.value == "endpoint":
            self._handle_endpoint_directive(arguments, parent, parents)

        if directive.name.value == "root":
            self._handle_root_directive(arguments, parent, parents)

    def _visit(self, node: Node, parents: list[Node] | None = None):
        # so, we want to visit all the notes, in order to collect responses and
        # use directives like @root and @status to change the shape of the response
        # and potentially create multiple responses when there's a status directive
        # status directives can only be used on inline fragments, we need to use
        # @status on all the inline fragments, just to make it more explicit what's
        # going on

        if parents is None:
            parents = []

        parents.append(node)

        can_have_directives = isinstance(
            node,
            (
                FieldNode,
                FragmentDefinitionNode,
                FragmentSpreadNode,
                InlineFragmentNode,
                OperationDefinitionNode,
            ),
        )

        if can_have_directives and node.directives:
            for directive in node.directives:
                self._handle_directive(directive, node, parents)

            node.directives = ()

        if isinstance(node, FieldNode) and node.selection_set:
            for selection in node.selection_set.selections:
                self._visit(selection, parents)
        elif isinstance(
            node, (FragmentDefinitionNode, OperationDefinitionNode, InlineFragmentNode)
        ):
            if node.selection_set:
                for selection in node.selection_set.selections:
                    self._visit(selection, parents)

        parents.pop()


def get_directives_arguments(directive: DirectiveNode) -> dict[str, str]:
    arguments: dict[str, str] = {}

    for argument in directive.arguments:
        name = argument.name.value

        if isinstance(argument.value, StringValueNode):
            value = argument.value.value
        elif isinstance(argument.value, IntValueNode):
            value = argument.value.value
        else:
            raise NotImplementedError(f"Argument value type {type(argument.value)}")

        arguments[name] = value

    return arguments
