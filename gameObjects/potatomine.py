
from . import mobile
from .mobile import Mobile
from .drawable import Drawable
from FSMs import animationpotato, movement
from pygame import transform

from utils import vec, rectAdd, resizeRect, RESOLUTION

from pygame.locals import *

import pygame
import numpy as np


def changColor(image, color):
      colouredImage = pygame.Surface(image.get_size())
      colouredImage.fill(color)
      
      finalImage = image.copy()
      finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
      return finalImage

class Potatomine(Mobile):
   def __init__(self, position, shooting, timer, starting,reward=False):
      position = (position[0] - 15 , position[1]-20)
      super().__init__(position, "spudow.png")
      
      self.framesPerSecond = 3
      self.nFrames = 1
      
      self.nFramesList = {
         "standing" : 0,
          "powered"   : 3
      }
      
      self.rowList = {
         "standing" : 0,
         "powered"   : 1
      }
      
      self.framesPerSecondList = {
         "powered"   : 3,
         "standing" : 1
      }

      self.type = 'potatomine'
      self.hp=500
      self.shooting = shooting
      self.timer = timer
      self.starting = starting
      self.reward=reward
    
      scale_factor = 0.07
      original_image = self.image.copy() 
      scaled_width = int(original_image.get_width() * scale_factor)
      scaled_height = int(original_image.get_height() * scale_factor)
      self.image = transform.smoothscale(original_image, (scaled_width, scaled_height))
      self.hitBox = rectAdd(self.position, self.getRect())
      image_rect = self.getRect()
      hitbox_width = image_rect.width // 3 
      hitbox_height = image_rect.height // 2  
      hitbox_rect = resizeRect(image_rect, hitbox_width, hitbox_height)
      self.hitBox = rectAdd(self.position, hitbox_rect)
      self.FSManimated = animationpotato.WalkingFSM(self)

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
      if self.frame == 2 and self.FSManimated=="powered":
       
       
         self.dead=True
         self.hp=0
         
   def draw(self, drawSurface):

      return super().draw(drawSurface)
      

   def draw_attack_range(self, screen):
      pygame.draw.rect(screen, (255, 0, 0), self.attackRange, 2) 
