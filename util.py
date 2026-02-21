from collections.abc import AsyncGenerator, Callable
from inspect import isasyncgen, iscoroutine
from types import CoroutineType
from typing import TYPE_CHECKING

from astrbot.api.event import AstrMessageEvent, MessageEventResult
from astrbot.core.star.star_tools import StarTools

from .structs import GroupState

if TYPE_CHECKING:
    from .main import KeywordMappingPlugin


def read_group_state(group: str):
    return GroupState.read(StarTools.get_data_dir() / f"{group}.json")


def save_group_state(group: str, data: GroupState):
    data.write(StarTools.get_data_dir() / f"{group}.json")


def use_group_state(save: bool, print_state: bool):
    def decorator(
        func: Callable[
            ["KeywordMappingPlugin", GroupState, AstrMessageEvent],
            AsyncGenerator[MessageEventResult] | CoroutineType,
        ],
    ):
        async def wrapper(
            self: "KeywordMappingPlugin",
            event: AstrMessageEvent,
        ) -> AsyncGenerator[MessageEventResult]:
            group = event.get_group_id()
            state = read_group_state(group)
            result = func(self, state, event)
            if isasyncgen(result):
                async for chunk in result:
                    yield chunk
            elif iscoroutine(result):
                await result
            if save:
                save_group_state(group, state)
            if print_state:
                yield event.plain_result(state.format())

        return wrapper

    return decorator
