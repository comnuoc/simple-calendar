import calendar
import datetime
from typing import Iterable
import unittest

from comnuoc.calendar.domain.util.calendar import CalendarUtil


class CalendarTest(unittest.TestCase):
    def testGetMonthDatesIso8601WeekStartsWithMonday(self) -> None:
        for (
            year,
            month,
            expectedMonthDates,
        ) in self.__getGetMonthDatesIso8601WeekStartsWithMondayData():
            self.__testGetMonthDates(
                True, calendar.MONDAY, year, month, expectedMonthDates
            )

    def testGetMonthDatesIso8601WeekStartsWithSunday(self) -> None:
        for (
            year,
            month,
            expectedMonthDates,
        ) in self.__getGetMonthDatesIso8601WeekStartsWithMondayData():
            self.__testGetMonthDates(
                True, calendar.SUNDAY, year, month, expectedMonthDates
            )

    def testGetMonthDatesWeekStartsWithMonday(self) -> None:
        for (
            year,
            month,
            expectedMonthDates,
        ) in self.__getGetMonthDatesWeekStartsWithMondayData():
            self.__testGetMonthDates(
                False, calendar.MONDAY, year, month, expectedMonthDates
            )

    def testGetMonthDatesWeekStartsWithSunday(self) -> None:
        for (
            year,
            month,
            expectedMonthDates,
        ) in self.__getGetMonthDatesWeekStartsWithSundayData():
            self.__testGetMonthDates(
                False, calendar.SUNDAY, year, month, expectedMonthDates
            )

    def testCalculateWeekNumberIso8601WeekStartsWithMonday(self) -> None:
        for (
            date,
            expectedWeekNumber,
        ) in self.__getCalculateWeekNumberIso8601WeekStartsWithMondayData():
            self.__testCalculateWeekNumber(
                True, calendar.MONDAY, date, expectedWeekNumber
            )

    def testCalculateWeekNumberIso8601WeekStartsWithSunday(self) -> None:
        for (
            date,
            expectedWeekNumber,
        ) in self.__getCalculateWeekNumberIso8601WeekStartsWithMondayData():
            self.__testCalculateWeekNumber(
                True, calendar.SUNDAY, date, expectedWeekNumber
            )

    def testCalculateWeekNumberWeekStartsWithMonday(self) -> None:
        for (
            date,
            expectedWeekNumber,
        ) in self.__getCalculateWeekNumberWeekStartsWithMondayData():
            self.__testCalculateWeekNumber(
                False, calendar.MONDAY, date, expectedWeekNumber
            )

    def testCalculateWeekNumberWeekStartsWithSunday(self) -> None:
        for (
            date,
            expectedWeekNumber,
        ) in self.__getCalculateWeekNumberWeekStartsWithSundayData():
            self.__testCalculateWeekNumber(
                False, calendar.SUNDAY, date, expectedWeekNumber
            )

    def __testGetMonthDates(
        self,
        iso8601: bool,
        firstWeekDay: int,
        year: int,
        month: int,
        expectedMonthDates: list,
    ) -> None:
        util = CalendarUtil(iso8601, firstWeekDay)
        monthDates = util.getMonthDates(year, month)

        self.assertEqual(len(monthDates), len(expectedMonthDates))

        i = 0

        for weekDates in monthDates:
            actualWeekNumber = weekDates[0]
            expectedWeekNumber = expectedMonthDates[i][0]
            actualDatesInWeek = weekDates[1]
            expectedDatesInWeek = expectedMonthDates[i][1]

            self.assertEqual(actualWeekNumber, expectedWeekNumber)
            self.assertEqual(len(actualDatesInWeek), len(expectedDatesInWeek))

            j = 0

            for weekDate in actualDatesInWeek:
                expectedDate = expectedDatesInWeek[j]

                self.assertEqual(weekDate.year, expectedDate[0])
                self.assertEqual(weekDate.month, expectedDate[1])
                self.assertEqual(weekDate.day, expectedDate[2])

                j += 1

            i += 1

    def __testCalculateWeekNumber(
        self,
        iso8601: bool,
        firstWeekDay: int,
        date: datetime.date,
        expectedWeekNumber: int,
    ) -> None:
        util = CalendarUtil(iso8601, firstWeekDay)
        self.assertEqual(util.calculateWeekNumber(date), expectedWeekNumber)

    def __getGetMonthDatesIso8601WeekStartsWithMondayData(self) -> Iterable:
        week2022_52 = self.__generateWeek(
            2022, 12, range(26, 32)
        ) + self.__generateWeek(2023, 1, [1])
        week2023_1 = self.__generateWeek(2023, 1, range(2, 9))
        week2023_2 = self.__generateWeek(2023, 1, range(9, 16))
        week2023_3 = self.__generateWeek(2023, 1, range(16, 23))
        week2023_4 = self.__generateWeek(2023, 1, range(23, 30))
        week2023_5 = self.__generateWeek(2023, 1, range(30, 32)) + self.__generateWeek(
            2023, 2, range(1, 6)
        )

        yield 2023, 1, [
            (52, week2022_52),
            (1, week2023_1),
            (2, week2023_2),
            (3, week2023_3),
            (4, week2023_4),
            (5, week2023_5),
        ]

        week2023_48 = self.__generateWeek(
            2023, 11, range(27, 31)
        ) + self.__generateWeek(2023, 12, range(1, 4))
        week2023_49 = self.__generateWeek(2023, 12, range(4, 11))
        week2023_50 = self.__generateWeek(2023, 12, range(11, 18))
        week2023_51 = self.__generateWeek(2023, 12, range(18, 25))
        week2023_52 = self.__generateWeek(2023, 12, range(25, 32))

        yield 2023, 12, [
            (48, week2023_48),
            (49, week2023_49),
            (50, week2023_50),
            (51, week2023_51),
            (52, week2023_52),
        ]

        week2024_1 = self.__generateWeek(2024, 1, range(1, 8))
        week2024_2 = self.__generateWeek(2024, 1, range(8, 15))
        week2024_3 = self.__generateWeek(2024, 1, range(15, 22))
        week2024_4 = self.__generateWeek(2024, 1, range(22, 29))
        week2024_5 = self.__generateWeek(2024, 1, range(29, 32)) + self.__generateWeek(
            2024, 2, range(1, 5)
        )

        yield 2024, 1, [
            (1, week2024_1),
            (2, week2024_2),
            (3, week2024_3),
            (4, week2024_4),
            (5, week2024_5),
        ]

    def __getGetMonthDatesWeekStartsWithMondayData(self) -> Iterable:
        week2023_1 = self.__generateWeek(2022, 12, range(26, 32)) + self.__generateWeek(
            2023, 1, [1]
        )
        week2023_2 = self.__generateWeek(2023, 1, range(2, 9))
        week2023_3 = self.__generateWeek(2023, 1, range(9, 16))
        week2023_4 = self.__generateWeek(2023, 1, range(16, 23))
        week2023_5 = self.__generateWeek(2023, 1, range(23, 30))
        week2023_6 = self.__generateWeek(2023, 1, range(30, 32)) + self.__generateWeek(
            2023, 2, range(1, 6)
        )

        yield 2023, 1, [
            (1, week2023_1),
            (2, week2023_2),
            (3, week2023_3),
            (4, week2023_4),
            (5, week2023_5),
            (6, week2023_6),
        ]

        week2023_49 = self.__generateWeek(
            2023, 11, range(27, 31)
        ) + self.__generateWeek(2023, 12, range(1, 4))
        week2023_50 = self.__generateWeek(2023, 12, range(4, 11))
        week2023_51 = self.__generateWeek(2023, 12, range(11, 18))
        week2023_52 = self.__generateWeek(2023, 12, range(18, 25))
        week2023_53 = self.__generateWeek(2023, 12, range(25, 32))

        yield 2023, 12, [
            (49, week2023_49),
            (50, week2023_50),
            (51, week2023_51),
            (52, week2023_52),
            (53, week2023_53),
        ]

        week2024_1 = self.__generateWeek(2024, 1, range(1, 8))
        week2024_2 = self.__generateWeek(2024, 1, range(8, 15))
        week2024_3 = self.__generateWeek(2024, 1, range(15, 22))
        week2024_4 = self.__generateWeek(2024, 1, range(22, 29))
        week2024_5 = self.__generateWeek(2024, 1, range(29, 32)) + self.__generateWeek(
            2024, 2, range(1, 5)
        )

        yield 2024, 1, [
            (1, week2024_1),
            (2, week2024_2),
            (3, week2024_3),
            (4, week2024_4),
            (5, week2024_5),
        ]

    def __getGetMonthDatesWeekStartsWithSundayData(self) -> Iterable:
        week2022_1 = self.__generateWeek(2021, 12, range(26, 32)) + self.__generateWeek(
            2022, 1, [1]
        )
        week2022_2 = self.__generateWeek(2022, 1, range(2, 9))
        week2022_3 = self.__generateWeek(2022, 1, range(9, 16))
        week2022_4 = self.__generateWeek(2022, 1, range(16, 23))
        week2022_5 = self.__generateWeek(2022, 1, range(23, 30))
        week2022_6 = self.__generateWeek(2022, 1, range(30, 32)) + self.__generateWeek(
            2022, 2, range(1, 6)
        )

        yield 2022, 1, [
            (1, week2022_1),
            (2, week2022_2),
            (3, week2022_3),
            (4, week2022_4),
            (5, week2022_5),
            (6, week2022_6),
        ]

        week2022_49 = self.__generateWeek(
            2022, 11, range(27, 31)
        ) + self.__generateWeek(2022, 12, range(1, 4))
        week2022_50 = self.__generateWeek(2022, 12, range(4, 11))
        week2022_51 = self.__generateWeek(2022, 12, range(11, 18))
        week2022_52 = self.__generateWeek(2022, 12, range(18, 25))
        week2022_53 = self.__generateWeek(2022, 12, range(25, 32))

        yield 2022, 12, [
            (49, week2022_49),
            (50, week2022_50),
            (51, week2022_51),
            (52, week2022_52),
            (53, week2022_53),
        ]

        week2024_1 = self.__generateWeek(2023, 12, [31]) + self.__generateWeek(
            2024, 1, range(1, 7)
        )
        week2024_2 = self.__generateWeek(2024, 1, range(7, 14))
        week2024_3 = self.__generateWeek(2024, 1, range(14, 21))
        week2024_4 = self.__generateWeek(2024, 1, range(21, 28))
        week2024_5 = self.__generateWeek(2024, 1, range(28, 32)) + self.__generateWeek(
            2024, 2, range(1, 4)
        )

        yield 2024, 1, [
            (1, week2024_1),
            (2, week2024_2),
            (3, week2024_3),
            (4, week2024_4),
            (5, week2024_5),
        ]

    def __getCalculateWeekNumberIso8601WeekStartsWithMondayData(
        self,
    ) -> tuple[datetime.date, int]:
        yield datetime.date(2022, 1, 2), 52
        yield datetime.date(2022, 12, 26), 52
        yield datetime.date(2023, 1, 1), 52
        yield datetime.date(2023, 1, 2), 1
        yield datetime.date(2023, 12, 25), 52
        yield datetime.date(2023, 12, 31), 52
        yield datetime.date(2024, 1, 1), 1
        yield datetime.date(2024, 1, 8), 2

    def __getCalculateWeekNumberWeekStartsWithMondayData(
        self,
    ) -> tuple[datetime.date, int]:
        yield datetime.date(2022, 1, 2), 1
        yield datetime.date(2022, 12, 25), 52
        yield datetime.date(2022, 12, 26), 53
        yield datetime.date(2023, 1, 1), 1
        yield datetime.date(2023, 1, 2), 2
        yield datetime.date(2023, 12, 25), 53
        yield datetime.date(2023, 12, 31), 53
        yield datetime.date(2024, 1, 1), 1
        yield datetime.date(2024, 1, 8), 2

    def __getCalculateWeekNumberWeekStartsWithSundayData(
        self,
    ) -> tuple[datetime.date, int]:
        yield datetime.date(2022, 1, 2), 2
        yield datetime.date(2022, 12, 26), 53
        yield datetime.date(2023, 1, 1), 1
        yield datetime.date(2023, 1, 2), 1
        yield datetime.date(2023, 12, 25), 52
        yield datetime.date(2023, 12, 31), 53
        yield datetime.date(2024, 1, 1), 1
        yield datetime.date(2024, 1, 8), 2

    def __generateWeek(
        self, year: int, month: int, days: Iterable[int]
    ) -> tuple[tuple[int, int, int]]:
        return self.__mergeListsIntoTuple([year] * len(days), [month] * len(days), days)

    def __mergeListsIntoTuple(self, *list: Iterable) -> tuple:
        return tuple(zip(*list))
