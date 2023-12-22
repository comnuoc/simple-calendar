from comnuoc.calendar.application.event.event_dto import EventDto
from comnuoc.calendar.application.setting.setting_service import SettingService

from comnuoc.calendar.presentation.cli.helper.input_helper import InputHelper
from comnuoc.calendar.presentation.cli.helper.menu_formatter import MenuFormatter


class SettingController(object):
    def __init__(
        self,
        inputHelper: InputHelper,
        menuFormatter: MenuFormatter,
        settingService: SettingService,
    ) -> None:
        self._inputHelper = inputHelper
        self._menuFormatter = menuFormatter
        self._settingService = settingService

    def updateSettings(self) -> None:
        defaultTimeZone = self._settingService.getTimeZone()
        defaultIso8601 = self._settingService.getIso8601()
        defaultWeekStart = self._settingService.getFirstWeekDay()
        defaultEventsPath = self._settingService.getEventsFilePath()

        print()
        print(self._menuFormatter.formatTitle("Calendar - Settings"))
        print()

        timeZone = self._inputHelper.inputStr(
            message="Time Zone",
            default=defaultTimeZone,
        )
        timeZone = timeZone.strip()

        if "" == timeZone:
            timeZone = None

        iso8601 = self._inputHelper.inputBool("Use ISO8601 standard?", defaultIso8601)

        weekStart = self._inputHelper.inputStr(
            message="First Week Day (mo: Monday, su: Sunday)",
            default=EventDto.RECURRENCE_WEEKDAYS[defaultWeekStart],
            validator=lambda val: val.upper()
            in [EventDto.RECURRENCE_WEEKDAYS[0], EventDto.RECURRENCE_WEEKDAYS[6]],
            errorMessage="Wrong weekday format.",
        )
        weekStart = weekStart.upper()
        weekStart = EventDto.RECURRENCE_WEEKDAYS.index(weekStart)

        eventsPath = self._inputHelper.inputStr("Events File", defaultEventsPath)

        try:
            self._settingService.setTimeZone(timeZone)
            self._settingService.setIso8601(iso8601)
            self._settingService.setFirstWeekDay(weekStart)
            self._settingService.setEventsFilePath(eventsPath)
        except Exception as e:
            print()
            self._inputHelper.printErrorMessage(str(e))

            return

        print()
        self._inputHelper.printSuccessMessage("Settings have just been updated.")
