#Faaiz Joad
#Final Project for 15112


import pygame
import random

#set up basic variables
#the window height and width can be adjusted to the users preference
winHeight = 800 #700
winWidth = 1000 #900
halfWinHeight = winHeight/2
halfWinWidth = winWidth/2
#tuple to reference the entire window with
win = (winWidth,winHeight)
#the size of a single square edge 
pixel = 32
#this is what how the game is created. It is 32x32, 32x32 squares.
#Later this will be used to form the background 
pixelBlock = (32,32)
#curernt level always starts from level 0 and it continues to the maximum level
currentLevel = 0
maxLevel = 10
obstacleAtMilliSecond = 500 #an obstacle will be created every x milliseconds
obstacleSpeed = 5   #offset for the speed of the obstacles 
WHITE = (255, 255, 255) #"#FFFFFF"
BLACK = (0, 0, 0) #"#000000"
RED = (255, 0, 0)
GREEN = (0, 255, 0) #"#00FF00"
BLUE = (0, 0, 255)

#this class is used by the pygame library. This is to form the sprites and group
#them together. All the other classes will inherit this classes functionality
class Object(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


#This is the first class that will be displayed on screen as an obstacle that
#can kill the player 
class Obstacle(Object):
    def __init__(self, levelWidth, levelHeight):
        Object.__init__(self)
        #creates actual obstacle 
        self.image = pygame.Surface(pixelBlock)
        self.width = 32
        self.height = 32
        #creates an obstcle that spawns at the border of the right edge of the
        #screen
        self.xpos = levelWidth - self.width
        #the position the obstacle spawns at on the y axis is random 
        self.ypos = random.randint(0 + self.height*2, levelHeight - self.height*2)
        #random color
        red = random.randint(0, 1)
        green = random.randint(0, 1)
        blue = random.randint(0, 1)
        self.color = pygame.Color(red * 255, green * 255, blue * 255)
        self.image.fill(self.color) 
        self.rect = pygame.Rect (self.xpos, self.ypos, pixel, pixel)
    def update(self):
        self.rect.left -= obstacleSpeed
        

#main class that defines the main character
class Player(Object):
    def __init__(self, x, y):
        Object.__init__(self)
        self.xVelocity = 0
        self.yVelocity = 0
        self.onGround = False
        self.image = pygame.Surface(pixelBlock)
        self.image.fill(GREEN) 
        self.rect = pygame.Rect(x, y, pixel, pixel)

    def update(self, up, down, left, right, move, platforms, spikes, obstacles):
        if up:
            # only jump if on the ground
            if self.onGround: self.yVelocity -= 10
        if down:
            pass
        if move:
            self.xVelocity = 12
        if left:
            self.xVelocity = -8
        if right:
            self.xVelocity = 8
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yVelocity += 0.3
            # max falling speed
            if self.yVelocity > 100: self.yVelocity = 100
        if not(left or right):
            self.xVelocity = 0
        # increment in x direction
        self.rect.left += self.xVelocity
        # do x-axis collisions
        self.collide(self.xVelocity, 0, platforms, spikes, obstacles)
        # increment in y direction
        self.rect.top += self.yVelocity
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yVelocity, platforms, spikes, obstacles)

    #fuctions to check for collisons 
    def collide(self, xVelocity, yVelocity, platforms, spikes, obstacles):
        #check if collison has occured and do the proper action
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                #if isinstance(p, ExitBlock):
                #    pygame.event.post(pygame.event.Event(QUIT))
                if xVelocity > 0:
                    self.rect.right = p.rect.left
                    #print "collide right"
                if xVelocity < 0:
                    self.rect.left = p.rect.right
                    #print "collide left"
                if yVelocity > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yVelocity = 0
                if yVelocity < 0:
                    self.rect.top = p.rect.bottom
        #if a collison occurs with the spike then restart
        for s in spikes:
            if pygame.sprite.collide_rect(self, s):
                #if the "spike" is an exitBlock, then increment the current level
                if s.isGate and currentLevel < maxLevel:
                    global currentLevel
                    currentLevel += 1
                else :
                    global currentLevel 
                    currentLevel = 0
                mainWin()
        #if collision with an obstacle then restart 
        for o in obstacles:
            if pygame.sprite.collide_rect(self, o):
                global currentLevel
                currentLevel = 0
                mainWin()


#class defining the spike obstacle             
class Spike(Object):
    def __init__(self, x, y, movable, isGate = False):
        Object.__init__(self)
        #loads spike with black background as the intial stage is not "switched"
        self.image = pygame.image.load("spikes_blackbg.png")
        self.rect = pygame.Rect(x, y - 4, pixel, pixel)
        #spikes can move!
        self.movable = movable     
        self.shiftBy = 100
        #if it is an exitBlock then use a different picture 
        self.isGate = isGate
        if isGate == True:
            self.image = pygame.image.load("finish_flag.png")
    #when the color changes so do the spikes so it doesnt look weird
    def switchColorAndPosition(self, switch):
        if not self.isGate:
            if switch:
                self.image = pygame.image.load("spikes_whitebg.png") 
                if self.movable == True:
                    self.rect = self.rect.move(-self.shiftBy, 0)
            else:
                self.image = pygame.image.load("spikes_blackbg.png") 
                if self.movable == True:
                    self.rect = self.rect.move(+self.shiftBy, 0)      
    def update(self):
        pass


#platform class 
class Platform(Object):
    def __init__(self, x, y, movable):
        Object.__init__(self)
        self.image = pygame.Surface(pixelBlock)
        #platforms are white
        #whether or not they can move is passed into the function 
        self.image.fill(WHITE) 
        self.rect = pygame.Rect(x, y, pixel, pixel)
        self.movable = movable
        self.shiftBy = 100
        
    #make the color black when "switched" so the platforms are visable     
    def switchColorAndPosition(self, switch):
        if switch:
            self.image.fill(BLACK) 
            if self.movable == True:
                self.rect = self.rect.move(-self.shiftBy, 0)
        else:
            self.image.fill(WHITE) 
            if self.movable == True:
                self.rect = self.rect.move(+self.shiftBy, 0)

    def update(self):
        pass

#camera function from stack overflow#        
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

#loads levels from files
def loadLevel():
        filename = "switch_level" + str(currentLevel) +".txt"
        levelfile = open(filename)
        hashlist = []
        line = levelfile.readline()
        line = line.strip() #remove the \n
        while line:
            hashlist.append(line)
            line = levelfile.readline() 
            line = line.strip() #remove the \n
        #returns the level as strings in a list
        #this is how pygame builds levels
        return hashlist

#obstacles only appear past level 4. Thank goodness!
def createObstacle (obstacles, objects, levelWidth, levelHeight):
    if currentLevel >= 4:
        obstacle = Obstacle(levelWidth, levelHeight)
        obstacles.append(obstacle)
        objects.add(obstacle)
    #print('obstacles count', len(obstacles))

#this is used in the spash() function
#it is called by splash(), but this is the function that actually displays the
#messages on screen
def displayMessage(mainWin, message, size, color, messageXPos, messageYPos):
    font = pygame.font.SysFont("Calibri", size)
    displayMessage = font.render(message, True, color)
    mainWin.blit(displayMessage, [messageXPos, messageYPos])

#function to make life easier 
def splash(mainWin, clock):
    showSplash = True
    mainWin.fill(WHITE)
    while showSplash:
        #allows user to quit from the splash screen so the program doesnt hang
        for i in pygame.event.get():
            if i.type == pygame.QUIT: 
                pygame.quit()
                quit()
            #break out of loop when key is pressed and initiate the game 
            if i.type == pygame.KEYDOWN:      
                showSplash = False
        #what the splash screen says
        displayMessage(mainWin, "Switch", 96, BLUE, halfWinWidth-100, halfWinHeight-300)
        displayMessage(mainWin, "Space Bar: Shift Platforms", 48, RED, halfWinWidth-100, halfWinHeight-200)
        displayMessage(mainWin, "< Left Arrow : Move Left", 48, RED, halfWinWidth-100, halfWinHeight-150)
        displayMessage(mainWin, "> Right Arrow : Move Right", 48, RED, halfWinWidth-100, halfWinHeight-100)
        displayMessage(mainWin, "/\ Up Arrow :  Jump", 48, RED, halfWinWidth-100, halfWinHeight-50)
        displayMessage(mainWin, "Press any key to continue", 36, BLACK, halfWinWidth-100, halfWinHeight+50)
        clock.tick(60)
        pygame.display.update()        

#the gameloop is within this function. The main code only calls this function once
def mainWin():
    #initialize pygame and create a single 32x32 pixel black square
    pygame.init()
    mainWin = pygame.display.set_mode(win)
    pygame.display.set_caption('Switch')
    background  = pygame.Surface(pixelBlock)
    background.fill(BLACK) 
    pygame.time.set_timer(pygame.USEREVENT, obstacleAtMilliSecond)
    clock = pygame.time.Clock()

    #show splash and init variables
    if currentLevel == 0 :
        splash(mainWin, clock)
    up = False
    down = False
    left = False
    right = False
    move = False
    objects = pygame.sprite.Group()
    player = Player(pixel, pixel)
    platforms = []
    spikes = []
    obstacles = []
    x=0
    y=0
    #get level from text file
    level = loadLevel()
    #build the level 
    for row in level:
        for column in row:
            if column == "B":   #border - unmovable platform
                platform = Platform(x, y, False)
                platforms.append(platform)
                objects.add(platform)
            if column == "P":   #plank - movable platform
                platform = Platform(x, y, True)
                platforms.append(platform)
                objects.add(platform)
            if column == "E":   #exit gate for next level
                spike = Spike(x, y, False, True)
                spikes.append(spike)
                objects.add(spike)
            if column == "A":   #unmovable spike 
                spike = Spike(x, y, False)
                spikes.append(spike)
                objects.add(spike)
            if column == "S":   #movable spike
                spike = Spike(x, y, True)
                spikes.append(spike)
                objects.add(spike)
            x+=pixel
        y+=pixel
        x=0
    #add player to the sprite group 
    objects.add(player)
    #level width/height for the camera 
    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    switch = False
    playGame = True
    #the main gameloop
    while playGame:
        #controls 
        for i in pygame.event.get():
            if i.type == pygame.QUIT: 
                playGame = False
            if i.type == pygame.USEREVENT:
                createObstacle(obstacles, objects, total_level_width, total_level_height)
            if i.type == pygame.KEYDOWN and i.key == pygame.K_UP:
                up = True
            if i.type == pygame.KEYDOWN and i.key == pygame.K_DOWN:
                down = True
            if i.type == pygame.KEYDOWN and i.key == pygame.K_LEFT:
                left = True
            if i.type == pygame.KEYDOWN and i.key == pygame.K_RIGHT:
                right = True
            if i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE:
                switch = not switch
                for p in platforms:
                    p.switchColorAndPosition(switch)
                for s in spikes:
                    s.switchColorAndPosition(switch)
                    
            if i.type == pygame.KEYUP and i.key == pygame.K_UP:
                up = False
            if i.type == pygame.KEYUP and i.key == pygame.K_DOWN:
                down = False
            if i.type == pygame.KEYUP and i.key == pygame.K_RIGHT:
                right = False
            if i.type == pygame.KEYUP and i.key == pygame.K_LEFT:
                left = False
        #black when "unswitched" and white when "switched"
        if switch == False:
            background.fill(BLACK) 
        else:
            background.fill(WHITE)
        #use the first 32x32 pixel square and multiply 32x32  times to create the background
        #for the level
        #probably max width/height? 
        for q in range(pixel):
            for p in range(pixel):
                mainWin.blit(background, (p*pixel, q*pixel))
        #update everything
        camera.update(player)
        for obstacle in obstacles:
            obstacle.update()
        player.update(up, down, left, right, move, platforms, spikes, obstacles)
        for o in objects:
            mainWin.blit(o.image, camera.apply(o))
        #who doesnt want 60fps?
        clock.tick(60)
        pygame.display.update()
    #if not in gameloop then the game is not being played, so we quit 
    pygame.quit()
    quit()

#partly from stack overflow
#essentially the players postion is tracked on screen and if that plus half the
#screen width/height != level width/height, then 1/2 screen width/height is added
#to the players position on the screen not the level 
def complex_camera(camera, target_rect): 
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+halfWinWidth, -t+halfWinHeight, w, h
    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-winWidth), l)    # stop scrolling at the right edge
    t = max(-(camera.height-winHeight), t)  # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return pygame.Rect(l, t, w, h)

#######this is the main code########
mainWin()
