import pygame

# Inits pygame
pygame.init()

# Inits clock to limit FPS
clock = pygame.time.Clock()

# Creates screen
map = pygame.image.load("./resources/ntuMap.jpeg")
mapSize = (1310,1600)
scaledSize = (int(mapSize[0]/3), int(mapSize[1]/3))
map = pygame.transform.scale(map, scaledSize)
screen = pygame.display.set_mode(scaledSize)

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
    screen.blit(map,(0,0))
    pygame.display.flip()

    # Set to 60 FPS
    clock.tick(60)

# Closes pygame
pygame.quit()
