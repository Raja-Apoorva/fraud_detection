# Import necessary libraries
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

# transaction data
data = {
    'source_account': ['John', 'John', 'Smith', 'Rob', 'Taylor', 'Mike', 'Stacey', 'Kim', 'Reed', 'Mark'],
    'target_account': ['Smith', 'Rob', 'Taylor', 'Mike', 'John', 'Stacey', 'Kim', 'Reed', 'Mark', 'Justin'],
    'transaction_amount': [100, 150, 200, 250, 300, 350, 400, 450, 500, 550],
    'transaction_date': pd.date_range(start='2024-01-01', periods=10, freq='D')
}

# Create a DataFrame
df = pd.DataFrame(data)

# Preview the data
print("Transaction Data:")
print(df)

# Build the transaction graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for idx, row in df.iterrows():
    G.add_edge(row['source_account'], row['target_account'], amount=row['transaction_amount'])

# Analyze the graph
# 1. Detect communities using connected components (for undirected graphs)
# For directed graphs, we can use strongly connected components
communities = list(nx.strongly_connected_components(G))
print("\nStrongly Connected Components (Potential Fraud Networks):")
for idx, community in enumerate(communities):
    print(f"Community {idx+1}: {community}")

# 2. Calculate centrality measures
pagerank = nx.pagerank(G, alpha=0.85)
print("\nPageRank Centrality:")
for node, score in pagerank.items():
    print(f"Node {node}: {score:.4f}")

# 3. Identify nodes with high in-degree and out-degree
in_degrees = dict(G.in_degree())
out_degrees = dict(G.out_degree())
print("\nNodes with High In-Degree (Potential Money Mules):")
high_in_degree = [node for node, degree in in_degrees.items() if degree > 1]
print(high_in_degree)

print("\nNodes with High Out-Degree (Potential Fraud Sources):")
high_out_degree = [node for node, degree in out_degrees.items() if degree > 1]
print(high_out_degree)

# Visualize the graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, k=0.5)
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1500)
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20)
nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
edge_labels = nx.get_edge_attributes(G, 'amount')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Transaction Network Graph")
plt.axis('off')
plt.savefig('results.png')
