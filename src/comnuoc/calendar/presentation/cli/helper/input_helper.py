from collections.abc import Callable
from colorama import Fore, Back, Style
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
            errorMessage="Year should be between 1 and 999",
        )

    def inputMonth(self, default: int = None, message: str = "Month") -> int:
        return self.inputInt(
            message,
            default,
            lambda value: value > 0 and value < 13,
            errorMessage="Month should be between 1 and 12",
        )

    def inputDay(self, default: int = None, message: str = "Day") -> int:
        return self.inputInt(
            message,
            default,
            lambda value: value > 0 and value < 32,
            errorMessage="Day should be between 1 and 31",
        )

    def inputHour(self, default: int = None, message: str = "Hour (24h)") -> int:
        return self.inputInt(
            message,
            default,
            lambda value: value >= 0 and value < 24,
            errorMessage="Hour should be between 0 and 23",
        )

    def inputMinute(self, default: int = None, message: str = "Minute") -> int:
        return self.inputInt(
            message,
            default,
            lambda value: value >= 0 and value < 60,
            errorMessage="Minute should be between 0 and 59",
        )

    def inputWeek(self, default: int = None, message: str = "Week") -> int:
        return self.inputInt(
            message,
            default,
            lambda value: value > 0 and value < 54,
            errorMessage="Week should be between 1 and 53",
        )

    def inputNotBlankStr(self, message: str, default: str = None) -> str:
        return self.inputStr(
            message,
            default,
            lambda value: len(value) > 0,
            errorMessage="Value should not be blank",
        )

    def inputInt(
        self,
        message: str,
        default: int = None,
        validator: Callable[[int], bool] = None,
        defaultInMessage: bool = True,
        errorMessage: str = None,
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

                if validator is None:
                    break
                else:
                    if validator(value):
                        break
                    elif errorMessage is not None:
                        self.printErrorMessage(errorMessage)
            except ValueError:
                if errorMessage is not None:
                    self.printErrorMessage(errorMessage)

        return value

    def inputStr(
        self,
        message: str,
        default: str = None,
        validator: Callable[[str], bool] = None,
        defaultInMessage: bool = True,
        errorMessage: str = None,
    ) -> str:
        if defaultInMessage:
            message = self.messageWithDefault(message, default)

        while True:
            value = input(message)

            if default is not None and "" == value:
                value = default

            if validator is None:
                break
            else:
                if validator(value):
                    break
                elif errorMessage is not None:
                    self.printErrorMessage(errorMessage)

        return value

    def inputBool(
        self,
        message: str,
        default: bool = None,
        defaultInMessage: bool = True,
    ) -> bool:
        message = message + " (y: yes, n: no)"
        boolValues = {"y": True, "n": False}

        if default:
            defaultStr = "y"
        else:
            defaultStr = "n"

        if defaultInMessage and default is not None:
            message = self.messageWithDefault(message, defaultStr)

        while True:
            value = input(message)

            if default is not None and "" == value:
                value = defaultStr

            if value in boolValues:
                break

        return boolValues[value]

    def inputMultipleInt(
        self,
        message: str,
        default: list[int] = None,
        singleValueValidator: Callable[[int], bool] = None,
        valuesValidator: Callable[[list[int]], bool] = None,
        defaultInMessage: bool = True,
        defaultMessage: str = "Default",
        singleValueErrorMessage: str = "There is an error",
        valuesErrorMessage: str = "Error occurs. The values are reset. Please enter again.",
        breakHint: Union[str, None] = "enter blank when you have done",
        allowClear: bool = True,
        useDefaultMessage: str = "Do you want to use default values?",
    ) -> list[int]:
        if defaultInMessage and default is not None:
            defaultStr = ", ".join([str(val) for val in default])
            print(f"{defaultMessage}: {defaultStr}")

        values = []
        message = self.messageWithDefault(message, breakHint)

        while True:
            while True:
                try:
                    value = input(message)

                    if "" == value:
                        break

                    value = int(value)

                    if singleValueValidator is None:
                        values.append(value)
                    else:
                        if singleValueValidator(value):
                            values.append(value)
                        else:
                            self.printErrorMessage(singleValueErrorMessage)
                except ValueError:
                    self.printErrorMessage(singleValueErrorMessage)

            if 0 == len(values) and default is not None:
                if not allowClear:
                    values = default
                else:
                    useDefault = self.inputBool(useDefaultMessage, True)

                    if useDefault:
                        values = default

            if (valuesValidator is not None) and (not valuesValidator(values)):
                self.printErrorMessage(valuesErrorMessage)
                values = []
            else:
                break

        return values

    def inputMultipleStr(
        self,
        message: str,
        default: list[str] = None,
        singleValueValidator: Callable[[str], bool] = None,
        valuesValidator: Callable[[list[str]], bool] = None,
        defaultInMessage: bool = True,
        defaultMessage: str = "Default",
        singleValueErrorMessage: str = "There is an error",
        valuesErrorMessage: str = "Error occurs. The values are reset. Please enter again.",
        breakHint: Union[str, None] = "enter blank when you have done",
        allowClear: bool = True,
        useDefaultMessage: str = "Do you want to use default values?",
    ) -> list[str]:
        if defaultInMessage and default is not None:
            defaultStr = ", ".join(default)
            print(f"{defaultMessage}: {defaultStr}")

        values = []
        message = self.messageWithDefault(message, breakHint)

        while True:
            while True:
                value = input(message)

                if "" == value:
                    break

                if singleValueValidator is None:
                    values.append(value)
                else:
                    if singleValueValidator(value):
                        values.append(value)
                    else:
                        self.printErrorMessage(singleValueErrorMessage)

            if 0 == len(values) and default is not None:
                if not allowClear:
                    values = default
                else:
                    useDefault = self.inputBool(useDefaultMessage, True)

                    if useDefault:
                        values = default

            if (valuesValidator is not None) and (not valuesValidator(values)):
                self.printErrorMessage(valuesErrorMessage)
                values = []
            else:
                break

        return values

    def messageWithDefault(
        self, message: str, default: Union[int, str, None] = None
    ) -> str:
        if default is not None:
            message = f"{message} ({default}): "
        else:
            message = f"{message}: "

        return message

    def printErrorMessage(self, message: str) -> None:
        self.printMessageWithColor(message, Back.RED, Fore.WHITE)

    def printSuccessMessage(self, message: str) -> None:
        self.printMessageWithColor(message, Back.GREEN, Fore.WHITE)

    def printInfoMessage(self, message: str) -> None:
        self.printMessageWithColor(message, Back.CYAN, Fore.WHITE)

    def printWarningMessage(self, message: str) -> None:
        self.printMessageWithColor(message, Back.YELLOW, Fore.BLACK)

    def printMessageWithColor(self, message: str, bgColor: int, fgColor: int) -> None:
        recLen = len(message) + 2
        print(bgColor + fgColor + " " * recLen)
        print(" " + message + " ")
        print(" " * recLen + Style.RESET_ALL)
        print()
