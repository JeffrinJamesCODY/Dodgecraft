import random
import sys # this is sys module which provider access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. We will use it to exit the game when the player clicks the quit button.
import pygame #this is the main library we are using to create our game.


pygame.init() # this initialises all the pygame modules that we will be using in our game, such as display, font, and mixer for sound.
pygame.mixer.init() # this specifically initalises the mixer module which is responisble for playing music and sound effects in our game.

# Fullscreen window 
# this will make the game adapt to any screen size, but you can change it to a fixed size if you want
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("DodgeCraft") # this is the title of the game that appears in the window title bar

clock = pygame.time.Clock() # this will help us control the frame rate of the game

# game state - this variable will keep track of all the settings and values that we need to run the game.
game_state = "menu"

player_speed = 10
health = 3
score = 0
mob_speed = 13

mobs = []

# resourcepack - this where we load all our images and music for the game.
menu_bg = pygame.image.load("resourcepack/1394736.png").convert() # this loads the background image for the menu screen. The convert() method is used to optimise the image for faster blitting onto the screen. The image should be in the resourcepack folder in the same direction
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT)) #this scales the menu background image to fit the entire screen, regardless of the screen size. It uses the WIDTH and HEIGHT variables we defined earlier to get the current screen dimensions.

logo = pygame.image.load("resourcepack/Dodgecraft02.png").convert_alpha() #convert_alpha() is used here instead of convert() because the logo image likely has transparency (alpha channel) that we want to preserve when blitting it onto the screen. This allows the logo to blend seamlessly with the background without any unwanted solid background color.
logo_rect = logo.get_rect(center=(WIDTH // 2, HEIGHT // 4)) # this gets the rectangular area of the logo image and sets its center position to be at the middle of the screen horizontally (WIDTH // 2) and one quarter down vertically (HEIGHT // 4). This will position the logo near the top center of the menu screen.

hangingupdate_img = pygame.image.load("resourcepack/hangingboard01.png").convert_alpha()
hangingupdate_rect = hangingupdate_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
hangingupdate_rect.topright = (WIDTH, 0) # this sets the top right corner of the hanging update image to be at the top right corner of the screen. This will position the hanging update image in the top right corner of the menu screen, slightly below the logo.

# Menu Buttons that is required for the menu screen. We load the images for the start, learn, and quit buttons, scale them to be appropriately sized based on the screen dimensions, and get their rectangular areas to position them on the menu screen and detect mouse clicks on them. The buttons will be positioned in the center of the menu screen, with the start button above the learn and quit buttons.
start_btn = pygame.image.load("resourcepack/startbutton01.png").convert_alpha()
learn_btn = pygame.image.load("resourcepack/learnbutton01.png").convert_alpha()
quit_btn = pygame.image.load("resourcepack/quitbutton01.png").convert_alpha()

button_width = int(WIDTH * 0.3) # this sets the width of the buttons to be 30% of the screen width, which will make them look good on different screen sizes. You can adjust this percentage if you want larger or smaller buttons.
button_height = int(HEIGHT * 0.08)

start_btn = pygame.transform.scale(start_btn, (button_width, button_height)) # this scales the start button image to the desired button width and height that we calculated based on the screen size. This ensures that the button will look good and be appropriately sized on different screen resolutions.
learn_btn = pygame.transform.scale(learn_btn, (button_width, button_height))
quit_btn = pygame.transform.scale(quit_btn, (button_width, button_height))

start_rect = start_btn.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)) # this gets the rectangular area of the start button image and sets its center position to be at the middle of the screen horizontally (WIDTH // 2) and slightly above the vertical center (HEIGHT // 2 - 40). This will position the start button in the middle of the menu screen, just above the learn and quit buttons. The 2 in here is to position the button above the center, and the 40 is to give it some space from the learn and quit buttons that will be below it.
learn_rect = learn_btn.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
quit_rect = quit_btn.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))

# all the game resources when start game is started by clicking the start button in the menu. This includes the game background, player character (Steve), mob image (Warden), heart image for health display, and music for the game. These resources will be used during the gameplay when the player is in the "playing" state.
game_bg = pygame.image.load("resourcepack/nether.png").convert()
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))

steve = pygame.image.load("resourcepack/steve02.png").convert_alpha()
steve_rect = steve.get_rect(center=(WIDTH // 2, HEIGHT - 120))

mob_img = pygame.image.load("resourcepack/Warden02.png").convert_alpha()
mob_img = pygame.transform.scale(mob_img, (70, 70)) # this loads the mob image (Warden) and scales it to be 70x70 pixels. This will make the mobs a consistent size on the screen, regardless of the original size of the image. You can adjust the size if you want larger or smaller mobs, but 70x70 is a good size for our game.

heart_img = pygame.image.load("resourcepack/heart01.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (40, 40))

# Music - this loads the music for the menu screen and starts playing it in a loop. The -1 argument in play() means that the music will loop indefinitely until we change it or stop it.
pygame.mixer.music.load("resourcepack/miceonvenus.mp3")
pygame.mixer.music.play(-1) 

# Font
font = pygame.font.SysFont("Minecraft", 36) # this creates a font object using the Minecraft font with a size of 36. This font will be used to render the score text during the gameplay. Make sure you have the Minecraft font installed on your system for this to work, or you can change it to a different font that you have available.

# the main loop - this is where the game runs continuously until the player decides to quit. It handles events (like keyboard and mouse input), updates the game state (like moving the player and mobs, checking for collisions, and updating the score), and draws everything on the screen every frame.
running = True # this variable is used to control the main game loop. When the player decides to quit the game, we will set running to False, which will exit the loop and end the game.

while running: # this is the main game loop that will keep running until the player decides to quit. Inside this loop, we will handle events, update the game state, and draw everything on the screen every frame.

    clock.tick(60) # this limits the game to run at 60 frames per second (FPS). This means that the game will update and redraw the screen 60 times every second, which helps to ensure smooth gameplay and consistent performance across different devices. You can adjust this value if you want a faster or slower frame rate, but 60 FPS is generally a good target for most games.

    # main loop events

    # in range is a common way to loop through a sequence of numbers, but in this case, we are using for event in pygame.event.get() to loop through all the events that have occurred since the last frame. This allows us to check for specific events (like quitting the game, pressing keys, or clicking buttons) and respond accordingly to control the game flow and player actions.
    #for event is a common way to loop through all the events that have occurred since the last frame. Pygame collects all user input and system events (like keyboard presses, mouse clicks, and window events) into an event queue. By using pygame.event.get(), we can retrieve all the events that have happened and process them one by one in this loop. This allows us to respond to user actions and control the game flow based on those events.
    for event in pygame.event.get(): # this loop goes through all the events that have happened since the last frame. This includes things like keyboard input, mouse clicks, and window events (like closing the game). We will check for specific events to control the game flow and player actions.

        if event.type == pygame.QUIT: # this checks if the player has clicked the close button on the game window. If this event occurs, we set running to False to exit the main game loop.
            running = False

        if event.type == pygame.KEYDOWN: # this checks if the player has pressed a key on the keyboard. We will check for specific keys to control the game, such as the escape key to quit and the spacebar for jumping.

            if event.key == pygame.K_ESCAPE: # this checks if the player has pressed the escape key. If this event occurs, we set running to False to exit the game.
                running = False

            # Jump (instant arcade jump) - this checks if the spacebar is pressed and if the game state is "playing". If both conditions are true, it checks if Steve is on the ground (by checking if his bottom is greater than or equal to the ground level). If Steve is on the ground, it moves him up by 120 pixels to simulate a jump. This creates an instant arcade-style jump where Steve will immediately move up when the spacebar is pressed, without any gradual acceleration or deceleration.
            if event.key == pygame.K_SPACE and game_state == "playing":
                if steve_rect.bottom >= HEIGHT - 40:
                    steve_rect.y -= 120

        # Menu mouse clicks 
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "menu": # this checks if the player has clicked the mouse button while in the menu state. If this event occurs, we will check if the click was on any of the menu buttons (start, learn, or quit) and respond accordingly.

            if start_rect.collidepoint(event.pos): #this checks if the mouse click occurred within the rectangular area of the start button. If this condition is true, it means the player has clicked the start button, and we will change the game state to "playing" to start the game. We will also load and play the game music, reset the player's health and score, clear any existing mobs, and position Steve at the starting location for the game.
#collidepoint() is a method that checks if a given point (in this case, the position of the mouse click) is inside the rectangular area defined by start_rect. If the mouse click is within the bounds of the start button, we will execute the code inside this if statement to start the game.
                game_state = "playing"

                pygame.mixer.music.load("resourcepack/Alpha.mp3")
                pygame.mixer.music.play(-1)

                health = 3
                score = 0
                mobs.clear() # this clears the list of mobs to ensure that there are no leftover mobs from a previous game when the player starts a new game. This is important to reset the game state and provide a fresh start for the player.

                steve_rect.center = (WIDTH // 2, HEIGHT - 120) #rect is a pygame object that represents a rectangular area, and it has various attributes and methods for positioning and collision detection. By setting the center attribute of steve_rect, we are positioning Steve at the horizontal center of the screen (WIDTH // 2) and near the bottom of the screen (HEIGHT - 120) to start the game. This ensures that Steve is in the correct starting position when the player clicks the start button in the menu.
#here steve_rect is the rectangular area that represents the player character (Steve) in the game. By setting its center attribute, we are positioning Steve at the desired location on the screen when the game starts. This allows us to control where Steve appears at the beginning of each game session, ensuring a consistent starting point for the player.
            elif quit_rect.collidepoint(event.pos): # this checks if the mouse click occurred within the rectangular area of the quit button. If this condition is true, it means the player has clicked the quit button, and we will set running to False to exit the main game loop and end the game. We also call pygame.quit() to uninitialize all pygame modules and sys.exit() to exit the program cleanly.
                pygame.quit()
                sys.exit() # this is a function from the sys module that we imported at the beginning. It is used to exit the program cleanly. When the player clicks the quit button, we want to not only exit the main game loop but also ensure that all resources are properly released and the program terminates without any errors. By calling sys.exit(), we can achieve this clean exit from the game when the quit button is clicked.

            elif learn_rect.collidepoint(event.pos):
                print("Learn clicked")

    # game update - this is where we update the game state based on player input, mob movement, collision detection, and score updates. This code will only run when the game state is "playing", which means the player has started the game from the menu.
    if game_state == "playing":

        # Player movement (hold key movement) is implemented by checking the current state of the keyboard using pygame.key.get_pressed(), which returns a list of boolean values representing the state of each key. We check if the left arrow key (pygame.K_LEFT) or the 'A' key (pygame.K_a) is pressed to move Steve left, and if the right arrow key (pygame.K_RIGHT) or the 'D' key (pygame.K_d) is pressed to move Steve right. We also ensure that Steve does not move off the screen by clamping his x position within the bounds of 0 and WIDTH - steve_rect.width.
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]: # you can use keys[pygame.K_LEFT] to check if the left arrow key is currently being pressed, and keys[pygame.K_a] to check if the 'A' key is being pressed. If either of these conditions is true, it means the player is trying to move Steve to the left, so we will decrease Steve's x position by player_speed to move him left on the screen.
            steve_rect.x -= player_speed # this line of code moves Steve to the left by decreasing his x position by the value of player_speed. The player_speed variable determines how fast Steve moves, and by subtracting it from steve_rect.x, we are effectively moving Steve left on the screen when the left arrow key or 'A' key is pressed.

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: # similarly, this checks if the right arrow key or 'D' key is being pressed. If either of these conditions is true, it means the player is trying to move Steve to the right, so we will increase Steve's x position by player_speed to move him right on the screen.
            steve_rect.x += player_speed

        steve_rect.x = max(0, min(WIDTH - steve_rect.width, steve_rect.x)) # this line of code ensures that Steve does not move off the screen. It uses the max() and min() functions to clamp Steve's x position within the bounds of 0 (the left edge of the screen) and WIDTH - steve_rect.width (the right edge of the screen). This means that if Steve tries to move left beyond the left edge, his x position will be set to 0, and if he tries to move right beyond the right edge, his x position will be set to WIDTH - steve_rect.width. This keeps Steve visible and playable within the screen boundaries.

        # Snap player to ground - this code checks if Steve is above the ground level (which is defined as HEIGHT - 40). If Steve's bottom is less than the ground level, it means he is in the air (either jumping or falling), so we will move him down by increasing his bottom position by 25 pixels to simulate gravity. If Steve's bottom is greater than or equal to the ground level, we will snap him to the ground by setting his bottom position to the ground level. This creates a simple gravity effect where Steve will fall back down after jumping and will stay on the ground when not jumping.
        ground_level = HEIGHT - 40 # this defines the y-coordinate of the ground level in the game. We will use this value to determine when Steve is on the ground and to snap him back to the ground after jumping or falling.
        if steve_rect.bottom < ground_level: # this checks if Steve's bottom position is less than the ground level. If this condition is true, it means Steve is in the air (either jumping or falling), so we will move him down by increasing his bottom position by 25 pixels to simulate gravity. This creates a simple gravity effect where Steve will fall back down after jumping and will stay on the ground when not jumping.
            steve_rect.bottom += 25 # this line of code simulates gravity by moving Steve down when he is in the air. By increasing his bottom position by 25 pixels, we are effectively moving him down on the screen. You can adjust this value to make the gravity stronger or weaker, but 25 pixels per frame is a good starting point for a simple arcade-style jump and fall mechanic.
        else:
            steve_rect.bottom = ground_level # this line of code snaps Steve to the ground by setting his bottom position to the defined ground level. This ensures that when Steve is not jumping or falling, he will stay on the ground and not sink below it. By setting steve_rect.bottom to ground_level, we are effectively placing Steve's feet at the correct position on the screen to create a solid ground for him to stand on.

        # Spawn mobs - this code randomly spawns mobs (Wardens) at the top of the screen. We use random.randint(1, 15) to generate a random number between 1 and 15, and if that number is 1, we will create a new mob. This means that on average, a new mob will spawn every 15 frames. We create a new mob by getting the rectangular area of the mob image, setting its x position to a random value between 0 and WIDTH - mob_rect.width (to ensure it spawns within the screen), and setting its y position to -70 (just above the top of the screen). We then add this mob_rect to the mobs list, which will be used to track all the mobs currently in the game.
        if random.randint(1, 15) == 1: #random.randint(1, 15) generates a random integer between 1 and 15 (inclusive). By checking if this random number is equal to 1, we are creating a condition that has a 1 in 15 chance of being true each frame. This means that, on average, a new mob will spawn every 15 frames, which creates a reasonable frequency of mobs appearing in the game without overwhelming the player.
            mob_rect = mob_img.get_rect()
            mob_rect.x = random.randint(0, WIDTH - mob_rect.width) #rand.int is used here to set the x position of the mob to a random value between 0 and WIDTH - mob_rect.width. This ensures that the mob will spawn within the horizontal bounds of the screen, preventing it from appearing partially off-screen. By using random.randint(), we can create a more dynamic and unpredictable gameplay experience, as mobs will appear at different horizontal positions each time they spawn.
            mob_rect.y = -70
            mobs.append(mob_rect) #append is a method used to add the newly created mob_rect to the mobs list. This allows us to keep track of all the mobs currently in the game, so we can update their positions, check for collisions with Steve, and draw them on the screen during each frame of the game loop.

        # Move mobs every frame - this code iterates through all the mobs in the mobs list and moves them down the screen by increasing their y position by mob_speed. We also check for collisions between each mob and Steve using the colliderect() method. If a collision is detected, we decrease the player's health by 1, remove the mob from the mobs list, and continue to the next mob. If a mob moves off the bottom of the screen (y > HEIGHT), we remove it from the mobs list and increase the player's score by 1. This code is responsible for updating the position of each mob, handling collisions with Steve, and updating the score when mobs are successfully dodged.
        for mob in mobs[:]:

            mob.y += mob_speed

            if mob.colliderect(steve_rect):
                health -= 1
                mobs.remove(mob)
                continue

            if mob.y > HEIGHT:
                mobs.remove(mob)
                score += 1

        # Game over - this code checks if the player's health has dropped to 0 or below. If this condition is true, it means the player has lost the game, so we will change the game state back to "menu" to return to the main menu screen. We will also load and play the menu music again to reset the audio for the menu screen. This allows the player to start a new game from the menu after losing.
        if health <= 0:
            game_state = "menu"

            pygame.mixer.music.load("resourcepack/miceonvenus.mp3")
            pygame.mixer.music.play(-1)

    #  The Draw section where we draw everything on the screen based on the current game state. If the game state is "menu", we will draw the menu background, logo, hanging update image, and menu buttons. We will also check for mouse hover on the buttons to create a simple hover effect by scaling the button images slightly when the mouse is over them. If the game state is "playing", we will draw the game background, Steve, mobs, health hearts, and score text on the screen. This section is responsible for rendering all the visual elements of the game based on the current state of the game.
    if game_state == "menu":

        screen.blit(menu_bg, (0, 0)) #blit is a method used to draw one image onto another. In this case, we are drawing the menu background image (menu_bg) onto the main screen at the position (0, 0), which is the top-left corner of the screen. This will fill the entire screen with the menu background image when we are in the "menu" game state.
        screen.blit(hangingupdate_img, hangingupdate_rect) # this draws the hanging update image onto the screen at the position defined by hangingupdate_rect. This will position the hanging update image in the top right corner of the menu screen, slightly below the logo, as we set its top right corner to be at the top right corner of the screen earlier in the code.
        screen.blit(logo, logo_rect) # this draws the logo image onto the screen at the position defined by logo_rect. This will position the logo near the top center of the menu screen, as we set its center to be at (WIDTH // 2, HEIGHT // 4) earlier in the code.

        mouse_pos = pygame.mouse.get_pos()

        for img, rect in [(start_btn, start_rect), # we create a list of tuples that pairs each button image with its corresponding rectangular area. This allows us to easily loop through each button and check for mouse hover effects in a clean and organized way. By using a list of tuples, we can avoid repetitive code and make it easier to manage multiple buttons in the menu.
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
                screen.blit(img, rect) # if the mouse is not hovering over the button, we simply draw the original button image at its defined rectangular area on the screen. This ensures that the buttons are displayed normally when the mouse is not over them, and only show the hover effect when the mouse is hovering over them.

    elif game_state == "playing":

        screen.blit(game_bg, (0, 0))
        screen.blit(steve, steve_rect)

        for mob in mobs:
            screen.blit(mob_img, mob)

        # Hearts UI # this code draws the heart images on the screen to represent the player's current health. We use a for loop that iterates from 0 to health - 1, and for each iteration, we draw a heart image at a position that is offset by 50 pixels for each heart. This creates a row of hearts in the top left corner of the screen, with each heart representing one unit of health. As the player loses health, the number of hearts displayed will decrease accordingly.
        for i in range(health):
            screen.blit(heart_img, (20 + i * 50, 20))

        # Score UI this code renders the score text using the font object we created earlier. We use the render() method to create a surface with the text "Score: {score}", where {score} is the current score value. We set the color of the text to white (255, 255, 255) and then blit this text surface onto the screen at a position near the top right corner (WIDTH - 200, 20). This will display the player's current score during the gameplay.
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH - 200, 20))

    pygame.display.flip() # this updates the entire display with everything we have drawn on the screen during this frame. It is necessary to call pygame.display.flip() at the end of each frame to ensure that all the visual changes we made (like drawing the background, player, mobs, UI elements, etc.) are actually shown on the screen. Without this call, the screen would not update and we would not see any of the changes we made during the game loop.

pygame.quit()
sys.exit()