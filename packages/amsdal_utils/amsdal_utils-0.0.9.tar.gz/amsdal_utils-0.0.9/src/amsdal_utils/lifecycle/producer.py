from collections import defaultdict
from typing import Any
from typing import ClassVar

from amsdal_utils.lifecycle.consumer import LifecycleConsumer
from amsdal_utils.lifecycle.enum import LifecycleEvent


class LifecycleProducer:
    __listeners: ClassVar[dict[LifecycleEvent, list[type[LifecycleConsumer]]]] = defaultdict(list)

    @classmethod
    def add_listener(
        cls,
        event: LifecycleEvent,
        listener: type[LifecycleConsumer],
        *,
        insert_first: bool = False,
    ) -> None:
        if listener in cls.__listeners[event]:
            return

        if insert_first:
            cls.__listeners[event].insert(0, listener)
        else:
            cls.__listeners[event].append(listener)

    @classmethod
    def publish(cls, event: LifecycleEvent, *args: Any, **kwargs: Any) -> None:
        for listener_class in cls.__listeners[event]:
            listener_class(event).on_event(*args, **kwargs)

    @classmethod
    def reset(cls) -> None:
        cls.__listeners.clear()
