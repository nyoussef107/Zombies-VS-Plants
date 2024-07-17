from FSMs import ScreenManagerFSM
from . import TextEntry, EventMenu
from utils import vec, RESOLUTION
from gameObjects import engine
from gameObjects import intro
from gameObjects import level1
from gameObjects import l2 , l3 , l4 ,l5


from soundManager2 import *
from pygame.locals import *

class ScreenManager(object):
      
    def __init__(self):
        self.game =  engine.GameEngine()
        
        self.intro =  intro.introEngine()
        
        self.level1 =  level1.lvl1Engine()
        
        self.level2 =  l2.lvl2Engine()
        
        self.level3 =  l3.lvl3Engine()
        
        self.level4 =  l4.lvl4Engine()
        
        self.level5 =  l5.lvl5Engine()
        
        self.curent=0
        
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),"Paused")
        self.SM = SoundManager.getInstance()
        size = self.pausedText.getSize()
        midpoint = RESOLUTION // 2 - size
        self.pausedText.position = vec(*midpoint)
        
        self.mainMenu = EventMenu("menu.png", fontName="default8")
        
        self.mainMenu.addOption("start", "Press 1 to start Game",
                                 RESOLUTION // 2 - vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_1,
                                 center="both")
        self.mainMenu.addOption("exit", "Press 2 to exit Game",
                                 RESOLUTION // 2 + vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_2,
                                 center="both")
        
        
        
        self.lvl1menu=EventMenu("background.png", fontName="default8")
        
        self.lvl1menu.addOption("next", "Press 1 to go to next level",
                                 RESOLUTION // 2 - vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_1,
                                 center="both")
        
        self.lvl1menu.addOption("exit", "Press 2 to exit Game",
                                 RESOLUTION // 2 + vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_2,
                                 center="both")
        
        self.losemenu=EventMenu("background.png", fontName="default8")
        
        self.losemenu.addOption("next", "Press 1 retry level",
                                 RESOLUTION // 2 - vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_1,
                                 center="both")
        
        self.losemenu.addOption("exit", "Press 2 to exit Game",
                                 RESOLUTION // 2 + vec(0,50),
                                 lambda x: x.type == KEYDOWN and x.key == K_2,
                                 center="both")
        
        self.mus =1
        
  
    def draw(self, drawSurf):
        if self.state.isInGame():
            self.game.draw(drawSurf)
        
            if self.state == "paused":
                self.pausedText.draw(drawSurf)
                
        if self.state == "intro":
            self.intro.draw(drawSurf)
            
        if self.state == "level1":
            self.level1.draw(drawSurf)
            
        if self.state == "level2":
            self.level2.draw(drawSurf)
            
        if self.state == "level3":
            self.level3.draw(drawSurf)
            
        if self.state == "level4":
            self.level4.draw(drawSurf)
        
        if self.state == "level5":
            self.level5.draw(drawSurf)
            
        if self.state == "lvlmenu":
            self.lvl1menu.draw(drawSurf)
            
            
        if self.state == "losemenu":
            self.losemenu.draw(drawSurf)
        
        
        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
        
   
    
    def handleEvent(self, event):
    
        if self.state in ["game", "paused"]:
      
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
            else:
                self.game.handleEvent(event)
                
        if self.state ==  "intro":
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
            else:
                self.intro.handleEvent(event)
        
        if self.state ==  "level1":
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
            else:
                self.level1.handleEvent(event)
                
        if self.state ==  "level2":
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
            else:
                self.level2.handleEvent(event)
                
        if self.state ==  "level3":
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
            else:
                self.level3.handleEvent(event)
                
                
        if self.state ==  "level4":
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
            else:
                self.level4.handleEvent(event)
                
        if self.state ==  "level5":
            if event.type == KEYDOWN and event.key == K_m:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
            else:
                self.level5.handleEvent(event)
                
        if self.state == "lvlmenu":
            choice2 = self.lvl1menu.handleEvent(event)
            if choice2 == "next":
                if self.curent==1:
                    self.state.next()
                    self.SM.playBGM("Loonboon.mp3")
                if self.curent==2:
                    self.state.next2()
                    self.SM.playBGM("UltimateBattle.mp3")
                if self.curent==3:
                    self.state.next3()
                    self.SM.playBGM("Zombotany.mp3")
                if self.curent==4:
                    self.state.next4()
                    self.SM.playBGM("Loonboon.mp3")
                if self.curent==5:
                    self.state.next5()
                    self.SM.playBGM("ZombiesonYourLawn.mp3")
            elif choice2 == "exit":
                return "exit"
            
        elif self.state == "losemenu":
            choice2 = self.losemenu.handleEvent(event)
          
            if choice2 == "next":
                if self.curent==1:
                    self.level1 =  level1.lvl1Engine()
                    self.state.next()
                    self.SM.playBGM("Loonboon.mp3")
                if self.curent==2:
                    self.level2 =  l2.lvl2Engine()
                    self.state.next2()
                    self.SM.playBGM("UltimateBattle.mp3")
                if self.curent==3:
                    self.level3 =  l3.lvl3Engine()
                    self.state.next3()
                    self.SM.playBGM("Zombotany.mp3")
                if self.curent==4:
                    self.level4 =  l4.lvl4Engine()
                    self.state.next4()
                    self.SM.playBGM("Loonboon.mp3")
                if self.curent==5:
                    self.level5 =  l5.lvl5Engine()
                    self.state.next5()
                    self.SM.playBGM("UltimateBattle.mp3")
            elif choice2 == "exit":
                return "exit"
                
        elif self.state == "mainMenu":
            if self.mus:
                self.SM.playBGM("CrazyDave.mp3")
            self.mus=0
            choice = self.mainMenu.handleEvent(event)
            if choice == "start":
                self.state.startGame()
                self.SM.playBGM("GrazetheRoof.mp3")
            elif choice == "exit":
                return "exit"
     
    
    def update(self, seconds):      
        if self.state == "game":
            self.game.update(seconds)
            
        if self.state == "intro":
            self.intro.update(seconds)
            if len(self.intro.plants) == 0:
                self.state.end()
                self.curent+=1
                self.SM.playBGM("CrazyDave.mp3")
                
        if self.state == "level1":
            self.level1.update(seconds)
            if len(self.level1.plants) == 0:
                self.state.end()
                self.curent+=1
                self.SM.playBGM("CrazyDave.mp3")
            elif self.level1.lose == True and  len(self.level1.plants) != 0:
                self.state.lost()
                self.SM.playBGM("CrazyDave.mp3")
                
        if self.state == "level2":
            self.level2.update(seconds)
            if len(self.level2.plants) == 0:
                self.state.end()
                self.curent+=1
                self.SM.playBGM("CrazyDave.mp3")
            elif self.level2.lose == True and len(self.level2.plants) != 0:
                self.state.lost()
                self.SM.playBGM("CrazyDave.mp3")
                
                
        if self.state == "level3":
            self.level3.update(seconds)
            if len(self.level3.plants) == 0:
                self.state.end()
                self.curent+=1
                self.SM.playBGM("CrazyDave.mp3")
            elif self.level3.lose == True and len(self.level3.plants) != 0:
                self.state.lost()
                self.SM.playBGM("CrazyDave.mp3")
                
                
        if self.state == "level4":
            self.level4.update(seconds)
            if len(self.level4.plants) == 0:
                self.state.end()
                self.curent+=1
                self.SM.playBGM("CrazyDave.mp3")
            elif self.level4.lose == True and len(self.level4.plants) != 0:
                self.state.lost()
                self.SM.playBGM("CrazyDave.mp3")
                
                
        if self.state == "level5":
            self.level5.update(seconds)
            if len(self.level5.plants) == 0:
           
                self.SM.playBGM("ZombiesonYourLawn.mp3")
            elif self.level5.lose == True and len(self.level5.plants) != 0:
                self.state.lost()
                self.SM.playBGM("CrazyDave.mp3")
                
                
        elif self.state == "losemenu":
            self.losemenu.update(seconds)        
                
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)
            
        elif self.state == "lvlmenu":
            self.lvl1menu.update(seconds)