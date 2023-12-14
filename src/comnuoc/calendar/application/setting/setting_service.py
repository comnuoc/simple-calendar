import datetime
from typing import Union

from comnuoc.calendar.domain.util.calendar import CalendarUtil

from comnuoc.calendar.infrastructure.util.setting_repository import (
    FileSettingRepository,
)


class SettingService(object):
    def __init__(
        self, settings: FileSettingRepository, calendarUtil: CalendarUtil
    ) -> None:
        self._settings = settings
        self._calendarUtil = calendarUtil

    def getTimeZone(self) -> Union[str, None]:
        return self._settings.getTimeZone()

    def getIso8601(self) -> bool:
        return self._settings.getIso8601()

    def getFirstWeekDay(self) -> int:
        return self._settings.getFirstWeekDay()

    def getEventsFilePath(self) -> Union[str, None]:
        return self._settings.getEventsFilePath()

    def setTimeZone(self, timeZone: Union[str, None]) -> None:
        self._settings.setTimeZone(timeZone)

    def setIso8601(self, is8601: bool) -> None:
        self._settings.setIso8601(is8601)

    def setFirstWeekDay(self, firstWeekDay: int) -> None:
        self._settings.setFirstWeekDay(firstWeekDay)

    def setEventsFilePath(self, path: str) -> None:
        self._settings.setEventsFilePath(path)

    def getNow(self) -> dict[str, int]:
        date = datetime.datetime.now(self._settings.getTzInfo())

        return self._createDateInfoResponse(date)

    def getDateInfo(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ) -> dict[str, int]:
        date = datetime.datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
            tzinfo=self._settings.getTzInfo(),
        )

        return self._createDateInfoResponse(date)

    def _createDateInfoResponse(self, date: datetime.datetime) -> dict[str, int]:
        return {
            "year": date.year,
            "month": date.month,
            "day": date.day,
            "hour": date.hour,
            "minute": date.minute,
            "second": date.second,
            "microsecond": date.microsecond,
            "week": self._calendarUtil.calculateWeekNumber(date.date()),
        }
