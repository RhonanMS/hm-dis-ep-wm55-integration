# Troubleshooting

Real issues hit (and fixed) during development of this integration.

## Device picker in Developer Tools → Actions shows no device

**Symptom:** `hm_dis_ep_wm55.send_message` is listed, but the device-target
picker at the top of the action dialog has no matching entries, even though
the device exists under **Settings → Devices & Services → Devices**.

**Cause:** Home Assistant removed support for `integration` device filters
on the `target:` block of a service (frontend ignored it since 2025.10,
validation fails outright from 2026.11 — see
[Device filter has been removed from target selector](https://developers.home-assistant.io/blog/2025/10/14/device-filter-removed-from-target-selector/)).

**Fix:** This integration no longer uses `target:` in `services.yaml`.
Instead, the device is a regular field called **"Display"** (`device_id`),
located with the other service fields rather than in the "Targets" section
at the top of the dialog. If you're on an old copy of this integration that
still has `target: device: integration:` in `services.yaml`, update to a
current version.

## Sending the SUBMIT string via the plain "Wert" text field does nothing

**Symptom:** Typing a byte sequence like `0x02,0x0A,...` directly into the
"Wert" (value) field of `homematicip_local.set_device_value` in
**Developer Tools → Actions** (UI mode) appears to do nothing, or the
display shows unrelated/stale content, no matter what you send.

**Cause:** This isn't a protocol problem — it's how the field is being
filled in. A plain UI text field can only contain typable, printable
characters. The SUBMIT protocol's control bytes (`0x02`, `0x0A`, `0x03`,
...) are **not** typable — and critically, the correct wire value for this
parameter *is* the literal, comma-separated hex-notation string (e.g.
`"0x02,0x0A,0x12,0x54,..."`) as plain text, which Home Assistant's
`homematicip_local` integration and the CCU translate into the actual
binary protocol. Typing that same literal string character-for-character
into the UI field does work for the *text* portions, but control bytes
and anything requiring exact byte sequences are easy to get subtly wrong
by hand.

**Fix:** Build the value programmatically (this integration's
`protocol.py` does exactly that — see
[docs/architecture.md](architecture.md)) rather than typing it by hand. If
you need to experiment manually, switch the action dialog to **YAML mode**
and write the value as a quoted YAML string — YAML's `\xNN` escape syntax
also works if you want to express raw bytes directly, e.g.
`value: "\x02\x0AText\x81\x03"`.

## "Target vs. field" mental model

When writing or debugging `services.yaml` for *any* custom integration,
remember: **`target:` is for entity/area/floor/label selection that Home
Assistant's core already understands generically** (entities, devices by
*entity* domain, areas). For anything integration-specific — like "only
show devices belonging to *my* integration" — define a regular **field**
with a `device` selector and an `integration:` filter instead. This is
also what `homematicip_local` itself does for `set_device_value`'s device
selection.

## See Also

- [HM-Dis-EP-WM55.md](../HM-Dis-EP-WM55.md) — protocol details and the
  hardware-verified reference strings.
- [docs/services.md](services.md) — full `send_message` field reference.
