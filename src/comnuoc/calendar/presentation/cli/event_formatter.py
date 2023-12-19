from comnuoc.calendar.application.event.event_dto import EventDto


class EventFormatter(object):
    def formatEvent(self, eventDto: EventDto, leftColWidth=26) -> str:
        dateValue = (
            f"{eventDto.dateYear}-{eventDto.dateMonth:02d}-{eventDto.dateDay:02d}"
        )
        startTimeValue = f"{eventDto.startDateHour:02d}:{eventDto.startDateMinute:02d}"
        endTimeValue = f"{eventDto.endDateHour:02d}:{eventDto.endDateMinute:02d}"

        if eventDto.isRecurrent:
            isRecurrent = "Yes"
        else:
            isRecurrent = "No"

        values = {
            "Id": eventDto.id,
            "Title": eventDto.title,
            "Date (YYYY-MM-DD)": dateValue,
            "Start Time (HH:MM)": startTimeValue,
            "End Time (HH:MM)": endTimeValue,
            "Is Recurrent": isRecurrent,
        }

        if eventDto.isRecurrent:
            values["Recurrence Interval"] = eventDto.recurrenceIntervalHumanText

        lines = []

        for label, value in values.items():
            lines.append(label.ljust(leftColWidth, " ") + value)

        return "\n".join(lines)
