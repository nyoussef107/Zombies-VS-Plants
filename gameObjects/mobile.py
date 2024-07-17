from gameObjects import animated 
from .animated import Animated
from utils import vec, magnitude, scale

class Mobile(Animated):
    def __init__(self, position, fileName=""):
        super().__init__(position, fileName)
        self.velocity = vec(0,0)

    def update(self, seconds):
        super().update(seconds)
 
        self.position += self.velocity * seconds
        
        
    def getRect(self):
        return self.image.get_rect()