import datetime

from dateutil import relativedelta

from comnuoc.calendar.domain.util.calendar import CalendarUtil
from comnuoc.calendar.domain.util.datetime_range import DateTimeRange

from comnuoc.calendar.infrastructure.event.event_repository import EventRepository
from comnuoc.calendar.infrastructure.util.setting_repository import (
    FileSettingRepository,
)


class CalendarService(object):
    WeekNumber = WeekDateYear = WeekDateMonth = WeekDateDay = int
    WeekDateHasEvent = bool
    WeekDates = tuple[WeekDateYear, WeekDateMonth, WeekDateDay, WeekDateHasEvent]
    WeekDatesResponse = tuple[WeekNumber, list[WeekDates]]

    def __init__(
        self,
        settings: FileSettingRepository,
        calendarUtil: CalendarUtil,
        eventRepository: EventRepository,
    ) -> None:
        self._settings = settings
        self._calendarUtil = calendarUtil
        self._eventRepository = eventRepository

    def getMonthDates(self, year: int, month: int) -> list[WeekDatesResponse]:
        monthDates = []
        weekDatesTuples = self._calendarUtil.getMonthDates(year, month)

        for weekDatesTuple in weekDatesTuples:
            monthDates.append(self.__createWeekDatesResponse(weekDatesTuple))

        return monthDates

    def getWeekDates(self, year: int, week: int) -> WeekDatesResponse:
        return self.__createWeekDatesResponse(
            self._calendarUtil.getWeekDates(year, week)
        )

    def __createWeekDatesResponse(
        self, weekDates: CalendarUtil.WeekDatesTuple
    ) -> WeekDatesResponse:
        weekNumber, dates = weekDates
        dateTuples = [
            (
                date.year,
                date.month,
                date.day,
                self.__hasDayEvent(year=date.year, month=date.month, day=date.day),
            )
            for date in dates
        ]

        return (weekNumber, dateTuples)

    def __hasDayEvent(self, year: int, month: int, day: int) -> bool:
        startDate = datetime.datetime(
            year=year, month=month, day=day, tzinfo=self._settings.getTzInfo()
        )
        endDate = startDate + relativedelta.relativedelta(days=+1)
        range = DateTimeRange(startDate, endDate, True, False)

        return self._eventRepository.hasEventInRange(range)
