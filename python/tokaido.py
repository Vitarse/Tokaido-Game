import random
import csv
from classes import Player
import station_effect as se

# Starting game menu
print("""==========TOKAIDO==========

Bienvenue à toi voyageur !

Choisis un mode de jeu: [0/1/2/3/4]
0) Voyage Initiatique ✓
1) Mode Normal X
2) Trajet Retour ✓
3) Gastronomie ✓
4) Préparatifs ✓
    """)

travel_init = False
normal_mode = False
back_travel = False
gastro_mode = False
setup_mode = False
# Gamemode choice
while True:    
    gamemode = int(input("Mode de jeu: "))

    if gamemode == 0:
        travel_init = True
        print("Mode: Voyage Initiatique")
        break

    elif gamemode == 1:
        normal_mode = True
        print("Mode Normal. En cours de développement")
        break

    elif gamemode == 2:
        back_travel = True
        print("Mode: Trajet Retour")
        break

    elif gamemode == 3:
        gastro_mode = True
        print("Mode: Gastronomie")
        break

    elif gamemode == 4:
        setup_mode = True
        print("Mode: Préparatifs")
        break
    
    else:
        print("Entrez une valeur correcte.")

# Player number
player_n = 0
while not 1 < player_n < 6:
    player_n = int(input("Nombre de joueurs: "))
    if not 1 < player_n < 6:
        print("Le nombre de joueurs doit être entre 2 et 5.")

# Player color
l_color = ['purple', 'yellow', 'green', 'gray', 'blue']
lplayer_color = []
print(l_color)
for player in range(1, player_n+1):
    loop = True
    while loop:
        ask_color = input(f"Couleur joueur {player}: ")
        for color in l_color:
            if ask_color == color:
                l_color.remove(f'{color}')
                lplayer_color.append(f'{color}')
                loop = False

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
for p in range(1, player_n+1):
    ask_pseudo = input(f"Pseudo du joueur {lplayer_color[p-1]}: ")
    if gamemode != 0: # CHOIX DES TUILES VOYAGEURS
        tuiledraw = []
        tuiledraw.append(l_tuile[0])
        tuiledraw.append(l_tuile[1])
        del(l_tuile[0:2])
        print(tuiledraw)
        tuile_ask = 0
        while not 0 < tuile_ask < 3:
            tuile_ask = int(input("Quelle tuile voulez-vous choisir ? [entrez position numérique de la tuile] : "))
            if not 0 < tuile_ask < 3:
                print("Entrez une valeur correcte.")
        startmoney = tuiledraw[tuile_ask-1][1]
        tuile = tuiledraw[tuile_ask-1][0]
        print(tuiledraw[tuile_ask-1])
    pl = Player(ask_pseudo, lplayer_color[p-1], fstation, startmoney, tuile, "Human")
    lplayer.append(pl)

# Player shuffle for starting
random.shuffle(lplayer)

for p in lplayer:
    p.afficher()

# Some setups 
if player_n >= 4:
    ldb_case = [2, 6, 7, 8, 10, 12, 18, 19, 20, 21, 23, 25, 31, 33, 35, 37, 38, 41, 44, 46, 48, 49, 52, 53]

relais = [1,15,28,42,55]
if gamemode == 2:
    a = 3
else:
    a = 1

l_meal = ["Misoshiru", "Misoshiru", "Misoshiru", "Nigirimeshi", "Nigirimeshi", "Nigirimeshi", "Dango", "Dango", "Dango", "Yakitori", "Yakitori", "Soba", "Soba", "Sushi", "Sushi", "Tofu", "Tofu", "Tempura", "Tempura", "Unagi", "Donburi", "Udon", "Fugu", "Tai Meshi", "Sashimi"]
random.shuffle(l_meal)
l_souvenir = ["Koma", "Gofu", "Washi", "Hashi", "Uchiwa", "Yunomi", "Ocha", "Sake", "Konpeito", "Kanaboko", "Daifuku", "Manju", "Netsuke", "Shamisen", "Jubako", "Sumie", "Shikki", "Ukiyoe", "Kanzashi", "Sandogasa", "Geta", "Haori", "Yukata", "Furoshiki"]
random.shuffle(l_souvenir)
l_meet = ["miko", "miko", "annaibito_mer", "annaibito_mer", "annaibito_mer", "annaibito_mont", "annaibito_mont", "annaibito_riz", "kuge", "kuge", "shokunin", "shokunin", "samurai", "samurai"]
random.shuffle(l_meet)


# Fixing first player turn
current_p = lplayer[0]

# Voyage Initiatique gamemode
while travel_init:

    print(f'Le joueur {current_p.color} joue')


    # Asking for a station
    move = 0
    while move <= current_p.locate or move > relais[a]:
        double = False
        move = int(input("Quelle station? : "))

        # Read CSV for board stations
        with open('python/board.csv') as board:
            reader = csv.reader(board, delimiter = ';')
            line_count = move
            for row in reader:
                if str(line_count) == row[0]:
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
                                move = 0
                        else:
                            print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                            move = 0
                    else:
                        print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                        move = 0
            if move != 0:
                if not se.checkstation(current_p, case, l_meet, l_souvenir, l_meal, player_n, gamemode):
                    move = 0
        else:
            print('Pas de retour en arrière ni de dépassement de relais !')
        
    # Move player
    current_p.locate = move
    if double:
        move += 0.1
        move = int(move)
        double = False
    print(f"Le joueur {current_p.color} est sur une case {case} situé à {move}.")

    # Check who's playing next (= farthest player)
    small_locate = 100
    for p in lplayer:
        if p.locate < small_locate:
            small_locate = p.locate
            current_p = p

    # Checking if all players are arrived at next relais
    nbrelais = 0
    for p in lplayer:
        if p.locate == relais[a]:
            nbrelais += 1
    
    if nbrelais == player_n:
        a += 1
        # Check if the game is finished
        if a == 5:
            break
        print(f"Vous passez maintenant à la {a}e partie du plateau.")
        l_meal.extend(se.mealdraw)
        print(l_meal)
        se.mealdraw = []
        print(se.mealdraw)
        nbrelais = 0

# Mode Normal gamemode (le mode 0 mais avec les persos)
while normal_mode:

    print(f'Le joueur {current_p.color} joue')


    # Asking for a station
    move = 0
    while move <= current_p.locate or move > relais[a]:
        double = False
        move = int(input("Quelle station? : "))

        # Read CSV for board stations
        with open('python/board.csv') as board:
            reader = csv.reader(board, delimiter = ';')
            line_count = move
            for row in reader:
                if str(line_count) == row[0]:
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
                                move = 0
                        else:
                            print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                            move = 0
                    else:
                        print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                        move = 0
            if move != 0:
                if not se.checkstation(current_p, case, l_meet, l_souvenir, l_meal, player_n, gamemode):
                    move = 0
        else:
            print('Pas de retour en arrière ni de dépassement de relais !')
        
    # Move player
    current_p.locate = move
    if double:
        move += 0.1
        move = int(move)
        double = False
    print(f"Le joueur {current_p.color} est sur une case {case} situé à {move}.")

    # Check who's playing next (= farthest player)
    small_locate = 100
    for p in lplayer:
        if p.locate < small_locate:
            small_locate = p.locate
            current_p = p

    # Checking if all players are arrived at next relais
    nbrelais = 0
    for p in lplayer:
        if p.locate == relais[a]:
            nbrelais += 1
    
    if nbrelais == player_n:
        a += 1
        # Check if the game is finished
        if a == 5:
            break
        print(f"Vous passez maintenant à la {a}e partie du plateau.")
        l_meal.extend(se.mealdraw)
        print(l_meal)
        se.mealdraw = []
        print(se.mealdraw)
        nbrelais = 0

# Trajet Retour gamemode
while back_travel:

    print(f'Le joueur {current_p.color} joue')

    # Asking for a station
    move = 56
    while move >= current_p.locate or move < relais[a]:
        double = False
        move = int(input("Quelle station? : "))

        # Read CSV for board stations
        with open('python/board.csv') as board:
            reader = csv.reader(board, delimiter = ';')
            line_count = move
            for row in reader:
                if str(line_count) == row[0]:
                    case = row[1]
            
        # Check if move is legally possible and legal = apply effect, else loop again
        if move < current_p.locate and move >= relais[a]:
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
                                move += 0.1
                            else:
                                print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                                move = 56
                        else:
                            print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                            move = 56
                    else:
                        print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                        move = 56
            if move != 56:
                if not se.checkstation(current_p, case, l_meet, l_souvenir, l_meal, player_n, gamemode):
                    move = 56
        else:
            print('Pas de retour en arrière ni de dépassement de relais !')
        
    # Move player
    current_p.locate = move
    if double:
        move -= 0.1
        move = int(move)
        double = False
    print(f"Le joueur {current_p.color} est sur une case {case} situé à {move}.")

    # Check who's playing next (= farthest player)
    big_locate = 0
    for p in lplayer:
        if p.locate > big_locate:
            big_locate = p.locate
            current_p = p

    # Checking if all players are arrived at next relais
    nbrelais = 0
    for p in lplayer:
        if p.locate == relais[a]:
            nbrelais += 1
    
    if nbrelais == player_n:
        a -= 1
        # Check if the game is finished
        if a == -1:
            break
        print(f"Vous passez maintenant à la {a+1}e partie du plateau.")
        l_meal.extend(se.mealdraw)
        print(l_meal)
        se.mealdraw = []
        print(se.mealdraw)
        nbrelais = 0

# Gastronomie gamemode
while gastro_mode:

    print(f'Le joueur {current_p.color} joue')

    # Asking for a station
    move = 0
    while move <= current_p.locate or move > relais[a]:
        double = False
        move = int(input("Quelle station? : "))

        # Read CSV for board stations
        with open('python/board.csv') as board:
            reader = csv.reader(board, delimiter = ';')
            line_count = move
            for row in reader:
                if str(line_count) == row[0]:
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
                                move = 0
                        else:
                            print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                            move = 0
                    else:
                        print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                        move = 0
            if move != 0:
                if not se.checkstation(current_p, case, l_meet, l_souvenir, l_meal, player_n, gamemode):
                    move = 0
        else:
            print('Pas de retour en arrière ni de dépassement de relais !')
        
    # Move player
    current_p.locate = move
    if double:
        move += 0.1
        move = int(move)
        double = False
    print(f"Le joueur {current_p.color} est sur une case {case} situé à {move}.")

    # Check who's playing next (= farthest player)
    small_locate = 100
    for p in lplayer:
        if p.locate < small_locate:
            small_locate = p.locate
            current_p = p

    # Checking if all players are arrived at next relais
    nbrelais = 0
    for p in lplayer:
        if p.locate == relais[a]:
            nbrelais += 1
    
    if nbrelais == player_n:
        a += 1
        # Check if the game is finished
        if a == 5:
            break
        print(f"Vous passez maintenant à la {a}e partie du plateau.")
        l_meal.extend(se.mealdraw)
        print(l_meal)
        se.mealdraw = []
        print(se.mealdraw)
        nbrelais = 0

# Préparatifs gamemode
# 2p, 1er = -1 pièce et 2e = +1 pièce
# 3p, 1er = -1 pièce, 2e = 0 pièce, 3e = +1 pièces
# 4p, 1er = -1 pièce, 2e = 0 pièce, 3e = +1 pièces, 4e = +2 pièces
# 5p, 1er = -1 pièce, 2e = -1 pièce, 3e = +0 pièces, 4e = +1 pièces, 5e = +2 pièces
if gamemode == 4:
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

while setup_mode:

    print(f'Le joueur {current_p.color} joue')

    # Asking for a station
    move = 0
    while move <= current_p.locate or move > relais[a]:
        double = False
        move = int(input("Quelle station? : "))

        # Read CSV for board stations
        with open('python/board.csv') as board:
            reader = csv.reader(board, delimiter = ';')
            line_count = move
            for row in reader:
                if str(line_count) == row[0]:
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
                                move = 0
                        else:
                            print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                            move = 0
                    else:
                        print(f"vous ne pouvez pas aller sur cette case, elle est occupée par le joueur {p.color} !")
                        move = 0
            if move != 0:
                if not se.checkstation(current_p, case, l_meet, l_souvenir, l_meal, player_n, gamemode):
                    move = 0
        else:
            print('Pas de retour en arrière ni de dépassement de relais !')
        
    # Move player
    current_p.locate = move
    if double:
        move += 0.1
        move = int(move)
        double = False
    print(f"Le joueur {current_p.color} est sur une case {case} situé à {move}.")

    # Check who's playing next (= farthest player)
    small_locate = 100
    for p in lplayer:
        if p.locate < small_locate:
            small_locate = p.locate
            current_p = p

    # Checking if all players are arrived at next relais
    nbrelais = 0
    for p in lplayer:
        if p.locate == relais[a]:
            nbrelais += 1
    
    if nbrelais == player_n:
        a += 1
        # Check if the game is finished
        if a == 5:
            break
        print(f"Vous passez maintenant à la {a}e partie du plateau.")
        l_meal.extend(se.mealdraw)
        print(l_meal)
        se.mealdraw = []
        print(se.mealdraw)
        nbrelais = 0


# GAME IS OVER AND WE NEED ADD BONUS POINTS

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
Félicitations !
Le joueur {lp_result[0].color} {lp_result[0].pseudo} remporte cette partie avec {lp_result[0].pts}pts !
""")

print("Classement des perdants:")
for other in range(1, len(lp_result)):
    print(f"En {other+1}e, le joueur {lp_result[other].color} {lp_result[other].pseudo} avec {lp_result[other].pts}pts")

print("\nstopping script")