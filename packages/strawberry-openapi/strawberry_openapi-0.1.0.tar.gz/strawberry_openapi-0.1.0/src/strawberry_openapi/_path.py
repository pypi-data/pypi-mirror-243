from __future__ import annotations

import dataclasses

from graphql import (
    FieldNode,
    InlineFragmentNode,
    Node,
)


@dataclasses.dataclass
class FieldSegment:
    name: str


@dataclasses.dataclass
class FragmentTypeSegment:
    type_name: str


@dataclasses.dataclass
class Path:
    segments: list[FieldSegment | FragmentTypeSegment]

    def __iter__(self):
        return iter(self.segments)

    def __len__(self):
        return len(self.segments)

    def __getitem__(self, index: int) -> FieldSegment | FragmentTypeSegment:
        return self.segments[index]

    def append(self, segment: FieldSegment | FragmentTypeSegment):
        self.segments.append(segment)

    @classmethod
    def from_nodes(cls, nodes: list[Node]) -> Path:
        path: Path = Path(segments=[])

        for node in nodes:
            if isinstance(node, FieldNode):
                path.append(FieldSegment(node.name.value))
            elif isinstance(node, InlineFragmentNode):
                path.append(FragmentTypeSegment(node.type_condition.name.value))

        return path

    @property
    def fields(self) -> list[str]:
        return [
            segment.name
            for segment in self.segments
            if isinstance(segment, FieldSegment)
        ]

    def with_field(self, field: str) -> Path:
        return Path(segments=self.segments + [FieldSegment(field)])
