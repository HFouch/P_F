from Class_Astar_Node import Node

class AstarAlgorithm:

    def __init__(self, start_state, end_state):
        self.start_state = start_state
        self.end_state = end_state
        self.start_node = Node(start_state)
        self.target_node = Node(end_state)
        self.Paths = []
        self.Actions = []


    def astar(self, k):
        '''

        :param k: the maximum number of shortest paths desired as output
        :return: 2 lists. A list of paths and the associated list of actions taken
        '''

        # create start and end node
        start_node = Node(self.start_state, None)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(self.end_state, None)
        end_node.g = end_node.h = end_node.f = 0

        # initialize open and closed lists
        open_list = []
        closed_list = []

        # add start_node
        open_list.append(start_node)

        # loop until find end state
        while len(open_list) > 0:

            # %%%
            # get current node (the node with the lowest f in the openlist)
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # remove current node from open list and add it to the closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # if the end state is achieved:
            if current_node.is_equivalent(self.end_state):
                path = []
                actions_taken = []
                current = current_node
                while current is not None:
                    path.append(current.state)
                    actions_taken.append(current.parent_operation)
                    current = current.parent

                self.Paths.append(path[::-1])
                self.Actions.append(actions_taken[::-1])
                # return path[::-1], actions_taken[::-1]

                if len(self.Paths) == k:
                    return self.Paths, self.Actions
                # CONTINUE AT %%% PART OF THE CODE

            children = []
            for operation in current_node.get_legal_operations(self.end_state):
                new_state = current_node.take_action(operation)
                new_node = Node(new_state, current_node)
                new_node.parent_operation = operation
                children.append(new_node)

            # loop through children
            for child in children:

                # child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # calculate f, g, and h values
                child.g = current_node.g + 1
                child.h = child.get_Astar_heuristic(child.state)
                child.f = child.g + child.h

                # child is already in the open list
                # can use hash table hear if run out of memory

                # add child to open list
                open_list.append(child)

        else:
            print('There are fewer solutions than the k specified')
            return self.Paths, self.Actions