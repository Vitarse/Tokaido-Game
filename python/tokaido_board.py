import pygame, sys, os
import station_effect as se
import random
import csv
import pickle
import time
from button import Button
from classes import Player, Case, Crosshair, Character_select
from fichier import Fichier
from sqlconnectlogin import update_winstat
from sound import Sound


# Init
pygame.init()
pygame.display.set_caption("Plateau Tokaido")
pygame.display.set_icon(pygame.image.load("python/images/sakura.png"))
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((1080,720))

# Crosshair
crosshair = Crosshair("python/images/sakura_flower.png")
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

music = Sound("python/music/theme1.mp3")

# Fonction rotation image
def rotation_image(image,angle):
    """il s'agit d'une fonction qui permet de faire une rotation d'image dans le cas
    où elle serait à l'envers par exemple"""
    location = image.get_rect().center
    rot_sprite = pygame.transform.rotate(image,angle)
    rot_sprite.get_rect().center = location
    return rot_sprite

# Defilement plateau
position = 0
position2 = 0
position_state = False
def scroll_image(bg,bg2,bg3):
    """fonction qui fait défiler les images"""
    global position
    global position2
    global position_state
    screen.fill((0,0,0))
    screen.blit(bg,(position,0))
    screen.blit(bg2,(bg.get_width()+ position,0))
    screen.blit(bg3,(bg.get_width() + bg2.get_width()+ position2,0))
    if position_state == True:
         position -= 10
         position2 -= 10

    elif position_state == False:
         position -=0
         position2 -=0

# Board's backgrounds
background = pygame.image.load("python/images/00.png")
background = pygame.transform.scale(background,(720,1080))
background2 = pygame.image.load("python/images/01.png")
background2 = pygame.transform.scale(background2,(720,1080))
background3 = pygame.image.load("python/images/02.png")
background3 = pygame.transform.scale(background3,(720,1080))

background = rotation_image(background,90)
background2 = rotation_image(background2,90)
background3 = rotation_image(background3,90)


end_bg = pygame.image.load("python/images/end.jpg")

# Couleurs Voyageurs
purple_rgb = (203,49,222)
blue_rgb = (0,127,255)
green_rgb = (22,184,78)
gray_rgb = (160,160,160)
yellow_rgb = (240,195,0)

# Get infos from pregame settings
lp_infos = Fichier("lplayer.dat").lire() # PSEUDO, COLOR, GENDER
gamemode = Fichier("gamemode.dat").lire() #MODE
player_n = len(lp_infos)

# Player class instance
if gamemode == 2:
    fstation = 55
else:
    fstation = 1

if gamemode == 0:
    startmoney = 7
    tuile = None
else:
    l_tuile = [("Kinko", 7), ("Hirotada", 8), ("Yoshiyasu", 9), ("Zen-emon", 6), ("Mitsukuni", 6), ("Sasayakko", 5), ("Umegae", 5), ("Chuubei", 4), ("Satsuki", 2), ("Hiroshige", 3)]
    random.shuffle(l_tuile)

lplayer = []

# Some setups
    # import stations hitboxes x,y pos
fichier_stations = open("python/Stations.py","rb")
Station_dico = pickle.load(fichier_stations)
fichier_stations.close()
    # put them in a list
liste_case = []
for k in range(55):
     case_posx = Station_dico[str(k)][-2]
     case_posy = Station_dico[str(k)][-1]
     case = Case((case_posx,case_posy),k)
     liste_case.append(case)

    # pos x,y of left part of the board for the scroll board function
pos_list = [-900, -895]
pos_listInter = [-1580, -1580]
pos_list2 = [-2140, -2140]

    # double slot stations list
if player_n >= 4:
    ldb_case = [2, 6, 7, 8, 10, 12, 18, 19, 20, 21, 23, 25, 31, 33, 35, 37, 38, 41, 44, 46, 48, 49, 52, 53]
else:
    ldb_case = []

    # relais stations list w/ a specific index
relais = [1,15,28,42,55]
if gamemode == 2:
    a = 3
else:
    a = 1

compteur_case = a
relais_nb = 0

# pour les ecarts de case sur le 1er relais

l_meal = ["Misoshiru", "Misoshiru", "Misoshiru", "Nigirimeshi", "Nigirimeshi", "Nigirimeshi", "Dango", "Dango", "Dango", "Yakitori", "Yakitori", "Soba", "Soba", "Sushi", "Sushi", "Tofu", "Tofu", "Tempura", "Tempura", "Unagi", "Donburi", "Udon", "Fugu", "Tai Meshi", "Sashimi"]
random.shuffle(l_meal)
l_souvenir = ["Koma", "Gofu", "Washi", "Hashi", "Uchiwa", "Yunomi", "Ocha", "Sake", "Konpeito", "Kamaboko", "Daifuku", "Manju", "Netsuke", "Shamisen", "Jubako", "Sumie", "Shikki", "Ukiyoe", "Kan Zashi", "Sandogasa", "Geta", "Haori", "Yukata", "Furoshiki"]
random.shuffle(l_souvenir)
l_meet = ["miko", "miko", "annaibito_mer", "annaibito_mer", "annaibito_mer", "annaibito_mont", "annaibito_mont", "annaibito_riz", "kuge", "kuge", "shokunin", "shokunin", "samurai", "samurai"]
random.shuffle(l_meet)

# Préparatifs gamemode
# 2p, 1er = -1 pièce et 2e = +1 pièce
# 3p, 1er = -1 pièce, 2e = 0 pièce, 3e = +1 pièces
# 4p, 1er = -1 pièce, 2e = 0 pièce, 3e = +1 pièces, 4e = +2 pièces
# 5p, 1er = -1 pièce, 2e = -1 pièce, 3e = +0 pièces, 4e = +1 pièces, 5e = +2 pièces

"""tuiledraw = []
tuiledraw.append(l_tuile[0])
tuiledraw.append(l_tuile[1])
del(l_tuile[0:2])
print(tuiledraw[0][0])
name1 = tuiledraw[0][0]
name2 = tuiledraw[1][0]
character_blit = Character_select(name1,(0,100))
character2_blit = Character_select(name2,(540,100))"""
    
#MAIN LOOP
loop = True

      

def playern_select(n):
    global l_tuile
    global gamemode
    global player_n
    global startmoney
    global tuile
        
    if player_n >= n:
        if gamemode == 0:
            pl = Player(lp_infos[n-1][0], lp_infos[n-1][1], fstation, startmoney, tuile, lp_infos[n-1][2])
            lplayer.append(pl) 
            print(lplayer)         
            selection_statePn = False

        if gamemode !=0:
            tuiledraw = []
            tuiledraw.append(l_tuile[0])
            tuiledraw.append(l_tuile[1])
            del(l_tuile[0:2])
            print(tuiledraw[0][0])
            name1 = tuiledraw[0][0]
            name2 = tuiledraw[1][0]
            character_blit = Character_select(name1,(100,150))
            character2_blit = Character_select(name2,(580,150))
            selection_statePn = True
            while selection_statePn == True:    
                # CHOIX DES TUILES VOYAGEURS
                mouse_pos = pygame.mouse.get_pos()
                screen.fill((255,255,255))    

                text_font = pygame.font.Font(None,80)
                text = text_font.render("Choisir un personnage",None,(0,0,0))
                text_rect = text.get_rect(center=(540,50))
                        
                user_name_font = pygame.font.Font(None,80)
                user_name = user_name_font.render(lp_infos[n-1][0],None,(0,0,0))
                user_name_rect = user_name.get_rect(center=(540,630))

                screen.blit(text,text_rect)
                screen.blit(character_blit.image,character_blit.rect)
                screen.blit(character2_blit.image,character2_blit.rect)
                screen.blit(user_name,user_name_rect)
                crosshair_group.draw(screen)
                crosshair_group.update()
                pygame.display.flip()

                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                                
                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        
                        if character_blit.rect.collidepoint(mouse_pos):
                            tuile_ask = int(1)
                            startmoney = tuiledraw[tuile_ask-1][1]
                            tuile = tuiledraw[tuile_ask-1][0]
                            print(tuiledraw[tuile_ask-1])
                            state = True
                                        
                        elif character2_blit.rect.collidepoint(mouse_pos):
                            tuile_ask = int(2)
                            startmoney = tuiledraw[tuile_ask-1][1]
                            tuile = tuiledraw[tuile_ask-1][0]
                            print(tuiledraw[tuile_ask-1])    
                            state = True
                        else :
                            state = False    
                                    
                        if state == True:    
                            pl = Player(lp_infos[n-1][0], lp_infos[n-1][1], fstation, startmoney, tuile, lp_infos[n-1][2])
                            lplayer.append(pl) 
                            print(lplayer)         
                            selection_statePn = False           

                pygame.time.Clock().tick(144)
                pygame.display.update()       
  
playern_select(1)
playern_select(2)
playern_select(3)
playern_select(4)
playern_select(5)
playern_select(6)
playern_select(7)
random.shuffle(lplayer)

if gamemode == 4:
        selection_compteur = 2
        if player_n == 5:
            lplayer[0].purse -= 1
            lplayer[1].purse -= 1
            #lplayer[2].purse ne change pas
            lplayer[3].purse += 1
            lplayer[4].purse += 2
                        
        elif player_n == 4:
            lplayer[0].purse -= 1
            #lplayer[1].purse ne change pas
            lplayer[2].purse += 1
            lplayer[3].purse += 2

        elif player_n == 3:
            lplayer[0].purse -= 1
            #lplayer[1].purse ne change pas
            lplayer[2].purse += 1

        elif player_n == 2:
            lplayer[0].purse -= 1
            lplayer[1].purse += 1
        for p in lplayer:
                print(p.purse)


gap = f"0.{player_n-1}"
gap = float(gap)
                        
for p in lplayer:
    print(p.locate)
    p.locate -= gap
    p.locate = round(p.locate, 1)
    gap -= 0.1
# Fixing first player turn
current_p = lplayer[0]
print(lplayer[1].pseudo)




coin_img = pygame.image.load("python/images/coin.png")
coin_img = pygame.transform.scale(coin_img, (50,50))
riz_img = pygame.image.load("python/images/paysage/dos_riz.png")
riz_img = pygame.transform.scale(riz_img, (30,50))
mont_img = pygame.image.load("python/images/paysage/dos_mont.png")
mont_img = pygame.transform.scale(mont_img, (30,50))
mer_img = pygame.image.load("python/images/paysage/dos_mer.png")
mer_img = pygame.transform.scale(mer_img, (30,50))
souv_img = pygame.image.load("python/images/dos_souv.jpeg")
souv_img = pygame.transform.scale(souv_img, (30,50))
meet_img = pygame.image.load("python/images/rencontre/dos_meet.png")
meet_img = pygame.transform.scale(meet_img, (30,50))
meal_img = pygame.image.load("python/images/repas/dos_meal.png")
meal_img = pygame.transform.scale(meal_img, (30,50))
amen_img = pygame.image.load("python/images/temple/icon_temple.png")
amen_img = pygame.transform.scale(amen_img, (50,50))
pts_img = pygame.image.load("python/images/baluchon.png")
pts_img = pygame.transform.scale(pts_img, (40,30))



while loop:
    #BLIT BOARD
    scroll_image(background, background2, background3)

    if compteur_case == 1:
          range_compteur = (0, 15)
          """selon la partie du plateau où on se trouve, j'organise la position des cases cliquables (invisibles)"""
          for i in range(range_compteur[1]):
               screen.blit(liste_case[i].surface,liste_case[i].rect)
     
    if compteur_case == 2:
          range_compteur = (15,28)
          for i in range (range_compteur[0],range_compteur[1]):
               screen.blit(liste_case[i].surface,liste_case[i].rect)
     
    if compteur_case == 3:
          range_compteur = (28,42)
          for i in range(range_compteur[0],range_compteur[1]):
               screen.blit(liste_case[i].surface,liste_case[i].rect)
     
    if compteur_case == 4:
          range_compteur = (42,55)
          for i in range(range_compteur[0],range_compteur[1]):
               screen.blit(liste_case[i].surface,liste_case[i].rect)                             

     #c'est comme ça que le défilement s'arrête automatiquement aux position que je souhaite
    if position == pos_list[0]:
        position_state = False
        compteur_case = 2
               
    if position2 == pos_listInter[1]:
        position_state = False
        compteur_case = 3

    if position2 == pos_list2[1]:
        position_state = False
        compteur_case = 4
    #INFOS
    font = pygame.font.Font(None, 40)
    infos_text = font.render("Press i", None, (0,0,0))
    screen.blit(infos_text, (10, 680))    
    #BLIT HUD
    se.hud_set(green_rgb, purple_rgb, yellow_rgb, blue_rgb, gray_rgb, current_p, screen,coin_img,riz_img,mont_img,souv_img,mer_img,meet_img,meal_img,amen_img,pts_img)

    #BLIT PIONS
    if position_state == False:
        for p in lplayer:
            with open('python/board.csv') as board:
                reader = csv.reader(board, delimiter = ';')
                line_count = p.locate
                for row in reader:
                    if a == 1:
                        if str(line_count) == row[0]:
                            p.x = int(row[2])
                            p.y = int(row[3])
                        elif str(float(line_count)) == row[0]:
                            p.x = int(row[2])
                            p.y = int(row[3])

                    elif a == 2:
                        if str(line_count) == row[0]:
                            p.x = int(row[4])
                            p.y = int(row[5])
                        elif str(float(line_count)) == row[0]:
                            p.x = int(row[4])
                            p.y = int(row[5])

                    elif a == 3:
                        if str(line_count) == row[0]:
                            p.x = int(row[6])
                            p.y = int(row[7])
                        elif str(float(line_count)) == row[0]:
                            p.x = int(row[6])
                            p.y = int(row[7])

                    elif a == 4:
                        if str(line_count) == row[0]:
                            p.x = int(row[8])
                            p.y = int(row[9])
                        elif str(float(line_count)) == row[0]:
                            p.x = int(row[8])
                            p.y = int(row[9])

            screen.blit(pygame.image.load(f"python/images/player_{p.color}.png"), (p.x, p.y))
        

    # PYGAME EVENTS DETECTION
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                music.popup_infos()

            elif event.key == pygame.K_m:
                music.change_theme()

            elif event.key == pygame.K_p:
                music.music_on_off()    

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if compteur_case > 0:
                for m in range(range_compteur[1]):
                    case = liste_case[m]
                    if case.rect.collidepoint(mouse_pos):
                        #MOVE STATION
                        move = int(case.nom)+1
                        if se.move_set(move, current_p, relais, a, lplayer, player_n, ldb_case, l_meet, l_souvenir, l_meal, gamemode, screen):
                            
                            # Checking if all players are arrived at next relais
                            nbrelais = 0
                            for p in lplayer:
                                if round(p.locate) == relais[a]:
                                    nbrelais += 1

                            if current_p.locate == relais[a]:
                                current_p.locate -= relais_nb
                                print(current_p.color, current_p.locate)
                                relais_nb += 0.1

                            # Check who's playing next (= farthest player)
                            small_locate = int(100)
                            for p in lplayer:
                                if p.locate < small_locate:
                                    small_locate = p.locate
                                    current_p = p
                            
                            if nbrelais == player_n:
                                a += 1

                                # Check if the game is finished
                                if a == 5:
                                    loop = False

                                print(f"Vous passez maintenant à la {a}e partie du plateau.")
                                l_meal.extend(se.mealdraw)
                                print(l_meal)
                                se.mealdraw = []
                                print(se.mealdraw)

                                relais_nb = 0
                                
                                position_state = True
                                pygame.display.update()

                            print(f'Le joueur {current_p.color} joue')

    pygame.time.Clock().tick(144)
    crosshair_group.draw(screen)
    crosshair_group.update()
    pygame.display.update()



# GAME IS OVER AND WE NEED ADD BONUS POINTS
print("FIN DE PARTIE, PLACE AU CLASSEMENT")

# Add Souvenir points to each player
for p in lplayer:
    se.souvenircheck(p)

# Temple bonus points
se.templebonus(lplayer)

# Add Success points (4 ENDGAME SUCCESS)
# GOURMET, BAIGNEUR, BAVARD, COLLECTIONNEUR

# Results and show the winner
winner = None
lp_result = []
for np in range(len(lplayer)):
    bigger_pts = -1
    for p in lplayer:
        if p.pts > bigger_pts:
            bigger_pts = p.pts
            winner = p
    lp_result.append(winner)
    lplayer.remove(winner)
    

print(f"""

Le joueur {lp_result[0].color} {lp_result[0].pseudo} remporte cette partie avec {lp_result[0].pts}pts !
""")

print("Classement des perdants:")
for other in range(1, len(lp_result)):
    print(f"En {other+1}e, le joueur {lp_result[other].color} {lp_result[other].pseudo} avec {lp_result[other].pts}pts")



pygame.display.set_caption("Classement fin de partie")
screen = pygame.display.set_mode((1280,720))

update_winstat(lp_result[0].pseudo)

while True:
    mouse_pos = pygame.mouse.get_pos()

    screen.blit(end_bg, (0,0))

    congrat_text = pygame.font.Font(None, 50).render("Félicitations !", True, "White")
    firstp_text = pygame.font.Font(None, 50).render(f"Le joueur {lp_result[0].color} {lp_result[0].pseudo} remporte cette partie avec {lp_result[0].pts}pts !", True, lp_result[0].color)
    congrat_rect = congrat_text.get_rect(center=(640, 100))
    firstp_rect = firstp_text.get_rect(center=(640, 200))
    screen.blit(congrat_text, congrat_rect)
    screen.blit(firstp_text, firstp_rect)

    b = 0
    for other in range(1, len(lp_result)):
        others_text = pygame.font.Font(None, 50).render(f"En {other+1}e, le joueur {lp_result[other].color} {lp_result[other].pseudo} avec {lp_result[other].pts}pts", True, lp_result[other].color)
        others_rect = others_text.get_rect(center=(640, 300+b))
        screen.blit(others_text, others_rect)
        b += 50

    back_button = Button(image=None, pos=(640, 350+b), 
                        text_input="BACK TO MAIN MENU", font=pygame.font.Font(None, 100), base_color="White", hovering_color="Pink")

    back_button.changeColor(mouse_pos)
    back_button.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.checkForInput(mouse_pos):
                pygame.quit()
                os.system('cmd /k "menu.bat"')

    pygame.time.Clock().tick(144)

    crosshair_group.draw(screen)
    crosshair_group.update()
    pygame.display.update()

