import pygame
import math
import time
import random
import copy

keys = keys = ['$-MUSIC-$', '$-SCORES-$',
               '$-FONTS-$', '$-END-$', '$-TEXTURES-$']

total = {'info': {}, 'MUSIC': {'FOLDER': 'data/music'}, 'SCORES': {'BEST': '0', 'LAST': '0'}, 'FONTS': {'FONT': 'data/ps2p-rr.ttf'}, 'TEXTURES': {'SHIP': 'data/bg/ship', 'BULLET': 'data/bg/bullet', 'BASTARD': 'data/bg/bastard'}}

class PAUSE():
    """MAIN VIEW CLASS"""

    def __init__(self, display, disableEvent, flipEvent, rules={}):
        self.disableEvent = disableEvent
        self.flipEvent = flipEvent
        self.screen = display
        self.timers = {}
        self.colors = COLORS()
        self.fps = 30
        self.clock = pygame.time.Clock()

        self.info = rules

        self.quit = pygame.QUIT
        self.keyDown = pygame.KEYDOWN
        self.keyUp = pygame.KEYUP
        self.moseMoved = pygame.MOUSEMOTION
        self.mouseUp = pygame.MOUSEBUTTONUP
        self.mouseDown = pygame.MOUSEBUTTONDOWN
        self.sizeChanged = pygame.VIDEORESIZE

        self.textstr = "PAUSE"
        self.startstr = "Press Enter to Play!"

    def createNewTimer(self, eventName, thisTime, event):
        pygame.time.set_timer(eventName, int(thisTime))
        self.timers[eventName] = (thisTime, event)

    def reloadSize(self, event):
        event.dict['size'] = max(event.dict['size'][0], 320), max(
            event.dict['size'][1], 320)
        self.screen = pygame.display.set_mode(
            event.dict['size'], pygame.RESIZABLE)
        self.width, self.height = self.screen.get_size()
        self.font = pygame.font.Font(
            self.info['FONTS']['FONT'], self.screen.get_width() // (4 + len(self.textstr)))
        self.fontH = pygame.font.Font(self.info['FONTS'][
                                      'FONT'], (self.screen.get_width() // (2 * len(self.startstr))))

    def initBackgound(self):
        self.font = pygame.font.Font(
            self.info['FONTS']['FONT'], self.screen.get_width() // (4 + len(self.textstr)))
        self.fontH = pygame.font.Font(self.info['FONTS'][
                                      'FONT'], (self.screen.get_width() // (2 * len(self.startstr))))
        self.pallete = self.colors.getTuple()
        self.point = 0
        self.pallete_size = len(self.pallete)
        self.color = self.pallete[self.point]

        standart_hid = self.screen.get_height() // 2
        self.text = self.font.render(self.textstr, 0, self.color[1])
        self.text_coords = (random.randint(self.text.get_width() // len(self.textstr),
                                           self.screen.get_width() - self.text.get_width() - self.text.get_width() // len(self.textstr)),
                            standart_hid + random.randint(-1 * self.text.get_height() // 8, self.text.get_height() // 8))

        self.start = self.fontH.render(self.startstr, 0, self.color[1])
        self.start_coords = (self.text_coords[
                             0], standart_hid + random.randint(-1 * self.text.get_height() // 8, self.text.get_height() // 8))

    def animate(self):
        self.color = self.pallete[self.point]
        random.shuffle(self.color)
        self.point += 1
        self.point %= self.pallete_size

        self.text = self.font.render(self.textstr, 0, self.color[1])
        #
        standart_hid = max(self.text.get_height(
        ) // 2, self.screen.get_height() // 2 - self.text.get_height() * 2)

        self.text_coords = (random.randint(self.text.get_width() // len(self.textstr),
                                           self.screen.get_width() - self.text.get_width() - self.text.get_width() // len(self.textstr)),
                            standart_hid + random.randint(-1 * self.text.get_height() // 4, self.text.get_height() // 4))

        self.start = self.fontH.render(self.startstr, 0, self.color[1])
        self.start_coords = ((self.screen.get_width() - self.start.get_width()) // 2,
                             max(self.text.get_height() * 2, self.screen.get_height() - 3 * self.start.get_height()))

    def render(self):
        self.screen.fill(self.color[0])
        self.screen.blit(self.text, self.text_coords)
        self.screen.blit(self.start, self.start_coords)
        self.flipEvent()

    def loop(self, thisDisabler=None, thisFlipper=None):
        if thisDisabler is not None:
            self.disableEvent = thisDisabler
        if thisFlipper is not None:
            self.flipEvent = thisFlipper

        pygame.mouse.set_visible(False)
        self.width, self.height = self.screen.get_size()

        self.initBackgound()

        class sizer():

            def __init__(self, screen):
                self.dict = {}
                self.dict['size'] = [screen.get_width(), screen.get_height()]

        self.reloadSize(sizer(self.screen))

        self.createNewTimer(30, 50, lambda: self.render())
        self.createNewTimer(31, 400, lambda: self.animate())
        # main Loop
        while 1:
            for Event in pygame.event.get():
                t = Event.type
                if t == self.quit:
                    self.disableEvent()
                    return
                if t == self.keyDown and Event.key == 13:
                    return self.screen
                if t == self.sizeChanged:
                    self.reloadSize(Event)
                if t in self.timers:
                    self.timers[t][1]()


class GAME():
    """MAIN GAME CLASS"""

    def summon(self):
        self.wave += 1
        i = 0
        r = random.randint(1, min(self.wave, self.back.cells_in_line - 2))
        while len(self.bastards) < r:
            self.bastards.append( BASTARD(self.back.lines_count - 2, len(self.bastards) + (self.back.cells_in_line - r)//2, self.info['TEXTURES']['BASTARD']) )
            self.bastards[-1].changeStaticTexture(0, 0)
            self.bastards[-1].load()
            self.bastards[-1].setSize(cell=self.back.cellSize)

    def __init__(self, display, disableEvent, flipEvent, rules={}):

        self.wave = 0
        self.bastards = []

        self.disableEvent = disableEvent
        self.flipEvent = flipEvent
        self.screen = display
        self.timers = {}
        self.colors = COLORS()
        self.fps = 30
        self.clock = pygame.time.Clock()

        self.info = rules

        self.bullets = []

        self.bastardBullets = []

        self.quit = pygame.QUIT
        self.keyDown = pygame.KEYDOWN
        self.keyUp = pygame.KEYUP
        self.moseMoved = pygame.MOUSEMOTION
        self.mouseUp = pygame.MOUSEBUTTONUP
        self.mouseDown = pygame.MOUSEBUTTONDOWN
        self.sizeChanged = pygame.VIDEORESIZE

        self.score = 0

        self.font = pygame.font.Font(
            self.info['FONTS']['FONT'], self.screen.get_height() // 30)

    def createNewTimer(self, eventName, thisTime, event):
        pygame.time.set_timer(eventName, int(thisTime))
        self.timers[eventName] = (thisTime, event)

    def reloadSize(self, event):
        event.dict['size'] = max(event.dict['size'][0], 320), max(
            event.dict['size'][1], 320)
        self.screen = pygame.display.set_mode(
            event.dict['size'], pygame.RESIZABLE)
        self.width, self.height = self.screen.get_size()

        self.back.resize(self.width, self.height)

        for bullet in self.bullets:
            bullet.setSize(cell=self.back.cellSize)

        for bullet in self.bastardBullets:
            bullet.setSize(cell=self.back.cellSize)

        for bastard in self.bastards:
            bastard.setSize(cell=self.back.cellSize)

        self.player.width = 1
        self.player.height = 1
        self.player.cell = self.back.cellSize
        self.player.setLayout(self.back.surface)
        self.player.load()

        self.font = pygame.font.Font(
            self.info['FONTS']['FONT'], self.screen.get_height() // 30)

    def initBackgound(self):
        self.back = BACKGROUND(self.width, self.height, rules=self.info)
        for i in range(self.back.lines_count):
            self.back.add_row()

    def moveEvent(self):
        t = self.clock.tick()
        self.back.move(t)
        # self.player.move(t)
        self.player.y += -1 * self.player.deltaPosByRad(t) / self.player.cell
        if self.player.y * self.player.cell < 0:
            self.player.y = 0
        if self.player.y > self.back.h:
            self.player.y = self.back.h
        #   self.player.rect.y += self.player.y
        #   print(self.player.vector, self.player.newVector, end='; ')
        #   self.player.countVector(t)
        #   print(self.player.vector, self.player.newVector, self.player.y * self.player.cell)
        c = 0
        for bullet in self.bullets:
            bullet.moveToCell([bullet.x + bullet.delta(t), bullet.y])
            if bullet.rect.x > self.screen.get_width():
                self.bullets.remove(bullet)

        for bullet in self.bastardBullets:
            bullet.moveToCell([bullet.x - bullet.delta(t), bullet.y])
            if bullet.rect.x < 0:
                self.bastardBullets.remove(bullet)
            if self.player.isMaskCrossing(bullet): 
                self.player.hp -= 200
                self.bastardBullets.remove(bullet)

        for bastard in self.bastards:
            bastard.moveToCell((bastard.x - bastard.delta(t), bastard.y))
            bastard.rect.x = bastard.x * bastard.cell
            bastard.rect.y = bastard.y * bastard.cell
            if self.player.isMaskCrossing(bastard):
                print(10)
                self.player.hp -= 100
                self.bastards.remove(bastard)
            elif bastard.x * bastard.cell <= 0:
                self.bastards.remove(bastard)
            elif any(list(map(lambda x: x.isMaskCrossing(bastard), self.bullets ))):
                self.bastards.remove(bastard)
                self.score += 1
                for i in filter(lambda x: x.isMaskCrossing(bastard), self.bullets ):
                    self.bullets.remove(i)

    def render(self):
        self.moveEvent()

        self.screen.fill(self.colors.BLACK)
        self.back.render(self.screen, self.width, self.height)

        self.player.setLayout(self.back.surface)
        self.player.draw_per_coords(
            self.player.surface, self.player.x * self.back.cellSize, self.player.y * self.back.cellSize)

        self.player.rect.x, self.player.rect.y = self.player.x * self.back.cellSize, self.player.y * self.back.cellSize

        for bullet in self.bullets:
            bullet.changeStaticTexture(self.T, 0)
            bullet.load()
            bullet.draw_per_coords(
                self.player.surface, bullet.x * self.back.cellSize, bullet.y * self.back.cellSize)

        for bullet in self.bastardBullets:
            bullet.changeStaticTexture(self.T, 0)
            bullet.load()
            bullet.image =  pygame.transform.rotate(bullet.image, 180)
            bullet.draw_per_coords(
                self.player.surface, bullet.x * self.back.cellSize, bullet.y * self.back.cellSize)


        for bastard in self.bastards:
            bastard.changeStaticTexture(self.T, 0)
            bastard.load()
            bastard.draw_per_coords(
                self.player.surface, bastard.x * self.back.cellSize, bastard.y * self.back.cellSize)

        self.screen.blit(self.player.surface, ((
            self.width - self.back.w) // 2, (self.height - self.back.h) // 2))

        self.text = self.font.render(
            "HP " + str(self.player.hp), 0, self.colors.WHITE)
        self.screen.blit(self.text, (self.text.get_height(),
                                     self.text.get_height() // 2))

        self.text = self.font.render(
            "SCORE " + str(self.score), 0, self.colors.WHITE)
        self.screen.blit(self.text, (self.text.get_height(),
                                     self.text.get_height() * 2))

        pygame.draw.rect(self.screen, self.colors.WHITE, (pygame.mouse.get_pos()[
                         0] - 10, pygame.mouse.get_pos()[1] - 10, 20, 20), 3)

        self.flipEvent()

    def countDegs(self):
        # (-1 if pygame.mouse.get_pos()[1] > self.player.y * self.player.cell else 1) *
        try:
            return math.atan((pygame.mouse.get_pos()[1] - (self.player.y + 0.5 * self.player.height) * self.player.cell) / abs(pygame.mouse.get_pos()[0] - self.player.x * self.player.cell)) / math.pi * -180
        except:
            return 90

    def built(self):
        self.bullets.append(self.player.createBullet())
        self.player.changeStaticTexture(self.T, 0)
        self.player.load()
        self.T += 1
        self.T %= 2
        for bastard in self.bastards:
            if random.randint(1, 100) < 25:
                self.bastardBullets.append(bastard.createBullet())

    def loop(self, thisDisabler=None, thisFlipper=None):
        self.T = 0
        if thisDisabler is not None:
            self.disableEvent = thisDisabler
        if thisFlipper is not None:
            self.flipEvent = thisFlipper

        self.width, self.height = self.screen.get_size()

        self.initBackgound()

        self.player = PLAYER(4, 4, self.info['TEXTURES']['SHIP'])

        self.player.staticImagesInit(
            ["/player_f1.png", "/player_f0.png", "/player_f0.png", "/player_f1.png"])
        self.player.changeStaticTexture(0, 0)
        self.player.load()

        class sizer():

            def __init__(self, screen):
                self.dict = {}
                self.dict['size'] = [screen.get_width(), screen.get_height()]

        self.reloadSize(sizer(self.screen))

        self.createNewTimer(30, 50, lambda: self.render())
        self.createNewTimer(31, 700, lambda: self.built())
        # main Loop
        # space is 32
        self.player.setNewVector(0)
        if (0 <= pygame.mouse.get_pos()[0] <= self.screen.get_width() and 0 <= pygame.mouse.get_pos()[1] <= self.screen.get_height()):
            self.player.setNewVector(self.countDegs())
        else:
            self.player.setNewVector(0)

        while 1:
            if len(self.bastards) <= 0:
                self.summon()

            if not self.player.isAlive():
                # print(1)
                return self.screen, self.score

            if (0 <= pygame.mouse.get_pos()[0] <= self.screen.get_width() and 0 <= pygame.mouse.get_pos()[1] <= self.screen.get_height()):
                self.player.setNewVector(self.countDegs())
            else:
                self.player.setNewVector(0)

            for Event in pygame.event.get():
                t = Event.type
                if t == self.keyDown and Event.key == 13:
                    self.screen = PAUSE(
                        self.screen, self.disableEvent, self.flipEvent, rules=self.info).loop()
                    self.reloadSize(sizer(self.screen))
                    self.clock.tick()
                    self.createNewTimer(30, 50, lambda: self.render())
                    self.createNewTimer(31, 500, lambda: self.built())
                    # return self.screen
                '''
                if t == self.keyDown:
                    print(Event.key)
                    self.player.lastKey = Event.key

                if t == self.keyUp:
                    if self.player.lastKey == Event.key:
                        self.player.lastKey = None
                '''
                if t == self.sizeChanged:
                    self.reloadSize(Event)

                if t == self.quit:
                    self.disableEvent()
                    return self.screen

                if t in self.timers:
                    self.timers[t][1]()


class STRATER():
    """MAIN VIEW CLASS"""

    def initMusicPlayer(self):
        self.musicFolder = self.info['MUSIC']['FOLDER']
        self.manager.setFolder(self.musicFolder + '/')
        self.musicFiles = self.manager.readFolder()
        # print(self.musicFiles)
        name = self.musicFolder + '/' + self.musicFiles[0]
        print(name)
        pygame.mixer.init(22050, -16, 2, 2048)
        pygame.mixer.music.load(name)
        pygame.mixer.music.unpause()
        pygame.mixer.music.play()

    def __init__(self, display, disableEvent, flipEvent, configer="config.data"):
        self.configer = configer
        pygame.init()
        self.textstr = "Space Warrior"
        self.beststr = ""
        self.startstr = "Press Enter to Play!"
        self.disableEvent = disableEvent
        self.flipEvent = flipEvent
        self.screen = display
        self.timers = {}
        self.colors = COLORS()
        self.fps = 30
        self.clock = pygame.time.Clock()
        self.manager = MANAGER()
        self.manager.setFolder("")
        try:
            self.manager.chooseFile(configer)
            data = []
            for i in self.manager.readFile():
                if("$-END-$" in i):
                    break
                data.append(i)

            self.info = total
            key = 'info'
            self.info['another'] = []
            for i in range(len(data)):
                if "$-" in data[i] and data[i].rstrip('\n') in keys:
                    key = ("" + data[i].rstrip('\n')
                           ).replace('$-', '').replace('-$', '')
                else:
                    if key not in self.info:
                        self.info[key] = {}
                    s = data[i].rstrip('\n')
                    if ' = ' in s:
                        d = s.split(' = ')
                        if len(d) >= 2:
                            self.info[key][d[0].replace('$', '')] = d[1]
                    else:
                        self.info['another'].append((key, s))
            print(self.info)
        except Exception as e:
            print(e)
            self.info = total

        try:
            self.initMusicPlayer()
            self.beststr = "Best Score: " + \
                str(int(self.info['SCORES']['BEST']))

        except Exception as e:
            print(e)

        self.quit = pygame.QUIT
        self.keyDown = pygame.KEYDOWN
        self.keyUp = pygame.KEYUP
        self.moseMoved = pygame.MOUSEMOTION
        self.mouseUp = pygame.MOUSEBUTTONUP
        self.mouseDown = pygame.MOUSEBUTTONDOWN
        self.sizeChanged = pygame.VIDEORESIZE

    def createNewTimer(self, eventName, thisTime, event):
        pygame.time.set_timer(eventName, int(thisTime))
        self.timers[eventName] = (thisTime, event)

    def reloadSize(self, event):
        event.dict['size'] = max(event.dict['size'][0], 320), max(
            event.dict['size'][1], 320)
        self.screen = pygame.display.set_mode(
            event.dict['size'], pygame.RESIZABLE)
        self.width, self.height = self.screen.get_size()
        self.font = pygame.font.Font(
            self.info['FONTS']['FONT'], self.screen.get_width() // (4 + len(self.textstr)))
        self.fontH = pygame.font.Font(
            self.info['FONTS']['FONT'], (self.screen.get_width() // (2 * len(self.beststr))))

    def initBackgound(self):
        self.font = pygame.font.Font(
            self.info['FONTS']['FONT'], self.screen.get_width() // (4 + len(self.textstr)))
        self.fontH = pygame.font.Font(
            self.info['FONTS']['FONT'], (self.screen.get_width() // (2 * len(self.beststr))))
        self.pallete = self.colors.getTuple()
        self.point = 0
        self.pallete_size = len(self.pallete)
        self.color = self.pallete[self.point]

        standart_hid = self.screen.get_height() // 2
        self.text = self.font.render(self.textstr, 0, self.color[1])
        self.text_coords = (random.randint(self.text.get_width() // len(self.textstr),
                                           self.screen.get_width() - self.text.get_width() - self.text.get_width() // len(self.textstr)),
                            standart_hid + random.randint(-1 * self.text.get_height() // 8, self.text.get_height() // 8))

        self.best = self.fontH.render(self.beststr, 0, self.color[1])
        self.best_coords = (self.text_coords[
                            0], standart_hid + random.randint(-1 * self.best.get_height() // 8, self.best.get_height() // 8))

        self.start = self.fontH.render(self.startstr, 0, self.color[1])
        self.start_coords = (self.best_coords[
                             0], standart_hid + random.randint(-1 * self.best.get_height() // 8, self.best.get_height() // 8))

    def animate(self):
        self.color = self.pallete[self.point]
        random.shuffle(self.color)
        self.point += 1
        self.point %= self.pallete_size

        self.text = self.font.render(self.textstr, 0, self.color[1])
        #
        standart_hid = max(self.text.get_height(
        ) // 2, self.screen.get_height() // 2 - self.text.get_height() * 2)

        self.text_coords = (random.randint(self.text.get_width() // len(self.textstr),
                                           self.screen.get_width() - self.text.get_width() - self.text.get_width() // len(self.textstr)),
                            standart_hid + random.randint(-1 * self.text.get_height() // 4, self.text.get_height() // 4))

        self.best = self.fontH.render(self.beststr, 0, self.color[1])
        self.best_coords = ((self.screen.get_width() - self.best.get_width()) //
                            2, self.text_coords[1] + self.text.get_height() * 2)
        self.best = pygame.transform.rotate(self.best, random.randint(-5, 5))

        self.start = self.fontH.render(self.startstr, 0, self.color[1])
        self.start_coords = ((self.screen.get_width() - self.start.get_width()) // 2,
                             max(self.best_coords[1] + self.best.get_height() * 2, self.screen.get_height() - 3 * self.start.get_height()))

    def render(self):
        self.screen.fill(self.color[0])
        self.screen.blit(self.text, self.text_coords)
        self.screen.blit(self.best, self.best_coords)
        self.screen.blit(self.start, self.start_coords)
        self.flipEvent()

    def saver(self):
        data = open(self.configer, 'w')
        for i in self.info:
            data.write("$-" + i + "-$\n")
            for j in self.info[i]:
                if "$-" + i + "-$" in keys:
                    data.write("$" + str(j) + " = " + str(self.info[i][j]) + '\n')

        data.write("$-END-$\n")
        data.close()

    def loop(self, thisDisabler=None, thisFlipper=None):
        if thisDisabler is not None:
            self.disableEvent = thisDisabler
        if thisFlipper is not None:
            self.flipEvent = thisFlipper

        pygame.mouse.set_visible(False)
        self.width, self.height = self.screen.get_size()

        self.initBackgound()

        class sizer():

            def __init__(self, scr=None):
                self.dict = {}
                if scr is None:
                    self.dict['size'] = [600, 320]
                else:
                    self.dict['size'] = [scr.get_width(), scr.get_height()]

        self.reloadSize(sizer())

        self.createNewTimer(30, 50, lambda: self.render())
        self.createNewTimer(31, 400, lambda: self.animate())
        # main Loop
        while 1:
            for Event in pygame.event.get():
                t = Event.type
                if t == self.quit:
                    self.saver()
                    self.disableEvent()
                    return 0
                if t == self.keyDown and Event.key == 13:
                    self.createNewTimer(30, 50, lambda: 0)
                    self.createNewTimer(31, 400, lambda: 0)
                    # pygame.mixer.music.pause()
                    self.screen, score = GAME(
                        self.screen, self.disableEvent, self.flipEvent, rules=self.info).loop()
                    self.info['SCORES'] = {"BEST": str(max(int(self.info['SCORES']["BEST"]), score)), "LAST": score}
                    self.saver()
                    self.beststr = "Best Score: " + \
                        str(int(self.info['SCORES']['BEST']))
                    self.reloadSize(sizer(scr=self.screen))
                    self.createNewTimer(30, 50, lambda: self.render())
                    self.createNewTimer(31, 400, lambda: self.animate())
                    self.startstr = "Press Enter to Play Again!"
                    # pygame.mixer.music.unpause()
                if t == self.sizeChanged:
                    self.reloadSize(Event)
                if t in self.timers:
                    self.timers[t][1]()


if __name__ == '__main__':
    print("CANT PLAY ON MAIN. IMPORT CLASS TO THE ANOTHER FILE")
    from colors import COLORS
    from manager import MANAGER
    from background import BACKGROUND
    from essences import *
    from screens import STRATER, ENDER

    pygame.font.init()
    screen = pygame.display.set_mode((600, 320), pygame.RESIZABLE)
    game = STRATER(screen, pygame.quit, pygame.display.flip)
    game.loop()
else:
    from classes.colors import COLORS
    from classes.manager import MANAGER
    from classes.background import BACKGROUND
    from classes.essences import *
