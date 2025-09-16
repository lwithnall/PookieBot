"""
Discord markdown formatting utilities
Applies specified formatting option to provided text

Details on Discord's formatting can be found here:
https://support.discord.com/hc/en-us/articles/210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline
"""


def hyperlink(text: str, url: str) -> str:
    return f"[{text}]({url})"


def bold(text: str) -> str:
    return f"**{text}**"


def italics(text: str) -> str:
    return f"*{text}*"


def underline(text: str) -> str:
    return f"__{text}__"


def strikethrough(text: str) -> str:
    return f"~~{text}~~"


def subtext(text: str) -> str:
    return f"-# {text}"


def heading(text: str, level: int) -> str:
    # Size of decreases with each # symbol added
    return f"{'#'*level} {text}"


def codebox(text: str, language: str = "") -> str:
    """Print given text in a codebox, formats it as specified language."""
    return f"```{language}\n{text}\n```"
