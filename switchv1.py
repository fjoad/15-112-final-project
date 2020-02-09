import pygame

winHeight = 700
winWidth = 900
halfWinHeight = winHeight/2
halfWinWidth = winWidth/2
win = (winWidth,winHeight)
pixel = 32
pixelBlock = (32,32)



class Object(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)




class Player(Object):
    def __init__(self, x, y):
        Object.__init__(self)
        self.xVelocity = 0
        self.yVelocity = 0
        self.onGround = False
        self.image = pygame.Surface(pixelBlock)
        self.image.fill(pygame.Color("#00FF00"))
        self.rect = pygame.Rect(x, y, pixel, pixel)

    def update(self, up, down, left, right, move, platforms, spikes):
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
        self.collide(self.xVelocity, 0, platforms, spikes)
        # increment in y direction
        self.rect.top += self.yVelocity
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yVelocity, platforms, spikes)

    def collide(self, xvelocity, yVelocity, platforms, spikes):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                #if isinstance(p, ExitBlock):
                #    pygame.event.post(pygame.event.Event(QUIT))
                if xvelocity > 0:
                    self.rect.right = p.rect.left
                    #print "collide right"
                if xvelocity < 0:
                    self.rect.left = p.rect.right
                    #print "collide left"
                if yVelocity > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yVelocity = 0
                if yVelocity < 0:
                    self.rect.top = p.rect.bottom
        for s in spikes:
            if pygame.sprite.collide_rect(self, s):
                mainWin()

            
class Spike(Object):
    def __init__(self, x, y):
        Object.__init__(self)
        #self.image = pygame.Surface((32, 32))
        #self.image.convert()
        #self.image.fill(pygame.Color("#00FF00"))
        self.image = pygame.image.load("spikes.png")
        self.rect = pygame.Rect(x, y, pixel, pixel)
    def update(self):
        pass



class Platform(Object):
    def __init__(self, x, y):
        Object.__init__(self)
        self.image = pygame.Surface(pixelBlock)
        #self.image.convert()
        self.image.fill(pygame.Color("#FFFFFF"))
        self.rect = pygame.Rect(x, y, pixel, pixel)

    def switchColorAndPosition(self,switch):
        if switch:
            self.image.fill(pygame.Color("#000000" ))
            #self.rect = Rect(self.x+30, self.y, 32, 32)
            #self.rect.x -= 30
            self.rect = self.rect.move(-100,0)
        else:
            self.image.fill(pygame.Color("#FFFFFF"))
            #self.rect = Rect(self.x-30, self.y, 32, 32)
            #self.rect.x += 30
            self.rect = self.rect.move(+100,0)

    def update(self):
        pass


        
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def mainWin():
    pygame.init()
    mainWin = pygame.display.set_mode(win)
    clock = pygame.time.Clock()
    up = False
    down = False
    left = False
    right = False
    move = False
    #switch = False
    background  = pygame.Surface(pixelBlock)
    background.fill(pygame.Color("#000000"))
    objects = pygame.sprite.Group()
    player = Player(pixel, pixel)
    #objects.add(player)
    platforms = []
    spikes = []
    x=0
    y=0
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                    PPPPPPPPPPP           P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P    PPPPPPPP                              P",
        "P                                          P",
        "P                          PPPPPPP         P",
        "P                 PPPPPP                   P",
        "P                                          P",
        "P         PPPPPPP                          P",
        "P                                          P",
        "P                     PPPPPP               P",
        "P                                          P",
        "P   PPPPPPPPPPP                            P",
        "P                                          P",
        "P                 PPPPPPPPPPP              P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                                         SP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    for row in level:
        for column in row:
            if column == "P":
                platform = Platform(x,y)
                platforms.append(platform)
                objects.add(platform)
            if column == "S":
                s = Spike(x, y)
                spikes.append(s)
                objects.add(s)
            x+=pixel
        y+=pixel
        x=0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    objects.add(player)
    switch = False

    while True:
        clock.tick(60)
        for i in pygame.event.get():
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

            if i.type == pygame.KEYUP and i.key == pygame.K_UP:
                up = False
            if i.type == pygame.KEYUP and i.key == pygame.K_DOWN:
                down = False
            if i.type == pygame.KEYUP and i.key == pygame.K_RIGHT:
                right = False
            if i.type == pygame.KEYUP and i.key == pygame.K_LEFT:
                left = False

        if switch == False:
            background.fill(pygame.Color("#000000"))
            #fill the background color
            for q in range(pixel):
                for p in range(pixel):
                    mainWin.blit(background,(p*pixel,q*pixel))
            camera.update(player)

            #show other objects on the screen and update the main char
            player.update(up, down, left, right, move, platforms, spikes)
            for o in objects:
                mainWin.blit(o.image, camera.apply(o))
        else:
            background.fill(pygame.Color("#FFFFFF"))
            #fill background
            for q in range(pixel):
                for p in range(pixel):
                    mainWin.blit(background,(p*pixel,q*pixel))
            camera.update(player)
            #show other objects on the screen and update the main char
            player.update(up, down, left, right, move, platforms, spikes)
            for o in objects:
                mainWin.blit(o.image, camera.apply(o))

        pygame.display.update()
            
def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return pygame.Rect(-l+halfWinWidth, -t+halfWinHeight, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+halfWinWidth, -t+halfWinHeight, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-winWidth), l)   # stop scrolling at the right edge
    t = max(-(camera.height-winHeight), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return pygame.Rect(l, t, w, h)





#class ExitBlock(Platform):
#    def __init__(self, x, y):
#        Platform.__init__(self, x, y)
#        self.image.fill(pygame.Color("#0033FF"))

#if __name__ == "__main__":
#    mainWin()

mainWin()
