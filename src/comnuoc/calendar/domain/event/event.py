import datetime
from typing import Union
from typing_extensions import Self

from comnuoc.calendar.domain.util.datetime_range import DateTimeRange


class EventId(object):
    def __init__(self, id: object) -> None:
        self._id = id

    def __eq__(self, __value: Self) -> bool:
        return self._id == __value.getId()

    def __str__(self) -> str:
        return str(self._id)

    def getId(self) -> object:
        return self._id


class EventTitle(object):
    def __init__(self, title: str) -> None:
        title = title.strip()

        if 0 == len(title):
            raise ValueError("Title should not be blank")

        self._title = title

    def __str__(self) -> str:
        return self._title


class EventInterval(object):
    def __init__(self, interval: object) -> None:
        self._interval = interval

    def __str__(self) -> str:
        return str(self._interval)

    def getInterval(self) -> object:
        return self._interval


class EventDateTimeRange(DateTimeRange):
    def __init__(
        self, startDate: datetime.datetime, endDate: datetime.datetime
    ) -> None:
        super().__init__(startDate, endDate, True, True)

    def getStartDate(self) -> datetime.datetime:
        return super().getStartDate()

    def getEndDate(self) -> datetime.datetime:
        return super().getEndDate()

    def getRealStartDate(self) -> datetime.datetime:
        return self.getStartDate()

    def getRealEndDate(self) -> datetime.datetime:
        return self.getEndDate()


class Event(object):
    def __init__(
        self,
        id: EventId,
        title: EventTitle,
        dateTimeRange: EventDateTimeRange,
        isRecurrent: bool = False,
        recurrenceInterval: EventInterval = None,
    ) -> None:
        self._id = id
        self._title = title
        self._dateTimeRange = dateTimeRange
        self.setRecurrence(isRecurrent, recurrenceInterval)

    def __eq__(self, __value: Self) -> bool:
        return self._id == __value.getId()

    def getId(self) -> EventId:
        return self._id

    def getTitle(self) -> EventTitle:
        return self._title

    def setTitle(self, title: EventTitle) -> None:
        self._title = title

    def getDateTimeRange(self) -> EventDateTimeRange:
        return self._dateTimeRange

    def setDateTimeRange(self, dateTimeRange: EventDateTimeRange) -> None:
        self._dateTimeRange = dateTimeRange

    def isRecurrent(self) -> bool:
        return self._isRecurrent

    def setRecurrence(
        self, isRecurrent: bool, recurrenceInterval: Union[EventInterval, None]
    ) -> None:
        self._isRecurrent = isRecurrent

        if not isRecurrent:
            self._recurrenceInterval = None
        else:
            if recurrenceInterval is None:
                raise ValueError("Recurrent interval should be set.")

            self._recurrenceInterval = recurrenceInterval

    def getRecurrenceInterval(self) -> Union[EventInterval, None]:
        return self._recurrenceInterval
