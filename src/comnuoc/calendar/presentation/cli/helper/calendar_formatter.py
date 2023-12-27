import calendar

from comnuoc.calendar.application.calendar.calendar_service import CalendarService


class CalendarFormatter(object):
    def __init__(self, firstWeekDay: int = calendar.MONDAY) -> None:
        self._textCalendar = calendar.TextCalendar(firstWeekDay)

    def formatMonth(
        self,
        year: int,
        month: int,
        weekDates: list[CalendarService.WeekDatesResponse],
        width: int = 5,
        line: int = 2,
    ) -> str:
        width = max(3, width)
        line = max(1, line)
        content = self._textCalendar.formatmonthname(year, month, 8 * (width + 1) - 1)
        content = content.rstrip()
        content += "\n" * line
        content += (
            " ".center(width)
            + " "
            + self._textCalendar.formatweekheader(width).rstrip()
        )
        content += "\n" * line

        for weekDatesResponse in weekDates:
            weekNumber, dates = weekDatesResponse
            content += self.__formatWeekInMonth(
                year, month, weekNumber, dates, width
            ).rstrip()
            content += "\n" * line

        return content

    def formatWeek(
        self,
        year,
        weekNumber: int,
        dates: list[CalendarService.WeekDates],
        width: int = 5,
        line: int = 2,
    ) -> str:
        content = "\n"
        content += (
            " ".center(width)
            + " "
            + self._textCalendar.formatweekheader(width).rstrip()
        )
        content += "\n" * line
        content += self.__formatWeekInMonth(year, 0, weekNumber, dates, width).rstrip()
        content += "\n" * line

        return content

    def formatDay(self, day: int, hasEvent: bool, width: int) -> str:
        if 0 == day:
            content = " "
        else:
            content = "%2i" % day  # right-align single-digit days

        if hasEvent:
            content = "*" + content

        return content.center(width)

    def __formatWeekInMonth(
        self,
        year: int,
        month: int,
        weekNumber: int,
        dates: list[CalendarService.WeekDates],
        width: int,
    ) -> str:
        content = [self.formatDay(weekNumber, False, width)]

        for weekDate in dates:
            day = weekDate[2]
            hasEvent = weekDate[3]

            if (year != weekDate[0]) or (month != 0 and month != weekDate[1]):
                day = 0
                hasEvent = False

            content.append(self.formatDay(day, hasEvent, width))

        return " ".join(content)
