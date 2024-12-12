class pièces: # caratéristiques des pièces
    
    vide = " " # utile quand aucune pièce n'est sur une case
    nom_pièces = [vide, "pion_noir", "cavalier_noir", "fou_noir", "tour_noir", "dame_noire", "roi_noir", "pion_blanc", "cavalier_blanc", "fou_blanc", "tour_blanc", "dame_blanche", "roi_blanc"] # nom en str
   
    valeur_pièces = [0, 1, 3, 3, 5, 10, 0, 1, 3, 3, 5, 10, 0]
    
    
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

    def __init__(self, nom = vide , couleur = " "): # l'objectif est de pouvoir donner des attributs à chaque pièce  en rentrant les information # si aucun nom m'est donné, c'est ( par défaut) vide. Pareil pour couleur
        self.nom = nom # j'ai donné des attributs pour chaque paramètre
        self.couleur = couleur # j'ai donné des attributs pour chaque paramètre
        self.valeur = self.valeur_pièces[self.nom_pièces.index(nom)] # donne la valeur associée au nom donné. Reprend les éléments associés lignes 4 et 6
        

    def is_empty(self):
        return self.nom == self.vide # si self.nom correspond à self.vide ( si ce que l'on a rentré est " "), alors la fonction retourne True
    

case_vide = pièces() # test
print(case_vide.is_empty()) # test