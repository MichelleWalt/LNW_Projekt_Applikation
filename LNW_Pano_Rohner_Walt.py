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

bilder_pro_sekunde = 60                 #Animation läuft wie flüssig
ziel_dauer = 12                         #Programm dauert max. 12 Sekunden

zeit = 0                                #Aktuelle Zeit in der Animation
laeuft = False                          #schaut, ob Animation gerade läuft
loesung_zeigen = False                  #schaut, ob Vorhersage im Diagramm sichtbar ist
aktiver_regler = None                   #Merkt, welcher Regler mit der Maus gezogen wird
meldung = ""                            #speichert den Text, wenn A, B eingeholt hat

blau = (50, 100, 220)                   #Farbe für Läufer A
gruen = (50, 160, 70)                   #Farbe für Läufer B

regler_start = 250                      #Koordinate, wo die Regler-Linien starten
regler_ende = 620                       #Koordinate, wo die Regler-Linie stoppt

#-----------------------------
#Darstellung
#-----------------------------
bahn_start = 150  # x-Position (Pixel), wo die Laufbahn beginnt
bahn_ende = 900  # x-Position (Pixel), wo die Laufbahn endet
faktor = 7  # 1 Meter = 7 Pixel auf dem Bildschirm


def titel_zeichnen():  # Funktion für die Überschrift
    py5.fill(30)  # Textfarbe: fast schwarz
    py5.text_size(28)  # Schriftgröße 28
    py5.text("Einholproblem: Wer holt wen ein?", 40, 45)  # Titel an Position (40, 45) schreiben


def laufbahn_zeichnen(strecke_a, strecke_b):  # Funktion für Bahnen und Läufer, bekommt die Strecken
    py5.fill(30)  # Textfarbe: fast schwarz
    py5.text_size(18)  # Schriftgröße 18
    py5.text("Läufer A", 40, 130)  # Beschriftung links neben Bahn A
    py5.text("Läufer B", 40, 210)  # Beschriftung links neben Bahn B

    py5.stroke(180)  # Linienfarbe: hellgrau
    py5.stroke_weight(2)  # Liniendicke: 2 Pixel
    py5.line(bahn_start, 125, bahn_ende, 125)  # Bahn A als waagrechte Linie bei y = 125
    py5.line(bahn_start, 205, bahn_ende, 205)  # Bahn B als waagrechte Linie bei y = 205

    x_a = bahn_start + strecke_a * faktor  # Position von A: Meter in Pixel umrechnen
    x_b = bahn_start + strecke_b * faktor  # Position von B: Meter in Pixel umrechnen

    py5.no_stroke()  # Kreise ohne Umrandung zeichnen
    py5.fill(50, 100, 220)  # Füllfarbe blau (Rot, Grün, Blau)
    py5.circle(x_a, 125, 30)  # Läufer A als Kreis, Durchmesser 30

    py5.fill(50, 160, 70)  # Füllfarbe grün
    py5.circle(x_b, 205, 30)  # Läufer B als Kreis, Durchmesser 30


def werte_anzeigen(strecke_a, strecke_b):  # Funktion für die Zahlen unter den Bahnen
    py5.fill(30)  # Textfarbe: fast schwarz
    py5.text_size(18)  # Schriftgröße 18
    py5.text("Zeit: " + str(round(zeit, 1)) + " s", 150, 280)  # Zeit, auf 1 Nachkommastelle gerundet
    py5.text("Distanz A: " + str(round(strecke_a, 1)) + " m", 400, 280)  # Strecke von A
    py5.text("Distanz B: " + str(round(strecke_b, 1)) + " m", 650, 280)  # Strecke von B


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


#-----------------------------
#Hauptprogramm
#-----------------------------
def setup():
    py5.size(1000,450)      #Fenster ist 1000 Pixel breit und 450 Pixel hoch

def draw():
    py5.background(250)                                 #weisser Hintergrund
    zeit_aktualisieren()                                #zeit weiterzählen  (Teil: Feste Werte und Berechnungen)
    strecke_a, strecke_b = strecken_berechnen()         #aktuelle Strecke holen (Teil: Feste Werte und Berechnungen)
    titel_zeichnen()                                    #Überschrift
    laufbahn_zeichnen(strecke_a, strecke_b)             #Bahnen und Läufer
    werte_anzeigen(strecke_a, strecke_b)                #Zahlen zeigen
    buttons_zeichnen()                                  #Buttons

py5.run_sketch()


