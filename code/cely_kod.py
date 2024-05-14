import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
from matplotlib.colors import LinearSegmentedColormap

graph = {}
nodes = set()
edges = []
#citanie suboru
with open('linky.txt','r',encoding="windows-1250") as file:
    for line in file:
        stanice = line.split(':  ')[1].strip('\n').split(';')
        linka =  line.split(':  ')[0]
        print(linka)
        for i,stanica in enumerate(stanice[:-1]):

            nodes.add(stanica)
            edges.append((stanice[i-1],stanica))
            if i != 0:
                try:
                    graph[stanice[i-1]][stanica] += 1
                except KeyError:
                    try:
                        graph[stanice[i-1]][stanica] = 1
                    except KeyError:
                        graph[stanice[i-1]] = {}
                        graph[stanice[i-1]][stanica] = 1

#pocty vrcholov, hran
n = len(nodes) 
m = len(edges)
print(n,m)

#orientovany graf
G = nx.DiGraph()
for node in graph:
    for neigbour in graph[node]:
        G.add_edges_from([(node,neigbour)], weight = graph[node][neigbour])

#orientovany graf s viacnasobnymi hranami
G2 = nx.MultiDiGraph()
for source, targets in graph.items():
    for target, weight in targets.items():
        for _ in range(weight):  # Add multiple edges if weight > 1
            G2.add_edge(source, target)

G.remove_edges_from(nx.selfloop_edges(G)) #vymazanie selfoops

### Vykreslenie grafu
plt.figure(figsize=(50, 50))
#pos = nx.bfs_layout(G, start="Riviéra")
#pos = nx.spring_layout(G)
pos = nx.kamada_kawai_layout(G)
node_opt = {"node_color":"black", "node_size":100}
edge_opt = {"edge_color":"green", "width":0.5}
nx.draw_networkx_nodes(G, pos, **node_opt)
nx.draw_networkx_edges(G, pos, **edge_opt)
node_labels = {node: node for node in G.nodes()}
#nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, font_color="black")
plt.show()


### Zakladne charakteristiky

print("Počet vrcholov:", G.number_of_nodes())
print("Počet hrán:", G.number_of_edges())

print("Priemerný stupeň vrchola:", sum(dict(G.degree()).values()) / G.number_of_nodes())

print("Hustota grafu:", nx.density(G))

print("Zhlukový koeficient:", nx.average_clustering(G))

strongly_connected_components = list(nx.strongly_connected_components(G))
print("Silne súvislé komponenty:")
print(len(strongly_connected_components))


#### ARTIKULACIE A MOSTY
bridges = list(nx.bridges(G.to_undirected()))  # Nájdenie mostov
articulation_points = list(nx.articulation_points(G.to_undirected()))  # Nájdenie artikulácií

plt.figure(figsize=(50, 50))

pos = nx.kamada_kawai_layout(G)
node_opt = {"node_color":"black", "node_size":100}
edge_opt = {"edge_color":"green", "width":0.5}
nx.draw_networkx_nodes(G, pos, **node_opt)
nx.draw_networkx_edges(G, pos, **edge_opt)
node_labels = {node: node for node in G.nodes()}
nx.draw_networkx_edges(G, pos, edgelist=bridges, edge_color='red', width=2)
nx.draw_networkx_nodes(G, pos, nodelist=articulation_points, node_color='orange', node_size=500)
nx.draw_networkx_labels(G, pos, font_size=5, font_family='sans-serif', font_color='black')

plt.show()




nx.closeness_centrality(G2)

print(nx.is_strongly_connected(G))
nx.number_strongly_connected_components(G)
nx.closeness_centrality(G)
a = dict(nx.shortest_path_length(G))
centrality = {}
for station in a:
    sum_dist = 0
    for neigbour in a[station]:
        sum_dist += a[station][neigbour]
    centrality[station] = sum_dist/n

minimal = float("inf")
maximal = 0
uzol = ""
koniec = ""
for station in centrality:
    if centrality[station] < minimal:
        minimal = centrality[station]
        uzol = station
    if centrality[station] > maximal:
        maximal = centrality[station]
        koniec = station
print(uzol, minimal)
print(koniec, maximal)
print(nx.closeness_centrality(G)['Račianske mýto'])
print(nx.closeness_centrality(G)['Hlavná stanica'])
print(nx.closeness_centrality(G)['Danubiana'])
print(nx.betweenness_centrality(G))
print(nx.degree_centrality(G))
print("artikulacie", list(nx.articulation_points(G.to_undirected())))
print("mosty", list(nx.bridges(G.to_undirected())))

#vykreslenie centrality st. vrchola
edge_labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])
dc = nx.degree_centrality(G)
node_importance_values = [dc[node] * (n-1) for node in G.nodes()]
print(node_importance_values)

colors = [(0, 'blue'), (0.5, 'green'), (0.75, 'yellow'), (1, 'red')]
custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors)

# vykreslenie a vypocet closeness centrality
closeness_centrality = nx.closeness_centrality(G)

node_colors = [closeness_centrality[node] for node in G.nodes()]

plt.figure(figsize=(100, 100))

pos = nx.kamada_kawai_layout(G)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw_networkx_labels(G, pos, font_size=5, font_family='sans-serif', font_color='black')

# vykresli
nodes = nx.draw(G, pos, node_color=node_colors, cmap=custom_cmap, node_size=[(np.log(val))*val * 50 for val in node_importance_values], edge_cmap=plt.cm.Reds)

# farby
dummy_mappable = plt.cm.ScalarMappable(cmap=custom_cmap)
dummy_mappable.set_array([]) 

#legenda
cbar = plt.colorbar(dummy_mappable)
cbar.set_label('Closeness Centrality')
plt.savefig("closeness.png")
#plt.show()


#### BIPARTITNY GRAF ####
Gb = nx.Graph()
line_counters = {}

with open('linky.txt', 'r') as file:
    for line in file:
        parts = line.strip().split(":")
        link_number = parts[0].strip()
        stops = [stop.strip() for stop in parts[1].split(";")][:-1]
        #print(stops)
        Gb.add_node(link_number, bipartite = 0)
        Gb.add_nodes_from(stops, bipartite = 1)
        for stop in stops:
            Gb.add_edge(link_number, stop)

nx.is_connected(Gb)
#Gb.nodes()
#connected_components = list(nx.connected_components(Gb))
#len(connected_components)
#connected_components
plt.figure(figsize=(50, 50))
pos = nx.bipartite_layout(Gb, nx.bipartite.sets(Gb)[0])
nx.draw(Gb, pos=pos, with_labels=True)
#plt.show()

least_transfer = {station: {} for station in G.nodes()}
for station1 in G.nodes():
    for station2 in G.nodes():
        if station1 != station2:
            path = find_shortest_path_with_transfers(Gb, station1, station2)
            least_transfer[station1][station2] = path
            least_transfer[station2][station1] = path[::-1]

number_of_transfers = {station: {} for station in G.nodes()}
for station1 in G.nodes():
    for station2 in G.nodes:
        number_of_transfers[station1][station2] = -1
        if station1 != station2:
            path = least_transfer[station1][station2]
            for element in path:
                try:
                    int(element)
                    number_of_transfers[station1][station2] += 1
                except ValueError:
                    continue
        else:
            number_of_transfers[station1][station2] = 0


print(least_transfer["Danubiana"]["Hrad Devín"])

trans = []
combinations = 0
sum_of_transfers = 0
for station1 in G.nodes():
    for station2 in G.nodes():
        value = number_of_transfers[station1][station2]
        sum_of_transfers +=  value
        trans.append(value)
        combinations += 1
print(sum_of_transfers/combinations)

unique_values = sorted(set(trans))

# sirka binu
bin_width = 1

#  histogram prestupy
plt.hist(trans, bins=[val - bin_width / 2 for val in unique_values] + [unique_values[-1] + bin_width / 2], align='mid', rwidth=0.8)
plt.xlabel('Počet prestupov')
plt.ylabel('Frekvencia')
plt.yscale("log")
plt.title('Frekvencia prestupov')
plt.xticks(unique_values)
#plt.show()

### PERKOLACIA ###
# Funkcia na získanie veľkosti najväčšej komponenty
def najvacsia_komponenta(graph):
    return len(max(nx.connected_components(graph), key=len))

# Pole pre ukladanie veľkostí najväčších komponent a podielov odstránených vrcholov
velkosti_komponent = []
podiely_funkcnych = []
G_un = G.to_undirected()
# Celkový počet vrcholov v grafe
pocet_vrcholov = len(G_un.nodes())

# Odstránenie vrcholov a zisťovanie veľkosti najväčšej komponenty a podielu odstránených vrcholov
while len(G_un.nodes()) > 0:
    velkosti_komponent.append(najvacsia_komponenta(G_un)/n)
    podiely_funkcnych.append( len(G_un.nodes()) / pocet_vrcholov)
    node_to_remove = list(G_un.nodes())[0]  # Môžete zvoliť vrchol podľa vášho výberu
    G_un.remove_node(node_to_remove)

# Výpis veľkostí najväčších komponent a podielov odstránených vrcholov po každom odstránení vrcholu
#print("Veľkosti najväčších komponent a podiely odstránených vrcholov:")
#for velkost, podiel in zip(velkosti_komponent, podiely_funkcnych):
 #   print("Veľkosť komponenty:", velkost, ", Podiel odstránených vrcholov:", podiel)

plt.plot(podiely_funkcnych, velkosti_komponent)
plt.xlabel("Podiel funkčných vrcholov")
plt.ylabel("Pravdepodobnosť, že vrchol patrí do max klastra")
plt.show()

# HISTOGRAM DISTR. STUPNOV
num_neighbors = {}
undirected_G = G.to_undirected()

# pocet susedov
for node in undirected_G.nodes():
    neighbors = len(list(undirected_G.neighbors(node)))
    num_neighbors[node] = neighbors

# Stupen kazdeho
degree_sequence = [num_neighbors[n] for n in num_neighbors]

# Plot
plt.figure(figsize=(20, 6))

plt.hist(degree_sequence, bins=range(max(degree_sequence) + 2), align='left', rwidth=0.8)
plt.xlabel('Degree')
plt.ylabel('Frequency')
plt.title('Degree Distribution')
plt.xticks(range(max(degree_sequence) + 1))
plt.yscale("log")

plt.grid(axis='y', alpha=0.75)
plt.show()