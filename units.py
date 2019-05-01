import pygame

class Unit(pygame.sprite.Sprite):
    def __init__(self, name, color, JobPrimary = None, JobSecondary = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(color + "_triangle.png")
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.name = name
        # Inital stats
        self.stat_hp       = 100
        self.stat_mp       = 100
        self.stat_bp       = 5
        self.stat_strength = 10
        self.stat_vitality = 10
        self.stat_magic    = 10
        self.stat_spirit   = 10
        self.stat_move     = 3
        self.stat_speed    = 8
        # Primary job stat adjustments
        self.job_stats(JobPrimary, 1)
        self.job_stats(JobSecondary, 2)

    def job_stats(self, Job = None, degree = 1):
        if Job is not None:
            self.stat_hp       += int(Job.d_hp / degree)
            self.stat_mp       += int(Job.d_mp / degree)
            self.stat_bp       += int(Job.d_bp / degree)
            self.stat_strength += int(Job.d_strength / degree)
            self.stat_vitality += int(Job.d_vitality / degree)
            self.stat_magic    += int(Job.d_magic / degree)
            self.stat_spirit   += int(Job.d_spirit / degree)
            self.stat_move     += int(Job.d_move / degree)
            self.stat_speed    += int(Job.d_speed / degree)

    def move_delta(self, dx, dy, Map):
        self.x = min(max(Map.xrange[0], self.x + dx), Map.xrange[1])
        self.y = min(max(Map.yrange[0], self.y + dy), Map.yrange[1])

    # Can probably simplify to not need Map since we can verify the possible
    # moves outside of the class, unless the get_paths method should be part
    # of this class?
    def move_exact(self, dx, dy, Map):
        if abs(self.x - dx) + abs(self.y - dy) <= self.stat_move and \
            Map.xrange[0] <= dx and dx <= Map.xrange[1] and \
            Map.yrange[0] <= dy and dy <= Map.yrange[1]:
            self.x = dx
            self.y = dy

    def get_paths(self, Units, Map):
        self.paths = [(self.x, self.y)]
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for p in self.paths:
            # distance under current path from origin
            dx = p[0] - self.paths[0][0]
            dy = p[1] - self.paths[0][1]
            # Break out of loop if total distance exceeds move limit
            if abs(dx) + abs(dy) >= self.stat_move:
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
                    for u in Units:
                        if tmp == (u.x, u.y):
                            test_flag = False
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
        #return paths


class Type1():
    d_hp = 10
    d_mp = 10
    d_bp = 10
    d_strength = 10
    d_vitality = 10
    d_magic = 10
    d_spirit = 10
    d_move = 1
    d_speed = 1

class Type2():
    d_hp = 10
    d_mp = 10
    d_bp = 10
    d_strength = 10
    d_vitality = 10
    d_magic = 10
    d_spirit = 10
    d_move = 3
    d_speed = 1
