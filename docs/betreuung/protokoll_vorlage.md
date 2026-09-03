# Abnahmeprotokoll TurtleBot 4

> Eine Kopie pro Roboter. Ablauf siehe [robotercheck.md](robotercheck.md).

**Roboter:** ______________  **Domain ID:** ______  **IP:** ________________
**Rolle:** ☐ Standardplatz ___  ☐ Ersatzgerät
**Geprüft von:** ______________  **Datum:** ____________  **Platz:** ______

---

## 1 Hardware

| Punkt | OK | Bemerkung |
|---|---|---|
| Aufkleber (Domain ID, MAC) lesbar | ☐ | |
| Räder frei, Laufflächen in Ordnung | ☐ | |
| Bumper federt | ☐ | |
| LiDAR dreht frei, Kuppel sauber | ☐ | |
| Kamera sauber und fest | ☐ | |
| Dock-Kontakte sauber | ☐ | |
| Ladestation frei aufgestellt | ☐ | |
| Display / Tasten | ☐ | |

## 2 Boot & Netzwerk

| Punkt | OK | Wert / Bemerkung |
|---|---|---|
| Bootet in < 2 min | ☐ | |
| `ping` erfolgreich | ☐ | |
| SSH-Login möglich | ☐ | |
| Domain ID stimmt mit Aufkleber | ☐ | |
| Create-3-Firmware | ☐ | Version: |

## 3 Automatischer Check (`tools/tb4_check.sh`)

| Punkt | OK | Bemerkung |
|---|---|---|
| Pakete auf dem Rechner vollständig | ☐ | |
| Alle Pflicht-Topics sichtbar | ☐ | |
| `/scan` ≥ 5 Hz | ☐ | Hz: |
| `/odom` ≥ 10 Hz | ☐ | Hz: |
| Akkustand | ☐ | %: |
| Diagnostics ohne ERROR | ☐ | |

Ausgabe gespeichert unter: ______________________________

## 4 Antrieb

| Punkt | OK | Bemerkung |
|---|---|---|
| Undock | ☐ | |
| 0,5 m geradeaus (kein Ziehen) | ☐ | |
| 180°-Drehung rund | ☐ | |
| Dock beim ersten Versuch | ☐ | |
| Lädt nach dem Docken | ☐ | |

## 5 SLAM

| Punkt | OK | Bemerkung |
|---|---|---|
| Karte entsteht in RViz | ☐ | |
| Wände einfach, nicht doppelt | ☐ | |
| Karte gespeichert (`.pgm` + `.yaml`) | ☐ | |

## 6 Navigation

| Punkt | OK | Bemerkung |
|---|---|---|
| Lokalisierung sitzt (Scan auf Wänden) | ☐ | |
| Nav2-Ziel erreicht | ☐ | |
| Weicht Hindernis aus | ☐ | |
| `patrol` fährt die Route und dockt | ☐ | |

---

## Gesamturteil

☐ **einsatzbereit**  ☐ **einsatzbereit mit Einschränkung**  ☐ **nicht einsatzbereit**

Offene Punkte / Reparaturbedarf:

_______________________________________________________________________

_______________________________________________________________________

Unterschrift: ______________________
