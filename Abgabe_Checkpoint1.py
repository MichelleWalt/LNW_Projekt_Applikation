import py5
#-----------------------------
#Feste Werte und Berechnungen
#-----------------------------
tempo_a = 4.5       # m/s
tempo_b = 3.5       # m/s
vorsprung_b = 14    # m

zeit = 0            #vergangene Zeit in s
laueft = False      #läuft die Animation gerade?

def zeit_aktualisieren():       #Funktion, welche die Zeit weiterzählt
    global zeit                 #globale Variable "zeit" verändern dürfen
    if laeuft:                  #nur wenn Animation gerade läuft
        zeit = zeit + 1 / 60    #Bild = 1/60 s dazuzählen (60 Bilder pro sekunde)

def strecken_berechnen():                         #Funktion, welche die zurückgelegte Strecke n berechnet
    strecke_a = tempo_a * zeit                    #Strecke A: s = v * t
    strecke_b = vorsprung_b + tempo_b * zeit      #Strecke B: Vorsprung + (v * t)
    return strecke_a, strecke_b                   #beide Werte an draw() zurückgeben

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



#-----------------------------
#Hauptprogramm
#-----------------------------
def setup():
    py5.size(1000,450)      #Fenster ist 1000 Pixel breit und 450 Pixel hoch

def draw():
    py5.background(250)                                 #weisser Hintergrund
    zeit_aktualisieren()                                #zeit weiterzählen  (Teil: Feste Werte und Berechnungen)
    strecke_a, strecke_b = strecken_berechnen()         #aktuelle Strecke holen (Teil: Feste Werte und Berechnungen)


py5.run_sketch()


