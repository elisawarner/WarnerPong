#!/usr/bin/env python
# coding: utf-8

# In[1]:

import numpy as np
import numpy.random
import pygame, sys
pygame.init()

# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0, 0, 255)

# initialize score:
score_dict = {1:0, 2:0}

# Open a new window
m = 700
n = 500
size = (m, n)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Warner Pong")

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True
 
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

def init_direction(player=2,speed=1):
    # direction of ball
    di = pygame.math.Vector2()
    if player == 2:
        di.x = speed
        di.y = speed
    else:
        di.x = -speed
        di.y = speed
    return di

def initialize_ball(player=2,speed=1):
    v = pygame.math.Vector2()
    if player == 2: # computer
        v.x = 21
        v.y = 20
        di = init_direction(2,speed)
    else:
        v.x = m-21
        v.y = 20
        di = init_direction(1,speed)
    return v, di

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

# initialize ball
v, di = initialize_ball()
ballcolor = BLACK

# initialize player paddle
p = pygame.math.Vector2()
p.x = m - 70
p.y = 200

topleft = p
topright = p + pygame.Vector2((20,0))
bottomright = p + pygame.Vector2((20,70))
bottomleft = p + pygame.Vector2((0,70))

# initialize computer paddle
p2 = pygame.math.Vector2()
p2.x = 50
p2.y = 200

p2_topleft = p2
p2_topright = p2 + pygame.Vector2((20,0))
p2_bottomright = p2 + pygame.Vector2((20,70))
p2_bottomleft = p2 + pygame.Vector2((0,70))

target_loc = pygame.math.Vector2()
target_loc.y = int(np.random.random() * 70) # can vary as any integer between
target_loc.x = 0

# paddle dir
pdi = pygame.math.Vector2()
pdi.x = 0
pdi.y = 1

# game parameters
r = 10 # radius of ball
u = 60 # controls speed of game

count_timer = 0
start_time = np.random.choice([2,3,4],1)
speed = 2
scored = False

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    keys = pygame.key.get_pressed()  #checking pressed keys
    if keys[pygame.K_UP] and topleft.y > 1:
        topleft = topleft - (4 * pdi)
        topright = topright - (4 * pdi)
        bottomright = bottomright - (4 * pdi)
        bottomleft = bottomleft - (4 * pdi)
    if keys[pygame.K_DOWN] and bottomleft.y < n :
        topleft = topleft + (4 * pdi)
        topright = topright + (4 * pdi)
        bottomright = bottomright + (4 * pdi)
        bottomleft = bottomleft + (4 * pdi)
 
    # --- Game logic should go here
    
    # control ball direction
    v = v + di

    if v.x > m - r:
        di.x = -speed
    elif v.y > n - 5:
        di.y = -speed
    elif v.x < r:
        di.x = speed
    elif v.y < r:
        di.y = speed

    # --- Drawing code should go here
    # First, clear the screen to white. 
    screen.fill(WHITE)
  
    font = pygame.font.Font('freesansbold.ttf', 20) 
    TextSurf, TextRect = text_objects('%d' % (score_dict[1]), font)
    TextRect.center = (m-10, n-10) 
    screen.blit(TextSurf, TextRect)

    TextSurf2, TextRect2 = text_objects('%d' % (score_dict[2]), font)
    TextRect2.center = (10, n-10) 
    screen.blit(TextSurf2, TextRect2)

    paddle1 = pygame.draw.polygon(screen, BLUE, [topleft, topright, bottomright, bottomleft], 0)
    paddle2 = pygame.draw.polygon(screen, RED, [p2_topleft, p2_topright, p2_bottomright, p2_bottomleft],0)
    ball = pygame.draw.circle(screen, ballcolor, [int(x) for x in v], r) # , 1
    ballcolor = BLACK

    # paddle control ball
    if paddle1.colliderect(ball):
        print(v)
        if v.x+r >= topright.x:
            di.x = di.x * -1.1
            v.x = v.x - r
        elif v.x-r <= topleft.x:
            #di.y = di.y * -1.6
            di.x = di.x * -1.1
            v.x = v.x - r
        else:
            if v.y < topright.y:
                di.y = di.y * 1.1
                di.x = di.x * -1.1
                v.y = v.y + r
                v.x = v.x - r
            else:
                di.y = di.y * -1.1
                v.y = v.y - r
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            carryOn = False # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN and paddle2.colliderect(ball):
            if event.key == pygame.K_LEFT:
                di.x = di.x * -2.6 # spike
                ballcolor = RED
 
    # AUTOMATE PADDLE 1
    start_time = np.random.choice([2,3,4],1)
    if v.x < (m / start_time) and v.x > p2_bottomright.x and p2_topleft != v-target_loc:
        if p2_topleft.y < (v.y - target_loc.y) and p2_bottomright.y < n:
            p2_topleft = p2_topleft + (4*pdi)
            p2_topright = p2_topright + (4*pdi)
            p2_bottomright = p2_bottomright + (4*pdi)
            p2_bottomleft = p2_bottomleft + (4*pdi)
        elif p2_topleft.y > (v.y - target_loc.y) and p2_topleft.y > 1 :
            p2_topleft = p2_topleft - (4*pdi)
            p2_topright = p2_topright - (4*pdi)
            p2_bottomright = p2_bottomright - (4*pdi)
            p2_bottomleft = p2_bottomleft - (4*pdi)
    
    if count_timer % 300 == 0:
        target_loc = pygame.math.Vector2()
        target_loc.y = int(np.random.random() * 70) # can vary as any integer between
        target_loc.x = 0
        start_time = np.random.choice([2,3,4],1)

    # paddle bounce
    if paddle2.colliderect(ball):
        if v.x+r >= p2_topright.x:
            di.x = di.x * -1.1
            v.x = v.x+r
        elif v.x-r <= p2_topleft.x:
            #di.y = di.y * -1.6
            di.x = di.x * -1.1
            v.x = v.x - r
        else:
            if v.y < p2_topright.y:
                di.y = di.y * 1.1
                di.x = di.x * -1.1
                v.x = v.x + r
                v.y = v.y + r
            else:
                di.y = di.y * -1.1
                v.y = v.y + r

    # DEFINE A WIN
    if v.x >= m - r: # player 2 computer wins
        print('Player 2 wins')
        v, di = initialize_ball(2, speed)
        score_dict[2] = score_dict[2] + 1
        scored = False
    elif v.x <= r: # player 1 human wins
        print('Player 1 wins')
        v, di = initialize_ball(1, speed)
        score_dict[1] = score_dict[1] + 1
        scored = False

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    count_timer += 1
    clock.tick(60)

    if score_dict[1] % 5 == 0 and scored == False:
        print(score_dict[1] % 5)
        speed += 1
        scored = True
 
 # Once we have exited the main program loop we can stop the game engine:
pygame.quit()


# In[ ]:




