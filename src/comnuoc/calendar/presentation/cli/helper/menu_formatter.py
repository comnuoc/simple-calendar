class MenuFormatter(object):
    def formatTitle(self, title: str, width: int = 69, borderChar: str = "*") -> str:
        width = max(len(title) + 4, width)
        content = []
        content.append(borderChar * width)
        content.append(borderChar + title.upper().center(width - 2) + borderChar)
        content.append(borderChar * width)

        return "\n".join(content)

    def formatContent(
        self,
        content: str,
        prependLine: bool = False,
        width: int = 69,
        borderChar: str = "*",
    ) -> str:
        return self.formatOptions(content.splitlines(), prependLine, width, borderChar)

    def formatOptions(
        self,
        options: list[str],
        prependLine: bool = False,
        width: int = 69,
        borderChar: str = "*",
    ) -> str:
        maxLenOption = max(options, key=len)
        width = max(len(maxLenOption) + 4, width)
        line = borderChar * width
        menuContent = []

        if prependLine:
            menuContent.append(line)

        options = [
            borderChar + " " + option.ljust(width - 3) + borderChar
            for option in options
        ]
        menuContent += options
        menuContent.append(line)

        return "\n".join(menuContent)
