# DeLonghi Dedica Zubehör

## Abtropfgitter mit Hexagon-Muster (`dedica_driptray_hex.scad` / `.stl`)

Einsatz für die schwarze Mulde der Abtropfschale. Die Oberseite schließt bündig
mit der Kante ab, an der das schwarze Teil ins graue Gehäuse übergeht.

**Vor dem Druck nachmessen** und oben in der `.scad` eintragen:

| Parameter      | Was messen                                   | Standardwert |
|----------------|----------------------------------------------|--------------|
| `mulde_breite` | Innenbreite der Mulde                        | 110 mm       |
| `mulde_tiefe`  | Innentiefe hinten bis vorderster Punkt       | 100 mm       |
| `hoehe`        | Muldenboden bis Kante schwarz/grau           | 18 mm        |

Dann in OpenSCAD `F6` → *Export as STL*.

Druck: Oberseite liegt auf dem Bett (bereits so orientiert), keine Stützen nötig.
PETG empfohlen (heißes Wasser), 0,2 mm Schicht, 3 Wände.
