# HM-Dis-EP-WM55-Ansteuerung aus Home Assistant

> Protokoll verifiziert an echter Hardware (siehe „Verifizierte Tests" unten).
> Quelle/Basis: [Gist von DrTob](https://gist.github.com/Folcr/896c6d32a161b1ede2c10892c4a513a7)
> (HomeMatic-Script für den CCU-Scripting-Dialekt, auf Home-Assistant-Komma-Hex-String übertragen).

## Übertragungsweg

Der Befehls-String wird per Service `homematicip_local.set_device_value` der
Integration „Homematic(IP) Local for OpenCCU" an das Gerät auf **Kanal `3`**
geschickt:

```yaml
action: homematicip_local.set_device_value
data:
  device_id: <device_id des Displays>
  channel: 3
  parameter: SUBMIT
  value: "0x02,0x0A,...,0x03"
  value_type: string
```

Der Wert ist ein **literaler, Komma-separierter Hex-String** (z. B.
`"0x02,0x0A,0x12,..."`) — keine rohen Binärbytes. Diese Textform wird von der
CCU/BidCos-RF-Schnittstelle in das tatsächliche Binärprotokoll zum Gerät
übersetzt.

## Verifizierte Tests

**Test A** — Zeile 2 „Text" mit Icon EIN, Zeile 3 leer, Zeile 4 „Text 1" mit
Icon FEHLER, kein Ton, kein LED-Blinken:

```
0x02,0x0A,0x12,0x54,0x65,0x78,0x74,0x13,0x81,0x0A,0x0A,0x12,0x54,0x65,0x78,0x74,0x20,0x31,0x13,0x84,0x0A,0x14,0xC0,0x1C,0xD0,0x1D,0xE0,0x16,0xF0,0x03
```

**Test B** — wie Test A, aber zweimal kurz piepen und rote LED:

```
0x02,0x0A,0x12,0x54,0x65,0x78,0x74,0x13,0x81,0x0A,0x0A,0x12,0x54,0x65,0x78,0x74,0x20,0x31,0x13,0x84,0x0A,0x14,0xC5,0x1C,0xD0,0x1D,0xE0,0x16,0xF1,0x03
```

Beide Strings wurden gesendet und ergaben das erwartete Anzeige-/Ton-/LED-Verhalten.

## Aufbau

```
Start-Code + 0x0A + [Zeile-2-Block] + [Zeile-3-Block] + [Zeile-4-Block] + [Sound/Repeat/Distance/Signal-Block] + End-Code
```

### Start-Code

`0x02`, gefolgt von einem **festen** `0x0A` (unabhängig von den Zeilen-Blöcken,
die jeweils selbst noch ein eigenes abschließendes `0x0A` mitbringen).

### End-Code

`0x03`

### Zeilen-Block

Es gibt **kein** eigenes Byte zur Auswahl der Zeilennummer. Die drei Zeilen
(physisch Zeile 2, 3, 4 des Displays — Zeile 1 ist nicht ansteuerbar) ergeben
sich allein aus der **Reihenfolge**, in der die drei Blöcke gesendet werden.

Jeder der drei Blöcke hat folgenden Aufbau:

* Falls Text und/oder Icon gesetzt werden sollen:
  `0x12` + [Text als Hex-Codes, siehe Zeichensatz] + (`0x13` + [Icon-Code], nur falls ein Icon gesetzt wird)
* Danach **immer** `0x0A` als Abschluss des Blocks — auch wenn für diese
  Zeile weder Text noch Icon gesendet wird (dann besteht der Block nur aus
  `0x0A` und die Zeile bleibt leer/unverändert... bzw. wird geleert, da jede
  Übertragung immer den kompletten Anzeigezustand ersetzt).

Beispiel für „Text" mit Icon EIN auf der ersten Zeile:
`0x12,0x54,0x65,0x78,0x74,0x13,0x81,0x0A`

### Text

* Maximal zwölf Zeichen pro Zeile
* Jedes Zeichen wird über die Zeichensatz-Tabelle in ein Hex-Byte übersetzt
  (keine reine ASCII-Codierung — siehe Tabelle unten)

### Zeichensatz-Tabelle

| Zeichen | Code | Zeichen | Code | Zeichen | Code |
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
| K | `0x4B` | k | `0x6B` | (Leerzeichen) | `0x20` |
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

Zeichen außerhalb dieser Tabelle sollten durch `0x3F` ("?") ersetzt werden.

### Icon-Codes

Werden nach dem Präfix-Byte `0x13` gesendet:

* `0x80` – `AUS` (Kein Icon)
* `0x81` – `EIN` (Glühbirne / gefüllter Kreis)
* `0x82` – `OFFEN` (Fenster offen)
* `0x83` – `GESCHLOSSEN` (Fenster zu)
* `0x84` – `FEHLER` (Ausrufezeichen / Dreieck)
* `0x85` – `ALLES OK` (Häkchen)
* `0x86` – `INFORMATION` (i-Symbol)
* `0x87` – `NEUE NACHRICHT` (Briefumschlag)
* `0x88` – `SERVICEMELDUNG` (Schraubenschlüssel)

### Sound/Repeat/Distance/Signal-Block

Nach den drei Zeilen-Blöcken folgt ein vierteiliger Block aus
Marker-Byte + Wert, der Ton, Wiederholungen, Abstand und LED-Signal
festlegt:

```
0x14 <Tonfolge> 0x1C <Wiederholungen-Code> 0x1D <Abstand-Code> 0x16 <Signal-Code>
```

#### Tonfolge (nach `0x14`)

* `0xC0` – Ton aus
* `0xC1` – Lang, lang
* `0xC2` – Lang, kurz
* `0xC3` – Lang, kurz, kurz
* `0xC4` – Kurz
* `0xC5` – Kurz, kurz
* `0xC6` – Lang

#### Wiederholungen (nach `0x1C`)

Wie oft die Nachricht wiederholt angezeigt/signalisiert wird:

* `1`–`15` → `0xD0 + (n-1)` (also `0xD0` = 1×, `0xD1` = 2×, … `0xDE` = 15×)
* `0` (unendlich) → `0xDF`

#### Abstand (nach `0x1D`)

Zeitlicher Abstand zwischen Wiederholungen in Sekunden, aufgerundet auf
10-Sekunden-Schritte, maximal 160 Sekunden:

`level = aufrunden(sekunden / 10)` (Bereich 1–16) → `0xE0 + (level-1)`

(`0xE0` = bis 10 s, `0xE1` = bis 20 s, … `0xEF` = bis 160 s)

#### Signal/LED (nach `0x16`)

Steuert die Hardware-LED am Gehäuse:

* `0xF0` – LED aus
* `0xF1` – LED Rot (meist blinkend für Fehler)
* `0xF2` – LED Grün (Erfolgsbestätigung)
* `0xF3` – LED Orange
