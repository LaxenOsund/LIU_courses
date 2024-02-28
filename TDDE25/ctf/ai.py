import math
import pymunk
from pymunk import Vec2d
import gameobjects
from collections import defaultdict, deque
import pygame

# NOTE: use only 'map0' during development!

MIN_ANGLE_DIF = math.radians(5) # 3 degrees, a bit more than we can turn each tick



def angle_between_vectors(vec1, vec2):
    """ Since Vec2d operates in a cartesian coordinate space we have to
        convert the resulting vector to get the correct angle for our space.
    """
    vec = vec1 - vec2 
    vec = vec.perpendicular()
    return vec.angle

def periodic_difference_of_angles(angle1, angle2): 
    return  (angle1% (2*math.pi)) - (angle2% (2*math.pi))


class Ai:
    """ A simple ai that finds the shortest path to the target using 
    a breadth first search. Also capable of shooting other tanks and or wooden
    boxes. """

    def __init__(self, tank,  game_objects_list, tanks_list, space, currentmap):
        self.tank               = tank
        self.game_objects_list  = game_objects_list
        self.tanks_list         = tanks_list
        self.space              = space
        self.currentmap         = currentmap
        self.flag = None
        self.MAX_X = currentmap.width - 1 
        self.MAX_Y = currentmap.height - 1

        self.path = deque()
        self.move_cycle = self.move_cycle_gen()
        self.last_shot = pygame.time.get_ticks()

        

    def update_grid_pos(self):
        """ This should only be called in the beginning, or at the end of a move_cycle. """
        self.grid_pos = self.get_tile_of_position(self.tank.body.position)


    def decide(self):
        """ Main decision function that gets called on every tick of the game. """
        if self.tank.cooldown >=50:
            self.maybe_shoot()
        next(self.move_cycle)


    def maybe_shoot(self):
        """ Makes a raycast query in front of the tank. If another tank
            or a wooden box is found, then we shoot. 
        """
        
        ray_start = (self.tank.body.position[0] - math.sin(self.tank.body.angle) * 0.5, self.tank.body.position[1] + math.cos(self.tank.body.angle) * 0.5)
        ray_end = (self.tank.body.position[0] - math.sin(self.tank.body.angle) * 10, self.tank.body.position[1] + math.cos(self.tank.body.angle) * 10)
        res = self.space.segment_query_first(ray_start, ray_end, 0, pymunk.ShapeFilter())

        if hasattr(res, "shape"):
            if hasattr(res.shape, "parent"):
                object = res.shape.parent
                if isinstance(object, gameobjects.Tank) or isinstance(object, gameobjects.Box) and object.shape.collision_type == 3:
                    bullet = self.tank.shoot(self.space)
                    self.game_objects_list.append(bullet)
                    self.tank.cooldown = 0
           

    def move_cycle_gen (self):
        """ A generator that iteratively goes through all the required steps
            to move to our goal.
        """       
        check_viable_path = 0  
        while True:
            self.update_grid_pos()
            check = 1000
            if check_viable_path == 1:
                path = self.find_shortest_path(check_viable_path)
                check_viable_path = 0
            else:
                path = self.find_shortest_path()
            
            if len(path) < 1:
                check_viable_path = 1
                yield
                continue # Start from the top of our cycle
            next_coord = path.popleft() + (0.5,0.5)
            correct_angle = angle_between_vectors(self.tank.body.position, next_coord)
            yield
            
            while not abs(periodic_difference_of_angles(self.tank.body.angle, correct_angle)) <= MIN_ANGLE_DIF:
                self.tank.stop_moving()
                if (correct_angle - self.tank.body.angle) % (2*math.pi) <= math.pi:
                    self.tank.turn_right()
                if (correct_angle - self.tank.body.angle) % (2*math.pi) >= math.pi:
                    self.tank.turn_left()
                yield
            self.tank.stop_turning()
            check_bool = True
            yield
            while check_bool:
                distance = self.tank.body.position.get_distance(next_coord)
                if distance >= check:
                    check_bool = False
                check = self.tank.body.position.get_distance(next_coord)
                self.tank.accelerate()
                yield
            continue

        
    def find_shortest_path(self, check = 0):
        """ A simple Breadth First Search using integer coordinates as our nodes.
            Edges are calculated as we go, using an external function.
        """

        shortest_path = []
        spawn = self.grid_pos
        queue = deque()
        visited = set()
        path = {}

        queue.appendleft(spawn)
        visited.add(spawn.int_tuple)
        path[spawn.int_tuple] = []
        while len(queue) > 0:
            node = queue.popleft()
            if node == self.get_target_tile():
                shortest_path = path[node.int_tuple]
                break
            if check == 1:
                for neighbor in self.get_tile_neighbors(node, check):
                    if not neighbor[0].int_tuple in visited:
                        queue.append(neighbor[0])
                        visited.add(node.int_tuple)
                        # path to neighbor = path to previous pos + neighbor pos
                        path[neighbor[0].int_tuple] = path[node.int_tuple] + [neighbor[0]]
            else:
                for neighbor in self.get_tile_neighbors(node):
                    if not neighbor[0].int_tuple in visited:
                        queue.append(neighbor[0])
                        visited.add(node.int_tuple)
                        # path to neighbor = path to previous pos + neighbor pos
                        path[neighbor[0].int_tuple] = path[node.int_tuple] + [neighbor[0]]
        return deque(shortest_path)
            
    def get_target_tile(self):
        """ Returns position of the flag if we don't have it. If we do have the flag,
            return the position of our home base.
        """
        if self.tank.flag != None:
            x, y = self.tank.start_position
        else:
            self.get_flag() # Ensure that we have initialized it.
            x, y = self.flag.x, self.flag.y
        return Vec2d(int(x), int(y))

    def get_flag(self):
        """ This has to be called to get the flag, since we don't know
            where it is when the Ai object is initialized.
        """
        if self.flag == None: 
        # Find the flag in the game objects list
            for obj in self.game_objects_list:
                if isinstance(obj, gameobjects.Flag):
                    self.flag = obj
                    break
        return self.flag

    def get_tile_of_position(self, position_vector):
        """ Converts and returns the float position of our tank to an integer position. """
        x, y = position_vector
        return Vec2d(int(x), int(y))

    def get_tile_neighbors(self, coord_vec, check = 0):
        """ Returns all bordering grid squares of the input coordinate.
            A bordering square is only considered accessible if it is grass
            or a wooden box.
        """
        neighbors = []# Find the coordinates of the tiles' four neighbors
        up = (coord_vec + Vec2d(0,1), check)
        down = (coord_vec + Vec2d(0,-1), check)
        left = (coord_vec + Vec2d(-1,0), check)
        right = (coord_vec + Vec2d(1,0), check)
        
        neighbors.append(up)
        neighbors.append(down)
        neighbors.append(left)
        neighbors.append(right)
        return filter(self.filter_tile_neighbors, neighbors)

    def filter_tile_neighbors (self, coord):
        coord, check = coord
        if check == 1:
            if coord[0] <= self.MAX_X and coord[0] >= 0 and\
                coord[1] <= self.MAX_Y and coord[1] >= 0:
                if self.currentmap.boxAt(coord[0],coord[1]) == 0 or self.currentmap.boxAt(coord[0],coord[1]) == 2 or self.currentmap.boxAt(coord[0],coord[1]) == 3:
                    return True
        if coord[0] <= self.MAX_X and coord[0] >= 0 and\
            coord[1] <= self.MAX_Y and coord[1] >= 0:
            if self.currentmap.boxAt(coord[0],coord[1]) == 0 or self.currentmap.boxAt(coord[0],coord[1]) == 2:
                return True
            else:
                return False

SimpleAi = Ai # Legacy