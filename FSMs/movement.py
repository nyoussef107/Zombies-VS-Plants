from . import AbstractGameFSM
from utils import vec, magnitude, EPSILON, scale, RESOLUTION

from statemachine import State

class MovementFSM(AbstractGameFSM):
    
    def __init__(self, obj):
        super().__init__(obj)
    
    def update(self, seconds):
        super().update(seconds)
        
        object_size = self.obj.getSize()

        current_pos = self.obj.position

        next_pos = current_pos + self.obj.velocity * seconds

        screen_width, screen_height = RESOLUTION

        


class AccelerationFSM(MovementFSM):
    mul = 1
    """Axis-based acceleration with gradual stopping."""
    not_moving = State(initial=True)
    
    negative = State()
    positive = State()
    
    stalemate = State()
    
    decrease  = not_moving.to(negative) | positive.to(stalemate)
    
    increase = not_moving.to(positive) | negative.to(stalemate)
    
    stop_decrease = negative.to(not_moving) | stalemate.to(positive)
    
    stop_increase = positive.to(not_moving) | stalemate.to(negative)
    
    stop_all      = not_moving.to.itself(internal=True) | negative.to(not_moving) | \
                    positive.to(not_moving) | stalemate.to(not_moving)
    
    def __init__(self, obj, axis=0):
        self.axis      = axis
        self.direction = vec(1,0)

        self.accel = 2000
        
        super().__init__(obj)

    def update(self, seconds=0):
        if self.obj.pow ==True:
            AccelerationFSM.mul = 4
        else:
            AccelerationFSM.mul = 1
        if self == "positive":
            self.obj.velocity = self.direction * self.accel * seconds * AccelerationFSM.mul
        elif self == "negative":
            self.obj.velocity = -self.direction * self.accel * seconds * AccelerationFSM.mul
                
        elif self == "stalemate":
            pass
        else:
            if self.obj.velocity[self.axis] > self.accel * seconds * AccelerationFSM.mul:
                self.obj.velocity[self.axis] -= self.accel * seconds * AccelerationFSM.mul
            elif self.obj.velocity[self.axis] < -self.accel * seconds * AccelerationFSM.mul:
                self.obj.velocity[self.axis] += self.accel * seconds * AccelerationFSM.mul
            else:
                self.obj.velocity[self.axis] = 0
        
        
    
        super().update(seconds)