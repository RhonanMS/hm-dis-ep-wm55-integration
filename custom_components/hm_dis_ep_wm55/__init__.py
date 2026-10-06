"""HM-Dis-EP-WM55 Display Integration.

Baut auf der Integration "Homematic(IP) Local for OpenCCU" (homematicip_local)
auf und stellt einen Service bereit, um Text/Icons/Ton/LED an das Display zu
schicken (SUBMIT-Parameter auf dem konfigurierten Kanal, siehe HM-Dis-EP-WM55.md).
"""
from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_DEVICE_ID
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.device_registry import async_get as async_get_device_registry

from . import protocol
from .const import (
    ATTR_DISTANCE,
    ATTR_ICON2,
    ATTR_ICON3,
    ATTR_ICON4,
    ATTR_LED,
    ATTR_LINE2,
    ATTR_LINE3,
    ATTR_LINE4,
    ATTR_REPEAT,
    ATTR_SOUND,
    CONF_CHANNEL,
    CONF_DEVICE_ID,
    DEFAULT_DISTANCE,
    DEFAULT_LED,
    DEFAULT_REPEAT,
    DEFAULT_SOUND,
    DOMAIN,
    HOMEMATIC_DOMAIN,
    HOMEMATIC_SET_DEVICE_VALUE_SERVICE,
    ICON_CODES,
    LED_CODES,
    MAX_DISTANCE,
    MAX_REPEAT,
    MIN_DISTANCE,
    MIN_REPEAT,
    SERVICE_SEND_MESSAGE,
    SOUND_CODES,
    SUBMIT_PARAMETER,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = []

SEND_MESSAGE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_DEVICE_ID): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(ATTR_LINE2): cv.string,
        vol.Optional(ATTR_ICON2): vol.In(ICON_CODES),
        vol.Optional(ATTR_LINE3): cv.string,
        vol.Optional(ATTR_ICON3): vol.In(ICON_CODES),
        vol.Optional(ATTR_LINE4): cv.string,
        vol.Optional(ATTR_ICON4): vol.In(ICON_CODES),
        vol.Optional(ATTR_SOUND, default=DEFAULT_SOUND): vol.In(SOUND_CODES),
        vol.Optional(ATTR_REPEAT, default=DEFAULT_REPEAT): vol.All(
            vol.Coerce(int), vol.Range(min=MIN_REPEAT, max=MAX_REPEAT)
        ),
        vol.Optional(ATTR_DISTANCE, default=DEFAULT_DISTANCE): vol.All(
            vol.Coerce(int), vol.Range(min=MIN_DISTANCE, max=MAX_DISTANCE)
        ),
        vol.Optional(ATTR_LED, default=DEFAULT_LED): vol.In(LED_CODES),
    }
)


def _find_entry_data(hass: HomeAssistant, ha_device_id: str) -> dict | None:
    for entry_data in hass.data.get(DOMAIN, {}).values():
        if entry_data["ha_device_id"] == ha_device_id:
            return entry_data
    return None


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HM-Dis-EP-WM55 aus einem Config Entry."""
    device_registry = async_get_device_registry(hass)
    device_entry = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.entry_id)},
        name=entry.title,
        manufacturer="eQ-3",
        model="HM-Dis-EP-WM55",
    )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "channel": entry.data[CONF_CHANNEL],
        "target_device_id": entry.data[CONF_DEVICE_ID],
        "ha_device_id": device_entry.id,
    }

    async def _async_handle_send_message(call: ServiceCall) -> None:
        submit_value = protocol.build_submit_string(
            line2=call.data.get(ATTR_LINE2),
            icon2=call.data.get(ATTR_ICON2),
            line3=call.data.get(ATTR_LINE3),
            icon3=call.data.get(ATTR_ICON3),
            line4=call.data.get(ATTR_LINE4),
            icon4=call.data.get(ATTR_ICON4),
            sound=call.data[ATTR_SOUND],
            repeat=call.data[ATTR_REPEAT],
            distance=call.data[ATTR_DISTANCE],
            led=call.data[ATTR_LED],
        )

        for ha_device_id in call.data[ATTR_DEVICE_ID]:
            entry_data = _find_entry_data(hass, ha_device_id)
            if entry_data is None:
                raise HomeAssistantError(
                    f"Kein HM-Dis-EP-WM55 Display für Geräte-ID {ha_device_id} gefunden"
                )

            _LOGGER.debug("Sende SUBMIT an %s: %s", ha_device_id, submit_value)
            await hass.services.async_call(
                HOMEMATIC_DOMAIN,
                HOMEMATIC_SET_DEVICE_VALUE_SERVICE,
                {
                    "device_id": entry_data["target_device_id"],
                    "channel": entry_data["channel"],
                    "parameter": SUBMIT_PARAMETER,
                    "value": submit_value,
                    "value_type": "string",
                },
                blocking=True,
            )

    if not hass.services.has_service(DOMAIN, SERVICE_SEND_MESSAGE):
        hass.services.async_register(
            DOMAIN,
            SERVICE_SEND_MESSAGE,
            _async_handle_send_message,
            schema=SEND_MESSAGE_SCHEMA,
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Config Entry entladen."""
    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    if not hass.data.get(DOMAIN):
        hass.services.async_remove(DOMAIN, SERVICE_SEND_MESSAGE)
    return True
