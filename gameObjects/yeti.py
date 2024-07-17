
from . import mobile
from .mobile import Mobile
from FSMs import animationYeti, movementyeti
from utils import vec, rectAdd,resizeRect, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


class Yeti(Mobile):
   Zombiecount=4
   powerup = False
   def __init__(self, position):
      position = (position[0] , position[1]-20)
      super().__init__(position, "yeti.png")
        
      self.framesPerSecond = 6
      self.nFrames = 6
      
      self.nFramesList = {
         "moving"   : 6,
         "standing" : 6,
         "powered" : 3,
         "shield" : 6,
         "eating": 4
      }
      
      self.rowList = {
         "moving"   : 2,
         "standing" : 0,
         "powered" : 5,
         "shield" : 6,
         "eating": 3

      }
      
      self.framesPerSecondList = {
         "moving"   : 6,
         "standing" : 6,
         "powered" : 6,
         "shield" : 6,
         "eating": 6
      }
            
      self.type = "yeti"
      self.hp = 30
      self.attack=2
      self.pow = False
      self.FSManimated = animationYeti.WalkingFSM(self)
      self.LR = movementyeti.AccelerationFSM(self, axis=0)
      self.spawn = True
      self.dead =  True
      
      
   def getRect(self):
        return self.image.get_rect()
      
   def handleEvent(self, event):
         if self.powerup == True:
            Yeti.powerup -=1
            self.pow=True
            self.hp=115
   
   def update(self, seconds): 
      if self.frame == 5 and self.spawn==True:
         self.FSManimated.move()
         self.LR.decrease()
         self.spawn=False
      
      if self.frame == 2 and self.FSManimated=="powered":
         self.FSManimated.shell()
      
      image_rect = self.getRect()
      hitbox_width = image_rect.width // 3 
      hitbox_height = image_rect.height // 2  
      hitbox_rect = resizeRect(image_rect, hitbox_width, hitbox_height)
      self.hitBox = rectAdd(self.position, hitbox_rect)
      self.LR.update(seconds)
      super().update(seconds)


   def draw(self, drawSurface):
      
      return super().draw(drawSurface)
      

   
  