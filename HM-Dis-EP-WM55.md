# Controlling the HM-Dis-EP-WM55 from Home Assistant

> Protocol verified against real hardware (see "Verified Tests" below).
> Source/basis: [Gist by DrTob](https://gist.github.com/Folcr/896c6d32a161b1ede2c10892c4a513a7)
> (a HomeMatic script for the CCU scripting dialect, adapted to a
> Home-Assistant comma-separated hex string).

## Transmission Method

The command string is sent via the `homematicip_local.set_device_value`
service of the "Homematic(IP) Local for OpenCCU" integration, to the device
on **channel `3`**:

```yaml
action: homematicip_local.set_device_value
data:
  device_id: <device_id of the display>
  channel: 3
  parameter: SUBMIT
  value: "0x02,0x0A,...,0x03"
  value_type: string
```

The value is a **literal, comma-separated hex string** (e.g.
`"0x02,0x0A,0x12,..."`) — not raw binary bytes. This text form is translated
into the actual binary protocol for the device by the CCU/BidCos-RF
interface.

## Verified Tests

**Test A** — line 2 "Text" with icon ON, line 3 empty, line 4 "Text 1" with
icon ERROR, no sound, no LED blinking:

```
0x02,0x0A,0x12,0x54,0x65,0x78,0x74,0x13,0x81,0x0A,0x0A,0x12,0x54,0x65,0x78,0x74,0x20,0x31,0x13,0x84,0x0A,0x14,0xC0,0x1C,0xD0,0x1D,0xE0,0x16,0xF0,0x03
```

**Test B** — same as Test A, but two short beeps and a red LED:

```
0x02,0x0A,0x12,0x54,0x65,0x78,0x74,0x13,0x81,0x0A,0x0A,0x12,0x54,0x65,0x78,0x74,0x20,0x31,0x13,0x84,0x0A,0x14,0xC5,0x1C,0xD0,0x1D,0xE0,0x16,0xF1,0x03
```

Both strings were sent and produced the expected display/sound/LED behavior.

## Protocol Structure

```
Start code + 0x0A + [line-2 block] + [line-3 block] + [line-4 block] + [sound/repeat/distance/signal block] + End code
```

### Start Code

`0x02`, followed by a **fixed** `0x0A` (independent of the line blocks,
each of which brings its own trailing `0x0A` as well).

### End Code

`0x03`

### Line Block

There is **no** dedicated byte to select the line number. The three lines
(physically lines 2, 3, 4 of the display — line 1 cannot be addressed)
result purely from the **order** in which the three blocks are sent.

Each of the three blocks has the following structure:

* If text and/or an icon should be set:
  `0x12` + [text as hex codes, see character set] + (`0x13` + [icon code], only if an icon is set)
* Followed **always** by `0x0A` to close the block — even if neither text
  nor an icon is sent for this line (in that case the block consists only
  of `0x0A`, and the line stays empty/is cleared, since every transmission
  always replaces the complete display state).

Example for "Text" with icon ON on the first line:
`0x12,0x54,0x65,0x78,0x74,0x13,0x81,0x0A`

### Text

* Maximum of twelve characters per line
* Each character is translated into a hex byte via the character set table
  below (not plain ASCII encoding — see table below)

### Character Set Table

| Character | Code | Character | Code | Character | Code |
|---|---|---|---|---|---|
| A | `0x41` | a | `0x61` | 0 | `0x30` |
| B | `0x42` | b | `0x62` | 1 | `0x31` |
| C | `0x43` | c | `0x63` | 2 | `0x32` |
| D | `0x44` | d | `0x64` | 3 | `0x33` |
| E | `0x45` | e | `0x65` | 4 | `0x34` |
| F | `0x46` | f | `0x66` | 5 | `0x35` |
| G | `0x47` | g | `0x67` | 6 | `0x36` |
| H | `0x48` | h | `0x68` | 7 | `0x37` |
| I | `0x49` | i | `0x69` | 8 | `0x38` |
| J | `0x4A` | j | `0x6A` | 9 | `0x39` |
| K | `0x4B` | k | `0x6B` | (space) | `0x20` |
| L | `0x4C` | l | `0x6C` | ! | `0x21` |
| M | `0x4D` | m | `0x6D` | " | `0x22` |
| N | `0x4E` | n | `0x6E` | % | `0x25` |
| O | `0x4F` | o | `0x6F` | & | `0x26` |
| P | `0x50` | p | `0x70` | = | `0x27` |
| Q | `0x51` | q | `0x71` | ( | `0x28` |
| R | `0x52` | r | `0x72` | ) | `0x29` |
| S | `0x53` | s | `0x73` | * | `0x2A` |
| T | `0x54` | t | `0x74` | + | `0x2B` |
| U | `0x55` | u | `0x75` | , | `0x2C` |
| V | `0x56` | v | `0x76` | - | `0x2D` |
| W | `0x57` | w | `0x77` | . | `0x2E` |
| X | `0x58` | x | `0x78` | / | `0x2F` |
| Y | `0x59` | y | `0x79` | : | `0x3A` |
| Z | `0x5A` | z | `0x7A` | ; | `0x3B` |
| Ä | `0x5B` | ä | `0x7B` | @ | `0x40` |
| Ö | `0x23` | ö | `0x7C` | > | `0x3E` |
| Ü | `0x24` | ü | `0x7D` | | | |
| ß | `0x5F` | | | | |

Characters outside this table should be replaced with `0x3F` ("?").

### Icon Codes

Sent after the prefix byte `0x13`:

* `0x80` – `OFF` (no icon)
* `0x81` – `ON` (lightbulb / filled circle)
* `0x82` – `OPEN` (window open)
* `0x83` – `CLOSED` (window closed)
* `0x84` – `ERROR` (exclamation mark / triangle)
* `0x85` – `ALL OK` (checkmark)
* `0x86` – `INFORMATION` (i symbol)
* `0x87` – `NEW MESSAGE` (envelope)
* `0x88` – `SERVICE MESSAGE` (wrench)

### Sound/Repeat/Distance/Signal Block

After the three line blocks follows a four-part block of marker byte +
value, which sets the sound, repeat count, repeat distance and LED signal:

```
0x14 <sound pattern> 0x1C <repeat code> 0x1D <distance code> 0x16 <signal code>
```

#### Sound Pattern (after `0x14`)

* `0xC0` – sound off
* `0xC1` – long, long
* `0xC2` – long, short
* `0xC3` – long, short, short
* `0xC4` – short
* `0xC5` – short, short
* `0xC6` – long

#### Repeat Count (after `0x1C`)

How many times the message is repeated/signaled:

* `1`–`15` → `0xD0 + (n-1)` (i.e. `0xD0` = 1×, `0xD1` = 2×, … `0xDE` = 15×)
* `0` (infinite) → `0xDF`

#### Repeat Distance (after `0x1D`)

Time interval between repeats in seconds, rounded up to 10-second steps,
maximum 160 seconds:

`level = ceil(seconds / 10)` (range 1–16) → `0xE0 + (level-1)`

(`0xE0` = up to 10 s, `0xE1` = up to 20 s, … `0xEF` = up to 160 s)

#### Signal/LED (after `0x16`)

Controls the hardware LED on the housing:

* `0xF0` – LED off
* `0xF1` – LED red (usually blinking, for errors)
* `0xF2` – LED green (success confirmation)
* `0xF3` – LED orange
