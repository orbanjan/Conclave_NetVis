# Import necessary libraries
import pandas as pd
import networkx as nx
import community as community_louvain
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from collections import defaultdict

def analyze_clusters():
    # Load the network data
    edges_df = pd.read_csv('edges.csv')
    nodes_df = pd.read_csv('nodes.csv')
    
    # Create NetworkX graph
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
    
    # Közösségi detektálás Louvain módszerrel
    communities = community_louvain.best_partition(G)
    n_communities = len(set(communities.values()))
    
    print("\n2. KÖZÖSSÉGEK ELEMZÉSE:")
    print(f"Detektált közösségek száma: {n_communities}")
    
    # Közösségek méretének elemzése
    community_sizes = pd.Series(communities.values()).value_counts()
    print("\nKözösségek méretei:")
    for comm_id, size in community_sizes.items():
        print(f"Közösség {comm_id}: {size} tag")
    
    # Közösségi statisztikák
    community_stats = defaultdict(lambda: {
        'size': 0,
        'countries': set(),
        'continents': set(),
        'avg_age': 0,
        'cb_count': 0,
        'total_weight': 0,
        'internal_edges': 0,
        'external_edges': 0
    })
    
    # Közösségek jellemzőinek számítása
    for node in G.nodes():
        comm_id = communities[node]
        stats = community_stats[comm_id]
        
        # Alap statisztikák
        stats['size'] += 1
        stats['countries'].add(G.nodes[node]['country'])
        stats['continents'].add(G.nodes[node]['continent'])
        stats['avg_age'] += G.nodes[node]['age']
        if G.nodes[node]['order'] == 'CB':
            stats['cb_count'] += 1
        stats['total_weight'] += G.nodes[node]['weight']
        
        # Élek elemzése
        for neighbor in G.neighbors(node):
            if communities[neighbor] == comm_id:
                stats['internal_edges'] += 1
            else:
                stats['external_edges'] += 1
    
    # Átlagok számítása
    for comm_id in community_stats:
        stats = community_stats[comm_id]
        stats['avg_age'] /= stats['size']
        stats['countries'] = len(stats['countries'])
        stats['continents'] = len(stats['continents'])
        stats['cb_ratio'] = stats['cb_count'] / stats['size']
        stats['internal_ratio'] = stats['internal_edges'] / (stats['internal_edges'] + stats['external_edges'])
    
    # Statisztikák DataFrame-be konvertálása
    stats_df = pd.DataFrame.from_dict(community_stats, orient='index')
    stats_df.index.name = 'Community'
    
    print("\n3. KÖZÖSSÉGEK JELLEMZŐI:")
    print(stats_df)
    
    # Vizualizációk
    plt.style.use('seaborn-v0_8')  # Javított stílus
    
    # 1. Közösségek mérete
    plt.figure(figsize=(10, 6))
    community_sizes.plot(kind='bar')
    plt.title('Közösségek mérete')
    plt.xlabel('Közösség ID')
    plt.ylabel('Csomópontok száma')
    plt.savefig('community_sizes.png')
    plt.close()
    
    # 2. Közösségek jellemzői
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Átlagéletkor
    sns.barplot(x=stats_df.index, y='avg_age', data=stats_df, ax=axes[0,0])
    axes[0,0].set_title('Átlagéletkor')
    
    # CB arány
    sns.barplot(x=stats_df.index, y='cb_ratio', data=stats_df, ax=axes[0,1])
    axes[0,1].set_title('CB kardinálisok aránya')
    
    # Országok száma
    sns.barplot(x=stats_df.index, y='countries', data=stats_df, ax=axes[1,0])
    axes[1,0].set_title('Országok száma')
    
    # Belső kapcsolatok aránya
    sns.barplot(x=stats_df.index, y='internal_ratio', data=stats_df, ax=axes[1,1])
    axes[1,1].set_title('Belső kapcsolatok aránya')
    
    plt.tight_layout()
    plt.savefig('community_characteristics.png')
    plt.close()
    
    # 3. Korrelációs mátrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(stats_df.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Közösségi jellemzők korrelációja')
    plt.savefig('community_correlations.png')
    plt.close()
    
    # 4. Hálózat vizualizáció közösségekkel
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
    
    print("\nAz elemzés kész! A vizualizációk a következő fájlokban találhatók:")
    print("- community_sizes.png")
    print("- community_characteristics.png")
    print("- community_correlations.png")
    print("- network_visualization.png")

if __name__ == "__main__":
    analyze_clusters() 