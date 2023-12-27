import datetime
from typing import Union

from dateutil import relativedelta

from comnuoc.calendar.application.event.event_dto import EventDto, EventDtoTransformer

from comnuoc.calendar.domain.event.event import *
from comnuoc.calendar.domain.event.event_serializer import *
from comnuoc.calendar.domain.util.datetime_range import DateTimeRange

from comnuoc.calendar.infrastructure.event.event_repository import *
from comnuoc.calendar.infrastructure.event.event_serializer import *
from comnuoc.calendar.infrastructure.util.setting_repository import (
    FileSettingRepository,
)


class EventService(object):
    def __init__(
        self,
        settings: FileSettingRepository,
        idNormalizer: EventIdNormalizer,
        repository: EventRepository,
        dtoTransformer: EventDtoTransformer,
    ) -> None:
        self._settings = settings
        self._idNormalizer = idNormalizer
        self._repository = repository
        self._dtoTransformer = dtoTransformer

    def getEvent(self, id: str) -> Union[EventDto, None]:
        event = self.__getEventById(id, False)

        if event is None:
            return None

        return self._dtoTransformer.createDtoFromEvent(event)

    def getEventsByDate(self, year: int, month: int, day: int) -> list[EventDto]:
        tzInfo = self._settings.getTzInfo()
        startDate = datetime.datetime(year=year, month=month, day=day, tzinfo=tzInfo)
        endDate = startDate + relativedelta.relativedelta(days=+1)
        range = DateTimeRange(startDate, endDate, True, False)

        events = self._repository.findByStartDate(range)
        eventDtos = []

        try:
            for event in events:
                eventDtos.append(self._dtoTransformer.createDtoFromEvent(event))
        finally:
            events.close()  # as https://peps.python.org/pep-0533/

        return eventDtos

    def insertEvent(self, dto: EventDto) -> EventDto:
        id = self._repository.generateId()
        event = self._dtoTransformer.createEventFromDto(dto, id)

        self._repository.insert(event)

        return self._dtoTransformer.createDtoFromEvent(event)

    def updateEvent(self, dto: EventDto) -> EventDto:
        if dto.id is None or "" == dto.id:
            raise KeyError(f"Event ID is required")

        event = self.__getEventById(dto.id, True)

        newEvent = self._dtoTransformer.createEventFromDto(dto, event.getId())

        self._repository.update(newEvent)

        return self._dtoTransformer.createDtoFromEvent(newEvent)

    def deleteEvent(self, id: str) -> EventDto:
        event = self.__getEventById(id, True)

        self._repository.delete(event)

        return self._dtoTransformer.createDtoFromEvent(event)

    def __getEventById(
        self, id: str, throwExceptionIfNotFound: bool = False
    ) -> Union[Event, None]:
        eventId = self._idNormalizer.denormalize(id)
        event = self._repository.find(eventId)

        if event is None and throwExceptionIfNotFound:
            raise KeyError(f'Event with ID "{id}" is not found')

        return event
