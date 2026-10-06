# Automation Example: Window Status Display

This page documents the architecture and template logic of a window-status
automation built on top of `hm_dis_ep_wm55.send_message`, so you can build
your own version for your rooms and devices. (The original, filled-in YAML
is not published here — it embeds installation-specific identifiers such as
a `homematicip_local` device ID for the button trigger — but every piece
needed to recreate it is below.)

## What It Does

1. **All windows closed** → `Alles OK!` on line 3, icon `alles_ok`, green LED.
2. **Any window open** → `OFFEN:` on line 2 (icon `offen`), followed by the
   abbreviations of the open rooms wrapped across line 3/4, red LED.
3. **Upper button pressed while Büro or Bad is open** → re-sends the exact
   same message as (2), additionally playing the `lang_kurz_kurz` sound.

## Architecture

A single script, `script.hm_dis_ep_wm55_fensterstatus`, holds all the logic
and takes one parameter (`sound`). Two automations call it with a different
`sound` value:

- **"Fensterstatus aktualisieren"** — triggers on any of the 6 window
  `binary_sensor` entities changing state, calls the script with
  `sound: aus` (silent update). This single trigger covers both the
  "all closed" and "some open" cases — the script's internal `choose`
  decides which message to build.
- **"Erinnerung bei Tastendruck"** — triggers on the display's upper-button
  device trigger, with a condition that Büro or Bad is currently open,
  calls the script with `sound: lang_kurz_kurz`.

Because both automations call the *same* script with the *same* window
sensors, the message content is guaranteed to be identical between an
automatic update and a button-triggered reminder — "gleichbleibende
Meldung" is a consequence of sharing the logic, not something tracked
separately.

### Line-wrapping

The script builds a single template string `"<line3>||<line4>"`: it
iterates over the configured rooms in a fixed order, and for every open
room appends its 3-letter abbreviation (space-separated) to line 3 until
that would exceed 12 characters, then continues on line 4. With up to 6
rooms at 3 letters each, this always fits in the two 12-character lines.
As a safety net, `protocol.py` itself also truncates (with a log warning)
if a line ever exceeds 12 characters for any reason.

The template is written entirely with `{%- -%}` whitespace trimming and
avoids relying on Home Assistant's "native type" template parsing for
intermediate lists — both are easy ways to accidentally turn a clean list
into a string full of stray newlines in Jinja. Splitting the final
`"<line3>||<line4>"` string on `||` sidesteps that entirely.

## Placeholders to Replace

| Placeholder | Where | What |
|-------------|-------|------|
| `<<DEVICE_ID_HM_DIS_EP_WM55>>` | Script (2×) | `device_id` of the HM-Dis-EP-WM55 device from the integration's config flow — see [INSTALLATION.md](../INSTALLATION.md). |
| `binary_sensor.FENSTER_BAD` / `_BUERO` / `_KIZ` / `_WOZ` / `_SCZ` / `_KUEC` | Script `rooms` dict, Automation A trigger, Automation B condition | One aggregated `binary_sensor` per room (`on` = at least one window open in that room). |

## Adapting It

- **Different rooms/abbreviations**: edit the `rooms` dict in the script —
  keep abbreviations short (3-4 letters) so the line-wrap math still works
  for your room count.
- **Different button**: replace the device trigger in Automation B — pick
  it via the Home Assistant UI trigger picker on your display device
  instead of copying ours, since the exact `type`/`subtype` values can
  differ by `homematicip_local` version and device firmware.
- **No reminder automation**: Automation B is optional; Automation A alone
  already covers requirements 1 and 2.
