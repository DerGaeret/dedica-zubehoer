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

Hinten ist das Gitter offen. Die Lippe an der Unterseite greift mit 0,5 mm Spiel
in den Behälter. `HOEHE = 43` im Skript entspricht der Serienhöhe.
Druck: `dedica_lowprofile_gitter_druck.stl` (Deckplatte unten, ohne Stützen),
Behälter in PETG. Die übrigen STL/STEP liegen in Gebrauchslage.

**Hinweis zur Passform:** Ein anderes getestetes Modell (Printables 1908025)
hat unten einen D-förmigen Zapfen von ca. 104 × 111 mm, der in eine Mulde der
Dedica-Basis greift. Der Behälter (101,7 × 110,6 mm) passt zu dieser Mulde. Das
ist ein Indiz, kein Nachweis für deine Maschine.
