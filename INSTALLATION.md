# Installation der HM-Dis-EP-WM55 Integration

Diese Integration ist (noch) nicht über HACS verfügbar, da sie lokal
entwickelt wurde. Sie muss manuell als „Custom Component" in Home Assistant
übernommen werden.

## Voraussetzung

Die Integration **„Homematic(IP) Local for OpenCCU"** (`homematicip_local`)
muss bereits installiert und eingerichtet sein, inklusive des Geräts für das
HM-Dis-EP-WM55 Display.

## Schritt 1: Dateien nach Home Assistant kopieren

Kopiere den kompletten Ordner `custom_components/hm_dis_ep_wm55/` aus diesem
Projekt in das `custom_components`-Verzeichnis Deiner Home-Assistant-Instanz,
sodass am Ende folgende Struktur existiert:

```
<HA-Konfigurationsverzeichnis>/
└── custom_components/
    └── hm_dis_ep_wm55/
        ├── __init__.py
        ├── config_flow.py
        ├── const.py
        ├── protocol.py
        ├── manifest.json
        ├── services.yaml
        ├── strings.json
        └── translations/
            └── de.json
```

Falls `custom_components/` in Deiner HA-Installation noch nicht existiert,
leg es im selben Verzeichnis an, in dem auch `configuration.yaml` liegt.

Je nachdem, wie Deine Home-Assistant-Instanz läuft, eignet sich eine der
folgenden Methoden:

### Option A: File editor / Studio Code Server (Add-on)

1. Im HA-Add-on **„File editor"** oder **„Studio Code Server"** zum
   Konfigurationsverzeichnis navigieren.
2. Ordner `custom_components/hm_dis_ep_wm55/` anlegen (falls nicht vorhanden)
   und alle Dateien aus diesem Projekt dort hochladen/einfügen.

### Option B: Samba / Netzwerkfreigabe

1. Im HA-Add-on-Store das **„Samba share"** Add-on installieren/starten
   (falls noch nicht vorhanden).
2. Die Freigabe `config` am eigenen Rechner einbinden.
3. Den Ordner `custom_components/hm_dis_ep_wm55/` aus diesem Projekt in
   `config/custom_components/` kopieren.

### Option C: SSH / SCP

```bash
scp -r custom_components/hm_dis_ep_wm55 \
    root@homeassistant.intern.bjoern-eilers.de:/config/custom_components/
```

(Pfad ggf. anpassen, je nachdem ob SSH-Add-on oder direkter Zugriff auf das
Host-Dateisystem genutzt wird.)

## Schritt 2: Home Assistant neu starten

Custom Components werden nur beim Start eingelesen:
**Einstellungen → System → Neu starten** (oder Entwicklerwerkzeuge → YAML →
„Home Assistant neu starten", ein vollständiger Neustart ist bei neuen
Integrationen sicherer als ein reines YAML-Reload).

## Schritt 3: Integration einrichten

1. **Einstellungen → Geräte & Dienste → Integration hinzufügen**
2. Nach „HM-Dis-EP-WM55 Display" suchen und auswählen.
3. Im Dialog:
   - **Display-Gerät**: das Homematic-Gerät auswählen, das Dein
     HM-Dis-EP-WM55 repräsentiert.
   - **Kanal**: `3` (Standardwert, i.d.R. unverändert lassen).
   - **Name**: optional, falls Du mehrere Displays einrichtest.
4. Mit „Absenden" bestätigen.

Für jedes weitere Display kann der Vorgang wiederholt werden (eigener Config
Entry pro Display/Kanal-Kombination).

## Schritt 4: Testen

**Entwicklerwerkzeuge → Aktionen** (bzw. „Developer Tools → Actions"):

1. Aktion `hm_dis_ep_wm55.send_message` auswählen.
2. Im Feld **„Display"** das beim Einrichten angelegte Gerät auswählen
   (Mehrfachauswahl möglich, falls mehrere Displays konfiguriert sind).
   Hinweis: Das Gerät wird hier bewusst als normales *Feld* ausgewählt und
   nicht über die „Ziel"-Funktion oben im Dialog — Home Assistant hat die
   Geräte-Filterung für „Ziel" entfernt, daher steht die Geräteauswahl direkt
   bei den anderen Service-Feldern.
3. Beispiel-Felder ausfüllen:
   - `line2`: `Test`
   - `icon2`: `ein`
   - `line4`: `Text 1`
   - `icon4`: `fehler`
   - `sound`: `kurz_kurz`
   - `led`: `rot`
4. Aktion ausführen und Display prüfen.

## In Automatisierungen verwenden

```yaml
action: hm_dis_ep_wm55.send_message
data:
  device_id: <device_id aus Schritt 3>
  line2: "{{ states('sensor.aussentemperatur') }}°C"
  icon2: information
  line4: "Tuer offen"
  icon4: fehler
  sound: kurz_kurz
  led: rot
```

`device_id` kann auch eine Liste sein, um mehrere Displays gleichzeitig
anzusteuern. Die ID bekommst Du am einfachsten, indem Du in
Entwicklerwerkzeuge → Aktionen das Display im Feld „Display" per UI auswählst
und dann in den YAML-Modus wechselst — dort steht die `device_id` dann im
Klartext.

## Deinstallation / Update

- **Update**: Dateien im `custom_components/hm_dis_ep_wm55/`-Ordner
  überschreiben, danach Home Assistant neu starten.
- **Deinstallation**: Integration über **Einstellungen → Geräte & Dienste**
  entfernen, danach den Ordner `custom_components/hm_dis_ep_wm55/` löschen und
  Home Assistant neu starten.
