# Changelog

All notable changes to this project are documented in this file.

## [1.0.1] - 2026-10-06

### Added

- HACS publishing readiness: `hacs.json`, brand icon
  (`custom_components/hm_dis_ep_wm55/brand/icon.png`), GitHub Actions for
  HACS validation and `hassfest`, repository topics.
- `manifest.json`: `homeassistant` minimum version and `integration_type`.

## [1.0.0] - 2026-10-06

### Added

- Initial release of the `hm_dis_ep_wm55` custom integration.
- Hardware-verified SUBMIT protocol encoder (`protocol.py`) for the
  HM-Dis-EP-WM55 display, built on top of
  [Homematic(IP) Local for OpenCCU](https://github.com/SukramJ/homematicip_local).
- Config Flow for selecting the display device and channel.
- Service `hm_dis_ep_wm55.send_message` with fields for per-line text/icon,
  sound, repeat count, repeat distance, and LED signal.
- Translations: `en`, `de`, `fr`, `it`, `nl`, `es`.
- Window-status automation walkthrough (`docs/automations.md`) showing a
  display with button-triggered re-alert.
- Full protocol documentation (`HM-Dis-EP-WM55.md`), installation guide
  (`INSTALLATION.md`), and additional docs under `docs/`.

[1.0.1]: https://github.com/RhonanMS/hm-dis-ep-wm55-integration/releases/tag/v1.0.1
[1.0.0]: https://github.com/RhonanMS/hm-dis-ep-wm55-integration/releases/tag/v1.0.0
