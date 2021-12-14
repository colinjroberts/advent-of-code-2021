from tools import (get_csv_line_input_as_list, get_line_input_as_list) 
"""
General Approach:
- Parse input to build a graph
- Search graph for paths 
    - Start at start
    - If current location is end:
        - End, add path to list, return nothing
    - Get list of neighbors
    - For each eligible neighbor (not lowercase already visited) repeat
    
I represented the graph as a dictionary because that what came to mind first.
Making a little graph class would clean this code up a bit. It would also clean 
up some of the recursion base case checking by needing fewer parameters and using
the more typical if node.visited type of stuff. The Graph object could keep track
of whether a duplicate path was found for Part 2, but that would also require setting
it back to 0 instead of letting the recursion take care of it like in this solution.

I'll be interested to see some tighter solutions.
"""

def part1(input_list):
    def path_find(node, current_path, successful_paths):
        current_path.append(node)

        # Stop if a end is reached and add path to successful_paths
        if node == 'end':
            successful_paths.append(current_path.copy())
            current_path.pop()
            return

        # Stop if start is reached again
        if node == 'start' and current_path.count(node) > 1:
            current_path.pop()
            return

        # Stop if a lowercase node is already in the path
        if node.islower() and current_path.count(node) > 1:
            current_path.pop()
            return

        # Otherwise, keep searching for valid paths
        else:
            for child_node in graph[node]:
                # print(f"On node {node} going to child {child_node}")
                path_find(child_node, current_path, successful_paths)

        # When done searching, pop this node off and finish the previous recursion
        current_path.pop()
        return

    def create_graph_dict(input_list):
        graph_dict = {}
        for line in input_list:
            elements = line.split('-')
            if elements[0] in graph_dict:
                graph_dict[elements[0]].add(elements[1])
            else:
                graph_dict[elements[0]] = {elements[1]}

            if elements[0] != 'start' and elements[1] != 'end':
                if elements[1] in graph_dict:
                    graph_dict[elements[1]].add(elements[0])
                else:
                    graph_dict[elements[1]] = {elements[0]}
        return graph_dict

    graph = create_graph_dict(input_list)
    # print(graph)
    current_path = []
    successful_paths = []
    path_find('start', current_path, successful_paths)
    return len(successful_paths)



def part2(input_list):
    """Part 2 Adds an additional end case.

    Now we also need to stop if the current node is lowercase AND a different lowercase
    letter has already been used
    """
    def path_find(node, current_path, doubled_path, successful_paths):
        # add the current node and mark true if it is a double
        current_path.append(node)

        # Stop if node is end
        if node == 'end':
            successful_paths.append(",".join(current_path))
            current_path.pop()
            return

        # Stop if start comes up more than once
        if node == 'start' and current_path.count(node) > 1:
            current_path.pop()
            return

        # Stop if lowercase letter is reached, already in list, and there is already a double
        if node != 'start' and node.islower():
            if doubled_path:
                if node == doubled_path and current_path.count(node) > 2:
                    current_path.pop()
                    return
                elif current_path.count(node) > 1:
                    current_path.pop()
                    return
            if current_path.count(node) == 2:
                for child_node in graph[node]:
                    path_find(child_node, current_path, node, successful_paths)
            else:
                for child_node in graph[node]:
                    path_find(child_node, current_path, doubled_path, successful_paths)

        # Otherwise, keep searching for valid paths
        else:
            for child_node in graph[node]:
                path_find(child_node, current_path, doubled_path, successful_paths)

        # When done searching, pop this node off and finish the previous recursion
        current_path.pop()
        return

    def create_graph_dict(input_list):
        graph_dict = {}
        for line in input_list:
            elements = line.split('-')
            if elements[0] in graph_dict:
                graph_dict[elements[0]].add(elements[1])
            else:
                graph_dict[elements[0]] = {elements[1]}

            if elements[0] != 'start' and elements[1] != 'end':
                if elements[1] in graph_dict:
                    graph_dict[elements[1]].add(elements[0])
                else:
                    graph_dict[elements[1]] = {elements[0]}
        return graph_dict

    graph = create_graph_dict(input_list)
    current_path = []
    successful_paths = []
    path_find('start', current_path, '', successful_paths)
    # for item in set(successful_paths):
    #     print(item)
    return len(set(successful_paths))

def p12():
    filename = "inputs/12"
    ext = ".txt"
    input_list = get_line_input_as_list(filename + ext, "string")
    input_list_test1 = get_line_input_as_list(filename + "-test1" + ext, "string")
    input_list_test2 = get_line_input_as_list(filename + "-test2" + ext, "string")
    input_list_test3 = get_line_input_as_list(filename + "-test3" + ext, "string")

    output1 = part1(input_list)
    output2 = part2(input_list)

    return output1, output2
