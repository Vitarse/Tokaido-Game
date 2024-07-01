import pygame, os, sys
import pygame_menu
from classes import Crosshair
from fichier import Fichier
from sqlconnectlogin import get_lplayer

pygame.init()
pygame.display.set_caption("Game settings")
pygame.display.set_icon(pygame.image.load("python/images/sakura.png"))
pygame.mouse.set_visible(False)
surface = pygame.display.set_mode((1280, 720))

# crosshair
crosshair = Crosshair("python/images/sakura_flower.png")
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# GO BACK TO TOKAIDO MENU
def back_mainmenu():
    pygame_menu.events.EXIT
    pygame.quit()
    os.system('cmd /k "menu.bat"')
    

# FUNCTIONS GET VALUES
def set_difficulty(selected, value) -> None:
    global mode

    """
    Set the difficulty of the game.
    """
    print(f'Set difficulty to {selected[0][0]} ({value})')
    mode = value

def set_player_nbr(selected, value) -> None:
    global n_player

    """
    Set the number of players in the game.
    """
    print(f'Set player number to {selected[0][0]} ({value})')
    n_player = value

def set_color(selected, value) -> None:
    global color

    """
    Set the color of players in the game.
    """
    print(f'Set player color to {selected[0][0]} ({value})')
    color = selected[0]

def set_pseudo(selected, value) -> None:
    global pseudo

    """
    Set the pseudo of players in the game.
    """
    print(f'Set player pseudo to {selected[0][0]} ({value})')
    pseudo = selected[0]

def set_gender(selected, value) -> None:
    global gender
    global change

    """
    Set the gender of players in the game.
    """
    print(f'Set player gender to {selected[0][0]} ({value})')
    gender = selected[0][0]
    change = True



# LOOP MENUS
def main_menu():

    global mode

    mode = 0

    menu.select_widget(None)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        # Draw the menu
        surface.fill((25, 0, 50))

        menu.update(events)
        menu.draw(surface)

        crosshair_group.draw(surface)
        crosshair_group.update()
        pygame.display.flip()

def menu_nbr_player():
    global n_player
    n_player = 2

    menu2.select_widget(None)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        # Draw the menu
        surface.fill((25, 0, 50))

        menu2.update(events)
        menu2.draw(surface)

        crosshair_group.draw(surface)
        crosshair_group.update()
        pygame.display.flip()

def menu_color():

    global color

    l_color = [('purple', 1), ('yellow', 2), ('green', 3), ('gray', 4), ('blue', 5)]
    lp_color = []
    for n in range(1, n_player+1):
        
        color = l_color[0]

        menu3.add.selector(f'Couleur joueur {n}: ', l_color, onchange=set_color)
        menu3.add.text_input('Press X key to valid', maxchar=1)
        menu3.add.button('Quit', back_mainmenu)

        menu3.select_widget(None)

        tr = True
        while tr:

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        print("X")
                        tr = False

            # Draw the menu
            menu3.update(events)
            menu3.draw(surface)

            crosshair_group.draw(surface)
            crosshair_group.update()
            pygame.display.flip()

        
        menu3.clear()
        print(color)
        lp_color.append(color[0])
        print(lp_color)
        l_color.remove(color)
        pygame.display.update()

    menu_player(lp_color)
        
    
def menu_player(lp_color):
    global pseudo
    global gender
    global change

    l_pseudo = get_lplayer()
    lp_pseudo = []
    lplayer = []
    for n in range(0, n_player):
        
        pseudo = l_pseudo[0]
        gender = 'Human'
        change = False

        menu4.add.selector(f'Pseudo joueur {lp_color[n]}: ', l_pseudo, onchange=set_pseudo)
        menu4.add.selector('Genre: ', [('Human', 0)])
        #menu4.add.selector('Genre: ', [('Human', 0), ('Computer', 1)], onchange=set_gender)
        menu4.add.text_input('Press X key to valid', maxchar=1)
        menu4.add.button('Quit', back_mainmenu)

        menu4.select_widget(None)

        tr = True
        while tr:
            
            if change:
                if gender == 'Human':
                    menu4.clear()
                    menu4.add.selector(f'Pseudo joueur {lp_color[n]}: ', l_pseudo, onchange=set_pseudo)
                    menu4.add.selector('Genre: ', [('Human', 0), ('Computer', 1)], onchange=set_gender)
                    menu4.add.text_input('Press X key to valid', maxchar=1)
                    menu4.add.button('Quit', back_mainmenu)
                    change = False
                    menu4.update(events)
                    menu4.draw(surface)
                    pygame.display.update()

                elif gender == 'Computer':
                    menu4.clear()
                    pseudo_ordi = menu4.add.text_input(f'Pseudo ordinateur {n+1}: ', default=f'Ordi {n+1}', maxchar=10)
                    menu4.add.selector('Genre: ', [('Computer', 1), ('Human', 0)], onchange=set_gender)
                    menu4.add.text_input('Press X key to valid', maxchar=1)
                    menu4.add.button('Quit', back_mainmenu)
                    change = False
                    menu4.update(events)
                    menu4.draw(surface)
                    pygame.display.update()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        print("X")
                        tr = False

            # Draw the menu
            menu4.update(events)
            menu4.draw(surface)

            crosshair_group.draw(surface)
            crosshair_group.update()
            pygame.display.flip()

        if gender == 'Computer':
            pseudo = pseudo_ordi.get_value()
            lp_pseudo.append((pseudo, gender))
        menu4.clear()
        print(pseudo, gender)
        if gender == 'Human':
            lp_pseudo.append((pseudo[0], gender))
            l_pseudo.remove(pseudo)
        print(lp_pseudo)
        pygame.display.update()

    for p in range(0, n_player):
        lplayer.append((lp_pseudo[p][0], lp_color[p], lp_pseudo[p][1]))
    start_game(lplayer, mode)


def start_game(lplayer, mode) -> None:
    Fichier("lplayer.dat").ecrire(lplayer)
    Fichier("gamemode.dat").ecrire(mode)

    print('Lancement du jeu')
    pygame_menu.events.EXIT
    pygame.quit()
    os.system('cmd /k "board_game.bat"')
    sys.exit()

# MENUS
menu = pygame_menu.Menu(
    width=1280,
    height=720,
    theme=pygame_menu.themes.THEME_DARK,
    title='Gamemode'
)

menu2 = pygame_menu.Menu(
    width=1280,
    height=720,
    theme=pygame_menu.themes.THEME_DARK,
    title='Nombre de joueurs'
)

menu3 = pygame_menu.Menu(
    width=1280,
    height=720,
    theme=pygame_menu.themes.THEME_DARK,
    title='Choix des couleurs'
)

menu4 = pygame_menu.Menu(
    width=1280,
    height=720,
    theme=pygame_menu.themes.THEME_DARK,
    title='Pseudo et genre des joueurs'
)

#user_name = menu.add.text_input('Name: ', default='John Doe', maxchar=10)
menu.add.text_input('Utilisez les flèches et le bouton entrer de préférence', maxchar=1)
menu.add.selector('Mode: ', [('Noob Travel', 0), ('Normal Travel', 1), ('Gastronomy Travel', 3), ('Setups Travel', 4)], onchange=set_difficulty)
#menu.add.selector('Mode: ', [('Noob Travel', 0), ('Normal Travel', 1), ('Back Travel', 2), ('Gastronomy Travel', 3), ('Setups Travel', 4)], onchange=set_difficulty)
menu.add.button('Next', menu_nbr_player)
menu.add.button('Quit', back_mainmenu)

menu2.add.selector('Nombre joueurs: ', [('2', 2), ('3', 3), ('4', 4), ('5', 5)], onchange=set_player_nbr)
menu2.add.button('Next', menu_color)
menu2.add.button('Quit', back_mainmenu)


main_menu()
    
