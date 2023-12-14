import uuid

from dateutil import rrule

from comnuoc.calendar.domain.event.event import EventId
from comnuoc.calendar.domain.event.event_serializer import *


class EventIdUuidNormalizer(EventIdNormalizer):
    def normalize(self, id: EventId) -> str:
        id = id.getId()

        if not isinstance(id, uuid.UUID):
            raise TypeError("The value of event ID should be an instance of uuid.UUID")

        return str(id.int)

    def denormalize(self, id: str) -> EventId:
        id = uuid.UUID(int=int(id))

        return EventId(id)


class EventIntervalRruleNormalizer(EventIntervalNormalizer):
    def normalize(self, interval: Union[EventInterval, None]) -> str:
        if interval is None:
            return ""

        interval = interval.getInterval()

        if not isinstance(interval, rrule.rrule):
            raise TypeError(
                "The value of event interval should be an instance of dateutil.rrule.rrule"
            )

        return str(interval)

    def denormalize(self, interval: str) -> Union[EventInterval, None]:
        if "" == interval:
            return None

        return EventInterval(rrule.rrulestr(interval))
