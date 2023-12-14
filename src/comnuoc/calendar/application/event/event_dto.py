import datetime
from typing import Union

from dateutil import rrule

from comnuoc.calendar.domain.event.event import *
from comnuoc.calendar.domain.event.event_serializer import (
    EventIdNormalizer,
    EventIntervalNormalizer,
)

from comnuoc.calendar.infrastructure.util.setting_repository import (
    FileSettingRepository,
)


class EventDto(object):
    def __init__(self) -> None:
        self.id: Union[str, None] = None
        self.title: Union[str, None] = None

        self.dateYear: Union[int, None] = None
        self.dateMonth: Union[int, None] = None
        self.dateDay: Union[int, None] = None

        self.startDateHour: Union[int, None] = None
        self.startDateMinute: Union[int, None] = None

        self.endDateHour: Union[int, None] = None
        self.endDateMinute: Union[int, None] = None

        self.isRecurrent: Union[bool, None] = None

        # @see https://datatracker.ietf.org/doc/html/rfc5545#section-3.3.10
        # @see https://dateutil.readthedocs.io/en/stable/rrule.html#rrulestr-examples
        # @todo: should split the interval into multiple parts,
        # create an assembler in order do assemble parts and disassemble into multiple parts
        self.recurrenceInterval: Union[str, None] = None


class EventDtoTransformer(object):
    def __init__(
        self,
        settings: FileSettingRepository,
        idNormalizer: EventIdNormalizer,
        intervalNormalizer: EventIntervalNormalizer,
    ) -> None:
        self._settings = settings
        self._idNormalizer = idNormalizer
        self._intervalNormalizer = intervalNormalizer

    def createDtoFromEvent(self, event: Event) -> EventDto:
        dto = EventDto()

        dto.id = self._idNormalizer.normalize(event.getId())
        dto.title = str(event.getTitle())

        tzInfo = self._settings.getTzInfo()
        startDate = event.getDateTimeRange().getRealStartDate().astimezone(tzInfo)
        endDate = event.getDateTimeRange().getRealEndDate().astimezone(tzInfo)
        dto.dateYear = startDate.year
        dto.dateMonth = startDate.month
        dto.dateDay = startDate.day

        dto.startDateHour = startDate.hour
        dto.startDateMinute = startDate.minute

        dto.endDateHour = endDate.hour
        dto.endDateMinute = endDate.minute

        dto.isRecurrent = event.isRecurrent()

        if dto.isRecurrent:
            dto.recurrenceInterval = self._intervalNormalizer.normalize(
                event.getRecurrenceInterval()
            )

        return dto

    def createEventFromDto(self, dto: EventDto, eventId: EventId) -> Event:
        title = EventTitle(dto.title)

        tzInfo = self._settings.getTzInfo()
        startDate = datetime.datetime(
            year=dto.dateYear,
            month=dto.dateMonth,
            day=dto.dateDay,
            hour=dto.startDateHour,
            minute=dto.startDateMinute,
            tzinfo=tzInfo,
        )
        endDate = datetime.datetime(
            year=dto.dateYear,
            month=dto.dateMonth,
            day=dto.dateDay,
            hour=dto.endDateHour,
            minute=dto.endDateMinute,
            tzinfo=tzInfo,
        )
        dateTimeRange = EventDateTimeRange(startDate, endDate)

        isRecurrent = dto.isRecurrent

        if isRecurrent and dto.recurrenceInterval is not None:
            recurrenceInterval = self._intervalNormalizer.denormalize(
                dto.recurrenceInterval
            )
            rule = recurrenceInterval.getInterval()

            # should replace start date and first week day in the rule
            # in order to ensure the integrity.
            if isinstance(rule, rrule.rrule):
                weekStart = self._settings.getFirstWeekDay()
                rule = rule.replace(dtstart=startDate, wkst=weekStart)
                recurrenceInterval = EventInterval(rule)
        else:
            recurrenceInterval = None

        return Event(
            id=eventId,
            title=title,
            dateTimeRange=dateTimeRange,
            isRecurrent=isRecurrent,
            recurrenceInterval=recurrenceInterval,
        )
