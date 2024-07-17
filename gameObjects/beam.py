
from . import mobile
from .mobile import Mobile
from FSMs import animation, movement


from utils import vec, rectAdd, RESOLUTION
from pygame import transform

from pygame.locals import *

import pygame
import numpy as np
import time


class Beam(Mobile):
    
    
    def __init__(self, position):
        super().__init__( position, "beamy.png")
        

        self.velocity = vec(0,0)

        self.accel =  vec(0,0)
        self.acc = vec(300,300)
        self.hitBox = pygame.Rect(0, 0, 50, 50)
        self.type = 'laser'
        self.not_used = 0
        self.creation = time.time()
        self.delete = 0


    def update(self, seconds):

        current = time.time()
        if (current - self.creation) >= 0.3:
            self.delete = 1
            
        self.velocity =  self.accel * seconds
        super().update(seconds)
        self.hitBox = rectAdd(self.position, self.getRect())
  
    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitBox, 2)  
