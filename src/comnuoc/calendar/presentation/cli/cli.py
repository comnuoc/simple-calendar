from comnuoc.calendar.application.event.event_dto import EventDto
from comnuoc.calendar.application.service_container import ServiceContainer

from comnuoc.calendar.presentation.cli.calendar_formatter import CalendarFormatter
from comnuoc.calendar.presentation.cli.event_formatter import EventFormatter
from comnuoc.calendar.presentation.cli.input_helper import InputHelper
from comnuoc.calendar.presentation.cli.menu_formatter import MenuFormatter


class Cli(object):
    def __init__(self) -> None:
        self._serviceContainer = ServiceContainer()
        self._calendarFormatter = CalendarFormatter(
            self._serviceContainer.getSettingService().getFirstWeekDay()
        )
        self._eventFormatter = EventFormatter()
        self._inputHelper = InputHelper()
        self._menuFormatter = MenuFormatter()

    def displayMenu(self, clearScreen: bool = False) -> None:
        # @todo: implement update settings feature
        options = [
            "1. View month",
            "2. View week",
            "3. View events",
            "4. View event detail",
            "5. Add event",
            "6. Update event",
            "7. Delete event",
            "8. Exit",
        ]

        if clearScreen:
            self._inputHelper.clearScreen()

        print()
        print(self._menuFormatter.formatTitle("Calendar"))
        print(self._menuFormatter.formatOptions(options))
        print()
        action = self._inputHelper.inputInt("Choose your action")

        if 1 == action:
            self._displayMonth()
        elif 2 == action:
            self._displayWeek()
        elif 3 == action:
            self._viewEvents()
        elif 4 == action:
            self._viewEventDetail()
        elif 5 == action:
            self._addEvent()
        elif 6 == action:
            self._updateEvent()
        elif 7 == action:
            self._deleteEvent()

    def _displayMonth(self) -> None:
        now = self._serviceContainer.getSettingService().getNow()

        self._inputHelper.clearScreen()

        print()
        print(self._menuFormatter.formatTitle("Calendar - View Month"))
        print()
        year = self._inputHelper.inputYear(now["year"])
        month = self._inputHelper.inputMonth(now["month"])

        monthDates = self._serviceContainer.getCalendarService().getMonthDates(
            year, month
        )

        print()
        print(
            self._menuFormatter.formatContent(
                self._calendarFormatter.formatMonth(year, month, monthDates), True, 53
            )
        )
        self.displayMenu()

    def _displayWeek(self) -> None:
        now = self._serviceContainer.getSettingService().getNow()

        self._inputHelper.clearScreen()

        print()
        print(self._menuFormatter.formatTitle("Calendar - View Week"))
        print()
        year = self._inputHelper.inputYear(now["year"])
        week = self._inputHelper.inputWeek(now["week"])

        weekNumber, dates = self._serviceContainer.getCalendarService().getWeekDates(
            year, week
        )

        print()
        print(
            self._menuFormatter.formatContent(
                self._calendarFormatter.formatWeek(year, weekNumber, dates), True, 53
            )
        )
        self.displayMenu()

    def _viewEvents(self) -> None:
        now = self._serviceContainer.getSettingService().getNow()

        self._inputHelper.clearScreen()

        print()
        print(self._menuFormatter.formatTitle("Calendar - View Events"))
        print()
        year = self._inputHelper.inputYear(now["year"])
        month = self._inputHelper.inputMonth(now["month"])
        day = self._inputHelper.inputDay(now["day"])

        events = self._serviceContainer.getEventService().getEventsByDate(
            year, month, day
        )

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
            print("There is no event on this day")

        self.displayMenu()

    def _viewEventDetail(self) -> None:
        self._inputHelper.clearScreen()

        print()
        print(self._menuFormatter.formatTitle("Calendar - View Event Detail"))
        print()
        id = self._inputHelper.inputNotBlankStr("Event ID")

        try:
            event = self._serviceContainer.getEventService().getEvent(id)
        except ValueError:
            event = None

        print()

        if event is None:
            print(f'Event with ID "{id}" is not found')
        else:
            print(
                self._menuFormatter.formatContent(
                    self._eventFormatter.formatEvent(event), True
                )
            )

        self.displayMenu()

    def _addEvent(self) -> None:
        now = self._serviceContainer.getSettingService().getNow()

        self._inputHelper.clearScreen()

        print()
        print(self._menuFormatter.formatTitle("Calendar - Add Event"))
        print()
        title = self._inputHelper.inputNotBlankStr("Title")
        year = self._inputHelper.inputYear(now["year"])
        month = self._inputHelper.inputMonth(now["month"])
        day = self._inputHelper.inputDay(now["day"])
        startHour = self._inputHelper.inputHour(now["hour"], "Start Hour")
        startMinute = self._inputHelper.inputMinute(now["minute"], "Start Minute")
        endHour = self._inputHelper.inputHour(now["hour"], "End Hour")
        endMinute = self._inputHelper.inputMinute(now["minute"], "End Minute")
        isRecurrent = self._inputHelper.inputBool("Is Recurrent Event?", False)
        recurrenceInterval = None

        if isRecurrent:
            recurrenceInterval = self._inputHelper.inputNotBlankStr(
                "Recurrence Interval"
            )

        eventDto = EventDto()
        eventDto.title = title
        eventDto.dateYear = year
        eventDto.dateMonth = month
        eventDto.dateDay = day
        eventDto.startDateHour = startHour
        eventDto.startDateMinute = startMinute
        eventDto.endDateHour = endHour
        eventDto.endDateMinute = endMinute
        eventDto.isRecurrent = isRecurrent
        eventDto.recurrenceInterval = recurrenceInterval

        try:
            eventDto = self._serviceContainer.getEventService().insertEvent(eventDto)
        except Exception as e:
            print()
            print("Error: " + str(e))
            self.displayMenu()

            return

        print()
        print("Event has just been added.")
        print()

        print(
            self._menuFormatter.formatContent(
                self._eventFormatter.formatEvent(eventDto), True
            )
        )

        self.displayMenu()

    def _updateEvent(self) -> None:
        self._inputHelper.clearScreen()

        print()
        print(self._menuFormatter.formatTitle("Calendar - Update Event"))
        print()
        id = self._inputHelper.inputNotBlankStr("Event ID")

        try:
            event = self._serviceContainer.getEventService().getEvent(id)
        except ValueError:
            event = None

        print()

        if event is None:
            print(f'Event with ID "{id}" is not found')
            self.displayMenu()

            return

        title = self._inputHelper.inputNotBlankStr("Title", event.title)
        year = self._inputHelper.inputYear(event.dateYear)
        month = self._inputHelper.inputMonth(event.dateMonth)
        day = self._inputHelper.inputDay(event.dateDay)
        startHour = self._inputHelper.inputHour(event.startDateHour, "Start Hour")
        startMinute = self._inputHelper.inputMinute(
            event.startDateMinute, "Start Minute"
        )
        endHour = self._inputHelper.inputHour(event.endDateHour, "End Hour")
        endMinute = self._inputHelper.inputMinute(event.endDateMinute, "End Minute")
        isRecurrent = self._inputHelper.inputBool(
            "Is Recurrent Event?", event.isRecurrent
        )
        recurrenceInterval = None

        if isRecurrent:
            recurrenceInterval = self._inputHelper.inputNotBlankStr(
                "Recurrence Interval", event.recurrenceInterval
            )

        eventDto = EventDto()
        eventDto.id = event.id
        eventDto.title = title
        eventDto.dateYear = year
        eventDto.dateMonth = month
        eventDto.dateDay = day
        eventDto.startDateHour = startHour
        eventDto.startDateMinute = startMinute
        eventDto.endDateHour = endHour
        eventDto.endDateMinute = endMinute
        eventDto.isRecurrent = isRecurrent
        eventDto.recurrenceInterval = recurrenceInterval

        try:
            eventDto = self._serviceContainer.getEventService().updateEvent(eventDto)
        except Exception as e:
            print()
            print("Error: " + str(e))
            self.displayMenu()

            return

        print()
        print("Event has just been updated.")
        print()

        print(
            self._menuFormatter.formatContent(
                self._eventFormatter.formatEvent(eventDto), True
            )
        )

        self.displayMenu()

    def _deleteEvent(self) -> None:
        self._inputHelper.clearScreen()

        print()
        print(self._menuFormatter.formatTitle("Calendar - Delete Event"))
        print()
        id = self._inputHelper.inputNotBlankStr("Event ID")

        try:
            deletedEvent = self._serviceContainer.getEventService().deleteEvent(id)
        except Exception as e:
            print()
            print("Error: " + str(e))
            self.displayMenu()

            return

        print()
        print("Event has just been deleted.")
        print()

        print(
            self._menuFormatter.formatContent(
                self._eventFormatter.formatEvent(deletedEvent), True
            )
        )

        self.displayMenu()
