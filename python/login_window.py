import pygame, sys
from settings import *

pygame.init()
pygame.display.set_caption("CONNEXION TOKAIDO")
pygame.display.set_icon(pygame.image.load("python/images/icon_game2.png"))
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

#username input
font = pygame.font.Font(None, 32)
input_box = pygame.Rect(535, 420, 140, 32)
color_inactive = pygame.Color('black')
color_active = pygame.Color('darkgreen')
color = color_inactive
active = False
text = 'username'

#password input
font2 = pygame.font.Font(None, 32)
input_box2 = pygame.Rect(535, 468, 140, 32)
color_inactive2 = pygame.Color('black')
color_active2 = pygame.Color('darkgreen')
color2 = color_inactive
active2 = False
text2 = 'password'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the username rect.
            if input_box.collidepoint(event.pos):
                # Toggle the active variable.
                active = not active
            else:
                active = False
            # Change the current color of the input box.
            color = color_active if active else color_inactive
            
            # If the user clicked on the password rect.
            if input_box2.collidepoint(event.pos):
                # Toggle the active variable.
                active2 = not active2
            else:
                active2 = False
            # Change the current color of the input box 2.
            color2 = color_active2 if active2 else color_inactive2
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                     print(text)
                     text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        
            if active2:
                if event.key == pygame.K_RETURN:
                     print(text2)
                     text2 = ''
                elif event.key == pygame.K_BACKSPACE:
                    text2 = text2[:-1]
                else:
                    text2 += event.unicode
        
    screen.fill("white")
    # Render the current text.
    txt_surface = font.render(text, True, color)
    txt_surface2 = font.render(text2, True, color2)
    # Resize the box if the text is too long.
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    width2 = max(200, txt_surface2.get_width()+10)
    input_box2.w = width2
    # Blit the text.
    screen.blit(pygame.image.load("python/images/wallpaper_tokaido.png"), (0,0))

    # Fond blanc de la case
    case = pygame.Rect(535, 420, 200, 32)
    pygame.draw.rect(screen, (255, 255, 255), case)

    # Fond blanc de la case password
    case2 = pygame.Rect(535, 468, 200, 32)
    pygame.draw.rect(screen, (255, 255, 255), case2)

    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    screen.blit(txt_surface2, (input_box2.x+5, input_box2.y+5))
    # Blit the input_box rect.
    
    pygame.draw.rect(screen, color, input_box, 2)
    pygame.draw.rect(screen, color2, input_box2, 2)

    pygame.display.flip()

    pygame.display.update()
    clock.tick(60)