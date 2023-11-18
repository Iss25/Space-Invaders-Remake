import math
import random
import sys

import pygame

size = screen_width, screen_height = 1280, 720
black = (0, 0, 0)
white = (255, 255, 255)
red  = (255, 0, 0)

class Lutin(pygame.sprite.Sprite):
    '''Cette classe représente un lutin
    '''
    def __init__(self, width, height):
        '''Crée un lutin de largeur 'width' et le hauteur 'height'
        '''
        # Démarre l'objet Lutin comme étant un Sprite (objet pygame)
        pygame.sprite.Sprite.__init__(self)

        # Ouvre l'image lutin.png
        self.image = pygame.image.load("lutin.png")
        # Redimentionne l'image pour qu'elle fasse
        # les largeur et hauteur voulues
        self.image = pygame.transform.scale(self.image, (width, height))

        # Crée le rectangle dans lequel sera dessinée l'image
        self.rect = self.image.get_rect()

        # Place le lutin en bas au centre de l'écran
        self.rect.x = screen_width/2
        self.rect.y = screen_height-self.rect.height
        
        # Donne un score de 0 au lutin au début de la partie
        self.score = 0

    def update(self,x):
        ''' Mise à jour de la position du lutin
        Le lutin est déplacé à la position x
        '''
        
        # Délace le lutin pour qu'il soit centré horizontalement sur x
        self.rect.x = x-self.rect.width/2

        # Bloque le lutin pour ne pas qu'il sorte de l'écran
        if self.rect.x<0:
            self.rect.x=0
        if self.rect.x>screen_width-self.rect.width:
            self.rect.x = screen_width-self.rect.width

    def attrape_cadeau(self, cadeau_group):
        ''' Attrape les cadeaux présents dans cadeau_group
        s'ils sont sur le lutin
        '''
        for cadeau in cadeau_group:
            if (cadeau.rect.bottom >= self.rect.top
                    and cadeau.rect.left <= self.rect.right
                    and cadeau.rect.right >= self.rect.left):
                # Quand le lutin est sur le cadeau,
                # le cadeau est supprimé et le score est augmenté
                cadeau.kill()
                self.score+=1
                


class Cadeau(pygame.sprite.Sprite):
    '''Cette classe représente un cadeau
    '''
    def __init__(self):
        ''' Crée un cadeau qui va se déplacer à la vitesse speed
        '''
        # Démarre l'objet Cadeau comme étant Sprite (objet pygame)
        pygame.sprite.Sprite.__init__(self)

        # Ouvre l'image cadeau.png
        self.image = pygame.image.load("cadeau.png")
        # Redimentionne l'image pour qu'elle ne soit pas trop grande
        self.image = pygame.transform.scale(self.image, (142, 150))

        # Crée le rectangle dans lequel sera dessinée l'image
        self.rect = self.image.get_rect()

        # Place le cadeau de façon aléatoire au dessus de l'écran
        self.rect.x = random.randrange(screen_width-self.rect.width)
        self.rect.y = -self.rect.height

        self.speed_y = 0

    def update(self):
        ''' Mise à jour de la position du cadeau
        '''
        self.rect.y += self.speed_y

    def acceleration(self,a):
        ''' Augmente la vitesse verticale du cadeau de a
        '''
        self.speed_y += a

if __name__=="__main__":

    # Démarre pygame
    pygame.init()

    # Crée l'écran de ta taille voulue (voir au début du fichier)
    screen = pygame.display.set_mode(size)
    # Crée une horloge pour limiter le nombre d'images par seconde
    clock = pygame.time.Clock()

    # Crée une groupe qui va contenir tous les cadeaux
    cadeau_group = pygame.sprite.Group()
    # Crée une groupe qui va contenir tous les objets
    all_group = pygame.sprite.Group()

    # Crée un lutin de taille 111 sur 150
    lutin = Lutin(111,150)
    # Ajoute le lutin à la liste de tous les objets
    all_group.add(lutin)

    # Variables utilisées pour savoir quand ajouter des nouveaux cadeaux
    iteration = 0
    level = 1
    
    # Variable qui détermine si le jeu doit encore s'exécuter
    running = True

    # Tant que running est vrai, le jeu continue
    while running:

        # Regarge tous les évènements
        # pour vérifier si le programme doit être quitté
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Récupère la position de la souris
        x,y = pygame.mouse.get_pos()
        # Déplace le lutin à la position x
        lutin.update(x)
        # Imprime le score du lutin
        print(lutin.score)

        # Dés que iteration est suffisement grand,
        # aoute un cadeau et on remet iteration à 0.
        # Comme level augmente à chaque fois,
        # le temps entre deux apparitions de cadeau va diminuer.
        if iteration>(60*4/math.sqrt(level)):
            iteration = 0
            level+=1
            cadeau = Cadeau()
            cadeau_group.add(cadeau)
            all_group.add(cadeau)
        iteration += 1
        
        # Appelle la fonction update pour tous les cadeaux
        cadeau_group.update()
        # Le lutin attrape tous les cadeaux à sa portée
        lutin.attrape_cadeau(cadeau_group)
        
        # Accélère la vitesse de descente de chaque cadeau
        for cadeau in cadeau_group:
            cadeau.acceleration(0.2)
            # Si un cadeau touche le bas de l'écran, le jeu s'arrête.
            if cadeau.rect.bottom >= screen_height:
                running = False

        # Met un fond blanc
        screen.fill(white)
        # Dessine tous les objets dans la mémoire
        all_group.draw(screen)

        # Met à jour l'écran
        pygame.display.flip()

        # Pour ne pas dépasser 60 images par secondes
        clock.tick(60)
    
    # Le jeu doit être quitté car on est hors de la boucle
    pygame.quit()

