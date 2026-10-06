"""Encoder für das HM-Dis-EP-WM55 SUBMIT-Protokoll.

Reine, von Home Assistant unabhängige Logik - siehe HM-Dis-EP-WM55.md für die
Protokollbeschreibung. Die Funktionen bauen den Komma-separierten Hex-String
zusammen, der als ``value`` an den Service
``homematicip_local.set_device_value`` (Parameter ``SUBMIT``) übergeben wird.
"""
from __future__ import annotations

import logging
import math

from .const import (
    CHAR_MAP,
    FALLBACK_CHAR_CODE,
    ICON_CODES,
    LED_CODES,
    MAX_DISTANCE,
    MAX_LINE_LENGTH,
    MAX_REPEAT,
    MIN_DISTANCE,
    MIN_REPEAT,
    SOUND_CODES,
)

_LOGGER = logging.getLogger(__name__)

START_CODE = "0x02"
END_CODE = "0x03"
LINE_TEXT_PREFIX = "0x12"
LINE_ICON_PREFIX = "0x13"
LINE_BLOCK_END = "0x0A"
SOUND_PREFIX = "0x14"
REPEAT_PREFIX = "0x1C"
DISTANCE_PREFIX = "0x1D"
SIGNAL_PREFIX = "0x16"


def _byte(value: int) -> str:
    return f"0x{value:02X}"


def encode_text(text: str | None) -> list[str]:
    """Wandelt Text in eine Liste von Hex-Tokens gemäß Zeichensatz-Tabelle um."""
    if not text:
        return []

    if len(text) > MAX_LINE_LENGTH:
        _LOGGER.warning(
            "Text %r ist länger als %d Zeichen und wird gekürzt",
            text,
            MAX_LINE_LENGTH,
        )
        text = text[:MAX_LINE_LENGTH]

    tokens: list[str] = []
    for char in text:
        code = CHAR_MAP.get(char)
        if code is None:
            _LOGGER.warning(
                "Zeichen %r wird vom Display nicht unterstützt und durch '?' ersetzt",
                char,
            )
            code = FALLBACK_CHAR_CODE
        tokens.append(_byte(code))
    return tokens


def _resolve_code(mapping: dict[str, int], name: str | None, kind: str) -> int | None:
    if not name:
        return None
    code = mapping.get(name)
    if code is None:
        raise ValueError(f"Unbekannter {kind}-Wert: {name!r}")
    return code


def build_line_block(text: str | None, icon: str | None) -> list[str]:
    """Baut den Protokoll-Block für eine Zeile (Text + optionales Icon)."""
    icon_code = _resolve_code(ICON_CODES, icon, "Icon")
    tokens: list[str] = []
    if text or icon_code is not None:
        tokens.append(LINE_TEXT_PREFIX)
        tokens.extend(encode_text(text))
        if icon_code is not None:
            tokens.append(LINE_ICON_PREFIX)
            tokens.append(_byte(icon_code))
    tokens.append(LINE_BLOCK_END)
    return tokens


def repeat_to_code(repeat: int) -> str:
    """Wandelt die Anzahl Wiederholungen in den Protokoll-Code um (0=unendlich)."""
    if repeat < MIN_REPEAT or repeat > MAX_REPEAT:
        _LOGGER.warning(
            "repeat=%s außerhalb des gültigen Bereichs (%d-%d), wird begrenzt",
            repeat,
            MIN_REPEAT,
            MAX_REPEAT,
        )
        repeat = max(MIN_REPEAT, min(MAX_REPEAT, repeat))

    if repeat == 0:
        return "0xDF"
    return _byte(0xD0 + (repeat - 1))


def distance_to_code(distance: int) -> str:
    """Wandelt den Abstand (Sekunden) in den Protokoll-Code um, aufgerundet auf 10s-Schritte."""
    if distance < MIN_DISTANCE or distance > MAX_DISTANCE:
        _LOGGER.warning(
            "distance=%s außerhalb des gültigen Bereichs (%d-%d), wird begrenzt",
            distance,
            MIN_DISTANCE,
            MAX_DISTANCE,
        )
        distance = max(MIN_DISTANCE, min(MAX_DISTANCE, distance))

    level = math.ceil(distance / 10)
    level = max(1, min(16, level))
    return _byte(0xE0 + (level - 1))


def build_submit_string(
    line2: str | None = None,
    icon2: str | None = None,
    line3: str | None = None,
    icon3: str | None = None,
    line4: str | None = None,
    icon4: str | None = None,
    sound: str | None = None,
    repeat: int = 1,
    distance: int = 10,
    led: str | None = None,
) -> str:
    """Baut den vollständigen SUBMIT-Komma-Hex-String."""
    sound_code = _resolve_code(SOUND_CODES, sound, "Sound") or SOUND_CODES["aus"]
    led_code = _resolve_code(LED_CODES, led, "LED") or LED_CODES["aus"]

    tokens: list[str] = [START_CODE, LINE_BLOCK_END]
    tokens.extend(build_line_block(line2, icon2))
    tokens.extend(build_line_block(line3, icon3))
    tokens.extend(build_line_block(line4, icon4))

    tokens.append(SOUND_PREFIX)
    tokens.append(_byte(sound_code))
    tokens.append(REPEAT_PREFIX)
    tokens.append(repeat_to_code(repeat))
    tokens.append(DISTANCE_PREFIX)
    tokens.append(distance_to_code(distance))
    tokens.append(SIGNAL_PREFIX)
    tokens.append(_byte(led_code))
    tokens.append(END_CODE)

    return ",".join(tokens)
