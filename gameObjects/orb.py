
from . import mobile
from .mobile import Mobile
from FSMs import animation, movement


from utils import vec, rectAdd, RESOLUTION
from pygame import transform

from pygame.locals import *

import pygame
import numpy as np


class Orb(Mobile):
    
    
    def __init__(self, position):
    
        super().__init__( position, "orb2.png")
        
        self.type = 'peas'
        self.velocity = vec(0,0)
        self.accel =  vec(20000,0)
   
        self.hitBox = pygame.Rect(0, 0, 50, 50)
            
    def update(self, seconds):


        self.velocity =  self.accel * seconds
        super().update(seconds)
        self.hitBox = rectAdd(self.position, self.getRect())
  
    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)  
