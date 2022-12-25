#-----------------------------------
##Tyler Boechler
##Comp Sci 20
##Final Project
##June 18th, 2018
#-----------------------------------

import pygame
import random
import time
#Importing necessary modules

def draw_player(screen, rect_x, player_ycoord, colour):
    """Creates the player"""
    pygame.draw.rect(screen, RED, [rect_x - 2, player_ycoord - 2, 54, 54])
    pygame.draw.rect(screen, colour, [rect_x, player_ycoord, 50, 50])
    
def draw_death_brick(screen, death_brick_x, death_brick_y):
    """Draws the falling bricks"""
    pygame.draw.rect(screen, (0, 0, 0), [death_brick_x - 2, death_brick_y - 2, 104, 54])
    pygame.draw.rect(screen, (135, 58, 43), [death_brick_x, death_brick_y, 100, 50])

#naming some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 50, 250)
ORANGE = (255, 101, 20)

pygame.init()
#Initiates the pygame module

size = (700, 500)
#Creates my window
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Dodging Bricks")
 #Names my window

clock = pygame.time.Clock()
#naming my clock variable

score_font = pygame.font.SysFont("Times new roman", 25)
start_font = pygame.font.SysFont("Britannic Bold", 55)
instructions_font = pygame.font.SysFont("Ariel", 27)
#Naming my three different fonts for my text in game

title = start_font.render("DODGING BRICKS", 1, BLUE)
instructions = instructions_font.render("Use the arrow keys to move. Every five rounds, you get a powerup.", 1, ORANGE)
instructions_2 = instructions_font.render("Use them to be invincible for a round. Press SPACE to use your powerups!", 1, ORANGE)
instructions_3 = instructions_font.render("PRESS SPACE TO BEGIN!", 1, ORANGE)
#my messages to be displayed in the game

player_lcorner_xcoord = 340
#The left corner of my player sprite's x coordinate
player_ycoord = 445
#The top y coordinate of my player

player_horizontal_speed = 0
#Naming my variable that moves the player

death_brick_x = random.randrange(0, 601)#random to make the brick appear anywhere
#The starting position of the bricks that fall on the player
death_brick_y = -75

death_brick_drop_speed = 8
#How many pixels the brick drops per frame

powerups = 0
#how many powerups the user has to start
score = 0
#how many rounds the user has played, keeps track of rounds

invincible = False
#/if the player uses a powerup, they become invincible, this keeps them vulnerable to start
done_playing = False
#My game loop variable
waiting_to_play = True
#The variable for my starting screen loop
dead = False

background_image = pygame.image.load("mountain_range.png").convert()
#The background image for the game imported from my game's file

while waiting_to_play:
#Starts a loop for the start screen
    screen.blit(background_image, [0, 0])
    
    #Draws my bg image on the screen
    for event in pygame.event.get():
        #This is a loop which finds every event in the current game, here we detect for any event the player does
        #Allow the player to quit when hitting the X
        
        if event.type == pygame.QUIT:
            done_playing = True
            #Doesn't start the game
            waiting_to_play = False
            dead = False
            break
            #ends the loop
        
        elif event.type == pygame.KEYDOWN:
            #If a key is pressed
            
            if event.key == pygame.K_SPACE:
                #If that key is the spacebar
                #Starts the game
                waiting_to_play = False
                break
            
    #draws the bricks falling in the background for asthetic effect
    death_brick_y += death_brick_drop_speed - 7.9 # Fell to fast
    draw_death_brick(screen, death_brick_x, death_brick_y)
    
    #Respawns the brick when it goes off the screen at a random x and y location above the screen
    if death_brick_y >= 548:
        death_brick_y = random.randrange(-100, -49)
        death_brick_x = random.randrange(0, 601)
    
    #Displays the text for the title screen
    screen.blit(title, (180,170))
    screen.blit(instructions, (110, 270))
    screen.blit(instructions_2, (20, 320))
    screen.blit(instructions_3, (235, 370))
    #draws the player before the game starts to make the start screen look similar to the actual game
    draw_player(screen, player_lcorner_xcoord, player_ycoord, WHITE)
    
    #Resets the screen to all new graphics to be added
    pygame.display.flip()
    
#Restates the bricks location and speed variables for the game
death_brick_x = random.randrange(0, 601)
death_brick_y = -75
death_brick_drop_speed = 8

while not done_playing:
    #My game loop
    for event in pygame.event.get():
        #Detects for events the player does 
        if event.type == pygame.QUIT:
            #If the player chooses to quit, it ends the game without the game over message
            done_playing = True
            break
        
        elif event.type == pygame.KEYDOWN:
            #If a key is pressed...
            if event.key == pygame.K_LEFT:
                #If the key is the left arrow, set the moving variable to move to the left
                player_horizontal_speed = -12
                
            elif event.key == pygame.K_RIGHT:
                #If the key is the right arrow, set the moving variable to move to the right
                player_horizontal_speed = 12
                
            elif event.key == pygame.K_SPACE:
                #If the player hits the space button, it uses a powerup
                if powerups > 0 and not invincible:
                    #If the user actually has powerups, and the user hasn't already used a powerup, it allows the user to use a powerup
                    invincible = True
                    powerups -= 1
                    
        elif event.type == pygame.KEYUP:
            #If the player lets go of the left or right arrow key, set the movement variable to not allow the player to move
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_horizontal_speed = 0
        #End of events
    
    
    #THE LOGIC OF THE GAME STARTS HERE
    
    if death_brick_y + 50 > 440 and not invincible:
    #If the bottom of the brick is at the player height, and the player isn't invincible checks to see if the player is hit by the box
        
        for i in range(death_brick_x - 1, death_brick_x + 101):
            #goes through all the x coordinates of the brick, then sees if they are within the range of the 
            if i > player_lcorner_xcoord - 1 and i < player_lcorner_xcoord + 51:
                # the -1 and + 51 accounts for the border
                #If the player is hit, then the game ends
                done_playing = True
                dead = True
                break
                
    if player_lcorner_xcoord >= 0 and player_lcorner_xcoord + 50 <= 700:
    #if the player is on the screen, it allows it to move left or right
        player_lcorner_xcoord += player_horizontal_speed
    
    else:
    #If the player is not within the screen range, it pushes it back onto the screen
        if player_lcorner_xcoord < 350:
            player_lcorner_xcoord += 1
        else:
            player_lcorner_xcoord -= 1
            
    if death_brick_y >= 548:
        #This means the player survived a brick/round
        #once the brick is off the screen, it respawns the brick at a random height (for different timing) and a different x coordinate
        death_brick_y = random.randrange(-100, -49)
        death_brick_x = random.randrange(0, 601)
        score += 1
        #adding one to the score
        if invincible:
            #If the player used a powerup, it wears off now
            invincible = False

        if score % 5 == 0:
        #every 10 bricks, they speed up slightly
            if death_brick_drop_speed <= 2000:
                death_brick_drop_speed += 1.2
            
        if score % 5 == 0:
        #Every 5 bricks, the player gets a powerup to use
            powerups += 1
    
    death_brick_y += death_brick_drop_speed
    #Changes the brick's y to make it fall
    
    screen.blit(background_image, [0, 0])
    #Draws the background on the screen
    #DRAWING BEGINS
    
    if not invincible:
    #Draws the player
        draw_player(screen, player_lcorner_xcoord, player_ycoord, WHITE)
    else:
    #If the player used a powerup, makes the player Blue
        draw_player(screen, player_lcorner_xcoord, player_ycoord, BLUE)
    draw_death_brick(screen, death_brick_x, death_brick_y)
    #draws the brick with it's new coordinates (falling)
    
    #Draws the score and the amount of powerups the user has
    text = score_font.render("Score: " + str(score) + "                                                                           Powerups: " + str(powerups), True, BLACK)
    screen.blit(text, [10, 5])
    
    #flips the display to show changes
    pygame.display.flip()
        
    clock.tick(30)
    #runs the game at 30 frames per second (FPS)
    
while dead:
    #When the user dies shows gameover message
    gameover_message = start_font.render("GAME OVER", True, BLACK)
    screen.blit(gameover_message, [250, 250])
    
    pygame.display.flip()

    time.sleep(3)#Freezes for 3 seconds
    break #breaks the loop
            
    
pygame.quit()
#Ends the pygame, closes the window