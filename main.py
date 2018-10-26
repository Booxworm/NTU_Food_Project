import pygame

# Inits pygame
pygame.init()

# Inits clock to limit FPS
clock = pygame.time.Clock()

# Sreates screen
introScreenImage = pygame.image.load("./resources/ntuMap.png")
screen = pygame.display.set_mode((669,474))

# Game loop
running = True
while running:
    # Event handler
    for event in pygame.event.get():
        # Handles quit event
        if event.type == pygame.QUIT:
            running = False
        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONUP:
            print(pygame.mouse.get_pos())

    # Display map
    screen.blit(introScreenImage,(0,0))
    pygame.display.flip()

    # Set to 60 FPS
    clock.tick(60)

# Closes pygame
pygame.quit()
