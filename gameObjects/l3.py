import pygame
import math
from . import Drawable, kirby, mobile
from .mobile import Mobile
from .kirby import Kirby
from .zombie import Zombie
from .yeti import Yeti
from .basic import Basic

from UI import TextEntry
from .orb import Orb
from .plant import Plant
from .laser import Laser
from .potatomine import Potatomine
from .beam import Beam
from .powerup import Powerup
from utils import vec, RESOLUTION, SCALE
from soundManager2 import *
import random




def closest_position(mouse_click, position_list):
    distances = [math.sqrt((mouse_click[0] - pos[0]) ** 2 + (mouse_click[1] - pos[1]) ** 2) for pos in position_list]
    min_distance_index = distances.index(min(distances))
    return position_list[min_distance_index]


class TimerStatic(object):
    def __init__(self, setTo):
        self.time = 0
        self.setTo = setTo
        self.reset()

    def reset(self):
        self.time = self.setTo

    def done(self):
        return self.time <= 0

    def update(self, seconds):
        self.time -= seconds


class lvl3Engine(object):
    

    def __init__(self):
        
        self.powerupcount = 0
        
        self.lose = False

        self.ycount= 0
        self.footballcount=7
        self.basicount=0
        self.powerups = [Powerup((random.randrange(60, 600), random.randrange(60, 300))), Powerup((random.randrange(60, 600), random.randrange(60, 300))), Powerup((random.randrange(60, 600), random.randrange(60, 300)))]
        self.orbs = []
        self.win = False
        self.zom = False
        self.yet = False
        self.regular = False
        self.zombies = []
        r = [5, 58, 58 * 2, 58 * 3, 58 * 4, 58 * 5, 58 * 6]
        c = [80, 80 * 2, 80 * 3, 80 * 4, 80 * 5]

        self.plants = [Plant((r[0], c[0]), 0, 0, 0, reward= True), Plant((r[1], c[0]), 0, 0, 0, reward= True), Plant((r[2], c[0]), 0, 0, 0, reward= True),
                       Plant((r[0], c[1]), 0, 0, 0), Potatomine((r[1], c[1]), 0, 0, 0), Plant((r[2], c[1]), 0, 0, 0), Potatomine((r[3], c[1]), 0, 0, 0),
                       Plant((r[0], c[2]), 0, 0, 0), Potatomine((r[1], c[2]), 0, 0, 0), Potatomine((r[2], c[2]), 0, 0, 0), Potatomine((r[3], c[2]), 0, 0, 0),
                       Plant((r[0], c[3]), 0, 0, 0, reward= True)]
        
        self.SM = SoundManager.getInstance()
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0, 0), "background.png")
        
        self.tankicon = Drawable((80, 5), "ticon.png")
        self.normalzicon = Drawable((5, 5), "std_icon.png")
        

        self.zombiesum = self.footballcount+ self.ycount+self.basicount+len(self.zombies)
      
        self.lanes = [(700, 55), (700, 130), (700, 215), (700, 300)]
        self.zom = False
        self.poweractive = False
        

        
        self.normalzcount = TextEntry((62, 62), str(self.basicount))
        self.normalznum = TextEntry((1,1), "1")
        
        self.tankcount = TextEntry((80 + 62, 62), str(self.footballcount))
        self.tanknum = TextEntry((80, 1), "2")
        
        self.powericon = Drawable((600, 10), "BrainyScaled.png")
        self.powerdesplay = TextEntry((650, 50), str(self.powerupcount))
        
        self.orb_creation_timer = 0
        self.story_text_lines = [
            "Poweups will appear as Brains. Click on them to collect them before they disappear",
            "Press W and click on a special zombie to activate",            
        ]
        
        self.current_story_line = 0
        self.show_press_enter = True
        self.tutorial = False

    def draw(self, drawSurface):
        self.background.draw(drawSurface)
        
        self.tankicon.draw(drawSurface)
        self.normalzicon.draw(drawSurface)

        self.tankcount.draw(drawSurface)
        self.tanknum.draw(drawSurface)
        
        self.normalzcount.draw(drawSurface)
        self.normalznum.draw(drawSurface)

        self.powerdesplay.draw(drawSurface)
        self.powericon.draw(drawSurface)

        [o.draw(drawSurface) for o in self.orbs]
                

        
        for o in self.powerups:
            if o.create == 1 and o.delete != 1:
              
                o.draw(drawSurface)   
  
                
        [o.draw(drawSurface) for o in self.zombies]
        [o.draw(drawSurface) for o in self.plants]
        
   

        if self.win:
            font = pygame.font.SysFont(None, 48)
            text = font.render("You win!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(RESOLUTION[0] // 2, RESOLUTION[1] // 2))
            drawSurface.blit(text, text_rect)

        if self.show_press_enter and not self.tutorial:
            font = pygame.font.SysFont(None, 18)
            press_enter_text = font.render("Press Enter to continue", True, (255, 255, 255))
            text_rect = press_enter_text.get_rect(center=(RESOLUTION[0] // 2, RESOLUTION[1] - 20))
            drawSurface.blit(press_enter_text, text_rect)
            
        if len(self.story_text_lines) > self.current_story_line:
            font = pygame.font.SysFont(None, 24)
            text = font.render(self.story_text_lines[self.current_story_line], True, (255, 255, 255))
            text_rect = text.get_rect(center=(RESOLUTION[0] // 2, RESOLUTION[1] // 4))
            drawSurface.blit(text, text_rect)

    def handleEvent(self, event):
        
        [o.handleEvent(event) for o in self.zombies]
        [o.handleEvent(event) for o in self.plants]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not self.tutorial:
                self.current_story_line += 1
                if self.current_story_line >= len(self.story_text_lines):
                    self.show_press_enter = False
                if self.current_story_line == 2:
                    self.tutorial=True
                else:
                    self.show_press_enter = True
    

            if event.key == pygame.K_1:
                self.regular = True
            if event.key == pygame.K_2:
                self.zom = True
            if event.key == pygame.K_3:
                self.yet = True
            
            if event.key == pygame.K_w:
                self.poweractive = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                self.regular = False
            if event.key == pygame.K_2:
                self.zom = False
            if event.key == pygame.K_3:
                self.yet = False
                
            if event.key == pygame.K_w:
                self.poweractive = False

                
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.zom and self.footballcount > 0:
                mousePosition = vec(*event.pos) // SCALE - vec(32, 34)
                mousePosition = closest_position(mousePosition, self.lanes)
                self.zombies.append(Zombie((700, mousePosition[1])))
                self.footballcount -= 1
                self.SM.playSFX("groan.mp3")

            if self.regular and self.basicount > 0:
                mousePosition = vec(*event.pos) // SCALE - vec(32, 34)
                mousePosition = closest_position(mousePosition, self.lanes)
                self.zombies.append(Basic((700, mousePosition[1])))
                self.basicount -= 1
                self.SM.playSFX("groan.mp3")

            if self.poweractive and self.powerupcount > 0:
                mousePosition = vec(*event.pos) // SCALE 
                for z in self.zombies:
                    if z.hitBox.colliderect(pygame.Rect(mousePosition[0], mousePosition[1], 3, 3)):
                        z.powerup = True
                        self.powerupcount -= 1
                        self.powerdesplay = TextEntry((650, 50), str(self.powerupcount))


            
            [o.handleEvent(event) for o in self.zombies]
                        
                        
        
            
            mousePosition = vec(*event.pos) // SCALE 
           
            for power in self.powerups:
                if power.create == 1 and power.delete != 1:
                    if power.hitBox.colliderect(pygame.Rect(mousePosition[0], mousePosition[1], 3, 3)):
                        self.powerupcount +=1
                        self.powerdesplay = TextEntry((650, 50), str(self.powerupcount))
                        power.delete = 1

            

    def update(self, seconds):
        
 
        
        
        [o.update(seconds) for o in self.powerups]
        [o.update(seconds) for o in self.plants]
        [o.update(seconds) for o in self.orbs]
        [o.update(seconds) for o in self.zombies]

        

        
        if not self.plants:
            self.win = True

        for plant in self.plants:
            if plant.type == 'pea':
                if plant.shooting == 1:
                    plant.starting += seconds
                    if plant.starting >= 1.5:
                        plant.starting = 0
                        pos = plant.position.copy()
                        pos[0] += 3
                        self.orbs.append(Orb(position=(pos)))
            
            if plant.type == 'laser':
                if plant.shooting == 1:
                    plant.starting += seconds
                    if plant.starting >= 1.5:
                        plant.starting = 0
                        pos = plant.position.copy()
                  
                        self.orbs.append(Beam(position=(pos)))


        
        self.normalzcount = TextEntry((62, 62), str(self.basicount))
        self.tankcount = TextEntry((80 + 62, 62), str(self.footballcount))
        self.yeticount = TextEntry((150 +62, 62), str(self.ycount))
                
        [o.update(seconds) for o in self.orbs]
        [o.update(seconds) for o in self.zombies]

        for orb in self.orbs:
            orb.update(seconds)
            if orb.position[0] > 800:
                self.orbs.remove(orb)
            if orb.type == 'laser' and orb.delete == 1:
                self.orbs.remove(orb)
                
        for j in range(len(self.zombies)):
            for r in range(len(self.orbs)):
                if self.orbs[r].type == 'peas':
                        if self.orbs[r].hitBox.colliderect(self.zombies[j].hitBox):
                            self.orbs.pop(r)
                            self.SM.playSFX("splat.mp3")
                            self.zombies[j].hp -= 1
                            break

                elif self.orbs[r].type == 'laser':
                    for j in range(len(self.zombies)):
                        if self.orbs[r].hitBox.colliderect(self.zombies[j].hitBox):
                            if self.orbs[r].not_used == 0:
                                self.zombies[j].hp -= 1
                                self.SM.playSFX("laser.mp3")
                                break
                    self.orbs[r].not_used = 1

         
        
        for j in range(len(self.zombies)):
            for r in range(len(self.plants)):
                if self.plants[r].type == 'potatomine':
            
                    if self.plants[r].hitBox.colliderect(self.zombies[j].hitBox) and self.plants[r].FSManimated != "powered":
                        self.zombies[j].hp -= 100
                        self.SM.playSFX("explosion.mp3")
                        self.plants[r].FSManimated.boom()
                        break

        def find_closest_lane(lane, lanes):
            closest_lane = min(lanes, key=lambda x: abs(x - lane))
            return closest_lane
        
        lanes = [80, 80 * 2, 80 * 3, 80 * 4]
        zombieInlane = [False, False, False, False]
        
        

        r = None
        for j in range(len(self.zombies)):
            for r in range(len(self.plants)):
                if self.plants[r].type == 'pea' or self.plants[r].type == 'laser':
                    if self.plants[r].attackRange.colliderect(self.zombies[j].hitBox):
                        self.plants[r].shooting = 1
                        plnt = self.plants[r]
                        lane= plnt.position[1]
                        inx = lanes.index(find_closest_lane(lane, lanes))
                        zombieInlane[inx] = True


        for i, ele in enumerate(zombieInlane):
            if not ele:
                for plant in self.plants:
                    
                    lane = plant.position[1]
                    inx = lanes.index(find_closest_lane(lane, lanes))
                    if inx == i:
                        plant.shooting = 0

        self.zombiesum = self.footballcount + self.ycount + self.basicount + len(self.zombies)
        if self.zombiesum == 0:
            self.lose = True
      

        for j in range(len(self.zombies)):
         
            if self.zombies[j].hp <= 0 or self.zombies[j].position[0]<0:
                self.zombies.pop(j)
                break

        for j in range(len(self.plants)):
            if self.plants[j].hp <= 0:
                if self.plants[j].reward:
                    self.basicount += 1
                self.plants.pop(j)
                break

        for j in range(len(self.zombies)):
            for r in range(len(self.plants)):
                if self.plants[r].hitBox.colliderect(self.zombies[j].hitBox) and self.zombies[j].FSManimated != "standing":
                    self.plants[r].hp -= self.zombies[j].attack
                    if (seconds*1000)%3==0:
                        self.SM.playSFX("bigchomp.mp3")
                    self.zombies[j].LR.stop_all()
                    break
                elif self.zombies[j].LR.current_state.id == "not_moving" and self.zombies[j].spawn is not True:
                    self.zombies[j].LR.decrease()

