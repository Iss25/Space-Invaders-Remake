import pygame
import random
import math

size = screen_width, screen_height = 1344,756
black = (1, 0, 0)
white = (0, 0, 45)
red  = (255, 0, 0)
m = 0

class Overlay(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load("overlay_level.png")
        #self.image = pygame.transform.scale(self.image, (135, 40))
        self.image = pygame.Surface([135, 80])
        self.image.fill(red)
        self.image.set_alpha(100)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 120

        self.scorelevel = 'level = 1'

        self.font_name = pygame.font.match_font('comicsans')
        self.font = pygame.font.Font(self.font_name, 30)
        self.text_surface = self.font.render(self.scorelevel, True, (255,255,255))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.x = 15
        self.text_rect.y = 130

        self.score = 0
        self.scorekill = 'score = {score:04d}'

        self.text_surface2 = self.font.render(self.scorekill.format(score=self.score), True, (255,255,255))
        self.text_rect2 = self.text_surface2.get_rect()
        self.text_rect2.x = 15
        self.text_rect2.y = 170
        
        
        #pygame.display.set_caption(str(scorelevel))
        #display_surface = pygame.display.set_mode((20,120)) 
        #font = pygame.font.Font('freesansbold.ttf', 32) 
        #text = font.render('GeeksForGeeks', True,white)
        #textRect = text.get_rect()
        #textRect.center = (200, 200)
    def update(self,newlevel,enemies_killed,screen):
        #scorelevel = newlevel
        self.scorelevel = 'level = %i'%(newlevel)#enemies_killed)
        #enemies killed = %i' % (newlevel,enemies_killed)
        self.text_surface = self.font.render(self.scorelevel , True, (255,255,255))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.x = 15
        self.text_rect.y = 130

        self.text_surface2 = self.font.render(self.scorekill.format(score=self.score), True, (255,255,255))
        self.text_rect2 = self.text_surface2.get_rect()
        self.text_rect2.x = 15
        self.text_rect2.y = 170


        #pygame.display.set_caption(str(scorelevel))
        #pygame.diplay.update(textRect)
    def draw(self,screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)
        screen.blit(self.text_surface2, self.text_rect2)

    def enemi_killed(self):
        self.score+=2


class Hero(pygame.sprite.Sprite):
    '''Cette classe représente un lutin
    '''

    life = 0

    def __init__(self, width, height, score):
        '''Crée un lutin de largeur 'width' et le hauteur 'height'
        '''
        # Démarre l'objet Lutin comme étant un Sprite (objet pygame)
        pygame.sprite.Sprite.__init__(self)

        # Ouvre l'image lutin.png
        self.image = pygame.image.load("vaisseau spatial.png")
        self.name = "vaisseau spatial.png"
        # Redimentionne l'image pour qu'elle fasse
        # les largeur et hauteur voulues
        self.image = pygame.transform.scale(self.image, (79, 72))

        # Crée le rectangle dans lequel sera dessinée l'image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Place le lutin en bas au centre de l'écran
        self.rect.x = screen_width/2
        self.rect.y = screen_height-self.rect.height
        
        # Donne un score de 0 au lutin au début de la partie
        self.score = score


    
    def shoot (self, scale ):
        return Missile(self,scale)
        
    def update(self,x, missile_group,bonus_group):
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
        
        for bonus in bonus_group:
            if pygame.sprite.collide_mask(bonus,self) is not None:
                bonus.filename
                if bonus.filename == "modern_bonus.png":
                    self.change_image(fichier="modern_spaceship.png", size_x=92, size_y=92)
                    self.name = "modern_spaceship.png"
                elif bonus.filename == "bonus_bleu.png":
                    self.change_image(fichier="blueship2.png", size_x=55, size_y=117)
                    self.name = "blueship2.png"
                else :
                    self.change_image(fichier="red_spaceship.png", size_x=106, size_y=94)
                    self.name = "red_spaceship.png"
                bonus.kill()


        for missile in missile_group:
            if pygame.sprite.collide_mask(missile,self) is not None:
                # Quand le lutin est sur le cadeau,
                # le cadeau est supprimé et le score est augmenté
                if Hero.life == 3:
                    self.kill()
                if self.name != "vaisseau spatial.png":
                    self.image = pygame.image.load("vaisseau spatial.png")
                    self.image = pygame.transform.scale(self.image, (80, 73))
                    self.name = "vaisseau spatial.png"
                    Hero.life += 1
                else: 
                    self.kill()
                missile.kill()
    
    def change_image(self, fichier, size_x, size_y):
        self.image = pygame.image.load(fichier)
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        x = self.rect.centerx-size_x/2 
        y = self.rect.bottom-size_y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
                

class Missile(pygame.sprite.Sprite):
    def __init__(self, shooter, scale):
        pygame.sprite.Sprite.__init__(self)

        if isinstance(shooter, Enemi):
            self.image = pygame.image.load("missile.red.png")
            self.image = pygame.transform.scale(self.image, (25*scale, 54*scale))
            self.speed_y = 5
        else:
            self.image = pygame.image.load("missile.shooter.png")
            self.image = pygame.transform.scale(self.image, (24*scale, 45*scale))
            self.speed_y = -5

        self.rect = self.image.get_rect()
        self.rect.x = shooter.rect.centerx-self.image.get_width()/2
        self.rect.y = shooter.rect.y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.rect.y > screen_height:
            self.kill()
        if self.rect.bottom < 0:   
            self.kill()
        self.rect.y+= self.speed_y

class Enemi(pygame.sprite.Sprite):
    '''Cette classe représente un cadeau
    '''
    def __init__(self,x,scale, score):
        ''' Crée un cadeau qui va se déplacer à la vitesse speed
        '''
        # Démarre l'objet Cadeau comme étant Sprite (objet pygame)
        pygame.sprite.Sprite.__init__(self)

        # Ouvre l'image cadeau.png
        self.image = pygame.image.load("alien.red.png")
        # Redimentionne l'image pour qu'elle ne soit pas trop grande
        self.image = pygame.transform.scale(self.image, (143//scale,74//scale))

        # Crée le rectangle dans lequel sera dessinée l'image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)   

        # Place le cadeau de façon aléatoire au dessus de l'écran
        self.rect.x = x
        self.rect.y = 0

        self.x = x
        
        self.speed_x = 5

        self.angle = random.randrange(0,360)
        self.score = score

    def update(self, missile_group, bonus_group):
        ''' Mise à jour de la position du cadeau
        '''
        self.angle += 3 
        self.x += self.speed_x
        self.rect.x = self.x + math.cos(math.pi * self.angle / 180)*40
        self.rect.y = 40+math.sin(math.pi * self.angle / 180)*40
        if self.rect.right>screen_width:
             self.speed_x = -5
        if self.rect.left<0:
             self.speed_x = 5

        for missile in missile_group:
            if pygame.sprite.collide_mask(missile,self) is not None:
                # Quand le lutin est sur le cadeau,
                # le cadeau est supprimé et le score est augmenté
                self.kill()
                self.score.enemi_killed()
                missile.kill()
                if random.randint(0, 2) == 1:
                    bonus = Bonus(self)
                    bonus_group.add(bonus)
                
    def shoot (self):
        return Missile(self,random.randrange(1,3))


class Bonus(pygame.sprite.Sprite):
    def __init__(self,enemi):
        pygame.sprite.Sprite.__init__(self)

        self.filename = random.choice(["bonus_bleu.png","modern_bonus.png","bonus_red.png"])

        self.image = pygame.image.load(self.filename)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.speed_y = 4

        self.rect = self.image.get_rect()
        self.rect.x = enemi.rect.x
        self.rect.y = enemi.rect.y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.rect.y > screen_height:
            self.kill()
        if self.rect.y < 0:   
            self.kill()
        self.rect.y+= self.speed_y

class Life(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("pixel_heart_full.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 210
        self.image2 = pygame.image.load("pixel_heart_full.png")
        self.image2 = pygame.transform.scale(self.image2, (40, 40))
        self.rect2 = self.image2.get_rect()
        self.rect2.x = 55
        self.rect2.y = 210
        self.image3 = pygame.image.load("pixel_heart_full.png")
        self.image3 = pygame.transform.scale(self.image3, (40, 40))
        self.rect3 = self.image3.get_rect()
        self.rect3.x = 100
        self.rect3.y = 210

    def update(self):
        if Hero.life == 1:
            self.image3 = pygame.image.load("pixel_heart_empty.png")
            self.image3 = pygame.transform.scale(self.image3, (40, 40))
        if Hero.life == 2:
            self.image2 = pygame.image.load("pixel_heart_empty.png")
            self.image2 = pygame.transform.scale(self.image2, (40, 40))
        if Hero.life == 3:
            self.image = pygame.image.load("pixel_heart_empty.png")
            self.image = pygame.transform.scale(self.image, (40, 40))
            
    def draw(self,screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.image2, self.rect2)
        screen.blit(self.image3, self.rect3)