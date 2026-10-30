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


