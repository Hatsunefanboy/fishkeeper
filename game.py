import pygame
import random
import math
from pathlib import Path
import os
import sys

BASE_DIR = Path(sys.argv[0]).resolve().parent
def chemin(*morceaux):
    return str(BASE_DIR.joinpath(*morceaux))
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


"""
foundamentale variable

"""
t=0 #absolute time
l=0 #looping time
v=(0,0)

(xs,ys)=(0,0) #position de la souris

active_dialogue = None #y'a til des dialogues

aquarium_fishs=[]

"""
music
"""
aquarium_music = chemin("music", "aquarium_music.mp3")
hub_music = chemin("music", "hub_music.mp3")
food_sound = chemin("music", "eat_sound.wav")
garden_music = chemin("music", "garden_music.mp3")
tree_minigame_music = chemin("music", "minigame_music.wav")
brique_music = chemin("music", "brique.mp3")







"""

graphiques

"""
image_table = pygame.image.load(chemin("asset", "table.png")).convert_alpha()
image_aquarium = pygame.image.load(chemin("asset", "aquarium.png")).convert_alpha()

image0_beta = pygame.image.load(chemin("asset", "beta", "beta1.png")).convert_alpha()
image1_beta = pygame.image.load(chemin("asset", "beta", "beta2.png")).convert_alpha()
image2_beta = pygame.image.load(chemin("asset", "beta", "beta3.png")).convert_alpha()

shrimp = pygame.image.load(chemin("asset", "shrimp.png")).convert_alpha()
aquarium_background = pygame.image.load(chemin("asset", "aquarium_background.png")).convert_alpha()
hub_background = pygame.image.load(chemin("asset", "hub_background.png")).convert_alpha()
home_image = pygame.image.load(chemin("asset", "home.png")).convert_alpha()
image_door = pygame.image.load(chemin("asset", "porte.webp")).convert_alpha()
garden_background = pygame.image.load(chemin("asset", "garden_background.png")).convert_alpha()

tree_animation_image = [
    pygame.image.load(chemin("asset", "arbre", "arbre1.png")).convert_alpha(),
    pygame.image.load(chemin("asset", "arbre", "arbre1.png")).convert_alpha()
]

tree_minigame_background0 = pygame.image.load(chemin("asset", "minijeux arbre", "minigamebackground.png")).convert_alpha()
tree_minigame_background1 = pygame.image.load(chemin("asset", "minijeux arbre", "minigamebackground2.png")).convert_alpha()

bee_image = pygame.image.load(chemin("asset", "minijeux arbre", "abeille.png")).convert_alpha()

bee_animations_images = [
    pygame.image.load(chemin("asset", "minijeux arbre", "abeille2.png")).convert_alpha(),
    pygame.image.load(chemin("asset", "minijeux arbre", "abeille.png")).convert_alpha()
]

guepe_animations_images = [
    pygame.image.load(chemin("asset", "minijeux arbre", "guepe2.png")).convert_alpha(),
    pygame.image.load(chemin("asset", "minijeux arbre", "guepe.png")).convert_alpha()
]

coeur = pygame.image.load(chemin("asset", "minijeux arbre", "coeur.png")).convert_alpha()

brique_image = pygame.image.load(chemin("asset", "brique_malicieuse.png")).convert_alpha()

gros_images = [
    pygame.image.load(chemin("asset", "beta", "gros0.png")).convert_alpha(),
    pygame.image.load(chemin("asset", "beta", "gros1.png")).convert_alpha()
]
"""

Vector function


"""
def angleto(v1,v2):
    d1=v1[0]-v2[0]
    d2=v1[1]-v2[1]
    return math.degrees(math.atan2(-d2,d1))


def scalar(v,lambd):
    return(v[0]*lambd,v[1]*lambd)


def plus(v1,v2):
    return (v1[0]+v2[0],v1[1]+v2[1])

def minus(v1,v2):
    return (v1[0]-v2[0],v1[1]-v2[1])

def distance(v1,v2):
    return ((v1[0]-v2[0])**2+(v1[1]-v2[1])**2)**(1/2)


def scalar_product(v1,v2):
    return v1[0]*v2[0]+v1[1]*v2[1]

def norme(v):
    return (scalar_product(v,v))**(1/2)


"""
theoric game object

"""
class stat:
    def __init__(self,life,speed,toughness,mana,strength):
        self.life=life
        self.speed=speed
        self.toughness=toughness
        self.mana=mana
        self.strength=strength

class animation:
    def __init__(self,imageL,time,duration):
        self.image=imageL
        self.time=time
        self.actual=0
        self.duration=duration

    def actualize(self,t):
        if t-self.time >= self.duration*len(self.image):
            self.actual=(self.actual+1)% len(self.image)
            self.time=t




class interactor:
    def __init__(self,coordinate,image):
        self.coordinate=coordinate
        self.image=image

class hitbox_interactor(interactor):
    def __init__(self,hitbox,coordinate,image):
        self.coordinate=coordinate
        self.image=image
        self.hitbox=hitbox

    def updatepos(self,new_pos):
        self.coordinate=new_pos

    def is_touching(self, other):
        return (
            self.coordinate[0] < other.coordinate[0] + other.hitbox[0] and
            self.coordinate[0] + self.hitbox[0] > other.coordinate[0] and
            self.coordinate[1] < other.coordinate[1] + other.hitbox[1] and
            self.coordinate[1] + self.hitbox[1] > other.coordinate[1]
        )

class clickable(hitbox_interactor):
    def __init__(self,hitbox,coordinate,image,effect,activeplace):
        self.hitbox=hitbox
        self.coordinate=coordinate
        self.image=image
        self.effect=effect
        self.activeplace=activeplace

    def click_bool(self,v):
        if self.coordinate[0]<=v[0]<=self.coordinate[0]+self.hitbox[0] and self.coordinate[1]<=v[1]<=self.coordinate[1]+self.hitbox[1]:
            return True
        else:
            return False


class choice_dialogue:
    def __init__(self, text, choices):
        self.active = False
        self.text = text
        self.choices = choices

        self.font = pygame.font.SysFont("arial", 28)
        self.small_font = pygame.font.SysFont("arial", 24)

        # boîte en bas de l'écran
        self.box = pygame.Rect(0, 530, 1280, 190)

        self.buttons = []
        start_x = 40
        y = 635

        for k in range(len(self.choices)):
            rect = pygame.Rect(start_x + k * 180, y, 140, 45)
            self.buttons.append(rect)

    def open(self):
        global active_dialogue
        active_dialogue = self
        self.active = True

    def close(self):
        global active_dialogue
        self.active = False
        active_dialogue = None

    def update_click(self, pos):
        if not self.active:
            return

        for k in range(len(self.buttons)):
            rect = self.buttons[k]
            label, effect = self.choices[k]

            if rect.collidepoint(pos):
                self.close()

                if effect != None:
                    effect()

    def draw(self, screen):
        if not self.active:
            return

        # fond transparent brutal
        dialogue_surface = pygame.Surface((1280, 190), pygame.SRCALPHA)
        dialogue_surface.fill((0, 0, 0, 150))
        screen.blit(dialogue_surface, (0, 530))

        # ligne supérieure simple
        pygame.draw.line(screen, (255, 255, 255), (0, 530), (1280, 530), 2)

        # texte
        text_img = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_img, (40, 565))

        mouse_pos = pygame.mouse.get_pos()

        # boutons sans vrai formatage
        for k in range(len(self.buttons)):
            rect = self.buttons[k]
            label, effect = self.choices[k]

            if rect.collidepoint(mouse_pos):
                color = (255, 255, 255)
                text_color = (0, 0, 0)
            else:
                color = (40, 40, 40)
                text_color = (255, 255, 255)

            pygame.draw.rect(screen, color, rect)

            label_img = self.small_font.render(label, True, text_color)
            screen.blit(label_img, (rect.x + 20, rect.y + 8))

class png(clickable):
    def __init__(self,hitbox,coordinate,image,effect,activeplace,animations):
        self.hitbox=hitbox
        self.coordinate=coordinate
        self.image= image
        self.effect=effect
        self.activeplace=activeplace
        self.animations=animations
    def actualize(self,i,t):
        self.animations[i].actualize(t)
        self.image=self.animations[i].image[self.animations[i].actual]






class fish(hitbox_interactor):
    def __init__(self,hitbox,coordinate,animation,stat,v,is_food=False):
        self.hitbox=hitbox
        self.coordinate=coordinate
        self.animation=animation
        self.image=self.animation.image[self.animation.actual]
        self.v=v
        self.stat=stat
        self.is_food=is_food

    def move(self,t,food):
        self.animation.actualize(t)
        self.image=self.animation.image[self.animation.actual]

        if self.v[0]>self.coordinate[0] :
            self.image=pygame.transform.flip(self.image,False,True)

        self.image=pygame.transform.rotate(self.image,angleto(self.coordinate,self.v))

        if self.is_food:
            if self.is_touching(food):
                pygame.mixer.Sound(food_sound).play()
                self.is_food=False
                self.v=(random.randint(0,1280-self.hitbox[0]),random.randint(0,720-self.hitbox[1]))



        else:
             if distance(self.coordinate,self.v)<8:
                self.is_food=False
                self.v=(random.randint(self.hitbox[0],1280-self.hitbox[0]),random.randint(self.hitbox[1],720-self.hitbox[1]))

        self.coordinate=plus(self.coordinate, scalar(minus(self.v,self.coordinate),self.stat.speed))


    def food(self,pos_food):
        self.v=pos_food
        self.is_food=True






"""
places
"""
places={'hub_p':True , 'menu_p': False , 'aquarium_p': False,'garden_p':False,'tree_minigame_p': False,'brique_p':False}

def go_to(place):
    global places
    for i in places.keys():
        places[i]=False
    places[place]=True

def go_to_aquarium():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(aquarium_music)
    pygame.mixer.music.play(-1)
    go_to("aquarium_p")

def go_to_hub():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(hub_music)
    pygame.mixer.music.play(-1)
    go_to("hub_p")

def go_to_garden():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(garden_music)
    pygame.mixer.music.play(-1)
    go_to("garden_p")

def go_to_tree_minigame():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(tree_minigame_music)
    pygame.mixer.music.play(-1)
    go_to("tree_minigame_p")

def go_to_brique():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(brique_music)
    pygame.mixer.music.play(-1)
    go_to("brique_p")





"""
values and real game object

"""


table=interactor((0,0),image_table)

aq_food=hitbox_interactor((50,70),(-4,-4),shrimp)



aquarium=clickable((200,100),(150,375),image_aquarium,go_to_aquarium,['hub_p'])

home=clickable((50,50),(30,30),home_image,go_to_hub,['aquarium_p','garden_p','hub_p','tree_minigame_p','brique_p'])

door=clickable((240,350),(1000,400),image_door,go_to_garden,['hub_p'])

beta_stat=stat(50,1/60,40,40,10)
beta_animation=animation([image0_beta,image1_beta,image2_beta],t,3)
beta=fish((300,200),(0,0),beta_animation,beta_stat,v)

gros_animation=animation(gros_images,t,5)
gros=fish((300,200),(0,0),gros_animation,beta_stat,v)

bee_stat=stat(50,1/200,40,40,10)
bee_animation=animation(bee_animations_images,t,3)
guepe_animation=animation(guepe_animations_images,t,3)


aquarium_fishs.append(beta)

tree_animation=animation(tree_animation_image,t,2)

tree_dialogue = choice_dialogue(
    "Veux-tu jouer à un jeu ?",
    [
        ("Oui", go_to_tree_minigame),
        ("Non", None)
    ]
)

tree = png(
    (500, 500),
    (500, 250),
    tree_animation_image[0],
    tree_dialogue.open,
    ['garden_p'],
    [tree_animation]
)
def bonne_reponse_abeille():
    aquarium_fishs.append(gros)
    print("bonne réponse")
    go_to_garden()

def mauvaise_reponse_abeille():
    print("mauvaise réponse")
    go_to_garden()


bee_question_dialogue = choice_dialogue(
    "Combien y avait-il d'abeilles ?",
    [
        ("10", mauvaise_reponse_abeille),
        ("12", bonne_reponse_abeille),
        ("15", mauvaise_reponse_abeille),
        ("18", mauvaise_reponse_abeille)
    ]
)


brique=clickable((20,30),(0,0),brique_image,go_to_brique,['hub_p'])
"""
clickable et autre tuc utile
"""
in_game_clickable=[aquarium,home,door,tree,brique]



minitimer=-1


"""
game boucle



"""
while running:
    '''
    time update
    '''
    t+=1
    l=t%60


    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            if active_dialogue != None:
                active_dialogue.update_click(pos)

            else:
                for i in in_game_clickable:
                    for j in i.activeplace:
                        if places[j]:
                            if i.click_bool(pos):
                                i.effect()


#rendering
    if places['hub_p']:
        minitimer=-1
        screen.blit(hub_background,(0,0))
        screen.blit(table.image,table.coordinate)
        screen.blit(aquarium.image,aquarium.coordinate)
        screen.blit(door.image,door.coordinate)

    if places['aquarium_p']:
        minitimer=-1
        screen.blit(aquarium_background,(0,0))
        for i in aquarium_fishs:
            i.move(t,aq_food)
            screen.blit(i.image,i.coordinate)
            if pygame.mouse.get_pressed()[0]:
                (xs,ys)=pygame.mouse.get_pos()
                beta.food((xs,ys))
                aq_food.updatepos((xs,ys))
            if beta.is_food:
                screen.blit(aq_food.image,aq_food.coordinate)



    if places['garden_p']:
        minitimer=-1
        screen.blit(garden_background,(0,0))
        screen.blit(tree.image,tree.coordinate)

    if places['tree_minigame_p']:
        if l<=15 or 30<l<=45:
            screen.blit(tree_minigame_background0,(0,0))
        else:
            screen.blit(tree_minigame_background1,(0,0))
        if minitimer==-1:
            bee=[fish((100,100),(-100,i*200-350),bee_animation,bee_stat,(640,360))for i in range(6)]+[fish((100,100),(1200,i*200-350),bee_animation,bee_stat,(640,360))for i in range(6)]
            guepe=[fish((100,100),(-100,0),guepe_animation,bee_stat,(640,360))]
            beep=guepe+bee

            minitimer=t
        if t-minitimer<4*60:
            screen.blit(bee_image,(random.randint(0,1280),random.randint(0,720)))
        elif t-minitimer<(1*60+13)*60:
            for i in range( len(beep)):
                beep[i].move(t,aq_food)
                screen.blit(beep[i].image,beep[i].coordinate)
                if i<len(beep)-1:
                    if beep[i].is_touching( beep[i+1]):
                        screen.blit(coeur,beep[i].coordinate)
        else:
            bee_question_dialogue.open()


    if places['brique_p']:
        minitimer=-1
        screen.fill('black')



    screen.blit(home.image,home.coordinate)
    if active_dialogue != None:
        active_dialogue.draw(screen)


    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()























