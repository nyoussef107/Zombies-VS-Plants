
from . import mobile
from .mobile import Mobile
from .drawable import Drawable
from FSMs import animation, movement
from pygame import transform
import random


from utils import vec, rectAdd, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np
import time




class Powerup(Drawable):
   def __init__(self, position):
      super().__init__(position, "brainy.png")

   
      scale_factor = 0.05
      original_image = self.image.copy()  
      scaled_width = int(original_image.get_width() * scale_factor)
      scaled_height = int(original_image.get_height() * scale_factor)
      self.image = transform.smoothscale(original_image, (scaled_width, scaled_height))
      self.hitBox = rectAdd(self.position, self.getRect())
       
      self.toggle_delete = 0
      self.creation = time.time()
      self.delete = 0  
      self.create = 0
      self.appear = random.randrange(1, 30)
      
   def getRect(self):
        return self.image.get_rect()
   
   def draw(self, drawSurface):
         drawSurface.blit(self.image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
     
   def update(self, seconds): 
      self.hitBox = rectAdd(self.position, self.getRect())
      
      super().update(seconds)
      
      if self.toggle_delete == 1:
         current = time.time()
         if (current - self.creation) >= 5:
            self.delete = 1
            
      current = time.time()
      if (current - self.creation) >= self.appear:
     
         self.create = 1
         self.creation = time.time()
         self.toggle_delete = 1

      
   def draw_hitbox(self, screen):
      pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)