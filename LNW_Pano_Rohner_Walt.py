import py5
#-----------------------------
#Berechnungen
#-----------------------------

def strecke(zeit, tempo, vorsprung=0):          #Berechnet Distanz zu einem bestimmten Zeitpunkt
    return vorsprung + (tempo * zeit)           #Formel: Vorsprung + (v * t)

def schoene_schrittweite(maximum):              #Bestimmt Abstände für Diagramm-Striche
    if maximum <= 20: return 2                  #Bei kurzen Distanzen oder Zeiten: 2er-Schritte
    elif maximum <= 50: return 5                #Bei mittleren: 5er-Schritte
    elif maximum <=100: return 10               #Bei grossen: 10er-Schritte
    elif maximum <= 200: return 20              #Bei noch grösseren: 20er-Schritte
    return 50                                   #Ganz grosse Werte: 50er-Schritte

def einholpunkt(tempo_a, tempo_b, vorsprung_b):         #Berechnet, wann und wo A, B einholt
    if tempo_a <= tempo_b:                              #Wenn A nicht schneller als B ist...
        return None                                     #...dann gibt es keinen Einholpunkt
    zeit_t = vorsprung_b / (tempo_a - tempo_b)          #Zeit berechnen: Vorsprung / durch Tempounterschied
    ort_t = strecke(zeit_t, tempo_a)                    #Ort berechnen: Zeit * Tempo von A
    return (zeit_t, ort_t)                              #Gibt Zeit und Ort zurück

def achsen_maximum(wert):                               #Rundet Achsen-Ende auf
    schritt = schoene_schrittweite(wert)                #Holt sich passende Schrittweite
    return int((wert / schritt) + 1) * schritt          #Berechent nächstes Vielfache dieser Schrittweite

#-----------------------------
#Einstellungen
#-----------------------------

BILDER_PRO_SEKUNDE = 60                 #Animation läuft wie flüssig
ZIEL_DAUER = 12                         #Programm dauert max. 12 Sekunden

zeit = 0                                #Aktuelle Zeit in der Animation
laeuft = False                          #schaut, ob Animation gerade läuft
loesung_zeigen = False                  #schaut, ob Vorhersage im Diagramm sichtbar ist
aktiver_regler = None                   #Merkt, welcher Regler mit der Maus gezogen wird
meldung = ""                            #speichert den Text, wenn A, B eingeholt hat

blau = (50, 100, 220)                   #Farbe für Läufer A
gruen = (50, 160, 70)                   #Farbe für Läufer B

regler_start = 250                      #Koordinate, wo die Regler-Linien starten
regler_ende = 620                       #Koordinate, wo die Regler-Linie stoppt

# Einstellungen der drei Schieberegler
regler = [
    {"text": "Tempo Läufer A (m/s)", "y": 680, "min": 1, "max": 8, "wert": 4.4, "schritt": 0.1},
    {"text": "Tempo Läufer B (m/s)", "y": 730, "min": 1, "max": 8, "wert": 3.1, "schritt": 0.1},
    {"text": "Startvorsprung B (m)", "y": 780, "min": 0, "max": 30, "wert": 14, "schritt": 1},
]

# Position und Grösse der Laufbahn und des Diagramms
bahn = {"x": 150, "breite": 750, "y_a": 125, "y_b": 195}
diagramm = {"x": 150, "y": 560, "breite": 750, "hoehe": 270}

# Position und Grösse der Buttons
button_start = (780, 660, 170, 45)
button_reset = (780, 720, 170, 45)
button_loesung = (780, 780, 170, 45)

# Aktuelle Werte der Schieberegler abrufen
def tempo_a():
    return regler[0]["wert"]

def tempo_b():
    return regler[1]["wert"]

def vorsprung_b():
    return regler[2]["wert"]

# ==============================================================================
# DARSTELLUNG, ZEICHNEN & GRAFIK
# ==============================================================================

def max_strecke():  # Berechnet den Maximalwert für die Y-Achse (Strecke)
    t = max_zeit()  # Holt die maximale Zeit des Diagramms
    weiteste = max(strecke(t, tempo_a()), strecke(t, tempo_b(), vorsprung_b()))  # Wer von beiden ist weiter gelaufen?
    return achsen_maximum(weiteste)  # Rundet diesen Maximalwert schön auf


def teilstriche(maximum):  # Berechnet, wo die Striche im Diagramm hinkommen
    schritt = schoene_schrittweite(maximum)  # Holt die optimale Schrittweite
    return [i * schritt for i in range(int(round(maximum / schritt)) + 1)]  # Erstellt eine Liste (0, 10, 20, 30...)


def zahl_text(wert): return format(wert, "g")  # Hilfsfunktion, um Zahlen ohne unnötige Nullstellen anzuzeigen


def draw():  # Haupt-Zeichenschleife, läuft 60x pro Sekunde
    zeit_weiterzaehlen()  # (Person 3) Zeit einen Schritt weitersetzen
    py5.background(250)  # Hintergrund hellgrau füllen (löscht altes Bild)
    py5.fill(30)  # Dunkle Schriftfarbe
    py5.text_size(28)  # Grosse Schrift
    py5.text("Einholproblem: Wann holt A den Läufer B ein?", 40, 45)  # Haupttitel zeichnen
    laufbahn_zeichnen()  # Funktion aufrufen: Laufbahnen zeichnen
    diagramm_zeichnen()  # Funktion aufrufen: Weg-Zeit-Diagramm zeichnen
    werte_zeichnen()  # Funktion aufrufen: Zahlen & Texte zeichnen
    for r in regler: regler_zeichnen(r)  # Funktion aufrufen: Alle Regler zeichnen
    buttons_zeichnen()  # Funktion aufrufen: Alle Buttons zeichnen


def bahn_x(meter):  # Rechnet eine Distanz (Meter) in eine X-Koordinate (Pixel) um
    return bahn["x"] + meter / max_strecke() * bahn["breite"]  # Startposition + (Prozentualer Anteil * Bahnbreite)


def laufbahn_zeichnen():  # Zeichnet den oberen Bereich (Läufer)
    py5.fill(30);
    py5.text_size(18)  # Textfarbe und -grösse
    py5.text("Läufer A", 40, bahn["y_a"] + 6)  # Beschriftung Bahn A
    py5.text("Läufer B", 40, bahn["y_b"] + 6)  # Beschriftung Bahn B

    py5.stroke(180);
    py5.stroke_weight(2)  # Hellgraue Linien, 2 Pixel dick
    py5.line(bahn["x"], bahn["y_a"], bahn["x"] + bahn["breite"], bahn["y_a"])  # Linie für Bahn A
    py5.line(bahn["x"], bahn["y_b"], bahn["x"] + bahn["breite"], bahn["y_b"])  # Linie für Bahn B

    py5.text_size(12)  # Kleinere Schrift für die Meter-Markierungen
    for meter in teilstriche(max_strecke()):  # Geht jeden Teilstrich durch (0, 10, 20...)
        x = bahn_x(meter)  # Wo liegt das auf dem Bildschirm?
        py5.stroke(200)  # Helles Grau für Markierungslinien
        py5.line(x, bahn["y_b"] + 18, x, bahn["y_b"] + 24)  # Kurze Linie unterhalb der Bahn
        py5.fill(120);
        py5.text_align(py5.CENTER)  # Graue, zentrierte Schrift
        py5.text(zahl_text(meter) + " m", x, bahn["y_b"] + 38)  # Meter-Zahl schreiben
    py5.text_align(py5.LEFT, py5.BASELINE)  # Ausrichtung wieder zurücksetzen

    punkt = einholpunkt(tempo_a(), tempo_b(), vorsprung_b())  # Treffpunkt berechnen
    if punkt is not None and (loesung_zeigen or zeit >= punkt[0]):  # Wenn Lösung an ist ODER Treffpunkt erreicht wurde:
        x = bahn_x(punkt[1])  # Pixel-Position der Ziellinie
        py5.stroke(220, 60, 60);
        py5.stroke_weight(2)  # Rot, 2 Pixel dick
        gestrichelte_linie(x, bahn["y_a"] - 25, x, bahn["y_b"] + 15)  # Vertikale rote Ziellinie zeichnen

    laeufer_zeichnen(bahn_x(strecke(zeit, tempo_a())), bahn["y_a"], blau,
                     "A")  # Läufer A an aktueller Position zeichnen
    laeufer_zeichnen(bahn_x(strecke(zeit, tempo_b(), vorsprung_b())), bahn["y_b"], gruen, "B")  # Läufer B zeichnen


def laeufer_zeichnen(x, y, farbe, name):  # Zeichnet einen einzelnen Läuferkreis
    py5.no_stroke();
    py5.fill(*farbe)  # Keine Umrandung, füllen mit der RGB-Farbe des Läufers
    py5.circle(x, y, 30)  # Kreis zeichnen, Durchmesser 30
    py5.fill(255);
    py5.text_size(15)  # Weisse Schrift
    py5.text_align(py5.CENTER, py5.CENTER)  # Zentriert im Kreis
    py5.text(name, x, y - 1)  # Buchstabe A oder B reinschreiben
    py5.text_align(py5.LEFT, py5.BASELINE)  # Ausrichtung zurücksetzen


def zu_pixel(t, s):  # Rechnet einen Punkt im Diagramm (Zeit, Strecke) in Pixel um
    x = diagramm["x"] + t / max_zeit() * diagramm["breite"]  # Anteil der Zeit * Breite des Diagramms
    y = diagramm["y"] - s / max_strecke() * diagramm["hoehe"]  # Anteil der Strecke * Höhe (Y geht nach oben!)
    return x, y  # Gibt X und Y Koordinate zurück


def diagramm_zeichnen():  # Zeichnet das gesamte Weg-Zeit-Diagramm
    dx, dy = diagramm["x"], diagramm["y"]  # Startpunkte (unten links) zur Übersicht speichern

    py5.stroke_weight(1);
    py5.text_size(13)  # Dünne Linien für Raster, kleine Schrift
    for t in teilstriche(max_zeit()):  # Vertikale Linien (Zeitachse)
        x, _ = zu_pixel(t, 0)  # Pixel-X berechnen
        py5.stroke(225);
        py5.line(x, dy, x, dy - diagramm["hoehe"])  # Graue Rasterlinie nach oben
        py5.fill(80);
        py5.text_align(py5.CENTER)  # Textfarbe, zentriert
        py5.text(zahl_text(t), x, dy + 18)  # Zeit-Beschriftung schreiben

    for s in teilstriche(max_strecke()):  # Horizontale Linien (Streckenachse)
        _, y = zu_pixel(0, s)  # Pixel-Y berechnen
        py5.stroke(225);
        py5.line(dx, y, dx + diagramm["breite"], y)  # Graue Rasterlinie nach rechts
        py5.fill(80);
        py5.text_align(py5.RIGHT, py5.CENTER)  # Textfarbe, rechtsbündig
        py5.text(zahl_text(s), dx - 8, y)  # Strecken-Beschriftung schreiben
    py5.text_align(py5.LEFT, py5.BASELINE)  # Ausrichtung zurücksetzen

    py5.stroke(50);
    py5.stroke_weight(2)  # Dunkle, dickere Linien für die Hauptachsen
    py5.line(dx, dy, dx + diagramm["breite"], dy)  # X-Achse (Zeit) zeichnen
    py5.line(dx, dy, dx, dy - diagramm["hoehe"])  # Y-Achse (Strecke) zeichnen

    py5.fill(30);
    py5.text_size(15)  # Achsenbeschriftungen:
    py5.text("Zeit t (s)", dx + diagramm["breite"] - 60, dy + 38)
    py5.text("Strecke s (m)", 40, dy - diagramm["hoehe"] - 12)

    if loesung_zeigen:  # Wenn Vorhersage aktiv ist:
        gerade_zeichnen(max_zeit(), tempo_a(), 0, blau, 60)  # Zeichne Linie von A bis zum Ende (transparent)
        gerade_zeichnen(max_zeit(), tempo_b(), vorsprung_b(), gruen, 60)  # Zeichne Linie von B bis zum Ende

    gerade_zeichnen(zeit, tempo_a(), 0, blau, 255)  # Zeichne dicke Linie von A bis zur aktuellen Zeit
    gerade_zeichnen(zeit, tempo_b(), vorsprung_b(), gruen, 255)  # Zeichne dicke Linie von B bis zur aktuellen Zeit

    einholpunkt_zeichnen()  # Zeichne den Schnittpunkt (falls erreicht/Lösung aktiv)


def gerade_zeichnen(t_ende, tempo, vorsprung, farbe, deckkraft):  # Hilfsfunktion für Linien im Diagramm
    py5.stroke(*farbe, deckkraft);
    py5.stroke_weight(3)  # Setzt Farbe, Deckkraft und Dicke
    py5.line(*zu_pixel(0, vorsprung), *zu_pixel(t_ende, strecke(t_ende, tempo, vorsprung)))  # Verbindet Start und Ende


def einholpunkt_zeichnen():  # Zeichnet den roten Punkt und die Hilfslinien
    punkt = einholpunkt(tempo_a(), tempo_b(), vorsprung_b())  # Holt den Treffpunkt
    if punkt is None:  # Wenn es keinen gibt (A ist zu langsam):
        if loesung_zeigen:  # Wenn Lösung zeigen aktiv ist:
            py5.fill(200, 60, 60);
            py5.text_size(16)  # Roter Warntext
            py5.text("Die Geraden schneiden sich nicht: A holt B nie ein.", diagramm["x"] + 20,
                     diagramm["y"] - diagramm["hoehe"] + 20)
        return
    if not (loesung_zeigen or zeit >= punkt[
        0]): return  # Nichts zeichnen, wenn Punkt noch nicht erreicht und Lösung aus

    t, s = punkt;
    x, y = zu_pixel(t, s)  # Koordinaten entpacken und in Pixel umwandeln
    py5.stroke(220, 60, 60);
    py5.stroke_weight(1.5)  # Rote, dünne Linie
    gestrichelte_linie(x, y, x, diagramm["y"])  # Hilfslinie runter zur Zeitachse
    gestrichelte_linie(x, y, diagramm["x"], y)  # Hilfslinie rüber zur Streckenachse

    py5.no_stroke();
    py5.fill(220, 60, 60)  # Roter Kreis
    py5.circle(x, y, 12)  # Zeichnet Schnittpunkt

    py5.text_size(15);
    beschriftung = f"t = {t:.1f} s,  s = {s:.1f} m"  # Erstellt Text für Schnittpunkt
    if x > diagramm["x"] + diagramm["breite"] - 220:  # Wenn der Punkt zu weit rechts ist (droht rauszurutschen):
        py5.text_align(py5.RIGHT);
        py5.text(beschriftung, x - 12, y + 26);
        py5.text_align(py5.LEFT, py5.BASELINE)
    else:  # Sonst normal rechts daneben schreiben:
        py5.text(beschriftung, x + 12, y + 26)


def gestrichelte_linie(x1, y1, x2, y2, strich=6):  # Zeichnet eine gestrichelte Linie
    laenge = py5.dist(x1, y1, x2, y2)  # Berechnet Gesamtlänge
    if laenge == 0: return  # Verhindert Fehler, wenn Linie 0 lang ist
    anzahl = int(laenge / strich)  # Wie viele Striche passen rein?
    for i in range(0, anzahl, 2):  # Geht jeden zweiten Abschnitt durch
        a = i / anzahl;
        b = min(i + 1, anzahl) / anzahl  # Prozentuale Start- und Endpunkte des Strichs
        py5.line(py5.lerp(x1, x2, a), py5.lerp(y1, y2, a), py5.lerp(x1, x2, b), py5.lerp(y1, y2, b))  # Zeichnet ihn


def werte_zeichnen():  # Zeichnet die Textwerte (Zeit, Distanz) mittig auf den Screen
    py5.fill(30);
    py5.text_size(17);
    y = 625  # Setzt Farbe, Grösse und Y-Position
    py5.text(f"Zeit: {zeit:.1f} s", 40, y)  # Schreibt die Zeit
    py5.fill(*blau);
    py5.text(f"Distanz A: {strecke(zeit, tempo_a()):.1f} m", 220, y)  # Schreibt Strecke A (in Blau)
    py5.fill(*gruen);
    py5.text(f"Distanz B: {strecke(zeit, tempo_b(), vorsprung_b()):.1f} m", 430, y)  # Strecke B (Grün)

    if zeitraffer() > 1:  # Wenn Zeitraffer aktiv ist:
        py5.fill(120);
        py5.text_size(14)
        py5.text(f"Zeitraffer x{zeitraffer()}", 640, y)  # ...schreibe die Geschwindigkeit dazu

    if meldung:  # Wenn es eine Sieges- oder Verlierermeldung gibt:
        py5.fill(200, 60, 60);
        py5.text_size(18)
        py5.text(meldung, 400, 80)  # ...schreibe sie ganz oben in Rot


def regler_position(r):  # Rechnet den Wert eines Reglers in seine Pixelposition um
    return py5.remap(r["wert"], r["min"], r["max"], regler_start, regler_ende)


def regler_zeichnen(r):  # Zeichnet einen Schieberegler
    grau = 170 if regler_gesperrt() else 30  # Farbe wird blass, wenn die Animation läuft (gesperrt)

    py5.fill(grau);
    py5.text_size(16)  # Textfarbe und Grösse
    py5.text(r["text"], 40, r["y"] + 5)  # Beschriftung des Reglers

    py5.stroke(200 if regler_gesperrt() else 150)  # Linienfarbe des Reglers (heller, wenn gesperrt)
    py5.stroke_weight(4);
    py5.line(regler_start, r["y"], regler_ende, r["y"])  # Zeichnet die Führungslinie

    py5.no_stroke();
    py5.fill(grau if regler_gesperrt() else 40)  # Farbe des Anfasserkreises
    py5.circle(regler_position(r), r["y"], 22)  # Zeichnet den runden Anfasser an der korrekten Position

    py5.fill(grau);
    py5.text(format(r["wert"], ".1f"), 640, r["y"] + 5)  # Schreibt den Zahlenwert rechts daneben

    if regler_gesperrt() and r is regler[0]:  # Zeigt beim obersten Regler einen Hinweis, falls blockiert:
        py5.fill(150);
        py5.text_size(13)
        py5.text("Zum Ändern zuerst pausieren", regler_start, r["y"] - 18)


def buttons_zeichnen():  # Entscheidet, welche Buttons gerade sichtbar sein sollen
    if laeuft:
        button_zeichnen(button_start, "Pause", (70, 170, 90))  # Animation läuft -> "Pause" zeigen
    elif zeit >= max_zeit():
        button_zeichnen(button_start, "Nochmals", (70, 170, 90))  # Ende erreicht -> "Nochmals" zeigen
    elif zeit > 0:
        button_zeichnen(button_start, "Weiter", (70, 170, 90))  # Pausiert -> "Weiter" zeigen
    else:
        button_zeichnen(button_start, "Start", (70, 170, 90))  # Steht am Anfang -> "Start" zeigen

    button_zeichnen(button_reset, "Zurücksetzen", (200, 200, 200))  # Zeichnet den Reset-Button

    if loesung_zeigen:
        button_zeichnen(button_loesung, "Lösung verbergen", (240, 190, 190))  # Lösung ist an -> "verbergen"
    else:
        button_zeichnen(button_loesung, "Lösung zeigen", (240, 190, 190))  # Lösung ist aus -> "zeigen"


def button_zeichnen(button, text, farbe):  # Malt einen Button auf den Schirm
    x, y, breite, hoehe = button  # Entpackt die Koordinaten
    py5.no_stroke()
    if ist_ueber(button):
        py5.fill(*[max(0, f - 25) for f in farbe])  # Macht den Button beim Hovern leicht dunkler
    else:
        py5.fill(*farbe)  # Ansonsten normale Farbe
    py5.rect(x, y, breite, hoehe, 8)  # Zeichnet Rechteck mit 8px Abrundung

    py5.fill(30);
    py5.text_size(17)  # Textfarbe dunkelgrau
    py5.text_align(py5.CENTER, py5.CENTER)  # Text im Button zentrieren
    py5.text(text, x + breite / 2, y + hoehe / 2)  # Text schreiben
    py5.text_align(py5.LEFT, py5.BASELINE)  # Ausrichtung zurücksetzen


py5.run_sketch()  # Startet das Py5 Fenster

#-----------------------------
#Bedienung inkl. Buttons
#-----------------------------
button_start = (150, 330, 160, 45)  # Start/Pause-Button: (x, y, Breite, Höhe)
button_reset = (330, 330, 160, 45)  # Zurücksetzen-Button: (x, y, Breite, Höhe)


def button_zeichnen(button, text, farbe):  # zeichnet einen Button mit Text und Farbe
    x, y, breite, hoehe = button  # Tupel in vier einzelne Variablen auspacken
    py5.no_stroke()  # keine Umrandung
    py5.fill(*farbe)  # Füllfarbe; * verteilt (R, G, B) auf drei Werte
    py5.rect(x, y, breite, hoehe, 8)  # Rechteck mit abgerundeten Ecken (Radius 8)
    py5.fill(30)  # Textfarbe: fast schwarz
    py5.text_size(18)  # Schriftgröße 18
    py5.text_align(py5.CENTER, py5.CENTER)  # Text waagrecht und senkrecht zentrieren
    py5.text(text, x + breite / 2, y + hoehe / 2)  # Text in die Mitte des Buttons schreiben
    py5.text_align(py5.LEFT, py5.BASELINE)  # Ausrichtung zurücksetzen, damit andere Texte stimmen


def buttons_zeichnen():  # zeichnet beide Buttons
    if laeuft:  # wenn die Animation läuft ...
        button_zeichnen(button_start, "Pause", (70, 170, 90))  # ... steht "Pause" auf dem Button
    else:  # sonst ...
        button_zeichnen(button_start, "Start", (70, 170, 90))  # ... steht "Start" darauf
    button_zeichnen(button_reset, "Zurücksetzen", (200, 200, 200))  # grauer Reset-Button


def ist_ueber(button):  # prüft, ob die Maus über einem Button ist
    x, y, breite, hoehe = button  # Tupel auspacken
    return x < py5.mouse_x < x + breite and y < py5.mouse_y < y + hoehe  # True, wenn Maus im Rechteck


def mouse_pressed():  # wird von py5 bei jedem Mausklick automatisch aufgerufen
    global laeuft  # globale Variable "laeuft" verändern dürfen
    global zeit  # globale Variable "zeit" verändern dürfen
    if ist_ueber(button_start):  # Klick auf Start/Pause?
        laeuft = not laeuft  # umschalten: True wird False und umgekehrt
    if ist_ueber(button_reset):  # Klick auf Zurücksetzen?
        zeit = 0  # Zeit auf 0 zurück
        laeuft = False  # Animation anhalten



