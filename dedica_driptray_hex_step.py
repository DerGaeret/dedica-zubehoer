"""DeLonghi Dedica Abtropfgitter mit Hexagon-Muster als STEP (CadQuery).

Gleiche Geometrie wie dedica_driptray_hex.scad, aber als echtes B-Rep-Modell.
Aufruf:  python3 dedica_driptray_hex_step.py   ->  dedica_driptray_hex.step
Ausgabe in Gebrauchslage (Deckplatte oben, Hinterkante bei y = 0).
"""
import math
import cadquery as cq

# Passform (aus Referenzmodellen, siehe README)
R_OBEN, R_UNTEN = 55.03, 60.25
Y_RUND = 57.5
HOEHE = 9.0
PLATTE = 3.0
WAND = 1.4
SCHUERZE_AB_Y = 1.0
ERHOEHUNG = 0.0          # mm zusätzlich nach unten (gerade Schürze)

# Rastnasen
NASE_X_INNEN, NASE_DICKE = 46.75, 3.0
NASE_Y = (27.55, 47.55)
NASE_Z_UNTEN = 1.0

# Hexagon-Muster
RAND, HEX_LOCH, HEX_STEG = 4.0, 7.0, 1.8


def d_wire(r, z, y0=0.0):
    """D-Form: hinten gerade bei y0, vorne Halbkreis um (0, Y_RUND)."""
    return (cq.Workplane("XY").workplane(offset=z)
            .moveTo(-r, y0).lineTo(r, y0).lineTo(r, Y_RUND)
            .threePointArc((0, Y_RUND + r), (-r, Y_RUND)).close())


def d_loft(r0, r1, z0, z1):
    w0 = d_wire(r0, z0).val()
    w1 = d_wire(r1, z1).val()
    return cq.Workplane("XY").add(cq.Solid.makeLoft([w0, w1], True))


def aussen(o=0.0):
    body = d_loft(R_UNTEN + o, R_OBEN + o, 0, HOEHE)
    if ERHOEHUNG > 0:
        body = body.union(d_wire(R_UNTEN + o, -ERHOEHUNG).extrude(ERHOEHUNG))
    return body


def hex_pts(cx, cy):
    rc = HEX_LOCH / math.sqrt(3)            # Eckradius
    return [(cx + rc * math.cos(math.radians(90 + 60 * k)),
             cy + rc * math.sin(math.radians(90 + 60 * k))) for k in range(6)]


z_platte = HOEHE - PLATTE
big = 400

# Schürze (hinten offen)
schuerze = (aussen().cut(aussen(-WAND))
            .cut(cq.Workplane("XY").box(big, big, big, centered=(True, False, True))
                 .translate((0, -big + SCHUERZE_AB_Y, 0))))

# Deckplatte
platte = aussen().intersect(
    cq.Workplane("XY").box(big, big, PLATTE, centered=(True, True, False))
    .translate((0, 0, z_platte)))

# Hexagon-Löcher, auf Innenbereich (Rand 4 mm) begrenzt
px = HEX_LOCH + HEX_STEG
py = px * math.sqrt(3) / 2
wp = cq.Workplane("XY").workplane(offset=z_platte - 1)
for j in range(-1, int(130 / py) + 1):
    for i in range(-int(70 / px) - 1, int(70 / px) + 2):
        wp = wp.polyline(hex_pts(i * px + (px / 2 if j % 2 else 0), j * py)).close()
hexe = wp.extrude(PLATTE + 2)
innen = d_wire(R_OBEN - RAND, z_platte - 1, y0=RAND).extrude(PLATTE + 2)
platte = platte.cut(innen.intersect(hexe))

teil = schuerze.union(platte)

# Rastnasen
for s in (-1, 1):
    x0 = NASE_X_INNEN if s > 0 else -NASE_X_INNEN - NASE_DICKE
    nase = (cq.Workplane("XY")
            .box(NASE_DICKE, NASE_Y[1] - NASE_Y[0], z_platte - NASE_Z_UNTEN + 0.01,
                 centered=False)
            .translate((x0, NASE_Y[0], NASE_Z_UNTEN)))
    teil = teil.union(nase)

teil = teil.translate((0, 0, ERHOEHUNG))
cq.exporters.export(teil, "dedica_driptray_hex.step")
v = teil.val()
bb = v.BoundingBox()
print(f"valid={v.isValid()} volume={v.Volume():.1f} mm3 "
      f"bbox=({bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f})")
