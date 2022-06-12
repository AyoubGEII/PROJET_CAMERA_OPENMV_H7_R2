#------------------------- ENVOIE DE MAIL EN FONCTION D'UN SUIVIE DE COULEUR --------------------------------

#--------------------------------------- CODE PAR OUENZERFI A. ----------------------------------------------

#La caméra utilisée a une définition de 320x240 pixels

#Le format LAB est utilisé pour la reconnaissance des couleurs, le L correspondant à la luminosité et
#le A et B à des valeurs spécifiques à chaque couleur par rapport à un spectre circulaire défini

#-----------------------------------------IMPORTATION DES LIBRAIRIES------------------------------------------

import time, sensor, image
from pyb import Pin, Timer,

#--------------------------------INITIALISATION DU TIMER ET DE LA CAMERA------------------------


tim = Timer(4, freq=1000) # Timer qui me sert à fabriquer le signal PWM
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # doit être désactivé pour le suivi de couleurs
sensor.set_auto_whitebal(False) # doit être désactivé pour le suivi de couleurs
clock = time.clock()

print("Initialisation de la couleur de fond. Ne rien mettre devant la caméra!")
time.sleep(3) # PERMET D INITIALISER LA COULEUR DE FOND VUE PAR LA CAMERA ET DONC LA LUMINOSITE

#---------------------------- CAPTURE DE LA PREMIERE COULEUR ---------------------------------------------

#Capture les seuils de couleur au format LAB pour l'objet au centre de l'image
r = [(320//2)-(50//2), (240//2)-(50//2), 50, 50] #création d'un rectangle au centre de l'image de 50 de côté

print("CAPTURE DE LA 1ère COULEUR")
print("Mettez le 1er objet dont vous voulez enregistrer la couleur devant la caméra")
print("FAITES EN SORTE QUE L'OBJET SOIT BIEN ENCADRE PAR LE RECTANGLE QUI VA APPARAÎTRE")

for i in range(60):
    img = sensor.snapshot() #la caméra prend une capture de l'environnement et retourne une image en objet
    img.draw_rectangle(r) #le rectangle est dessiné

print("Apprentissage des seuils/thresholds")

threshold = [50,50, 0, 0, 0, 0] #Création d'une liste avec les valeurs médianes pour L, A et B
for i in range(60):
    img = sensor.snapshot()
    hist = img.get_histogram(roi=r) #Création d'un histogramme enregistrant les différentes valeurs L,A et B pour la détermination des seuils
    lo = hist.get_percentile(0.01) #Va permettre d'obtenir les valeurs min des seuils de détection de couleurs (en retournant la valeur qui atteint 1% de la répartition totale de l'histogramme en balayant de gauche à droite)
    hi = hist.get_percentile(0.99) #Va permettre d'obtenir les valeurs max des seuils de détection de couleurs (en retournant la valeur qui atteint 99% de la répartition totale de l'histogramme en balayant de gauche à droite)

    #Nous allons donc définir les valeurs de la liste comme les valeurs min et max des seuils de couleur (une couleur est détectée par la caméra si ses valeurs L,A et B sont comprises entre ces seuils)

    threshold[0] = (threshold[0] + lo.l_value()) // 2 - 20  #Seuil bas pour L (auquel on retire 20 pour un éventail plus large)
    threshold[1] = (threshold[1] + hi.l_value()) // 2 + 20  #Seuil haut pour L (auquel on ajoute 20 pour un éventail plus large)
    threshold[2] = (threshold[2] + lo.a_value()) // 2       #Seuil bas pour A
    threshold[3] = (threshold[3] + hi.a_value()) // 2       #Seuil haut pour A
    threshold[4] = (threshold[4] + lo.b_value()) // 2       #Seuil bas pour B
    threshold[5] = (threshold[5] + hi.b_value()) // 2       #Seuil haut pour B

    for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect()) #création et dessin d'un rectangle encadrant l'objet pour lequel on enregistre la couleur
        img.draw_cross(blob.cx(), blob.cy()) #création et dessin d'une croix au centre de ce rectangle qui définira la position de l'objet
        img.draw_rectangle(r)

print("Seuils appris...")
print("CAPTURE DE LA 2ème COULEUR")

time.sleep(5) #la caméra reste bloquée 5s pour nous laisser le temps de changer d'objet et de vérifier que la capture s'est bien faite

#---------------------------------- CAPTURE DE LA DEUXIEME COULEUR ---------------------------------------------

#Capture les seuils de couleur au format LAB pour l'objet au centre de l'image
r_2 = [(320//2)-(50//2), (240//2)-(50//2), 50, 50] #création d'un rectangle au centre de l'image de 50 de côté

print("Mettez le 2ème objet dont vous voulez enregistrer la couleur devant la caméra")
print("FAITES EN SORTE QUE L'OBJET SOIT BIEN ENCADRE PAR LE RECTANGLE QUI VA APPARAÎTRE")

for i in range(60):
    img = sensor.snapshot() #la caméra prend une capture de l'environnement et retourne une image en objet
    img.draw_rectangle(r_2) #le rectangle est dessiné

print("Apprentissage des seuils/thresholds...")

threshold_2 = [50, 50, 0, 0, 0, 0] #Création d'une liste avec les valeurs médianes pour L, A et B
for i in range(60):
    img = sensor.snapshot()
    hist = img.get_histogram(roi=r_2) #Création d'un histogramme enregistrant les différentes valeurs L,A et B pour la détermination des seuils
    lo = hist.get_percentile(0.01) #Va permettre d'obtenir les valeurs min des seuils de détection de couleurs (en retournant la valeur qui atteint 1% de la répartition totale de l'histogramme en balayant de gauche à droite)
    hi = hist.get_percentile(0.99) #Va permettre d'obtenir les valeurs max des seuils de détection de couleurs (en retournant la valeur qui atteint 99% de la répartition totale de l'histogramme en balayant de gauche à droite)

    #Nous allons donc définir les valeurs de la liste comme les valeurs min et max des seuils de couleur (une couleur est détectée par la caméra si ses valeurs L,A et B sont comprises entre ces seuils)

    threshold_2[0] = (threshold_2[0] + lo.l_value()) // 2 -20   #Seuil bas pour L (auquel on retire 20 pour un éventail plus large)
    threshold_2[1] = (threshold_2[1] + hi.l_value()) // 2 +20   #Seuil haut pour L (auquel on ajoute 20 pour un éventail plus large)
    threshold_2[2] = (threshold_2[2] + lo.a_value()) // 2       #Seuil bas pour A
    threshold_2[3] = (threshold_2[3] + hi.a_value()) // 2       #Seuil haut pour A
    threshold_2[4] = (threshold_2[4] + lo.b_value()) // 2       #Seuil bas pour B
    threshold_2[5] = (threshold_2[5] + hi.b_value()) // 2       #Seuil haut pour B

    for blob in img.find_blobs([threshold_2], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect()) #création et dessin d'un rectangle encadrant l'objet pour lequel on enregistre la couleur
        img.draw_cross(blob.cx(), blob.cy()) #création et dessin d'une croix au centre de ce rectangle qui définira la position de l'objet
        img.draw_rectangle(r_2)

print("Seuils appris...")
print("CAPTURE DE LA 3ème COULEUR ")

time.sleep(5) #la caméra reste bloquée 5s pour nous laisser le temps de changer d'objet et de vérifier que la capture s'est bien faite

#---------------------------------CAPTURE DE LA TROISIEME COULEUR ------------------------------------------------

#Capture les seuils de couleur au format LAB pour l'objet au centre de l'image
r_3 = [(320//2)-(50//2), (240//2)-(50//2), 50, 50] #création d'un rectangle au centre de l'image de 50 de côté

print("Mettez le 3ème objet dont vous voulez enregistrer la couleur devant la caméra")
print("FAITES EN SORTE QUE L'OBJET SOIT BIEN ENCADRE PAR LE RECTANGLE QUI VA APPARAÎTRE")

for i in range(60):
    img = sensor.snapshot() #la caméra prend une capture de l'environnement et retourne une image en objet
    img.draw_rectangle(r_3) #le rectangle est dessiné

print("Apprentissage des seuils/thresholds...")

threshold_3 = [50,50, 0, 0, 0, 0] #Création d'une liste avec les valeurs médianes pour L, A et B
for i in range(60):
    img = sensor.snapshot()
    hist = img.get_histogram(roi=r_3) #Création d'un histogramme enregistrant les différentes valeurs L,A et B pour la détermination des seuils
    lo = hist.get_percentile(0.01) #Va permettre d'obtenir les valeurs min des seuils de détection de couleurs (en retournant la valeur qui atteint 1% de la répartition totale de l'histogramme en balayant de gauche à droite)
    hi = hist.get_percentile(0.99) #Va permettre d'obtenir les valeurs max des seuils de détection de couleurs (en retournant la valeur qui atteint 99% de la répartition totale de l'histogramme en balayant de gauche à droite)

    #Nous allons donc définir les valeurs de la liste comme les valeurs min et max des seuils de couleur (une couleur est détectée par la caméra si ses valeurs L,A et B sont comprises entre ces seuils)

    threshold_3[0] = (threshold_3[0] + lo.l_value()) // 2   #Seuil bas pour L
    threshold_3[1] = (threshold_3[1] + hi.l_value()) // 2   #Seuil haut pour L
    threshold_3[2] = (threshold_3[2] + lo.a_value()) // 2   #Seuil bas pour A
    threshold_3[3] = (threshold_3[3] + hi.a_value()) // 2   #Seuil haut pour A
    threshold_3[4] = (threshold_3[4] + lo.b_value()) // 2   #Seuil bas pour B
    threshold_3[5] = (threshold_3[5] + hi.b_value()) // 2   #Seuil haut pour B

    for blob in img.find_blobs([threshold_3], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect()) #création et dessin d'un rectangle encadrant l'objet pour lequel on enregistre la couleur
        img.draw_cross(blob.cx(), blob.cy()) #création et dessin d'une croix au centre de ce rectangle qui définira la position de l'objet
        img.draw_rectangle(r_3)

print("Seuils appris...")
print("FIN DES COULEURS ")

#----------------------------------------INITIALISATION DES VARIABLES----------------------------------------------------------------

detect_couleur1=0
detect_couleur2=0
detect_couleur3=0

CORPSTEXTE = " "

recup_blob_cy = 0

ch1 = tim.channel(1, Timer.PWM, pin=Pin("P7")) #création du signal PWM permettant d'allumer une LED de temoin
ch2 = tim.channel(2, Timer.PWM, pin=Pin("P8")) #création du signal PWM permettant d'allumer une LED de temoin
ch1.pulse_width_percent(0)
ch2.pulse_width_percent(0)


#-----------------------------------------------------FONCTION-----------------------------------------------------------------------

def DirectionObject(detect_couleur1, detect_couleur2, detect_couleur3,LED_gauche,LED_droite,CORPSTEXTE): #fonction "DirectionObject" permettant d'adapter le corps de mail et les leds en fonction de la couleur vue par la caméra
    if (detect_couleur1==1 and detect_couleur2 == 0 and detect_couleur3 ==0): #détection de coul1 UNIQUEMENT
       ch1.pulse_width_percent(int(LED_droite)) #le signal PWM avec la valeur de rapport cyclique en argument est envoyé
       ch2.pulse_width_percent(int(LED_gauche)) #le signal PWM avec la valeur de rapport cyclique en argument est envoyé
       #Ajout corps du mail le numero de l'object
       #body += "Couleur 1"
       print("Detecte object 1")
    if ((detect_couleur3 == 1) or (detect_couleur3 == 0 and detect_couleur2 == 0 and detect_couleur1 == 0)): #détection de couleur 2 (qui est prioritaire même en présence de couleur 1 et/ou couleur 2 )
       ch1.pulse_width_percent(0) #Aucune action
       ch2.pulse_width_percent(0) #Aucune action
       #Ajout corps du mail le numero de l'object
       #body += "Couleur 2"
       print("Detecte object 2")
    if ((detect_couleur3 == 0 and detect_couleur2 == 1)): #détection de couleur 2 SANS mettre en priorité le couleur 3
       ch1.pulse_width_percent(int(LED_droite))
       ch2.pulse_width_percent(int(LED_gauche))
       #Ajout corps du mail le numero de l'object
       #body += "Couleur 3"
       print("Detecte object 3")

#----------------------------------------------------BOUCLE INFINIE------------------------------------------------------------------

while(True):
    clock.tick()
    img = sensor.snapshot()                                 #la caméra prend une capture de l'environnement et retourne une image en objet
    for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10): #détection d'un blob correspondant à la première liste threshold enregistrée (ici l'object 1)
        img.draw_rectangle(blob.rect())                     #dessine un rectangle délimitant l'objet 1 détecté
        img.draw_cross(blob.cx(), blob.cy())                #dessine une croix au centre du rectangle dessiné précédemment et sert de référence pour la position de l'objet
        detect_couleur1 = 1
        recup_blob_cy = blob.cy()                           #prototype de récupération de la position en y pour l'utilisation d'envoie de mail
        if(blob.cx()>180):                                  #si la position x (horizontale) de la croix est entre 180 et 320 (donc vers la droite de la caméra), on envoie mail : DIRECTION DROITE en paramètre
            ##METTRE LE PARAMETRE D'ENVOIE DE MAIL : CORPS DE CELUI-CI DIFFERENTS
        if(blob.cx()<140):                                  #si la position x (horizontale) de la croix est entre 0 et 140 (donc vers la gauche de la caméra), on envoie mail :  DIRECTION GAUCHE en paramètre
             ##METTRE LE PARAMETRE D'ENVOIE DE MAIL : CORPS DE CELUI-CI DIFFERENTS
        if(blob.cx()>=140 and blob.cx()<=180):              #si la position x (horizontale) de la croix est entre 140 et 180 (donc vers le centre de la caméra), on envoie mail :  DIRECTION CENTRE en paramètre
            ##METTRE LE PARAMETRE D'ENVOIE DE MAIL : CORPS DE CELUI-CI DIFFERENTS
    for blob in img.find_blobs([threshold_3], pixels_threshold=100, area_threshold=100, merge=True, margin=10): #détection d'un blob correspondant à la troisième liste threshold_3 enregistrée
        img.draw_rectangle(blob.rect())                     #dessine un rectangle délimitant l'object 3
        img.draw_cross(blob.cx(), blob.cy())                #dessine une croix au centre du rectangle dessiné précédemment et sert de référence pour la position de l'objet
        detect_object3 = 1
        recup_blob_cy = blob.cy()
    for blob in img.find_blobs([threshold_2], pixels_threshold=100, area_threshold=100, merge=True, margin=10): #détection d'un blob correspondant à la deuxième liste threshold_2 enregistrée
        img.draw_rectangle(blob.rect())                     #dessine un rectangle délimitant l'objet
        img.draw_cross(blob.cx(), blob.cy())                #dessine une croix au centre du rectangle dessiné précédemment et sert de référence pour la position de l'objet
        detect_couleur2 = 1
        recup_blob_cy = blob.cy()                           #prototype de récupération de la position
        #la suite agit de manière identique que pour le cas "1" avec des équations différentes
        #De plus, l'analyse des signaux et leurs rapport peut se faire par oscillo
        if(blob.cx()>180):
            LED_gauche = (1/7)*blob.cx()+(30/7)
            LED_droite = -(1/7)*blob.cx()+(390/7)
        if(blob.cx()<140):
            LED_gauche = (1/7)*blob.cx()+10
            LED_droite = -(1/7)*blob.cx()+50
        if(blob.cx()>=140 and blob.cx()<=180):
            LED_gauche = 30
            LED_droite = 30

    print(threshold, threshold_2,threshold_3)
    DirectionObject(detect_couleur1,detect_couleur2,detect_couleur3,LED_gauche,LED_droite,CORPSTEXTE) #appel de la fonction "DirectionObject" avec les variables de validation pour les mails !
    detect_couleur3=0   #remise à zéro des variables de détection des couleurs pour recommencer un cycle
    detect_couleur2=0
