import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from community import community_louvain
import seaborn as sns

# Load the data
nodes_df = pd.read_csv('nodes.csv')
edges_df = pd.read_csv('edges.csv')

# Create a NetworkX graph
G = nx.Graph()

# Add nodes with attributes
for _, row in nodes_df.iterrows():
    G.add_node(row['Id'], 
               country=row['Country'],
               continent=row['Continent'],
               order=row['Order'],
               age=row['Age'],
               weight=row['Weight'])

# Add edges with weights
for _, row in edges_df.iterrows():
    G.add_edge(row['Source'], row['Target'], weight=row['Weight'])

print("=== HÁLÓZATI ELEMZÉS ===")
print("\n1. ALAPVETŐ JELLEMZŐK:")
print(f"Csomópontok száma: {G.number_of_nodes()}")
print(f"Élek száma: {G.number_of_edges()}")
print(f"Átlagos fokszám: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
print(f"Hálózat átmérője: {nx.diameter(G)}")
print(f"Átlagos legrövidebb út: {nx.average_shortest_path_length(G):.2f}")
print(f"Klaszterezettségi együttható: {nx.average_clustering(G):.2f}")

print("\n2. LEGFONTOSABB KARDINÁLISOK:")
# Fokszám alapján
degree_centrality = nx.degree_centrality(G)
top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("\nLegmagasabb fokszámú kardinálisok:")
for node, centrality in top_degree:
    print(f"{node}: {centrality:.3f}")

# Közelségi központiság alapján
closeness_centrality = nx.closeness_centrality(G)
top_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("\nLegközelebbi kardinálisok (legrövidebb átlagos út):")
for node, centrality in top_closeness:
    print(f"{node}: {centrality:.3f}")

# Közvetítő központiság alapján
betweenness_centrality = nx.betweenness_centrality(G)
top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("\nLegfontosabb közvetítő kardinálisok:")
for node, centrality in top_betweenness:
    print(f"{node}: {centrality:.3f}")

print("\n3. KÖZÖSSÉGEK ELEMZÉSE:")
# Louvain módszerrel közösségek keresése
communities = community_louvain.best_partition(G)
num_communities = len(set(communities.values()))
print(f"Talált közösségek száma: {num_communities}")

# Közösségek méretének elemzése
community_sizes = pd.Series(communities.values()).value_counts()
print("\nKözösségek méretei:")
for comm_id, size in community_sizes.items():
    print(f"Közösség {comm_id}: {size} tag")

print("\n4. FÖLDRAJZI ELEMZÉS:")
# Kontinensek szerinti csoportosítás
continent_groups = {}
for node in G.nodes():
    continent = G.nodes[node]['continent']
    if continent not in continent_groups:
        continent_groups[continent] = []
    continent_groups[continent].append(node)

print("\nKontinensek szerinti eloszlás:")
for continent, nodes in continent_groups.items():
    print(f"{continent}: {len(nodes)} kardinális")

# Kontinensek közötti kapcsolatok
continent_edges = []
for u, v in G.edges():
    u_continent = G.nodes[u]['continent']
    v_continent = G.nodes[v]['continent']
    if u_continent != v_continent:
        continent_edges.append((u_continent, v_continent))

print("\nKontinensek közötti kapcsolatok száma:")
continent_connections = pd.Series(continent_edges).value_counts()
for (cont1, cont2), count in continent_connections.items():
    print(f"{cont1} - {cont2}: {count} kapcsolat")

print("\n5. ÉLETKOR ELEMZÉS:")
# Életkor szerinti csoportosítás
age_groups = {
    '70 alatt': [],
    '70-75': [],
    '75-80': [],
    '80 felett': []
}

for node in G.nodes():
    age = G.nodes[node]['age']
    if age < 70:
        age_groups['70 alatt'].append(node)
    elif age < 75:
        age_groups['70-75'].append(node)
    elif age < 80:
        age_groups['75-80'].append(node)
    else:
        age_groups['80 felett'].append(node)

print("\nÉletkor szerinti eloszlás:")
for group, nodes in age_groups.items():
    print(f"{group}: {len(nodes)} kardinális")

# Életkor és központiság kapcsolata
age_centrality = []
for node in G.nodes():
    age = G.nodes[node]['age']
    centrality = degree_centrality[node]
    age_centrality.append((age, centrality))

age_centrality_df = pd.DataFrame(age_centrality, columns=['Age', 'Centrality'])
print("\nÉletkor és központiság korrelációja:")
print(f"Korrelációs együttható: {age_centrality_df['Age'].corr(age_centrality_df['Centrality']):.3f}")

# Vizuálizációk
plt.figure(figsize=(15, 10))

# 1. Életkor eloszlás
plt.subplot(2, 2, 1)
sns.histplot(data=nodes_df, x='Age', bins=20)
plt.title('Kardinálisok életkorának eloszlása')

# 2. Kontinensek eloszlása
plt.subplot(2, 2, 2)
continent_counts = nodes_df['Continent'].value_counts()
plt.pie(continent_counts, labels=continent_counts.index, autopct='%1.1f%%')
plt.title('Kontinensek szerinti eloszlás')

# 3. Életkor és központiság kapcsolata
plt.subplot(2, 2, 3)
sns.scatterplot(data=age_centrality_df, x='Age', y='Centrality')
plt.title('Életkor és központiság kapcsolata')

# 4. Fokszám eloszlás
plt.subplot(2, 2, 4)
degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
plt.hist(degree_sequence, bins=20)
plt.title('Fokszám eloszlás')

plt.tight_layout()
plt.savefig('network_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("\nAz elemzés kész! A részletes vizualizációk a 'network_analysis.png' fájlban találhatók.") 