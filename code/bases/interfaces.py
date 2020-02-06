'''
    
    INTERFACES. ONLY FUNCTION CLASSES.

'''
import pygame

class IMAGE_LOADER():
    def load(self, size=32):
        self.image = pygame.image.load(self.folder + self.texturename).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.setSize(size)

class DRAWABLE():
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class DRAWABLE_PER_COORDS():
    def draw_per_coords(self, screen, x, y):
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, self.rect)

class CROSSABLE():
    def isCrossing(self, item):
        return pygame.sprite.spritecollideany(self, item)

    def isMaskCrossing(self, item):
        return pygame.sprite.collide_mask(self, item)

class CHECKER():
    def areCrossed(self, item1, item2):
        pass
        


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
        self.speed = speed

    def changeVector(self, vector):
        self.movingVector = vector

    def move(self, x, y):
        
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
        self.changeMoveTexture(self.movingFrame, self.movingVector)
        self.rect.x = x
        self.rect.y = y
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


class STATIC_VECTOR(STATICABLE):

    def changeStaticTexture(self, frame, vector):
        self.texturename = self.staticImages[vector]


class STATIC_FRAME(STATICABLE):

    def changeStaticTexture(self, frame, vector):
        self.texturename = self.staticImages[frame]


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

    def keyManager(self, key, ads):
        if not ads and key == self.lastKey:
            self.lastKey = None
            self.changeStaticTexture(self.movingFrame, self.movingVector)
        elif ads:
            self.lastKey = key # list(filter(lambda x: (key in x), [self.forward + [], self.back + [], self.right + [], self.left + []]))

    def moveManager(self):
        if self.lastKey in self.forward:
            return [(self.rect.x, self.rect.y + self.speed), (self.rect.x + self.rect.width, self.rect.y + self.rect.height + self.speed)]
        elif self.lastKey in self.back:
            return [(self.rect.x, self.rect.y - self.speed), (self.rect.x + self.rect.width, self.rect.y + self.rect.height - self.speed)]
        elif self.lastKey in self.right:
            return [(self.rect.x + self.speed, self.rect.y), (self.rect.x + self.rect.width + self.speed, self.rect.y + self.rect.height)]
        elif self.lastKey in self.left:
            return [(self.rect.x - self.speed, self.rect.y), (self.rect.x + self.rect.width - self.speed, self.rect.y + self.rect.height)]

#UI METHODS
import sys

class DANGEON_MANAGER():
    def manager(w, h, rules):
        import random
        maps = [[ False for i in range(w + 1)] for i in range(h + 1)]

        binary = [ [0] for i in range(2**(rules["deep"] if "deep" in rules else 4) + 10)]
        sister_bridges = []

        queue = [(0, 1, 1, w - 1, h - 1, 0)]
        i = 1
        # queue[i] = (Index, parentX1, parentY1, parentX2, parentY2, parentIndex)
        # generate binary
        CAN = True
        while i <= 2**(rules["deep"] if "deep" in rules else 4) and CAN:
            newQueue = []
            while len(queue) != 0:
                if i <= 2**(rules["deep"] if "deep" in rules else 4):
                    parent = queue[0]
                    queue.pop(0)
                    if abs(parent[4] - parent[2]) < abs(parent[3] - parent[1]) and parent[3] - parent[1] > 8:
                        if parent[1] + 3 < parent[3] - 3: 
                            line = random.randint(parent[1] + 3, parent[3] - 3)

                            binary[i] = [i, parent[1], parent[2], line, parent[4], max(0, parent[0])]
                            newQueue.append(binary[i])
                            i += 1
                            binary[parent[0]] = [parent[0], line, parent[2], parent[3], parent[4], parent[5]]
                            newQueue.append(binary[parent[0]])
                            sister_bridges.append([i - 1, parent[0]])
                    elif parent[4] - parent[2] > 8:
                        if parent[2] + 3 < parent[4] - 3:
                            line = random.randint(parent[2] + 3, parent[4] - 3)
                            binary[i] = [i, parent[1], parent[2], parent[3], line, max(0, parent[0])]
                            newQueue.append(binary[i])
                            i += 1
                            binary[parent[0]] = [parent[0], parent[1], line, parent[3], parent[4], parent[5]]
                            newQueue.append(binary[parent[0]])

                            sister_bridges.append([i - 1, parent[0]])
                else:
                    queue = []
                    newQueue = []
                    CAN = False
                    break
            queue = sorted(newQueue)
        #print(binary)
        binary = list(filter(lambda x: len(x) == 6, binary))
        binaryNew = binary + []
        for area in binary:
            rWid = area[3] - area[1]#random.randint(max(3, area[3] - area[1] - 1), area[3] - area[1])
            rHei = area[4] - area[2]#random.randint(2, area[4] - area[2])

            rWid = max(1, area[3] - area[1] - 2)
            rHei = max(1, area[4] - area[2] - 2)
            #print(rWid, rHei, area[0])
            for i in range(area[1], area[1] + rWid + 1):
                for j in range(area[2], area[2] + rHei + 1):
                    try:
                        binary[area[0]] = [area[0], area[1], area[2], area[1] + rWid, area[2] + rHei, area[1]]
                        maps[j][i] = True
                    except:
                        print("ERROR", i, j, rWid, rHei, area)
        # do some bridges
        for line in sister_bridges:
            #print(line, len(binary))
            if binary[line[0]][3] < binary[line[1]][1]:
                # means that i.x < parent.x; need corridor to right
                y = (binary[line[0]][4] - binary[line[0]][2]) // 2 + binary[line[0]][2]
                #print(line)
                for i in range(binary[line[0]][3], binary[line[1]][1]):
                    try:
                        maps[y][i] = True #str(area[0])
                    except:
                        print("ERROR", i, j, rWid, rHei, area)
            if binary[line[1]][2] > binary[line[0]][4]:
                # need corridor to down
                x = (binary[line[0]][3] - binary[line[0]][1]) // 2 + binary[line[0]][1]
                #print(line)
                for i in range(binary[line[0]][4], binary[line[1]][2]):
                    try:
                        maps[i][x] = True #str(area[0])
                    except:
                        print("ERROR", i, j, rWid, rHei, area)

        return maps


if __name__ == '__main__':
    print("\n".join(list(map(lambda x: " ".join(list(map(lambda y: "{:3d}".format(int(y)), x))), DANGEON_MANAGER.manager(48, 48, {"deep":4})))))