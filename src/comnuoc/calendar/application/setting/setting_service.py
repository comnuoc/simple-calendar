import datetime
import os
import tarfile
from typing import Union

from dateutil import zoneinfo

from comnuoc.calendar.domain.util.calendar import CalendarUtil

from comnuoc.calendar.infrastructure.util.setting_repository import (
    FileSettingRepository,
)


class SettingService(object):
    def __init__(
        self,
        settings: FileSettingRepository,
        calendarUtil: CalendarUtil,
        defaultEventsPath: str,
    ) -> None:
        self._settings = settings
        self._calendarUtil = calendarUtil
        self._defaultEventsPath = defaultEventsPath

    def getTimeZone(self) -> Union[str, None]:
        return self._settings.getTimeZone()

    def getIso8601(self) -> bool:
        return self._settings.getIso8601()

    def getFirstWeekDay(self) -> int:
        return self._settings.getFirstWeekDay()

    def getEventsFilePath(self) -> str:
        return self._settings.getEventsFilePath(self._defaultEventsPath)

    def setTimeZone(self, timeZone: Union[str, None]) -> None:
        if not self._isTimeZoneValid(timeZone):
            raise ValueError(f'Time zone "{timeZone}" is not valid.')

        self._settings.setTimeZone(timeZone)

    def setIso8601(self, is8601: bool) -> None:
        self._settings.setIso8601(is8601)

    def setFirstWeekDay(self, firstWeekDay: int) -> None:
        self._settings.setFirstWeekDay(firstWeekDay)

    def setEventsFilePath(self, path: str) -> None:
        dirname = os.path.dirname(path)

        if not os.path.isdir(dirname):
            raise OSError(f'Invalid events file. "{dirname}" is not a directory.')

        if os.path.isdir(path):
            raise OSError(f'Invalid events file. "{path}" is a directory.')

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

    def _isTimeZoneValid(self, timeZone: Union[str, None]) -> bool:
        if timeZone is None:
            return True

        ziPath = os.path.abspath(os.path.dirname(zoneinfo.__file__))
        zonesFile = tarfile.TarFile.open(
            os.path.join(ziPath, "dateutil-zoneinfo.tar.gz")
        )
        zoneNames = zonesFile.getnames()

        return timeZone in zoneNames
