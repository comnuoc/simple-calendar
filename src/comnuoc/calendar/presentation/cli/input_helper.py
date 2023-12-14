from collections.abc import Callable
import os
from typing import Union


class InputHelper(object):
    def clearScreen(self) -> None:
        # for windows
        if os.name == "nt":
            os.system("cls")
        # for mac and linux(here, os.name is 'posix')
        else:
            os.system("clear")

    def inputYear(self, default: int = None, message: str = "Year") -> int:
        return self.inputInt(
            message,
            default,
            lambda value: value > 0 and value < 10000,
        )

    def inputMonth(self, default: int = None, message: str = "Month") -> int:
        return self.inputInt(
            message,
            default,
            lambda value: value > 0 and value < 13,
        )

    def inputDay(self, default: int = None, message: str = "Day") -> int:
        return self.inputInt(
            message,
            default,
            lambda value: value > 0 and value < 32,
        )

    def inputHour(self, default: int = None, message: str = "Hour") -> int:
        return self.inputInt(
            message,
            default,
            lambda value: value >= 0 and value <= 24,
        )

    def inputMinute(self, default: int = None, message: str = "Minute") -> int:
        return self.inputInt(
            message,
            default,
            lambda value: value >= 0 and value < 60,
        )

    def inputWeek(self, default: int = None, message: str = "Week") -> int:
        return self.inputInt(
            message,
            default,
            lambda value: value > 0 and value < 54,
        )

    def inputNotBlankStr(self, message: str, default: str = None) -> str:
        return self.inputStr(message, default, lambda value: len(value) > 0)

    def inputInt(
        self,
        message: str,
        default: int = None,
        validator: Callable[[int], bool] = None,
        defaultInMessage: bool = True,
    ) -> int:
        if defaultInMessage:
            message = self.messageWithDefault(message, default)

        while True:
            try:
                value = input(message)

                if default is not None and "" == value:
                    value = default
                else:
                    value = int(value)

                if validator is None or validator(value):
                    break
            except ValueError:
                pass

        return value

    def inputStr(
        self,
        message: str,
        default: str = None,
        validator: Callable[[str], bool] = None,
        defaultInMessage: bool = True,
    ) -> str:
        if defaultInMessage:
            message = self.messageWithDefault(message, default)

        while True:
            value = input(message)

            if default is not None and "" == value:
                value = default

            if validator is None or validator(value):
                break

        return value

    def inputBool(
        self,
        message: str,
        default: bool = None,
        defaultInMessage: bool = True,
    ) -> bool:
        message = message + " (y: yes / n: no / 1: yes / 0: no)"
        boolValues = {"y": True, "n": False, "1": True, "0": False}

        if default:
            defaultStr = "y"
        else:
            defaultStr = "n"

        if defaultInMessage:
            message = self.messageWithDefault(message, defaultStr)

        while True:
            value = input(message)

            if default is not None and "" == value:
                value = defaultStr

            if value in boolValues:
                break

        return boolValues[value]

    def messageWithDefault(
        self, message: str, default: Union[int, str, None] = None
    ) -> str:
        if default is not None:
            message = f"{message} ({default}): "
        else:
            message = f"{message}: "

        return message
