from pygame.locals import *
import pygame
import sys
import random


class flappyBird:
    def __init__(self):
        self.FPS = 32
        self.SCREENWIDHT = 289
        self.SCREENHEIGHT = 511
        self.SCREEN = pygame.display.set_mode(
            (self.SCREENWIDHT, self.SCREENHEIGHT))
        self.GAMESPIRIT = {}
        self.GAMESOUND = {}
        self.basex = 0
        self.basey = int(self.SCREENHEIGHT*0.8)
        self.PIPE="gallery/sprites/pipe.png"
        self.GAMESPIRIT["background"] = pygame.image.load(
            "gallery/sprites/background.png").convert()
        self.GAMESPIRIT["message"] = pygame.image.load(
            "gallery/sprites/message.png").convert_alpha()
        self.GAMESPIRIT["bird"] = pygame.image.load(
            "gallery/sprites/bird.png").convert_alpha()
        self.GAMESPIRIT["base"] = pygame.image.load(
            "gallery/sprites/base.png").convert_alpha()
        self.GAMESPIRIT["pipe"] = (pygame.transform.rotate(pygame.image.load(self.PIPE).convert_alpha(), 180),
                            pygame.image.load(self.PIPE).convert_alpha())
        self.GAMESOUND["hit"] = pygame.mixer.Sound("gallery/audio/hit.wav")
        self.GAMESOUND["point"] = pygame.mixer.Sound("gallery/audio/point.wav")
        self.GAMESOUND["wing"] = pygame.mixer.Sound("gallery/audio/wing.wav")
        self.GAMESOUND["swoosh"] = pygame.mixer.Sound(
            "gallery/audio/swoosh.wav")
        self.GAMESOUND["die"] = pygame.mixer.Sound("gallery/audio/die.wav")

    def welcomeScreen(self):
        playerx = int(self.SCREENWIDHT/5)
        playery = int((self.SCREENHEIGHT - self.GAMESPIRIT['bird'].get_height())/2)
        messagex = int((self.SCREENWIDHT - self.GAMESPIRIT['message'].get_width())/2)
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
                    self.SCREEN.blit(self.GAMESPIRIT['background'], (0, 0))    
                    self.SCREEN.blit(self.GAMESPIRIT["bird"], (playerx, playery))    
                    self.SCREEN.blit(self.GAMESPIRIT['message'], (messagex,messagey ))    
                    self.SCREEN.blit(self.GAMESPIRIT['base'], (self.basex, self.basey))    
                    pygame.display.update()
                    FPSCLOCK.tick(self.FPS)

    def mainGame(self):
        score = 0
        player_x = int(self.SCREENWIDHT/5)
        player_y = int(self.SCREENHEIGHT/2)
        newPipe1 = self.getRandomPipe()
        newPipe2 = self.getRandomPipe()

        upperPipes = [{"x": self.SCREENWIDHT+200, "y": newPipe1[0]["y"]},
                    {"x": self.SCREENWIDHT+200+(self.SCREENWIDHT/2), "y": newPipe2[0]["y"]},
                    ]
        lowerPipes = [{"x": self.SCREENWIDHT+200, "y": newPipe1[1]["y"]},
                    {"x": self.SCREENWIDHT+200+(self.SCREENWIDHT/2), "y": newPipe2[1]["y"]},
                    ]
        pipVelX = -4
        playerVelY = -8
        playerMaxVelY = 10
        playerAccY = 1
        playerFlapped = False
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if player_y > 0:
                        playerVelY = -8
                        playerFlapped = True
                        self.GAMESOUND["wing"].play()

            crashTest = self.isCollide(player_x, player_y, upperPipes, lowerPipes)
            if crashTest:
                return self.mainGame()
            playerMidPos = player_x+self.GAMESPIRIT["bird"].get_width()/2
            for pipe in upperPipes:
                pipMidPos = pipe["x"]+self.GAMESPIRIT["pipe"][0].get_width()/2
                if pipMidPos <= playerMidPos <pipMidPos+4:
                    score += 1
                    self.GAMESOUND["point"].play()
                    print(f"your point is {score} ")
            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY
            if playerFlapped:
                playerFlapped = False
            playerHeight = self.GAMESPIRIT["bird"].get_height()
            player_y = player_y+min(playerVelY, self.basey-player_y-playerHeight)

            for upperpipe, lowerPipe in zip(upperPipes, lowerPipes):
                upperpipe["x"] += pipVelX
                lowerPipe["x"] += pipVelX



            self.SCREEN.blit(self.GAMESPIRIT["background"],(0,0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                self.SCREEN.blit(self.GAMESPIRIT["pipe"][0], (upperPipe["x"], upperPipe["y"]))
                self.SCREEN.blit(self.GAMESPIRIT["pipe"][1], (lowerPipe["x"], lowerPipe["y"]))
            self.SCREEN.blit(self.GAMESPIRIT["background"],(0,0))
            self.SCREEN.blit(self.GAMESPIRIT["bird"],(player_x,player_y))
            self.SCREEN.blit(self.GAMESPIRIT["base"],(self.basex,self.basey))
            pygame.display.update()
            FPSCLOCK.tick(self.FPS)

    def isCollide(self,playerx, playery, upperPipes, lowerPipes):
        if playery> self.basey - 25  or playery<0:
            self.GAMESOUND['hit'].play()
            return True
        
        for pipe in upperPipes:
            pipeHeight = self.GAMESPIRIT['pipe'][0].get_height()
            if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < self.GAMESPIRIT['pipe'][0].get_width()):
                self.GAMESOUND['hit'].play()
                return True

        for pipe in lowerPipes:
            if (playery + self.GAMESPIRIT['bird'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < self.GAMESPIRIT['pipe'][0].get_width():
                self.GAMESOUND['hit'].play()
                return True

        return False
    def getRandomPipe(self):
        pipeHeight = self.GAMESPIRIT["pipe"][0].get_height()
        offset = int(self.SCREENHEIGHT/4)+random.randint(0,5)
        y2 = random.randrange(
            offset, int(self.SCREENHEIGHT-self.GAMESPIRIT["base"].get_height()-1.2*offset))
        pipex = self.SCREENWIDHT+15
        y1 = pipeHeight-y2+offset
        pipe = [{"x": pipex, "y": -y1},
                {"x": pipex, "y": y2}
                ]
        return pipe


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy bird by VJ")
    bird = flappyBird()
    while True:
        bird.welcomeScreen()
        bird.mainGame()
