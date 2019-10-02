from Class_extremities_and_adjacencies import Extremities_and_adjacencies
from Class_Astar_algorithm import AstarAlgorithm

genomeA = [[1,-3,-2, 4, 6, 5, 7]]
genomeB = [[1, 2,3 ,4 , 5, 6, 7]]

#from genes to adjacencies
get_adjacencies = Extremities_and_adjacencies()
adjacencies_genomeA = get_adjacencies.adjacencies_ordered_and_sorted(genomeA)
adjacencies_genomeB = get_adjacencies.adjacencies_ordered_and_sorted(genomeB)

print('Adjacencies of the genomes: ')
print('Genome A: ', adjacencies_genomeA)
print('Genome B: ', adjacencies_genomeB)
print('____________________________________')
print()
print()

#run Astar
astar_algorithm = AstarAlgorithm(adjacencies_genomeA, adjacencies_genomeB)
a_star = astar_algorithm.astar(k=10)

paths = a_star[0]
actions = a_star[1]
print()
print('Astar paths: ')
for path in paths:
    print(path)
print()
print('___________________________________________')

print()
print()
print('Astar actions: ')
for action in actions:
    print(action)
print()
print("_____________________________________________")