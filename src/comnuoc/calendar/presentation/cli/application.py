from comnuoc.calendar.application.service_container import ServiceContainer

from comnuoc.calendar.presentation.cli.controller.calendar_controller import (
    CalendarController,
)
from comnuoc.calendar.presentation.cli.controller.event_controller import (
    EventController,
)
from comnuoc.calendar.presentation.cli.controller.setting_controller import (
    SettingController,
)

from comnuoc.calendar.presentation.cli.helper.calendar_formatter import (
    CalendarFormatter,
)
from comnuoc.calendar.presentation.cli.helper.event_formatter import EventFormatter
from comnuoc.calendar.presentation.cli.helper.input_helper import InputHelper
from comnuoc.calendar.presentation.cli.helper.menu_formatter import MenuFormatter
from comnuoc.calendar.presentation.cli.helper.recurrence_event_input_helper import (
    RecurrenceEventInputHelper,
)


class Application(object):
    def __init__(self) -> None:
        serviceContainer = ServiceContainer()
        settingService = serviceContainer.getSettingService()

        self._inputHelper = InputHelper()
        self._menuFormatter = MenuFormatter()
        self._calendarController = CalendarController(
            inputHelper=self._inputHelper,
            menuFormatter=self._menuFormatter,
            settingService=settingService,
            calendarService=serviceContainer.getCalendarService(),
            calendarFormatter=CalendarFormatter(settingService.getFirstWeekDay()),
        )
        self._eventController = EventController(
            inputHelper=self._inputHelper,
            settingService=settingService,
            eventService=serviceContainer.getEventService(),
            menuFormatter=self._menuFormatter,
            eventFormatter=EventFormatter(),
            recurrenceEventInputHelper=RecurrenceEventInputHelper(self._inputHelper),
        )
        self._settingController = SettingController(
            inputHelper=self._inputHelper,
            menuFormatter=self._menuFormatter,
            settingService=settingService,
        )

    def run(self, clearScreen: bool = False) -> None:
        if clearScreen:
            self._inputHelper.clearScreen()

        self._eventController.displayTodayEvents()
        self.__displayMenu(clearScreen)

    def __displayMenu(self, clearScreen: bool = False) -> None:
        # @todo: implement update settings feature
        options = [
            " 1  View month",
            " 2. View week",
            " 3. View today events",
            " 4. View events on a day",
            " 5. View event detail",
            " 6. Add event",
            " 7. Update event",
            " 8. Delete event",
            " 9. Update settings",
            "10. Exit",
        ]

        print()
        print(self._menuFormatter.formatTitle("Calendar"))
        print(self._menuFormatter.formatOptions(options))
        print()

        action = self._inputHelper.inputInt("Choose your action")

        if clearScreen:
            self._inputHelper.clearScreen()

        if 1 == action:
            self._calendarController.displayMonth()
        elif 2 == action:
            self._calendarController.displayWeek()
        elif 3 == action:
            self._eventController.displayTodayEvents()
        elif 4 == action:
            self._eventController.displayDayEvents()
        elif 5 == action:
            self._eventController.displayEventDetail()
        elif 6 == action:
            self._eventController.addEvent()
        elif 7 == action:
            self._eventController.updateEvent()
        elif 8 == action:
            self._eventController.deleteEvent()
        elif 9 == action:
            self._settingController.updateSettings()
            # restart application in order to use new settings
            self.__init__()
        else:
            return

        self.__displayMenu(clearScreen)
