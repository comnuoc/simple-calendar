import datetime
from typing import Union


class DateTimeRange(object):
    def __init__(
        self,
        startDate: datetime.datetime = None,
        endDate: datetime.datetime = None,
        includesStartDate: bool = True,
        includesEndDate: bool = True,
    ) -> None:
        self._startDate = startDate
        self._endDate = endDate
        self._includesStartDate = includesStartDate
        self._includesEndDate = includesEndDate

        if not self._isValidRange():
            raise ValueError("End date should be greater than start date")

    def getStartDate(self) -> Union[datetime.datetime, None]:
        return self._startDate

    def getEndDate(self) -> Union[datetime.datetime, None]:
        return self._endDate

    def getRealStartDate(self) -> Union[datetime.datetime, None]:
        if self._startDate is None:
            return None

        if self._includesStartDate:
            return self._startDate

        return self._startDate + datetime.timedelta(microseconds=1)

    def getRealEndDate(self) -> Union[datetime.datetime, None]:
        if self._endDate is None:
            return None

        if self._includesEndDate:
            return self._endDate

        return self._endDate - datetime.timedelta(microseconds=1)

    def isStartDateIncluded(self) -> bool:
        return self._includesStartDate

    def isEndDateIncluded(self) -> bool:
        return self._includesEndDate

    def includes(self, date: datetime.datetime) -> bool:
        if self._startDate is not None:
            startDate = self.getRealStartDate()

            if date < startDate:
                return False

        if self._endDate is not None:
            endDate = self.getRealEndDate()

            if date > endDate:
                return False

        return True

    def _isValidRange(self) -> bool:
        realStartDate = self.getRealStartDate()
        realEndDate = self.getRealEndDate()

        if realStartDate is None or realEndDate is None:
            return True

        return realEndDate >= realStartDate
