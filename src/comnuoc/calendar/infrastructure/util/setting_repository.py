import calendar
import configparser
import datetime
from re import sub
from typing import Union

from dateutil import tz

from comnuoc.calendar.domain.util.setting_repository import SettingRepository


class FileSettingRepository(SettingRepository):
    def __init__(
        self,
        filePath: str,
        section: str = "comnuoc.calendar",
        settingTimeZone: str = "timeZone",
        settingIso8601: str = "iso8601",
        settingFirstWeekDay: str = "firstWeekDay",
        settingEventsFilePath: str = "eventsFilePath",
    ) -> None:
        self._filePath = filePath
        self._section = section
        self._config = configparser.ConfigParser()
        self._config.read(filePath)
        self._settingTimeZone = settingTimeZone
        self._settingIso8601 = settingIso8601
        self._settingFirstWeekDay = settingFirstWeekDay
        self._settingEventsFilePath = settingEventsFilePath

    def get(self, key: str, default: str = "") -> str:
        return self._config.get(self._section, key, fallback=default)

    def set(self, key: str, value: str) -> None:
        self.setMultiple({key, value})

    def getMultiple(self, keys: list[str]) -> dict[str, str]:
        return {key: self._get(key) for key in keys}

    def setMultiple(self, values: dict[str, str]) -> None:
        for key, value in values.items():
            self._config.set(self._section, key, value)

        with open(self._filePath, "w") as file:
            self._config.write(file)

    def getTzInfo(self) -> datetime.tzinfo:
        timeZoneName = self.getTimeZone()

        return tz.gettz(timeZoneName)

    def getTimeZone(self, default: str = None) -> Union[str, None]:
        timeZone = self.get(self._settingTimeZone, default)

        if timeZone is None or "" == timeZone:
            return None

        return timeZone

    def setTimeZone(self, timeZone: Union[str, None]) -> None:
        if timeZone is None:
            timeZone = ""

        self.set(self._settingTimeZone, timeZone)

    def getIso8601(self, default: bool = True) -> bool:
        iso = self.get(self._settingIso8601, default)

        if True == iso or "1" == iso:
            return True

        return False

    def setIso8601(self, is8601: bool) -> None:
        if is8601:
            value = "1"
        else:
            value = "0"

        self.set(self._settingIso8601, value)

    def getFirstWeekDay(self, default: int = calendar.MONDAY) -> int:
        value = self.get(self._settingFirstWeekDay, default)

        return int(value)

    def setFirstWeekDay(self, firstWeekDay: int) -> None:
        self.set(self._settingFirstWeekDay, str(firstWeekDay))

    def getEventsFilePath(self, default: None) -> Union[str, None]:
        return self.get(self._settingEventsFilePath, default)

    def setEventsFilePath(self, path: str) -> None:
        self.set(self._settingEventsFilePath, path)
