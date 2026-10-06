"""Config Flow für die HM-Dis-EP-WM55 Integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.helpers import selector
from homeassistant.helpers.device_registry import async_get as async_get_device_registry

from .const import CONF_CHANNEL, CONF_DEVICE_ID, DEFAULT_CHANNEL, DOMAIN, HOMEMATIC_DOMAIN


class HmDisEpWm55ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config Flow: Auswahl des Homematic-Display-Geräts und Kanals."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            device_registry = async_get_device_registry(self.hass)
            device = device_registry.async_get(user_input[CONF_DEVICE_ID])
            if device is None:
                errors["base"] = "device_not_found"
            else:
                await self.async_set_unique_id(
                    f"{user_input[CONF_DEVICE_ID]}_{user_input[CONF_CHANNEL]}"
                )
                self._abort_if_unique_id_configured()
                name = (
                    user_input.get(CONF_NAME)
                    or device.name_by_user
                    or device.name
                    or "HM-Dis-EP-WM55"
                )
                return self.async_create_entry(
                    title=name,
                    data={
                        CONF_DEVICE_ID: user_input[CONF_DEVICE_ID],
                        CONF_CHANNEL: int(user_input[CONF_CHANNEL]),
                    },
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_DEVICE_ID): selector.DeviceSelector(
                    selector.DeviceSelectorConfig(integration=HOMEMATIC_DOMAIN)
                ),
                vol.Required(
                    CONF_CHANNEL, default=DEFAULT_CHANNEL
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1, max=99, mode=selector.NumberSelectorMode.BOX
                    )
                ),
                vol.Optional(CONF_NAME): selector.TextSelector(),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
