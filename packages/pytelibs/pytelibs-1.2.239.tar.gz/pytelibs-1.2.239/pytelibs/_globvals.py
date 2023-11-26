# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from asyncio import Lock
from typing import Set

_GCAST_LOCKED: Set[int] = set()
_GUCAST_LOCKED: Set[int] = set()
_GBAN_LOCKED: Set[int] = set()
_UNGBAN_LOCKED: Set[int] = set()

_INVITED_LOCKED: Set[int] = set()
_KICKED_LOCKED: Set[int] = set()

_HELP_ACCEPT: Set[int] = set()
_HELP_LOCK = Lock()

_MENTION_LOCKED: Set[int] = set()

SETMODE_ONLINE: Set[int] = set()
SETMODE_OFFLINE: Set[int] = set()

_PYTEL_UPDATE = Lock()

LOCK_TYPES: dict = {
    "all": "Everything.",
    "messages": "Text, contacts, locations and venues.",
    "media": "Audio files, documents, photos, videos, video notes and voice notes.",
    "others": "Stickers, games, gifs, inline.",
    "links": "Web priview.",
    "polls": "Polling.",
    "info": "Change info.",
    "invite": "Invite users.",
    "pin": "Pinned messages.",
}

_CHARACTER_NAMES = {
    "`": "",
    "*": "",
    "_": "",
    "-": "",
    "~": "",
    "/": "",
    "|": "",
    "[": "",
    "]": "",
    "<": "",
    ">": "",
    "'": "",
    "{": "",
    "}": "",
    ")": "",
    "(": "",
    "’": "",
    "‘": "",
    "=": "",
    "#": "",
    "&": "",
    "+": "",
    "^": "",
    "%": "",
    "°": "",
    ";": "",
    ":": "",
    "?": "",
    "!": "",
    "@": "",
    "¡": "",
    "¿": "",
    "‽": "",
    "♪": "",
    "±": "",
    '″': '',
    "‚": "",
    ".": "",
    "№": "",
    "—": "",
    "–": "",
    "·": "",
}

SIZE_UNITS = [
    "B",
    "KB",
    "MB",
    "GB",
    "TB",
    "PB",
    "EB",
]

OUT_AFK = [
    "Is Alive !!",
    "Is Here !!",
    "Is Back !!",
    "Is Awake !!",
    "Is Awakening !!",
    "Is Online !!",
    "Is Active !!",
    "Is Finally Here !!",
    "Well Done !!",
    "No Longer AFK !!",
    "Is Coming !!",
    "No Longer Offline !!",
    "Back Again !!",
]

STATISTIC_PYTEL = r"""
📊 Data Usage
Upload: {}
Download: {}

💾 Disk Space
Total: {}
Used: {}
Free: {}

📈 Memory Usage
CPU: {}
RAM: {}
SWAP: {}
"""

STATISTIC_DB = r"""
DATABASE ( PYTEL-Premium )

• Database Type: {}
• Database Size: {}
• Database Table Contents:
  › Table: {}
  › Contents: {}

Copyright (C) 2023-present @kastaid
"""

WEATHER_ICONS: dict = {
    "01d": "☀️",
    "02d": "⛅️",
    "03d": "☁️",
    "04d": "☁️",
    "09d": "🌧",
    "10d": "🌦",
    "11d": "⛈" ,
    "13d": "🌨❄️" ,
    "50d": "🌫",
    "01n": "🌕",
    "02n": "☁🌔",
    "03n": "☁️",
    "04n": "️️☁☁️",
    "09n": "🌧",
    "10n": "🌧🌑",
    "11n": "⛈",
    "13n": "🌨❄️",
    "50n": "🌫",
}
