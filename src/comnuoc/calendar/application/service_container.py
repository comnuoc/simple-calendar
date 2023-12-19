import os

from comnuoc.calendar.application.calendar.calendar_service import CalendarService
from comnuoc.calendar.application.event.event_dto import (
    EventDtoTransformer,
    EventRecurrenceAssembler,
)
from comnuoc.calendar.application.event.event_service import EventService
from comnuoc.calendar.application.setting.setting_service import SettingService

from comnuoc.calendar.domain.event.event_serializer import EventNormalizer
from comnuoc.calendar.domain.util.calendar import CalendarUtil

from comnuoc.calendar.infrastructure.event.event_repository import (
    CsvEventRepository,
    EventIdUuidGenerator,
    EventRecurrenceRruleChecker,
)
from comnuoc.calendar.infrastructure.event.event_serializer import *
from comnuoc.calendar.infrastructure.util.setting_repository import (
    FileSettingRepository,
)


class ServiceContainer(object):
    def __init__(self) -> None:
        # @todo: lazy initialize services
        self._services = {}
        dirName = os.path.dirname(__file__)
        settingsPath = os.path.join(dirName, "data", "settings.ini")

        eventsPath = os.path.join(dirName, "data", "events.csv")

        # write file if not exist
        if not os.path.isfile(eventsPath):
            with open(eventsPath, "w") as fp:
                pass

        settingRepository = FileSettingRepository(settingsPath)
        eventIdNormalizer = EventIdUuidNormalizer()
        eventIntervalNormalizer = EventIntervalRruleNormalizer()
        eventNormalizer = EventNormalizer(
            idNormalizer=eventIdNormalizer, intervalNormalizer=eventIntervalNormalizer
        )
        eventIdGenerator = EventIdUuidGenerator()
        firstWeekDay = settingRepository.getFirstWeekDay()
        eventRecurrenceChecker = EventRecurrenceRruleChecker(firstWeekDay)
        eventRepository = CsvEventRepository(
            idGenerator=eventIdGenerator,
            normalizer=eventNormalizer,
            recurrenceChecker=eventRecurrenceChecker,
            filePath=eventsPath,
        )
        eventDtoTransformer = EventDtoTransformer(
            settings=settingRepository,
            idNormalizer=eventIdNormalizer,
            intervalNormalizer=eventIntervalNormalizer,
            intervalAssembler=EventRecurrenceAssembler(),
        )
        self._services["event"] = EventService(
            settings=settingRepository,
            idNormalizer=eventIdNormalizer,
            repository=eventRepository,
            dtoTransformer=eventDtoTransformer,
        )

        calendarUtil = CalendarUtil(
            iso8601=settingRepository.getIso8601(), firstWeekDay=firstWeekDay
        )
        self._services["calendar"] = CalendarService(
            settings=settingRepository,
            calendarUtil=calendarUtil,
            eventRepository=eventRepository,
        )
        self._services["setting"] = SettingService(settingRepository, calendarUtil)

    def getEventService(self) -> EventService:
        return self._services["event"]

    def getCalendarService(self) -> CalendarService:
        return self._services["calendar"]

    def getSettingService(self) -> SettingService:
        return self._services["setting"]
