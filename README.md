# DeLonghi Dedica Zubehör

## Abtropfgitter mit Hexagon-Muster (`dedica_driptray_hex.scad` / `.stl`)

Ersatz-Abtropfgitter für die Dedica EC680 / EC685 / EC885, mit durchgehendem
Hexagon-Lochmuster.

Die Passform stammt aus mehreren erprobten Community-Modellen, die alle auf
demselben Original-Gitter basieren:
[Printables 1608242](https://www.printables.com/model/1608242),
[1142660](https://www.printables.com/model/1142660),
[687455](https://www.printables.com/model/687455).

| Maß                       | Wert              |
|---------------------------|-------------------|
| Unterkante (Schürze)      | 120,5 × 117,75 mm |
| Deckplatte oben           | 110,1 × 112,5 mm  |
| Höhe                      | 9 mm (+ `erhoehung`) |
| Deckplatte                | 3 mm              |
| Rastnasen                 | 2 × 3 × 20 mm, innen links/rechts |

**Höher machen:** `erhoehung` in der `.scad` setzen (z. B. `5`). Die Schürze
wird dann unten gerade verlängert und die Oberseite sitzt entsprechend höher.

Druck: Oberseite liegt auf dem Bett (bereits so orientiert), keine Stützen
nötig. PETG empfohlen (heißes Wasser), 0,2 mm Schicht, 3 Wände.

### STEP-Datei

`dedica_driptray_hex.step` ist dasselbe Modell als echtes CAD-Modell (B-Rep)
für Fusion 360, Onshape, FreeCAD usw. Es ist in Gebrauchslage (Deckplatte
oben). Neu erzeugen: `pip install cadquery`, dann
`python3 dedica_driptray_hex_step.py` (Parameter oben in der Datei).

## Flache Abtropfschale, 2 Teile (`dedica_lowprofile.py`)

Ersetzt die Serien-Abtropfschale komplett: **Wabengitter oben + Abtropfbehälter
unten**, Bauhöhe 32 mm statt ca. 43 mm. Konzept angelehnt an die Schale auf
studio48nord.de (ohne deren Prägung/Branding).

Dateien: `dedica_lowprofile_gitter.{step,stl}`, `dedica_lowprofile_behaelter.{step,stl}`,
`dedica_lowprofile_montage.stl` (nur Ansicht). Neu erzeugen: `python3 dedica_lowprofile.py`.

| Teil     | Maß (B × T × H)        | Quelle |
|----------|------------------------|--------|
| Gitter   | 148,7 × 134,1 × 32 mm  | Produktseite |
| Behälter | 101,7 × 110,6 × 21,2 mm | Produktseite |
| Wandstärken, Schräge, Lippe, Spiel, Wabengröße | siehe Skriptkopf | **geschätzt** |
| Anschluss hinten an die Maschine | – | **unbekannt, bitte prüfen** |

Draufsicht: Halbkreis vorne mit geraden Seiten (D-Form). Nach dem Halbkreis bleibt
die Seite noch `GERADE_VOR` = 15 mm ganz gerade; erst dann beginnt an den oberen
Seitenkanten die Schräge, die zur offenen Hinterkante hin größer wird. Von hinten
gesehen ist das Gitter ein Trapez (unten senkrechte Seiten, dann Schultern, schmalere
Oberseite). Winkel `SCHULTER_WINKEL` = 30° zur Senkrechten, gemessen am Maschinenrand
im Printables-Modell 1908025 (29-32°); `SCHULTER_H` = 18 mm Höhe der Schulter (aus der
Skizze), daraus ca. 10,4 mm Versatz pro Seite.
Gegenprobe an anderen Modellen: Mulde der Maschinenbasis 103-104 × 110-113 mm
(Printables 1799189, 1488151, 585177), Serien-Schale 148 × 132 mm mit 58 mm geraden
Seiten (Printables 1737892). Beides passt zu den Maßen hier.
Der Behälter hat vorne einen Griff (30 mm breit, 14 mm lang, 45°-Unterseite ohne
Stützen druckbar, Leiste am Ende), daher ist er 124,6 mm tief.

Hinten ist das Gitter offen. Die Lippe an der Unterseite greift mit 0,5 mm Spiel
in den Behälter. `HOEHE = 43` im Skript entspricht der Serienhöhe.
Druck: `dedica_lowprofile_gitter_druck.stl` (Deckplatte unten, ohne Stützen),
Behälter in PETG. Die übrigen STL/STEP liegen in Gebrauchslage.

**Hinweis zur Passform:** Ein anderes getestetes Modell (Printables 1908025)
hat unten einen D-förmigen Zapfen von ca. 104 × 111 mm, der in eine Mulde der
Dedica-Basis greift. Der Behälter (101,7 × 110,6 mm) passt zu dieser Mulde. Das
ist ein Indiz, kein Nachweis für deine Maschine.

## Druck-Setup: Qidi Plus 4 + OrcaSlicer

`dedica_lowprofile_druckplatte.3mf` enthält beide Teile in Druckausrichtung
(Gitter mit der Platte nach unten, Behälter normal), mittig auf dem Bett
(305 × 305 × 280 mm). Belegt: ca. 262 × 134 mm, höchstes Teil 32 mm. Das 3MF
enthält nur die Geometrie, keine Slicer-Einstellungen: Drucker, Prozess und
Filament wählst du in Orca selbst.

**Profile in Orca:** Drucker `Qidi Plus 4 0.4 nozzle`, Prozess `0.20mm Standard`,
Filament `Qidi PETG` (bzw. `Qidi PLA`). Die Maße sind auf 0,4-mm-Düse und 0,2-mm-Schichten
abgestimmt (Wand 2,4 mm = 6 Linien, Lippe 1,6 mm = 4 Linien, Wabenstege 1,4 mm,
Deckplatte 3,0 mm = 15 Schichten, Behälterwand 2,0 mm, Boden 2,0 mm).

| Einstellung | Wert |
|---|---|
| Material | Behälter PETG (steht im Wasser). Gitter PETG oder PLA |
| Düse PETG | 240–260 °C (Qidi-Datenblatt: 240–275 °C) |
| Bett PETG | 70–80 °C (Qidi-Datenblatt) |
| Kammer | Heizung aus bzw. niedrig, Deckel/Tür bei PLA offen. Bei PLA/PETG nicht auf 60 °C heizen |
| Stützen | keine nötig (Schrägen 30°, Griffkeil 45°, Gitter liegt auf der Platte) |
| Wandanzahl | 4–5 Wände (Behälter wasserdicht), Wandgenerator Arachne |
| Boden/Deckel | Behälter: 5 Boden-/Deckschichten. Gitterplatte ist 15 Schichten massiv |
| Füllung | 15 % Gyroid reicht, die Teile bestehen fast nur aus Wänden |
| Naht | Gitter: hinten (offene Seite), Behälter: hinten |
| Kühlung PETG | Bauteillüfter 30–50 % |

Hinweise: PETG haftet auf texturiertem PEI sehr gut, bei Bedarf einen dünnen
Kleberstift-Film als Trennschicht auftragen. Nach dem Druck Behälter auf Dichtheit
prüfen (Wasser einfüllen). Werte für Düse/Bett stammen aus dem Qidi-Datenblatt für
PETG. Passe sie an dein konkretes Filament an.
