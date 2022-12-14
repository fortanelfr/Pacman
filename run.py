import pygame
from pygame.locals import *
from src.constants import *
from src.pacman import Pacman
from src.nodes import NodeGroup
from src.pellets import PelletGroup
from src.ghosts import GhostGroup
from src.fruit import Fruit
from src.pauser import Pause
from src.text import TextGroup
from src.sprites import LifeSprites
from src.sprites import MazeSprites

class GameController(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pacman')
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self .background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0

    def setBackground(self):
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level%5)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        self.flashBG = False
        self.background = self.background_norm

    def startGame(self):
        self.mazesprites = MazeSprites("mazes/maze1.txt", "mazes/maze1_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup("mazes/maze1.txt")
        self.nodes.setPortalPair((0,17), (27,17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
        self.pellets = PelletGroup("mazes/maze1.txt")

        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))

        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.nodes.denyAccessList(12, 14, UP, self.ghosts)
        self.nodes.denyAccessList(15, 14, UP, self.ghosts)
        self.nodes.denyAccessList(12, 26, UP, self.ghosts)
        self.nodes.denyAccessList(15, 26, UP, self.ghosts)
        self.game_start = pygame.mixer.Sound("sound/game_start.wav")
        self.siren_1 = pygame.mixer.Sound("sound/siren_1.wav")
        self.siren_2 = pygame.mixer.Sound("sound/siren_2.wav")
        self.siren_3 = pygame.mixer.Sound("sound/siren_3.wav")
        self.siren_4 = pygame.mixer.Sound("sound/siren_4.wav")
        self.siren_5 = pygame.mixer.Sound("sound/siren_5.wav")
        self.power = pygame.mixer.Sound("sound/power_pellet.wav")
        self.eat_ghost = pygame.mixer.Sound("sound/eat_ghost.wav")
        self.eat_fruit = pygame.mixer.Sound("sound/eat_fruit.wav")
        self.spawn = pygame.mixer.Sound("sound/retreating.wav")
        self.loop_channel = pygame.mixer.Channel(0)
        self.eat_ghost_channel = pygame.mixer.Channel(2)
        self.start_channel = pygame.mixer.Channel(3)
        self.current__sound = None
        self.new_sound = self.game_start
        if self.new_sound == self.game_start:
                   self.start_channel.play(self.new_sound)
                   self.new_sound = self.siren_1



    def update(self):
        dt = self.clock.tick(30)/ 1000.0
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            if self.ghosts.Spawn_state():
                self.new_sound = self.spawn
            elif self.ghosts.Freight_state():
                self.new_sound = self.power
            elif self.pellets.numEaten >= 195:
                self.new_sound = self.siren_5
            elif self.pellets.numEaten >= 122:
                self.new_sound = self.siren_4
            elif self.pellets.numEaten >= 70:
                self.new_sound = self.siren_3
            elif self.pellets.numEaten >= 30:
                self.new_sound = self.siren_2    
            else:
                self.new_sound = self.siren_1

            if not self.current__sound == self.new_sound:
                self.loop_channel.play(self.new_sound,-1)
                self.current__sound = self.new_sound
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()
        else:
            if self.loop_channel.get_busy():
               self.loop_channel.stop()
               self.current__sound = None
               print('pausa')

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()
    
    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    pygame.mixer.Sound.play(self.eat_ghost)
                    self.pacman.visible = False
                    self.updateScore(ghost.points)
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    ghost.visible = False
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current is not SPAWN:
                     if self.pacman.alive:
                         self.lives -=  1
                         self.lifesprites.removeImage()
                         self.pacman.die()                        
                         self.ghosts.hide()
                         if self.lives <= 0:
                             self.textgroup.showText(GAMEOVERTXT)
                             self.pause.setPause(pauseTime=3, func=self.restartGame)
                         else:
                             self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20))
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                pygame.mixer.Sound.play(self.eat_fruit)
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1) 
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None


    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                #it's only possible to start the game if the start sound has finished
                if not self.start_channel.get_busy():
                    if event.key == K_SPACE  and self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSETXT)
                            self.hideEntities()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        #Dejamos de dibujar los nodos
        #self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)
        

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))
        
        pygame.display.update()

    
    def checkPelletEvents(self):
        munch = [pygame.mixer.Sound("sound/munch_2.wav"),pygame.mixer.Sound("sound/munch_1.wav")]
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:  
            pygame.mixer.Sound.play(munch[self.pellets.numEaten % 2])
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
                
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
               self.ghosts.startFreight()
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)

    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)
        self.startGame()

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)
        

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
