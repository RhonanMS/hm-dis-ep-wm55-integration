# Changelog

All notable changes to this project are documented in this file.

## [0.1.0] - 2026-10-06

### Added

- Initial release of the `hm_dis_ep_wm55` custom integration.
- Hardware-verified SUBMIT protocol encoder (`protocol.py`) for the
  HM-Dis-EP-WM55 display, built on top of
  [Homematic(IP) Local for OpenCCU](https://github.com/SukramJ/homematicip_local).
- Config Flow for selecting the display device and channel.
- Service `hm_dis_ep_wm55.send_message` with fields for per-line text/icon,
  sound, repeat count, repeat distance, and LED signal.
- Translations: `en`, `de`, `fr`, `it`, `nl`, `es`.
- Example automation (`examples/automations.yaml`) showing a window-status
  display with button-triggered re-alert.
- Full protocol documentation (`HM-Dis-EP-WM55.md`), installation guide
  (`INSTALLATION.md`), and additional docs under `docs/`.

[0.1.0]: https://github.com/RhonanMS/hm-dis-ep-wm55-integration/releases/tag/v0.1.0
