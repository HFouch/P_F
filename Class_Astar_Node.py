import copy
import numpy as np

class Node:

    def __init__(self, state=None, parent=None):
        self.state = state
        self.parent = parent
        self.parent_operation = None
        self.children = []

        self.h = 0
        self.g = 0
        self.f = 0

    def get_Astar_heuristic(self, adjacenciesB):
        adjacenciesA = self.state
        adjacenciesB = adjacenciesB

        counter = 0
        for adj in adjacenciesB:
            if adj not in adjacenciesA:
                counter += 1

        heuristic = counter / 2
        return heuristic


    def get_legal_operations(self, adjacenciesB):
        list_of_legal_operations = []
        adjacenciesA = self.state
        adjacenciesB = adjacenciesB

        for element in adjacenciesB:
            adjacenciesA_copy = copy.deepcopy(adjacenciesA)

            # if element is an adjacency:
            if type(element) is tuple:
                p = element[0]
                q = element[1]
                u = 0
                v = 0

                # if elements containing p and q respectively in a are adjacencies
                for marker in adjacenciesA_copy:
                    if type(marker) is tuple:
                        if marker[0] == p or marker[1] == p:
                            u = marker

                        if marker[0] == q or marker[1] == q:
                            v = marker

                # element containing p in A is a telomere
                if u == 0:
                    u = p
                # element containing q in A is a telomere
                if v == 0:
                    v = q

                if u != v:
                    adjacenciesA_copy.append((p, q))
                    adjacenciesA_copy.remove(u)
                    adjacenciesA_copy.remove(v)

                    # if u is an adjacency:
                    if type(u) is tuple:
                        # calcultate u'p
                        if u[0] == p:
                            u_not_p = u[1]
                        else:
                            u_not_p = u[0]

                        # if v is an adjacency:
                        if type(v) is tuple:
                            # calcultate v'q
                            if v[0] == q:
                                v_not_q = v[1]
                            else:
                                v_not_q = v[0]

                            adjacenciesA_copy.append((u_not_p, v_not_q))
                            operation = ((u, v), ((p, q), (u_not_p, v_not_q)))

                            # order operation before appending
                            op_1 = 0
                            op_2_1 = 0
                            op_2_2 = 0
                            op_2 = 0

                            if u[0] < v[0]:
                                op_1 = (u, v)
                            else:
                                op_1 = (v, u)
                            if p < q:
                                op_2_1 = (p, q)
                            else:
                                op_2_1 = (q, p)
                            if u_not_p < v_not_q:
                                op_2_2 = (u_not_p, v_not_q)
                            else:
                                op_2_2 = (v_not_q, u_not_p)
                            if op_2_1[0] < op_2_2[0]:
                                op_2 = (op_2_1, op_2_2)
                            else:
                                op_2 = (op_2_2, op_2_1)
                            ordered_operation = (op_1, op_2)

                            if ordered_operation not in list_of_legal_operations:
                                list_of_legal_operations.append((ordered_operation))
                            else:
                                pass


                        # else v is a telomere
                        else:
                            adjacenciesA_copy.append(u_not_p)
                            operation = ((u, v), ((p, q), (u_not_p)))
                            # if u[0] < v:
                            #    op_1 = (u, v)
                            # else:
                            #    op_1 = (v, u)
                            if p < q:
                                op_2_1 = (p, q)
                            else:
                                op_2_1 = (q, p)
                                # if op_2_1[0] < u_not_p:
                                op_2 = (op_2_1, u_not_p)
                            # else:
                            #    op_2 = (u_not_p, op_2_1)
                            op_2 = (op_2_1, u_not_p)
                            ordered_operation = ((u, v), op_2)

                            if ordered_operation not in list_of_legal_operations:
                                list_of_legal_operations.append((ordered_operation))
                            else:
                                pass


                    # else u is a telomere
                    else:
                        # if v is an adjacency
                        if type(v) is tuple:
                            # calculate v'q
                            if v[0] == q:
                                v_not_q = v[1]
                            else:
                                v_not_q = v[0]
                            adjacenciesA_copy.append(v_not_q)
                            operation = ((v, u), ((p, q), (v_not_q)))

                            if p < q:
                                op_2_1 = (p, q)
                            else:
                                op_2_1 = (q, p)

                            ordered_operation = ((v, u), (op_2_1, v_not_q))

                            if ordered_operation not in list_of_legal_operations:
                                list_of_legal_operations.append((ordered_operation))
                            else:
                                pass


                        # e;se v is a telomere
                        else:
                            operation = (u, v, ((p, q)))
                            if p < q:
                                op_2 = (p, q)
                            else:
                                op_2 = (q, p)
                            if u < v:
                                ordered_operation = (u, v, op_2)
                            else:
                                ordered_operation = (v, u, op_2)

                            if ordered_operation not in list_of_legal_operations:
                                list_of_legal_operations.append((ordered_operation))
                            else:
                                pass


            # else if the element is a telomere
            #elif type(element) is str:
            else:
                u = 0
                p = element

                for marker in adjacenciesA_copy:
                    if type(marker) is tuple:
                        if marker[0] == p or marker[1] == p:
                            u = marker

                if u == 0:
                    u = p

                # if u is not a telomere:
                if u != p:
                    adjacenciesA_copy.append(u[0])
                    adjacenciesA_copy.append(u[1])
                    adjacenciesA_copy.remove(u)
                    operation = ((u), (u[0]), (u[1]))
                    if operation not in list_of_legal_operations:
                        list_of_legal_operations.append((operation))
                    else:
                        pass

        return list_of_legal_operations


    def take_action(self, operation):
        state_copy = copy.deepcopy(self.state)

        # if it is a fusion or fission:

        if len(operation) == 3:

            # fission
            if type(operation[0]) is tuple:

                state_copy.remove(operation[0])
                state_copy.append(operation[1])
                state_copy.append(operation[2])

            # fusion
            else:
                state_copy.remove(operation[0])
                state_copy.remove(operation[1])

                # ensure gene extremities in correct order for downstream comparisions with genome B extremities
                if operation[2][0] < operation[2][1]:
                    state_copy.append(operation[2])
                else:
                    state_copy.append((operation[2][1], operation[2][0]))

        # else it is another rearrangment
        elif len(operation) == 2:
            # transpositions, balanced translcations and block interchanges:
            # if type(operation[0]) is tuple and type(operation[-1]) is tuple:
            if type(operation[0][0]) is tuple and type(operation[0][1]) is tuple:
                state_copy.remove(operation[0][0])
                state_copy.remove(operation[0][1])

                # ensure gene extremities in correct order for downstream comparision with genome B extremities

                if operation[1][0][0] < operation[1][0][1]:
                    state_copy.append(operation[1][0])
                else:
                    state_copy.append((operation[1][0][1], operation[1][0][0]))

                if operation[1][1][0] < operation[1][1][1]:
                    state_copy.append(operation[1][1])
                else:
                    state_copy.append((operation[1][1][1], operation[1][1][0]))



            # unbalanced translocations and intrachromosomal transpositions to end of chromosome
            elif type(operation[0][0]) is not tuple or type(operation[0][-1]) is not tuple:

                state_copy.remove(operation[0][0])
                state_copy.remove(operation[0][1])

                # ensure gene extremities in correct order for downstream comparisions with genome B extremities
                if operation[1][0][0] < operation[1][0][1]:
                    state_copy.append(operation[1][0])
                else:
                    state_copy.append((operation[1][0][1], operation[1][0][0]))

                state_copy.append(operation[1][1])


        else:
            # RAISE AN ERROR
            print("YOU'VE GOT A PROBLEM DARLING")

        # order and sort
        ordered_and_sorted = Node.order_and_sort(self, state_copy)

        return ordered_and_sorted


    def is_equivalent(self, adjacenciesB):
        adjacenciesA = copy.deepcopy(self.state)
        adjacenciesB = adjacenciesB

        ordered_adjacenciesA = []
        for element in adjacenciesA:
            if type(element) is tuple:
                if int(element[0]) < int(element[1]):
                    ordered_adjacenciesA.append(element)
                else:
                    ordered_adjacenciesA.append((element[1], element[0]))
            else:
                ordered_adjacenciesA.append(element)

        for element in adjacenciesB:
            if element in ordered_adjacenciesA:
                pass
            else:
                return False

        return True


    def order_adjacencies(self):
        ordered = []
        for element in self.state:
            if type(element) is tuple:
                if int(element[0]) < int(element[1]):
                    ordered.append(element)
                else:
                    ordered.append((element[1], element[0]))
            else:
                ordered.append(element)
        sort = []
        tuples = []
        not_tuples = []
        for element in ordered:
            if type(element) is tuple:
                tuples.append(element)
            else:
                not_tuples.append(element)
        for element in sorted(not_tuples):
            sort.append(element)
        for element in sorted(tuples):
            sort.append(element)

        self.state = sort

    def order_and_sort(self, adjacencies):
        ordered = []
        for element in adjacencies:
            if type(element) is tuple:
                if int(element[0]) < int(element[1]):
                    ordered.append(element)
                else:
                    ordered.append((element[1], element[0]))
            else:
                ordered.append(element)
        sort = []
        tuples = []
        not_tuples = []
        for element in ordered:
            if type(element) is tuple:
                tuples.append(element)
            else:
                not_tuples.append(element)
        for element in sorted(not_tuples):
            sort.append(element)
        for element in sorted(tuples):
            sort.append(element)

        return sort

    def get_Astar_heuristic(self, adjacenciesB):
        adjacenciesA = self.state
        adjacenciesB = adjacenciesB

        counter = 0
        for adj in adjacenciesB:
            if adj not in adjacenciesA:
                counter += 1

        heuristic = counter / 2
        return heuristic

