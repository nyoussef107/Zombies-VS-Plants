from . import AbstractGameFSM
from statemachine import State
from soundManager2 import *


SM = SoundManager.getInstance()
class ScreenManagerFSM(AbstractGameFSM):
    mainMenu = State(initial=True)
    level2 = State()
    level3 =State()
    level4=State()
    level5=State()
    intro = State()
    game     = State()
    lvlmenu = State()
    level1    = State()    
    paused   = State()
    losemenu = State()

    
    pause = game.to(paused) | paused.to(game) | intro.to(paused) | paused.to(intro) | level1.to(paused) | paused.to(level1) | level2.to(paused) | paused.to(level2) | level3.to(paused) | paused.to(level3) | level4.to(paused) | paused.to(level4) | level5.to(paused) | paused.to(level5) 
    
    startGame = mainMenu.to(intro)
    
    end = intro.to(lvlmenu)|level1.to(lvlmenu)|level2.to(lvlmenu)|level3.to(lvlmenu)|level4.to(lvlmenu)|level5.to(lvlmenu)
    
    next = lvlmenu.to(level1)  | losemenu.to(level1)
    next2 = lvlmenu.to(level2) | losemenu.to(level2)
    next3 = lvlmenu.to(level3) | losemenu.to(level3)
    next4 = lvlmenu.to(level4) | losemenu.to(level4)
    next5 = lvlmenu.to(level5) | losemenu.to(level5) 
    
    lost = level1.to(losemenu)|level2.to(losemenu)|level3.to(losemenu)|level4.to(losemenu)|level5.to(losemenu)
    
    
    
    skip = level1.to(game)
    quitGame  = game.to(mainMenu) | \
                paused.to.itself(internal=True)
                

    def isInGame(self):
        return self == "game" or self == "paused"
    
