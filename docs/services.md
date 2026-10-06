# Service Reference: `hm_dis_ep_wm55.send_message`

Sends text, icons, a beeper sound and an LED signal to one or more
HM-Dis-EP-WM55 displays. Internally builds the SUBMIT byte string (see
[HM-Dis-EP-WM55.md](../HM-Dis-EP-WM55.md)) and forwards it via
`homematicip_local.set_device_value`.

## Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|--------------|
| `device_id` | device selector (multiple) | yes | — | One or more HM-Dis-EP-WM55 devices, as set up via the integration's config flow. |
| `line2` | string | no | *(empty)* | Text for line 2, max. 12 characters (see character set below). |
| `icon2` | select | no | *(none)* | Icon for line 2. |
| `line3` | string | no | *(empty)* | Text for line 3, max. 12 characters. |
| `icon3` | select | no | *(none)* | Icon for line 3. |
| `line4` | string | no | *(empty)* | Text for line 4, max. 12 characters. |
| `icon4` | select | no | *(none)* | Icon for line 4. |
| `sound` | select | no | `aus` | Beeper sound pattern played once. |
| `repeat` | number | no | `1` | How many times the message/signal repeats. `0` = infinite, `1`-`15` otherwise. |
| `distance` | number | no | `10` | Seconds between repeats (only relevant if `repeat != 1`), rounded up to the next 10-second step, max. `160`. |
| `led` | select | no | `aus` | LED signal color. `rot` blinks by hardware design (see device behavior notes). |

Text longer than 12 characters is truncated with a log warning; characters
outside the supported set are replaced with `?` and logged. German umlauts
(`ä ö ü Ä Ö Ü ß`) are natively supported — no transliteration needed.

## `icon2`/`icon3`/`icon4` options

| Value | Meaning |
|-------|---------|
| `aus` | Off (no icon) |
| `ein` | On (filled bulb/circle) |
| `offen` | Open (window) |
| `geschlossen` | Closed (window) |
| `fehler` | Error (exclamation mark / triangle) |
| `alles_ok` | All OK (checkmark) |
| `information` | Information (i) |
| `neue_nachricht` | New message (envelope) |
| `servicemeldung` | Service message (wrench) |

## `sound` options

| Value | Meaning |
|-------|---------|
| `aus` | No sound |
| `lang_lang` | Long, long |
| `lang_kurz` | Long, short |
| `lang_kurz_kurz` | Long, short, short |
| `kurz` | Short |
| `kurz_kurz` | Short, short |
| `lang` | Long |

## `led` options

| Value | Meaning |
|-------|---------|
| `aus` | LED off |
| `rot` | Red (typically blinks, device-dependent) |
| `gruen` | Green |
| `orange` | Orange |

## Example

```yaml
action: hm_dis_ep_wm55.send_message
data:
  device_id: <device_id>
  line2: "Temperatur"
  icon2: information
  line3: "21.5 Grad"
  line4: "Fenster offen"
  icon4: fehler
  sound: kurz_kurz
  led: rot
```

## See Also

- [Protocol details](../HM-Dis-EP-WM55.md) — exact SUBMIT byte layout and
  the two hardware-verified reference strings.
- [Automation example](automations.md) — a full window-status automation
  using this service.
