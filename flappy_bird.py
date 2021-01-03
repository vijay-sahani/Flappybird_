from pygame.locals import *
import pygame
import sys
import random

GAME_SPRITES = {}
GAME_SOUNDS = {}
ALIVE=3
class flappyBird:
    def __init__(self):
        self.FPS = 32
        self.SCREENWIDTH = 289
        self.SCREENHEIGHT = 511
        self.fontcolor="#ffffff"
        self.SCREEN = pygame.display.set_mode(
            (self.SCREENWIDTH, self.SCREENHEIGHT))
        self.basex = 0
        self.basey = int(self.SCREENHEIGHT*0.8)
        self.PIPE="gallery/sprites/pipe.png"
        GAME_SPRITES["background"] = pygame.image.load(
            "gallery/sprites/background.png").convert()
        GAME_SPRITES["message"] = pygame.image.load(
            "gallery/sprites/message.jpg").convert_alpha()
        GAME_SPRITES["player"] = pygame.image.load(
            "gallery/sprites/bird.png").convert_alpha()
        GAME_SPRITES["base"] = pygame.image.load(
            "gallery/sprites/base.png").convert_alpha()
        GAME_SPRITES["pipe"] = (pygame.transform.rotate(pygame.image.load(self.PIPE).convert_alpha(), 180),
                            pygame.image.load(self.PIPE).convert_alpha())
        GAME_SOUNDS["hit"] = pygame.mixer.Sound("gallery/audio/hit.wav")
        GAME_SOUNDS["point"] = pygame.mixer.Sound("gallery/audio/point.wav")
        GAME_SOUNDS["wing"] = pygame.mixer.Sound("gallery/audio/wing.wav")
        GAME_SOUNDS["swoosh"] = pygame.mixer.Sound(
            "gallery/audio/swoosh.wav")
        GAME_SOUNDS["die"] = pygame.mixer.Sound("gallery/audio/die.wav")

    def welcomeSCREEN(self):
        playerx = int(self.SCREENWIDTH/5)
        playery = int((self.SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
        messagex = int((self.SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
        messagey = int(self.SCREENHEIGHT*0.13)
        while True:
            for event in pygame.event.get():
                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                # If the user presses space or up key, start the game for them
                elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                    return
                else:
                    self.SCREEN.blit(GAME_SPRITES['background'], (0, 0))    
                    self.SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                    self.SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                    self.SCREEN.blit(GAME_SPRITES['base'], (self.basex, self.basey))    
                    pygame.display.update()
                    FPSCLOCK.tick(self.FPS)

    def mainGame(self):
        global ALIVE
        score = 0
        player_x = int(self.SCREENWIDTH/5)
        player_y = int(self.SCREENHEIGHT/2)
<<<<<<< HEAD
        Alive_meter = myfont.render(f"Life:"+"*"*ALIVE, False, (self.fontcolor if ALIVE>=2 else (255,0,0)))
=======
        Alive_meter = myfont.render(f"Life:"+"*"*+ALIVE, False, (self.fontcolor if ALIVE>=2 else (255,0,0)))
>>>>>>> 01874d1af794ea787c985fc4afbebc1cb11732be
        Score_meter = myfont.render(None, False, self.fontcolor)
        Gameover = myfont.render("GAME OVER!", False, "Red")
        newPipe1 =self.getRandomPipe()
        newPipe2 = self.getRandomPipe()

        upperPipes = [{"x": self.SCREENWIDTH+200, "y": newPipe1[0]["y"]},
                    {"x": self.SCREENWIDTH+200+(self.SCREENWIDTH/2), "y": newPipe2[0]["y"]},
                    ]
        lowerPipes = [{"x": self.SCREENWIDTH+200, "y": newPipe1[1]["y"]},
                    {"x": self.SCREENWIDTH+200+(self.SCREENWIDTH/2), "y": newPipe2[1]["y"]},
                    ]
        pipVelX = -4
        playerVelY = -8
        playerMaxVelY = 10
        playerAccY = 1
        playerFlapacc = -8
        playerFlapped = False
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if player_y > 0:
                        playerVelY = playerFlapacc
                        playerFlapped = True
                        GAME_SOUNDS["wing"].play()

            crashTest = self.isCollide(player_x, player_y, upperPipes, lowerPipes)
            if crashTest:
                if ALIVE>1:
                    ALIVE-=1
                    return self.mainGame()
                else:
                    ALIVE+=2
                    self.SCREEN.blit(Gameover,(80,210))
                    pygame.display.update()
                    FPSCLOCK.tick(self.FPS)
                    return 
            playerMidPos = player_x+GAME_SPRITES['player'].get_width()/2

            for pipe in upperPipes:
                pipMidPos = pipe["x"]+GAME_SPRITES["pipe"][0].get_width()/2
                if pipMidPos <= playerMidPos <pipMidPos+4:
                    score += 1
                    GAME_SOUNDS["point"].play()
                    Score_meter = myfont.render(f"Score:{score}", False, self.fontcolor)
                    print(f"your point is {score} ")
            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY
            if playerFlapped:
                playerFlapped = False
            playerHeight = GAME_SPRITES["player"].get_height()
            player_y = player_y+min(playerVelY, self.basey-player_y-playerHeight)

            for upperpipe, lowerPipe in zip(upperPipes, lowerPipes):
                upperpipe["x"] += pipVelX
                lowerPipe["x"] += pipVelX

            if 0<upperPipes[0]["x"] <5:
                newpipe=self.getRandomPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])
            if upperPipes[0]["x"]< -GAME_SPRITES["pipe"][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)
            
            self.SCREEN.blit(GAME_SPRITES["background"], (0, 0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                self.SCREEN.blit(GAME_SPRITES["pipe"][0], (upperPipe["x"], upperPipe["y"]))
                self.SCREEN.blit(GAME_SPRITES["pipe"][1], (lowerPipe["x"], lowerPipe["y"]))
            self.SCREEN.blit(Alive_meter,(0,0))
            self.SCREEN.blit(Score_meter,(200,0))
            self.SCREEN.blit(GAME_SPRITES["base"], (self.basex, self.basey))
            self.SCREEN.blit(GAME_SPRITES["player"], (player_x, player_y))
            pygame.display.update()
            FPSCLOCK.tick(self.FPS)


    def isCollide(self,playerx, playery, upperPipes, lowerPipes):
        if playery> 370  or playery<0:
            GAME_SOUNDS['hit'].play()
            return True
        
        for pipe in upperPipes:
            pipeHeight = GAME_SPRITES['pipe'][0].get_height()
            if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
                GAME_SOUNDS['hit'].play()
                return True

        for pipe in lowerPipes:
            if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
                GAME_SOUNDS['hit'].play()
                return True

        return False
    def getRandomPipe(self):
        pipeHeight = GAME_SPRITES["pipe"][0].get_height()
        offset = int(self.SCREENHEIGHT/4)
        y2 = random.randrange(
            offset, int(self.SCREENHEIGHT-GAME_SPRITES["base"].get_height()-1.2*offset))
        pipex = self.SCREENWIDTH+15
        y1 = pipeHeight-y2+offset
        pipe = [{"x": pipex, "y": -y1},
                {"x": pipex, "y": y2}
                ]
        return pipe


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.font.init() 
    myfont = pygame.font.SysFont('Times', 20,"bold")
    pygame.display.set_caption("Flappy bird by VJ")
    bird = flappyBird()
    while True:
        bird.welcomeSCREEN()
        bird.mainGame()
