import pygame

def getCoordsClick(imagePath, size):
    """
    getCoordsClick creates an image based on the input, and returns the co-ordinates of the mouse click
    Accepts path to file, and image resolution as parameters
    Returns a tuple (x,y)
    """
    # Inits pygame
    pygame.init()

    # Inits clock to limit FPS
    clock = pygame.time.Clock()

    # Creates screen
    image = pygame.image.load(imagePath)
    map = pygame.transform.scale(image, size)
    screen = pygame.display.set_mode(size)

    # Co-ordinates of user click
    coords = False

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
                coords = pygame.mouse.get_pos()
                running = False

        # Display map
        screen.blit(map,(0,0))
        pygame.display.flip()

        # Set to 60 FPS
        clock.tick(60)

    # Closes pygame
    pygame.quit()

    return coords
