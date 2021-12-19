from tools import (get_csv_line_input_as_list, get_line_input_as_list)
import math

"""
IDEAS:
- Definitely seems like this is a weighted graph finding a path with the 
least total weight.
- Maybe start simple by doing DFS and making it all the way through, then
backtrack and stop if the path is ever more than that. It seems likely
that all 5s might also be a fine starting place.
- Feels like I might be able to do this with two DFS from start and end.

NOTES:
As the code below shows, I ended up implementing Dijkstra's for both solutions. 
Part 1 uses object representations of the graph and nodes with pointers to neighbors.
Part 2 uses a matrix representation, but doesn't actually build the FULL graph. Instead,
it calculates indices as needed. Building the whole graph from the beginning would 
probably speed up the algorithm, but at the cost of having to keep the whole thing in 
memory.
"""


class Graph:
    """Graph representing puzzle input used in part 1"""
    class Node:
        def __init__(self, value, north=None, east=None, south=None, west=None):
            self.value = value
            self.visited = False
            self.distance_from_start = value
            self.north = north
            self.east = east
            self.south = south
            self.west = west
            self.node_neighbors = []
            self.path_parent = None
            self.path_parent_direction = None
            self.visited = False
            self.distance_from_start = math.inf

    def __init__(self, input_list):
        """For each input number, make a graph with all of the nodes"""
        self.height = len(input_list)
        self.width = len(input_list[0])
        self.max_path = self.width * self.height * 9
        self.min_path_to_end = self.max_path
        self.node_list = []
        for i, line in enumerate(input_list):
            for j, char in enumerate(line):
                # make nodes for each item
                n = self.Node(int(char))
                self.node_list.append(n)

        for i, line in enumerate(input_list):
            for j, char in enumerate(line):

                # connect the nodes
                index = i * len(input_list[0]) + j

                # if not top row add bottom
                if i != len(input_list) - 1:
                    self.node_list[index].south = self.node_list[index + len(input_list[0])]
                    self.node_list[index].node_neighbors.append(self.node_list[index].south)

                # if not last column add right
                if j != len(input_list[0])-1:
                    self.node_list[index].east = self.node_list[index+1]
                    self.node_list[index].node_neighbors.append(self.node_list[index].east)

                # if not first column add left
                if j != 0:
                    self.node_list[index].west = self.node_list[index - 1]
                    self.node_list[index].node_neighbors.append(self.node_list[index].west)

                # if not bottom row add top
                if i != 0:
                    self.node_list[index].north = self.node_list[index - len(input_list[0])]
                    self.node_list[index].node_neighbors.append(self.node_list[index].north)

        self.start = self.node_list[0]
        self.end = self.node_list[len(input_list[0]) * len(input_list) - 1]

    def __str__(self):
        left_node = self.start
        output = []
        while left_node.south:
            node = left_node
            row = []
            while node.east:
                row.append(node.value)
                node = node.east
            row.append(node.value)
            output.append("".join(row))
            left_node = left_node.south

        row = []
        node = left_node
        while node.east:
            row.append(node.value)
            node = node.east
        row.append(node.value)
        output.append("".join(row))

        return "\n".join(output)

    def get_value(self, index):
        """Gives value of passed index"""
        node = self.node_list[index]
        return node.value

    def find_shortest_path_dijkstra(self):
        """Implements dijkstra's shortest path algorithm returning the shortest
        distance from the start of the end node with a few notes:
        - saves time by not setting visited to False and distance_from_start for all
          (Assumes I'll only be running this once per program run)
        - First past just scanned all of the nodes to find the next smallest node. Turning
          that into a set (like the algorithm is supposed to have) roughly halved the execution
          time. Next, adding only discovered nodes to the set instead of having them all in memory
          at the beginning reduced run time from a few seconds to about one second. A further
          optimization would be to use a priority queue instead of a set.
        """

        # set all nodes visited to False and distance to node value
        # This is skipped because nodes are initialized with it and I assume
        # that I'm only finding the shortest path once

        self.start.distance_from_start = 0
        n = self.start
        node_horizon_set = {n}
        while n and not self.end.visited:

            for neighbor in n.node_neighbors:
                if not neighbor.visited:
                    node_horizon_set.add(neighbor)
                    # update the distances to those nodes using the current one
                    neighbor.distance_from_start = min(neighbor.distance_from_start,
                                                       n.distance_from_start + neighbor.value)

            # mark the current node as visited and remove it from the horizon
            n.visited = True
            node_horizon_set.remove(n)

            # get the next smallest unvisited node by checking the horizon set
            next_node_distance_from_start = math.inf
            node_to_use_next = None
            for pn in node_horizon_set:
                if pn.distance_from_start < next_node_distance_from_start:
                    next_node_distance_from_start = pn.distance_from_start
                    node_to_use_next = pn
            n = node_to_use_next

        return self.end.distance_from_start


class LargeGraph:
    """Graph representing puzzle input used in part 2

    Only real hiccup was shifting fully from my object-based approach in part 1 to
    this less object focused one. The approach used here only creates Nodes as they
    are discovered (instead of making them all in the beginning). Eventually, I realized
    that I hadn't implemented __eq__ or __hash__ methods for Nodes, so they kept being
    duplicated in the set of potential nodes to visit.
    """

    class Node:
        def __init__(self, index, value, distance=math.inf):
            self.index = int(index)
            self.value = int(value)
            self.distance = distance

        def __eq__(self, other):
            return self.index == other.index

        def __hash__(self):
            return hash(self.index)

    def __init__(self, input_list):
        # input_list is matrix of graph
        self.block_matrix = input_list

        # save handy dimensions
        self.block_width = len(input_list[0])
        self.block_height = len(input_list)
        self.map_width = self.block_width * 5
        self.map_height = self.block_height * 5

        # save handy nodes
        self.start = self.Node(0, input_list[0][0], 0)
        self.end = self.Node((self.map_width * self.map_height) - 1, self.get(self.map_width * self.map_height - 1))

        # used in neighbor methods
        self.directions = ["north", "east", "south", "west"]

    def __str__(self):
        output = []
        for i in range(self.map_height):
            line = []
            for j in range(self.map_width):
                line.append(str(self.get(j + self.map_width * i)))
            output.append("".join(line))
        return "\n".join(output) + "\n"

    def is_index_valid(self, index):
        """Returns block_diff from original of an index or -1 if it doesn't exist.
        Given an absolute index, the block diff will be vertical blocks * horizontal blocks away
        """
        output = -1
        if index > self.map_height * self.map_width - 1:
            return output
        else:
            # horizontal block diff is how many blocks right from the original block it is
            h_blocks = (index % self.map_width) // self.block_width

            # vertical block diff is how many blocks down from the original block it is
            v_blocks = index // (self.map_width * self.block_height)
            output = h_blocks + v_blocks

        return output

    def get_neighbor(self, index, direction):
        """Returns the index to the {direction} of the passed index"""
        # North
        if direction == "north":
            north_index = self.is_index_valid(index - self.map_width)
            if north_index >= 0:
                return index - self.map_width
        # East
        if direction == "east":
            east_index = self.is_index_valid(index + 1)
            if east_index >= 0 and index % self.map_width < self.map_width:
                return index + 1
        # South
        if direction == "south":
            south_index = self.is_index_valid(index + self.map_width)
            if south_index >= 0:
                return index + self.map_width
        # West
        if direction == "west":
            west_index = self.is_index_valid(index - 1)
            if west_index >= 0 and index % self.map_width > 0:
                return index - 1

        return -1

    def get_indices_of_neighbors(self, index):
        # If number not in whole map, raise error
        index_block_diff = self.is_index_valid(index)
        if index_block_diff < 0:
            raise ValueError(f"Index {index} is not in map with width: {self.map_width} height: {self.map_height}")
        else:
            # get neighbor indices
            neighbor_indices = []
            for direction in self.directions:
                new_index = self.get_neighbor(index, direction)
                if new_index > -1:
                    neighbor_indices.append(new_index)
        return neighbor_indices

    def get(self, index):
        # If number not in whole map, raise error
        index_block_diff = self.is_index_valid(index)
        if index_block_diff < 0:
            raise ValueError(f"Index {index} is not in map with width: {self.map_width} height: {self.map_height}")

        # If index is within the block, return the value found in the block
        v = index // self.map_width % self.block_width
        w = index % self.block_width
        block_value = int(self.block_matrix[index // self.map_width % self.block_width][index % self.block_width])

        # indices_to_check = [0, 1, 2, 50, 51, 52, 49, 99, 2499]
        # an index is in the block if
        if (index % self.map_width // self.block_width) == 0 and index < self.block_height * self.map_width:
            return self.block_matrix[index // self.map_width][index % self.map_width]

        # Otherwise take the value found in the block and increment it by 1 per block away the number is
        else:
            node_value = (index_block_diff + block_value) % 9
            if node_value == 0:
                node_value = 9
            return node_value

    def find_shortest_path_dijkstra(self):
        """Implements dijkstra's shortest path algorithm discovering nodes and
           calculates their value as it goes.
        """
        self.start.distance_from_start = 0
        n = self.start
        # node_horizon_set = set(self.node_list)
        node_horizon_set = {n}
        nodes_visited_set = set()
        while n:
            # get node neighbors
            if n.index == 2449:
                n.index = n.index
            node_neighbors = self.get_indices_of_neighbors(n.index)
            # print(f"on node: {n.index} with value {n.value} and neighbors {node_neighbors}")
            for neighbor_index in node_neighbors:
                if neighbor_index not in nodes_visited_set:

                    # Add each neighbor node to the horizon if it hasn't been visited
                    neighbor_node = self.Node(neighbor_index, self.get(neighbor_index))
                    # print(f"Added {neighbor_node.index}, {neighbor_node.value}")
                    node_horizon_set.add(neighbor_node)

                    # Update the min distance from start of each neighbor
                    neighbor_node.distance = min(neighbor_node.distance, n.distance + neighbor_node.value)

            # Remove the current node from the horizon and added it to the set of visited
            nodes_visited_set.add(n.index)

            # Get the next smallest unvisited node by checking the horizon set
            next_node_distance_from_start = math.inf
            node_to_use_next = None
            for potential_next_node in node_horizon_set:
                if potential_next_node.distance < next_node_distance_from_start:
                    next_node_distance_from_start = potential_next_node.distance
                    node_to_use_next = potential_next_node

            # Break loop if end is processed
            if n.index == self.end.index:
                return n.distance

            else:
                n = node_to_use_next
                node_horizon_set.remove(n)
        return self.end.distance


def part1(input_list):
    g = Graph(input_list)
    path = g.find_shortest_path_dijkstra()
    return path


def part2(input_list):
    """Seems like there are two approachs:
       - Build the whole graph first then treat it like the first problem
       - Build the graph as you go

       I like the building as you go idea and it kind of means we can use dijkstra's
       without the burden of using an actual graph

       Start on index 0.
       Make empty set of discovered nodes
       Add starting node
       While end hasn't been visited and there are nodes left:
       - Get node with smallest distance
       - For each of the potentially four direction neighbors:
         - Use current index to calculate index of the neighbor
         - If the neighbor exists:
            - Make a node with just a value and distance and add it to the queue
       - Mark current node as visited...or just pop it from the stack.
       - set current node as the next lowest distance node from the stack

       In the end, calculating the final answer took about 20 seconds to run.
       """
    g = LargeGraph(input_list)

    path = g.find_shortest_path_dijkstra()
    return path


def p15():
    filename = "inputs/15"
    ext = ".txt"
    input_list = get_line_input_as_list(filename + ext, "string")
    input_list_test = get_line_input_as_list(filename + "-test" + ext, "string")
    input_list_test2 = get_line_input_as_list(filename + "-test2" + ext, "string")

    output1 = part1(input_list_test2)
    output2 = part2(input_list_test)

    return output1, output2
