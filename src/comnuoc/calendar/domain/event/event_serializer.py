import datetime
from abc import ABC, abstractmethod
from typing import Union

from comnuoc.calendar.domain.event.event import *


class EventIdNormalizer(ABC):
    @abstractmethod
    def normalize(self, id: EventId) -> str:
        raise NotImplementedError

    @abstractmethod
    def denormalize(self, id: str) -> EventId:
        raise NotImplementedError


class EventIntervalNormalizer(ABC):
    @abstractmethod
    def normalize(self, interval: Union[EventInterval, None]) -> str:
        raise NotImplementedError

    @abstractmethod
    def denormalize(self, interval: str) -> Union[EventInterval, None]:
        raise NotImplementedError


class EventNormalizer(object):
    def __init__(
        self,
        idNormalizer: EventIdNormalizer,
        intervalNormalizer: EventIntervalNormalizer,
        trueValue: str = "1",
        falseValue: str = "0",
    ) -> None:
        self._idNormalizer = idNormalizer
        self._intervalNormalizer = intervalNormalizer
        self._trueValue = trueValue
        self._falseValue = falseValue

    def normalize(self, event: Event) -> list[str]:
        return [
            self._idNormalizer.normalize(event.getId()),
            str(event.getTitle()),
            self.normalizeDateTime(event.getDateTimeRange().getRealStartDate()),
            self.normalizeDateTime(event.getDateTimeRange().getRealEndDate()),
            self.normalizeBoolean(event.isRecurrent()),
            self._intervalNormalizer.normalize(event.getRecurrenceInterval()),
        ]

    def denormalize(self, data: list[str]) -> Event:
        return Event(
            id=self._idNormalizer.denormalize(data[0]),
            title=EventTitle(data[1]),
            dateTimeRange=EventDateTimeRange(
                self.denormalizeDateTime(data[2]), self.denormalizeDateTime(data[3])
            ),
            isRecurrent=self.denormalizeBoolean(data[4]),
            recurrenceInterval=self._intervalNormalizer.denormalize(data[5]),
        )

    def normalizeDateTime(self, date: datetime.datetime) -> str:
        return date.astimezone(datetime.timezone.utc).isoformat()

    def denormalizeDateTime(self, date: str) -> datetime.datetime:
        return datetime.datetime.fromisoformat(date)

    def normalizeBoolean(self, isX: bool) -> str:
        if isX:
            return self._trueValue

        return self._falseValue

    def denormalizeBoolean(self, isX: str) -> bool:
        if self._trueValue == isX:
            return True

        return False
