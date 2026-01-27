import pygame
import random

pygame.init()

screen = pygame.display.set_mode((640, 640))

test_img = pygame.image.load('images/test.png').convert()
test_img = pygame.transform.scale(test_img,
                                   (test_img.get_width() * 2,
                                   test_img.get_height() * 2))
test_img.set_colorkey((255, 255, 255))

target = pygame.Rect(300, 70, 160, 280)
tiles = [pygame.Rect(100, 400, 75, 75), pygame.Rect(200, 450, 75, 75)]
hitbox = pygame.Rect(- test_img.get_width() / 2,
                         - test_img.get_height() / 2,
                         test_img.get_width(), test_img.get_height())
hitbox.x, hitbox.y = 100, 100

x = 0
prev_mx, prev_my = 0, 0
mx, my = 0, 0
running = True
clock = pygame.time.Clock()
delta_time = 0.1 # manage gamespeed w regard to user fps
bg_colour = (37, 150, 190)

# Functions

def changeBg():
    tempList = [random.randint(0, 255) for _ in range(3)]
    return (tempList[0], tempList[1], tempList[2])

def collision_test(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions

def move(rect, movement, tiles): # Movement eg. [5, 2] (new coordinates)
   
    
    # Vertical movement corrections
    rect.x += movement[0]
    collisions = collision_test(rect, tiles)

    for tile in collisions:
        if movement[0] > 0: # moving right
            rect.right = tile.left
        if movement[0] < 0: # moving left
            rect.left = tile.right

    # Horizontal movement corrections
    rect.y += movement[1]
    collisions = collision_test(rect, tiles)

    for tile in collisions:
        if movement[1] > 0: # moving down
            rect.bottom = tile.top
        if movement[1] < 0: # moving up
            rect.top = tile.bottom

    
    return rect




while running: # Main game loop

    # background rendering
    screen.fill(bg_colour)


    

    # collision checking
    
    
    mx, my = pygame.mouse.get_pos()
    
    
    # hitbox = move(hitbox, [mx - prev_mx, my - prev_my], tiles)
    
    # if abs(mx - test_img.get_width() / 2 - hitbox.x)  > test_img.get_width()  + 80:
    #     hitbox.x = mx - test_img.get_width() / 2
    # if abs(my - test_img.get_height() / 2 - hitbox.y)  > test_img.get_height()  + 80:
    #     hitbox.y = my - test_img.get_height() / 2
    


    collision = hitbox.colliderect(target)
    m_collision = target.collidepoint((mx, my))
    pygame.draw.rect(screen, (255 * collision, 255 * m_collision, 0), target)

    # img rendering

    
    screen.blit(test_img, (hitbox.x, hitbox.y))
    for tile in tiles:
        pygame.draw.rect(screen, (255, 0, 0), tile)


    # movement
    x += 10 * delta_time 

    # prev_mx, prev_my = mx, my # update previous position
    
   

    # event checker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bg_colour = changeBg()
            if event.key == pygame.K_ESCAPE:
                running = False



    pygame.display.flip() # display stuff on window

    delta_time = clock.tick(180) / 1000 # max framerate 180 
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()