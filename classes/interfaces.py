'''
    
    INTERFACES. ONLY FUNCTION CLASSES.

'''
import pygame
import math
import  classes.essences as ESSENCE

class RESIZEABLE():
    def resizeImage(self):
        self.image = pygame.transform.scale(self.image, (self.width * self.cell, self.height * self.cell))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def setSize(self, sizeW=None, sizeH=None, cell=None):
        if cell is not None:
            self.cell = cell
        if sizeW is not None:
            self.width = sizeW
        if sizeH is not None:            
            self.height = sizeH
        self.load()
        self.resizeImage()

class IMAGE_LOADER(RESIZEABLE):
    def load(self):
        self.image = pygame.image.load(self.folder + self.texturename).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.resizeImage()

class DRAWABLE(IMAGE_LOADER):
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class DRAWABLE_PER_COORDS(DRAWABLE):
    def draw_per_coords(self, screen, x, y):
        old_coords = (self.rect.x, self.rect.y)
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, self.rect)
        self.rect.x = old_coords[0]
        self.rect.y = old_coords[1]

class CROSSABLE(DRAWABLE_PER_COORDS):
    def isCrossing(self, item):
        a = pygame.sprite.Group()
        a.add(item)
        return pygame.sprite.spritecollideany(self, a)

    def isMaskCrossing(self, item):
        self.mask = pygame.mask.from_surface(self.image)
        return pygame.sprite.collide_mask(self, item)

class CHECKER():
    def areCrossed(self, item1, item2):
        pass
        
#MOVING

class STATICABLE():
    def staticImagesInit(self, staticImages):
        self.staticImages = staticImages

    def changeVector(self, vector):
        self.movingVector = vector

class MOVEABLE():

    def changeMoveTexture(self, *arg, **args):
        pass

    def moveableInit(self):
        self.movingFrame = 0
        self.movingVector = 0

    def setSpeedPerTick(self, speed):
        self.rawSpeed = speed

    def changeVector(self, vector):
        self.movingVector = vector

    def moveToCell(self, cell):
        x = cell[0]
        y = cell[1]
        self.movingFrame = (self.movingFrame + 1) % 2
        if self.x < x:
            # right
            self.movingVector = 0
        if self.y > y:
            # down
            self.movingVector = 1
        if self.x > x:
            # left
            self.movingVector = 2
        elif self.y < y:
            # right
            self.movingVector = 3
        # self.changeMoveTexture(self.movingFrame, self.movingVector)
        self.rect.x = x * self.cell
        self.rect.y = y * self.cell
        self.x = x
        self.y = y

#MOVEABLE METHODS


class MOVE_ANIMATED(MOVEABLE):

    def moveImagesInit(self, moveImages):
        self.texturename = moveImages[0][0]
        self.moveImages = moveImages

    def changeMoveTexture(self, frame, vector):
        if frame == -1:
            print(
                "MOVE_ANIMATED CLASS ERROR, HAVE -1 MOVING FRAME ON MOVING EVENT. object: ", self)
        else:
            self.texturename = self.moveImages[vector][frame]


class MOVE_FRAME(MOVE_ANIMATED):
    def changeMoveTexture(self, frame, vector):
        self.texturename = self.moveImages[frame]


class MOVE_VECTOR(MOVE_ANIMATED):
    def changeMoveTexture(self, frame, vector):
        self.texturename = self.moveImages[vector]


#STATIC METHODS

class STATIC_ANIMATED(STATICABLE):

    def staticImagesInit(self, staticImages):
        self.staticImages = staticImages

    def changeStaticTexture(self, frame, vector):
        if frame == -1:
            print(
                "STATIC_ANIMATED CLASS ERROR, HAVE -1 MOVING FRAME ON STATIC EVENT. object: ", self)
        else:
            self.texturename = self.staticImages[vector][frame]


class STATIC_VECTOR(STATIC_ANIMATED):

    def changeStaticTexture(self, frame, vector):
        self.texturename = self.staticImages[vector]


class STATIC_FRAME(STATIC_ANIMATED):

    def changeStaticTexture(self, frame, vector):
        self.texturename = self.staticImages[frame]

class VECTORMOVEABLE(CROSSABLE):
    def initVector(self, vector=0, radialSpeed=0):
        self.vector = vector
        self.newVector = -60
        self.radialSpeed = radialSpeed
        self.position = -1

    def setRadSpeed(self, speed):
        self.radialSpeed = speed # degrees per tick

    def setNormal(self):
        self.vector = 0 #degrees

    def setVector(self, vector):
        self.vector = vector

    def setNewVector(self, nv):
        self.newVector = nv

    def countVector(self, timer):
        if self.vector != self.newVector: self.vector += self.radialSpeed * timer * (-1 if self.vector > self.newVector else 1)
        if self.vector > 60: self.vector = 60
        if self.vector < -60: self.vector = -60

    def deltaPosByRad(self, ticks):
        self.countVector(ticks)
        return round(self.rawSpeed * ticks * math.sin(self.vector / 180 * math.pi), 2)


class CONTROLLED(MOVEABLE):
    def initControlKeys(self, keys={}):
        self.forward = keys["forward"]
        self.back = keys["back"]
        self.right = keys["right"] 
        self.left = keys["left"]
        self.lastKey = None
        self.all = self.forward + self.back + self.right + self.left
        self.moveableInit()

    def useable(self, key):
        return (key in self.all)

    def correctPos(self, pos):
        x = pos[0] * self.cell
        y = pos[1] * self.cell
        if x < -1 * self.rect.width // 2 or y < 0:
            return False
        if x > self.surface.get_width() - self.rect.width // 2 or y > self.surface.get_height() - self.rect.height:
            return False


        return True

    def move(self, t=1000):
        newPos = self.newPosManager(time=t)
        if newPos is not None and self.correctPos(newPos):
            self.moveToCell(newPos)


    def keyManager(self, key, ads=True):
        '''
        if not ads and key == self.lastKey:
            self.lastKey = None
            self.changeStaticTexture(self.movingFrame, self.movingVector)
        elif ads:
            self.lastKey = key # list(filter(lambda x: (key in x), [self.forward + [], self.back + [], self.right + [], self.left + []]))
        '''
        self.lastKey = key

    def newPosManager(self, time=1000):
        time /= 1000
        if self.lastKey in self.forward:
            return (self.x, self.y - self.rawSpeed * self.cell * time)
            
        elif self.lastKey in self.back:
            return (self.x, self.y + self.rawSpeed * self.cell * time)
            
        elif self.lastKey in self.right:
            return (self.x + self.rawSpeed * self.cell * time, self.y)
            
        elif self.lastKey in self.left:
            return (self.x - self.rawSpeed * self.cell * time, self.y)


class SHOOTING():
    def shootInit(self, speed=500):
        self.shootingSpeed = speed

    def createBullet(self):
        Bullet = ESSENCE.BULLET(self, self.x + self.width, self.y + self.height // 2, self.cell)
        Bullet.moveableInit()
        Bullet.setSize(1, 1)
        return Bullet

    def shoot(self):
        return self.createBullet()
            



# SOUNDER

class SPEACKING():

    def initSound(self, sound):
        pass

    def play(self):
        pass
        

class KILLABLE():
    def setMaxHP(self, hp=100):
        self.maxHP = hp

    def setHP(self, hp=100):
        self.hp = hp
        self.maxHP = hp

    def reborn(self, hp=None):
        if hp is not None:
            self.setHP(hp)
        self.hp = self.maxHP

    def getHP(self):
        return self.hp

    def getMaxHP(self):
        return self.maxHP

    def getDamage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = -1

    def isAlive(self):
        return (self.hp > 0)

    def kill(self):
        self.hp = -1
        #self = DEADSPRITE(self.x, self.x, self.cell, self.folder, texturename='/dead.png')