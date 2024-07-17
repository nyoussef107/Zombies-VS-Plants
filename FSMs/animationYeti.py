from . import AbstractGameFSM
from utils import magnitude, EPSILON, SpriteManager
from pygame import transform
from statemachine import State

class AnimateFSM(AbstractGameFSM):
    """For anything that animates. Adds behavior on
       transitioning into a state to change animation."""
    def on_enter_state(self):
        
        state = self.current_state.id
        if self.obj.row != self.obj.rowList[state]:
            self.obj.nFrames = self.obj.nFramesList[state]
            self.obj.frame = 0
            self.obj.row = self.obj.rowList[state]
            self.obj.framesPerSecond = self.obj.framesPerSecondList[state]
            self.obj.animationTimer = 0
            self.obj.image = SpriteManager.getInstance().getSprite(self.obj.imageName,
                                                                   (self.obj.frame, self.obj.row))
        
class WalkingFSM(AnimateFSM):
    """Two-state FSM for walking / stopping in
       a top-down environment."""
       
    standing = State(initial=True)
    moving   = State()
    powered= State()
    eating = State()
    shield= State()
  

    move = standing.to(moving)  | eating.to(moving)
    stop = moving.to(standing)
    power = moving.to(powered) 
    eat = standing.to(eating)  | moving.to(eating) 
    shell = powered.to(shield)

    
    def updateState(self):
        if self.obj.pow==True and self != "standing" and self != "powered" and self != "shield":
            self.power()
            
        if self.hasVelocity() and self == "standing":
            self.move()

    def hasVelocity(self):
        return magnitude(self.obj.velocity) > EPSILON
    
    def noVelocity(self):
        return not self.hasVelocity()