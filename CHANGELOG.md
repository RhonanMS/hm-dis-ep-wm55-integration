# Changelog

All notable changes to this project are documented in this file.

## Unreleased

### Documentation

- Corrected the "clearing an icon" guidance introduced in v1.0.5: that
  entry recommended explicitly passing `icon: aus` (`0x80`) to reliably
  remove an icon from a line. This is now believed to be wrong — `aus` is
  most likely a distinct "unlit bulb" icon graphic (the counterpart to
  `ein`'s lit bulb), not a "no icon" value, and was never hardware-verified
  for its visual appearance. The documented way to clear an icon is now to
  simply omit the `iconX` field — `build_line_block()` already only sends
  the icon sub-block when an icon is given. Flagged as **not yet
  hardware-verified** pending a real-device test; see the open "Test E"
  note in [HM-Dis-EP-WM55.md](HM-Dis-EP-WM55.md#icon-codes). No code
  change — `protocol.py` already behaved this way.

## [1.0.5] - 2026-10-06

### Added

- `README.md`/`INSTALLATION.md`: documented installing via HACS as a
  custom repository (`RhonanMS/hm-dis-ep-wm55-integration`, category
  Integration) — already possible ahead of an official HACS default
  listing.

### Documentation

- Fixed the OFFEN icon example to show it on line 3, not line 2.
- Documented sending an explicit `icon: aus` for reliable icon clearing on
  state change.
- Noted in `CHANGELOG.md` that v1.0.0–v1.0.2 were deleted/unpublished.

## [1.0.4] - 2026-10-06

### Fixed

- `protocol.py`: a line block is now always sent with at least a space
  character as text. Hardware testing showed the display silently ignores
  any line block without text bytes (both a fully empty `0x0A` block and an
  icon-only block) and keeps showing the line's previous content — so
  blanking a line or showing an icon without visible text now requires a
  space filler. See the "Line Block" and "Verified Tests" sections in
  [HM-Dis-EP-WM55.md](HM-Dis-EP-WM55.md) (Test C/D) for details.

## [1.0.3] - 2026-10-06

### Fixed

- Reordered `manifest.json` keys as required by hassfest: `domain`, `name`,
  then the rest alphabetically.

## 1.0.2 - 2026-10-06

> **Note:** this release/tag was deleted after v1.0.3 was published and is
> no longer available on GitHub — superseded within minutes by the fix
> below. Kept here only for a complete history.

### Fixed

- Removed the `homeassistant` key from `manifest.json` — it's not a valid
  manifest field (hassfest rejected it); the minimum Home Assistant version
  is already declared correctly in `hacs.json`.

## 1.0.1 - 2026-10-06

> **Note:** this release/tag was deleted after v1.0.3 was published and is
> no longer available on GitHub — superseded within minutes by v1.0.2/v1.0.3.
> Kept here only for a complete history.

### Added

- HACS publishing readiness: `hacs.json`, brand icon
  (`custom_components/hm_dis_ep_wm55/brand/icon.png`), GitHub Actions for
  HACS validation and `hassfest`, repository topics.
- `manifest.json`: `homeassistant` minimum version and `integration_type`.

## 1.0.0 - 2026-10-06

> **Note:** this release/tag was deleted after v1.0.3 was published and is
> no longer available on GitHub — superseded by v1.0.1. Kept here only for
> a complete history.

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

[1.0.5]: https://github.com/RhonanMS/hm-dis-ep-wm55-integration/releases/tag/v1.0.5
[1.0.4]: https://github.com/RhonanMS/hm-dis-ep-wm55-integration/releases/tag/v1.0.4
[1.0.3]: https://github.com/RhonanMS/hm-dis-ep-wm55-integration/releases/tag/v1.0.3
