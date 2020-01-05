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

PADDLE_WIDTH = 20
PADDLE_LENGTH = 70

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
    ball_vec = pygame.math.Vector2()
    if player == 2:
        ball_vec.x = speed
        ball_vec.y = speed
    else:
        ball_vec.x = -speed
        ball_vec.y = speed
    return ball_vec

def initialize_ball(player=2,speed=1):
    ball_coord = pygame.math.Vector2()
    if player == 2: # computer
        ball_coord.x = 21
        ball_coord.y = int(np.random.random() * n)
        ball_vec = init_direction(2,speed)
    else:
        ball_coord.x = m-21
        ball_coord.y = int(np.random.random() * n)
        ball_vec = init_direction(1,speed)
    return ball_coord, ball_vec

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def paddle(top_left_coord):
    topleft = top_left_coord
    topright = top_left_coord + pygame.Vector2((PADDLE_WIDTH,0))
    bottomright = top_left_coord + pygame.Vector2((PADDLE_WIDTH,PADDLE_LENGTH))
    bottomleft = top_left_coord + pygame.Vector2((0,PADDLE_LENGTH))

    return [topleft, topright, bottomright, bottomleft]

# initialize ball
ball_coord, ball_vec = initialize_ball()
ballcolor = BLACK

# initialize player paddle coordinates
player1_coord = pygame.math.Vector2()
player1_coord.x = m - PADDLE_LENGTH
player1_coord.y = np.round(n / 2) - 50

# initialize computer paddle coordinates
comp_coord = pygame.math.Vector2()
comp_coord.x = 50
comp_coord.y = np.round(n / 2) - 50


target_loc = pygame.math.Vector2()
target_loc.y = int(np.random.random() * PADDLE_LENGTH) # can vary as any integer between
target_loc.x = 0
player1_speed = 0 # default speed of paddle 1 (player)
default_speed = 4 # default speed of paddle 2 (computer)
comp_speed = default_speed # set temp speed of paddle 2
reset_round = False

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

    # close window to exit
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            carryOn = False # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN and paddle2.colliderect(ball):
            if event.key == pygame.K_LEFT:
                ball_vec.x = ball_vec.x * -2.6 # spike
                ballcolor = RED
        elif event.type == pygame.KEYUP:
            player1_speed = 0

    # control ball direction
    ball_coord = ball_coord + ball_vec

    if ball_coord.x > m - r:
        ball_vec.x = -speed
    elif ball_coord.y > n - 5:
        ball_vec.y = -speed
    elif ball_coord.x < r:
        ball_vec.x = speed
    elif ball_coord.y < r:
        ball_vec.y = speed

    ## DRAWING CODE ##
    # First, clear the screen to white. 
    screen.fill(WHITE)
  
    # scoreboard
    font = pygame.font.Font('freesansbold.ttf', 20) 
    TextSurf, TextRect = text_objects('%d' % (score_dict[1]), font)
    TextRect.center = (m-10, n-10) 
    screen.blit(TextSurf, TextRect)

    TextSurf2, TextRect2 = text_objects('%d' % (score_dict[2]), font)
    TextRect2.center = (10, n-10) 
    screen.blit(TextSurf2, TextRect2)

    # draw paddles and ball
    paddle1 = pygame.draw.polygon(screen, BLUE, paddle(player1_coord), 0)
    paddle2 = pygame.draw.polygon(screen, RED, paddle(comp_coord),0)
    ball = pygame.draw.circle(screen, ballcolor, [int(x) for x in ball_coord], r) # , 1
    ballcolor = BLACK


    ### GAME LOGIC ###
    # player 1 paddle control
    keys = pygame.key.get_pressed()  #checking pressed keys
    if keys[pygame.K_UP] and player1_coord.y > 1:
        player1_speed += 1
        player1_coord = player1_coord - (player1_speed * pdi)
    if keys[pygame.K_DOWN] and player1_coord.y + PADDLE_LENGTH < n :
        player1_speed += 1
        player1_coord = player1_coord + (player1_speed * pdi)

    # paddle hit ball
    if paddle1.colliderect(ball): # player
        #if ball_coord.x+r >= player1_coord.x + PADDLE_WIDTH: # if hits back of the paddle
        #    ball_vec.x = ball_vec.x * -1.1
        #    ball_coord.x = ball_coord.x - int(np.random.random()*r)
        if ball_coord.x-r <= player1_coord.x: # if hits front of paddle
            ball_vec.x = ball_vec.x * -1.1
            ball_coord.x = ball_coord.x - int(np.random.random()*r)
        elif ball_coord.y < player1_coord.y: # hits above paddle
            ball_vec.y = ball_vec.y * 1.1
            ball_vec.x = ball_vec.x * -1.1
            ball_coord.y = ball_coord.y + int(np.random.random()*r)
            ball_coord.x = ball_coord.x - int(np.random.random()*r)
        elif ball_coord.y > player1_coord.y: # hits below paddle
            ball_vec.y = ball_vec.y * -1.1
            ball_coord.y = ball_coord.y - int(np.random.random()*r)
    

    # AUTOMATE COMPUTER PADDLE
    if ball_coord.x < (m / start_time) and ball_coord.x > (comp_coord.x + PADDLE_WIDTH) and comp_coord != ball_coord - target_loc:
        if comp_coord.y < (ball_coord.y - target_loc.y) and comp_coord.y + PADDLE_LENGTH < n:
            comp_coord = comp_coord + (comp_speed * pdi)

            if (ball_coord.y - target_loc.y) - comp_coord.y < comp_speed and comp_speed > 1:
                comp_speed -= 1
            else:
                comp_speed = round(default_speed)
        elif comp_coord.y > (ball_coord.y - target_loc.y) and comp_coord.y > 1 :
            comp_coord = comp_coord - (comp_speed * pdi)

            if comp_coord.y - (ball_coord.y - target_loc.y) < comp_speed and comp_speed > 1:
                comp_speed -= 1
            else:
                comp_speed = round(default_speed)
    else: # go back to center
        if comp_coord.y < 200:
            comp_coord = comp_coord + (comp_speed * pdi)

            if 200 -  comp_coord.y < comp_speed and comp_speed > 1:
                comp_speed -= 1
            else:
                comp_speed = round(default_speed)
        elif comp_coord.y > 200:
            comp_coord = comp_coord - (comp_speed * pdi)

            if comp_coord.y - 200 < comp_speed and comp_speed > 1:
                comp_speed -= 1
            else:
                comp_speed = round(default_speed)
    
    # if you've started a new round
    if reset_round:
        # update target location for ball contact with computer paddle
        target_loc = pygame.math.Vector2()
        target_loc.y = int(np.random.random() * PADDLE_LENGTH) # can vary as any integer between
        target_loc.x = 0

        # update when computer starts to move
        start_time = np.random.choice([2,3,4],1)

        # update computer speed
        default_speed += .2

        reset_round = False

    # paddle bounce
    if paddle2.colliderect(ball):
        if ball_coord.x + r >= comp_coord.x + PADDLE_WIDTH:
            ball_vec.x = ball_vec.x * -1.1
            ball_coord.x = ball_coord.x+ int(np.random.random()*r)
        #elif ball_coord.x - r <= comp_coord.x: # if it hits the back of the comp paddle
        #    ball_vec.x = ball_vec.x * -1.1
        #    ball_coord.x = ball_coord.x - int(np.random.random()*r)
        elif ball_coord.y < comp_coord.y: # hits the top of comp paddle
                ball_vec.y = ball_vec.y * 1.1
                ball_vec.x = ball_vec.x * -1.1
                ball_coord.x = ball_coord.x + r
                ball_coord.y = ball_coord.y + int(np.random.random()*r)
        elif ball_coord.y > comp_coord.y: # hits the bottom of comp paddle
            ball_vec.y = ball_vec.y * -1.1
            ball_coord.y = ball_coord.y + int(np.random.random()*r)

    # DEFINE A WIN
    if ball_coord.x >= m - r: # player 2 computer wins
        print('Player 2 wins')
        ball_coord, ball_vec = initialize_ball(2, speed)
        score_dict[2] = score_dict[2] + 1
        scored = False
        reset_round = True
    elif ball_coord.x <= r: # player 1 human wins
        print('Player 1 wins')
        ball_coord, ball_vec = initialize_ball(1, speed)
        score_dict[1] = score_dict[1] + 1
        scored = False
        reset_round = True

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




