import re

from comnuoc.calendar.application.event.event_dto import EventDto
from comnuoc.calendar.application.service_container import ServiceContainer

from comnuoc.calendar.presentation.cli.calendar_formatter import CalendarFormatter
from comnuoc.calendar.presentation.cli.event_formatter import EventFormatter
from comnuoc.calendar.presentation.cli.input_helper import InputHelper
from comnuoc.calendar.presentation.cli.menu_formatter import MenuFormatter


class Cli(object):
    RECURRENCE_FREQS = dict(zip(["y", "m", "w", "d"], EventDto.RECURRENCE_FREQS))
    RECURRENCE_FREQ_SHORTCUTS = {v: k for k, v in RECURRENCE_FREQS.items()}

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
        self._inputHelper.clearScreen()

        print()
        print(self._menuFormatter.formatTitle("Calendar - View Month"))
        print()

        now = self._serviceContainer.getSettingService().getNow()
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
        self._inputHelper.clearScreen()

        print()
        print(self._menuFormatter.formatTitle("Calendar - View Week"))
        print()

        now = self._serviceContainer.getSettingService().getNow()
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
        self._inputHelper.clearScreen()

        print()
        print(self._menuFormatter.formatTitle("Calendar - View Events"))
        print()

        now = self._serviceContainer.getSettingService().getNow()
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
        self._inputHelper.clearScreen()

        print()
        print(self._menuFormatter.formatTitle("Calendar - Add Event"))
        print()

        eventDto = self._inputEvent(self._createDefaultEventDto())

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

        eventDto = self._inputEvent(event)
        eventDto.id = event.id

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

    def _createDefaultEventDto(self) -> EventDto:
        now = self._serviceContainer.getSettingService().getNow()

        defaultDto = EventDto()

        defaultDto.title = None
        defaultDto.dateYear = now["year"]
        defaultDto.dateMonth = now["month"]
        defaultDto.dateDay = now["day"]
        defaultDto.startDateHour = defaultDto.endDateHour = now["hour"]
        defaultDto.startDateMinute = defaultDto.endDateMinute = now["minute"]

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

        self._inputEventRecurrence(eventDto, defaultDto)

        return eventDto

    def _inputEventRecurrence(self, eventDto: EventDto, defaultDto: EventDto) -> None:
        eventDto.isRecurrent = self._inputHelper.inputBool(
            "Is Recurrent Event?", defaultDto.isRecurrent
        )

        if not eventDto.isRecurrent:
            return

        print()
        print("Repeat:")
        print("1. Every day")
        print("2. Every week")
        print("3. Every 2 weeks")
        print("4. Every month")
        print("5. Every year")
        print("6. Custom")

        defaultRepeatChoice = None

        if (
            (defaultDto.recurrenceIntervalByWeekDay is not None)
            or (defaultDto.recurrenceIntervalByMonthDay is not None)
            or (defaultDto.recurrenceIntervalByMonth is not None)
        ):
            defaultRepeatChoice = 6
        elif (
            "DAILY" == defaultDto.recurrenceIntervalFreq
            and 1 == defaultDto.recurrenceIntervalInterval
        ):
            defaultRepeatChoice = 1
        elif (
            "WEEKLY" == defaultDto.recurrenceIntervalFreq
            and 1 == defaultDto.recurrenceIntervalInterval
        ):
            defaultRepeatChoice = 2
        elif (
            "WEEKLY" == defaultDto.recurrenceIntervalFreq
            and 2 == defaultDto.recurrenceIntervalInterval
        ):
            defaultRepeatChoice = 3
        elif (
            "MONTHLY" == defaultDto.recurrenceIntervalFreq
            and 1 == defaultDto.recurrenceIntervalInterval
        ):
            defaultRepeatChoice = 4
        elif (
            "YEARLY" == defaultDto.recurrenceIntervalFreq
            and 1 == defaultDto.recurrenceIntervalInterval
        ):
            defaultRepeatChoice = 5
        elif defaultDto.recurrenceIntervalFreq is not None:
            defaultRepeatChoice = 6

        repeatChoice = self._inputHelper.inputInt(
            message="Choose the repeat",
            default=defaultRepeatChoice,
            validator=lambda val: val > 0 and val < 7,
        )

        if 1 == repeatChoice:
            eventDto.recurrenceIntervalFreq = "DAILY"
            eventDto.recurrenceIntervalInterval = 1
        elif 2 == repeatChoice:
            eventDto.recurrenceIntervalFreq = "WEEKLY"
            eventDto.recurrenceIntervalInterval = 1
        elif 3 == repeatChoice:
            eventDto.recurrenceIntervalFreq = "WEEKLY"
            eventDto.recurrenceIntervalInterval = 2
        elif 4 == repeatChoice:
            eventDto.recurrenceIntervalFreq = "MONTHLY"
            eventDto.recurrenceIntervalInterval = 1
        elif 5 == repeatChoice:
            eventDto.recurrenceIntervalFreq = "YEARLY"
            eventDto.recurrenceIntervalInterval = 1
        else:
            self._inputEventRecurrenceCustom(eventDto, defaultDto)

    def _inputEventRecurrenceCustom(
        self, eventDto: EventDto, defaultDto: EventDto
    ) -> None:
        print()

        self._inputEventRecurrenceFreq(eventDto, defaultDto)

        if "WEEKLY" == eventDto.recurrenceIntervalFreq:
            self._inputEventRecurrenceWeekly(eventDto, defaultDto)
        elif "MONTHLY" == eventDto.recurrenceIntervalFreq:
            self._inputEventRecurrenceMonthly(eventDto, defaultDto)
        elif "YEARLY" == eventDto.recurrenceIntervalFreq:
            self._inputEventRecurrenceYearly(eventDto, defaultDto)

    def _inputEventRecurrenceFreq(
        self, eventDto: EventDto, defaultDto: EventDto
    ) -> None:
        recurrenceIntervalFreqHint = ", ".join(
            [f"{k}: {v}" for k, v in self.RECURRENCE_FREQS.items()]
        )
        recurrenceIntervalFreq = self._inputHelper.inputStr(
            message=f"Recurrence Frequency ({recurrenceIntervalFreqHint})",
            default=self.RECURRENCE_FREQ_SHORTCUTS[defaultDto.recurrenceIntervalFreq],
            validator=lambda val: val.lower() in self.RECURRENCE_FREQS.keys(),
        )
        recurrenceIntervalFreq = recurrenceIntervalFreq.lower()

        eventDto.recurrenceIntervalFreq = self.RECURRENCE_FREQS[recurrenceIntervalFreq]
        eventDto.recurrenceIntervalInterval = self._inputHelper.inputInt(
            message="The interval between each freq iteration",
            default=defaultDto.recurrenceIntervalInterval,
            validator=lambda val: val > 0,
        )

    def _inputEventRecurrenceWeekly(
        self, eventDto: EventDto, defaultDto: EventDto
    ) -> None:
        weekDaysMessage = [
            "The weekdays where the recurrence will be applied:",
            "Value is one of: '" + "', '".join(EventDto.RECURRENCE_WEEKDAYS) + "'.",
        ]
        print()
        print("\n".join(weekDaysMessage))

        recurrenceIntervalByWeekDay = self._inputHelper.inputMultipleStr(
            message="The weekday",
            default=defaultDto.recurrenceIntervalByWeekDay,
            singleValueValidator=lambda val: val.upper()
            in EventDto.RECURRENCE_WEEKDAYS,
            defaultMessage="Default weekdays",
            singleValueErrorMessage="Wrong weekday format",
        )

        eventDto.recurrenceIntervalByWeekDay = [
            val.upper() for val in recurrenceIntervalByWeekDay
        ]

    def _inputEventRecurrenceMonthly(
        self, eventDto: EventDto, defaultDto: EventDto
    ) -> None:
        print()
        isRecurrenceIntervalByWeekDay = self._inputHelper.inputBool(
            "By weekdays?", defaultDto.recurrenceIntervalByWeekDay is not None
        )

        if isRecurrenceIntervalByWeekDay:
            self._inputEventRecurrenceByWeekDay(eventDto, defaultDto)
        else:
            print()
            print("The month days to apply the recurrence to:")

            eventDto.recurrenceIntervalByMonthDay = self._inputHelper.inputMultipleInt(
                message="The month day",
                default=defaultDto.recurrenceIntervalByMonthDay,
                singleValueValidator=lambda val: val > 0 and val < 32,
                singleValueErrorMessage="Day should be between 1 and 31",
                defaultMessage="Default month days",
            )

    def _inputEventRecurrenceYearly(
        self, eventDto: EventDto, defaultDto: EventDto
    ) -> None:
        print()
        print("The months to apply the recurrence to:")

        eventDto.recurrenceIntervalByMonth = self._inputHelper.inputMultipleInt(
            message="The month",
            default=defaultDto.recurrenceIntervalByMonth,
            singleValueValidator=lambda val: val > 0 and val < 13,
            singleValueErrorMessage="Month should be between 1 and 12",
            defaultMessage="Default months",
        )

        print()
        isRecurrenceIntervalByWeekDay = self._inputHelper.inputBool(
            "By weekdays?", defaultDto.recurrenceIntervalByWeekDay is not None
        )

        if isRecurrenceIntervalByWeekDay:
            self._inputEventRecurrenceByWeekDay(eventDto, defaultDto)

    def _inputEventRecurrenceByWeekDay(
        self, eventDto: EventDto, defaultDto: EventDto
    ) -> None:
        weekDaysMessage = [
            "The weekdays where the recurrence will be applied:",
            "Value is one of: '" + "', '".join(EventDto.RECURRENCE_WEEKDAYS) + "'",
            "Or '+1MO' or 'MO(+1)': the first Monday",
            "Or '+2TU' or 'TU(+2)': the second Tuesday",
        ]
        print()
        print("\n".join(weekDaysMessage))

        weekDaysRegex = "|".join(EventDto.RECURRENCE_WEEKDAYS)
        regex1 = f"^(\+[1-5])?({weekDaysRegex})$"  # e.g: +1MO
        regex2 = f"^({weekDaysRegex})\(\+[1-5]\)$"  # e.g: MO(+1)
        regex = f"({regex1})|({regex2})"

        recurrenceIntervalByWeekDay = self._inputHelper.inputMultipleStr(
            message="The weekday",
            default=defaultDto.recurrenceIntervalByWeekDay,
            singleValueValidator=lambda val: re.search(regex, val.upper()) is not None,
            singleValueErrorMessage="Wrong weekday format",
            defaultMessage="Default weekdays",
        )

        eventDto.recurrenceIntervalByWeekDay = [
            val.upper() for val in recurrenceIntervalByWeekDay
        ]
