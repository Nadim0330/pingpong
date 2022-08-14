import pygame
import time
pygame.init()

#solid colors
Black=(0,0,0)
White=(255,255,255)
LightRed=(255,0,0)
LightGreen=(0,255,0)
Red=(200,0,0)
Green=(0,200,0)

#screen specifications
display_width= 800
display_height=600
screenCaption = pygame.display.set_caption("Pingpong by Nadim")
screen= pygame.display.set_mode([display_width,display_height])
clock = pygame.time.Clock() #game clock

#loading images
ball = pygame.image.load("ball.jpg")
platform= pygame.image.load("platform.png")

def DisplayCount(count):
    font = pygame.font.SysFont(None,30)
    text = font.render("Bounced: "+str(count),True,White)
    screen.blit(text,(0,0))

def TextObjects(text,font,color):
    textSurface= font.render(text,True,color)
    return textSurface,textSurface.get_rect()

def DisplayMessage(text):
    largeFont=pygame.font.Font('freesansbold.ttf',115)
    TextSurf,TextRect = TextObjects(text, largeFont,Red)
    TextRect.center = ((display_width/2),(display_height/2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    game_loop()

def GameOver():
    DisplayMessage('Game over!')

def button(msg,x,y,w,h,ic,ac,action=None):
    mousePos=pygame.mouse.get_pos()
    mouseClick=pygame.mouse.get_pressed()

    if x+w>mousePos[0]>x and y+h>mousePos[1]>y:
        pygame.draw.rect(screen,ac,(x,y,w,h))
        if mouseClick[0]==1 and action !=None:
            action()
    else:
        pygame.draw.rect(screen,ic,(x,y,w,h))

    smallText=pygame.font.Font("freesansbold.ttf",20)
    textSurf,textRect=TextObjects(msg,smallText,Black)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def MainMenu():
    intro=True
    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(White)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = TextObjects("Ping-Pong", largeText,Black)
        TextRect.center = ((display_width/2),(display_height/2-100))
        screen.blit(TextSurf, TextRect)

        button("Play",350,350,100,30,Green,LightGreen,game_loop)
        button("Quit",350,450,100,30,Red,LightRed,pygame.QUIT)
        pygame.display.update()
        clock.tick(15)

def game_loop():
    gameOver=False
    platPosX= (display_width*0.45)
    platPosY=(display_height*0.8)
    bounce_count=0
    #get rect
    ballrect=ball.get_rect()
    platform_rect=platform.get_rect(center=(platPosX,platPosY))
    platform_width=100 #image width
    ball_speed=[6,6]
    platform_speed=1
    
    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()  #checking pressed keys and moving platform
        if keys[pygame.K_LEFT]:
            platform_rect=platform_rect.move([-5*platform_speed,0])
        if keys[pygame.K_RIGHT]:
            platform_rect=platform_rect.move([+5*platform_speed,0])
        #keeping platform in the screen boundries
        if platform_rect.x > display_width-platform_width or platform_rect.x<0:
            platform_rect=platform_rect.clamp(screen.get_rect())


        #ball move and bounce 
        ballrect = ballrect.move(ball_speed)
        if ballrect.left < 0 or ballrect.right > display_width:
            ball_speed[0] = -ball_speed[0]
        if ballrect.top < 0 :
            ball_speed[1] = -ball_speed[1]
        #if the ball touches the bottom of the screen
        if ballrect.bottom > display_height:
            GameOver()
        #if the ball collides with platform
        if(ballrect.colliderect(platform_rect)):
            ball_speed[1] = -ball_speed[1]
            bounce_count+=1
            #increasse ball speed after each bounce
            ball_speed=[ball_speed[0]*1.04,ball_speed[1]*1.04]
            #increase platform move speed as well
            platform_speed+=0.2

        
        screen.fill(Black)
        screen.blit(ball,ballrect)
        screen.blit(platform,platform_rect)
        
        DisplayCount(bounce_count)
        pygame.display.update()
        clock.tick(60)

MainMenu()
game_loop()
pygame.quit()
quit()
