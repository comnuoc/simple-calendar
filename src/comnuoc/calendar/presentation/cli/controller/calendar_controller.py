from comnuoc.calendar.application.calendar.calendar_service import CalendarService
from comnuoc.calendar.application.setting.setting_service import SettingService

from comnuoc.calendar.presentation.cli.helper.calendar_formatter import (
    CalendarFormatter,
)

from comnuoc.calendar.presentation.cli.helper.input_helper import InputHelper
from comnuoc.calendar.presentation.cli.helper.menu_formatter import MenuFormatter


class CalendarController(object):
    def __init__(
        self,
        inputHelper: InputHelper,
        menuFormatter: MenuFormatter,
        settingService: SettingService,
        calendarService: CalendarService,
        calendarFormatter: CalendarFormatter,
    ) -> None:
        self._inputHelper = inputHelper
        self._menuFormatter = menuFormatter
        self._settingService = settingService
        self._calendarService = calendarService
        self._calendarFormatter = calendarFormatter

    def displayMonth(self) -> None:
        print()
        print(self._menuFormatter.formatTitle("Calendar - View Month"))
        print()

        now = self._settingService.getNow()
        year = self._inputHelper.inputYear(now["year"])
        month = self._inputHelper.inputMonth(now["month"])

        monthDates = self._calendarService.getMonthDates(year, month)

        print()
        print(
            self._menuFormatter.formatContent(
                self._calendarFormatter.formatMonth(year, month, monthDates), True, 53
            )
        )

    def displayWeek(self) -> None:
        print()
        print(self._menuFormatter.formatTitle("Calendar - View Week"))
        print()

        now = self._settingService.getNow()
        year = self._inputHelper.inputYear(now["year"])
        week = self._inputHelper.inputWeek(now["week"])

        weekNumber, dates = self._calendarService.getWeekDates(year, week)

        print()
        print(
            self._menuFormatter.formatContent(
                self._calendarFormatter.formatWeek(year, weekNumber, dates), True, 53
            )
        )
