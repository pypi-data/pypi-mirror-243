# ruff: noqa: D100, D101, D102, D103, D104, D105, D107
from __future__ import annotations

from collections import defaultdict
from inspect import signature
from threading import Lock
from typing import (
    Callable,
    Generic,
    Protocol,
    cast,
)

from .basic_types import (
    Action,
    AutorunReturnType,
    BaseAction,
    ComparatorOutput,
    Event,
    Immutable,
    ReducerType,
    Selector,
    SelectorOutput,
    State,
    State_co,
    is_reducer_result,
    is_state,
)


class CreateStoreOptions(Immutable):
    initial_run: bool = True


class AutorunType(Protocol, Generic[State_co]):
    def __call__(
        self: AutorunType,
        selector: Callable[[State_co], SelectorOutput],
        comparator: Selector | None = None,
    ) -> Callable[
        [
            Callable[[SelectorOutput], AutorunReturnType]
            | Callable[[SelectorOutput, SelectorOutput], AutorunReturnType],
        ],
        Callable[[], AutorunReturnType],
    ]:
        ...


class EventSubscriber(Protocol):
    def __call__(
        self: EventSubscriber,
        event_type: type[Event],
        handler: Callable[[Event], None],
    ) -> Callable[[], None]:  # pyright: ignore[reportGeneralTypeIssues]
        pass


class InitializeStateReturnValue(Immutable, Generic[State, Action]):
    dispatch: Callable[[Action | list[Action]], None]
    subscribe: Callable[[Callable[[State], None]], Callable[[], None]]
    subscribe_event: EventSubscriber
    autorun: AutorunType[State]


def create_store(
    reducer: ReducerType[State, Action, Event],
    options: CreateStoreOptions | None = None,
) -> InitializeStateReturnValue[State, Action]:
    _options = CreateStoreOptions() if options is None else options

    state: State
    listeners: set[Callable[[State], None]] = set()
    event_handlers: defaultdict[
        type[Event],
        set[Callable[[Event], None]],
    ] = defaultdict(set)

    actions_queue: list[Action] = []
    events_queue: list[Event] = []
    is_running = Lock()

    def run() -> None:
        nonlocal state, is_running
        with is_running:
            while len(actions_queue) > 0 or len(events_queue) > 0:
                if len(actions_queue) > 0:
                    action = actions_queue.pop(0)
                    result = reducer(state if 'state' in locals() else None, action)
                    if is_reducer_result(result):
                        state = result.state
                        if result.actions:
                            actions_queue.extend(result.actions)
                        if result.events:
                            events_queue.extend(result.events)
                    elif is_state(result):
                        state = result

                    if len(actions_queue) == 0:
                        for listener in listeners.copy():
                            listener(state)

                if len(events_queue) > 0:
                    event = events_queue.pop(0)
                    for event_handler in event_handlers[type(event)].copy():
                        event_handler(event)
                    continue

    def dispatch(actions: Action | list[Action]) -> None:
        if isinstance(actions, BaseAction):
            actions = [actions]

        actions_queue.extend(actions)
        if not is_running.locked():
            run()

    def subscribe(listener: Callable[[State], None]) -> Callable[[], None]:
        listeners.add(listener)
        return lambda: listeners.remove(listener)

    def subscribe_event(
        event_type: type[Event],
        handler: Callable[[Event], None],
    ) -> Callable[[], None]:
        event_handlers[event_type].add(handler)
        return lambda: event_handlers[event_type].remove(handler)

    def autorun(
        selector: Callable[[State], SelectorOutput],
        comparator: Callable[[State], ComparatorOutput] | None = None,
    ) -> Callable[
        [
            Callable[[SelectorOutput], AutorunReturnType]
            | Callable[[SelectorOutput, SelectorOutput], AutorunReturnType],
        ],
        Callable[[], AutorunReturnType],
    ]:
        nonlocal state

        def decorator(
            fn: Callable[[SelectorOutput], AutorunReturnType]
            | Callable[[SelectorOutput, SelectorOutput], AutorunReturnType],
        ) -> Callable[[], AutorunReturnType]:
            last_selector_result: SelectorOutput | None = None
            last_comparator_result: ComparatorOutput | None = None
            last_value: AutorunReturnType | None = None

            def check_and_call(state: State) -> None:
                nonlocal last_selector_result, last_comparator_result, last_value
                selector_result = selector(state)
                if comparator is None:
                    comparator_result = cast(ComparatorOutput, selector_result)
                else:
                    comparator_result = comparator(state)
                if comparator_result != last_comparator_result:
                    previous_result = last_selector_result
                    last_selector_result = selector_result
                    last_comparator_result = comparator_result
                    if len(signature(fn).parameters) == 1:
                        last_value = cast(
                            Callable[[SelectorOutput], AutorunReturnType],
                            fn,
                        )(selector_result)
                    else:
                        last_value = cast(
                            Callable[
                                [SelectorOutput, SelectorOutput | None],
                                AutorunReturnType,
                            ],
                            fn,
                        )(
                            selector_result,
                            previous_result,
                        )

            if _options.initial_run and state is not None:
                check_and_call(state)

            subscribe(check_and_call)

            def call() -> AutorunReturnType:
                if state is not None:
                    check_and_call(state)
                return cast(AutorunReturnType, last_value)

            return call

        return decorator

    return InitializeStateReturnValue(
        dispatch=dispatch,
        subscribe=subscribe,
        subscribe_event=cast(Callable, subscribe_event),
        autorun=autorun,
    )
