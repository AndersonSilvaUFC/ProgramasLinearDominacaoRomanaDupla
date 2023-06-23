# Implementation of the ILP model DRDP-1'' from article:
# Integer Linear Programming Formulations for Double Roman Domination Problem
# Authors: Qingqiong Cai, Neng Fan, Yongtang Shi, Shunyu Yao
# ArXiV Link: https://arxiv.org/pdf/1902.07863.pdf

from ortools.linear_solver import pywraplp
import random

# create a solver using GLOP backend
msolver = pywraplp.Solver('double roman domination', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

# generate a Loupekine snark with k blocks
k = 9

# Número de vértices de ligação
z = 3

# Se True, vai gerar as arestas de ligação de forma direta ou cruzada de forma aleatória para cada aresta 
gera_arestas_ligacao_aleatorias = True

# Se True e a gera_arestas_ligacao_aleatorias False, vai gerar apenas arestas diretas
apenas_arestas_diretas = False

# Se True e as outras opções False, vai gerar apenas arestas cruzadas
apenas_arestas_cruzadas = True


edges = []


for i in range(0,k):
    # Arestas internas do bloco de construção
    edges.append([7*i + 0, 7*i + 1])
    edges.append([7*i + 0, 7*i + 2])
    edges.append([7*i + 1, 7*i + 3])
    edges.append([7*i + 2, 7*i + 5])
    edges.append([7*i + 2, 7*i + 6])
    edges.append([7*i + 3, 7*i + 4])
    edges.append([7*i + 3, 7*i + 6])
    edges.append([7*i + 4, 7*i + 5])

    # Arestas de ligação
    if gera_arestas_ligacao_aleatorias:
        if random.randint(0,1) == 0:
            edges.append([7*i + 1, + 7*( (i+1) % k ) ])
            edges.append([7*i + 5, + 7*( (i+1) % k ) + 4 ])
            print('arestas diretas')
        else:
            edges.append([7*i + 1, + 7*( (i+1) % k ) + 4 ])
            edges.append([7*i + 5, + 7*( (i+1) % k ) ])
            print ('arestas cruzadas')
    elif apenas_arestas_diretas:
        edges.append([7*i + 1, + 7*( (i+1) % k ) ])
        edges.append([7*i + 5, + 7*( (i+1) % k ) + 4 ])
    elif apenas_arestas_cruzadas:
        edges.append([7*i + 1, + 7*( (i+1) % k ) + 4 ])
        edges.append([7*i + 5, + 7*( (i+1) % k ) ])



# Adção dos vértices de ligação
j = 0
for i in range(0,z):
    edges.append([7*k + i, 7*j+6])
    edges.append([7*k + i, 7*(j+1)+6])
    edges.append([7*k + i, 7*(j+2)+6])
    j = j + 3

l = j
while l < k: 
    edges.append([7*l+6, 7*(l+1)+6])
    l =  l + 2

G = dict()

for e in edges:
    if e[0] not in G:
        G[e[0]] = []
    if e[1] not in G:
        G[e[1]] = []
    G[e[0]].append(e[1])
    G[e[1]].append(e[0])

edges = []

#define two lists of variables for the vertices of the graph
y = []
z = []
for i in range(0, len(G)):
    y.append(msolver.IntVar(0, 1, f'y_{i}'))
    z.append(msolver.IntVar(0, 1, f'z_{i}'))

# add constraints
for i in range(0, len(G)):
    vector = []
    vector.append(y[i])
    vector.append(z[i])
    for vertex in G[i]:
        vector.append((1/2)*y[vertex])
        vector.append(z[vertex])
    msolver.Add(sum(vector)>=1) # constraint for vertex i

# objective function
msolver.Minimize(2*sum(y)+3*sum(z))

# calculate the optimal solution
mstatus = msolver.Solve()

# if an optimal solution has been found, print results
if mstatus == pywraplp.Solver.OPTIMAL:
    print(f'Optimal function weight = {msolver.Objective().Value()}')
    print('Vertex Labels:')
    for v in range(0,len(G)):
        print(f'label of v_{v} = {2*y[v].solution_value()+3*z[v].solution_value()}')
else:
    print('The solver could not find an optimal solution')