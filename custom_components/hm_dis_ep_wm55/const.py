"""Konstanten für die HM-Dis-EP-WM55 Integration."""
from __future__ import annotations

DOMAIN = "hm_dis_ep_wm55"

HOMEMATIC_DOMAIN = "homematicip_local"
HOMEMATIC_SET_DEVICE_VALUE_SERVICE = "set_device_value"
SUBMIT_PARAMETER = "SUBMIT"

DEFAULT_CHANNEL = 3
MAX_LINE_LENGTH = 12

CONF_CHANNEL = "channel"
CONF_DEVICE_ID = "device_id"

SERVICE_SEND_MESSAGE = "send_message"

ATTR_LINE2 = "line2"
ATTR_ICON2 = "icon2"
ATTR_LINE3 = "line3"
ATTR_ICON3 = "icon3"
ATTR_LINE4 = "line4"
ATTR_ICON4 = "icon4"
ATTR_SOUND = "sound"
ATTR_REPEAT = "repeat"
ATTR_DISTANCE = "distance"
ATTR_LED = "led"

# Zeichensatz-Tabelle laut HM-Dis-EP-WM55.md (inkl. deutscher Umlaute).
# Zeichen, die hier nicht vorkommen, werden beim Encodieren durch "?" (0x3F) ersetzt.
CHAR_MAP: dict[str, int] = {
    **{chr(ord("A") + i): 0x41 + i for i in range(26)},
    **{chr(ord("a") + i): 0x61 + i for i in range(26)},
    **{str(d): 0x30 + d for d in range(10)},
    " ": 0x20,
    "!": 0x21,
    '"': 0x22,
    "%": 0x25,
    "&": 0x26,
    "=": 0x27,
    "(": 0x28,
    ")": 0x29,
    "*": 0x2A,
    "+": 0x2B,
    ",": 0x2C,
    "-": 0x2D,
    ".": 0x2E,
    "/": 0x2F,
    ":": 0x3A,
    ";": 0x3B,
    "@": 0x40,
    ">": 0x3E,
    "Ä": 0x5B,
    "Ö": 0x23,
    "Ü": 0x24,
    "ä": 0x7B,
    "ö": 0x7C,
    "ü": 0x7D,
    "ß": 0x5F,
}
FALLBACK_CHAR_CODE = 0x3F  # "?"

ICON_CODES: dict[str, int] = {
    "aus": 0x80,
    "ein": 0x81,
    "offen": 0x82,
    "geschlossen": 0x83,
    "fehler": 0x84,
    "alles_ok": 0x85,
    "information": 0x86,
    "neue_nachricht": 0x87,
    "servicemeldung": 0x88,
}

SOUND_CODES: dict[str, int] = {
    "aus": 0xC0,
    "lang_lang": 0xC1,
    "lang_kurz": 0xC2,
    "lang_kurz_kurz": 0xC3,
    "kurz": 0xC4,
    "kurz_kurz": 0xC5,
    "lang": 0xC6,
}

LED_CODES: dict[str, int] = {
    "aus": 0xF0,
    "rot": 0xF1,
    "gruen": 0xF2,
    "orange": 0xF3,
}

DEFAULT_SOUND = "aus"
DEFAULT_LED = "aus"
DEFAULT_REPEAT = 1
DEFAULT_DISTANCE = 10

MIN_REPEAT = 0
MAX_REPEAT = 15
MIN_DISTANCE = 10
MAX_DISTANCE = 160
