"""DeLonghi Dedica – flache Abtropfschale (2 Teile): Wabengitter + Abtropfbehälter.

Ersetzt die Serien-Abtropfschale komplett. Aufbau (angelehnt an das Konzept
"Gitter oben, Behälter unten"):

  * Gitter (Schale): hohler Korpus, hinten offen, Seiten leicht ausgestellt,
    Deckplatte mit Hexagon-Feld und einer Lippe an der Unterseite, die in die
    Mündung des Behälters greift.
  * Behälter: flache D-Form, fängt das Wasser, lässt sich mit zwei Fingern
    herausheben (Griffmulde vorne).

MASSE – woher sie kommen
  Von der Produktseite des Vorbilds (veröffentlicht):
    Gitter 148,7 x 134,1 x 32,0 mm, Behälter 101,7 x 110,6 x 21,2 mm.
  GESCHÄTZT (nicht veröffentlicht, bitte prüfen): Wandstärken, Schräge,
  Lippe, Spiel, Wabengröße, Höhe der Platte.
  UNBEKANNT: Anschluss hinten an die Maschine (Säule / Standfläche).

Aufruf:  python3 dedica_lowprofile.py
Ausgabe: dedica_lowprofile_gitter.{step,stl}, dedica_lowprofile_behaelter.{step,stl},
         dedica_lowprofile_montage.stl (nur zur Ansicht)
Koordinaten: x = links/rechts (Mitte 0), y = nach vorne, Hinterkante bei y = 0,
z = nach oben (Gebrauchslage).
"""
import math
import cadquery as cq

# ---------------- Gitter (veröffentlicht) ----------------
BREITE, TIEFE, HOEHE = 148.7, 134.1, 32.0     # Hoehe: 43 = Serienhöhe
# ---------------- Behälter (veröffentlicht) ----------------
B_BREITE, B_TIEFE, B_HOEHE = 101.7, 110.6, 21.2

# ---------------- geschätzt ----------------
SCHRAEGE = 1.5        # Oberseite pro Seite um so viel schmaler als unten
WAND = 2.4            # Wand des Gitterkorpus
PLATTE = 3.0          # Deckplatte
B_WAND = 2.0          # Behälterwand
B_BODEN = 2.0
SPIEL = 0.5           # Luft pro Seite zwischen Lippe und Behälter
LIPPE_WAND = 1.6
LIPPE_EINTAUCH = 4.0  # so tief taucht die Lippe in den Behälter
HEX_LOCH, HEX_STEG = 5.6, 1.4   # Schlüsselweite / Steg -> Raster 7,0 mm
GRIFF_R = 9.0         # Radius der Griffmulde vorne am Behälter

R = BREITE / 2
Y_RUND = TIEFE - R               # Mittelpunkt der Frontrundung
BR = B_BREITE / 2
B_Y_RUND = B_TIEFE - BR          # = Y_RUND, beide konzentrisch, hinten bündig
BIG = 400.0


def dform(r, z, y0=0.0, y_rund=None):
    """D-Form: hinten gerade bei y0, vorne Halbkreis um (0, y_rund)."""
    yr = Y_RUND if y_rund is None else y_rund
    return (cq.Workplane("XY").workplane(offset=z)
            .moveTo(-r, y0).lineTo(r, y0).lineTo(r, yr)
            .threePointArc((0, yr + r), (-r, yr)).close())


def loft(r0, z0, r1, z1, y0=0.0):
    a = dform(r0, z0, y0).val()
    b = dform(r1, z1, y0).val()
    return cq.Workplane("XY").add(cq.Solid.makeLoft([a, b], True))


def hex_loecher(z, hoehe, r_feld, y0_feld):
    px = HEX_LOCH + HEX_STEG
    py = px * math.sqrt(3) / 2
    rc = HEX_LOCH / math.sqrt(3)
    proto = (cq.Workplane("XY").workplane(offset=z)
             .polyline([(rc * math.cos(math.radians(90 + 60 * k)),
                         rc * math.sin(math.radians(90 + 60 * k))) for k in range(6)])
             .close().extrude(hoehe).val())
    solids = []
    for j in range(-1, int(TIEFE / py) + 2):
        for i in range(-int(R / px) - 1, int(R / px) + 2):
            cx = i * px + (px / 2 if j % 2 else 0)
            solids.append(proto.translate(cq.Vector(cx, j * py, 0)))
    feld = dform(r_feld, z - 0.5, y0_feld).extrude(hoehe + 1.0)
    return cq.Workplane("XY").add(cq.Compound.makeCompound(solids)).intersect(feld)


# =============== Behälter ===============
def behaelter():
    aussen = dform(BR, 0, 0, B_Y_RUND).extrude(B_HOEHE)
    innen = dform(BR - B_WAND, B_BODEN, B_WAND, B_Y_RUND).extrude(B_HOEHE)
    t = aussen.cut(innen)
    # Griffmulde vorne
    griff = (cq.Workplane("XY").workplane(offset=B_HOEHE - 8.0)
             .center(0, B_TIEFE).circle(GRIFF_R).extrude(9.0))
    return t.cut(griff)


# =============== Gitter ===============
def gitter():
    r_top = R - SCHRAEGE
    aussen = loft(R, 0, r_top, HOEHE)
    innen = loft(R - WAND, -0.01, r_top - WAND, HOEHE - PLATTE)
    # nach hinten offen: Innenraum bis über die Hinterkante verlängern
    innen = innen.union(
        cq.Workplane("XY").box(2 * (R - WAND), 6.0, HOEHE - PLATTE + 0.01,
                               centered=(True, False, False))
        .translate((0, -6.0, -0.01)))
    korpus = aussen.cut(innen)

    # Lippe: greift in die Behälter-Mündung
    z_pl = HOEHE - PLATTE                    # Unterseite Deckplatte
    z_l0 = z_pl - ((z_pl) - (B_HOEHE - LIPPE_EINTAUCH))   # = B_HOEHE - Eintauchtiefe
    l_aussen_r = BR - B_WAND - SPIEL
    l_innen_r = l_aussen_r - LIPPE_WAND
    y_l = B_WAND + SPIEL
    lippe = (dform(l_aussen_r, z_l0, y_l, B_Y_RUND).extrude(z_pl - z_l0 + 0.01)
             .cut(dform(l_innen_r, z_l0 - 0.1, y_l + LIPPE_WAND, B_Y_RUND)
                  .extrude(z_pl - z_l0 + 0.3)))
    teil = korpus.union(lippe)

    # Hexagon-Feld in der Deckplatte, innerhalb der Lippe
    r_feld = l_innen_r - 0.8
    teil = teil.cut(hex_loecher(z_pl - 0.5, PLATTE + 1.0, r_feld, y_l + LIPPE_WAND + 0.8))
    return teil


if __name__ == "__main__":
    g, b = gitter(), behaelter()
    for name, t in (("gitter", g), ("behaelter", b)):
        cq.exporters.export(t, f"dedica_lowprofile_{name}.step")
        cq.exporters.export(t, f"dedica_lowprofile_{name}.stl",
                            tolerance=0.02, angularTolerance=0.1)
        v = t.val(); bb = v.BoundingBox()
        print(f"{name}: valid={v.isValid()} vol={v.Volume():.0f} mm3 "
              f"bbox={bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}")
    ueber = g.val().intersect(b.val()).Volume()
    print(f"Überschneidung Gitter/Behälter: {ueber:.2f} mm3 (soll 0 sein)")
    cq.exporters.export(cq.Workplane().add(g.val()).add(b.val()),
                        "dedica_lowprofile_montage.stl", tolerance=0.05)
