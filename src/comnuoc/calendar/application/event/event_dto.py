import datetime
from typing import Union

from dateutil import rrule
from recurrent.event_parser import RecurringEvent

from comnuoc.calendar.domain.event.event import *
from comnuoc.calendar.domain.event.event_serializer import (
    EventIdNormalizer,
    EventIntervalNormalizer,
)

from comnuoc.calendar.infrastructure.util.setting_repository import (
    FileSettingRepository,
)


class EventDto(object):
    RECURRENCE_FREQS = ["YEARLY", "MONTHLY", "WEEKLY", "DAILY"]
    RECURRENCE_WEEKDAYS = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]

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
        # The frequency. Values are 'YEARLY', 'MONTHLY', 'WEEKLY', 'DAILY'
        self.recurrenceIntervalFreq: Union[str, None] = None

        # The interval between each freq iteration. For example, when using
        # YEARLY, an interval of 2 means once every two years, but with DAILY,
        # it means once every two days. The default interval is 1.
        self.recurrenceIntervalInterval: int = 1

        # The weekdays where the recurrence will be applied.
        # Values in list are 'MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'
        # or '+1MO', 'MO(+1)': first Monday
        # or '-1MO', 'MO(-1)': last Monday
        self.recurrenceIntervalByWeekDay: Union[list[str], None] = None

        # The month days to apply the recurrence to.
        # Values in list are '1', '2', '3', ..., '31'
        self.recurrenceIntervalByMonthDay: Union[list[int], None] = None

        # The months to apply the recurrence to.
        # Values in list are '1', '2', '3', ..., '12'
        self.recurrenceIntervalByMonth: Union[list[int], None] = None

        self.recurrenceIntervalHumanText: Union[str, None] = None


class EventRecurrenceAssembler(object):
    FREQ = "FREQ"
    INTERVAL = "INTERVAL"
    BYWEEKDAY = "BYWEEKDAY"
    BYMONTHDAY = "BYMONTHDAY"
    BYMONTH = "BYMONTH"
    BYDAY = "BYDAY"
    MULTIPLE_PROPERTIES = [BYWEEKDAY, BYMONTHDAY, BYMONTH]
    INT_PROPERTIES = [INTERVAL, BYMONTHDAY, BYMONTH]

    def assemble(
        self, parts: dict[str, Union[str, int, list[str], list[int], None]]
    ) -> str:
        ruleParts = {}

        for key, val in parts.items():
            if self._isEmpty(val):
                continue

            upperCaseKey = key.upper()

            if self.BYDAY == upperCaseKey:
                upperCaseKey = self.BYWEEKDAY

            if upperCaseKey in self.MULTIPLE_PROPERTIES:
                if upperCaseKey in self.INT_PROPERTIES:
                    val = [str(item) for item in val]

                val = ",".join(val)
            elif upperCaseKey in self.INT_PROPERTIES:
                val = str(val)

            ruleParts[upperCaseKey] = val

        ruleParts = [f"{key}={val}" for key, val in ruleParts.items()]

        return ";".join(ruleParts)

    def disassemble(
        self, rule: str
    ) -> dict[str, Union[str, int, list[str], list[int]]]:
        ruleParts = {}
        parts = rule.split(";")

        for part in parts:
            splitParts = part.split("=")

            if (2 == len(splitParts)) and (not self._isEmpty(splitParts[1])):
                upperCaseKey = splitParts[0].upper()

                if self.BYDAY == upperCaseKey:
                    upperCaseKey = self.BYWEEKDAY

                val = splitParts[1]

                if upperCaseKey in self.MULTIPLE_PROPERTIES:
                    val = val.split(",")

                    if upperCaseKey in self.INT_PROPERTIES:
                        val = [int(item) for item in val]
                elif upperCaseKey in self.INT_PROPERTIES:
                    val = int(val)

                ruleParts[upperCaseKey] = val

        return ruleParts

    def _isEmpty(self, val: Union[str, int, list, None]) -> bool:
        if val is None:
            return True

        if isinstance(val, list) and 0 == len(val):
            return True

        if isinstance(val, int) and 0 == val:
            return True

        if isinstance(val, str) and "" == val:
            return True

        return False


class EventDtoTransformer(object):
    def __init__(
        self,
        settings: FileSettingRepository,
        idNormalizer: EventIdNormalizer,
        intervalNormalizer: EventIntervalNormalizer,
        intervalAssembler: EventRecurrenceAssembler,
    ) -> None:
        self._settings = settings
        self._idNormalizer = idNormalizer
        self._intervalNormalizer = intervalNormalizer
        self._intervalAssembler = intervalAssembler

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

        if not dto.isRecurrent:
            return dto

        recurrenceInterval = self._intervalNormalizer.normalize(
            event.getRecurrenceInterval()
        )
        recurrenceInterval = recurrenceInterval.splitlines()
        recurrenceInterval = recurrenceInterval[
            len(recurrenceInterval) - 1
        ]  # get only latest line
        recurrenceInterval = recurrenceInterval[
            6:
        ]  # remove 'RRULE:' from the beginning
        recurrenceIntervalParts = self._intervalAssembler.disassemble(
            recurrenceInterval
        )

        if EventRecurrenceAssembler.FREQ in recurrenceIntervalParts:
            dto.recurrenceIntervalFreq = recurrenceIntervalParts[
                EventRecurrenceAssembler.FREQ
            ]

        if EventRecurrenceAssembler.INTERVAL in recurrenceIntervalParts:
            dto.recurrenceIntervalInterval = recurrenceIntervalParts[
                EventRecurrenceAssembler.INTERVAL
            ]

        if EventRecurrenceAssembler.BYWEEKDAY in recurrenceIntervalParts:
            dto.recurrenceIntervalByWeekDay = recurrenceIntervalParts[
                EventRecurrenceAssembler.BYWEEKDAY
            ]

        if EventRecurrenceAssembler.BYMONTHDAY in recurrenceIntervalParts:
            dto.recurrenceIntervalByMonthDay = recurrenceIntervalParts[
                EventRecurrenceAssembler.BYMONTHDAY
            ]

        if EventRecurrenceAssembler.BYMONTH in recurrenceIntervalParts:
            dto.recurrenceIntervalByMonth = recurrenceIntervalParts[
                EventRecurrenceAssembler.BYMONTH
            ]

        r = RecurringEvent()
        dto.recurrenceIntervalHumanText = r.format(
            self._intervalNormalizer.normalize(
                self._ensureRecurrenceIntervalIntegrity(
                    event.getRecurrenceInterval(),
                    startDate,
                )
            )
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

        if isRecurrent and dto.recurrenceIntervalFreq is not None:
            recurrenceInterval = self._intervalNormalizer.denormalize(
                self._intervalAssembler.assemble(
                    {
                        EventRecurrenceAssembler.FREQ: dto.recurrenceIntervalFreq,
                        EventRecurrenceAssembler.INTERVAL: dto.recurrenceIntervalInterval,
                        EventRecurrenceAssembler.BYWEEKDAY: dto.recurrenceIntervalByWeekDay,
                        EventRecurrenceAssembler.BYMONTHDAY: dto.recurrenceIntervalByMonthDay,
                        EventRecurrenceAssembler.BYMONTH: dto.recurrenceIntervalByMonth,
                    }
                )
            )
            recurrenceInterval = self._ensureRecurrenceIntervalIntegrity(
                recurrenceInterval, startDate
            )
        else:
            recurrenceInterval = None

        return Event(
            id=eventId,
            title=title,
            dateTimeRange=dateTimeRange,
            isRecurrent=isRecurrent,
            recurrenceInterval=recurrenceInterval,
        )

    def _ensureRecurrenceIntervalIntegrity(
        self, interval: EventInterval, startDate: datetime.datetime
    ) -> EventInterval:
        rule = interval.getInterval()

        # Replace start date and first week day in the rule
        # in order to ensure the integrity.
        if isinstance(rule, rrule.rrule):
            weekStart = self._settings.getFirstWeekDay()
            rule = rule.replace(dtstart=startDate, wkst=weekStart)
            interval = EventInterval(rule)

        return interval
