import pandas as pd
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

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

# Create an interactive visualization using pyvis
net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="black")

# Add nodes with custom properties
for node in G.nodes():
    node_data = G.nodes[node]
    net.add_node(node,
                label=node,
                title=f"Country: {node_data['country']}<br>Continent: {node_data['continent']}<br>Age: {node_data['age']}",
                size=node_data['weight']/50)  # Scale node size based on weight

# Add edges
for edge in G.edges(data=True):
    net.add_edge(edge[0], edge[1], value=edge[2]['weight'])

# Set the physics layout
net.set_options("""
{
  "physics": {
    "forceAtlas2Based": {
      "gravitationalConstant": -50,
      "centralGravity": 0.01,
      "springLength": 100,
      "springConstant": 0.08
    },
    "maxVelocity": 50,
    "solver": "forceAtlas2Based",
    "timestep": 0.35,
    "stabilization": {
      "enabled": true,
      "iterations": 1000
    }
  }
}
""")

# Save the interactive visualization
net.save_graph("conclave_network.html")

# Create a static visualization using matplotlib
plt.figure(figsize=(15, 15))
pos = nx.spring_layout(G, k=1, iterations=50)
nx.draw(G, pos,
        with_labels=True,
        node_color='lightblue',
        node_size=[G.nodes[node]['weight']/10 for node in G.nodes()],
        font_size=8,
        font_weight='bold',
        edge_color='gray',
        width=[G[u][v]['weight']/5 for u,v in G.edges()],
        alpha=0.7)

plt.title("Conclave Network Visualization")
plt.savefig("conclave_network_static.png", dpi=300, bbox_inches='tight')
plt.close()

print("Visualization files have been created:")
print("1. conclave_network.html - Interactive visualization")
print("2. conclave_network_static.png - Static visualization") 