import pygame

class Unit(pygame.sprite.Sprite):
    def __init__(self, team, name, color, JobPrimary = None, JobSecondary = None):
        pygame.sprite.Sprite.__init__(self)
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
        # Weaknesses
        self.weakness = []
        # Action properties
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

    # Can probably simplify to not need Map since we can verify the possible
    # moves outside of the class, unless the get_paths method should be part
    # of this class?
    def move_exact(self, dx, dy, Map):
        if abs(self.x - dx) + abs(self.y - dy) <= self.base_move and \
            Map.xrange[0] <= dx and dx <= Map.xrange[1] and \
            Map.yrange[0] <= dy and dy <= Map.yrange[1]:
            self.x = dx
            self.y = dy

    def get_paths(self, Units, Map):
        self.paths = [(self.x, self.y)]
        ally_locs = []
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for p in self.paths:
            # distance under current path from origin
            dx = p[0] - self.paths[0][0]
            dy = p[1] - self.paths[0][1]
            # Break out of loop if total distance exceeds move limit
            if abs(dx) + abs(dy) >= self.base_move:
                break
            for d in directions:
                # Add current location p to directional movement d
                tmp = tuple(map(sum, zip(p, d)))
                try:
                    # Only proceed if the proposed location hasn't been traversed before
                    self.paths.index(tmp)
                except:
                    test_flag = True
                    # check not to collide with other units
                    # can't pass enemies, but can pass allies
                    for u in Units:
                        if tmp == (u.x, u.y):
                            if self.team != u.team:
                                test_flag = False
                            else:
                                ally_locs.append(tmp)
                    if test_flag:
                        try:
                            # check if proposed move location is a valid grid point on the map
                            # (think of the missing spots as impassable trees, not holes to jump over)
                            Map.grid.index(tmp)
                            self.paths.append(tmp)
                            #pygame.draw.rect(area.screen, (0, 128, 0),
                            #    grid_to_pixel(tmp[0] + 1, tmp[1] + 1) + \
                            #    (GRID_TO_PIXEL-25, GRID_TO_PIXEL-25))
                        except:
                            pass

        # Remove any ally locations (so passable but can't end on it)
        for a in ally_locs:
            if a in self.paths:
                self.paths.pop(self.paths.index(a))

        # Don't include current location as allowable place to move
        self.paths.pop(0)


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


# Different attack possibilities:
# Shield > 0, not weak: 25% DMG
# Shield > 0, weak:     50% DMG
# Shield = 0, not weak: 90% DMG
# Shield = 0, weak:     100% DMG

# You are punished more for not having shield
# Shield is only reduced when hit by a weakness


# Function for displaying unit stats on the side
def show_stats(gameDisplay, unit):
    # HARD CODED
    rel_x = 600
    rel_dx = 100
    rel_dy1 = 21
    rel_dy2 = 11

    # Calculate the coordinates
    def xy(n, dx_ind = 0, dy_ind = 0):
        return ((rel_x + dx_ind * rel_dx, 8 + rel_dy1 * n + dy_ind * rel_dy2))

    myfont = pygame.font.SysFont('Arial', 16)

    attr_order = ['name', '_hp', '_mp', '_bp', '_shield', '_ct', '_strength', '_vitality',
        '_magic', '_spirit', '_move', '_speed']
    attr_display = ['Name', 'HP', 'MP', 'BP', 'SH', 'CT', 'STR', 'VIT',
        'MAG', 'SPR', 'Move', 'Speed']

    # Specifying the coordinates
    # (The variables are poorly named, not intuitive as to what this is)
    n_vec = [0, 1, 2, 3, 4, 5, 6, 6, 7, 7, 8, 8]
    a_vec = [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1]
    b_vec = [0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]

    for i in range(len(attr_order)):
        attrs = [a for a in dir(unit) if attr_order[i] in a]
        # Special case for CT
        if [a for a in attrs if "stat_ct" in a]:
            tmp_text = attr_display[i] + ": " + str(getattr(unit, attrs[0])) + " / 100"
            textsurface = myfont.render(str(tmp_text), False, (128, 0, 0))
            gameDisplay.blit(textsurface, xy(n_vec[i], a_vec[i], b_vec[i]))
            continue

        # If "stat" is found in the attribute, goes on the left of " / ", otherwise just
        # show the "base"
        if [a for a in attrs if "stat" in a]:
            tmp_text = attr_display[i] + ": " + str(getattr(unit, attrs[-1])) + \
                " / " + str(getattr(unit, attrs[0]))
            textsurface = myfont.render(str(tmp_text), False, (128, 0, 0))
            gameDisplay.blit(textsurface, xy(n_vec[i], a_vec[i], b_vec[i]))
        else:
            tmp_text = attr_display[i] + ": " + str(getattr(unit, attrs[0]))
            textsurface = myfont.render(str(tmp_text), False, (128, 0, 0))
            gameDisplay.blit(textsurface, xy(n_vec[i], a_vec[i], b_vec[i]))

