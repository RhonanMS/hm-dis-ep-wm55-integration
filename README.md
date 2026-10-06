# HM-Dis-EP-WM55 for Home Assistant

[![Release][release-shield]][release]
[![License][license-shield]](LICENSE)
[![Home Assistant Custom Integration][ha-shield]][ha]

A custom Home Assistant integration to drive the Homematic **HM-Dis-EP-WM55**
e-paper status display: per-line text and icons, beeper sound, LED signal —
sent via a service you call from your own automations.

## At a Glance

- Builds on [Homematic(IP) Local for OpenCCU][homematicip-local] — this
  integration does not talk to the CCU/device itself, it forwards a
  hardware-verified `SUBMIT` byte string through
  `homematicip_local.set_device_value`.
- One service, `hm_dis_ep_wm55.send_message`: text + icon for each of the
  display's 3 lines, beeper sound, repeat count/distance, LED color.
- No entities, no polling — a small, write-only config-flow integration
  (see [docs/architecture.md](docs/architecture.md) for why).
- The wire protocol was reverse-engineered and verified against real
  hardware; see [HM-Dis-EP-WM55.md](HM-Dis-EP-WM55.md).

## Quick Start

| Resource | Link |
|----------|------|
| **Protocol Details** | [HM-Dis-EP-WM55.md](HM-Dis-EP-WM55.md) |
| **Installation** | [INSTALLATION.md](INSTALLATION.md) |
| **Service Reference** | [docs/services.md](docs/services.md) |
| **Automation Example** | [docs/automations.md](docs/automations.md) |
| **Troubleshooting** | [docs/troubleshooting.md](docs/troubleshooting.md) |
| **Changelog** | [CHANGELOG.md](CHANGELOG.md) |
| **Issues** | [GitHub Issues][issues] |

## Installation

This integration is not (yet) listed in the official HACS default
repository, but it already meets all HACS requirements and can be added
right now as a **custom repository**:

1. In HACS → the three-dot menu (top right) → **Custom repositories**.
2. Add `RhonanMS/hm-dis-ep-wm55-integration` as category **Integration**.
3. Install "HM-Dis-EP-WM55 Display" from HACS, then restart Home Assistant.
4. **Settings → Devices & Services → Add Integration** → search for
   "HM-Dis-EP-WM55 Display" → select your display device and channel
   (default `3`).

Alternatively, install manually:

1. Copy `custom_components/hm_dis_ep_wm55/` into your Home Assistant
   `config/custom_components/` directory.
2. Restart Home Assistant.
3. **Settings → Devices & Services → Add Integration** → search for
   "HM-Dis-EP-WM55 Display" → select your display device and channel
   (default `3`).

Full step-by-step instructions, including how to copy files onto your HA
instance: [INSTALLATION.md](INSTALLATION.md).

## Requirements

- Home Assistant with [Homematic(IP) Local for OpenCCU][homematicip-local]
  installed and configured, with the HM-Dis-EP-WM55 already set up as a
  device there.
- An HM-Dis-EP-WM55 e-paper display, addressable on channel `3` (the
  device's default `SUBMIT` channel).

## Usage

```yaml
action: hm_dis_ep_wm55.send_message
data:
  device_id: <device_id from the config flow>
  line2: "Temperatur"
  icon2: information
  line3: "21.5 Grad"
  line4: "Fenster offen"
  icon4: fehler
  sound: kurz_kurz
  led: rot
```

Full field reference (all icons/sounds/LED colors, defaults, limits):
[docs/services.md](docs/services.md).

## Documentation

| Topic | Link |
|-------|------|
| **Protocol (SUBMIT byte format)** | [HM-Dis-EP-WM55.md](HM-Dis-EP-WM55.md) |
| **Installation** | [INSTALLATION.md](INSTALLATION.md) |
| **Service Reference** | [docs/services.md](docs/services.md) |
| **Automation Example Walkthrough** | [docs/automations.md](docs/automations.md) |
| **Troubleshooting** | [docs/troubleshooting.md](docs/troubleshooting.md) |
| **Architecture** | [docs/architecture.md](docs/architecture.md) |
| **Changelog** | [CHANGELOG.md](CHANGELOG.md) |

## Examples

[docs/automations.md](docs/automations.md) walks through a full window-status
automation (all-clear message, open-window list with LED/sound,
button-triggered reminder) — architecture, template logic and how to adapt
it for your own rooms/devices.

## Development

Parts of this project — including the protocol reverse-engineering, the
integration code, tests and documentation — were developed with agentic AI
assistance, primarily [Claude Code](https://www.anthropic.com/claude-code).
Every protocol detail was nonetheless verified against a real HM-Dis-EP-WM55
device by a human before landing in `protocol.py` — see the "Verified
Tests" section in [HM-Dis-EP-WM55.md](HM-Dis-EP-WM55.md). Details and
expectations for contributions: [AI_POLICY.md](AI_POLICY.md).

## Support and Contributing

| Resource | Link |
|----------|------|
| **Report Issues** | [GitHub Issues][issues] |
| **Contributing** | [CONTRIBUTING.md](CONTRIBUTING.md) |
| **AI Contribution Policy** | [AI_POLICY.md](AI_POLICY.md) |

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.

[homematicip-local]: https://github.com/SukramJ/homematicip_local
[issues]: https://github.com/RhonanMS/hm-dis-ep-wm55-integration/issues
[release]: https://github.com/RhonanMS/hm-dis-ep-wm55-integration/releases
[release-shield]: https://img.shields.io/github/v/release/RhonanMS/hm-dis-ep-wm55-integration?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/RhonanMS/hm-dis-ep-wm55-integration.svg?style=for-the-badge
[ha-shield]: https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-41BDF5.svg?style=for-the-badge&logo=home-assistant&logoColor=white
[ha]: https://www.home-assistant.io/getting-started/concepts-terminology/#integrations
