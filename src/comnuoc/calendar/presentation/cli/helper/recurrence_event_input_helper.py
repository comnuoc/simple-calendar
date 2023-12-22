import re

from comnuoc.calendar.application.event.event_dto import EventDto

from comnuoc.calendar.presentation.cli.helper.input_helper import InputHelper


class RecurrenceEventInputHelper(object):
    RECURRENCE_FREQS = dict(zip(["y", "m", "w", "d"], EventDto.RECURRENCE_FREQS))
    RECURRENCE_FREQ_SHORTCUTS = {v: k for k, v in RECURRENCE_FREQS.items()}

    def __init__(self, inputHelper: InputHelper) -> None:
        self._inputHelper = inputHelper

    def inputEventRecurrence(self, eventDto: EventDto, defaultDto: EventDto) -> None:
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

        if defaultDto.recurrenceIntervalFreq in self.RECURRENCE_FREQ_SHORTCUTS:
            defaultFreq = self.RECURRENCE_FREQ_SHORTCUTS[
                defaultDto.recurrenceIntervalFreq
            ]
        else:
            defaultFreq = None

        recurrenceIntervalFreq = self._inputHelper.inputStr(
            message=f"Recurrence Frequency ({recurrenceIntervalFreqHint})",
            default=defaultFreq,
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
        self._inputEventRecurrenceByWeekDay(eventDto, defaultDto)

    def _inputEventRecurrenceMonthly(
        self, eventDto: EventDto, defaultDto: EventDto
    ) -> None:
        self._inputEventRecurrenceByMonthDay(eventDto, defaultDto)
        self._inputEventRecurrenceByWeekDay(eventDto, defaultDto)

    def _inputEventRecurrenceYearly(
        self, eventDto: EventDto, defaultDto: EventDto
    ) -> None:
        self._inputEventRecurrenceByYearDay(eventDto, defaultDto)
        self._inputEventRecurrenceByMonth(eventDto, defaultDto)
        self._inputEventRecurrenceByMonthDay(eventDto, defaultDto)
        self._inputEventRecurrenceByWeekDay(eventDto, defaultDto)

    def _inputEventRecurrenceByWeekDay(
        self, eventDto: EventDto, defaultDto: EventDto
    ) -> None:
        weekDaysMessage = [
            "The weekdays where the recurrence will be applied:",
            "Value is one of: '" + "', '".join(EventDto.RECURRENCE_WEEKDAYS) + "'.",
        ]

        if "WEEKLY" != eventDto.recurrenceIntervalFreq:
            weekDaysMessage += [
                "Or '+1MO' or 'MO(+1)': the first Monday",
                "Or '+2TU' or 'TU(+2)': the second Tuesday",
                "Or '-1MO' or 'MO(-1)': the last Monday",
            ]

            weekDaysRegex = "|".join(EventDto.RECURRENCE_WEEKDAYS)
            regex1 = f"^(\+|\-[1-5])?({weekDaysRegex})$"  # e.g: +1MO
            regex2 = f"^({weekDaysRegex})\(\+|\-[1-5]\)$"  # e.g: MO(+1)
            regex = f"({regex1})|({regex2})"
            singleValueValidator = lambda val: re.search(regex, val.upper()) is not None
        else:
            singleValueValidator = (
                lambda val: val.upper() in EventDto.RECURRENCE_WEEKDAYS
            )

        print()
        print("\n".join(weekDaysMessage))

        recurrenceIntervalByWeekDay = self._inputHelper.inputMultipleStr(
            message="The weekday",
            default=defaultDto.recurrenceIntervalByWeekDay,
            singleValueValidator=singleValueValidator,
            singleValueErrorMessage="Wrong weekday format.",
            defaultMessage="Default weekdays",
        )

        eventDto.recurrenceIntervalByWeekDay = [
            val.upper() for val in recurrenceIntervalByWeekDay
        ]

    def _inputEventRecurrenceByMonthDay(
        self, eventDto: EventDto, defaultDto: EventDto
    ) -> None:
        message = [
            "The month days to apply the recurrence to:",
            "Valid values are 1 to 31 or -31 to -1.",
            "-10: represents the tenth to the last day of the month.",
            "-1: represents the last day of the month.",
        ]

        print()
        print("\n".join(message))

        eventDto.recurrenceIntervalByMonthDay = self._inputHelper.inputMultipleInt(
            message="The month day",
            default=defaultDto.recurrenceIntervalByMonthDay,
            singleValueValidator=lambda val: val > -32 and val < 32 and val != 0,
            singleValueErrorMessage="Valid values are 1 to 31 or -31 to -1.",
            defaultMessage="Default month days",
        )

    def _inputEventRecurrenceByMonth(
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

    def _inputEventRecurrenceByYearDay(
        self, eventDto: EventDto, defaultDto: EventDto
    ) -> None:
        message = [
            "The year days to apply the recurrence to:",
            "Valid values are 1 to 366 or -366 to -1.",
            "-1: represents the last day of the year (December 31st)."
            "-306: represents the 306th to the last day of the year (March 1st).",
        ]

        print()
        print("\n".join(message))

        eventDto.recurrenceIntervalByYearDay = self._inputHelper.inputMultipleInt(
            message="The year day",
            default=defaultDto.recurrenceIntervalByYearDay,
            singleValueValidator=lambda val: val > -367 and val < 367 and val != 0,
            singleValueErrorMessage="Valid values are 1 to 366 or -366 to -1.",
            defaultMessage="Default year days",
        )
