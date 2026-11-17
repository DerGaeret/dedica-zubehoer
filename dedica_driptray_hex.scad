// =====================================================================
//  DeLonghi Dedica – Abtropfgitter / Driptray-Einsatz mit Hexagon-Muster
// ---------------------------------------------------------------------
//  Der Einsatz wird in die schwarze Mulde der Abtropfschale gelegt.
//  Seine Oberseite liegt bündig mit der Kante, an der das schwarze
//  Kunststoffteil in das graue Gehäuse übergeht.
//
//  ALLE MASSE SIND SCHÄTZWERTE AUS DEM FOTO -> bitte nachmessen!
//    mulde_breite  : Innenbreite der Mulde (links <-> rechts)
//    mulde_tiefe   : Innentiefe der Mulde (hinten <-> vorderster Punkt)
//    hoehe         : vom Boden der Mulde bis zur Kante schwarz/grau
//  Danach in OpenSCAD F6 + "Export as STL".
// =====================================================================

/* [Mulde (nachmessen!)] */
mulde_breite   = 110;   // mm
mulde_tiefe    = 100;   // mm
hoehe          = 18;    // mm, Muldenboden bis Kante schwarz/grau
eckradius_hinten = 8;   // mm, Radius der hinteren Ecken der Mulde
spiel          = 0.6;   // mm Luft pro Seite, damit er leicht reinpasst

/* [Gitter] */
platte_dicke   = 2.4;   // mm, Stärke der Deckplatte
rand_breite    = 4;     // mm, geschlossener Rand um das Muster
hex_loch       = 7;     // mm, Lochgröße (Schlüsselweite)
hex_steg       = 1.8;   // mm, Stegbreite zwischen den Löchern

/* [Unterbau] */
wand_dicke     = 2.0;   // mm, Außenwand
rippe_dicke    = 1.6;   // mm, Stützrippen
rippe_abstand  = 25;    // mm
ablauf_hoehe   = 3;     // mm, Wasserdurchlässe unten in Wand/Rippen
ablauf_breite  = 8;     // mm

/* [Ausgabe] */
druckorientierung = true; // true = Oberseite liegt auf dem Druckbett

$fn = 96;

B = mulde_breite - 2*spiel;
T = mulde_tiefe  - 2*spiel;
R = B/2;                         // Radius der vorderen Rundung

// ---------- 2D-Grundform: hinten gerade, vorne halbrund ----------
// Ursprung: Mitte der Hinterkante, +Y zeigt nach vorne
module grundform(o = 0) {
    offset(delta = o) hull() {
        // hintere Ecken
        for (s = [-1, 1])
            translate([s*(B/2 - eckradius_hinten), eckradius_hinten])
                circle(r = eckradius_hinten);
        // vordere Rundung
        translate([0, T - R]) circle(r = R);
    }
}

// ---------- Hexagon-Lochraster ----------
module hex_raster() {
    pitch_x = hex_loch + hex_steg;              // Abstand in X
    pitch_y = pitch_x * sqrt(3) / 2;            // Zeilenabstand
    d_ecke  = hex_loch / cos(30);               // Eckmaß
    nx = ceil(B / pitch_x) + 2;
    ny = ceil(T / pitch_y) + 2;
    for (j = [-1 : ny], i = [-nx/2 - 1 : nx/2 + 1]) {
        x = i * pitch_x + ((j % 2 == 0) ? 0 : pitch_x/2);
        y = j * pitch_y;
        translate([x, y]) rotate(30) circle(d = d_ecke, $fn = 6);
    }
}

module deckplatte() {
    linear_extrude(platte_dicke) difference() {
        grundform();
        intersection() {
            grundform(-rand_breite);
            hex_raster();
        }
    }
}

// Durchlässe unten, damit Wasser in der Mulde frei verteilen kann
module ablauf_schlitze() {
    pitch = 18;
    for (x = [-B : pitch : B])
        translate([x - ablauf_breite/2, -T, -1])
            cube([ablauf_breite, 3*T, ablauf_hoehe + 1]);
    for (y = [-T : pitch : 2*T])
        translate([-B, y - ablauf_breite/2, -1])
            cube([2*B, ablauf_breite, ablauf_hoehe + 1]);
}

module unterbau() {
    unter_h = hoehe - platte_dicke;
    difference() {
        union() {
            // Außenwand
            linear_extrude(unter_h) difference() {
                grundform();
                grundform(-wand_dicke);
            }
            // Stützrippen (Kreuzraster) innerhalb der Form
            linear_extrude(unter_h) intersection() {
                grundform(-wand_dicke/2);
                union() {
                    for (x = [-B : rippe_abstand : B])
                        translate([x - rippe_dicke/2, -1]) square([rippe_dicke, T + 2]);
                    for (y = [rippe_abstand : rippe_abstand : T])
                        translate([-B, y - rippe_dicke/2]) square([2*B, rippe_dicke]);
                }
            }
        }
        ablauf_schlitze();
    }
}

module einsatz() {
    // Gebrauchslage: Unterbau unten, Deckplatte oben
    unterbau();
    translate([0, 0, hoehe - platte_dicke]) deckplatte();
}

if (druckorientierung)
    translate([0, 0, hoehe]) mirror([0, 0, 1]) einsatz();   // Deckplatte aufs Bett
else
    einsatz();
