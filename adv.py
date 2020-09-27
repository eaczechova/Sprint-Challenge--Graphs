from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

class Graph:
    def __init__(self):
        self.vertices = {}
    
    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = {}
            # directions = player.current_room.get_exits()
       
            # for d in directions:
            #     graph.vertices[vertex_id][d] = '?'

    def add_edge(self, vertex_id, key, value):
        self.vertices[vertex_id][key] = value
            
    def __repr__(self):
        return str(self.vertices)


class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)


# list of directions to follow
traversal_path = []

# list of visited rooms
visited_rooms = set()

# instantiate Graph class
graph = Graph()

# instantiate Stack class
stack = Stack()

# Helper functions

# function to find opposite direction 
def reverse_direction(direction):
    if direction == "n":
        return "s"
    elif direction == "s":
        return "n"
    elif direction == "e":
        return "w"
    else:
        return "e"

# additional function that draw new maze - to be fixed !!!
def draw_graph(current_room, direction, next_room):
    rev_direction = reverse_direction(direction)
    
    graph.add_vertex(current_room)
    if direction in player.current_room.get_exits():
        graph.add_edge(current_room, direction, next_room)
    graph.add_vertex(next_room)
    # if direction in player.current_room.get_exits():
    graph.add_edge(next_room, rev_direction, current_room)

# add first direction from current room direction array, e.g 'n', to traversal_path
traversal_path = [player.current_room.get_exits()[0]]
# add first direction from current room direction array, e.g 'n', to the stack
stack.push(player.current_room.get_exits()[0])

# while stack is not empty we traverse the maze
while stack.size() > 0:
    # get direction from the end of the stack
    move = stack.pop()
    
    ### for draw_graph()
    cur_room = player.current_room
    # print("cur_room", cur_room)
    # travel (current room changes)
    player.travel(move)

    ### for draw_graph()
    n_room = player.current_room

    # check if the current room has not been visited before
    if player.current_room not in visited_rooms:
        # append reverse_direction of taken direction to the traversal_path and stack
        traversal_path.append(reverse_direction(move))
        stack.push(reverse_direction(move))
        # add room to visited to avoid going in circles
        visited_rooms.add(player.current_room)
    
    # get all the direction from the current room 
    room_directions = player.current_room.get_exits()
    # loop over each direction player can go from the current room  
    for direction in room_directions:
        # set the next room for each direction
        next_room = player.current_room.get_room_in_direction(direction)
     
        # print("next_room", next_room.id)
        # if the room has not been visited
        if next_room and next_room not in visited_rooms:
            # append direction to out traversal_path and stack
            draw_graph(cur_room, direction, next_room)
            traversal_path.append(direction)
            stack.push(direction)
            break

print("Traversal_path:", traversal_path)
print("New graph:", graph.vertices)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
