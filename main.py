import pygame
import sys
import random

# -------- INITIALISE --------
pygame.init()
pygame.mixer.init()

# Fullscreen window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("DodgeCraft")

clock = pygame.time.Clock()

button_spacing = 140
menu_center_y = HEIGHT // 2

# -------- LOAD IMAGES --------
menu_bg = pygame.image.load("resourcepack/1394736.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

logo = pygame.image.load("resourcepack/Dodgecraft02.png").convert_alpha()
logo_rect = logo.get_rect(center=(WIDTH // 2, HEIGHT // 4))

# Load buttons
start_btn = pygame.image.load("resourcepack/startbutton01.png").convert_alpha()
learn_btn = pygame.image.load("resourcepack/learnbutton01.png").convert_alpha()
quit_btn = pygame.image.load("resourcepack/quitbutton01.png").convert_alpha()

# Scale buttons relative to screen size
button_width = int(WIDTH * 0.3)
button_height = int(HEIGHT * 0.08)

start_btn = pygame.transform.scale(start_btn, (button_width, button_height))
learn_btn = pygame.transform.scale(learn_btn, (button_width, button_height))
quit_btn = pygame.transform.scale(quit_btn, (button_width, button_height))

# Create button positions
start_rect = start_btn.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
learn_rect = learn_btn.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
quit_rect = quit_btn.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))

# // Game resources for {Start Game}

game_bg = pygame.image.load("resourcepack/nether.png").convert()

# -------- LOAD MUSIC --------
pygame.mixer.music.load("resourcepack/miceonvenus.mp3")
pygame.mixer.music.play(-1)  # Loop forever

# -------- GAME STATE --------
game_state = "menu"

# -------- GAME LOOP --------
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "menu":
            if start_rect.collidepoint(event.pos):
                print("Start Game Clicked")
                game_state = "playing"

            if learn_rect.collidepoint(event.pos):
                print("Learn Clicked")
                game_state = "learn"

            if quit_rect.collidepoint(event.pos):
                print("Quit Clicked")
                pygame.quit()
                sys.exit()

    # -------- DRAW --------
    if game_state == "menu":
        # Always draw background first
        screen.blit(menu_bg, (0, 0))

        # Draw logo
        screen.blit(logo, logo_rect)

        # Hover effect
        mouse_pos = pygame.mouse.get_pos()

        for img, rect in [(start_btn, start_rect),
                          (learn_btn, learn_rect),
                          (quit_btn, quit_rect)]:

            if rect.collidepoint(mouse_pos):
                hover_img = pygame.transform.scale(
                    img,
                    (int(rect.width * 1.05), int(rect.height * 1.05))
                )
                hover_rect = hover_img.get_rect(center=rect.center)
                screen.blit(hover_img, hover_rect)
            else:
                screen.blit(img, rect)

    pygame.display.flip()

pygame.quit()
sys.exit()