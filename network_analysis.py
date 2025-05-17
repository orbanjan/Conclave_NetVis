import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from community import community_louvain
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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

def analyze_network(edges_file='edges.csv', nodes_file='nodes.csv'):
    # Adatok betöltése
    edges_df = pd.read_csv(edges_file)
    nodes_df = pd.read_csv(nodes_file)
    
    # Hálózat létrehozása
    G = nx.Graph()
    
    # Csomópontok hozzáadása
    for _, row in nodes_df.iterrows():
        G.add_node(row['Id'], 
                   weight=row['Weight'],
                   country=row['Country'],
                   continent=row['Continent'],
                   order=row['Order'],
                   age=row['Age'])
    
    # Élek hozzáadása
    for _, row in edges_df.iterrows():
        G.add_edge(row['Source'], row['Target'], weight=row['Weight'])
    
    print(f"Hálózat statisztikái:")
    print(f"Csomópontok száma: {G.number_of_nodes()}")
    print(f"Élek száma: {G.number_of_edges()}")
    
    # Közösségi detektálás Louvain módszerrel
    communities = community_louvain.best_partition(G)
    
    # Közösségek számának kiírása
    n_communities = len(set(communities.values()))
    print(f"Detektált közösségek száma: {n_communities}")
    
    # Közösségi attribútum hozzáadása a csomópontokhoz
    nx.set_node_attributes(G, communities, 'community')
    
    # Közösségek méretének vizualizálása
    community_sizes = pd.Series(communities.values()).value_counts()
    plt.figure(figsize=(10, 6))
    community_sizes.plot(kind='bar')
    plt.title('Közösségek mérete')
    plt.xlabel('Közösség ID')
    plt.ylabel('Csomópontok száma')
    plt.savefig('community_sizes.png')
    plt.close()
    
    # Hálózat vizualizálása közösségekkel
    plt.figure(figsize=(15, 15))
    
    # Pozíciók számítása
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Csomópontok rajzolása közösségek szerint színezve
    node_colors = [communities[node] for node in G.nodes()]
    node_sizes = [G.nodes[node]['weight']/10 for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, 
                          node_color=node_colors,
                          node_size=node_sizes,
                          alpha=0.8)
    
    # Élek rajzolása
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, 
                          width=edge_weights,
                          alpha=0.2)
    
    # Címkék rajzolása
    nx.draw_networkx_labels(G, pos, 
                           font_size=8,
                           font_family='sans-serif')
    
    plt.title('Bíborosok hálózata közösségekkel')
    plt.axis('off')
    plt.savefig('network_visualization.png')
    plt.close()
    
    # Közösségi statisztikák
    community_stats = {}
    
    for community_id in set(communities.values()):
        # Közösséghez tartozó csomópontok
        community_nodes = [node for node, comm in communities.items() if comm == community_id]
        
        # Alhálózat létrehozása
        subgraph = G.subgraph(community_nodes)
        
        # Statisztikák számítása
        stats = {
            'size': len(community_nodes),
            'density': nx.density(subgraph),
            'avg_degree': sum(dict(subgraph.degree()).values()) / len(community_nodes),
            'avg_weight': np.mean([G.nodes[node]['weight'] for node in community_nodes]),
            'countries': len(set(G.nodes[node]['country'] for node in community_nodes)),
            'continents': len(set(G.nodes[node]['continent'] for node in community_nodes))
        }
        
        community_stats[community_id] = stats
    
    # Statisztikák DataFrame-be konvertálása
    stats_df = pd.DataFrame.from_dict(community_stats, orient='index')
    stats_df.index.name = 'Community'
    
    # Statisztikák mentése CSV-be
    stats_df.to_csv('community_stats.csv')
    
    # Közösségek jellemzőinek vizualizálása
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Sűrűség
    sns.barplot(x=stats_df.index, y='density', data=stats_df, ax=axes[0,0])
    axes[0,0].set_title('Közösségek sűrűsége')
    
    # Átlagos fokszám
    sns.barplot(x=stats_df.index, y='avg_degree', data=stats_df, ax=axes[0,1])
    axes[0,1].set_title('Átlagos fokszám')
    
    # Országok száma
    sns.barplot(x=stats_df.index, y='countries', data=stats_df, ax=axes[1,0])
    axes[1,0].set_title('Országok száma')
    
    # Kontinensek száma
    sns.barplot(x=stats_df.index, y='continents', data=stats_df, ax=axes[1,1])
    axes[1,1].set_title('Kontinensek száma')
    
    plt.tight_layout()
    plt.savefig('community_characteristics.png')
    plt.close()
    
    # Közösségek jellemzőinek korrelációja
    plt.figure(figsize=(10, 8))
    sns.heatmap(stats_df.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Közösségi jellemzők korrelációja')
    plt.savefig('community_correlations.png')
    plt.close()
    
    return G, communities, stats_df

if __name__ == "__main__":
    G, communities, stats_df = analyze_network() 