import random
import csv
import pygame
import time
from classes import Crosshair, Repas, Amen
from button import Button

# Crosshair
crosshair = Crosshair("python/images/sakura_flower.png")
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

riz_complete = 0
mont_complete = 0
mer_complete = 0
riz_first = None
mont_first = None
mer_first = None

# Fonction about landscape effect
def panoramacheck(player, case, screen):

    global riz_complete, mont_complete, mer_complete, riz_first, mont_first, mer_first

    if case == "riziere":
        if player.riz < 3:
            player.riz += 1
            player.pts += player.riz
            print(f"Vous obtenez +1 carte panorama rizière. Total = {player.riz}")

            # RIZ CARD SCREEN
            riz_card = pygame.image.load(f"python/images/paysage/riz{player.riz}.png")
            riz_card = pygame.transform.scale(riz_card, (300, 500))
            screen.fill((255, 255, 255))
            screen.blit(riz_card, (380, 110))
            pygame.display.update()
            time.sleep(1.0)

            # Si panorama rizière complété
            if player.riz == 3:
                print(f"Bravo, le joueur {player.color} a complété le panorama rizière !")
                if riz_complete == 0:
                    riz_first = player
                    riz_first.pts += 3
                    print(f"Le joueur {riz_first.color} {riz_first.pseudo} obtient la carte accomplissement panorama rizière. +3pts bonus !")
                riz_complete += 1
                
            return True
        
        else:
            print("Vous avez déjà complété ce panorama.")
            return False

    elif case == "montagne":
        montagne_img = pygame.image.load("media/montagne.jpg")
        montagne_img = pygame.transform.scale(montagne_img,(500,500))
        if player.mont < 4:
            player.mont += 1
            player.pts += player.mont
            print(f"Vous obtenez +1 carte panorama montagne. Total = {player.mont}")

            # MONT CARD SCREEN
            mont_card = pygame.image.load(f"python/images/paysage/mont{player.mont}.png")
            mont_card = pygame.transform.scale(mont_card, (150, 250))
            screen.fill((255,255,255))
            screen.blit(montagne_img,(0,0))
            screen.blit(mont_card, (380, 110))
            pygame.display.update()
            loop_montagne = True
            while loop_montagne:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            loop_montagne = False

            # Si panorama montagne complété
            if player.mont == 4:
                print(f"Bravo, le joueur {player.color} a complété le panorama montagne !")
                if mont_complete == 0:
                    mont_first = player
                    mont_first.pts += 3
                    print(f"Le joueur {mont_first.color} {mont_first.pseudo} obtient la carte accomplissement panorama montagne. +3pts bonus !")
                mont_complete += 1
                
            return True

        else:
            print("Vous avez déjà complété ce panorama.")
            return False

    elif case == "mer":
        background_mer = pygame.image.load("media/about.jpg")
        background_mer = pygame.transform.scale(background_mer,(1080,720))
        if player.mer < 5:
            player.mer += 1
            player.pts += player.mer
            print(f"Vous obtenez +1 carte panorama mer. Total = {player.mer}")

            # MER CARD SCREEN
            mer_card = pygame.image.load(f"python/images/paysage/mer{player.mer}.png")
            mer_card = pygame.transform.scale(mer_card, (150, 250))
            screen.blit(background_mer,(0,0))
            screen.blit(mer_card, (800, 30))
            pygame.display.update()
            loop_mer = True
            while loop_mer:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            loop_mer = False
                            

            # Si panorama mer complété
            if player.mer == 5:
                print(f"Bravo, le joueur {player.color} a complété le panorama mer !")
                if mer_complete == 0:
                    mer_first = player
                    mer_first.pts += 3
                    print(f"Le joueur {mer_first.color} {mer_first.pseudo} obtient la carte accomplissement panorama mer. +3pts bonus !")
                mer_complete += 1
                
            return True

        else:
            print("Vous avez déjà complété ce panorama.")
            return False



mealdraw = []
relais_nb = 0
# Check the station for applying effect on player
def checkstation(player, case, l_meet, l_souvenir, l_meal, player_n, gamemode, screen):

    global mealdraw, relais_nb

    # Relais
    if case == "relais":

        if player.purse > 0:
            # En fonction du mode de jeu, change ou non le nombre de cartes repas à piocher
            if gamemode == 3:
                n_meal = player_n
            else:
                n_meal = player_n+1

            # Pioche n+1 cartes repas (Tous les autres modes) ou pioche n cartes repas (Mode Gastronomie)
            if len(mealdraw) == 0:
                for meal in range(0, n_meal):
                    mealdraw.append(l_meal[meal])
                del(l_meal[0:3])
            
            print(l_meal)
            print(mealdraw)
            
            small_price = 10
            price = 0
            for m in mealdraw:
                with open('python/repas.csv') as mealcsv:
                    reader = csv.reader(mealcsv, delimiter = ';')
                    for row in reader:
                        if m == row[0]:
                            price = int(row[1])
                
                if price < small_price:
                    small_price = price

            if player.perso == "Kinko":
                small_price -= 1

            if player.purse >= small_price:
                meal_ask = -1
                while not -1 < meal_ask < len(mealdraw)+1:
                    meal_ask = meal_blit(mealdraw, screen)
                    if not -1 < meal_ask < len(mealdraw)+1:
                        print("Entrez une valeur correcte.")
                    
                    elif meal_ask == 0:
                        break

                    else:
                        repas = mealdraw[meal_ask-1]
                        print(repas)
                        with open('python/repas.csv') as mealcsv:
                            reader = csv.reader(mealcsv, delimiter = ';')
                            for row in reader:
                                if repas == row[0]:
                                    price = int(row[1])
                                    print(price)

                        if player.perso == "Kinko":
                            price -= 1

                        if player.purse < price:
                            print("Repas trop cher pour vous ! En choisir un autre")
                            meal_ask = -1

                if meal_ask == 0:
                    print("Vous décidez de ne pas manger.")
                    print(mealdraw)
                
                else:
                    player.purse -= price
                    player.pts += 6
                    player.mealdeck.append(repas)
                    print(f"Vous achetez le repas {repas}, -{price} pièces.")
                    mealdraw.remove(repas)
                    print(mealdraw)

            else:
                print("Vous n'avez pas les moyens d'acheter l'un des repas proposés.")


        else:
            print("Vous n'avez pas d'argent donc aucun achat de repas possible.")
            
        return True
    
    # Echoppe
    if case == "echoppe":
        if player.purse > 0:
            # Pioche 3 cartes souvenirs
            souvdraw = []
            souvdepot = []
            for souv in range(0, 3):
                souvdraw.append(l_souvenir[souv])
            del(l_souvenir[0:3])
            
            print(l_souvenir)
            print(souvdraw)
            
            for s in souvdraw:
                with open('python/souvenir.csv') as souvcsv:
                    reader = csv.reader(souvcsv, delimiter = ';')
                    for row in reader:
                        if s == row[1]:
                            price = int(row[2])

                if player.purse >= price:
                    while True:
                        souv_ask = souv_blit(s, screen)
                        #souv_ask = int(input(f"Voulez-vous acheter le souvenir {s} pour {price} pièces [oui=1 ou non=0] : "))
                        if souv_ask == 0:
                            print("Vous décidez de ne pas l'acheter.")
                            souvdepot.append(s)
                            break

                        elif souv_ask == 1:
                            player.purse -= price
                            player.souvdeck.append(s)
                            print(f"Vous achetez le souvenir {s}, -{price} pièces.")
                            break

                        else:
                            print("Entrez une réponse correcte.")

                else:
                    print(f"Vous n'avez pas les moyens d'acheter ce souvenir: {s} valant {price} pièces")

            random.shuffle(souvdepot)
            l_souvenir.extend(souvdepot)
            print(l_souvenir)
            return True

        else:
            print("Vous ne pouvez pas y aller sans argent.")
            return False
    
    # Temple
    if case == "temple":
        if player.purse > 0:
            depot = 0
            while not 0 < depot < 4 or not player.purse >= depot:
                print("Vous devez déposer un nombre de pièces adéquat avec votre bourse.")
                depot = amen_blit(screen)
                #depot = int(input("Combien de pièces à déposer? [1, 2 ou 3]: "))
            
            player.purse -= depot
            player.amen += depot
            player.pts += depot
            print(f"Vous avez déposé {depot} pièces au temple.")
            return True

        else:
            print("Vous ne pouvez pas y aller sans argent.")
            return False

    # Rencontre
    if case == "rencontre":
        #pioche carte
        meetcard = l_meet[0]
        del(l_meet[0])

        # MEETING CARD SCREEN
        meet_card = pygame.image.load(f"python/images/rencontre/{meetcard.lower()}.png")
        meet_card = pygame.transform.scale(meet_card, (300, 500))
        screen.fill((255, 255, 255))
        screen.blit(meet_card, (380, 110))
        pygame.display.update()
        time.sleep(1.0)

        if meetcard == "miko":
            player.amen += 1
            player.meetdeck.append(meetcard)
            print("Carte Miko, une pièce de la banque est placé sur votre slot temple !")
            return True

        elif meetcard == "annaibito_mer":
            print("Carte Annaibito mer !")
            player.meetdeck.append(meetcard)
            if player.mer == 5:
                print("Vous avez déjà complété le panorama mer.")
                lpano_choice = []
                if player.riz < 3:
                    lpano_choice.append("riziere")
                if player.mont < 4:
                    lpano_choice.append("montagne")

                pano = 0
                while not 0 < pano < len(lpano_choice)+1:
                    pano = int(input(f"Choisir un panorama parmi {lpano_choice} [entrez position numérique du panorama]: "))
                    panoramacheck(player, lpano_choice[pano-1], screen)
                return True
            
            else:
                panoramacheck(player, "mer", screen)
                return True
            

        elif meetcard == "annaibito_mont":
            print("Carte Annaibito montagne !")
            player.meetdeck.append(meetcard)
            if player.mont == 4:
                print("Vous avez déjà complété le panorama montagne.")
                lpano_choice = []
                if player.riz < 3:
                    lpano_choice.append("riziere")
                if player.mer < 5:
                    lpano_choice.append("mer")

                pano = 0
                while not 0 < pano < len(lpano_choice)+1:
                    pano = int(input(f"Choisir un panorama parmi {lpano_choice} [entrez position numérique du panorama]: "))
                    panoramacheck(player, lpano_choice[pano-1], screen)
                return True
            
            else:
                panoramacheck(player, "montagne", screen)
                return True

        elif meetcard == "annaibito_riz":
            print("Carte Annaibito rizière !")
            player.meetdeck.append(meetcard)
            if player.riz == 3:
                print("Vous avez déjà complété le panorama rizière.")
                lpano_choice = []
                if player.mer < 5:
                    lpano_choice.append("mer")
                if player.mont < 4:
                    lpano_choice.append("montagne")

                pano = 0
                while not 0 < pano < len(lpano_choice)+1:
                    pano = int(input(f"Choisir un panorama parmi {lpano_choice} [entrez position numérique du panorama]: "))
                    panoramacheck(player, lpano_choice[pano-1], screen)
                return True
            
            else:
                panoramacheck(player, "riziere", screen)
                return True

        elif meetcard == "kuge":
            player.purse += 3
            player.meetdeck.append(meetcard)
            print("Carte Kuge, vous gagnez 3 pièces !")
            return True

        elif meetcard == "shokunin":
            alea = random.randint(0, len(l_souvenir))
            player.souvdeck.append(l_souvenir[alea])
            l_souvenir.remove(l_souvenir[alea])
            player.meetdeck.append(meetcard)
            print("Carte Shokunin, vous gagnez 1 carte souvenir aléatoire !")
            return True

        elif meetcard == "samurai":
            player.pts += 3
            player.meetdeck.append(meetcard)
            print("Carte Samurai, vous gagnez 3 points !")
            return True

    # Ferme
    if case == "ferme":
        player.purse += 3
        print("Vous gagnez 3 pièces.")
        gold = pygame.image.load(f"python/images/temple/amen3.png")
        gold = pygame.transform.scale(gold, (200, 200))
        screen.fill((255, 255, 255))
        screen.blit(gold, (440, 250))
        pygame.display.update()
        time.sleep(1.0)
        return True

    # Source chaude
    if case == "source":
        #pioche carte
        sccard = random.randint(2,3)
        player.pts += sccard
        print(f"Vous piochez une carte source chaude valant {sccard} points. +{sccard}pts !")
        sc_card = pygame.image.load(f"python/images/source/sc{sccard}.png")
        sc_card = pygame.transform.scale(sc_card, (300, 500))
        screen.fill((255, 255, 255))
        screen.blit(sc_card, (380, 110))
        pygame.display.update()
        time.sleep(1.0)
        return True

    # Rizière
    if case == "riziere" or "montagne" or "mer":
        if panoramacheck(player, case, screen):
            return True
        else:
            return False



# Count all souvenir points at the end of the game
def souvenircheck(player):
    l = []
    l2 = []
    i = 0
    points = 0

    if len(player.souvdeck) != 0:

        for souv in player.souvdeck:
            with open('python/souvenir.csv') as souvcsv:
                reader = csv.reader(souvcsv, delimiter = ';')
                for row in reader:
                    if souv == row[1]:
                        fam = int(row[0])
                        l.append(fam)

        if len(l) <= 4:
            i = 1
        if 4 < len(l) <= 8:
            i = 2
        if 8 < len(l) <= 12:
            i = 3
        if 12 < len(l) <= 16:
            i = 4
        if 16 < len(l) <= 20:
            i = 5
        if 20 < len(l) <= 24:
            i = 6

        for n in range(i):
            for fam1 in l:
                if not fam1 in l2:
                    l2.append(fam1)

            for fam2 in l2:
                l.remove(fam2)
            print(l2)
        
            points += ((len(l2)*2) - 1) #petite suite arithmétique (GROS FLEX)
            l2 = []
            print(points)
        
        player.pts += points
        print(f"Le joueur {player.color} gagne {points}pts avec ses cartes souvenirs !")

    else:
        print(f"Aucun souvenir dans la collection du joueur {player.color}.")



# Temple bonus points function
def templebonus(lplayer):

    lp = []
    for p in lplayer:
        lp.append(p)
    
    # Range dans l'ordre décroissant les scores d'offrandes et les joueurs associés
    bigamen = None
    l_amen = []
    l_amen_player = []
    for np in range(len(lp)):
        bigger_amen = -1
        for p in lp:
            if p.amen > bigger_amen:
                bigger_amen = p.amen
                bigamen = p
        l_amen.append(bigger_amen)
        l_amen_player.append(bigamen)
        lp.remove(bigamen)
        # EN FAIT CE CODE EST BON

    # Permet de détecter les égalités d'offrande
    l_verif = [[], [], [], [], []]
    l_verif_player = [[], [], [], [], []]

    for e in l_amen:
        b = 0
        ind = 0
        for nb in range(len(l_amen)):
            if e in l_verif[nb]:
                pass

            else:
                if b == 0:
                    l_verif[l_amen.index(e)].append(e)
                    l_verif_player[l_amen.index(e)].append(l_amen_player[ind])
                    print(l_amen.index(e))
                    b = 1

            ind += 1

    print(l_verif)
    print(l_verif_player)

    # Ajout des points bonus pour le temple
    i = 0
    for lilp in l_verif_player:
        if len(lilp) != 0 and not all(x.amen in (0,0) for x in lilp):
            if i == 0:
                for p in lilp:
                    p.pts += 10
                    print(f"joueur {p.color} +10pts bonus temple")
            if i == 1:
                for p in lilp:
                    p.pts += 7
                    print(f"joueur {p.color} +7pts bonus temple")
            if i == 2:
                for p in lilp:
                    p.pts += 4
                    print(f"joueur {p.color} +4pts bonus temple")
            if i == 3:
                for p in lilp:
                    p.pts += 2
                    print(f"joueur {p.color} +2pts bonus temple")
            i += 1
        elif all(x.amen in (0,0) for x in lilp):
            for p in lilp:
                print(f"Pas de points pour le joueur {p.color} car pas d'offrande")



# SUCCESS FUNCTION !


#MOVE FONCTION
def move_set(move,current_p, relais, a, lplayer, player_n, ldb_case, l_meet, l_souvenir, l_meal, gamemode, screen):

    if not move <= current_p.locate or move > relais[a]:
        double = False

        # Read CSV for board stations
        case = None
        with open('python/board.csv') as board:
            reader = csv.reader(board, delimiter = ';')
            line_count = move
            for row in reader:
                if str(line_count) == row[0]:
                    case = row[1]
                elif str(float(line_count)) == row[0]:
                    case = row[1]
            
        # Check if move is legally possible and legal = apply effect, else loop again
        if move > current_p.locate and move <= relais[a]:
            for p in lplayer:
                if move == p.locate and move != relais[a]:
                    if player_n >= 4:
                        count = 0
                        for p2 in lplayer:
                            if move-0.5 < p2.locate < move+0.5:
                                count += 1
                        if count < 2:
                            for num in ldb_case:
                                if num == move:
                                    double = True
                                    break
                            if double:
                                move = float(move)
                                move -= 0.1
                            else:
                                print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                                return False
                        else:
                            print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                            return False
                    else:
                        print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                        return False
            if move != 0:
                if not checkstation(current_p, case, l_meet, l_souvenir, l_meal, player_n, gamemode, screen):
                    return False
                else:
                    # Move player
                    if type(move) != "float":
                        current_p.locate = float(move)
                    else:
                        current_p.locate = move
                    if double:
                        move += 0.1
                        move = int(move)
                        double = False
                    if case == "relais":
                        move = round(move)
                    print(f"Le joueur {current_p.color} est sur une case {case} situé à {move}.")
                    return True

        else:
            print('Pas de retour en arrière ni de dépassement de relais !')
            return False

    else:
        print('Pas de retour en arrière ni de dépassement de relais !')
        return False
    


#HUD FONCTION
def hud_set(green, purple, yellow, blue, gray, player, screen,coin_img,riz_img,mont_img,souv_img,mer_img,meet_img,meal_img,amen_img,pts_img):
    hud_color = None

    if player.color == "green":
        hud_color = green
    elif player.color == "purple":
        hud_color = purple
    elif player.color == "yellow":
        hud_color = yellow
    elif player.color == "blue":
        hud_color = blue
    elif player.color == "gray":
        hud_color = gray

    hud = pygame.Surface((1280,75))
    hud.fill(hud_color)
    rect = hud.get_rect(topleft= (0,0))

    font = pygame.font.Font(None, 40)
    pseudo_text = font.render(str(player.pseudo), None, (0,0,0))
    money_text = font.render(str(player.purse), None, (0,0,0))
    riz_text = font.render(str(player.riz), None, (0,0,0))
    mont_text = font.render(str(player.mont), None, (0,0,0))
    mer_text = font.render(str(player.mer), None, (0,0,0))
    souv_text = font.render(str(len(player.souvdeck)), None, (0,0,0))
    meet_text = font.render(str(len(player.meetdeck)), None, (0,0,0))
    meal_text = font.render(str(len(player.mealdeck)), None, (0,0,0))
    amen_text = font.render(str(player.amen), None, (0,0,0))
    pts_text = font.render(str(player.pts), None, (0,0,0))

    
    if player.perso != None:
        tuile_img = pygame.image.load(f"python/images/tuiles/{player.perso}.png")
        tuile_img = pygame.transform.scale(tuile_img, (110,160))

        bindle_img = pygame.image.load(f"python/images/baluchons/bindle_{player.color}.png")
        bindle_img = pygame.transform.scale(bindle_img, (30,30))

        screen.blit(tuile_img, (0, 75))
        screen.blit(bindle_img, (6, 83))
        

    screen.blit(hud, rect)

    screen.blit(coin_img, (25,12))
    screen.blit(money_text, (80,25))
    
    screen.blit(riz_img, (125,12))
    screen.blit(riz_text, (160,25))
    
    screen.blit(mont_img, (205,12))
    screen.blit(mont_text, (240,25))
    
    screen.blit(mer_img, (285,12))
    screen.blit(mer_text, (320,25))

    screen.blit(souv_img, (365,12))
    screen.blit(souv_text, (400,25))

    screen.blit(meet_img, (445,12))
    screen.blit(meet_text, (480,25))

    screen.blit(meal_img, (525,12))
    screen.blit(meal_text, (560,25))

    screen.blit(amen_img, (595,12))
    screen.blit(amen_text, (650,25))

    screen.blit(pts_img, (775,20))
    screen.blit(pts_text, (825,25))

    screen.blit(pseudo_text, (875,25))


# RELAIS SCREEN
def meal_blit(meals, screen):
    comptoir_img = pygame.image.load("media/comptoir.jpg")
    comptoir_img = pygame.transform.scale(comptoir_img,(1080,720))

    ask = 0
    meal_loop = True
    while meal_loop:
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(comptoir_img,(0,0))

        font = pygame.font.Font(None, 80)
        info_text = font.render("Choisir un Repas", None, (0,0,0))
        info_rect = info_text.get_rect(center=(540, 170))
        screen.blit(info_text, info_rect)

        non_button = Button(image=None, pos=(540, 660), 
                        text_input="NE PAS ACHETER", font=pygame.font.Font(None, 100), base_color="Black", hovering_color="Red")

        non_button.changeColor(mouse_pos)
        non_button.update(screen)


        c = 0
        if len(meals) == 1:
            for meal in meals:
                m = Repas(f"python/images/repas/{meal.lower()}.png", (500, 380))
                screen.blit(m.image, m.pos)
                screen.blit(m.surface, m.rect)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if m.rect.collidepoint(mouse_pos):
                            print(f"CARTE TROUVEE, numero {meals.index(meal)+1}")
                            ask = meals.index(meal)+1
                            meal_loop = False

        elif len(meals) == 2:
            for meal in meals:
                m = Repas(f"python/images/repas/{meal.lower()}.png", (420+c, 380))
                screen.blit(m.image, m.pos)
                screen.blit(m.surface, m.rect)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if m.rect.collidepoint(mouse_pos):
                            print(f"CARTE TROUVEE, numero {meals.index(meal)+1}")
                            ask = meals.index(meal)+1
                            meal_loop = False

                c += 150
        elif len(meals) == 3:
            for meal in meals:
                m = Repas(f"python/images/repas/{meal.lower()}.png", (330+c, 380))
                screen.blit(m.image, m.pos)
                screen.blit(m.surface, m.rect)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if m.rect.collidepoint(mouse_pos):
                            print(f"CARTE TROUVEE, numero {meals.index(meal)+1}")
                            ask = meals.index(meal)+1
                            meal_loop = False
                c += 150

        elif len(meals) == 4:
            for meal in meals:
                m = Repas(f"python/images/repas/{meal.lower()}.png", (250+c, 380))
                screen.blit(m.image, m.pos)
                screen.blit(m.surface, m.rect)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if m.rect.collidepoint(mouse_pos):
                            print(f"CARTE TROUVEE, numero {meals.index(meal)+1}")
                            ask = meals.index(meal)+1
                            meal_loop = False
                c += 150

        elif len(meals) == 5:
            for meal in meals:
                m = Repas(f"python/images/repas/{meal.lower()}.png", (170+c, 380))
                screen.blit(m.image, m.pos)
                screen.blit(m.surface, m.rect)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if m.rect.collidepoint(mouse_pos):
                            print(f"CARTE TROUVEE, numero {meals.index(meal)+1}")
                            ask = meals.index(meal)+1
                            meal_loop = False
                c += 150

        elif len(meals) == 6:
            for meal in meals:
                m = Repas(f"python/images/repas/{meal.lower()}.png", (100+c, 380))
                screen.blit(m.image, m.pos)
                screen.blit(m.surface, m.rect)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if m.rect.collidepoint(mouse_pos):
                            print(f"CARTE TROUVEE, numero {meals.index(meal)+1}")
                            ask = meals.index(meal)+1
                            meal_loop = False
                c += 150

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if non_button.checkForInput(mouse_pos):
                    ask = 0
                    meal_loop = False

        pygame.time.Clock().tick(144)

        crosshair_group.draw(screen)
        crosshair_group.update()
        pygame.display.update()

    return ask

# SOUVENIR SCREEN
def souv_blit(souv, screen):

    s = pygame.image.load(f"python/images/souvenir/{souv.lower()}.png")
    s = pygame.transform.scale(s, (210, 350))
    
    souv_loop = True
    while souv_loop:
        mouse_pos = pygame.mouse.get_pos()

        screen.fill((255,255,255))
        screen.blit(s, (410, 160))

        font = pygame.font.Font(None, 80)
        info_text = font.render("Acheter le souvenir ?", None, (0,0,0))
        info_rect = info_text.get_rect(center=(540, 100))
        screen.blit(info_text, info_rect)

        non_button = Button(image=None, pos=(400, 600), 
                        text_input="NON", font=pygame.font.Font(None, 100), base_color="Black", hovering_color="Red")

        non_button.changeColor(mouse_pos)
        non_button.update(screen)

        oui_button = Button(image=None, pos=(680, 600), 
                        text_input="OUI", font=pygame.font.Font(None, 100), base_color="Black", hovering_color="Green")

        oui_button.changeColor(mouse_pos)
        oui_button.update(screen)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if non_button.checkForInput(mouse_pos):
                    ask = 0
                    souv_loop = False

                if oui_button.checkForInput(mouse_pos):
                    ask = 1
                    souv_loop = False

        pygame.time.Clock().tick(144)

        crosshair_group.draw(screen)
        crosshair_group.update()
        pygame.display.update()

    return ask


def amen_blit(screen):

    ask = 0
    amen_loop = True
    while amen_loop:
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((255,255,255))

        font = pygame.font.Font(None, 80)
        info_text = font.render("Choisir une Offrande", None, (0,0,0))
        info_rect = info_text.get_rect(center=(540, 100))
        screen.blit(info_text, info_rect)
        
        c = 0
        for amen in range(1, 4):
            am = Amen(f"python/images/temple/amen{amen}.png", (275+c, 280))
            screen.blit(am.image, am.pos)
            screen.blit(am.surface, am.rect)
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if am.rect.collidepoint(mouse_pos):
                        print(f"AMEN = {amen} pieces")
                        ask = amen
                        amen_loop = False
            c += 175

        pygame.time.Clock().tick(144)

        crosshair_group.draw(screen)
        crosshair_group.update()
        pygame.display.update()

    return ask