# Architecture

A short tour of `custom_components/hm_dis_ep_wm55/` for anyone extending or
reviewing the integration.

## Files

| File | Role |
|------|------|
| `protocol.py` | Pure SUBMIT-string encoder. No Home Assistant imports — takes text/icon/sound/repeat/distance/led values and returns the comma-separated hex string. Hardware-verified against two real SUBMIT strings (see `tests/test_protocol.py`). |
| `const.py` | Shared constants: character map (incl. German umlauts), icon/sound/LED code tables, defaults and valid ranges. Also has no Home Assistant imports. |
| `config_flow.py` | UI setup: a `DeviceSelector` filtered to `homematicip_local` devices, plus a channel number (default `3`). Creates one config entry per display. |
| `__init__.py` | On `async_setup_entry`: registers a Home Assistant *device* for the config entry (so the entry is targetable by `device_id` in the service field), and registers the `send_message` service (once, shared across all config entries) which calls `protocol.build_submit_string(...)` and forwards the result to `homematicip_local.set_device_value`. |
| `services.yaml` | Service field schema (no `target:` block — see [troubleshooting.md](troubleshooting.md) for why). |
| `strings.json` / `translations/*.json` | UI text for config flow and service fields, per language. |

## Why `protocol.py`/`const.py` Have No Home Assistant Dependency

This is deliberate: it lets `tests/test_protocol.py` run with just `pytest`
installed, no Home Assistant package required. `tests/conftest.py` loads the
two modules via a manual `sys.modules` stub for the parent package, so
Python's relative imports (`from .const import ...`) resolve without
executing the real `__init__.py` (which *does* import Home Assistant).

## Why No Entities

The integration intentionally exposes **no entities** — just a device (for
targeting) and a service. The display is write-only (SUBMIT has no
corresponding readable state), and the use case is "send a message when an
automation decides to", not "represent display state in the entity
registry". A `notify` entity platform was considered during planning but
rejected: the standard `notify.send_message` action only supports
`message`/`title`, not the per-line text/icon/sound/LED/repeat/distance
structure this device needs.

## Service Routing for Multiple Displays

Each config entry gets its own Home Assistant device
(`identifiers={(DOMAIN, entry.entry_id)}`). The service handler resolves an
incoming `device_id` back to the right config entry's data (target
`homematicip_local` device + channel) via a simple linear scan over
`hass.data[DOMAIN]` — intentionally simple, since the expected number of
displays is small (a handful at most).

## See Also

- [HM-Dis-EP-WM55.md](../HM-Dis-EP-WM55.md) — the wire protocol itself.
- [docs/services.md](services.md) — service field reference.
- [CONTRIBUTING.md](../CONTRIBUTING.md) — running the tests.
