import calendar
import datetime


class CalendarUtil(object):
    WeekDatesTuple = tuple[int, list[datetime.date]]

    def __init__(
        self, iso8601: bool = True, firstWeekDay: int = calendar.MONDAY
    ) -> None:
        self._iso8601 = iso8601

        if self._iso8601:
            self._firstWeekDay = calendar.MONDAY
        else:
            self._firstWeekDay = firstWeekDay

        self._calendar = calendar.Calendar(self._firstWeekDay)

    def getFirstWeekDay(self) -> int:
        return self._firstWeekDay

    def isIso8601(self) -> bool:
        return self._iso8601

    def getMonthDates(self, year: int, month: int) -> list[WeekDatesTuple]:
        """
        Return a list of tuples representing a month's calendar.
        Each tuple represents a week. The first item in tuple is the week number,
        the second item is a list of datetime.date values.
        """
        return [
            (self.calculateWeekNumber(weekDates[0]), weekDates)
            for weekDates in self._calendar.monthdatescalendar(year, month)
        ]

    def getWeekDates(self, year: int, week: int) -> WeekDatesTuple:
        """
        Get dates in a week by a specific week number.
        Return tuple represents a week. The first item in tuple is the week number,
        the second item is a list of datetime.date values.
        """
        yearFormat, weekNumberFormat, weekDayFormat, weekDays = self._getFormats()
        dateFormat = f"{yearFormat}-W{weekNumberFormat}-{weekDayFormat}"
        dates = []
        weekNumber = str(week).zfill(2)
        year = str(year).zfill(4)

        for weekDay in weekDays:
            dateString = f"{year}-W{weekNumber}-{weekDay}"
            dates.append(datetime.datetime.strptime(dateString, dateFormat).date())

        return (week, dates)

    def getWeekDatesByDate(self, date: datetime.date) -> WeekDatesTuple:
        """
        Get dates in a week by a specific date object.
        Return tuple represents a week. The first item in tuple is the week number,
        the second item is a list of datetime.date values.
        """
        week = self.calculateWeekNumber(date)
        year = date.year

        if (
            date.month == 1 and week >= 52
        ):  # in case of the week belongs to previous year
            year -= 1

        return self.getWeekDates(year, week)

    def calculateWeekNumber(self, date: datetime.date) -> int:
        return int(date.strftime(self._getWeekNumberFormat()))

    def _getWeekNumberFormat(self) -> str:
        yearFormat, weekNumberFormat, weekDayFormat, weekDays = self._getFormats()

        return weekNumberFormat

    def _getFormats(self) -> tuple[str, str, str, list[int]]:
        # @see: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
        if self._iso8601:
            yearFormat = "%G"
            weekNumberFormat = "%V"
            weekDayFormat = "%u"
            weekDays = list(range(1, 8))  # 1 is Monday, 6 is Saturday, 7 is Sunday
        else:
            yearFormat = "%Y"
            weekDayFormat = "%w"

            if calendar.MONDAY == self._firstWeekDay:
                weekNumberFormat = "%W"
                weekDays = list(range(1, 7)) + [
                    0
                ]  # 1 is Monday, 6 is Saturday, 0 is Sunday
            else:
                weekNumberFormat = "%U"
                weekDays = list(range(0, 7))  # 0 is Sunday, 1 is Monday, 6 is Saturday

        return yearFormat, weekNumberFormat, weekDayFormat, weekDays
