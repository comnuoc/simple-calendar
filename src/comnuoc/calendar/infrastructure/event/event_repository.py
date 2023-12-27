import csv
import shutil
import uuid
from collections.abc import Generator, Iterable
from tempfile import NamedTemporaryFile
from typing import Union

from dateutil import rrule

from comnuoc.calendar.domain.event.event import Event, EventId
from comnuoc.calendar.domain.event.event_repository import (
    EventIdGenerator,
    EventRecurrenceChecker,
    EventRepository,
)
from comnuoc.calendar.domain.event.event_serializer import EventNormalizer
from comnuoc.calendar.domain.util.datetime_range import DateTimeRange


class CsvEventRepository(EventRepository):
    def __init__(
        self,
        idGenerator: EventIdGenerator,
        normalizer: EventNormalizer,
        recurrenceChecker: EventRecurrenceChecker,
        filePath: str,
        dialectName: str = "excel",
        encoding: str = "utf-8",
    ) -> None:
        self._idGenerator = idGenerator
        self._normalizer = normalizer
        self._recurrenceChecker = recurrenceChecker
        self._filePath = filePath
        self._dialectName = dialectName
        self._encoding = encoding

    def find(self, id: EventId) -> Union[Event, None]:
        events = self.__readEvents()

        try:
            for event in events:
                if event.getId() == id:
                    return event
        finally:
            events.close()  # as https://peps.python.org/pep-0533/

        return None

    def findByStartDate(self, startDateRange: DateTimeRange) -> Iterable[Event]:
        events = self.__readEvents()

        try:
            for event in events:
                if not event.isRecurrent():
                    if startDateRange.includes(event.getDateTimeRange().getStartDate()):
                        yield event
                else:
                    if self._recurrenceChecker.isStartDateInRange(
                        event, startDateRange
                    ):
                        yield event
        finally:
            events.close()  # as https://peps.python.org/pep-0533/

    def hasEventInRange(self, startDateRange: DateTimeRange) -> bool:
        events = self.__readEvents()

        try:
            for event in events:
                if not event.isRecurrent():
                    if startDateRange.includes(event.getDateTimeRange().getStartDate()):
                        return True
                else:
                    if self._recurrenceChecker.isStartDateInRange(
                        event, startDateRange
                    ):
                        return True
        finally:
            events.close()  # as https://peps.python.org/pep-0533/

        return False

    def insert(self, event: Event) -> None:
        with open(self._filePath, "a", newline="", encoding=self._encoding) as csvFile:
            writer = csv.writer(csvFile, dialect=self._dialectName)
            writer.writerow(self._normalizer.normalize(event))

    def update(self, newEvent: Event) -> None:
        self.__update(newEvent, False)

    def delete(self, deletedEvent: Event) -> None:
        self.__update(deletedEvent, True)

    def generateId(self) -> EventId:
        return self._idGenerator.generate()

    def __readEvents(self) -> Generator[Event, None, None]:
        with open(self._filePath, newline="", encoding=self._encoding) as csvFile:
            reader = csv.reader(csvFile, dialect=self._dialectName)

            for row in reader:
                event = self._normalizer.denormalize(row)

                yield event

    def __update(self, updatedEvent: Event, isDeleted: bool = False) -> None:
        tempFile = NamedTemporaryFile(
            mode="w", newline="", delete=False, encoding=self._encoding
        )

        with tempFile:
            writer = csv.writer(tempFile, dialect=self._dialectName)
            events = self.__readEvents()

            try:
                for event in events:
                    if event == updatedEvent:
                        if not isDeleted:
                            writer.writerow(self._normalizer.normalize(updatedEvent))
                    else:
                        writer.writerow(self._normalizer.normalize(event))
            finally:
                events.close()  # as https://peps.python.org/pep-0533/

        shutil.move(tempFile.name, self._filePath)


class EventIdUuidGenerator(EventIdGenerator):
    def generate(self) -> EventId:
        uuid4 = uuid.uuid4()

        return EventId(uuid4)


class EventRecurrenceRruleChecker(EventRecurrenceChecker):
    def __init__(self, firstWeekDay: int = 0) -> None:
        self._firstWeekDay = firstWeekDay

    def isStartDateInRange(self, event: Event, startDateRange: DateTimeRange) -> bool:
        interval = event.getRecurrenceInterval()

        if interval is None:
            raise ValueError("Event interval should not be none")

        interval = interval.getInterval()

        if not isinstance(interval, rrule.rrule):
            raise TypeError(
                "The value of event interval should be an instance of dateutil.rrule.rrule"
            )

        # Replace start date (with the timezone of the date range) and first week day in the rule
        # in order to ensure the integrity.
        interval = interval.replace(
            dtstart=event.getDateTimeRange()
            .getRealStartDate()
            .astimezone(startDateRange.getRealStartDate().tzinfo),
            wkst=self._firstWeekDay,
        )

        occurrences = interval.between(
            after=startDateRange.getRealStartDate(),
            before=startDateRange.getRealEndDate(),
            inc=True,
        )

        return len(occurrences) > 0
