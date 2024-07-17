
from . import mobile
from .mobile import Mobile
from .drawable import Drawable
from FSMs import animation, movement
from pygame import transform


from utils import vec, rectAdd, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


def changColor(image, color):
      colouredImage = pygame.Surface(image.get_size())
      colouredImage.fill(color)
      
      finalImage = image.copy()
      finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
      return finalImage

class Laser(Drawable):
   def __init__(self, position, shooting, timer, starting,reward=False):
      position = (position[0], position[1] - 4.5)
      super().__init__(position, "lazer.png")

      self.type = 'laser'
      self.hp=500
      self.shooting = shooting
      self.timer = timer
      self.starting = starting
      self.reward=reward

      scale_factor = 0.1
      original_image = self.image.copy()  
      scaled_width = int(original_image.get_width() * scale_factor)
      scaled_height = int(original_image.get_height() * scale_factor)
      self.image = transform.smoothscale(original_image, (scaled_width, scaled_height))
      self.hitBox = rectAdd(self.position, self.getRect())
  
      self.attackRange = pygame.Rect(self.position[0], self.position[1], 500, 50) 
      
      self.dead =  False
      
   def getRect(self):
        return self.image.get_rect()
   
   def draw(self, drawSurface):
      if self.reward:
         color_image = changColor(self.image, (255,0,255))
         drawSurface.blit(color_image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
      else:
          drawSurface.blit(self.image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
     
     
   def update(self, seconds): 
      self.hitBox = rectAdd(self.position, self.getRect())
      super().update(seconds)

   def draw_attack_range(self, screen):
      pygame.draw.rect(screen, (255, 0, 0), self.attackRange, 2) 
