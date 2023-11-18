import math
import random
import sys
import time

import pygame

from sprites_savecopy import Hero, Missile, Enemi, Overlay, Life

m = 0

size = screen_width, screen_height = 1344,756
background = (5, 4, 60)

def random_shoot():
    return random.randrange(1000, 2500, 100)
    
 
def new_enemi (enemi_group, all_group,level, overlay):
    scale = random.randrange(2,3)
    for i in range (level*2):
        enemi = Enemi(i*143+10*i,scale, score=overlay)
        enemi_group.add(enemi)
        all_group.add(enemi)


if __name__=="__main__":

    # Démarre pygame
    pygame.init()

    # Crée l'écran de ta taille voulue (voir au début du fichier)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    # Crée une horloge pour limiter le nombre d'images par seconde
    clock = pygame.time.Clock()

    # Crée une groupe qui va contenir tous les cadeaux
    missile_hero_group = pygame.sprite.Group()
    missile_enemi_group = pygame.sprite.Group()
    enemi_group = pygame.sprite.Group()
    overlay_group = pygame.sprite.Group()
    bonus_group = pygame.sprite.Group()
    life_group = pygame.sprite.Group()
    # Crée une groupe qui va contenir tous les objets
    all_group = pygame.sprite.Group()

    # Crée un lutin de taille 111 sur 150
    overlay = Overlay()
    life = Life()
    hero = Hero(111,150, score=overlay)
    # Ajoute le lutin à la liste de tous les objets
    all_group.add(hero)



    # Variables utilisées pour savoir quand ajouter des nouveaux cadeaux
    iteration = 0
    level = 1

    new_enemi(enemi_group, all_group, level, overlay)
    
    # Variable qui détermine si le jeu doit encore s'exécuter
    running = True

    last_shoot_hero_time = time.time()
    last_shoot_enemi_time = time.time()
    curTick = 0

    # Tant que running est vrai, le jeu continue
    while running:
        curTick += 1
        

        # Regarge tous les évènements
        # pour vérifier si le programme doit être quitté
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and curTick>45:
                missile=hero.shoot(2)
                all_group.add(missile)
                missile_hero_group.add(missile)
                curTick = 0

        # Récupère la position de la souris
        x,y = pygame.mouse.get_pos()
        
        # Déplace le lutin à la position x
        hero.update(x, missile_enemi_group,bonus_group)

        current_time = time.time()
        if current_time-last_shoot_hero_time >= 1:
            missile=hero.shoot(1)
            all_group.add(missile)
            missile_hero_group.add(missile)
            last_shoot_hero_time = current_time

        for enemi in enemi_group:
            if current_time-last_shoot_enemi_time >= random.uniform(0.5,3)/((level+1)/5): 
                if enemi.alive():
                    missile=enemi.shoot()
                    all_group.add(missile)
                    missile_enemi_group.add(missile)
                    last_shoot_enemi_time = current_time

            
        missile_hero_group.update()
        missile_enemi_group.update()
        if not len(enemi_group):
            level+=1
            new_enemi(enemi_group, all_group, level,overlay)
            
        

        
        # Appelle la fonction update pour tous les cadeaux
        enemi_group.update(missile_hero_group, bonus_group)
        bonus_group.update()
        life.update()

        # Met un fond
        screen.fill(background)

        #test overlay
        #font_name = pygame.font.match_font('comicsans')
        #font = pygame.font.Font(font_name, 20)
        #text_surface = font.render('test', True, (255,255,255))
        #text_rect = text_surface.get_rect()
        #text_rect.midtop = (50, 50)
        #screen.blit(text_surface, text_rect)
        overlay.update(level,0,screen)
        sc = overlay.score
        lvl = overlay.scorelevel
        
        # Dessine tous les objets dans la mémoire
        all_group.draw(screen)
        bonus_group.draw(screen)
        overlay.draw(screen)
        life.draw(screen)

        # Met à jour l'écran
        pygame.display.flip()

        if not hero.alive():
            print("you lose")
            print("Yours stats are: \n score = " + str(sc) + " \n " + str(lvl))
                
            break

        # Pour ne pas dépasser 60 images par secondes
        clock.tick(60)

        
    
    # Le jeu doit être quitté car on est hors de la boucle
    pygame.quit()

    question = str(input("Would you like to save your stats ('yes' or 'no'):"))
    if question == "yes":
        name = str(input("What's your name:"))
        file = open("tableau score.dat","a")
        file.write(name + ":\n Yours stats are: \n score = " + str(sc) + " \n " + str(lvl) + "\n \n")
    else :
        pass
