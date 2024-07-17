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
from utils import vec, RESOLUTION, SCALE
from soundManager2 import *


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


class introEngine(object):

    def __init__(self):

        self.orbs = []
        self.win = False
        self.zom = False
        
        self.zombies = []
        r = [5, 58, 58 * 2, 58 * 3, 58 * 4, 58 * 5]
        c = [80, 80 * 2, 80 * 3, 80 * 4, 80 * 5]

        self.plants = [Plant((r[-1], c[2]), 0, 0, 0, reward=True), Plant((r[-1], c[1]), 0, 0, 0, reward=True)]
        self.SM = SoundManager.getInstance()
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0, 0), "background.png")
        self.dave = Mobile((50, 120), "dave.png")
        self.tankicon = Drawable((5, 5), "std_icon.png")
        self.lanes = [(700, 55), (700, 130), (700, 215), (700, 300)]
        self.zom = False
        self.tankcount = TextEntry((62, 62), str(Zombie.Zombiecount))
        self.tanknum = TextEntry((1, 1), "1")
        self.orb_creation_timer = 0
        
        self.story_text_lines = [
            "We were Always told the zombies were the evil ones....",
            "But they were just peaceful neighbors, until they met their untimely demise at the hands of Dave...",
            "Buried in his yard they were imprisoned underground by the malevolent plants guarding Dave's yard...",
            "With vengeance burning in their hollow eyes, they rise from their graves not as mindless husks...",
            "but as avengers seeking justice against botanical tyranny...",
            "Hold down the zombie number and click on a lane to place a zombie..",
            "Destroy Purple plants to free your zombie friends...",
            "Destroy all plants to win...",
            "Well done !!!"
            
        ]
        self.current_story_line = 0
        self.show_press_enter = True
        self.tutorial = False
        
    def draw(self, drawSurface):
        self.background.draw(drawSurface)
        self.tankicon.draw(drawSurface)
        self.tankcount.draw(drawSurface)
        self.tanknum.draw(drawSurface)
        self.dave.draw(drawSurface)
        [o.draw(drawSurface) for o in self.orbs]
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN  and not self.tutorial:
                self.current_story_line += 1
                if self.current_story_line >= len(self.story_text_lines):
                    self.show_press_enter = False
                if self.current_story_line == 5:
                    self.tutorial=True
                else:
                    self.show_press_enter = True
    

            if event.key == pygame.K_1:
                self.zom = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1:
                self.zom = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.zom and Zombie.Zombiecount > 0:
                mousePosition = vec(*event.pos) // SCALE - vec(32, 34)
                mousePosition = closest_position(mousePosition, self.lanes)
                if self.current_story_line == 5:
                    self.current_story_line += 1
                    self.SM.playSFX("CrazyDave'sGreeting.mp3")
                self.zombies.append(Basic((700, mousePosition[1])))
                Zombie.Zombiecount -= 1
                self.SM.playSFX("groan.mp3")
                
        if len(self.zombies) > 0:
       
            self.dave.flip = True
            self.dave.velocity = vec(-50, 0) 

    def update(self, seconds):
        self.dave.update(seconds)
        [o.update(seconds) for o in self.orbs]
        [o.update(seconds) for o in self.zombies]
        if not self.plants:
            self.win = True

        for plant in self.plants:
            if plant.shooting == 1:
                plant.starting += seconds
                if plant.starting >= 2:
                    plant.starting = 0
                    pos = plant.position.copy()
                    pos[0] += 3
                    self.orbs.append(Orb(position=(pos)))

        self.tankcount = TextEntry((62, 62), str(Zombie.Zombiecount))
        [o.update(seconds) for o in self.orbs]
        [o.update(seconds) for o in self.zombies]

        for orb in self.orbs:
            orb.update(seconds)
            if orb.position[0] > 800:
                self.orbs.remove(orb)

        for j in range(len(self.zombies)):
            for r in range(len(self.orbs)):
                if self.orbs[r].hitBox.colliderect(self.zombies[j].hitBox):
                    self.zombies[j].hp -= 1
                    self.SM.playSFX("splat.mp3")
                    self.orbs.pop(r)
                    break

        zombieInRange = False

        r = None
        for j in range(len(self.zombies)):
            for r in range(len(self.plants)):
                if self.plants[r].attackRange.colliderect(self.zombies[j].hitBox):
                    self.plants[r].shooting = 1
                    zombieInRange = True
                    break
            else:
                if r is not None:
                    self.plants[r].shooting = 0

        if not zombieInRange:
            for plant in self.plants:
                plant.shooting = 0

        for j in range(len(self.zombies)):
            if self.zombies[j].hp <= 0:
                self.zombies.pop(j)
                break

        for j in range(len(self.plants)):
            if self.plants[j].hp <= 0:
                if self.plants[j].reward:
                    Zombie.Zombiecount += 1
                self.plants.pop(j)
              
                self.current_story_line += 1
                break

        for r in range(len(self.plants)):
            for j in range(len(self.zombies)):
                if self.plants[r].hitBox.colliderect(self.zombies[j].hitBox) :
                    self.plants[r].hp -= self.zombies[j].attack
                    self.zombies[j].LR.stop_all()
                    if (seconds*1000)%3==0:
                        self.SM.playSFX("bigchomp.mp3")
                    if self.zombies[j].FSManimated == "moving":
                        self.zombies[j].FSManimated.eat()
                        break
                elif self.zombies[j].LR.current_state.id == "not_moving" and self.zombies[j].spawn is not True and self.zombies[j].FSManimated == "eating":
                    self.zombies[j].LR.decrease()
                    self.zombies[j].FSManimated.move()
                    
