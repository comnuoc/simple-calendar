from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Union

from comnuoc.calendar.domain.event.event import Event, EventId
from comnuoc.calendar.domain.event.event_serializer import EventIdNormalizer
from comnuoc.calendar.domain.util.datetime_range import DateTimeRange


class EventRepository(ABC):
    @abstractmethod
    def find(self, id: EventId) -> Union[Event, None]:
        raise NotImplementedError

    @abstractmethod
    def findByStartDate(self, startDateRange: DateTimeRange) -> Iterable[Event]:
        raise NotImplementedError

    @abstractmethod
    def hasEventInRange(self, startDateRange: DateTimeRange) -> bool:
        raise NotImplementedError

    @abstractmethod
    def insert(self, event: Event) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, event: Event) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, event: Event) -> None:
        raise NotImplementedError

    @abstractmethod
    def generateId(self) -> EventId:
        raise NotImplementedError


class EventIdGenerator(ABC):
    @abstractmethod
    def generate(self) -> EventId:
        raise NotImplementedError


class EventRecurrenceChecker(ABC):
    @abstractmethod
    def isStartDateInRange(self, event: Event, startDateRange: DateTimeRange) -> bool:
        raise NotImplementedError


class DictEventRepository(EventRepository):
    def __init__(
        self,
        idNormalizer: EventIdNormalizer,
        idGenerator: EventIdGenerator,
        recurrenceChecker: EventRecurrenceChecker,
    ) -> None:
        self._events: dict[str, Event] = {}
        self._idNormalizer = idNormalizer
        self._idGenerator = idGenerator
        self._recurrenceChecker = recurrenceChecker

    def find(self, id: EventId) -> Union[Event, None]:
        normalizedId = self.__normalizeId(id)

        if normalizedId in self._events:
            return self._events[normalizedId]

        return None

    def findByStartDate(self, startDateRange: DateTimeRange) -> Iterable[Event]:
        for id in self._events:
            event = self._events[id]

            if not event.isRecurrent():
                if startDateRange.includes(event.getDateTimeRange().getStartDate()):
                    yield event
            else:
                if self._recurrenceChecker.isStartDateInRange(event, startDateRange):
                    yield event

    def hasEventInRange(self, startDateRange: DateTimeRange) -> bool:
        for id in self._events:
            event = self._events[id]

            if not event.isRecurrent():
                if startDateRange.includes(event.getDateTimeRange().getStartDate()):
                    return True
            else:
                if self._recurrenceChecker.isStartDateInRange(event, startDateRange):
                    return True

        return False

    def insert(self, event: Event) -> None:
        normalizedId = self.__normalizeId(event.getId())

        self._events[normalizedId] = event

    def update(self, event: Event) -> None:
        self.insert(event)

    def delete(self, event: Event) -> None:
        normalizedId = self.__normalizeId(event.getId())

        if normalizedId in self._events:
            del self._events[normalizedId]

    def generateId(self) -> EventId:
        return self._idGenerator.generate()

    def __normalizeId(self, id: EventId) -> str:
        return self._idNormalizer.normalize(id)
