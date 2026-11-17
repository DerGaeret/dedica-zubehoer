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
