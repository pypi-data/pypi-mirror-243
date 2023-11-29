from __future__ import annotations

from datetime import date, datetime, time
from typing import List, Union
from typing_extensions import Annotated

import strawberry

import pytest


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    age: int | None = None


@strawberry.type
class Article:
    id: strawberry.ID
    title: str
    content: str


@strawberry.type
class Photo:
    id: strawberry.ID
    url: str


FeedItem = Annotated[Union[Article, Photo], strawberry.union(name="FeedItem")]


@strawberry.type
class Query:
    hello: str = "world"
    float: float = 1.0
    int: int = 1
    bool: bool = True
    optional: str | None = None
    json: strawberry.scalars.JSON
    list_of_ints: List[int]
    list_of_lists_of_ints: List[List[int]]
    optional_list_of_ints: List[int] | None
    list_of_optional_ints: List[int | None]
    users: List[User | None] | None
    feed: List[FeedItem | None] | None
    date: date
    datetime: datetime
    time: time

    @strawberry.field
    def user(self, id: strawberry.ID) -> User | None:
        return User(id=id, name="Patrick")

    @strawberry.field
    def feed_item(self, id: str) -> FeedItem:
        return Article(id=strawberry.ID(id), title="Test", content="Test")

    @strawberry.field
    def hello_world(self) -> str:
        return "Hello, world!"

    @strawberry.field
    def this_raises_an_error(self) -> str:
        raise ValueError("This is an error")


@strawberry.input
class UserInput:
    name: str
    age: int | None = None


@strawberry.type
class CreateUserSuccess:
    user: User


@strawberry.type
class CreateUserError:
    message: str


CreateUserResponse = Annotated[
    Union[CreateUserSuccess, CreateUserError],
    strawberry.union(name="CreateUserResponse"),
]


@strawberry.input
class SayHelloInput:
    name: str


@strawberry.input
class EchoInput:
    text: str


@strawberry.type
class Mutation:
    @strawberry.mutation
    def say_hello(self, name: str) -> str:
        return f"Hello, {input}!"

    @strawberry.mutation
    def basic_create_user(self, input: UserInput) -> User:
        return User(id=strawberry.ID("1"), name=input.name, age=input.age)

    @strawberry.mutation
    def create_user(self, input: UserInput) -> CreateUserResponse:
        # TODO: have a way to trigger an error
        return CreateUserSuccess(user=User(id=strawberry.ID("1"), name=input.name))

    @strawberry.mutation
    def say_hello_to_user(self, id: strawberry.ID, input: SayHelloInput) -> str:
        return f"Hello, {input.name}!"

    @strawberry.mutation
    def echo(self, input: List[EchoInput]) -> str:
        return input[0].text


@pytest.fixture
def schema():
    return strawberry.Schema(query=Query, mutation=Mutation)
