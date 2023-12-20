from comnuoc.calendar.application.event.event_dto import EventDto
from comnuoc.calendar.application.event.event_service import EventService
from comnuoc.calendar.application.setting.setting_service import SettingService

from comnuoc.calendar.presentation.cli.helper.event_formatter import EventFormatter
from comnuoc.calendar.presentation.cli.helper.input_helper import InputHelper
from comnuoc.calendar.presentation.cli.helper.menu_formatter import MenuFormatter
from comnuoc.calendar.presentation.cli.helper.recurrence_event_input_helper import (
    RecurrenceEventInputHelper,
)


class EventController(object):
    def __init__(
        self,
        inputHelper: InputHelper,
        settingService: SettingService,
        eventService: EventService,
        menuFormatter: MenuFormatter,
        eventFormatter: EventFormatter,
        recurrenceEventInputHelper: RecurrenceEventInputHelper,
    ) -> None:
        self._inputHelper = inputHelper
        self._settingService = settingService
        self._eventService = eventService
        self._menuFormatter = menuFormatter
        self._eventFormatter = eventFormatter
        self._recurrenceEventInputHelper = recurrenceEventInputHelper

    def displayTodayEvents(self) -> None:
        now = self._settingService.getNow()

        print()
        print(
            self._menuFormatter.formatTitle(
                f'Calendar - Today Events - {now["year"]}-{now["month"]}-{now["day"]}'
            )
        )

        self._printDayEvents(now["year"], now["month"], now["day"])

    def displayDayEvents(self) -> None:
        print()
        print(self._menuFormatter.formatTitle("Calendar - View Events"))
        print()

        now = self._settingService.getNow()
        year = self._inputHelper.inputYear(now["year"])
        month = self._inputHelper.inputMonth(now["month"])
        day = self._inputHelper.inputDay(now["day"])

        self._printDayEvents(year, month, day)

    def displayEventDetail(self) -> None:
        print()
        print(self._menuFormatter.formatTitle("Calendar - View Event Detail"))
        print()

        id = self._inputHelper.inputNotBlankStr("Event ID")

        try:
            event = self._eventService.getEvent(id)
        except ValueError:
            event = None

        print()

        if event is None:
            self._inputHelper.printErrorMessage(f'Event with ID "{id}" is not found')
        else:
            print(
                self._menuFormatter.formatContent(
                    self._eventFormatter.formatEvent(event), True
                )
            )

    def addEvent(self) -> None:
        print()
        print(self._menuFormatter.formatTitle("Calendar - Add Event"))
        print()

        eventDto = self._inputEvent(self._createDefaultEventDto())

        try:
            eventDto = self._eventService.insertEvent(eventDto)
        except Exception as e:
            print()
            self._inputHelper.printErrorMessage(str(e))

            return

        print()
        self._inputHelper.printSuccessMessage("Event has just been added.")
        print(
            self._menuFormatter.formatContent(
                self._eventFormatter.formatEvent(eventDto), True
            )
        )

    def updateEvent(self) -> None:
        print()
        print(self._menuFormatter.formatTitle("Calendar - Update Event"))
        print()

        id = self._inputHelper.inputNotBlankStr("Event ID")

        try:
            event = self._eventService.getEvent(id)
        except ValueError:
            event = None

        print()

        if event is None:
            self._inputHelper.printErrorMessage(f'Event with ID "{id}" is not found')

            return

        eventDto = self._inputEvent(event)
        eventDto.id = event.id

        try:
            eventDto = self._eventService.updateEvent(eventDto)
        except Exception as e:
            print()
            self._inputHelper.printErrorMessage(str(e))

            return

        print()
        self._inputHelper.printSuccessMessage("Event has just been updated.")
        print(
            self._menuFormatter.formatContent(
                self._eventFormatter.formatEvent(eventDto), True
            )
        )

    def deleteEvent(self) -> None:
        print()
        print(self._menuFormatter.formatTitle("Calendar - Delete Event"))
        print()

        id = self._inputHelper.inputNotBlankStr("Event ID")

        print()
        self._inputHelper.printWarningMessage(
            "Are you sure you want to delete this event?"
        )
        print()

        confirm = self._inputHelper.inputBool("Please confirm", False)

        if not confirm:
            return

        try:
            deletedEvent = self._eventService.deleteEvent(id)
        except Exception as e:
            print()
            self._inputHelper.printErrorMessage(str(e))

            return

        print()
        self._inputHelper.printSuccessMessage("Event has just been deleted.")
        print(
            self._menuFormatter.formatContent(
                self._eventFormatter.formatEvent(deletedEvent), True
            )
        )

    def _printDayEvents(self, year: int, month: int, day: int) -> None:
        events = self._eventService.getEventsByDate(year, month, day)

        print()

        if len(events) > 0:
            for event in events:
                print(
                    self._menuFormatter.formatContent(
                        self._eventFormatter.formatEvent(event), True
                    )
                )
                print()
        else:
            self._inputHelper.printInfoMessage("There is no event on this day")

    def _createDefaultEventDto(self) -> EventDto:
        now = self._settingService.getNow()

        defaultDto = EventDto()

        defaultDto.title = None
        defaultDto.dateYear = now["year"]
        defaultDto.dateMonth = now["month"]
        defaultDto.dateDay = now["day"]
        defaultDto.startDateHour = defaultDto.endDateHour = now["hour"]
        defaultDto.startDateMinute = defaultDto.endDateMinute = now["minute"]
        defaultDto.isRecurrent = False

        return defaultDto

    def _inputEvent(self, defaultDto: EventDto) -> EventDto:
        eventDto = EventDto()

        eventDto.title = self._inputHelper.inputNotBlankStr("Title", defaultDto.title)
        eventDto.dateYear = self._inputHelper.inputYear(defaultDto.dateYear)
        eventDto.dateMonth = self._inputHelper.inputMonth(defaultDto.dateMonth)
        eventDto.dateDay = self._inputHelper.inputDay(defaultDto.dateDay)
        eventDto.startDateHour = self._inputHelper.inputHour(
            defaultDto.startDateHour, "Start Hour"
        )
        eventDto.startDateMinute = self._inputHelper.inputMinute(
            defaultDto.startDateMinute, "Start Minute"
        )
        eventDto.endDateHour = self._inputHelper.inputHour(
            defaultDto.endDateHour, "End Hour"
        )
        eventDto.endDateMinute = self._inputHelper.inputMinute(
            defaultDto.endDateMinute, "End Minute"
        )

        self._recurrenceEventInputHelper.inputEventRecurrence(eventDto, defaultDto)

        return eventDto
