import pygame
import random

from clickTest import *
from field import *
from menu import *

class Unit(pygame.sprite.Sprite):
    def __init__(self, team, name, color, JobPrimary = None, JobSecondary = None):
        pygame.sprite.Sprite.__init__(self)
        #super().__init__(self)
        self.team = team
        self.image = pygame.image.load(color + "_triangle.png")
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.name = name
        # Base stats
        self.base_hp_max       = 100
        self.base_mp_max       = 100
        self.base_bp_max       = 5
        self.base_shield_max   = 3
        self.base_strength     = 10
        self.base_vitality     = 10
        self.base_magic        = 10
        self.base_spirit       = 10
        self.base_move         = 3
        self.base_speed        = 8
        # Primary job stat adjustments
        self.job_stats(JobPrimary, 1)
        self.job_stats(JobSecondary, 2)
        # Current stats
        self.stat_hp = self.base_hp_max
        self.stat_mp = self.base_mp_max
        self.stat_bp = 1
        self.stat_ct = 0
        self.stat_shield = self.base_shield_max
        self.boost_count = 0
        # Weaknesses
        self.weakness = []
        # Action properties
        self.paths = None
        self.moved = False
        self.acted = False
        self.boosted = False

    def job_stats(self, Job = None, degree = 1):
        if Job is not None:
            self.base_hp_max       += int(Job.d_hp_max / degree)
            self.base_mp_max       += int(Job.d_mp_max / degree)
            self.base_bp_max       += int(Job.d_bp_max / degree)
            self.base_shield_max   += int(Job.d_shield_max / degree)
            self.base_strength     += int(Job.d_strength / degree)
            self.base_vitality     += int(Job.d_vitality / degree)
            self.base_magic        += int(Job.d_magic / degree)
            self.base_spirit       += int(Job.d_spirit / degree)
            self.base_move         += int(Job.d_move / degree)
            self.base_speed        += int(Job.d_speed / degree)

    def move_delta(self, dx, dy, Map):
        self.x = min(max(Map.xrange[0], self.x + dx), Map.xrange[1])
        self.y = min(max(Map.yrange[0], self.y + dy), Map.yrange[1])

    def move_exact(self, x, y, Map):
        if self.path_ends:
            if (x, y) in self.path_ends:
                self.x = x
                self.y = y

    def get_paths(self, Units, Map):
        ally_locs = []
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        self.paths = [[[]]] * (self.base_move + self.boost_count + 1)
        self.paths[0] = [[(self.x, self.y)]]

        for i in range(self.base_move + self.boost_count):
            tmp = []
            for d in directions:
                for p in self.paths[i]:
                    tmp_add = tuple(map(sum, zip(p[-1], d)))
                    add_flag = True
                    if tmp_add in [t[-1] for t in tmp]:
                        add_flag = False

                    if tmp_add not in Map.grid:
                        add_flag = False

                    for u in Units:
                        if tmp_add == (u.x, u.y):
                            if self.team != u.team:
                                add_flag = False
                            else:
                                ally_locs.append(tmp_add)


                    if add_flag:
                        tmp.append(p + [tmp_add])

            for j in range(i):
                tl = [t[-1] for t in tmp]
                pl = [p[-1] for p in self.paths[j]]
                rm_ind = [tl.index(t) for t in tl if t in pl]
                for k in sorted(rm_ind, reverse=True):
                    del tmp[k]

            self.paths[i+1] = tmp

        # Remove any ally locations (so passable but can't end on it)
        for a in ally_locs:
            for i in reversed(range(len(self.paths))):
                for j in reversed(range(len(self.paths[i]))):
                    if a == self.paths[i][j][-1]:
                        del self.paths[i][j]

        # Don't include current location as allowable place to move
        self.paths.pop(0)

        self.path_ends = []
        for path in self.paths:
            for p in path:
                self.path_ends.append(p[-1])




class Type1():
    d_hp_max = 10
    d_mp_max = 10
    d_bp_max = 0
    d_shield_max = 0
    d_strength = 10
    d_vitality = 10
    d_magic = 10
    d_spirit = 10
    d_move = 0
    d_speed = 2

class Type2():
    d_hp_max = 9
    d_mp_max = 10
    d_bp_max = 0
    d_shield_max = 0
    d_strength = 10
    d_vitality = 10
    d_magic = 10
    d_spirit = 10
    d_move = 1
    d_speed = 1



# For waiting for user to select movement square
class doMove():

    def __init__(self, unit, Units, gameDisplay):
        unit.get_paths(Units, gameDisplay)
        self.paths = unit.path_ends
        self.clickables = []
        self.boost_count = unit.boost_count
        for p in self.paths:
            self.clickables.append(clickTest(gameDisplay, p[0], p[1]))
            #self.clickables.append(clickTest(
            #    gameDisplay.grid_to_pixel(p[0] + 5/gameDisplay.GRID_TO_PIXEL, p[1] + 5/gameDisplay.GRID_TO_PIXEL, False) + \
            #    (gameDisplay.GRID_TO_PIXEL-10, gameDisplay.GRID_TO_PIXEL-10)))
                #grid_to_pixel(p[0] + 5/GRID_TO_PIXEL, p[1] + 5/GRID_TO_PIXEL) + \
                #(GRID_TO_PIXEL-10, GRID_TO_PIXEL-10)))

    def handleEvent(self, event, unit, gameDisplay):
        for c in self.clickables:
            if c.handleEvent(event):
                pos = pygame.mouse.get_pos()
                #pos = pixel_to_grid(*pygame.mouse.get_pos())
                #pos = pixel_to_grid(*tuple(map(sum, zip(pos, (-gameDisplay.pixel_offset[0], -gameDisplay.pixel_offset[1])))))
                pos = gameDisplay.pixel_to_grid(*pos)
                unit.move_exact(*pos, gameDisplay)
                unit.moved = True
                break

        return unit

    def draw(self, gameDisplay):
        for c in self.clickables:
            c.draw(gameDisplay, (128, 96, 64))
            #c.draw(gameDisplay.screen, (128, 96, 64))


# For waiting for user to select movement square
class doAttack():

    def __init__(self, gameDisplay, unit):
        self.clickables = []
        self.boost_count = unit.boost_count
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        for d in directions:
            self.clickables.append(clickTest(gameDisplay, unit.x + d[0], unit.y + d[1]))
            #self.clickables.append(clickTest(
            #    grid_to_pixel(unit.x + d[0] + 5/GRID_TO_PIXEL, unit.y + d[1] + 5/GRID_TO_PIXEL) + \
            #    (GRID_TO_PIXEL - 10, GRID_TO_PIXEL - 10)))

    def handleEvent(self, event, gameDisplay, unit, Units):
        attacked_unit = None
        for c in self.clickables:
            if c.handleEvent(event):
                pos = gameDisplay.pixel_to_grid(*pygame.mouse.get_pos())
                attacked_unit = 'nothing'
                for u in Units:
                    if pos == (u.x, u.y):
                        attacked_unit = u
                unit.acted = True
                break

        return attacked_unit

    def draw(self, gameDisplay):
        for c in self.clickables:
            c.draw(gameDisplay, (64, 0, 16))
            #c.draw(gameDisplay.screen, (64, 0, 16))



# Function for displaying unit stats on the side
def show_stats(gameDisplay, unit):
    # (less) HARD CODED
    rel_x = 50
    rel_dx1 = 150
    rel_dx2 = 150
    rel_y = gameDisplay.map_h + 12
    rel_dy1 = 21
    rel_dy2 = 11

    # Calculate the coordinates
    def xy(n, dx_ind = 0, dy_ind = 0):
        return ((rel_x + dx_ind * rel_dx1, rel_y + rel_dy1 * n + dy_ind * rel_dy2))

    myfont = pygame.font.SysFont('Arial', 16)

    attr_order = ['name', '_hp', '_mp', '_bp', '_shield', '_ct', '_strength', '_vitality',
        '_magic', '_spirit', '_move', '_speed']
    attr_display = ['Name', 'HP', 'MP', 'BP', 'SH', 'CT', 'STR', 'VIT',
        'MAG', 'SPR', 'Move', 'Speed']

    # Specifying the coordinates
    # (The variables are poorly named, not intuitive as to what this is)
    #n_vec = [0, 1, 2, 3, 4, 5, 6, 6, 7, 7, 8, 8]
    #a_vec = [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1]
    #b_vec = [0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
    n_vec = [0, 1, 2, 3, 4, 5, 1, 1, 2, 2, 3, 3]
    a_vec = [0, 0, 0, 0, 0, 0, 1, 1.6, 1, 1.6, 1, 1.6]
    b_vec = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    for i in range(len(attr_order)):
        attrs = [a for a in dir(unit) if attr_order[i] in a]
        # Special case for CT
        if [a for a in attrs if "stat_ct" in a]:
            tmp_text = attr_display[i] + ": " + str(getattr(unit, attrs[0])) + " / 100"
            textsurface = myfont.render(str(tmp_text), False, (128, 0, 0))
            gameDisplay.screen.blit(textsurface, xy(n_vec[i], a_vec[i], b_vec[i]))
            continue

        # If "stat" is found in the attribute, goes on the left of " / ", otherwise just
        # show the "base"
        if [a for a in attrs if "stat" in a]:
            tmp_text = attr_display[i] + ": " + str(getattr(unit, attrs[-1])) + \
                " / " + str(getattr(unit, attrs[0]))
            textsurface = myfont.render(str(tmp_text), False, (128, 0, 0))
            gameDisplay.screen.blit(textsurface, xy(n_vec[i], a_vec[i], b_vec[i]))
        else:
            tmp_text = attr_display[i] + ": " + str(getattr(unit, attrs[0]))
            textsurface = myfont.render(str(tmp_text), False, (128, 0, 0))
            gameDisplay.screen.blit(textsurface, xy(n_vec[i], a_vec[i], b_vec[i]))



# Get unit next in turn order
# This is a recursive function that continually increases each units' CT by its
# base speed until there is a unit with CT >= 100. The unit with the highest CT
# is return, it is that unit's turn.
def unit_order(Units):
    # Sort first so highest CT will go first
    sl = sorted(Units, key = lambda x: x.stat_ct, reverse = True)
    # Check if any unit's CT as reached 100
    for u in sl:
        if u.stat_ct >= 100:
            return u
    else:
        # Increase all units CT by SPEED, don't need to use sorted list
        for u in Units:
            u.stat_ct += u.base_speed

        # Repeat until a unit reaches 100
        return unit_order(Units)

# Ceiling function
def ceil(a, b = 1): return int(-(-a // b))


# Class to display amount of damage taken over a unit
class dmgText():
    def __init__(self, text, unit, delay = 0, limit = 21):
        self.text = text
        self.delay = delay
        self.timer = 0
        self.limit = limit
        self.pos = (unit.x, unit.y)
        #self.pos_current = gameDisplay.grid_to_pixel(self.pos[0], self.pos[1])
        self.multiplier = random.randrange(800, 1200) / 1000.0
        self.font = pygame.font.SysFont('Arial', 16)
        self.textsurface = self.font.render(str(text), False, (255, 255, 255))

    def update(self):
        if self.delay > 0:
            self.delay -= 1
        else:
            self.timer += 1

    def draw(self, gameDisplay):
        self.update()
        if self.delay <= 0 and self.timer <= self.limit:
            # Up and down centered
            tmp = gameDisplay.grid_to_pixel(
                self.pos[0] + 0.5,
                self.pos[1] + 0.5 - max(0, (9 ** 2 - ((self.timer) - 9)**2) / 9.0 * self.multiplier) / gameDisplay.GRID_TO_PIXEL)
            gameDisplay.screen.blit(self.textsurface, tmp)


# Function for attacking a unit
def func_attack(attacker, defender, delay = 0):
    if defender.stat_shield > 0 and [] not in defender.weakness:
        p = 0.25
    if defender.stat_shield > 0 and [] in defender.weakness:
        p = 0.50
    if defender.stat_shield == 0 and [] not in defender.weakness:
        p = 0.90
    if defender.stat_shield == 0 and [] in defender.weakness:
        p = 1.00

    p = 1.00
    dmg = ceil( (2*attacker.base_strength - defender.base_vitality) * p)
    defender.stat_hp -= max(0, dmg)
    obj_dmgText = dmgText(str(dmg), defender, delay)
    return defender, obj_dmgText

# Different attack possibilities:
# Shield > 0, not weak: 25% DMG
# Shield > 0, weak:     50% DMG
# Shield = 0, not weak: 90% DMG
# Shield = 0, weak:     100% DMG

# You are punished more for not having shield
# Shield is only reduced when hit by a weakness

# Boost effects (max 3 BP can be used):
# - Regular attack: 1 + BP number of attacks
# - Magic attack:   DMG = DMG * (1 + BP * 0.75)
# - Accuracy:       Prob (p) = sum_{i = 1}^{BP} p * (1-p)^i, or sum(dgeom(0:BP, p)) # in R
#                   (This reduces the increase as BP increases, doesn't surpass 1)
# - Enables ultimates at 3 BP
# - Move increased by each BP
# - Status effects last BP more turns (as opposed to strengthening the effects)
# - Restore shield?
# - Temporarily guard against a weakness?
# - Increase starting CT after waiting?
# - Should using a boost on something other than waiting lower the starting CT?
#       (e.g. 3 BP move and no act reduces CT by 75+5*3 instead of 75?)

# Formulae
# Attack
#   DMG = CEIL((2 * STR - VIT) * P)
#
#           0.25    if Shield > 0 and not weak
#       P = 0.50    if Shield > 0 and weak
#           0.90    if Shield == 0 and not weak
#           1.00    if Shield == 0 and weak
#
#   ACC depends on defender's direction and class
#

