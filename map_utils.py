from tdl.map import Map
from random import randint
from entity import Entity
from components.ai import BasicMonster
from components.fighter import Fighter
from render_functions import RenderOrder


class GameMap(Map):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.explored = [[False for y in range(height)] for x in range(width)]


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


def create_room(game_map, room):
    # go through the tiles in the room and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            game_map.walkable[x, y] = True
            game_map.transparent[x, y] = True


def create_h_tunnel(game_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True


def create_v_tunnel(game_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True


def place_entities(room, entities, max_monsters_per_room, colors):
    number_of_monsters = randint(0, max_monsters_per_room)

    for i in range(number_of_monsters):
        # get a random location in the room
        x = randint(room.x1 + 1, room.x2 -1)
        y = randint(room.y1 + 1, room.y2 -1)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            choice = randint(0, 100)
            if choice < 60:
                fighter_component = Fighter(hp=10, defense=0, power=3)
                ai_component = BasicMonster()
                # withered husk

                monster = Entity(x, y, "h", colors.get("dark_gray"), "withered husk", blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
            elif choice < 60 + 30:
                # rusted automaton
                fighter_component = Fighter(hp=16, defense=1, power=4)
                ai_component = BasicMonster()

                monster = Entity(x, y, "a", colors.get("brass"), "rusted automaton", blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
            else:
                # kobold bandit
                fighter_component = Fighter(hp=20, defense=0, power=5)
                ai_component = BasicMonster()

                monster = Entity(x, y, "b", colors.get("darker_flame"), "kobold bandit", blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

            entities.append(monster)


def make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
             max_monsters_per_room, colors):

    rooms = []
    num_rooms = 0

    for r in range(max_rooms):
        # random width and height
        w = randint(room_min_size, room_max_size)
        h = randint(room_min_size, room_max_size)
        # random position within map boundaries
        x = randint(0, map_width - w - 1)
        y = randint(0, map_height - h - 1)

        # Rect class makes rectangles easier to use
        new_room = Rect(x, y, w, h)

        # check other rooms for intersections
        for other_room in rooms:
            if new_room.intersect(other_room):
                break

        else:
            create_room(game_map, new_room)

            # center coordinates of new room, for later
            (new_x, new_y) = new_room.center()

            if num_rooms == 0:
                # this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y
            else:
                # all rooms after the first are connected to the previous one by tunnel

                # center of previous room
                (prev_x, prev_y) = rooms[num_rooms -1].center()

                # flip a coin
                if randint(0, 1) == 1:
                    # horizontal then vertical
                    create_h_tunnel(game_map, prev_x, new_x, prev_y)
                    create_v_tunnel(game_map, prev_y, new_y, new_x)
                else:
                    # vertical then horizontal
                    create_v_tunnel(game_map, prev_y, new_y, prev_x)
                    create_h_tunnel(game_map, prev_x, new_x, new_y)

            place_entities(new_room, entities, max_monsters_per_room, colors)

            rooms.append(new_room)
            num_rooms += 1