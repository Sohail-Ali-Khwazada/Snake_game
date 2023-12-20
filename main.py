import pygame
import random
import os

pygame.mixer.init()
pygame.init()

#colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
green = (0,255,0)
# darkgreen = (1,50,32)

screenwidth = 950
screenheight = 500
fps = 60
clock = pygame.time.Clock()


#creating a game window 
gameWindow = pygame.display.set_mode((screenwidth,screenheight))
pygame.display.set_caption("PYTHON EATS")

#background image
bgimg = pygame.image.load('snakeimage.png')
bgimg = pygame.transform.scale(bgimg,(screenwidth,screenheight)).convert_alpha()

#background image for gameover
gameoverimg = pygame.image.load('gameover.png')
gameoverimg = pygame.transform.scale(gameoverimg,(screenwidth,screenheight)).convert_alpha()


def plotsnake(gameWindow,color,snakelist,snakesize):
    for x,y in snakelist:
        pygame.draw.rect(gameWindow,color,[x,y,snakesize,snakesize])



font = pygame.font.SysFont(None,45)
def text_screen(text,color,x,y):
    screentext = font.render(text,True,color)
    gameWindow.blit(screentext,[x,y])

#homescreen
def welcome():
    exitgame = False
    while not exitgame:
        gameWindow.fill(green)
        gameWindow.blit(bgimg,(0,0))

        # Create a semi-transparent surface
        s = pygame.Surface((screenwidth,screenheight))  # the size of your rect
        s.set_alpha(128)                # alpha level(0->fully transparent,255->fully opaque)
        s.fill(white)           #fills the entire surface

        gameWindow.blit(s, (0,0)) 


        text_screen("Welcome to Snakes",black,screenwidth/3,screenheight/2.5) 
        text_screen("Press Spacebar To Play!",black,screenwidth/3.2,screenheight/2) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitgame = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('backgmus.mp3')
                    pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
        clock.tick(fps)


#creating a game loop

def gameloop():
    #game specific variables
    exitgame = False
    gameover = False
    snake_x = 45  #intial position
    snake_y = 55
    food_x = random.randint(20,int(screenwidth/2)) 
    food_y = random.randint(20,int(screenheight/2))
    snake_size = 30
    initvelocity = 5
    velocity_x = 0
    velocity_y = 0
    score = 0

    snakelist = [[snake_x,snake_y]]
    snakelength = 1

    #check if snakehighscore file exits or not
    if(not os.path.exists("snakehighscore.txt")):
        with open('snakehighscore.txt','w') as f:
            f.write("0")

    with open('snakehighscore.txt','r') as f:
        highscore = int(f.read())

    while not exitgame:
        if gameover:
            gameWindow.fill(green)
            gameWindow.blit(gameoverimg,(0,0))
            with open('snakehighscore.txt','w') as f:
                f.write(str(highscore))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitgame = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
                                           
        
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitgame = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x += initvelocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x -= initvelocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y -= initvelocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y += initvelocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y
            snakelist.append([snake_x,snake_y])

            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 10
                snakelength += 5
                food_x = random.randint(20,int(screenwidth/2)) 
                food_y = random.randint(20,int(screenheight/2))
                if score > highscore:
                    highscore = score

            if len(snakelist) > snakelength:
                del snakelist[0]


            if snake_x < 0 or snake_x > screenwidth or snake_y < 0 or snake_y > screenheight or [snake_x,snake_y] in snakelist[:-1]:
                gameover = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()


            gameWindow.fill(green)
            text_screen("Score: "+str(score)+"  High score: "+str(highscore),red,10,10)
            pygame.draw.rect(gameWindow,red,[food_x,food_y,snake_size,snake_size])
            plotsnake(gameWindow,black,snakelist,snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()