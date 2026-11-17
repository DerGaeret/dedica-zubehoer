// =====================================================================
//  DeLonghi Dedica (EC680 / EC685 / EC885) – Abtropfgitter mit Hexagon-Muster
// ---------------------------------------------------------------------
//  Passform aus bestehenden, erprobten Community-Modellen übernommen
//  (Printables 1608242 / 1142660 / 687455, alle basieren auf demselben
//  Original-Gitter):
//    - Grundriss: hinten gerade, vorne halbrund (Mittelpunkt 57,5 mm
//      hinter der Hinterkante)
//    - Deckplatte oben 110,1 x 112,5 mm, Schürze unten 120,5 x 117,7 mm
//    - Gesamthöhe 9 mm, Deckplatte 3 mm, schräge Schürze nach unten
//    - zwei Rastnasen 3 x 20 mm innen links/rechts
//  Neu: Hexagon-Lochmuster über die ganze Fläche.
//
//  "erhoehung" > 0 hebt die Oberseite an (die Schürze wird unten gerade
//  verlängert), falls das Gitter höher bis zur Kante schwarz/grau
//  reichen soll.
// =====================================================================

/* [Passform – aus Referenzmodell] */
r_oben      = 55.03;  // halbe Breite oben (Deckplatte)
r_unten     = 60.25;  // halbe Breite unten (Schürzenkante)
y_rund      = 57.5;   // Abstand Hinterkante -> Mittelpunkt der Rundung
hoehe_ref   = 9;      // Höhe des Originals
platte_dicke = 3;     // Deckplatte
schuerze_wand = 1.4;  // Wandstärke der Schürze (horizontal gemessen)
schuerze_ab_y = 1.0;  // Schürze beginnt 1 mm vor der Hinterkante (hinten offen)

/* [Höhe anpassen] */
erhoehung   = 0;      // mm zusätzlich, z.B. 5 => Oberseite 5 mm höher

/* [Rastnasen] */
nasen       = true;
nase_x_innen = 46.75; // Innenkante der Nase ab Mitte
nase_dicke  = 3;
nase_y      = [27.55, 47.55]; // von/bis ab Hinterkante
nase_z_unten = 1;     // ab Unterkante des Originals

/* [Hexagon-Muster] */
rand_breite = 4;      // geschlossener Rand um das Muster
hex_loch    = 7;      // Schlüsselweite der Löcher
hex_steg    = 1.8;    // Stegbreite

/* [Ausgabe] */
druckorientierung = true; // true = Oberseite liegt auf dem Druckbett

$fn = 128;

H = hoehe_ref + erhoehung;

// D-Form mit halber Breite r; Hinterkante bei y = 0, +Y nach vorne
module dform(r) {
    intersection() {
        hull() {
            translate([-r, 0]) square([2*r, y_rund]);
            translate([0, y_rund]) circle(r = r);
        }
        translate([-200, 0]) square([400, 400]);   // hinten gerade abschneiden
    }
}

// dünne Scheibe der D-Form auf Höhe z
module scheibe(r, z) { translate([0, 0, z]) linear_extrude(0.01) dform(r); }

// Radius der schrägen Außenfläche auf Höhe z (z ab Unterkante Original)
function r_bei(z) = r_unten + (r_oben - r_unten) * z / hoehe_ref;

// Außenkörper (Original-Schräge + gerade Verlängerung nach unten)
module aussen(o = 0) {
    hull() { scheibe(r_unten + o, 0); scheibe(r_oben + o, hoehe_ref - 0.01); }
    if (erhoehung > 0)
        translate([0, 0, -erhoehung]) linear_extrude(erhoehung) dform(r_unten + o);
}

module hex_raster() {
    px = hex_loch + hex_steg;
    py = px * sqrt(3) / 2;
    d  = hex_loch / cos(30);
    for (j = [-1 : ceil(130 / py)], i = [-ceil(70 / px) : ceil(70 / px)])
        translate([i * px + ((j % 2 == 0) ? 0 : px / 2), j * py])
            rotate(30) circle(d = d, $fn = 6);
}

module gitter() {
    z_platte = hoehe_ref - platte_dicke;
    difference() {
        union() {
            // Schürze: Außenkörper minus Innenkörper, hinten offen
            difference() {
                aussen();
                aussen(-schuerze_wand);
                translate([-100, -50, -erhoehung - 1]) cube([200, 50 + schuerze_ab_y, H + 2]);
            }
            // Deckplatte
            intersection() {
                aussen();
                translate([-100, -1, z_platte]) cube([200, 200, platte_dicke]);
            }
            // Rastnasen
            if (nasen) for (s = [-1, 1])
                translate([s > 0 ? nase_x_innen : -nase_x_innen - nase_dicke,
                           nase_y[0], nase_z_unten])
                    cube([nase_dicke, nase_y[1] - nase_y[0], z_platte - nase_z_unten + 0.01]);
        }
        // Hexagon-Löcher in der Deckplatte
        translate([0, 0, hoehe_ref - platte_dicke - 1])
            linear_extrude(platte_dicke + 2)
                intersection() {
                    offset(delta = -rand_breite) dform(r_oben);
                    hex_raster();
                }
    }
}

if (druckorientierung)
    translate([0, 0, hoehe_ref]) mirror([0, 0, 1]) gitter();  // Deckplatte aufs Bett
else
    translate([0, 0, erhoehung]) gitter();
