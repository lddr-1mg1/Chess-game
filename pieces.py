class pièces: # caratéristiques des pièces
    
    vide = " " # utile quand aucune pièce n'est sur une case
    nom_pièces = [vide, "pion_noir", "cavalier_noir", "fou_noir", "tour_noir", "dame_noire", "roi_noir", "pion_blanc", "cavalier_blanc", "fou_blanc", "tour_blanc", "dame_blanche", "roi_blanc"] # nom en str
   
    valeur_pièces = [0, 1, 3, 3, 5, 10, 0, 1, 3, 3, 5, 10, 0]
   
    couleur_pièces = ["noir", "blanc"] # couleur en str 
    
    délimitation_échiquier = (
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1,  0,  1,  2,  3,  4,  5,  6,  7, -1,
        -1,  8,  9, 10, 11, 12, 13, 14, 15, -1,
        -1, 16, 17, 18, 19, 20, 21, 22, 23, -1,
        -1, 24, 25, 26, 27, 28, 29, 30, 31, -1,
        -1, 32, 33, 34, 35, 36, 37, 38, 39, -1,
        -1, 40, 41, 42, 43, 44, 45, 46, 47, -1,
        -1, 48, 49, 50, 51, 52, 53, 54, 55, -1,
        -1, 56, 57, 58, 59, 60, 61, 62, 63, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        ) 
            # tableau utile pour le mouvement des pièces: délimitations de l'échiquier
            # méthode "Mailbox" # tableau unidimensionelle
            # les "-1" représentent les exceptions
        
    déplacement_pièces = (
        1,  2,  3,  4,  5,  6,  7,  8,
        9, 10, 11, 12, 13, 14, 15, 16,
       17, 18, 19, 20, 21, 22, 23, 24,
       25, 26, 27, 28, 29, 30, 31, 32,
       33, 34, 35, 36, 37, 38, 39, 40,
       41, 42, 43, 44, 45, 46, 47, 48,
       49, 50, 51, 52, 53, 54, 55, 56,
       57, 58, 59, 60, 61, 62, 63, 64,
       )   # version simplifier et compressé du tableau "délimitaion_échiquier"
  
    # mouvements selon le tableau "délimitation_échiquier"
    mouvement_tour = [10, -10, 1, -1] # mouvement en ligne  
    mouvement_fou = [11, -11, 9, -9] # mouvement en diagonale
    mouvement_cavalier = [-12,-21,-19,-8,12,21,19,8] # mouvement en L
    mouvement_dame = [-11, -10, -9, -1, 1, 9, 10, 11] # le déplacement de la dame est equivalent à celui du fou + celui de la tour
    mouvement_roi = [-11, -10, -9, -1, 1, 9, 10, 11] # mouvement identique à celui de la dame mais uniquement d'une case
    mouvement_pion = [-11, -9, -10, -20] # à préciser quand quel mouvement est possible !!!!!!

    def __init__(self, nom, couleur, valeur, déplacement): # l'objectif est de pouvoir donner des attributs à chaque pièce
        self.nom = nom
        self.couleur = couleur
        self.valeur = valeur
        self.déplacemnt = déplacement

    Pion_noir = (nom := nom_pièces[1], couleur := couleur_pièces[0] , valeur := valeur_pièces[1], déplacement := mouvement_pion )
    Cavalier_noir = (nom := nom_pièces[2], couleur := couleur_pièces[0], valeur := valeur_pièces[2], déplacement := mouvement_cavalier)
    Fou_noir = (nom := nom_pièces[3], couleur := couleur_pièces[0], valeur := valeur_pièces[3], déplacement := mouvement_fou)
    Tour_noir = (nom := nom_pièces[4], couleur := couleur_pièces[0], valeur := valeur_pièces[4], déplacement := mouvement_tour)
    Dame_noir = (nom := nom_pièces[5], couleur := couleur_pièces[0], valeur := valeur_pièces[5], déplacement := mouvement_dame)
    Roi_noir = (nom := nom_pièces[6], couleur := couleur_pièces[0], valeur := valeur_pièces[6], déplacement := mouvement_roi)
    Pion_blanc = (nom := nom_pièces[7], couleur := couleur_pièces[1], valeur := valeur_pièces[7], déplacement := mouvement_pion)
    Cavalier_blanc = (nom := nom_pièces[8], couleur := couleur_pièces[1], valeur := valeur_pièces[8], déplacement := mouvement_cavalier)
    Fou_blanc = (nom := nom_pièces[9], couleur := couleur_pièces[1], valeur := valeur_pièces[9], déplacement := mouvement_fou)
    Tour_blanc = (nom := nom_pièces[10], couleur := couleur_pièces[1], valeur := valeur_pièces[10], déplacement := mouvement_tour)
    Dame_blanc = (nom := nom_pièces[11], couleur := couleur_pièces[1], valeur := valeur_pièces[11], déplacement := mouvement_dame)
    Roi_blanc = (nom := nom_pièces[12], couleur := couleur_pièces[1], valeur := valeur_pièces[12], déplacement := mouvement_roi)
    # chaque pièce a maintenat un nom et une couleur en str, une valeur et un déplacement selon les tableaus unidimensionnel



    print(Roi_blanc)# test