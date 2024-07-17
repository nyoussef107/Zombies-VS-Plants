
from . import mobile
from .mobile import Mobile
from FSMs import animation, movement


from utils import vec, rectAdd, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


class Zombie(Mobile):
   Zombiecount=4
   powerup = False
   def __init__(self, position):
      super().__init__(position, "zom.png")
        
      

      self.framesPerSecond = 6
      self.nFrames = 6
      
      self.nFramesList = {
         "moving"   : 8,
         "damage1"   : 8,
         "damage2"   : 8,
         "damage3"   : 8,
         "damage4"   : 8,
         "standing" : 6,
          "powered"   : 8
          
      }
      
      self.rowList = {
         "moving"   : 1,
         "damage1"   : 2,
         "damage2"   : 3,
         "damage3"   : 4,
         "damage4"   : 5,
         "standing" : 0,
         "powered"   : 6
      }
      
      self.framesPerSecondList = {
         "moving"   : 8,
         "damage1"   : 8,
         "damage2"   : 8,
         "damage3"   : 8,
         "damage4"   : 8,
         "powered"   : 8,
         "standing" : 8
      }
            
      
      self.hp = 20
      self.attack=5
      self.pow = False

      self.FSManimated = animation.WalkingFSM(self)
      self.LR = movement.AccelerationFSM(self, axis=0)
      self.spawn = True
      self.dead =  True
      self.type = "football"
      
      
   def getRect(self):
        return self.image.get_rect()
      
   def handleEvent(self, event):
         if self.powerup == True:
            Zombie.powerup -=1
            self.pow=True
            self.hp=30
            self.attack=10
   
   def update(self, seconds): 
      if self.frame == 5 and self.spawn==True:
         self.FSManimated.move()
         self.LR.decrease()
         self.spawn=False
      self.LR.update(seconds)
      self.hitBox = rectAdd(self.position, self.getRect())
      super().update(seconds)



  