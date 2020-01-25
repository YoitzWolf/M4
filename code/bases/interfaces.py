'''
	
	INTERFACES. ONLY FUNCTION CLASSES.

'''


class STATICABLE():

    def changeVector(self, vector):
        self.movingVector = vector


class MOVEABLE():

    def moveableInit(self):
        self.movingFrame = 0
        self.movingVector = 0

    def setSpeedPerTick(self, speed):
        self.speed = speed

    def move(self, x, y):
        self.movingFrame = (self.movingFrame + 1) % 2
        if self.x < x:
            # down
            self.movingVector = 0
        if self.y > y:
            # left
            self.movingVector = 1
        if self.x > x:
            # up
            self.movingVector = 2
        elif self.y < y:
            # right
            self.movingVector = 3

        if issubclass(self, MOVE_ANIMATED):
            self.changeMoveTexture(self.movingFrame, self.movingVector)
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y


class MOVE_ANIMATED(MOVEABLE):

    def moveImagesInit(self, moveImages):
        self.moveImages = moveImages

    def changeMoveTexture(self, frame, vector):
        if frame == -1:
            print(
                "MOVE_ANIMATED CLASS ERROR, HAVE -1 MOVING FRAME ON MOVING EVENT. object: ", self)
        else:
            self.imageName = self.moveImages[vector][frame]


class MOVE_FRAME(MOVEABLE):

    def moveImagesInit(self):
        self.moveImages = moveImages

    def changeMoveTexture(self, frame, vector):
        self.imageName = self.moveImages[frame]


class MOVE_VECTOR(MOVEABLE):

    def moveImagesInit(self):
        self.moveImages = moveImages

    def changeMoveTexture(self, frame, vector):
        self.imageName = self.moveImages[vector]


class STATIC_ANIMATED(STATICABLE):

    def staticImagesInit(self, staticImages):
        self.staticImages = staticImages

    def changeStaticTexture(self, frame, vector):
        if frame == -1:
            print(
                "STATIC_ANIMATED CLASS ERROR, HAVE -1 MOVING FRAME ON STATIC EVENT. object: ", self)
        else:
            self.imageName = self.staticImages[vector][frame]


class STATIC_VECTOR(STATICABLE):

    def staticImagesInit(self, staticImages):
        self.staticImages = staticImages

    def changeStaticTexture(self, frame, vector):
        self.imageName = self.staticImages[vector]


class STATIC_FRAME(STATICABLE):

    def staticImagesInit(self, staticImages):
        self.staticImages = staticImages

    def changeStaticTexture(self, frame, vector):
        self.imageName = self.staticImages[frame]
