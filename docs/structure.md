# Structure

The source contains a script ([cli.py](../cli.py)) and a package ([src/comnuoc/calendar/](../src/comnuoc/calendar/)).

The script is just a way to run (call) the application ([src/comnuoc/calendar/presentation/cli/application.py](../src/comnuoc/calendar/presentation/cli/application.py)) in the package.

The package tree structure:
```bash
src/comnuoc/calendar
├── application
│   ├── calendar
│   │   └── calendar_service.py
│   ├── event
│   │   ├── event_dto.py
│   │   └── event_service.py
│   ├── setting
│   │   └── setting_service.py
│   └── service_container.py
├── domain
│   ├── event
│   │   ├── event.py
│   │   ├── event_repository.py
│   │   └── event_serializer.py
│   └── util
│       ├── calendar.py
│       ├── datetime_range.py
│       └── setting_repository.py
├── infrastructure
│   ├── event
│   │   ├── event_repository.py
│   │   └── event_serializer.py
│   └── util
│       └── setting_repository.py
└── presentation
    └── cli
        ├── controller
        │   ├── calendar_controller.py
        │   ├── event_controller.py
        │   └── setting_controller.py
        ├── helper
        │   ├── calendar_formatter.py
        │   ├── event_formatter.py
        │   ├── input_helper.py
        │   ├── menu_formatter.py
        │   └── recurrence_event_input_helper.py
        └── application.py

```



## Layers

There are 4 layers with dependencies as below:

```bash

   ┌─────────────────────────────┐
   │                             │
   │        Presentation         │
   │                             │
   └─────────────┬───────────────┘
                 │
                 │
                 │
   ┌─────────────▼───────────────┐
   │                             │
   │        Application          ├─────────────────────────────┐
   │                             │                             │
   └─────────────┬───────────────┘            ┌────────────────▼────────────┐
                 │                            │                             │
                 │                            │             Domain          │
                 │                            │                             │
   ┌─────────────▼───────────────┐            └────────────────▲────────────┘
   │                             │                             │
   │        Infrastucture        ├─────────────────────────────┘
   │                             │
   └─────────────────────────────┘


```
