
from . import mobile
from .mobile import Mobile
from FSMs import animationBASIC, movementBASIC

from utils import vec, rectAdd, resizeRect, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


class Basic(Mobile):
   Zombiecount=4
   powerup = 5
   def __init__(self, position):
      super().__init__(position, "stdzom.png")
        
      
      self.framesPerSecond = 6
      self.nFrames = 6
      
      self.nFramesList = {
         "moving"   : 7,
         "standing" : 6,
         "eating" : 7

      }
      
      self.rowList = {
         "moving"   : 1,
         "standing" : 0,
         "eating" : 2
      }
      
      self.framesPerSecondList = {
         "moving"   : 8,
         "standing" : 8,
         "eating" : 8
      }
            
      self.type = "basic"
      self.hp = 14
      self.attack=5
      self.pow = False
      self.hitBox = rectAdd(self.position, self.getRect())
      self.FSManimated = animationBASIC.WalkingFSM(self)
      self.LR = movementBASIC.AccelerationFSM(self, axis=0)
      self.spawn = True
      self.dead =  True
      
      
   def getRect(self):
        return self.image.get_rect()
      

   
   def update(self, seconds): 
  
      if self.frame == 5 and self.spawn==True:
         self.FSManimated.move()
         self.LR.decrease()
         self.spawn=False
      self.LR.update(seconds)
      self.hitBox = rectAdd(self.position, self.getRect())
      image_rect = self.getRect()
      hitbox_width = image_rect.width // 3 
      hitbox_height = image_rect.height // 2  
      hitbox_rect = resizeRect(image_rect, hitbox_width, hitbox_height)
      self.hitBox = rectAdd(self.position, hitbox_rect)
      super().update(seconds)


   def draw(self, drawSurface):
     
         return super().draw(drawSurface)


  