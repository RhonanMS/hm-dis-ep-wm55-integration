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

> **Clearing a line reliably:** omitted text is always sent as a single
> space, so an unset `lineX` reliably blanks that line (hardware-verified).
> To remove an icon from a line, simply omit `iconX` from the call (together
> with the `lineX` text you want shown, since a full line is always
> rewritten anyway) — the protocol has no dedicated "no icon" value; the
> icon sub-block (`0x13` + code) is only sent when `iconX` is set, and
> omitting it is the mechanism for showing no icon. **This is not yet
> hardware-verified in this repository** — see the open question in
> [HM-Dis-EP-WM55.md](../HM-Dis-EP-WM55.md#icon-codes) and
> [docs/automations.md](automations.md#clearing-icons-on-every-state-change).
> Previously this page recommended passing `iconX: aus` explicitly instead;
> that is now believed to be wrong — `aus` (`0x80`) is most likely a
> distinct icon graphic (an unlit bulb, the counterpart to `ein`'s lit
> bulb), not a "no icon" sentinel, so sending it would show an icon rather
> than clear one.

## `icon2`/`icon3`/`icon4` options

| Value | Meaning |
|-------|---------|
| `aus` | Off — likely a distinct "unlit bulb" icon graphic (counterpart to `ein`), **not** a "no icon" value; see the note above on clearing icons |
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
