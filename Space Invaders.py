import pygame
import random
import math
#----Creating Game Window-----

#it is an constructor in pygame
pygame.init()

#--score
score=0
font=pygame.font.Font('freesansbold.ttf', 32)
textX=10
textY=10


#gameover 

over=pygame.font.Font('freesansbold.ttf', 64)


#siaplay.set_mode is used to make screen of (Width, height)
screen=pygame.display.set_mode((800, 600))

#--adding backgroud image

background=pygame.image.load('background.png')

#till here the screen will be setup but will close immeditely

#---Title and Icon----
pygame.display.set_caption('Space Invaders')
#to add the image make sure PNG 32bytes
icon=pygame.image.load('ufo.png')
#this sets our image as an icon in window
pygame.display.set_icon(icon)

#now loading the player image
playerimg=pygame.image.load('player.png')
#setting the x and y corrdinates
playerX=370
playerY=480
playerx=0
playery=0

#--img for enemy


enemyimg=[]
enemyX=[]
enemyY=[]
enemyx=[]
enemyy=[]

enemies=6

for i in range(enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,300))

    #---how many pixels do we want our enemy to move

    enemyx.append(4)
    enemyy.append(40)



#--bullet
bullet=pygame.image.load('bullet.png')
#--setting bullets coordinates--
 
bulletX=0
bulletY=480
bulletx=0
bullety=10
bulletstate='Ready'



#used for creation of img on screen of player
def player(x, y):
    #blit is used for creating the img on screen
    screen.blit(playerimg, (x, y))
    
#used for creation of enemy on screen    
def enemy(x, y, i):
    #blit is used for creating the img on screen
    screen.blit(enemyimg[i], (x, y))
    
def fire_bullet(x, y):
    #we set it global so that we can access to that variable
    global bulletstate
    bulletstate='fire'
    #we added 16 and 10 so that it may appear in center of spaceship
    screen.blit(bullet ,(x, y))

#use to check whether collisions occured or not
def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance=math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY- bulletY, 2)))
    if distance< 27:
        return True
    else:
        return False


def Sound():
    sound=pygame.mixer.Sound('explosion.wav')
    sound.play()

def Laser():
    sound=pygame.mixer.Sound('laser.wav')
    sound.play()
    
def Score(x, y):
    score_rend=font.render("Score :" + str(score), True, (255,255,255))
    screen.blit(score_rend,(x, y))

def Game_over():
    over_rend=over.render("GAME OVER",True, (255,255,255))
    screen.blit(over_rend,(200, 250))

#whatever you do in your game window is considered as an evemt even closing window is an event

running=True
#---we setted an infinte loop----
while running:
    
    #to change the background-color in window we will write this inside the while loop because we want the change to remain continusously in the window thats why we didnt write outside the loop
    #--screen.fill takes RGB as parameter and values written is the color code 0-255
    screen.fill((101,84,84))
    
    #----adding background image using blit in loop so it persists
    
    screen.blit(background,(0, 0))
    
    #---we went through each events in pygame window by using pygame.event.get()
    for event in pygame.event.get():
        #we checked that whether the event which we pressed to close the window is equal to the pygame.quit() event so make the running variable false and terminate the infinite loop false
        if event.type==pygame.QUIT:
            running=False
        
        #----keydown checks for the keys that have been pressed
        if event.type==pygame.KEYDOWN:
            #if the left key is pressed so change x coordinates to less
            if event.key==pygame.K_LEFT:
                    #called the player function
                    playerx=-5
            #if right key is pressed so x coordiante increased
            if event.key==pygame.K_RIGHT:
                    #called the player function
                    playerx=5
            
                
            if event.key==pygame.K_SPACE:
                #we implemented this because if we had not done this so when our bullets were not ready so it was firing which was causing bullets to restart again
                if bulletstate=='Ready':
                    #we did this because we want our bullet to go straight not when we move player so bullet also changes its direction when going towards top
                    bulletX=playerX
                    fire_bullet(bulletX, bulletY)
                    Laser()                        
        #keyup is used to check that the key which we pressed has been released if yes then it stops the space ship
        if event.type==pygame.KEYUP:
            #if up arrow so y coordinate is decreased
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                
                    #called the player function
                    playerx=0
           
    playerX+=playerx
   
    
    
    #----to set the boudaries that it should not go beyond it---
    if playerX<=0:
        playerX=0
        
    elif playerX>=760:
        playerX=760
        
        
    
    
    #----changing position for enemy
    for i in range(enemies):
        
        #game over
        
        #if enemy reachers certain y point so it breaks the game
        if enemyY[i]>450:
            #we called another loop as we want the all enemies to get out
            for j in range(enemies):
                #we setted it equal to 2000 so that all enemies could get out of screen
                enemyY[j]=2000
            Game_over()
            break
            
        enemyX[i]+=enemyx[i]
        
        #----we want our enemy to continuously move in x direction and when it hit the boudary so it should move down in y direction by 40 pixels thats why we increamented in y direction and to move in x direction we setted value just---
        if enemyX[i]<=0:
            enemyx[i] = 4
            enemyY[i]+=enemyy[i]
        
        elif enemyX[i]>=760:
            enemyx[i] = -4
            enemyY[i]+=enemyy[i]
   
         #collision
        collision=iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY=480
            bulletstate='Ready'
            Sound()
            score+=1
            
            enemyX[i]=random.randint(0,800)
            enemyY[i]=random.randint(50,300)

        enemy(enemyX[i], enemyY[i], i)

        
    #shooting multiple bullets
    if bulletY<=0:
        #when it reaches the top so it should reset to original position
        bulletY=480
        bulletstate='Ready'         
    
    #bullets movement
    if bulletstate=='fire':
        fire_bullet(bulletX, bulletY)
        bulletY-=bullety
        
   
    player(playerX, playerY)
    Score(textX, textY)
    #we add the update to make sure that the change we made by adding the color is updated
    pygame.display.update()