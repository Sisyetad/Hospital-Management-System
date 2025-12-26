# shared/domain_event.py
from typing import Callable, Dict, List, Type

class DomainEvent:
    pass

class EventDispatcher:
    _handlers: Dict[Type[DomainEvent], List[Callable]] = {}

    @classmethod
    def register(cls, event_type: Type[DomainEvent], handler: Callable):
        cls._handlers.setdefault(event_type, []).append(handler)

    @classmethod
    def dispatch(cls, event: DomainEvent):
        for handler in cls._handlers.get(type(event), []):
            handler(event)
